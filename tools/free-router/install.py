"""Install the free worker router for Claude Code (and Cursor).

    python tools/free-router/install.py [--target ~/.claude/mcp] [--register]

Copies the router, its providers.json and .env.example to the target folder. It never overwrites
an existing .env or providers.json (your keys and your model choices stay yours). It writes a
Cursor snippet with this machine's paths, and prints the `claude mcp add` command; with
--register it runs it. Token-saving tools that see agent traffic (RTK, Headroom, mcp-compressor,
token-optimizer-mcp) are never installed here: each needs its own yes (see README.md).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
UV_ARGS = ["run", "--with", "mcp", "--with", "openai", "--with", "python-dotenv", "python"]


def install(target: Path, uv: str) -> None:
    target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(HERE / "free_router_mcp.py", target / "free_router_mcp.py")
    shutil.copy2(HERE / ".env.example", target / ".env.example")
    for keep in ("providers.json", ".env"):
        if not (target / keep).exists():
            src = HERE / ("providers.json" if keep == "providers.json" else ".env.example")
            shutil.copy2(src, target / keep)
    snippet = {"mcpServers": {"free-router": {"command": uv, "args": UV_ARGS + [str(target / "free_router_mcp.py")]}}}
    (target / "cursor_mcp_snippet.json").write_text(json.dumps(snippet, indent=2) + "\n", encoding="utf-8")


def register_command(target: Path, uv: str) -> list[str]:
    return ["claude", "mcp", "add", "--scope", "user", "free-router", "--", uv] + UV_ARGS + [
        str(target / "free_router_mcp.py")]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Install the free worker router.")
    ap.add_argument("--target", type=Path, default=Path.home() / ".claude" / "mcp")
    ap.add_argument("--register", action="store_true", help="also run `claude mcp add` (user scope)")
    a = ap.parse_args(argv)
    uv = shutil.which("uv") or "uv"
    install(a.target, uv)
    cmd = register_command(a.target, uv)
    print(f"Installed to {a.target}. Put your keys in {a.target / '.env'} (see .env.example).")
    print(f"Cursor: copy {a.target / 'cursor_mcp_snippet.json'} into Cursor's MCP settings.")
    if a.register:
        return subprocess.call(cmd)
    print("Not registered with Claude Code. To register, run:\n  " + " ".join(f'"{c}"' if " " in c else c for c in cmd))
    return 0


if __name__ == "__main__":
    sys.exit(main())
