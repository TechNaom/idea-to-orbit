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

## Task cards

Cards for each milestone were written when that milestone started.

### T1 Repository, CI, `.env.example`

Serves: N3. Depends on: none. Size: S. Issue: #1

**Files**
- Create: `pyproject.toml`, `pulse/__init__.py`, `.env.example`, `.github/workflows/ci.yml`
- Test: `tests/test_smoke.py`

**Steps**
1. Write `tests/test_smoke.py::test_package_imports`: `import pulse` and check `pulse.__version__ == "0.1.0"`.
   Run `pytest -q`. Expect: `1 failed ... ModuleNotFoundError: No module named 'pulse'`.
2. Create `pyproject.toml` (Python 3.12, pytest) and `pulse/__init__.py` with `__version__ = "0.1.0"`.
   Run `pytest -q`. Expect: `1 passed`.
3. Add `.github/workflows/ci.yml`: on pull request and push to main, Python 3.12, `pip install -e .[test]`, `pytest -q`.
4. Add `.env.example` with `PULSE_GITHUB_TOKEN=<read-only fine-grained token>` and `PULSE_TO_EMAIL=<you@example.com>`.
5. Commit, push, open a pull request.

**Done check:** the CI run on the pull request is green, and `git ls-files | grep -c '^\.env$'` prints `0`.

### T2 AWS budget: $2 cap, alerts and forecast

Serves: N1. Depends on: T1. Size: S. Issue: #2

**Files**
- Create: `infra/budget.json`, `scripts/check_budget.py`
- Test: `tests/test_budget.py`

**Interfaces**
- `check_budget(budget: dict) -> list[str]`: the problems found; empty when the budget is right.

**Steps**
1. Write `tests/test_budget.py::test_flags_missing_alerts`: a budget of $2 with only a 100% alert returns
   `["missing alert at 25%", "missing alert at 50%", "missing alert at 80%", "missing forecast alert"]`.
   Run `pytest tests/test_budget.py -q`. Expect: `1 failed ... ImportError`.
2. Write `scripts/check_budget.py`. Run it. Expect: `1 passed`.
3. Write `tests/test_budget.py::test_accepts_full_budget` against `infra/budget.json`. Red, then green.
4. Create the budget: `aws budgets create-budget --account-id <id> --cli-input-json file://infra/budget.json`.

**Done check:** `python scripts/check_budget.py --live` prints `budget repo-pulse: $2.00, 5 alerts, ok`.

### T3 Lambda that sends a "hello" email with SES

Serves: R4. Depends on: T2. Size: M. Issue: #3

**Files**
- Create: `pulse/handler.py`, `pulse/mailer.py`
- Test: `tests/test_mailer.py`, `tests/fakes.py`

**Interfaces**
- `send_email(ses, to: str, subject: str, text: str, html: str) -> str`: the SES message id. Raises `SendFailed` on any SES error.
- `handler(event, context) -> dict`: `{"status": "sent", "message_id": ...}`.

**Steps**
1. Write `tests/test_mailer.py::test_sends_one_email` with `FakeSES` from `tests/fakes.py`: one call, the right recipient, returns the fake id.
   Run `pytest tests/test_mailer.py -q`. Expect: `1 failed ... ImportError: cannot import name 'send_email'`.
2. Write `pulse/mailer.py`. Expect: `1 passed`.
3. Write `test_wraps_ses_error`: an SES error raises `SendFailed` with the SES error code. Watch it fail, then make it pass.
4. Write `pulse/handler.py` sending "hello". Test `tests/test_handler.py::test_hello`. Run `pytest -q`: all pass.

**Done check:** `aws lambda invoke --function-name repo-pulse out.json` returns `"status": "sent"`, and the email is in the inbox.

**Watch out:** SES sandbox only sends to verified addresses; request production access in this task.

### T4 Scheduler at Mon 02:30 UTC, deploy from CI

Serves: R4. Depends on: T3. Size: M. Issue: #4

**Files**
- Create: `template.yaml` (AWS SAM), `.github/workflows/deploy.yml`
- Test: `tests/test_template.py`

**Steps**
1. Write `tests/test_template.py::test_schedule_and_limits`: the template has the schedule `cron(30 2 ? * MON *)`, concurrency 1, timeout 120, memory 256.
   Run it. Expect: `1 failed ... FileNotFoundError: template.yaml`.
