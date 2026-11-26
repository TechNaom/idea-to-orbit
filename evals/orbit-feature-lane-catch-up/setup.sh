#!/usr/bin/env bash
# A product for this case, for the session-start hook and the skills to read.
set -e
mkdir -p docs/orbit
cat > docs/orbit/STATE.md <<'STATE'
# Product state: Ledger Lite

Started: 2026-10-01

## Current

- Stage: orbit
- Status: approved
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
| blueprint | approved | owner | 2026-10-04 |
| assemble | approved | owner | 2026-10-05 |
| build | approved | owner | 2026-10-20 |
| test-flight | approved | owner | 2026-10-22 |
| launch | approved | owner | 2026-10-23 |
| orbit | approved | owner | 2026-10-24 |

## In flight

- none

## Open questions

- None.

## Log

- 2026-10-24 Orbit set up.
STATE
