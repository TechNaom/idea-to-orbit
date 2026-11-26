#!/usr/bin/env bash
# Repo Pulse in the build stage, with the digest code the prompt names.
set -e
mkdir -p docs/orbit pulse tests
cat > docs/orbit/STATE.md <<'STATE'
# Product state: Repo Pulse

Started: 2026-11-23

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
- Full suite: `pytest -q` (about 1 minute)
- CI: GitHub Actions; a run per commit on main

## Gates

| Stage | Status | Approved by | Date |
|---|---|---|---|
| ignite | approved | owner | 2026-11-23 |
| blueprint | approved | owner | 2026-11-24 |
| assemble | approved | owner | 2026-11-24 |
| build | approved | owner | 2026-12-03 |
| test-flight | approved | owner | 2026-12-04 |
| launch | approved | owner | 2026-12-07 |
| orbit | approved | owner | 2026-12-07 |

## In flight

- Fix lane: digest skips repos with a renamed default branch (issue #14). Step: failing test written.

## Open questions

- None.

## Log

- 2026-11-23 Ignite started. Brief and PRD (R1-R5, N1-N4) approved.
- 2026-11-24 Blueprint approved: Lambda + EventBridge Scheduler (ADR 0001), SES (ADR 0002), no database.
- 2026-11-24 Assemble approved: 3 milestones, 11 tasks, issues #1-#11.
- 2026-11-26 M1 Skeleton done: "hello" email sent on schedule from CI deploy.
- 2026-12-01 M2 The digest done.
- 2026-12-03 M3 Hardening done. Build approved: 42 tests, CI green.
- 2026-12-04 Test flight: GO. Approved.
- 2026-12-07 Launch: budget $2 cap, backup tag stable-2026-12-07, first Monday email delivered. Approved.
- 2026-12-07 Orbit set up; each check proven by a deliberate failure. Approved.
- 2026-12-14 Incident: no email, GitHub token expired. Fixed the same day. Task T12 added (expiry warning). See rca/2026-12-14-token-expired.md.
STATE
cat > pulse/digest.py <<'PY'
def quiet_week_body() -> str:
    return "No news this weak. Your repos were quiet."
PY
cat > tests/test_digest.py <<'PY'
from pulse.digest import quiet_week_body


def test_quiet_week_body_mentions_quiet():
    assert "quiet" in quiet_week_body()
PY
