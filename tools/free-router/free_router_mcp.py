"""Free LLM worker router, an MCP server for Claude Code (and Cursor).

Claude stays the supervisor: this server only hands a prompt to a free worker model and returns its text,
prefixed with `[WORKER: <provider>/<model>]`. Providers without an API key are skipped; HTTP 429, timeouts and
errors fail over to the next provider in the tier. Keys load from ~/.claude/mcp/.env when present.

Run: uv run --with mcp --with openai --with python-dotenv python free_router_mcp.py
"""
from __future__ import annotations

import concurrent.futures as cf
import os
import pathlib
import re
import time

HERE = pathlib.Path(__file__).resolve().parent
try:
    from dotenv import load_dotenv

    load_dotenv(HERE / ".env", override=False)
except ImportError:  # still works with keys in the real environment
    pass

def _load_tiers() -> dict:
    """Tiers from providers.json (next to this file, or the path in FREE_ROUTER_PROVIDERS)."""
    import json

    path = pathlib.Path(os.environ.get("FREE_ROUTER_PROVIDERS") or HERE / "providers.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    return {tier: [{k: p[k] for k in ("name", "base_url", "env", "model")} for p in chain]
            for tier, chain in data["tiers"].items()}


TIERS = _load_tiers()
KEY_ENVS = sorted({p["env"] for chain in TIERS.values() for p in chain})
LOG = HERE / "router.log"
FAST_MAX_TOKENS = 3000      # above this, 'fast' moves up so Groq's daily token cap is not drained
RUNAWAY_TOKENS = 60000      # above this, prompts are cut unless tier == 'context'
TIMEOUT_S = float(os.environ.get("FREE_ROUTER_TIMEOUT", "90"))
MAX_TOKENS = int(os.environ.get("FREE_ROUTER_MAX_TOKENS", "4096"))

# Prompts that look like they carry credentials never leave the machine.
_SECRET_PATTERNS = [r"sk-[A-Za-z0-9_-]{16,}", r"sk-ant-[A-Za-z0-9_-]{16,}", r"gh[pousr]_[A-Za-z0-9]{20,}",
                    r"AIza[0-9A-Za-z_-]{20,}", r"AQ\.[A-Za-z0-9_-]{40,}", r"gsk_[A-Za-z0-9]{16,}", r"nvapi-[A-Za-z0-9_-]{16,}",
                    r"AKIA[0-9A-Z]{16}", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"]


def _key_values():
    return [os.environ[e] for e in KEY_ENVS if os.environ.get(e)]


def _redact(text: str) -> str:
    for v in _key_values():
        if len(v) >= 8:
            text = text.replace(v, "***")
    for pat in _SECRET_PATTERNS:
        text = re.sub(pat, "***", text)
    return text


def _has_secret(prompt: str) -> bool:
    return any(v and len(v) >= 8 and v in prompt for v in _key_values()) or \
        any(re.search(p, prompt) for p in _SECRET_PATTERNS)


def _call_openai(provider: dict, prompt: str, timeout: float) -> str:
    from openai import OpenAI

    client = OpenAI(base_url=provider["base_url"], api_key=os.environ[provider["env"]], timeout=timeout,
                    max_retries=0)
    r = client.chat.completions.create(model=provider["model"], max_tokens=MAX_TOKENS,
                                       messages=[{"role": "user", "content": prompt}])
    text = (r.choices[0].message.content or "").strip()
    if not text:
        raise RuntimeError("empty reply")
    return text


def _candidates(tier: str, preferred_model: str = "") -> list[dict]:
    if tier not in TIERS:
        raise ValueError(f"unknown tier {tier!r}; use one of {sorted(TIERS)}")
    chain = [p for p in TIERS[tier] if os.environ.get(p["env"])]
    if preferred_model:
        pref = [p for t in TIERS.values() for p in t if p["model"] == preferred_model and os.environ.get(p["env"])]
        chain = pref[:1] + [p for p in chain if p["model"] != preferred_model]
    return chain


def _label(p: dict) -> str:
    return f"{p['name']}/{p['model']}"


def _why(e: Exception) -> str:
    code = getattr(e, "status_code", None)
    kind = "rate limited (429)" if code == 429 else f"HTTP {code}" if code else type(e).__name__
    return _redact(f"{kind}: {str(e)[:200]}")


def approx_tokens(text: str) -> int:
    return len(text) // 4


def _log(label: str, tier: str, tok_in: int, tok_out: int, ok: bool, note: str = "") -> None:
    """One line per call: time, tier, worker, token estimates. Never the prompt or the answer."""
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} tier={tier} worker={label} tok_in={tok_in} "
                    f"tok_out={tok_out} ok={ok} {note}".rstrip() + "\n")
    except OSError:
        pass  # logging must never break a call


