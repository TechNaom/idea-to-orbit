# Changelog

## 0.5.2 - 2026-11-26

From the first run of the 0.5 pressure scenarios (7 of 10 held; the skill loaded in 4 of 10):

- Build: the check on an outside builder's log is in the build skill itself, with a red flag,
  not only in `external-builders.md` (the scenario failed: the builder was never checked).
- Session-start hook rule 9: load the skill before acting (verify before any status message,
  review before a merge, learn when trouble repeats, the stage's skill for stage work); rule 10:
  one real call before a test pins a model setting.
- Learn: its description names the words owners use ("be more careful", "a one-off").
- Every new scenario starts in a product with a `STATE.md`, as real sessions do; four graders
  judge the rule only, not missing files or tools the case does not give.
- Results after these changes (one run each): 8 of 10 new scenarios hold. Still failing, known
  gaps for the next release: `build-pin-model-param` and `verify-slow-suite-other-folder`.
  In both, Claude answers the request without loading the build or verify skill, so the rule
  in that skill is not applied.

## 0.5.1 - 2026-11-26

- Test flight's gate has an exit list, like every other stage.
- Long lines from 0.5.0 re-wrapped.

## 0.5.0 - 2026-11-26

From a review against a second, larger product: an enterprise app on GitLab and AWS, built by
outside agents (Cursor, Kiro), with AI features and many screens. Each new rule has an eval case.

- **Settings in `STATE.md`:** the code host (GitHub or GitLab), the work and release branches,
  promotion (work branch, then staging, then prod), who builds, the fast tests and the full
  suite with its time, and a **profile**. Every stage reads them instead of assuming GitHub,
  `main` and Claude's subagents. The session-start hook reports them.
- **Profiles:** *startup* (the old defaults) and *enterprise* (a managed secret store, a
  compliance mapping, data classification, no personal data in logs, staged promotion).
  Plain-text secrets on shared machines are a finding in both.
- **Outside builders:** `skills/build/external-builders.md`: a launcher, a per-worktree
  allow-list, commands written for the builder's shell (Git Bash eats backslashes), a probe
  run, and a check of the builder's first command within minutes. The builder changes files;
  the supervisor commits.
- **A slow suite:** the verify skill says what counts as "tests pass" when the full suite takes
  hours: the affected tests, found by a repository-wide search for every test that reads a
  changed file, then CI green for that exact commit.
- **Cold read:** before the Assemble gate a fresh agent reads the cards and lists where a
  builder would guess (`skills/review/cold-read.md`).
- **AI products:** Blueprint covers model choice, guardrails checked in code, eval bars and
  metering; cards for model calls carry an eval case; test flight runs the evals on the
  release commit; a red flag for pinning a model setting without one real call.
- **Screens:** Blueprint keeps a screen list (route, roles, key controls) and agrees a mockup;
  every UI card has a browser test per role; test flight gives the owner a screen-by-screen
  checklist.
- **Journal:** `JOURNAL.md` for every change, fix made in review and roadblock (cause, how it
  was cleared, the lesson).
- **Learn:** a fourth helper skill that groups the journal by cause and turns the top patterns
  into checks, card lines, red flags and eval cases.
- **Lanes:** feature, fix and hotfix lanes for work on a product that is past Build, listed
  under **In flight** in `STATE.md`, with the same rules and fewer steps.
- **Test flight:** every CI job that is allowed to fail is made blocking or justified.
- **Existing products:** the catch-up fills the Settings from the repository and maps the
  product's own plan, task list and journal instead of copying them.
- 10 new pressure scenarios (23 in all); the offline check covers the new hook output.

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
