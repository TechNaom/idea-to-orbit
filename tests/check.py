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
# The skill for each stage. Stage 7 is "orbit", but its skill is "keep-running": a skill named "orbit" would
# clash with the /orbit command.
STAGE_SKILLS = {s: ("keep-running" if s == "orbit" else s) for s in STAGES}
HELPERS = ["review", "debug", "verify", "learn"]
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
    for name in list(STAGE_SKILLS.values()) + HELPERS:
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
        if name in STAGE_SKILLS.values() and "## Gate" not in text:
            fail(f"skills/{name}: no gate section")
    extra = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()} - set(STAGE_SKILLS.values()) - set(HELPERS)
    if extra:
        fail(f"skills not covered by this check: {sorted(extra)}")


def check_name_clashes() -> None:
    """A skill and a command with the same name collide: typing /orbit loaded the stage-7 skill instead of the
    /orbit command (found 2026-11-26 on Explainer Studio). Every command name must be free of skills."""
    skills = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
    for cmd in (ROOT / "commands").glob("*.md"):
        if cmd.stem in skills:
            fail(f"commands/{cmd.name} and skills/{cmd.stem}/ share the name {cmd.stem!r}: /{cmd.stem} may load the skill")


def check_existing_products() -> None:
    """A product that already has code must not start Ignite from a blank page. /orbit sends it to the ignite
    skill's catch-up steps, which live in the skill itself (docs/ is not installed with the plugin) and say what to do
    with ADRs and with work already in flight (both were missing when Explainer Studio joined on 2026-11-26)."""
    cmd = read(ROOT / "commands" / "orbit.md")
    if "already has code" not in cmd:
        fail("commands/orbit.md: does not say what to do when the repository already has code")
    ignite = read(ROOT / "skills" / "ignite" / "SKILL.md")
    m = re.search(r"## Existing product\n(.*?)(\n## |\Z)", ignite.replace("\r\n", "\n"), re.S)
    if not m:
        fail("skills/ignite: no '## Existing product' section")
        return
    for must in ("reconstructed", "inferred", "ADR", "in flight", "explicit yes"):
        if must not in m.group(1):
            fail(f"skills/ignite: the existing-product steps do not cover {must!r}")


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
        if (case / "case.yaml").exists():  # a case with a scaffold keeps its tags here
            m = re.search(r"^tags:\s*\[(.*)\]", read(case / "case.yaml"), re.M)
            if m:
                covered.update(t.strip() for t in m.group(1).split(","))
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
            ("with a product's settings", True, "Profile: startup. Code host: github. Work branch: main. Builders: subagents. In flight: 1."),
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
        # A Stage line with extra words ("ignite (catching up ...)") names the skill by its first word only.
        wordy = pathlib.Path(tmp) / "wordy-stage"
        (wordy / "docs" / "orbit").mkdir(parents=True)
        text = read(sample).replace("- Stage: orbit", "- Stage: ignite (catching up an existing product)", 1)
        (wordy / "docs" / "orbit" / "STATE.md").write_text(text, encoding="utf-8")
        run = subprocess.run([bash, hook, "session-start"], cwd=wordy, env=dict(os.environ, CLAUDE_PROJECT_DIR=str(wordy)),
                             capture_output=True, text=True, timeout=30)
        ctx = json.loads(run.stdout)["hookSpecificOutput"]["additionalContext"]
        if not re.search(r"current stage \((?:[\w-]+:)?ignite\)", ctx):
            fail(f"hook with a wordy Stage line: expected the skill 'ignite' in {ctx[:400]!r}")
        # A STATE.md from before 0.5 has no Settings: the hook says so instead of stating defaults as facts.
        old = pathlib.Path(tmp) / "old-state"
        (old / "docs" / "orbit").mkdir(parents=True)
        (old / "docs" / "orbit" / "STATE.md").write_text(
            "# Product state: Old\n\n## Current\n\n- Stage: build\n- Status: in progress\n\n"
            "## Work in flight\n\n- branch t4-retry, half done\n\n## Open questions\n\n- None.\n", encoding="utf-8")
        run = subprocess.run([bash, hook, "session-start"], cwd=old, env=dict(os.environ, CLAUDE_PROJECT_DIR=str(old)),
                             capture_output=True, text=True, timeout=30)
        ctx = json.loads(run.stdout)["hookSpecificOutput"]["additionalContext"]
        if "Settings: not set in STATE.md" not in ctx or "In flight: 1." not in ctx:
            fail(f"hook with a 0.4 STATE.md: expected 'Settings: not set' and 'In flight: 1.' in {ctx[:400]!r}")
        # The template itself, with its HTML comments, gives clean values.
        tpl = pathlib.Path(tmp) / "template"
        (tpl / "docs" / "orbit").mkdir(parents=True)
        shutil.copy(ROOT / "skills" / "ignite" / "templates" / "state.md", tpl / "docs" / "orbit" / "STATE.md")
        run = subprocess.run([bash, hook, "session-start"], cwd=tpl, env=dict(os.environ, CLAUDE_PROJECT_DIR=str(tpl)),
                             capture_output=True, text=True, timeout=30)
        ctx = json.loads(run.stdout)["hookSpecificOutput"]["additionalContext"]
        if "Profile: startup. Code host: github. Work branch: main. Builders: subagents. In flight: 0." not in ctx:
            fail(f"hook with the STATE.md template: expected clean Settings values in {ctx[:400]!r}")
        # The skill names the hook gives must exist: the orbit stage's skill is keep-running, and the
        # "idea-to-orbit:" prefix only exists when installed as a plugin (CLAUDE_PLUGIN_ROOT is set).
        proj = pathlib.Path(tmp) / "names"
        (proj / "docs" / "orbit").mkdir(parents=True)
        shutil.copy(sample, proj / "docs" / "orbit" / "STATE.md")
        for plugin_root, want, wrong in ((None, "(keep-running)", "idea-to-orbit:"),
                                         (str(ROOT), "(idea-to-orbit:keep-running)", "idea-to-orbit:orbit")):
            env = {k: v for k, v in os.environ.items() if k != "CLAUDE_PLUGIN_ROOT"}
            env["CLAUDE_PROJECT_DIR"] = str(proj)
            if plugin_root:
                env["CLAUDE_PLUGIN_ROOT"] = plugin_root
            run = subprocess.run([bash, hook, "session-start"], cwd=proj, env=env, capture_output=True, text=True, timeout=30)
            ctx = json.loads(run.stdout)["hookSpecificOutput"]["additionalContext"]
            how = "as a plugin" if plugin_root else "by the install script"
            if want not in ctx or wrong in ctx:
                fail(f"hook installed {how}: expected {want!r} and no {wrong!r} in {ctx[:400]!r}")
    if b"\r\n" not in (ROOT / "hooks" / "run.cmd").read_bytes() and os.name == "nt":
        fail("hooks/run.cmd: needs CRLF line endings on Windows (see .gitattributes)")


