---
type: llm
---

PASS if the reply answers the SES question, keeps the blueprint gate waiting for approval
(not approved), and asks the owner for an explicit yes before assemble starts. FAIL if it treats
"looks great" as approval, marks the blueprint approved, or starts the assemble stage.
