# Tasks: <product name>

Version <n>, <YYYY-MM-DD>. Architecture: [architecture.md](architecture.md)

## Milestones

| Milestone | Leaves the product able to | Tasks |
|---|---|---|
| M1 Skeleton | <deploy and answer one request end to end> | T1-T5 |
| M2 | | |

## M1 Skeleton

| ID | Task | Serves | Test (written first) | Done check | Depends on | Size | Issue |
|---|---|---|---|---|---|---|---|
| T1 | Repository, CI and `.env.example` | N1 | CI runs on a pull request | CI is green on main | - | S | |
| T2 | Budget cap and alerts | N1 | Alert test fires | Cap and alerts visible in the console | T1 | S | |
| T3 | Walking skeleton deployed | R1 | Smoke test against the live URL | Smoke test passes | T2 | M | |

## Coverage

| Requirement | Tasks |
|---|---|
| R1 | T3 |

Gaps: <requirements with no task, or "none">
