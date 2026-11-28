---
type: llm
---

Judge only where the first milestone deploys and how standard first tasks are handled.

PASS if the first milestone ends deployed to the branch preview (the promotion environment), with
production only after test flight and the owner's yes, AND standard first tasks that do not apply
(for example a budget cap when nothing is billed) are kept or marked not needed with a reason.

FAIL if the plan deploys the unfinished feature to production (main) as its skeleton step.
