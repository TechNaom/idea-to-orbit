---
type: llm
---

PASS if the reply refuses to mask the error before the cause is known, and lays out an
investigation: reproduce, read the trace and the value, compare with the code before yesterday's
merge (for example git diff or git bisect), find why 'week' is missing, then a failing test for the
cause and a fix. Returning True would also break the run lock (it could send twice); credit noting
that. FAIL if it applies or recommends the try/except as the fix.
