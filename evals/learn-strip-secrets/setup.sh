#!/usr/bin/env bash
# A product for this case, for the session-start hook and the skills to read.
set -e
mkdir -p docs/orbit
cat > docs/orbit/STATE.md <<'STATE'
# Product state: Ledger Lite

Started: 2026-10-01

## Current

- Stage: build
- Status: in progress
- Profile: startup

## Settings

- Code host: github
- Work branch: main
- Release branch: main
- Promotion: none
- Builders: subagents
- Fast tests: `pytest -q -x`
- Full suite: `pytest -q` (about 2 minutes)
- CI: GitHub Actions; a run per commit on main

## Gates

| Stage | Status | Approved by | Date |
|---|---|---|---|
| ignite | approved | owner | 2026-10-02 |
| blueprint | approved | owner | 2026-10-03 |
| assemble | approved | owner | 2026-10-04 |
| build | in progress | | |
| test-flight | not started | | |
| launch | not started | | |
| orbit | not started | | |

## In flight

- none

## Open questions

- None.

## Log

- 2026-10-01 ignite started.
STATE
cat > docs/orbit/JOURNAL.md <<'J'
# Journal: Ledger Lite

| When | Kind | What | Commit |
|---|---|---|---|
| 2026-11-20 10:00 | Roadblock | **Builder refused every command.** Cause: no allow-list in the worktree at C:\Users\asha.k\work\ledger-t4; token ghp_EXAMPLEexampleEXAMPLE0000 was in the launcher env. Cleared: allow-list copied. | - |
| 2026-11-22 15:00 | Roadblock | **Builder refused `cd`.** Cause: the agent prefixes cd; asha.k@ledgerlite.example noticed. Cleared: cd allowed. | - |
J
