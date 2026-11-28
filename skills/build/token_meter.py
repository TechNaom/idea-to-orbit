"""Token meter: what the AI builders used, and what was saved.

Reads Claude Code session logs (a project folder under ~/.claude/projects, with each session's
subagents) and reports tokens by agent, task, role, model and day. It reads only the usage counts,
the model, the time and each subagent's short description: never prompt or file contents.

    python token_meter.py <project folder> [--session ID] [--prices prices.json]
        [--sizes T1=M,T2=S] [--budget S=60000,M=150000] [--baseline S=120000,M=180000] [--ledger]

Costs appear only with a prices file you keep (per million tokens, with its date); nothing is
guessed. Plain Python 3.10+, no dependencies.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

KINDS = ("input", "output", "cache_write", "cache_read")
USAGE_KEYS = {"input": "input_tokens", "output": "output_tokens",
              "cache_write": "cache_creation_input_tokens", "cache_read": "cache_read_input_tokens"}
TASK = re.compile(r"\bT\d+\b")


@dataclass
class Run:
    agent: str                      # "main" or the subagent's id
    description: str = ""
    input: int = 0
    output: int = 0
    cache_write: int = 0
    cache_read: int = 0
    replies: int = 0
    models: set = field(default_factory=set)
    by_model: dict = field(default_factory=dict)   # model -> {kind: tokens}
    first_day: str = ""

    @property
    def total(self) -> int:
        return self.input + self.output + self.cache_write + self.cache_read

    @property
    def fresh(self) -> int:
        """New tokens: everything except cache reads, which re-read the context at a far lower price."""
        return self.input + self.output + self.cache_write

    @property
    def tasks(self) -> list[str]:
        return list(dict.fromkeys(TASK.findall(self.description)))

    @property
    def role(self) -> str:
        if self.agent == "main":
            return "supervisor"
        d = self.description.lower()
        if re.search(r"\b(check|review|cold read|verify)\b", d):
            return "check"
        if re.search(r"\bbuild", d):
            return "builder"
        return "other"

    @property
    def model(self) -> str:
        return ", ".join(sorted(self.models)) or "unknown"


def read_run(path: Path, agent: str, description: str = "") -> Run:
    run, seen = Run(agent, description), set()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        msg = row.get("message") if isinstance(row, dict) else None
        usage = msg.get("usage") if isinstance(msg, dict) else None
        if not isinstance(usage, dict):
            continue
        key = msg.get("id") or row.get("requestId") or row.get("uuid")
        if key in seen:  # one reply can be written as several lines
            continue
        seen.add(key)
        model = msg.get("model") or "unknown"
        if model == "<synthetic>":  # written by the harness itself, not a model reply
            continue
        per = run.by_model.setdefault(model, dict.fromkeys(KINDS, 0))
        for kind, name in USAGE_KEYS.items():
            n = int(usage.get(name) or 0)
            setattr(run, kind, getattr(run, kind) + n)
            per[kind] += n
        run.replies += 1
        run.models.add(model)
        day = str(row.get("timestamp", ""))[:10]
        if day and (not run.first_day or day < run.first_day):
            run.first_day = day
    return run


def scan(project: Path, session: str | None = None) -> list[Run]:
    """Every session in a project folder (or one), with its subagents."""
    runs = []
    for log in sorted(Path(project).glob("*.jsonl")):
        if session and log.stem != session:
            continue
        runs.append(read_run(log, "main"))
        sub = log.with_suffix("") / "subagents"
        for alog in sorted(sub.glob("agent-*.jsonl")):
            meta, desc = alog.with_suffix(".meta.json"), ""
            if meta.exists():
                try:
                    desc = str(json.loads(meta.read_text(encoding="utf-8")).get("description", ""))
                except ValueError:
                    pass
            runs.append(read_run(alog, alog.stem.removeprefix("agent-"), desc))
    return runs


def per_task(runs: list[Run], measure: str = "fresh") -> dict[str, float]:
    """Agent tokens per task ("fresh" or "total"); a run shared by several tasks is split evenly."""
    out: dict[str, float] = {}
    for r in runs:
        for t in r.tasks:
            out[t] = out.get(t, 0) + getattr(r, measure) / len(r.tasks)
    return out


def lean_savings(per: dict, sizes: dict, baseline: dict) -> dict[str, float]:
    """Tokens saved per task against a measured full-loop average for its size."""
    return {t: baseline[sizes[t]] - n for t, n in per.items() if sizes.get(t) in baseline}


def budget_flags(per: dict, sizes: dict, budget: dict) -> dict[str, str]:
    out = {}
    for t, n in per.items():
        cap = budget.get(sizes.get(t, ""))
        if not cap:
            continue
        pct = round(100 * n / cap)
        if n > cap:
            out[t] = f"over: {pct}% of {cap:,}"
        elif n >= 0.8 * cap:
            out[t] = f"warning: {pct}% of {cap:,}"
    return out


def summary(runs: list[Run], prices: dict | None = None) -> dict:
    s = {k: sum(getattr(r, k) for r in runs) for k in KINDS}
    s["total"] = sum(s[k] for k in KINDS)
    s["cost"], s["by_model_cost"], s["cache_saved_cost"] = None, {}, {}
    if prices:
        table = prices.get("per_million", {})
        for r in runs:
            for model, t in r.by_model.items():
                p = table.get(model)
                if not p:
                    continue
                cost = sum(t[k] * p.get(k, 0) for k in KINDS) / 1e6
                s["by_model_cost"][model] = s["by_model_cost"].get(model, 0) + cost
                saved = t["cache_read"] * (p.get("input", 0) - p.get("cache_read", 0)) / 1e6
                s["cache_saved_cost"][model] = s["cache_saved_cost"].get(model, 0) + saved
        s["cost"] = sum(s["by_model_cost"].values())
    return s


def ledger_rows(runs: list[Run]) -> str:
    """Rows for token-ledger.md: date, tasks, role, model, all tokens, fresh tokens."""
    lines = []
    for r in runs:
        tasks = ", ".join(r.tasks) or "-"
        lines.append(f"| {r.first_day or '-'} | {tasks} | {r.role} | {r.model} | {r.total:,} | {r.fresh:,} |")
    return "\n".join(lines) + "\n"


def report(runs: list[Run], prices: dict | None = None, sizes: dict | None = None,
           budget: dict | None = None, baseline: dict | None = None) -> str:
    s = summary(runs, prices)
    out = [f"Agents: {len(runs)}. Tokens: {s['total']:,} (input {s['input']:,}, output {s['output']:,}, "
           f"cache write {s['cache_write']:,}, cache read {s['cache_read']:,}).",
           f"Fresh tokens (input, output and cache writes): {s['input'] + s['output'] + s['cache_write']:,}. "
           f"Served from the prompt cache: {s['cache_read']:,} "
           f"({100 * s['cache_read'] / max(s['total'], 1):.0f}% of all; budgets count fresh tokens)."]
    if prices:
        out.append(f"API-equivalent cost: ${s['cost']:.2f}; saved by the cache: "
                   f"${sum(s['cache_saved_cost'].values()):.2f} (prices as of {prices.get('as_of', 'unknown')}).")
    else:
        out.append("Cost: tokens only (no prices file given).")
    out += ["", "| Agent | Role | Tasks | Model | Fresh tokens | All tokens |", "|---|---|---|---|---|---|"]
    for r in sorted(runs, key=lambda r: -r.fresh):
        out.append(f"| {r.agent} | {r.role} | {', '.join(r.tasks) or '-'} | {r.model} | {r.fresh:,} | {r.total:,} |")
    per = per_task(runs)
    if per:
        out += ["", "| Task | Agent fresh tokens | Budget | Saved vs full loop |", "|---|---|---|---|"]
        flags = budget_flags(per, sizes or {}, budget or {})
        saved = lean_savings(per, sizes or {}, baseline or {})
        for t in sorted(per, key=lambda x: int(x[1:])):
            sv = f"{saved[t]:,.0f}" if t in saved else "-"
            out.append(f"| {t} | {per[t]:,.0f} | {flags.get(t, 'ok' if budget else '-')} | {sv} |")
    return "\n".join(out) + "\n"


def _pairs(text: str | None, cast=int) -> dict:
    return {k: cast(v) for k, v in (p.split("=", 1) for p in text.split(","))} if text else {}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("project", type=Path)
    ap.add_argument("--session")
    ap.add_argument("--prices", type=Path)
    ap.add_argument("--sizes")
    ap.add_argument("--budget")
    ap.add_argument("--baseline")
    ap.add_argument("--ledger", action="store_true", help="print ledger rows only")
    a = ap.parse_args(argv)
    runs = scan(a.project, a.session)
    if not runs:
        print("No session logs found.", file=sys.stderr)
        return 1
    if a.ledger:
        sys.stdout.write(ledger_rows(runs))
        return 0
    prices = json.loads(a.prices.read_text(encoding="utf-8")) if a.prices else None
    sys.stdout.write(report(runs, prices, _pairs(a.sizes, str), _pairs(a.budget), _pairs(a.baseline)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
