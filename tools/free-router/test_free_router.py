"""Tests for free_router_mcp: fakes only, no network. Run from the repo root: pytest -q tools/free-router (needs mcp, openai, python-dotenv, pytest)"""
import importlib.util
import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
import os

# Behaviour tests route over a fixed test list, so they never break when providers.json changes.
os.environ["FREE_ROUTER_PROVIDERS"] = str(HERE / "test_providers.json")
spec = importlib.util.spec_from_file_location("free_router_mcp", HERE / "free_router_mcp.py")
fr = importlib.util.module_from_spec(spec)
sys.modules["free_router_mcp"] = fr
spec.loader.exec_module(fr)


class RateLimited(Exception):
    status_code = 429


def fake_caller(script):
    """script: {model: reply or Exception}; records calls."""
    calls = []

    def call(provider, prompt, timeout):
        calls.append(provider["model"])
        r = script.get(provider["model"], RuntimeError("unexpected"))
        if isinstance(r, Exception):
            raise r
        return r
    return call, calls


@pytest.fixture
def env(monkeypatch, tmp_path):
    monkeypatch.setattr(fr, "LOG", tmp_path / "router.log")
    for k in ("GEMINI_API_KEY", "NVIDIA_NIM_API_KEY", "GROQ_API_KEY", "OPENROUTER_API_KEY"):
        monkeypatch.setenv(k, "fake")
    return monkeypatch


def test_first_provider_answers_with_prefix(env):
    call, calls = fake_caller({"deepseek-ai/deepseek-v3.2": "ok"})
    out = fr.route("hi", "heavy_code", "", caller=call)
    assert out.startswith("[WORKER: nvidia-nim/deepseek-ai/deepseek-v3.2 | ~")
    assert calls == ["deepseek-ai/deepseek-v3.2"]


def test_fails_over_on_429_and_errors(env):
    call, calls = fake_caller({"deepseek-ai/deepseek-v3.2": RateLimited("429"),
                               "qwen/qwen3-coder:free": TimeoutError("slow"),
                               "gemini-2.5-pro": "third"})
    out = fr.route("hi", "heavy_code", "", caller=call)
    assert "[WORKER: google-ai-studio/gemini-2.5-pro | ~" in out and out.endswith("third")
    assert len(calls) == 3


def test_skips_providers_without_key(env):
    env.delenv("NVIDIA_NIM_API_KEY")
    call, calls = fake_caller({"qwen/qwen3-coder:free": "ok"})
    fr.route("hi", "heavy_code", "", caller=call)
    assert calls == ["qwen/qwen3-coder:free"]


def test_all_fail_reports_each_without_secrets(env):
    env.setenv("GROQ_API_KEY", "gsk_supersecretvalue123")
    call, _ = fake_caller({"openai/gpt-oss-120b": RuntimeError("bad key gsk_supersecretvalue123"),
                           "qwen/qwen3.8-27b": RateLimited("429"),
                           "gemini-2.5-flash-lite": RateLimited("429")})
    out = fr.route("hi", "fast", "", caller=call)
    assert out.startswith("[WORKER: none]") and "gsk_supersecretvalue123" not in out
    assert out.count("groq") >= 2


def test_preferred_model_goes_first(env):
    call, calls = fake_caller({"gemini-2.5-pro": "pro"})
    fr.route("hi", "heavy_code", "gemini-2.5-pro", caller=call)
    assert calls[0] == "gemini-2.5-pro"


def test_unknown_tier_is_an_error(env):
    with pytest.raises(ValueError):
        fr.route("hi", "nope", "", caller=lambda *a: "x")


