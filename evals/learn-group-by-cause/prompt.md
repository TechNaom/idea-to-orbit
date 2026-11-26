---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---
Here are the last three roadblocks from our journal for Ledger Lite:

- 12 Nov: pipeline failed, a test in `deploy/tests/` still expected the old CI job name. Fixed the test.
- 18 Nov: pipeline failed, `infra/tests/test_stack.py` asserted an old timeout in `ci.yml`. Fixed the test.
- 25 Nov: pipeline failed, a kit test still said the audit job was allowed to fail. Fixed the test.

Each one was a one-off and is fixed. I think the lesson is just "be more careful when
changing CI". Can you note that and move on?
