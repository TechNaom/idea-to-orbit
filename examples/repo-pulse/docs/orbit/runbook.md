# Runbook: Repo Pulse

Updated 2026-12-14. Deploy plan: [deploy-plan.md](deploy-plan.md)

## What healthy looks like
- Every Monday by 08:05 IST, one email arrives listing last week's news.
- The SSM parameter `/repo-pulse/last-sent` holds this ISO week and an SES message id.

## Watching

| Check | Runs on | Schedule | Alerts to |
|---|---|---|---|
| Health check: was this week's email sent? | GitHub Actions (its own clock, not the AWS scheduler) | Monday 09:00 IST | Issue labelled `alert` |
| Token expiry warning (T12) | GitHub Actions | Daily 09:00 IST | Issue labelled `alert`, 7 days ahead |
| Cost | AWS Budgets | Continuous | Email at 25/50/80/100% and forecast |

Each was proven by a deliberate failure on 2026-12-07: schedule removed, bad token, two runs
at once.

## Self-healing

| Failure | Automatic action | Attempt cap | Spend cap | Then |
|---|---|---|---|---|
| GitHub API error | Wait 30 s, retry the whole collection | 1 retry | n/a | Exit without sending; health check alerts |
| A second run in the same week | Exit "already sent" | n/a | n/a | Nothing |
| Monthly cost passes $2 | Budget action sets concurrency to 0 | n/a | $2 | Email to the owner |

There is deliberately no automatic re-send: a wrong re-send is worse than a late email.

## Common problems

| Symptom | First check | Fix |
|---|---|---|
| No email, alert says 401 | Token expiry date in GitHub settings | Make a new fine-grained token (read-only: metadata, issues, actions; 1-year expiry), run `gh secret set PULSE_GITHUB_TOKEN`, then `gh workflow run deploy.yml` |
| No email, no run at all | EventBridge schedule exists and is enabled | `gh workflow run deploy.yml` recreates it |
| Email in spam | SES sender verification | Re-verify the sender; mark as "not spam" once |
| Email late | Lambda duration in CloudWatch | Over 60 s: check the repository count and the parallel limit |

## Send this week's email by hand
After fixing the cause: `aws lambda invoke --function-name repo-pulse --region ap-south-1 out.json`.
The run lock stops it sending twice.

## Roll back
1. `gh workflow run rollback.yml -f tag=<last stable tag>`
2. Confirm with a manual invoke.

## Pause
- Pause: `aws scheduler update-schedule ... --state DISABLED` (full command in `scripts/pause.sh`).
- Resume: `scripts/pause.sh --resume`.

## Contacts and access
- AWS account: ap-south-1; budget "repo-pulse".
- GitHub: repository settings for secrets; issues labelled `alert`.
