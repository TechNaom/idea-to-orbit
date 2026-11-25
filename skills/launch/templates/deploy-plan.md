# Deploy plan: <product name>

Version <n>, <YYYY-MM-DD>. Release gate: [release.md](release.md)

## Where it runs

| Part | Provider and service | Scales to zero? | Limits (concurrency, timeout) |
|---|---|---|---|

## Cost guard

- Account plan and credits: <plan, credit left, expiry>
- Monthly cap: <amount>
- Alerts: 25 / 50 / 80 / 100% and forecast, sent to <channel>
- Stop action at 100%: <what stops, or "not available on this provider">
- Expected monthly cost: <amount>

## Silo

- Keys: <which keys belong only to this product>
- Data: <database or project, only for this product>
- Alerts: <channel>

## Secrets

| Name | Stored in | Used by |
|---|---|---|

## Release

- Backup tag: `stable-<YYYY-MM-DD>` at <sha>
- Deploy: <CI workflow name>
- Rollback: `<exact command>`

## Live

- URL: <url>
- Version: <version>
- Smoke test: <result and evidence>
- Delivery confirmed: <what was checked>
