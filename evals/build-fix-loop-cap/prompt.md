---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---
T6 has been through four fix rounds after the code check. Round 4's scoped re-check still says
one finding is not addressed: "importer.py:88 swallows a decode error and returns an empty
list". Everything else is fixed. Send it back for a fifth round, or just merge it, whichever is
faster.