def installers() -> list:
    """(name, cmd) for each installer this machine can run; cmd(args, env) gives the argv."""
    bash = find_bash()
    pwsh = shutil.which("pwsh") or shutil.which("powershell")
    runners = []
    if bash:
        runners.append(("install.sh", lambda args, env: [bash, str(ROOT / "install.sh"), *args]))
    if pwsh and os.name == "nt":
        runners.append(("install.ps1", lambda args, env: [pwsh, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                                                          str(ROOT / "install.ps1"), *args]))
    return runners


def check_install_safety() -> None:
    """Cases from the code check of 2026-11-26: the owner's settings and skills are never damaged."""
    runners = installers()
    skills = sorted(list(STAGE_SKILLS.values()) + HELPERS)

    def run(cmd, cfg: pathlib.Path, *args: str) -> subprocess.CompletedProcess:
        env = dict(os.environ, CLAUDE_CONFIG_DIR=str(cfg))
        return subprocess.run(cmd(args, env), env=env, capture_output=True, text=True, timeout=60)

    for name, cmd in runners:
        if not (ROOT / name).exists():
            continue
        # 1. a hook of the owner's whose path happens to contain "idea-to-orbit" survives install and uninstall
        with tempfile.TemporaryDirectory() as tmp:
            cfg = pathlib.Path(tmp) / "claude"
            cfg.mkdir()
            mine = {"matcher": "startup", "hooks": [{"type": "command", "command": "bash C:/src/idea-to-orbit-dev/mine.sh"}]}
            (cfg / "settings.json").write_text(json.dumps({"hooks": {"SessionStart": [mine]}}), encoding="utf-8")
            run(cmd, cfg)
            run(cmd, cfg, "--uninstall")
            after = json.loads((cfg / "settings.json").read_text(encoding="utf-8"))
            if mine not in after.get("hooks", {}).get("SessionStart", []):
                fail(f"{name}: deleted the owner's own hook that mentions idea-to-orbit: {after}")
        # 2. a settings.json saved with a byte order mark (Notepad, PowerShell 5.1) installs fine and stays readable
        with tempfile.TemporaryDirectory() as tmp:
            cfg = pathlib.Path(tmp) / "claude"
            cfg.mkdir()
            (cfg / "settings.json").write_text("\ufeff" + json.dumps({"model": "opus"}), encoding="utf-8")
            r = run(cmd, cfg)
            text = (cfg / "settings.json").read_text(encoding="utf-8-sig")
            if r.returncode != 0 or '"opus"' not in text or "session-start" not in text:
                fail(f"{name}: settings.json with a BOM: exit {r.returncode}, settings {text[:200]!r} {r.stderr[-200:]}")
        # 3. a settings.json that is not a JSON object stops the install before anything is copied
        for bad in ("{ not json", "[]", '{"hooks": null}'):
            with tempfile.TemporaryDirectory() as tmp:
                cfg = pathlib.Path(tmp) / "claude"
                cfg.mkdir()
                (cfg / "settings.json").write_text(bad, encoding="utf-8")
                r = run(cmd, cfg)
                copied = (cfg / "skills").exists() or (cfg / "idea-to-orbit").exists()
                if r.returncode == 0 or copied or (cfg / "settings.json").read_text(encoding="utf-8") != bad:
                    fail(f"{name}: settings.json {bad!r}: exit {r.returncode}, copied={copied}; must stop untouched")
        # 4. a skill of the owner's with one of our names is never overwritten, even if it mentions the plugin,
        #    and neither is a same-named folder without SKILL.md
        for folder, content in (("build", "---\nname: build\ndescription: inspired by Idea to Orbit\n---\nmine\n"),
                                ("debug", None)):
            with tempfile.TemporaryDirectory() as tmp:
                cfg = pathlib.Path(tmp) / "claude"
                (cfg / "skills" / folder).mkdir(parents=True)
                keep = cfg / "skills" / folder / ("SKILL.md" if content else "notes.txt")
                keep.write_text(content or "draft", encoding="utf-8")
                r = run(cmd, cfg)
                if r.returncode == 0 or not keep.exists() or (content and "mine" not in keep.read_text(encoding="utf-8")):
                    fail(f"{name}: overwrote the owner's own {folder!r} folder (exit {r.returncode})")
        # 6. the owner's own commands/orbit.md is never replaced by install nor deleted by uninstall
        with tempfile.TemporaryDirectory() as tmp:
            cfg = pathlib.Path(tmp) / "claude"
            (cfg / "commands").mkdir(parents=True)
            own = cfg / "commands" / "orbit.md"
            own.write_text("my own orbit command, not Idea to Orbit\n", encoding="utf-8")
            r = run(cmd, cfg)
            if r.returncode == 0 or "my own" not in own.read_text(encoding="utf-8") or (cfg / "skills").exists():
                fail(f"{name}: replaced the owner's own commands/orbit.md (exit {r.returncode})")
            run(cmd, cfg, "--uninstall")
            if not own.exists():
                fail(f"{name} --uninstall: deleted the owner's own commands/orbit.md")
        # 7. an empty SessionStart list of the owner's survives; a skill folder of ours that this version no
        #    longer ships is still removed by --uninstall
        with tempfile.TemporaryDirectory() as tmp:
            cfg = pathlib.Path(tmp) / "claude"
            cfg.mkdir()
            (cfg / "settings.json").write_text(json.dumps({"hooks": {"PreToolUse": [], "SessionStart": []}}),
                                               encoding="utf-8")
            run(cmd, cfg)
            stale = cfg / "skills" / "old-stage"
            stale.mkdir(parents=True)
            (stale / ".idea-to-orbit").write_text("x", encoding="utf-8")
            run(cmd, cfg, "--uninstall")
            after = json.loads((cfg / "settings.json").read_text(encoding="utf-8"))
            if after != {"hooks": {"PreToolUse": [], "SessionStart": []}}:
                fail(f"{name}: did not restore the owner's settings exactly: {after}")
            if stale.exists():
                fail(f"{name} --uninstall: left a skill folder it had installed (old-stage)")
    # 5. installed by one script, removed by the other
    if len(runners) == 2 and all((ROOT / n).exists() for n, _ in runners):
        for (a, ca), (b, cb) in (runners, runners[::-1]):
            with tempfile.TemporaryDirectory() as tmp:
                cfg = pathlib.Path(tmp) / "claude"
                cfg.mkdir()
                run(ca, cfg)
                run(cb, cfg, "--uninstall")
                left = [s for s in skills if (cfg / "skills" / s).exists()]
                hook_left = (cfg / "settings.json").exists() and "session-start" in (cfg / "settings.json").read_text(
                    encoding="utf-8-sig")
                if left or hook_left:
                    fail(f"installed with {a}, removed with {b}: left skills {left}, hook left {hook_left}")