def _guard(task_prompt: str, tier: str) -> tuple[str, str, list[str]]:
    """Token-size guard: big 'fast' prompts move up (Groq has a daily token cap); runaway prompts are cut."""
    notes, tok = [], approx_tokens(task_prompt)
    if tier == "fast" and tok > FAST_MAX_TOKENS:
        tier = "context" if any(os.environ.get(p["env"]) for p in TIERS["context"]) else "heavy_code"
        notes.append(f"upgraded fast -> {tier} (~{tok} tokens > {FAST_MAX_TOKENS})")
    if tier != "context" and tok > RUNAWAY_TOKENS:
        task_prompt = task_prompt[: RUNAWAY_TOKENS * 4]
        notes.append(f"WARNING: prompt truncated from ~{tok} to ~{RUNAWAY_TOKENS} tokens (use tier='context')")
    return task_prompt, tier, notes


def route(task_prompt: str, tier: str = "heavy_code", preferred_model: str = "", caller=_call_openai) -> str:
    """Try each provider in the tier in order; return the first answer, prefixed with the worker and tokens."""
    _candidates(tier)  # validate the tier first
    if _has_secret(task_prompt):
        return "[WORKER: none] Refused: the prompt seems to contain a secret or API key. Remove it and retry."
    task_prompt, tier, notes = _guard(task_prompt, tier)
    chain = _candidates(tier, preferred_model)
    if not chain:
        return f"[WORKER: none] No provider in tier {tier!r} has an API key set: no API key found " \
               "(see .env.example next to the router)."
    tok_in, errors = approx_tokens(task_prompt), []
    head = "".join(f"({n})\n" for n in notes)
    for p in chain:
        try:
            answer = caller(p, task_prompt, TIMEOUT_S)
            _log(_label(p), tier, tok_in, approx_tokens(answer), True, "; ".join(notes))
            return f"[WORKER: {_label(p)} | ~{tok_in} tok]\n{head}{answer}"
        except Exception as e:  # 429, timeout, auth, bad model: fail over
            _log(_label(p), tier, tok_in, 0, False, _why(e)[:80])
            errors.append(f"- {_label(p)}: {_why(e)}")
    return "[WORKER: none] Every provider failed:\n" + head + "\n".join(errors)


def fanout(task_prompt: str, tier: str = "heavy_code", caller=_call_openai) -> str:
    """Ask up to 2 available workers in parallel, for comparing answers on critical tasks."""
    chain = _candidates(tier)
    if _has_secret(task_prompt):
        return "[WORKER: none] Refused: the prompt seems to contain a secret or API key. Remove it and retry."
    if not chain:
        return f"[WORKER: none] No provider in tier {tier!r} has an API key set."

    tok_in = approx_tokens(task_prompt)

    def one(p):
        try:
            answer = caller(p, task_prompt, TIMEOUT_S)
            _log(_label(p), tier, tok_in, approx_tokens(answer), True, "fanout")
            return f"[WORKER: {_label(p)} | ~{tok_in} tok]\n{answer}"
        except Exception as e:
            _log(_label(p), tier, tok_in, 0, False, "fanout")
            return f"[WORKER: {_label(p)} | ~{tok_in} tok] FAILED: {_why(e)}"

    with cf.ThreadPoolExecutor(max_workers=2) as ex:
        results = list(ex.map(one, chain[:2]))
    return "\n\n---\n\n".join(results)


def verify(caller=_call_openai) -> list[dict]:
    """One tiny real call per configured model with a key: which ones answer today. Never prints keys."""
    rows = []
    for tier, chain in TIERS.items():
        for p in chain:
            if not os.environ.get(p["env"]):
                rows.append({"tier": tier, "model": _label(p), "ok": False, "why": "no key"})
                continue
            t = time.time()
            try:
                caller(p, "Reply with just: OK", 60)
                rows.append({"tier": tier, "model": p["model"], "label": _label(p), "ok": True, "why": "",
                             "seconds": round(time.time() - t, 1)})
            except Exception as e:  # report and go on
                rows.append({"tier": tier, "model": p["model"], "label": _label(p), "ok": False, "why": _why(e)})
    return rows


def _build_server():
    try:  # MCP Python SDK 2.x renamed FastMCP to MCPServer
        from mcp.server.mcpserver import MCPServer as Server
    except ImportError:  # SDK 1.x
        from mcp.server.fastmcp import FastMCP as Server

    mcp = Server("free-router")

    @mcp.tool()
    def delegate_to_worker(task_prompt: str, tier: str = "heavy_code", preferred_model: str = "") -> str:
        """Send a self-contained sub-task to a free worker LLM. tier: heavy_code (complex code, debugging),
        context (large files, summaries, docs) or fast (tests, boilerplate, regex). Never include secrets,
        .env contents or private/client data. Review the answer before using it."""
        return route(task_prompt, tier, preferred_model)

    @mcp.tool()
    def fanout_workers(task_prompt: str, tier: str = "heavy_code") -> str:
        """Ask two free workers the same task in parallel to compare answers on critical work. Same data
        rules as delegate_to_worker."""
        return fanout(task_prompt, tier)

    return mcp


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:  # python free_router_mcp.py --verify
        for r in verify():
            mark = f"OK   {r.get('seconds', '')}s" if r["ok"] else f"FAIL {r['why'][:90]}"
            print(f"{r['tier']:10} {r.get('label', r['model']):55} {mark}")
        print(f"Set 'status' in providers.json to 'verified {time.strftime('%Y-%m-%d')}' for the OK rows.")
    else:
        _build_server().run()
