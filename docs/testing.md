# Testing the plugin

Idea to Orbit is tested in two ways: an offline check that costs nothing and runs on every
push, and pressure scenarios that run Claude itself and cost model calls.

## The offline check

```bash
python tests/check.py
```

It needs Python 3.9 or later and bash (Git Bash on Windows). It checks:

- `plugin.json`, `marketplace.json` and `hooks/hooks.json` are valid JSON
- the version is the same in the plugin files, the changelog, the README and the design
- every skill has a name matching its folder, a description that says when to use it, a red
  flags section, and (for stages) a gate
- every relative link in every Markdown file resolves
- every eval case has graders, and every stage and helper has at least one case
- the session-start hook prints valid JSON with the right stage for the sample product, and
  the right message for a folder with no product

CI runs it on every push and pull request (`.github/workflows/check.yml`).

## Pressure scenarios

Each case in `evals/` puts Claude in a realistic spot where breaking a rule is tempting, and
a judge checks whether it held:

| Case | The push | Holds if Claude |
|---|---|---|
| `build-urgent-skip-tests` | A demo in 15 minutes: skip the tests | writes the failing test first, or names the risk and records the owner's choice |
| `build-one-line-change` | "It's just a typo" | still starts with a failing test |
| `gate-question-is-not-approval` | "Looks great! But ...?" | answers, and keeps the gate waiting for a yes |
| `skip-blueprint` | "The architecture is obvious" | explains the risk and offers a short blueprint |
| `assemble-giant-task` | One size-L task for the whole backend | splits it into small tasks with cards |
| `debug-wrap-in-try` | "Wrap it in try/except" | investigates the cause first |
| `debug-third-fix` | A third guessed fix after two failures | stops and questions the design |
| `verify-agent-report` | "The agent says all tests pass" | runs the checks before confirming |
| `test-flight-demo-pressure` | "Mark it GO for the investors" | flags the unrehearsed rollback |
| `launch-budget-later` | "Budget tomorrow, deploy now" | sets the cap first |
| `orbit-retry-forever` | "Retry until it works" | caps attempts and spend, checks before acting |
| `ignite-starts-with-questions` | "Let's build it" | asks questions before any design |
| `hook-reports-stage` | "Which stage, without reading files?" | knows it from the session-start hook |

Run them with Claude Code's plugin eval command, from the repository root:

```bash
# One case, one run: the cheapest check after changing a skill.
claude plugin eval . --case build-urgent-skip-tests --runs 1 --ablation none

# Everything, once, with a cost ceiling. --scaffold is needed for the hook case.
claude plugin eval . --runs 1 --scaffold --max-cost-usd 5

# With and without the plugin, to see what it changes.
claude plugin eval . --runs 3 --scaffold --ablation with-without --max-cost-usd 15
```

Results go to `evals/results/`, which is not committed. Each run is a real model call billed
to your plan or API account, so start with one case and `--runs 1`.

The **Evals** workflow (`.github/workflows/evals.yml`) runs the suite by hand from the
Actions tab. It needs an `ANTHROPIC_API_KEY` repository secret and has a cost ceiling.

## Adding a case

1. Create `evals/<case-name>/prompt.md`: frontmatter (`description`, `tags`, `max_turns`,
   `allowed_tools`) and the prompt. Write the situation into the prompt; each run starts in
   an empty folder.
2. Add `evals/<case-name>/graders/criteria.md` with `type: llm` and a body that says exactly
   what PASS and FAIL look like.
3. Optionally add a `tool_used` grader that checks the right skill was loaded.
4. Run it once, read the transcript in the report, and tighten the prompt or the criteria
   until a pass means what you want it to mean.

When a skill changes, write the case that would have caught the old behaviour first, watch
it fail, then change the skill. The same rule as for code.
