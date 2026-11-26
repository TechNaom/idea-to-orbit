# Release gate: <product name> <version>

Date: <YYYY-MM-DD>. Commit: <sha>. Decision: **<go | no-go>**

## Requirements

| ID | Acceptance check | Result | Evidence |
|---|---|---|---|
| R1 | | pass | <command, output or CI link> |

## Checks

| Check | Result | Evidence |
|---|---|---|
| Full test suite and CI green on the release commit | | |
| CI jobs allowed to fail: each blocking, or with a reason and an owner | | <list them> |
| End-to-end flows on staging | | |
| Each outside dependency failed in turn | | |
| Burst of requests | | |
| No secrets in repository or history | | |
| Least-privilege keys | | |
| Every credential's expiry date recorded, with a warning before it | | |
| Dependency scan (blocking) | | |
| Enterprise: control mapping checked, no personal data or secrets in logs, passive scan of staging | | <or "startup profile"> |
| AI: eval suite on the release commit against the live model, every bar met | | <or "no model calls"> |
| AI: guardrail checks tested; spend metered and inside budget | | |
| Screens: browser tests for every screen and role, accessibility, phone width | | <or "no UI"> |
| Screens: the owner's screen-by-screen checklist, and what they found | | |
| Cost at expected load: <amount> | | |
| Cost at 10x load: <amount> | | |
| Rollback rehearsed on staging | | |

## Not tested
- <what, and why> (or "nothing")

## Must change before launch (no-go only)
- <item> → new task T<n>
