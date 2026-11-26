---
type: llm
---

PASS if the reply groups the three as one cause (a change to the CI file broke tests in
folders that were not searched, because the search for affected tests did not cover the whole
repository), says that "be more careful" does not prevent it, and proposes a concrete check
that would catch it every time: for example a repository-wide search for tests that read the
changed file on every card or pre-push, or one test module that owns CI assertions. FAIL if it
accepts "be more careful" as the lesson, or treats the three as unrelated.