2. Write `template.yaml`. Expect: `1 passed`. Run `pytest -q`: all pass.
3. Write `deploy.yml`: on push to main, OIDC role `AWS_DEPLOY_ROLE_ARN`, `sam deploy`. Run it once with `--no-execute-changeset`. Expect: a change set listing the function, the schedule and the role.

**Done check:** the scheduled "hello" arrives on Monday at 08:00 IST.

### T5 New issues in the last 7 days, pull requests excluded

Serves: R1. Depends on: T4. Size: S. Issue: #5

**Files**
- Create: `pulse/issues.py`
- Test: `tests/test_issues.py`, fixture `tests/fixtures/issues.json`

**Interfaces**
- `new_issues(gh, repo: str, since: datetime) -> list[Issue]`: issues opened at or after `since`, oldest first.

**Steps**
1. Write `tests/test_issues.py::test_lists_issues_opened_in_window`: the fixture has 3 issues in the window, 1 before it.
   Run `pytest tests/test_issues.py -q`. Expect: `1 failed ... ImportError: cannot import name 'new_issues'`.
2. Write `pulse/issues.py`. Expect: `1 passed`.
3. Write `test_excludes_pull_requests`: add 1 pull request (it has a `pull_request` key) to the fixture; still 3. Watch it fail, then filter.
   Suite: `15 passed`.
4. Write `test_old_issue_with_new_comment_is_left_out`. Red, then green. Suite: `16 passed`.

**Done check:** a real run against your account lists this week's issues and no pull requests.

**Watch out:** the issues API returns pull requests too; `since` filters on update time, so check `created_at` as well.

### T6 Failed CI runs on default branches

Serves: R2. Depends on: T4. Size: S. Issue: #6

**Files**
- Create: `pulse/runs.py`. Test: `tests/test_runs.py`, fixture `tests/fixtures/runs.json`

**Interfaces**
- `failed_runs(gh, repo: str, branch: str, since: datetime) -> list[Run]`

**Steps**
1. Write `test_only_default_branch`: failures on `main` and on `feature-x`; only `main` is listed. Expect first: `1 failed ... ImportError`.
2. Write `pulse/runs.py`. Expect: `1 passed`.
3. Write `test_ignores_cancelled`: a cancelled run is not a failure. Red, then green. Run `pytest -q`: all pass.

**Done check:** a real run matches the failures shown in the Actions tab for the last 7 days.

### T7 New stars per repository

Serves: R3. Depends on: T4. Size: S. Issue: #7

**Files**
- Create: `pulse/stars.py`. Test: `tests/test_stars.py`, fixture `tests/fixtures/stars.json`

**Interfaces**
- `new_stars(gh, repo: str, since: datetime) -> int`

**Steps**
1. Write `test_counts_stars_in_window`: 5 stars, 2 older than 7 days; returns 3. Expect first: `1 failed ... ImportError`.
2. Write `pulse/stars.py` using the `application/vnd.github.star+json` media type for star times. Expect: `1 passed`.
3. Write `test_pages_through_results`: 120 stars over 2 pages. Red, then green. Run `pytest -q`: all pass.

**Done check:** a real run matches the repository's star history for the week.

### T8 Email layout, quiet-week email, parallel collection

Serves: R4, R5, N2. Depends on: T5, T6, T7. Size: M. Issue: #8

**Files**
- Create: `pulse/digest.py`, `pulse/collect.py`
- Change: `pulse/handler.py`
- Test: `tests/test_digest.py`, `tests/test_collect.py`, snapshots in `tests/snapshots/`

**Interfaces**
- `collect(gh, repos: list[str], since: datetime, limit: int = 5) -> list[RepoNews]`
- `render(news: list[RepoNews], week: str) -> tuple[str, str]`: plain text and HTML.

**Steps**
1. Write `test_digest.py::test_busy_week_snapshot` and `test_quiet_week_snapshot`. Expect first: `2 failed ... ImportError`.
2. Write `pulse/digest.py`. Expect: `2 passed`; review both snapshots by eye before accepting them.
3. Write `test_collect.py::test_hundred_repos_under_two_minutes` with a fake client that sleeps 0.5 s per call. Expect first: a failure on time.
4. Write `pulse/collect.py` with at most 5 repositories at a time. Expect: `passed in` under 120 s.
5. Wire `collect` and `render` into `handler.py`. Run `pytest -q`: all pass.

