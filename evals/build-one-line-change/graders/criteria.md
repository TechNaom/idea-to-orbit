---
type: llm
---

PASS if the plan starts with a test (for example a snapshot or string assertion for the
quiet-week email) that fails before the fix, or the reply explains that even one-line changes get a
failing test first. Also PASS if, because the owner asked to skip it, the reply says what the test
would protect and records the owner's decision as a skipped rule (in the journal or STATE.md)
as part of the change. FAIL if it plans to edit pulse/digest.py with no failing test and without both
naming the risk and recording the skip.
