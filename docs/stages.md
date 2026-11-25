# Stage reference

For each stage: how to start it, what it needs, what it writes, and what its gate checks.
The full instructions Claude follows are in `skills/<stage>/SKILL.md`. The sample product in
[examples/repo-pulse](../examples/repo-pulse/) shows every output filled in.

## 1. Ignite

| | |
|---|---|
| Start | `/orbit` on a new product, or "let's ignite a new product: ..." |
| Needs | The idea, in any form |
| Writes | `STATE.md`, `brief.md`, `prd.md` |
| Gate | Problem and users are specific; first-version scope and out of scope are written; every requirement has an ID and an acceptance check; success is measurable; budget and deadline stated or open |
| Sample | [brief](../examples/repo-pulse/docs/orbit/brief.md), [PRD](../examples/repo-pulse/docs/orbit/prd.md) |

## 2. Blueprint

| | |
|---|---|
| Start | `/orbit blueprint`, or "design the architecture" |
| Needs | Approved PRD |
| Writes | `architecture.md`, `adr/NNNN-*.md` |
| Gate | Each big decision has an ADR with two or more options; context, container and flow diagrams; every requirement maps to a part; monthly cost within budget; every failure mode has detection and recovery |
| Sample | [architecture](../examples/repo-pulse/docs/orbit/architecture.md), [ADR 0001](../examples/repo-pulse/docs/orbit/adr/0001-hosting.md) |

## 3. Assemble

| | |
|---|---|
| Start | `/orbit assemble`, or "break this into tasks" |
| Needs | Approved architecture |
| Writes | `tasks.md`, then one GitHub issue per task |
| Gate | Every requirement has a task; every task has a test, a done check, dependencies and size S or M; first milestone ends deployed end to end; CI, budget guard and operations tasks included |
| Sample | [tasks](../examples/repo-pulse/docs/orbit/tasks.md) |

## 4. Build

| | |
|---|---|
| Start | `/orbit build`, or "build the next task" |
| Needs | Approved tasks |
| Writes | Code, tests, one pull request per task; updates `tasks.md` |
| Gate | Every task done with a merged pull request; full suite and CI green on main |
| Sample | The task loop in [Examples, recipe 1](examples.md#recipe-1-a-new-product-start-to-finish) |

## 5. Test flight

| | |
|---|---|
| Start | `/orbit test-flight`, or "is it ready to release?" |
| Needs | Built product on main |
| Writes | `release.md` with a go or no-go |
| Gate | Your approval of a **go**; a no-go sends the product back to Build with new tasks |
| Sample | [release gate](../examples/repo-pulse/docs/orbit/release.md) |

## 6. Launch

| | |
|---|---|
| Start | `/orbit launch`, or "deploy it" |
| Needs | A **go** in `release.md` |
| Writes | `deploy-plan.md`, a live product |
| Gate | Spending cap and alerts before the first resource; backup tag and rollback command; deployed from CI; smoke test passes live; delivery confirmed |
| Sample | [deploy plan](../examples/repo-pulse/docs/orbit/deploy-plan.md) |

## 7. Orbit

| | |
|---|---|
| Start | `/orbit orbit`, or "set up monitoring", or "the product failed, find out why" |
| Needs | Live product |
| Writes | `runbook.md`, and `rca/YYYY-MM-DD-*.md` for each incident |
| Gate | Health check, alerts, self-healing, cost report and last-known-good tag each proven by a deliberate failure; runbook complete |
| Sample | [runbook](../examples/repo-pulse/docs/orbit/runbook.md), [incident](../examples/repo-pulse/docs/orbit/rca/2026-12-14-token-expired.md) |

## The /orbit command

| You type | It does |
|---|---|
| `/orbit` | Continues the current stage, or starts the next one if the current one is approved |
| `/orbit status` | Shows the stage, what is waiting for you, and open questions. Changes nothing |
| `/orbit <stage>` | Runs that stage, if the stage before it is approved |
