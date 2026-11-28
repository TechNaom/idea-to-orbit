# PRD: <product name>

Version <n>, <YYYY-MM-DD>. Brief: [brief.md](brief.md)

## Users and their jobs
| User | Wants to | So that |
|---|---|---|
| <user> | <job> | <outcome> |

## Requirements

| ID | Requirement | Priority | Acceptance check |
|---|---|---|---|
| R1 | <the product must ...> | must | <how we test that it does> |
| R2 | | should | |

## Non-functional requirements

| ID | Area | Requirement | Acceptance check |
|---|---|---|---|
| N1 | Cost | <runs within X per month> | <billing alert never passes 80%> |
| N2 | Availability | | |
| N3 | Security and privacy | | |
| N4 | Performance | | |
| N5 | Release | <versioned, tagged; how a rollback works> | |
| N6 | Guardrails | <what the product may never do or decide on its own> | |
| N7 | Governance | <audit log, kill switch, who can change what; and for the AI builders: what agents may never do (merge to production, read secrets, add a vendor, weaken a test)> | |
| N8 | Token guard | <tokens per call and per day; what happens past the limit; and for the builders: tokens per task, logged in `token-ledger.md`> | |
| N9 | Budget guard | <spend cap per day and month; what stops at the cap; and for the builders: the plan or API budget, an estimate before each milestone, a clean stop at the limit> | |
| N10 | Evals | <the product's eval bars if it calls a model; and for the builders: first-pass task checks, fixes in review and tokens per task> | |

Every area above gets a requirement, or "not needed" with a reason (a product with no model
call needs no token guard; say so).

## Out of scope
- <not in this version>

## Success measures
| Measure | Target | By |
|---|---|---|
| <measure> | <number> | <date> |

## Risks and assumptions
| Risk or assumption | Impact | How we check or reduce it |
|---|---|---|

## Scope changes
Dated, newest first. A change that widens the scope adds new requirement IDs; it does not
rewrite approved or reconstructed ones.

| Date | Change | Requirement IDs | Owner's words |
|---|---|---|---|

## Open questions
- <question>
