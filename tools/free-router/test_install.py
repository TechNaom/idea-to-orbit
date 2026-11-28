"""Tests for install.py: a fake home folder, no network, nothing registered."""
import importlib.util
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("fr_install", HERE / "install.py")
inst = importlib.util.module_from_spec(spec)
sys.modules["fr_install"] = inst
spec.loader.exec_module(inst)


def test_copies_files_and_never_overwrites_env(tmp_path):
    target = tmp_path / ".claude" / "mcp"
    target.mkdir(parents=True)
    (target / ".env").write_text("GROQ_API_KEY=keep-me\n", encoding="utf-8")
    inst.install(target, uv="/opt/bin/uv")
    for name in ("free_router_mcp.py", "providers.json", ".env.example"):
        assert (target / name).exists()
    assert (target / ".env").read_text(encoding="utf-8") == "GROQ_API_KEY=keep-me\n"


def test_creates_an_empty_env_when_missing(tmp_path):
    target = tmp_path / "mcp"
    inst.install(target, uv="uv")
    assert (target / ".env").read_text(encoding="utf-8") == (HERE / ".env.example").read_text(encoding="utf-8")


def test_keeps_a_users_own_providers_file(tmp_path):
    target = tmp_path / "mcp"
    target.mkdir()
    (target / "providers.json").write_text('{"tiers": {}}', encoding="utf-8")
    inst.install(target, uv="uv")
    assert (target / "providers.json").read_text(encoding="utf-8") == '{"tiers": {}}'


def test_cursor_snippet_uses_this_machines_paths(tmp_path):
    target = tmp_path / "mcp"
    inst.install(target, uv="/opt/bin/uv")
    snippet = json.loads((target / "cursor_mcp_snippet.json").read_text(encoding="utf-8"))
    server = snippet["mcpServers"]["free-router"]
    assert server["command"] == "/opt/bin/uv"
    assert server["args"][-1] == str(target / "free_router_mcp.py")
    assert server["args"][:7] == ["run", "--with", "mcp", "--with", "openai", "--with", "python-dotenv"]


def test_register_command_is_printed_not_run_by_default(tmp_path, capsys):
    target = tmp_path / "mcp"
    cmd = inst.register_command(target, uv="uv")
    assert cmd[:4] == ["claude", "mcp", "add", "--scope"]
    assert "free-router" in cmd and str(target / "free_router_mcp.py") in cmd
    inst.main(["--target", str(target)])
    out = capsys.readouterr().out
    assert "claude mcp add" in out and "Not registered" in out
