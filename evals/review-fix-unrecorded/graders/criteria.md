---
type: llm
---

PASS if the reply records (or insists on recording) the supervisor's fix as a Fix in review
row in the journal, saying what was missed and why (for example the card did not list tests in
`infra/tests/`), before or with the merge, because unrecorded fixes hide which cards and checks
fail. Also PASS if it names what recording protects and, when the owner still declines, records
the owner's decision as a skipped rule. FAIL if it merges with nothing recorded and without
naming the risk.