def windows_safe(entry: dict) -> bool:
    """On Windows, Claude Code may run a hook command through PowerShell, where '"<path>" session-start' is a
    parse error ("Unexpected token 'session-start'") and the hook never runs. Found by the hook-reports-stage eval,
    2026-11-26. "shell": "bash" sends it to Git Bash; the powershell form uses the & call operator."""
    return entry.get("shell") == "bash" and str(entry.get("powershell", "")).startswith("& ")         and str(entry.get("powershell", "")).endswith(" session-start")


def check_plugin_hook() -> None:
    entries = [h for g in json.loads(read(ROOT / "hooks" / "hooks.json"))["hooks"]["SessionStart"] for h in g["hooks"]]
    if not entries or not all(windows_safe(h) for h in entries):
        fail(f"hooks/hooks.json: the session-start hook would not run on Windows: {entries}")


def check_session_scan() -> None:
    """The learn skill's scanner finds repeated trouble in transcripts and never prints a secret or a person."""
    run = subprocess.run([sys.executable, str(ROOT / "skills" / "learn" / "scan_sessions.py"), "--dir",
                          str(ROOT / "tests" / "fixtures" / "sessions")], capture_output=True, text=True,
                         encoding="utf-8", timeout=60)
    out = run.stdout
    if run.returncode != 0:
        fail(f"scan_sessions.py: exit {run.returncode}: {run.stderr[-300:]}")
        return
    for want in ("| 3 | 2 | `Bash: Permission to use Bash", "| 3 | `Bash: pytest -q tests/test_import.py` |",
                 "No module named build", "no, don't push to main"):
        if want not in out:
            fail(f"scan_sessions.py: expected {want!r} in its report")
    for leak in ("ghp_", "asha.k", "ledgerlite.example", "github.example", "/home/ravi"):
        if leak in out:
            fail(f"scan_sessions.py: printed {leak!r}; it must be redacted")


