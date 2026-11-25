# Runbook: <product name>

Updated <YYYY-MM-DD>. Deploy plan: [deploy-plan.md](deploy-plan.md)

## What healthy looks like
- <the job it does, how often, and how to confirm it was done>

## Watching

| Check | Runs on | Schedule | Alerts to |
|---|---|---|---|
| Health check (did it do its job?) | <its own trigger> | | |
| Cost report | | | |

## Self-healing

| Failure | Automatic action | Attempt cap | Spend cap | Then |
|---|---|---|---|---|
| <failure> | <retry, fallback> | <n> | <amount> | Alert the owner |

## Common problems

| Symptom | First check | Fix |
|---|---|---|

## Roll back
1. `<exact command>` to the last known good tag.
2. Confirm with the smoke test.

## Pause
- <how to stop it fully, and how to resume>

## Contacts and access
- <where the consoles, keys and alerts live>
