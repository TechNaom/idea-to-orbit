"""Static checks for the Idea to Orbit plugin. No model calls, no network, no cost.

Run from the repository root:  python tests/check.py
CI runs it on every push and pull request.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
STAGES = ["ignite", "blueprint", "assemble", "build", "test-flight", "launch", "orbit"]
HELPERS = ["review", "debug", "verify"]
failures: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)


def read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"---\n(.*?)\n---\n", text.replace("\r\n", "\n"), re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def check_json() -> dict:
    data = {}
    for rel in [".claude-plugin/plugin.json", ".claude-plugin/marketplace.json", "hooks/hooks.json"]:
        try:
            data[rel] = json.loads(read(ROOT / rel))
        except Exception as e:  # noqa: BLE001
            fail(f"{rel}: not valid JSON ({e})")
    return data


def check_versions(data: dict) -> None:
    plugin = data.get(".claude-plugin/plugin.json", {}).get("version")
    market = data.get(".claude-plugin/marketplace.json", {})
    versions = {
        "plugin.json": plugin,
        "marketplace metadata": market.get("metadata", {}).get("version"),
        "marketplace plugin": (market.get("plugins") or [{}])[0].get("version"),
    }
    m = re.search(r"^## (\d+\.\d+\.\d+)", read(ROOT / "CHANGELOG.md"), re.M)
    versions["CHANGELOG.md"] = m.group(1) if m else None
    # README and DESIGN name the minor version only ("Version 0.3"); compare on that.
    versions = {k: ".".join(v.split(".")[:2]) if v else None for k, v in versions.items()}
    for rel in ["README.md", "docs/DESIGN.md"]:
        m = re.search(r"Version (\d+\.\d+)", read(ROOT / rel))
        versions[rel] = m.group(1) if m else None
    if len(set(versions.values())) != 1:
        fail(f"versions disagree: {versions}")


def check_skills() -> None:
    for name in STAGES + HELPERS:
        path = ROOT / "skills" / name / "SKILL.md"
        if not path.exists():
            fail(f"missing skill: skills/{name}/SKILL.md")
            continue
        text = read(path)
        fm = frontmatter(text)
        if fm.get("name") != name:
            fail(f"skills/{name}: frontmatter name is {fm.get('name')!r}")
        desc = fm.get("description", "")
        if not desc:
            fail(f"skills/{name}: no description")
        if len(desc) > 1024:
            fail(f"skills/{name}: description is {len(desc)} characters (max 1024)")
        if "Use " not in desc:
            fail(f"skills/{name}: description does not say when to use it")
        if "## Red flags" not in text:
            fail(f"skills/{name}: no red flags section")
        if name in STAGES and "## Gate" not in text:
            fail(f"skills/{name}: no gate section")
    extra = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()} - set(STAGES + HELPERS)
    if extra:
        fail(f"skills not covered by this check: {sorted(extra)}")


def check_links() -> None:
    link = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
    for md in ROOT.rglob("*.md"):
        if any(part in {".git", "node_modules", "results", "templates"} for part in md.parts):
            continue
        for target in link.findall(read(md)):
            if re.match(r"[a-z]+:", target) or target.startswith("#"):
                continue
            path = target.split("#", 1)[0]
            if path and not (md.parent / path).resolve().exists():
                fail(f"{md.relative_to(ROOT)}: broken link {target}")


def check_evals() -> None:
    evals = ROOT / "evals"
    cases = [p for p in evals.iterdir() if p.is_dir() and ((p / "prompt.md").exists() or (p / "case.yaml").exists())]
    if len(cases) < 10:
        fail(f"evals: only {len(cases)} cases")
    covered = set()
    for case in cases:
        graders = list((case / "graders").glob("*.md")) if (case / "graders").exists() else []
        if not graders:
            fail(f"evals/{case.name}: no graders")
        for g in graders:
            if not frontmatter(read(g)).get("type"):
                fail(f"evals/{case.name}/graders/{g.name}: no type")
        if (case / "prompt.md").exists():
            fm = frontmatter(read(case / "prompt.md"))
            covered.update(t.strip() for t in fm.get("tags", "").strip("[]").split(","))
    for name in STAGES + HELPERS:
        if name not in covered and name not in {"review"}:
            fail(f"evals: no case tagged {name}")


def find_bash() -> str | None:
    if os.name == "nt":
        for p in [r"C:\Program Files\Git\bin\bash.exe", os.path.expandvars(r"%LOCALAPPDATA%\Programs\Git\bin\bash.exe")]:
            if os.path.exists(p):
                return p
    return shutil.which("bash")


def check_hook() -> None:
    bash = find_bash()
    if not bash:
        fail("hook: bash not found, cannot test the session-start hook")
        return
    hook = str(ROOT / "hooks" / "run.cmd")
    sample = ROOT / "examples" / "repo-pulse" / "docs" / "orbit" / "STATE.md"
    with tempfile.TemporaryDirectory() as tmp:
        for label, with_state, expect in [
            ("with a product", True, "Stage: orbit. Status: approved. Open questions: 0."),
            ("without a product", False, "no docs/orbit/STATE.md"),
        ]:
            proj = pathlib.Path(tmp) / label.replace(" ", "-")
            (proj / "docs" / "orbit").mkdir(parents=True)
            if with_state:
                shutil.copy(sample, proj / "docs" / "orbit" / "STATE.md")
            env = dict(os.environ, CLAUDE_PROJECT_DIR=str(proj))
            run = subprocess.run([bash, hook, "session-start"], cwd=proj, env=env, capture_output=True, text=True, timeout=30)
            try:
                ctx = json.loads(run.stdout)["hookSpecificOutput"]["additionalContext"]
            except Exception as e:  # noqa: BLE001
                fail(f"hook {label}: output is not the expected JSON ({e}): {run.stdout[:200]!r} {run.stderr[:200]!r}")
                continue
            if expect not in ctx:
                fail(f"hook {label}: expected {expect!r} in {ctx[:200]!r}")
    if b"\r\n" not in (ROOT / "hooks" / "run.cmd").read_bytes() and os.name == "nt":
        fail("hooks/run.cmd: needs CRLF line endings on Windows (see .gitattributes)")


def main() -> int:
    data = check_json()
    check_versions(data)
    check_skills()
    check_links()
    check_evals()
    check_hook()
    if failures:
        print(f"{len(failures)} problem(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("All checks passed: JSON, versions, skills, links, evals and the session-start hook.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
