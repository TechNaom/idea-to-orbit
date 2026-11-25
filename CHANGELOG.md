# Changelog

## 0.4.0 - 2026-11-26

From running the first real product (Explainer Studio) through the plugin:

- **Install scripts** for Claude Code surfaces without `/plugin` (for example VS Code):
  `install.sh` and `install.ps1` copy the skills and `/orbit`, register the session-start hook,
  keep the owner's own settings (exactly, even empty lists), never add the hook twice, stop before
  any change if settings.json is unreadable, never overwrite or delete a skill or `/orbit` command
  of the owner's, and `--uninstall` removes exactly what they added, whichever script installed it.
  Checked by a fresh-agent code review (8 findings, all fixed) and 20 offline test cases in CI.
- **Existing products:** `/orbit` now notices a repository that already has code and runs the
  ignite skill's new **Existing product** steps: reconstruct the documents from the code, mark
  what was inferred, say what to do with ADRs and with work already in flight, and pass the
  gates only on the owner's explicit yes.
- The session-start hook names skills that exist: `keep-running` for stage 7, and the
  `idea-to-orbit:` prefix only when installed as a plugin.
- The brief template says "none" is a fine buyer for an owner's own tool.

## 0.3.1 - 2026-11-26

- Fixed: typing `/orbit` could load the stage-7 skill instead of the `/orbit` command, because
  both were named `orbit`. The stage is still called Orbit; its skill is now `keep-running`.
  A new offline check fails if any skill shares a name with a command.

## 0.3.0 - 2026-11-26

- **Session-start hook:** every session in a product repository begins with the product's
  stage, status and open questions, and the rules that hold for the whole session. Works on
  Windows, macOS and Linux.
- **Build, rebuilt:** one iron rule (no production code without a failing test first); each
  task goes to a fresh builder agent, then a task check and a code check by two more fresh
  agents; a branch check at the end of every milestone; parallel builds in worktrees.
- **Task cards:** assemble now writes, for each task, the exact files, steps, commands and
  expected output, so a builder never has to guess.
- **Three helper skills:** review (the three checks and how to handle findings), debug (root
  cause before any fix; stop after two failed fixes) and verify (evidence before claims).
- **Red flags** in every stage and helper: the thoughts that mean "stop", and what to do instead.
- **Tests:** 13 pressure scenarios for `claude plugin eval`, and an offline check script that
  CI runs on every push.
- The sample product now has a task card for every task.
- Fixed: the design document named the wrong version.

## 0.2.0 - 2026-11-26

- Docs: getting started, concepts, stage reference, examples with sample sessions, existing
  projects, FAQ and troubleshooting.
- A complete sample product, Repo Pulse, with every document from brief to incident report.
- Test flight now checks every credential's expiry date.

## 0.1.0 - 2026-11-25

- Seven stages as skills: ignite, blueprint, assemble, build, test-flight, launch, orbit.
- Templates for every document a stage writes.
- The `/orbit` command.