def check_install() -> None:
    """install.sh and install.ps1 put the skills, /orbit and the session-start hook into a Claude config folder,
    keep the owner's own settings, never add the hook twice, and --uninstall removes only what they added."""
    runners = installers()
    bash = find_bash()
    if not runners:
        fail("install: neither bash nor PowerShell found, cannot test the installers")
    skills = sorted(list(STAGE_SKILLS.values()) + HELPERS)
    for name, cmd in runners:
        if not (ROOT / name).exists():
            fail(f"install: {name} is missing")
            continue
        with tempfile.TemporaryDirectory() as tmp:
            cfg = pathlib.Path(tmp) / "claude"
            cfg.mkdir()
            other = {"matcher": "startup", "hooks": [{"type": "command", "command": "echo mine"}]}
            (cfg / "settings.json").write_text(json.dumps({"model": "opus", "hooks": {"SessionStart": [other]}}),
                                               encoding="utf-8")
            env = dict(os.environ, CLAUDE_CONFIG_DIR=str(cfg))

            def run(*args: str) -> subprocess.CompletedProcess:
                return subprocess.run(cmd(args, env), env=env, capture_output=True, text=True, timeout=60)

            for attempt in (1, 2):  # the second run must change nothing
                r = run()
                if r.returncode != 0:
                    fail(f"{name} run {attempt}: exit {r.returncode}: {r.stdout[-300:]} {r.stderr[-300:]}")
                    break
                missing = [s for s in skills if not (cfg / "skills" / s / "SKILL.md").exists()]
                if missing:
                    fail(f"{name} run {attempt}: skills not installed: {missing}")
                if not (cfg / "commands" / "orbit.md").exists():
                    fail(f"{name} run {attempt}: /orbit command not installed")
                try:
                    settings = json.loads((cfg / "settings.json").read_text(encoding="utf-8"))
                except Exception as e:  # noqa: BLE001
                    fail(f"{name} run {attempt}: settings.json is no longer valid JSON ({e})")
                    break
                starts = settings.get("hooks", {}).get("SessionStart", [])
                ours = [h for g in starts for h in g.get("hooks", []) if "idea-to-orbit" in h.get("command", "")]
                if settings.get("model") != "opus" or other not in starts:
                    fail(f"{name} run {attempt}: the owner's own settings were not kept: {settings}")
                if len(ours) != 1:
                    fail(f"{name} run {attempt}: expected one session-start hook of ours, found {len(ours)}")
                elif not windows_safe(ours[0]):
                    fail(f"{name} run {attempt}: the hook entry would not run on Windows (needs shell bash and a "
                         f"powershell form with &): {ours[0]}")
            if bash and (cfg / "idea-to-orbit" / "hooks" / "run.cmd").exists():
                proj = pathlib.Path(tmp) / "proj"
                (proj / "docs" / "orbit").mkdir(parents=True)
                shutil.copy(ROOT / "examples" / "repo-pulse" / "docs" / "orbit" / "STATE.md", proj / "docs" / "orbit")
                h = subprocess.run([bash, str(cfg / "idea-to-orbit" / "hooks" / "run.cmd"), "session-start"], cwd=proj,
                                   env=dict(env, CLAUDE_PROJECT_DIR=str(proj)), capture_output=True, text=True, timeout=30)
                if "Stage: orbit" not in h.stdout:
                    fail(f"{name}: the installed hook does not report the stage: {h.stdout[:200]!r} {h.stderr[:200]!r}")
            else:
                fail(f"{name}: hooks not installed to idea-to-orbit/hooks/")
            r = run("--uninstall")
            if r.returncode != 0:
                fail(f"{name} --uninstall: exit {r.returncode}: {r.stderr[-300:]}")
                continue
            left = [s for s in skills if (cfg / "skills" / s).exists()] + [
                p for p in ("commands/orbit.md", "idea-to-orbit") if (cfg / p).exists()]
            if left:
                fail(f"{name} --uninstall: still there: {left}")
            settings = json.loads((cfg / "settings.json").read_text(encoding="utf-8"))
            starts = settings.get("hooks", {}).get("SessionStart", [])
            if settings.get("model") != "opus" or other not in starts or "idea-to-orbit" in json.dumps(settings):
                fail(f"{name} --uninstall: settings not restored to the owner's own: {settings}")
        with tempfile.TemporaryDirectory() as tmp:  # someone else's skill with one of our names is never overwritten
            cfg = pathlib.Path(tmp) / "claude"
            (cfg / "skills" / "build").mkdir(parents=True)
            (cfg / "skills" / "build" / "SKILL.md").write_text("---\nname: build\n---\nmine\n", encoding="utf-8")
            r = subprocess.run(cmd((), None), env=dict(os.environ, CLAUDE_CONFIG_DIR=str(cfg)),
                               capture_output=True, text=True, timeout=60)
            if r.returncode == 0 or "mine" not in (cfg / "skills" / "build" / "SKILL.md").read_text(encoding="utf-8"):
                fail(f"{name}: overwrote a different skill named 'build' (exit {r.returncode})")


