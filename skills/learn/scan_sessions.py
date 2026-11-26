#!/usr/bin/env python3
"""Find repeated trouble in a project's past Claude Code sessions, for the learn skill.

Reads the session transcripts (.jsonl) that Claude Code keeps for one project and reports, as
Markdown: tool calls that failed with the same error, commands that were refused, commands
retried several times in one session, and messages where the owner corrected course. Every
example is redacted in code before it is printed: tokens and keys, emails, hosts, IP addresses
and user paths become placeholders. Nothing is written or sent anywhere.

Usage:
  python scan_sessions.py --project <path to the product's repository>
  python scan_sessions.py --dir <folder of .jsonl transcripts>
Options: --days N (only sessions changed in the last N days), --top N (rows per table).
Standard library only; Python 3.8 or later.
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
import time
from pathlib import Path

REDACTIONS = [
    (re.compile(r"\b(?:gh[pousr]|github_pat)_[A-Za-z0-9_]{10,}"), "[TOKEN]"),
    (re.compile(r"\bglpat-[A-Za-z0-9_\-]{10,}"), "[TOKEN]"),
    (re.compile(r"\bsk-[A-Za-z0-9_\-]{10,}"), "[TOKEN]"),
    (re.compile(r"\bxox[abposr]-[A-Za-z0-9\-]{10,}"), "[TOKEN]"),
    (re.compile(r"\bA[KS]IA[0-9A-Z]{16}\b"), "[TOKEN]"),
    (re.compile(r"(?i)\b(bearer|token|password|passwd|secret|api[_-]?key)\b(\s*[:=]\s*|\s+)\S+"), r"\1\2[SECRET]"),
    (re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"), "[EMAIL]"),
    (re.compile(r"\bhttps?://[^\s\"'<>)]+"), "[URL]"),
    (re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), "[IP]"),
    (re.compile(r"(?i)\b[A-Z]:[\\/]+Users[\\/]+[^\\/\s\"']+"), "[PATH]"),
    (re.compile(r"(?<![\w.])/(?:home|Users)/[^/\s\"']+"), "[PATH]"),
    (re.compile(r"\b[A-Za-z0-9+/_\-]{40,}={0,2}"), "[LONG-VALUE]"),
]
REFUSED = re.compile(r"(?i)permission|denied|not allowed|refused|rejected|blocked by|requires approval")
CORRECTION = re.compile(r"(?i)^\s*(no\b|don'?t|do not|stop\b|wrong\b|that'?s (not|wrong)|not (what|that)|why did you|you (forgot|missed|didn'?t))")


def redact(text: str) -> str:
    for pattern, repl in REDACTIONS:
        text = pattern.sub(repl, text)
    return text


def shape(text: str, width: int = 90) -> str:
    """One line, redacted, with numbers and quoted names folded so the same error groups together."""
    line = next((ln.strip() for ln in str(text).splitlines() if ln.strip()), "")
    line = redact(line)
    line = re.sub(r"\b\d+\b", "N", line)
    line = re.sub(r"'[^']{1,60}'|\"[^\"]{1,60}\"", "'…'", line)
    return line[:width]


def project_folder(project: str) -> Path:
    base = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "projects"
    name = re.sub(r"[^A-Za-z0-9]", "-", str(Path(project).resolve()))
    exact = base / name
    if exact.is_dir():
        return exact
    matches = [p for p in base.glob("*") if p.is_dir() and p.name.lower() == name.lower()]
    return matches[0] if matches else exact


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def scan(files: list[Path]) -> dict:
    errors = collections.Counter()
    error_sessions = collections.defaultdict(set)
    refused = collections.Counter()
    refused_sessions = collections.defaultdict(set)
    retried = collections.Counter()
    corrections = []
    for path in files:
        session = path.stem[:8]
        calls = {}
        runs = collections.Counter()
        failed_cmds = set()
        for raw in path.open(encoding="utf-8", errors="replace"):
            try:
                rec = json.loads(raw)
            except ValueError:
                continue
            kind = rec.get("type")
            if kind not in ("user", "assistant"):
                continue
            content = (rec.get("message") or {}).get("content")
            if kind == "user" and not (isinstance(content, list) and any(
                    isinstance(b, dict) and b.get("type") == "tool_result" for b in content)):
                said = text_of(content)
                if said and CORRECTION.match(said) and not said.lstrip().startswith("<"):
                    corrections.append((session, shape(said, 110)))
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    name = block.get("name", "?")
                    cmd = (block.get("input") or {}).get("command")
                    key = f"{name}: {shape(cmd, 70)}" if isinstance(cmd, str) else None
                    calls[block.get("id")] = (name, key)
                    if key:
                        runs[key] += 1
                elif block.get("type") == "tool_result" and block.get("is_error"):
                    name, key = calls.get(block.get("tool_use_id"), ("?", None))
                    body = block.get("content")
                    body = body if isinstance(body, str) else text_of(body) or json.dumps(body)[:300]
                    if REFUSED.search(body):
                        refused[f"{name}: {shape(body)}"] += 1
                        refused_sessions[f"{name}: {shape(body)}"].add(session)
                    else:
                        errors[f"{name}: {shape(body)}"] += 1
                        error_sessions[f"{name}: {shape(body)}"].add(session)
                    if key:
                        failed_cmds.add(key)
        for key, n in runs.items():
            if n >= 3 and key in failed_cmds:
                retried[key] += n
    return {"errors": (errors, error_sessions), "refused": (refused, refused_sessions),
            "retried": retried, "corrections": corrections, "files": len(files)}


def report(found: dict, top: int) -> str:
    out = [f"# Repeated trouble in {found['files']} session(s)", "",
           "Every example below is redacted. Check the patterns against the journal before acting.", ""]

    def table(title: str, counter, sessions=None):
        out.extend([f"## {title}", ""])
        rows = [(k, n) for k, n in counter.most_common(top) if n >= 2 or sessions is None]
        if not rows:
            out.extend(["None seen twice.", ""])
            return
        out.append("| Count | Sessions | Pattern |" if sessions else "| Runs | Pattern |")
        out.append("|---|---|---|" if sessions else "|---|---|")
        for k, n in rows:
            pat = k.replace("|", "\\|")
            out.append(f"| {n} | {len(sessions[k])} | `{pat}` |" if sessions else f"| {n} | `{pat}` |")
        out.append("")

    table("Refused commands and tools", *found["refused"])
    table("Tool errors seen more than once", *found["errors"])
    table("Commands retried three or more times in a session (at least one failed)", found["retried"])
    out.extend(["## Owner corrections", ""])
    if found["corrections"]:
        out.extend(f"- {s}: {t}" for s, t in found["corrections"][:top])
    else:
        out.append("None found.")
    out.append("")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--project", help="path to the product's repository")
    src.add_argument("--dir", help="folder of .jsonl session transcripts")
    ap.add_argument("--days", type=int, default=0, help="only sessions changed in the last N days")
    ap.add_argument("--top", type=int, default=15, help="rows per table")
    args = ap.parse_args(argv)
    folder = Path(args.dir) if args.dir else project_folder(args.project)
    if not folder.is_dir():
        print(f"No session folder at {redact(str(folder))}. Pass --dir with the right folder.", file=sys.stderr)
        return 1
    files = sorted(folder.glob("*.jsonl"))
    if args.days:
        cutoff = time.time() - args.days * 86400
        files = [f for f in files if f.stat().st_mtime >= cutoff]
    print(report(scan(files), args.top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
