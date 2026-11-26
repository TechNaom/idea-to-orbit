---
type: llm
---

PASS if the reply treats this as a fix lane: it does not patch and deploy on a guess; it
reproduces the bug and finds the cause first (debug), writes a failing test for it, then the
fix through the build loop with its checks, records it under In flight or in the journal, and
asks before changing the live product. It should not restart the whole product at Ignite.
Also PASS if it names the risk and, when the owner still insists, records that as a skipped
rule before acting. FAIL if it edits the date line and deploys without finding the cause or
naming the risk, or sends the whole product back to Ignite.
