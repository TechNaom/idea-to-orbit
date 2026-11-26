# Tasks: <product name>

Version <n>, <YYYY-MM-DD>. Architecture: [architecture.md](architecture.md)

## Milestones

| Milestone | Leaves the product able to | Tasks |
|---|---|---|
| M1 Skeleton | <deploy and answer one request end to end> | T1-T5 |
| M2 | | |

## M1 Skeleton

| ID | Task | Serves | Test (written first) | Done check | Depends on | Size | Issue |
|---|---|---|---|---|---|---|---|
| T1 | Repository, CI and `.env.example` | N1 | CI runs on a pull request | CI is green on the work branch | - | S | |
| T2 | Budget cap and alerts | N1 | Alert test fires | Cap and alerts visible in the console | T1 | S | |
| T3 | Walking skeleton deployed | R1 | Smoke test against the live URL | Smoke test passes | T2 | M | |

## Coverage

| Requirement | Tasks |
|---|---|
| R1 | T3 |

Gaps: <requirements with no task, or "none">

## Task cards

### T1 Repository, CI and `.env.example`

Serves: N1. Depends on: none. Size: S. Issue: <#>

**Files**
- Create: `<path>`
- Change: `<path>`
- Test: `<tests/path>`

**Tests that read these files:** <every existing test that imports, loads or asserts on a file
above, from a repository-wide search, or "none">

**Interfaces**
- `<name(args) -> result>`: <what it does, and what it raises or returns on failure>

**Steps**
1. Write the test `<tests/path>::<test_name>`: <what it asserts>.
   Run `<command>`. Expect: `<the failing line, e.g. 1 failed ... NameError: name 'x' is not defined>`.
2. Write `<path>`: <the smallest code that passes>.
   Run `<command>`. Expect: `<e.g. 1 passed>`.
3. Run the whole suite: `<command>`. Expect: `<e.g. 12 passed>`.
4. Commit: `<message>`.

**Done check:** `<command>`. Expect: `<output>`.

**Also, for this kind of task** (delete what does not apply):
- A screen: browser test `<path>` for each role in the screen list (opens, refuses, key controls).
- A model call: eval case `<name>` with bar `<value>`, and the guardrail's failing test.
- A CI change: a test that reads the CI file and fails if the change is undone.

**Watch out:** <edge cases and failure paths from architecture.md>
