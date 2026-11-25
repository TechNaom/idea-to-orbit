# Deploy plan: Repo Pulse

Version 1, 2026-12-07. Release gate: [release.md](release.md)

## Where it runs

| Part | Provider and service | Scales to zero? | Limits (concurrency, timeout) |
|---|---|---|---|
| pulse | AWS Lambda, ap-south-1, Python 3.12, 256 MB | Yes | Concurrency 1, timeout 120 s |
| Scheduler | EventBridge Scheduler, `cron(30 2 ? * MON *)` UTC | Yes | 1 target, no retry (the function retries itself) |
| Email | Amazon SES, ap-south-1, verified sender | Yes | Production access, 1 recipient |
| Token and run lock | SSM Parameter Store, 2 standard parameters | n/a | - |
| Health check | GitHub Actions, `30 3 * * 1` UTC | Yes | Timeout 5 minutes |

## Cost guard

- Account plan and credits: standard AWS account; no credits used.
- Monthly cap: $2.
- Alerts: 25 / 50 / 80 / 100% and forecast, sent to the owner's email.
- Stop action at 100%: a budget action that sets the function's concurrency to 0.
- Expected monthly cost: $0.00.

## Silo

- Keys: one GitHub token used only by Repo Pulse; one AWS role only for Repo Pulse.
- Data: two SSM parameters under `/repo-pulse/`; nothing shared.
- Alerts: issues labelled `alert` in the Repo Pulse repository.

## Secrets

| Name | Stored in | Used by |
|---|---|---|
| `/repo-pulse/github-token` | SSM SecureString | pulse |
| `AWS_DEPLOY_ROLE_ARN` | GitHub secret | deploy workflow (OIDC, no long-lived keys) |
| `PULSE_GITHUB_TOKEN` | GitHub secret | deploy workflow, writes the SSM parameter |

## Release

- Backup tag: `stable-2026-12-07` at 5c1e9a0
- Deploy: GitHub Actions workflow `deploy`
- Rollback: `gh workflow run rollback.yml -f tag=stable-2026-12-07`

## Live

- Function: `repo-pulse` in ap-south-1
- Version: 1.0 (5c1e9a0)
- Smoke test: invoked once by hand at 14:12 IST; email received at 14:12; 4 repositories with
  news, 27 left out. Run time 36 s.
- Delivery confirmed: SES message id stored in the run lock; the email arrived in the inbox,
  not spam.