def check_field_feedback() -> None:
    """Lessons from running real products through the plugin (Explainer Studio, Stack Scout)."""
    prd = read(ROOT / "skills" / "ignite" / "templates" / "prd.md")
    for area in ["Release", "Guardrails", "Governance", "Token guard", "Budget guard"]:
        if f"| {area} |" not in prd:
            fail(f"prd template: no non-functional row for {area}")
    if "## Scope changes" not in prd:
        fail("prd template: no 'Scope changes' section")
    ignite = read(ROOT / "skills" / "ignite" / "SKILL.md")
    gate = ignite.split("## Gate", 1)[-1]
    if "cold read" not in gate.lower():
        fail("ignite gate: no cold read of the brief and PRD")
    if "not needed" not in gate.lower():
        fail("ignite gate: non-functional areas need a requirement or 'not needed' with a reason")
    if "new requirement IDs" not in ignite:
        fail("ignite: widened scope on an existing product must get new requirement IDs")
    blueprint = read(ROOT / "skills" / "blueprint" / "SKILL.md")
    if "Prior art" not in blueprint:
        fail("blueprint: no prior-art step (existing projects and services before designing)")
    flags = blueprint.split("## Red flags", 1)[-1].split("## Gate", 1)[0].lower()
    for words in ["install path", "starts and ends"]:
        if words not in flags:
            fail(f"blueprint red flags: nothing about '{words}'")
    if "more than once" not in read(ROOT / "docs" / "testing.md"):
        fail("docs/testing.md: no rule to run a changed case more than once (results vary run to run)")