**Done check:** the real email reads well on a phone and on a desktop.

**Watch out:** repositories with no news are left out of the email; the quiet-week email still sends.

### T9 Run lock: one email per ISO week

Serves: N4. Depends on: T8. Size: S. Issue: #9

**Files**
- Create: `pulse/lock.py`
- Change: `pulse/handler.py`
- Test: `tests/test_lock.py`

**Interfaces**
- `claim_week(ssm, week: str) -> bool`: true only for the first caller in that week.
- `record_sent(ssm, week: str, message_id: str) -> None`

**Steps**
1. Write `test_lock.py::test_two_runs_send_one_email`: two handlers started together with a shared fake SSM; exactly one `send_email` call.
   Run it. Expect: `1 failed ... assert 2 == 1`.
2. Write `pulse/lock.py` using a conditional put on `/repo-pulse/last-sent`, and call it first in the handler. Expect: `1 passed`.
3. Write `test_second_run_says_already_sent`. Red, then green. Run `pytest -q`: all pass.

**Done check:** a second manual invoke in the same week returns `"status": "already sent"`.

**Watch out:** claim the week before collecting, and record the message id only after SES accepts the email.

### T10 Health check at Mon 03:30 UTC, alert issue

Serves: N4. Depends on: T9. Size: M. Issue: #10

**Files**
- Create: `scripts/health_check.py`, `.github/workflows/health.yml`
- Test: `tests/test_health.py`

**Interfaces**
- `check(last_sent: dict | None, week: str) -> str | None`: the alert text, or none when this week was sent.

**Steps**
1. Write `test_missing_record_alerts`: no record for this week returns an alert naming the week. Expect first: `1 failed ... ImportError`.
2. Write `scripts/health_check.py`. Expect: `1 passed`.
3. Write `test_one_alert_per_day`: an open alert issue from today means no new issue. Red, then green. Run `pytest -q`: all pass.
4. Write `health.yml` on its own schedule, `30 3 * * 1`, which opens an issue labelled `alert`.

**Done check:** with the schedule disabled on purpose, Monday's health check opens an alert issue.

### T11 Backup tag and rollback workflow

Serves: N4. Depends on: T10. Size: S. Issue: #11

**Files**
- Create: `.github/workflows/rollback.yml`, `scripts/pause.sh`
- Change: `.github/workflows/deploy.yml` (tag `stable-<date>` after a healthy deploy)
- Test: `tests/test_workflows.py`

**Steps**
1. Write `test_rollback_takes_a_tag_input`: `rollback.yml` is manual only, takes `tag`, and deploys that tag. Expect first: `1 failed ... FileNotFoundError`.
2. Write `rollback.yml`. Expect: `1 passed`.
3. Write `test_deploy_tags_after_smoke_test`: the tag step comes after the smoke test step. Red, then green. Suite: `42 passed`.
4. Rehearse on staging: deploy, then `gh workflow run rollback.yml -f tag=<previous tag>`.

**Done check:** the rehearsed rollback finishes in under a minute, and a manual invoke works on the old version.

### T12 Warn 7 days before the GitHub token expires

Serves: N4. Depends on: T10. Size: S. Issue: #19. Added after the incident on 2026-12-14.

**Files**
- Create: `scripts/token_expiry.py`, `.github/workflows/token-expiry.yml`
- Test: `tests/test_token_expiry.py`

**Interfaces**
- `expiry_warning(expires_at: datetime | None, now: datetime) -> str | None`

**Steps**
1. Write `tests/test_token_expiry.py::test_warns_seven_days_ahead`: a token expiring in 6 days returns a warning with the date. Expect first: `1 failed ... ImportError`.
2. Write `scripts/token_expiry.py`, reading the `github-authentication-token-expiration` response header. Expect: `1 passed`.
3. Write `test_no_expiry_is_quiet` and `test_eight_days_is_quiet`. Red, then green. Run `pytest -q`: all pass.
4. Write `token-expiry.yml`, daily at 03:30 UTC, opening an issue labelled `alert`.

**Done check:** with a short-lived test token, the warning issue opens on the next daily run.
