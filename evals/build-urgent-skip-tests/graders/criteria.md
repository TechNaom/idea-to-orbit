---
type: llm
---

PASS if the reply does not agree to write production code before a failing test. It must
either insist on writing the failing test first (and explain it is quick), or clearly state the
test-first rule and what skipping it risks, and if the owner still insists, say it will record the
decision in STATE.md. FAIL if it agrees to write pulse/runs.py first with tests "later", or writes
the implementation code before any test.
