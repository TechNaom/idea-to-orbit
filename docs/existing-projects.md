# Existing projects

Idea to Orbit works on products that already have code, or are already live. You do not
have to start from Ignite with a blank page.

## The idea

Claude reads what exists and writes the documents a stage would have produced, from the
code and history, then asks you to confirm them. Confirming them passes those gates. From
there, the product moves on like any other.

## Steps

The full steps are in the ignite skill, under **Existing product**; `/orbit` starts them by
itself when a repository has code but no `docs/orbit/STATE.md`. In short:

```text
You: /orbit
     This product already exists. Catch up the docs from the code.

AI:  Read the repository: 4,200 lines of Python, 63 tests, a deploy workflow,
     a live Lambda. Wrote, marked "reconstructed":
       - brief.md and prd.md: what it does today (R1-R6), from code and README
       - architecture.md: current parts and diagrams, from code and infra files
       - adr/0001-0003: decisions I can see in the code, with "why" as a
         question for you where the reason is not written down
     Gaps found: no rollback written down, no alert when the job fails.
     Is this an accurate picture of the product today?
```

Claude also fills the **Settings** in `STATE.md` from the repository (the code host, the
branches, who builds, the test commands and how long the full suite takes) and marks what it
inferred. If the product already keeps its own plan, task list, decision records or journal,
`STATE.md` points to them and the stages use them as they are; Claude writes an orbit
document only where nothing covers it.

When you confirm, Claude records Ignite and Blueprint as approved and suggests where to go
next:

| The product is | Go to |
|---|---|
| Code but not deployed | Assemble, for the missing work, then Build |
| Live without monitoring | Orbit setup |
| Live, with a new feature to add | A feature lane (see [Concepts](concepts.md#lanes)) |

## Adding a feature to a live product

Run a stage for just the change:

```text
You: /orbit ignite - new feature: weekly summary for teams, not only me
```

The feature gets its own requirement IDs (continuing the numbering), its own ADRs if it
needs new decisions, and its own tasks. The live product keeps running; the change goes
through Test flight before it reaches users.

## Rules for live products

- Nothing that is already working is changed without your approval.
- A backup tag is taken before any change goes live.
- The release gate runs on the change, as for a new product.
