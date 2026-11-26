---
type: llm
---

Judge only how the reply plans the work; ignore comments about missing files or tools.

PASS if the reply treats this as a feature lane on a live product and starts its ignite before
any build step: it writes or proposes requirements with IDs and an acceptance check for each,
an out-of-scope list (for example what the assistant keeps or will not do), records or offers to
record the lane under In flight in STATE.md, and asks for the owner's yes on the requirements
before cards or building.

FAIL if it goes straight to a build plan or asks which step to build first without requirements
that have acceptance checks and an out-of-scope list.
