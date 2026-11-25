# Release gate: Repo Pulse 1.0

Date: 2026-12-04. Commit: 5c1e9a0. Decision: **go**

## Requirements

| ID | Acceptance check | Result | Evidence |
|---|---|---|---|
| R1 | 3 issues + 1 pull request fixture lists exactly 3 | pass | `pytest tests/test_issues.py` 4 passed; staging email lists this week's 6 issues |
| R2 | Failed runs on main only | pass | `pytest tests/test_runs.py` 3 passed; staging email matches the Actions tab (2 failures) |
| R3 | 5 stars, 2 old, shows 3 | pass | `pytest tests/test_stars.py` 2 passed |
| R4 | Monday 08:00-08:05 IST; quiet repositories left out | pass | Staging schedule moved to Thursday 08:00 IST for the test: email at 08:00:41; 27 of 31 repositories correctly left out |
| R5 | Quiet-week email | pass | Snapshot test; staging run against an empty fixture account |
| N1 | Budget and alerts exist; cost $0.00 | pass | `scripts/check_budget.py`: cap $2, 5 alerts; Cost Explorer $0.00 month to date |
| N2 | Under 2 minutes for 100 repositories | pass | 31 real repositories: 38 s. 100-repository fixture: 71 s |
| N3 | Read-only token; no secrets in repository | pass | Token permissions: metadata, issues, actions, all read-only. Secret scan of history: clean |
| N4 | One email per week; alert within 1 hour | pass | Two invokes together: 1 email, second logged "already sent". Disabled schedule: alert issue at 09:00 IST |

## Checks

| Check | Result | Evidence |
|---|---|---|
| Full test suite and CI green | pass | 42 passed; CI run "test" #31 green on 5c1e9a0 |
| End-to-end flows on staging | pass | Staging stack, own SES sender, own token |
| Each outside dependency failed in turn | pass | GitHub API blocked: one retry, then exit, no email, alert. SES sandbox reject: exit, alert |
| Burst of requests | pass | 5 invokes within 2 seconds: 1 email |
| No secrets in repository or history | pass | Secret scan clean |
| Least-privilege keys | pass | Role allows 2 parameters, 1 sender; nothing else |
| Dependency scan | pass | No known vulnerabilities |
| Cost at expected load: $0.00 | pass | Free tiers |
| Cost at 10x load: $0.01 | pass | 50 emails a month |
| Rollback rehearsed on staging | pass | Rolled back to the previous tag in 40 seconds; "hello" email received after |

## Not tested
- An account with more than 100 repositories: the test account has 31, and the fixture
  covers 100. GitHub's rate limit leaves room for about 1,500.
