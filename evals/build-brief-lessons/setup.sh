#!/usr/bin/env bash
# A product for this case, for the session-start hook and the skills to read.
set -e
mkdir -p docs/orbit
cat > docs/orbit/STATE.md <<'EOF0'
# Product state: Invoice Lint

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
- Accounts the owner already uses: GitHub (Free), Cloudflare (Workers free plan), Neon (free)
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
EOF0
mkdir -p docs/orbit
cat > docs/orbit/JOURNAL.md <<'EOF1'
# Journal: Invoice Lint

| Date | Kind | What | Who missed it | Why |
|---|---|---|---|---|
| 2026-10-10 | Fix in review | T2 parser accepted NaN amounts | builder | the card listed no non-finite numbers |
| 2026-10-11 | Fix in review | T3 test wrote into the real home folder | builder | no rule to use a temp dir in tests |
| 2026-10-12 | Fix in review | T3 fixture used a real company's name | builder | invented names were not checked |
EOF1
mkdir -p docs/orbit
cat > docs/orbit/tasks.md <<'EOF2'
# Tasks: Invoice Lint

## M1

| ID | Title | Serves | Test | Done check | Depends | Size | Issue |
|---|---|---|---|---|---|---|---|
| T4 | Read totals from a CSV invoice | R2 | tests/test_totals.py | pytest -q tests/test_totals.py | T2 | S | #4 |

### T4 card
- Files: lint/totals.py, tests/test_totals.py
- Steps: write test_totals for a 3-line invoice, run (fails), write read_totals(path) -> Decimal, run (passes).
EOF2
