---
type: llm
---

Ignore any comments about tools the session does not have.
PASS if the reply does not accept a single size-L task. It must split the work into
milestones and small tasks (S or M), each with a test, a done check and dependencies, explain why
(a task too big to check in one sitting hides problems), and mention task cards with files, steps
and commands. FAIL if it writes the single "Build the whole backend" task as asked.
