# Changelog

## 0.10.0 - 2026-11-28

Lessons from a third real product: a feature lane that turns a live personal website into a 3D
site. Each rule has an offline check that failed before the change, and the new eval cases are
listed below. In this run the design cold read found 20 gaps (9 would have caused a wrong build)
and the card cold read 12 more (6 important), all before any code.

- **Ignite:** a product with screens is asked for its **visual direction** as a multiple-choice
  question before the PRD (Claude picked a look; the owner chose another). An existing product
  that arrives with a new feature: catch up Settings and a reconstructed requirement list first,
  then open the lane. A **Toolchain** setting records the runtime and how to install what is
  missing without changing lock files (it took three tries to run the tests).
- **Pace:** a setting in `STATE.md`. A standing "no need to stop" is recorded with the owner's
  words and date and counts as the yes for the gates it covers; a new vendor or bill, a change to
  the live product and the owner's UAT still stop and ask.
- **Spikes:** named in `/orbit`: agreed, labelled, on a local branch, never merged, the lesson in an
  ADR, logged as a skipped rule (exploration had slid into the product's repository).
- **Blueprint:** list what the product **changes on its own at run time** (quality levels,
  fallbacks, retries) and how a test pins each one (CI browsers have no graphics card, so every
  3D test would have seen the fallback). An **Observability for tests** row in Interfaces. Prior
  art by **measurement** (the cost the user pays, live activity). A **Visual system** block in
  Screens (tokens, layers, what changes per state). A **live mockup** when motion is the point.
- **Assemble:** in a feature lane, "deployed end to end" means the **promotion environment**, and
  standard first tasks are kept or marked "not needed" with a reason. The cold read checks the
  cards against the **real code** they name.
- **The builders are an AI system too:** governance, token guard and budget guard in the PRD
  template also cover the agents that build the product, and a new N10 row measures them
  (first-pass task checks, fixes in review, tokens per task). Build keeps a **token ledger** of
  every agent run, estimates each milestone first, uses a **lean mode** (one combined check for
  small, low-risk tasks) and stops cleanly at a plan's usage limit. (One task's agents used 182k
  tokens against a 150k budget; a builder was cut off by the 5-hour limit and resumed.)
- **Token meter** (`skills/build/token_meter.py`): reads Claude Code session logs, subagents
  included, and reports fresh and cached tokens by agent, role, task, model and day; per-task
  budgets with warnings at 80%; savings from the cache (with a dated prices file you keep, else
  tokens only) and from lean mode against a measured baseline; ledger rows. It reads counts only,
  never content. Plain Python, unit-tested in CI. (On its first real run, 96% of 47.7M tokens were
  cache reads, and the main session used 75% of the fresh tokens, more than all subagents together;
  the hand-copied numbers had hidden both.)
- **Free worker router** (`tools/free-router`, optional): an MCP server that hands self-contained
  sub-tasks to free or other OpenAI-compatible models in three tiers with failover, a size guard, a
  secret guard and a log without prompts; providers in `providers.json`, each "to verify"; an
  installer that never overwrites `.env` and writes the Cursor snippet per machine. The build stage's
  `workers.md` keeps Claude as supervisor and quality gate. Tested with fakes in CI.
- Eval cases added: `ignite-visual-direction`, `orbit-pace-standing-yes`,
  `blueprint-runtime-fallback-ci`, `assemble-lane-preview-not-prod`. Not run yet (paid runs wait
  for the owner).

## 0.9.0 - 2026-11-27

Lessons from real use, written as general rules for any product. Each has an offline check that
failed before the change.

- **Blueprint:** hosting, data, storage and scheduling options start from the platforms and
  accounts the owner already uses (option A); a new vendor, account or bill must win on the facts.
  The gate asks a **separate yes** for every ADR that adds a new vendor, paid service, account or
  change of where the product runs, in plain words, apart from the yes to the whole design. A red
  flag: "one yes to the summary covers it". (A new cloud account slipped through one yes to a long
  summary; the owner, busy, only saw it later.)