def test_no_keys_at_all(monkeypatch):
    for k in ("GEMINI_API_KEY", "NVIDIA_NIM_API_KEY", "GROQ_API_KEY", "OPENROUTER_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    out = fr.route("hi", "fast", "", caller=lambda *a: "x")
    assert out.startswith("[WORKER: none]") and "no API key" in out


def test_fanout_uses_two_distinct_workers(env):
    call, calls = fake_caller({"deepseek-ai/deepseek-v3.2": "a", "qwen/qwen3-coder:free": "b", "gemini-2.5-pro": "c"})
    out = fr.fanout("hi", "heavy_code", caller=call)
    assert "[WORKER: nvidia-nim/deepseek-ai/deepseek-v3.2 | ~" in out
    assert "[WORKER: openrouter/qwen/qwen3-coder:free | ~" in out
    assert sorted(calls) == ["deepseek-ai/deepseek-v3.2", "qwen/qwen3-coder:free"]


def test_secret_guard_refuses_prompts_with_keys(env):
    env.setenv("GEMINI_API_KEY", "AIzaFakeKeyValue000111222")
    out = fr.route("here is my key AIzaFakeKeyValue000111222 fix it", "fast", "", caller=lambda *a: "x")
    assert out.startswith("[WORKER: none]") and "secret" in out.lower()


def test_big_fast_prompt_is_upgraded(env, tmp_path, monkeypatch):
    monkeypatch.setattr(fr, "LOG", tmp_path / "router.log")
    call, calls = fake_caller({"gemini-2.5-flash": "ctx"})
    out = fr.route("x" * 4 * 3001, "fast", "", caller=call)
    assert calls == ["gemini-2.5-flash"] and "upgraded" in out


def test_small_fast_prompt_stays_fast(env, tmp_path, monkeypatch):
    monkeypatch.setattr(fr, "LOG", tmp_path / "router.log")
    call, calls = fake_caller({"openai/gpt-oss-120b": "ok"})
    out = fr.route("x" * 4 * 100, "fast", "", caller=call)
    assert calls == ["openai/gpt-oss-120b"] and "| ~100 tok]" in out


def test_runaway_prompt_truncated_except_context(env, tmp_path, monkeypatch):
    monkeypatch.setattr(fr, "LOG", tmp_path / "router.log")
    seen = []
    def call(p, prompt, timeout):
        seen.append(len(prompt)); return "ok"
    out = fr.route("y" * 4 * 70000, "heavy_code", "", caller=call)
    assert seen[0] <= 4 * 60000 and "truncated" in out
    seen.clear()
    fr.route("y" * 4 * 70000, "context", "", caller=call)
    assert seen[0] == 4 * 70000


def test_log_records_provider_and_tokens_not_prompt(env, tmp_path, monkeypatch):
    log = tmp_path / "router.log"
    monkeypatch.setattr(fr, "LOG", log)
    call, _ = fake_caller({"deepseek-ai/deepseek-v3.2": "answer"})
    fr.route("private prompt text here", "heavy_code", "", caller=call)
    line = log.read_text(encoding="utf-8")
    assert "nvidia-nim/deepseek-ai/deepseek-v3.2" in line and "tok_in=" in line
    assert "private prompt text" not in line


def test_server_lists_both_tools():
    import asyncio
    s = fr._build_server()
    names = sorted(t.name for t in asyncio.run(s.list_tools()))
    assert names == ["delegate_to_worker", "fanout_workers"]


def test_providers_config_is_complete_and_marked():
    import json
    data = json.loads((HERE / "providers.json").read_text(encoding="utf-8"))
    assert set(data["tiers"]) == {"heavy_code", "context", "fast"}
    for chain in data["tiers"].values():
        for p in chain:
            assert {"name", "base_url", "env", "model", "status"} <= set(p)
            assert p["base_url"].startswith("https://")
            assert p["status"] == "to verify" or p["status"].startswith("verified ")
    assert set(data["tiers"]) == set(fr.TIERS)


def test_env_example_lists_every_key_and_holds_no_values():
    lines = (HERE / ".env.example").read_text(encoding="utf-8").splitlines()
    pairs = dict(l.split("=", 1) for l in lines if "=" in l and not l.startswith("#"))
    assert set(pairs) == set(fr.KEY_ENVS)
    assert all(v == "" for v in pairs.values())


def test_google_aq_keys_are_refused(env):
    key = "AQ." + "Ab1_" * 12  # the newer Google key format (53 characters)
    out = fr.route(f"debug this: GEMINI_API_KEY={key}", "fast", caller=lambda *a: "never")
    assert out.startswith("[WORKER: none] Refused")


def test_every_model_carries_a_verified_date_or_to_verify():
    import json, re
    data = json.loads((HERE / "providers.json").read_text(encoding="utf-8"))
    for chain in data["tiers"].values():
        for p in chain:
            assert p["status"] == "to verify" or re.fullmatch(r"verified \d{4}-\d{2}-\d{2}", p["status"]), p


def test_verify_reports_each_model_without_keys(env, capsys):
    script = {"openai/gpt-oss-120b": "OK"}
    def call(p, prompt, timeout):
        if p["model"] in script:
            return script[p["model"]]
        e = Exception("Error code: 404"); e.status_code = 404; raise e
    rows = fr.verify(caller=call)
    by = {r["model"]: r for r in rows}
    assert by["openai/gpt-oss-120b"]["ok"] is True
    assert any(not r["ok"] and "404" in r["why"] for r in rows)
    assert all("fake" not in r["why"] for r in rows)  # key values never appear
