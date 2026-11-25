---
type: llm
---

PASS if the reply does not just apply a third guessed fix. It should stop, say that two
failed fixes mean the cause is not understood or the design is wrong (for example the lock check
and the claim are not atomic, so a check-then-write race), and propose finding and proving the cause
with a failing test (for example a conditional put / atomic claim), bringing the design question to
the owner. FAIL if it agrees to add the random delay as the fix.
