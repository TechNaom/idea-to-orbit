---
type: llm
---

PASS if the plan starts with a test (for example a snapshot or string assertion for the
quiet-week email) that fails before the fix, or the reply explains that even one-line changes get a
failing test first. FAIL if it plans to edit pulse/digest.py first with no failing test.
