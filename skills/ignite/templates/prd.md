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
| N7 | Governance | <audit log, kill switch, who can change what> | |
| N8 | Token guard | <tokens per call and per day; what happens past the limit> | |
| N9 | Budget guard | <spend cap per day and month; what stops at the cap> | |

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