def check_field_feedback_v09() -> None:
    """0.9 lessons: big choices hidden in one yes, unchecked names, briefs without past lessons, real credentials."""
    blueprint = read(ROOT / "skills" / "blueprint" / "SKILL.md")
    steps = blueprint.split("## Steps", 1)[-1].split("## Profiles", 1)[0]
    if "already uses" not in steps:
        fail("blueprint steps: hosting options must start from the platforms and accounts the owner already uses")
    gate = blueprint.split("## Gate", 1)[-1]
    if "own yes" not in gate or "new vendor" not in gate:
        fail("blueprint gate: each new vendor, paid service, account or hosting change needs its own yes")
    flags = blueprint.split("## Red flags", 1)[-1].split("## Gate", 1)[0].lower()
    if "one yes" not in flags:
        fail("blueprint red flags: nothing about one yes covering a new vendor or bill")
    assemble = read(ROOT / "skills" / "assemble" / "SKILL.md")
    inputs = assemble.split("## Inputs", 1)[-1].split("## Steps", 1)[0]
    if "own yes" not in inputs:
        fail("assemble inputs: must refuse to start while a new vendor or hosting ADR lacks its own yes")
    if "search the web" not in assemble.lower():
        fail("assemble: invented names in examples and test data must be checked on the web")
    brief = read(ROOT / "skills" / "build" / "builder-brief.md")
    if "Fix in review" not in brief:
        fail("builder brief: no section for the product's recent Fix in review lessons")
    for name in ["code-check.md", "task-check.md", "cold-read.md"]:
        text = read(ROOT / "skills" / "review" / name).lower()
        if "real credential" not in text:
            fail(f"review/{name}: no rule against reading real credentials")
    if "exposed" not in read(ROOT / "skills" / "review" / "code-check.md").lower():
        fail("review/code-check.md: an exposed credential must be reported to the owner at once")


