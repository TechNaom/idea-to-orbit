# Tasks: Repo Pulse

Version 1, 2026-11-24. Architecture: [architecture.md](architecture.md)

## Milestones

| Milestone | Leaves the product able to | Tasks |
|---|---|---|
| M1 Skeleton | Send a "hello" email on schedule, deployed from CI | T1-T4 |
| M2 The digest | Send the real Monday email | T5-T8 |
| M3 Hardening | Never send twice, alert when it fails, roll back in one step | T9-T11 |

## M1 Skeleton

| ID | Task | Serves | Test (written first) | Done check | Depends on | Size | Issue | Status |
|---|---|---|---|---|---|---|---|---|
| T1 | Repository, CI, `.env.example` | N3 | CI runs tests on a pull request | CI green on main | - | S | #1 | done |
| T2 | AWS budget: $2 cap, alerts 25/50/80/100% and forecast | N1 | Script confirms the budget and its 5 alerts | Visible in the console | T1 | S | #2 | done |
| T3 | Lambda that sends a "hello" email with SES | R4 | Unit test with a fake SES client | Email received from a manual invoke | T2 | M | #3 | done |
| T4 | Scheduler at Mon 02:30 UTC, deploy from CI | R4 | Deploy workflow dry run | Scheduled "hello" received on time | T3 | M | #4 | done |

## M2 The digest

| ID | Task | Serves | Test (written first) | Done check | Depends on | Size | Issue | Status |
|---|---|---|---|---|---|---|---|---|
| T5 | New issues in the last 7 days, pull requests excluded | R1 | Fixture of 3 issues and 1 pull request lists 3 | Real run lists this week's issues | T4 | S | #5 | done |
| T6 | Failed CI runs on default branches | R2 | Fixture with main and a feature branch lists only main | Real run matches the Actions tab | T4 | S | #6 | done |
| T7 | New stars per repository | R3 | Fixture of 5 stars, 2 old, shows 3 | Real run matches star history | T4 | S | #7 | done |
| T8 | Email layout, quiet-week email, parallel collection (5 at a time) | R4, R5, N2 | Snapshot test of both emails; 100-repository fixture under 2 minutes | Real email reads well on phone and desktop | T5, T6, T7 | M | #8 | done |

## M3 Hardening

| ID | Task | Serves | Test (written first) | Done check | Depends on | Size | Issue | Status |
|---|---|---|---|---|---|---|---|---|
| T9 | Run lock: one email per ISO week | N4 | Two runs started together send one email | A second manual invoke exits "already sent" | T8 | S | #9 | done |
| T10 | Health check workflow at Mon 03:30 UTC, alert issue | N4 | A missing "sent" record opens an issue (fixture) | A disabled schedule raises an alert | T9 | M | #10 | done |
| T11 | Backup tag and rollback workflow | N4 | Rollback dry run on staging | Rollback rehearsed in under 1 minute | T10 | S | #11 | done |

## Added later

| ID | Task | Serves | Test (written first) | Done check | Depends on | Size | Issue | Status |
|---|---|---|---|---|---|---|---|---|
| T12 | Warn 7 days before the GitHub token expires (from incident 2026-12-14) | N4 | A token expiring in 6 days opens a warning issue (fixture) | Warning seen with a short-lived test token | T10 | S | #19 | done |

## Coverage

| Requirement | Tasks |
|---|---|
| R1 | T5 |
| R2 | T6 |
| R3 | T7 |
| R4 | T3, T4, T8 |
| R5 | T8 |
| N1 | T2 |
| N2 | T8 |
| N3 | T1 |
| N4 | T9, T10, T11, T12 |

Gaps: none.
