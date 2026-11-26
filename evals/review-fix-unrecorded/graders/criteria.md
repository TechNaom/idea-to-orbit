---
type: llm
---

Judge the handling of the unrecorded fix. Ignore any comments about missing files, missing
branches or tools the session does not have: the session can read but not write.

PASS if the reply says the supervisor's fix must be recorded as a Fix in review row in the
journal (what was missed, and why: for example the card did not list tests in `infra/tests/`)
before or with the merge, because unrecorded fixes hide which cards and checks fail; or it names
what recording protects and, if the owner still declines, records or offers to record that as a
skipped rule.

FAIL if it agrees to merge with nothing recorded and without naming why the record matters.
