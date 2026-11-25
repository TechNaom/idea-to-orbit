# Release gate: <product name> <version>

Date: <YYYY-MM-DD>. Commit: <sha>. Decision: **<go | no-go>**

## Requirements

| ID | Acceptance check | Result | Evidence |
|---|---|---|---|
| R1 | | pass | <command, output or CI link> |

## Checks

| Check | Result | Evidence |
|---|---|---|
| Full test suite and CI green | | |
| End-to-end flows on staging | | |
| Each outside dependency failed in turn | | |
| Burst of requests | | |
| No secrets in repository or history | | |
| Least-privilege keys | | |
| Every credential's expiry date recorded, with a warning before it | | |
| Dependency scan | | |
| Cost at expected load: <amount> | | |
| Cost at 10x load: <amount> | | |
| Rollback rehearsed on staging | | |

## Not tested
- <what, and why> (or "nothing")

## Must change before launch (no-go only)
- <item> → new task T<n>