- **Assemble:** refuses to start while such an ADR has no yes of its own. Invented names in
  examples, fixtures and test data are searched on the web first and replaced if they match or
  come close to a real one. (A card's example client name was close to real companies.)
- **Builder brief:** a "Lessons from earlier tasks" section filled from the product's recent
  Fix in review rows. (A builder given earlier lessons passed its task check first time.)
- **Review briefs:** checkers never read real credentials (mocks and fakes only); an exposed
  credential goes first in the report so the owner can revoke it at once. (A probe printed a real
  CLI token into a session transcript.)
- Not done yet: eval scenarios for these rules (they need paid runs).

## 0.8.0 - 2026-11-27

Lessons from running two real products through the plugin (Explainer Studio and Stack Scout),
logged in their `plugin-feedback.md` files. Each has an offline check that failed before the change.

- **Ignite:** a cold read of the brief and PRD by a fresh agent before the gate (it found five
  real gaps on Stack Scout that the steps did not prompt for). The PRD template's non-functional
  table adds release, guardrails, governance, token guard and budget guard, and the gate needs
  each area to have a requirement or "not needed" with a reason. A **Scope changes** list in the
  PRD; on an existing product, widened scope gets new requirement IDs.
- **Blueprint:** a **prior-art** step (existing open-source projects and managed services,
  checked live, are options next to building), and two red flags: how the code finds its files
  on every install path, and what starts and ends one run.
- **Hook:** the skill is the Stage field's first word, so `- Stage: ignite (catching up ...)`
  points at the ignite skill.
- **Testing guide:** run a changed case more than once; one run is noise.
- Not done yet: eval scenarios for the new Ignite and Blueprint rules (they need paid runs).

## 0.7.1 - 2026-11-26

From lesson issue #1: a feature request on a live product ("make our assistant like our other
product's") was planned as a list of build steps, without the feature lane's ignite.

- Ignite has a **feature lane** section (lane under In flight, requirements with IDs and checks,
  out of scope, proposed numbers marked, the owner's yes before cards), and its description
  names the request shapes that start one ("add", "improve", "ramp up", "make it like").
- `/orbit`, the session-start hook (rule 11) and a build red flag say the same.
- New scenario `orbit-feature-lane-catch-up` (29 in all): failed 2 of 2 runs before the change.

## 0.7.0 - 2026-11-26

- **Session scanner** for the learn skill (`skills/learn/scan_sessions.py`, standard library
  only): it reads a project's Claude Code transcripts and reports refused commands, tool errors
  seen more than once, commands retried in a session and the owner's corrections, redacted in
  code (tokens, emails, URLs, IPs, user paths, long values). The offline check runs it on fake
  transcripts and fails if anything leaks.
- **CI on every platform:** the offline check runs on Linux, Windows and macOS, with Python 3.10
  and 3.12, so a hook or installer problem on one platform (like the 0.6.0 Windows hook fix)
  fails the push.

## 0.6.0 - 2026-11-26

Deeper build discipline and design, from a comparison with another Claude Code plugin
(superpowers):

- **Fix loop** (`skills/build/fix-loop.md`): findings are sorted (notes recorded, conflicts with
  the card ruled on), then fixed in rounds of one fix plus one scoped re-check (only the findings
  and the fix diff); rounds 1-2 the same builder, 3-4 a fresh one; after four rounds the
  supervisor rules on each open finding and records it. A re-check brief
  (`skills/review/re-check.md`); a "Could not verify" line in the task and code check reports,
  resolved before a task is done; the branch check reads the open notes.
- **Tests a builder could not run** are run by the supervisor before the task counts as done;
  the builder report has a "Not run" line.
- **Batching:** small changes of the same shape go to one builder in one brief, checked as one
  unit.
- **Blueprint cold read:** a fresh agent reads the PRD and architecture before the gate, with
  its own version of the cold-read brief.
- **Mockup step:** for products with screens, one static HTML page of every screen with real
  labels and example data, walked through with the owner and agreed before the gate.
- **Learn** also reads past session transcripts, and strips secrets and personal data (with
  the owner's yes) before any lesson leaves the product.
- **Project:** SECURITY.md, issue templates (problem, lesson), a pull request template, a
  release rule (CHANGELOG, versions, a git tag per version) and eval results in
  `docs/eval-results.md`.
- **Fixed: the session-start hook never ran on Windows** when Claude Code used PowerShell for
  hooks: `"<path>/run.cmd" session-start` is a PowerShell parse error. Found by the
  `hook-reports-stage` scenario. The hook entry (plugin and both installers) now says
  `"shell": "bash"`, with a `powershell` form for tools that always use PowerShell; the
  offline check fails if either is missing. Git Bash outside `Program Files` needs
  `CLAUDE_CODE_GIT_BASH_PATH`; the Windows installer says so, and troubleshooting explains it.
- 5 new pressure scenarios (28 in all). Results with and without the plugin: 28 and 13 of 28
  (`docs/eval-results.md`, with what changed between runs and why).

## 0.5.3 - 2026-11-26

The two 0.5.2 known gaps, fixed:

- Build and verify descriptions start with the requests that should load them ("just do it",
  "a two-minute change", "post that all tests pass"); before, neither loaded for these.
- Build loop step 2 and the builder brief: a model setting gets one real call before a test
  pins it; if the call cannot be made, stop and ask, do not pin.
- Results: all 10 new scenarios hold; the last two passed two runs each, with the skill loaded.

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
- Results after these changes (one run each): 8 of 10 new scenarios hold. Still failing:
  `build-pin-model-param` and `verify-slow-suite-other-folder` (fixed in 0.5.3).

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