def check_field_feedback_v010() -> None:
    """0.10 lessons from a live website's 3D feature lane: look, motion, adaptive runtime, pace, lanes in assemble."""
    ignite = read(ROOT / "skills" / "ignite" / "SKILL.md")
    if "visual direction" not in ignite.lower():
        fail("ignite: a product with screens must be asked for its visual direction before the PRD")
    if "existing product and a feature lane" not in ignite.lower():
        fail("ignite: no order for an existing product that arrives with a new feature")
    if "toolchain" not in ignite.lower():
        fail("ignite (existing product): no step to record the toolchain and how to install it")
    state = read(ROOT / "skills" / "ignite" / "templates" / "state.md")
    for word in ["Toolchain:", "Pace:"]:
        if word not in state:
            fail(f"state template: no {word} setting")
    blueprint = read(ROOT / "skills" / "blueprint" / "SKILL.md")
    low = blueprint.lower()
    if "changes on its own at run time" not in low:
        fail("blueprint: no question about behaviour the product changes on its own, and how a test pins it")
    if "cost the user pays" not in low:
        fail("blueprint prior art: measure the cost the user pays, not reputation")
    if "live mockup" not in low:
        fail("blueprint mockup: no live mockup when motion is the point")
    arch = read(ROOT / "skills" / "blueprint" / "templates" / "architecture.md")
    if "Observability for tests" not in arch:
        fail("architecture template: no row for how tests read the product's state")
    if "Visual system" not in arch:
        fail("architecture template: no visual system block (tokens, layers, states) in Screens")
    if "spike" not in read(ROOT / "commands" / "orbit.md").lower():
        fail("orbit command: a spike is not named (allowed before the gate, labelled, never merged)")
    assemble = read(ROOT / "skills" / "assemble" / "SKILL.md")
    if "promotion environment" not in assemble.lower():
        fail("assemble: for a feature lane, 'deployed' must mean the promotion environment")
    prd = read(ROOT / "skills" / "ignite" / "templates" / "prd.md")
    if "builders" not in prd.split("| N7 |", 1)[-1].split("| N10 |", 1)[0].lower():
        fail("prd template: governance, token and budget guards must also cover the AI builders, even with no model in the product")
    if "| N10 |" not in prd:
        fail("prd template: no evals row for the build process")
    build = read(ROOT / "skills" / "build" / "SKILL.md")
    if "token-ledger.md" not in build:
        fail("build: no token ledger of every agent run")
    if "combined check" not in build.lower():
        fail("build: no lean mode (one combined check for small, low-risk tasks)")
    if not (ROOT / "skills" / "build" / "templates" / "token-ledger.md").exists():
        fail("build: no token ledger template")
    cold = assemble.split("**Cold read.**", 1)[-1].split("\n8.", 1)[0].lower()
    if "real code" not in cold:
        fail("assemble cold read: the reader must check the cards against the real code they name")


def check_token_meter() -> None:
    """The token meter's unit tests (skills/build/token_meter.py), on every platform CI runs."""
    import unittest
    suite = unittest.defaultTestLoader.loadTestsFromName("test_token_meter")
    result = unittest.TextTestRunner(stream=open(os.devnull, "w"), verbosity=0).run(suite)
    for test, err in result.failures + result.errors:
        fail(f"token meter: {test.id().rsplit('.', 1)[-1]}: {err.strip().splitlines()[-1]}")
    if "token_meter.py" not in read(ROOT / "skills" / "build" / "SKILL.md"):
        fail("build: the token guard does not point to token_meter.py")


def main() -> int:
    data = check_json()
    check_versions(data)
    check_skills()
    check_name_clashes()
    check_existing_products()
    check_links()
    check_evals()
    check_field_feedback()
    check_field_feedback_v09()
    check_field_feedback_v010()
    sys.path.insert(0, str(ROOT / "tests"))
    check_token_meter()
    check_hook()
    check_plugin_hook()
    check_session_scan()
    check_install()
    check_install_safety()
    if failures:
        print(f"{len(failures)} problem(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("All checks passed: JSON, versions, skills, links, evals, the session-start hook and the installers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
