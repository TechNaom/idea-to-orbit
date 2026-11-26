# Journal: <product name>

Every change and every roadblock, newest first. `STATE.md` says where the product is; this
file says what happened on the way and what it taught. The learn skill reads it.

| When | Kind | What | Commit |
|---|---|---|---|
| <YYYY-MM-DD HH:MM> | Roadblock | **<what went wrong, in one line>.** Cause: <the root cause, with the evidence>. Cleared: <what changed>. Lesson: <the rule or check that would have caught it>. | <hash or -> |
| <YYYY-MM-DD HH:MM> | Fix in review | **<task ID>: <what the checks or the supervisor fixed>.** Missed by: <builder, task check, code check>. Why: <the card was unclear, the check did not look there ...>. | <hash> |
| <YYYY-MM-DD HH:MM> | Change | **<what changed>** (<task ID or lane>). <why, in one line>. Evidence: <the check and its result>. | <hash> |
| <YYYY-MM-DD HH:MM> | Decision | **<what the owner decided>.** <options and the reason, or a link to the ADR>. | - |

Kinds: Change, Fix in review, Roadblock, Decision, Skipped rule (the owner chose to skip a
rule: which one, what it protects, and why).
