#!/usr/bin/env bash
# A product for this case, for the session-start hook and the skills to read.
set -e
mkdir -p docs/orbit
cat > docs/orbit/STATE.md <<'STATE'
# Product state: Ledger Lite

Started: 2026-10-01

## Current

- Stage: assemble
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
| assemble | in progress | | |
| build | not started | | |
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
cat > docs/orbit/tasks.md <<'TASKS'
# Tasks: Ledger Lite

## M1 Skeleton

| ID | Task | Serves | Test (written first) | Done check | Depends on | Size | Issue |
|---|---|---|---|---|---|---|---|
| T1 | Repository, CI and `.env.example` | N1 | CI runs on a pull request | CI green | - | S | |
| T2 | Invoice import from CSV | R1 | `tests/test_import.py` | 3 rows imported | T1 | M | |

### T2 Invoice import from CSV

**Files:** `ledger/importer.py`, `tests/test_import.py`
**Steps:** write `test_imports_three_rows`; expect `ImportError`; write `import_csv(path)`.
**Done check:** `pytest -q tests/test_import.py`. Expect: `1 passed`.
TASKS
