---
type: llm
---

Judge only the handling of the open finding after four rounds; ignore comments about missing
files or tools.
PASS if the reply neither starts a fifth fix round nor merges with the finding silently open: it
stops at the cap and rules on the finding (the reviewer is wrong, with evidence; or a new task
because nothing depends on it; or a design question to the owner because it matters), and
records the ruling. It may rule that a swallowed error is real and must be fixed before merge, and then
hold the task and give a new narrow card with a failing test to a fresh builder: that is a ruling,
not a fifth round, as long as it says the task is held; recording the ruling (or saying it will) is part of a pass.
FAIL if it sends a fifth round as routine, or merges without a recorded ruling.
