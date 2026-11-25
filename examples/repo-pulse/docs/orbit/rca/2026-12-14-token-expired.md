# Incident: no Monday email, GitHub token expired

Date: 2026-12-14. Status: fixed

## What happened
- 02:30 UTC (08:00 IST): the scheduler started the run. GitHub returned `401 Bad credentials`.
- 02:30:31 UTC: the run retried once, got 401 again, and exited without sending, as designed.
- 03:30 UTC (09:00 IST): the health check found no "sent" record for this week and opened
  alert issue #18 with the last error line.
- 05:40 UTC (11:10 IST): the owner made a new token; CI redeployed.
- 05:50 UTC (11:20 IST): a manual invoke sent this week's email.

## Impact
This week's email arrived 3 hours 20 minutes late. Nothing else was affected.

## Root cause
The GitHub token was reused from an older script and had a 30-day expiry. It expired on
2026-12-13. Evidence: the Lambda log line `GET /user/repos -> 401`, and the token's expiry
date on the GitHub settings page.

## Why it was not caught earlier
Nothing watched the token's expiry date. The release gate checked the token's permissions,
not its lifetime.

## Fix
- New fine-grained token, read-only, 1-year expiry, used only by Repo Pulse.
- Test that reproduces it: `tests/test_token_expiry.py::test_warns_seven_days_ahead`.
- Change: task T12, pull request #20 (daily expiry check, warning issue 7 days ahead).

## Prevention
- The daily token check warns 7 days before expiry (T12).
- The release checklist now asks for every credential's expiry date, not only its scopes.
