# Idea to Orbit

**From idea to orbit, and it stays up.**

Idea to Orbit is a Claude Code plugin that takes a product from a rough idea to a running
product, and then keeps it running. It plans, designs the architecture, breaks the work into
tasks, builds test-first, checks the release, deploys within a budget and watches the product
in production. The owner approves every stage before the next one starts.

A TechNaom AI R&D Labs project.

## The seven stages

| Stage | What happens | What you get |
|---|---|---|
| 1. **Ignite** | Questions until the idea is clear: problem, users, scope, success | `brief.md`, `prd.md` |
| 2. **Blueprint** | Architecture with options weighed, data model, interfaces, diagrams | `architecture.md`, `adr/` |
| 3. **Assemble** | The plan becomes small, ordered, testable tasks | `tasks.md`, GitHub issues |
| 4. **Build** | Each task built test-first, reviewed, committed in small steps | Code and tests |
| 5. **Test flight** | The release gate: tests, risks, security, cost, rollback | `release.md` |
| 6. **Launch** | A budget-guarded deploy that sleeps when idle, with a backup first | `deploy-plan.md`, a live product |
| 7. **Orbit** | Watchdog, alerts, self-healing within limits, root cause on failure | `runbook.md`, `rca/` |

Every stage ends at a **gate**: Claude shows what it made and waits for you to say go.
Nothing moves forward on a guess.

## Install

In Claude Code:

```
/plugin marketplace add TechNaom/idea-to-orbit
/plugin install idea-to-orbit@idea-to-orbit
```

## Use

Open your product's repository in Claude Code and run:

```
/orbit
```

It reads `docs/orbit/STATE.md`, tells you which stage the product is in and what comes next.
On a new product it starts **Ignite**. You can also name a stage directly, for example
"run the blueprint stage" or "move to test flight".

Everything the stages write lives in your product repository, under `docs/orbit/`:

```
docs/orbit/
  STATE.md            current stage, gate approvals, open questions
  brief.md            one page: the problem, who has it, why now
  prd.md              requirements and success measures
  architecture.md     the design, with diagrams
  adr/                one file per architecture decision
  tasks.md            the ordered task list
  release.md          the release gate checklist and its result
  deploy-plan.md      where and how it runs, what it costs
  runbook.md          how it is watched, healed and rolled back
  rca/                one file per incident
```

## Principles

- **The owner decides.** Each gate needs an explicit yes. Silence is not approval.
- **Docs before code.** The brief, PRD and architecture are approved before any code.
- **Test first.** A task is done when its tests pass, not when the code is written.
- **Small steps.** Small commits, pushed often, each one working.
- **Budget first.** A spending cap and alerts exist before anything is deployed.
- **Scale to zero.** Nothing runs when nobody is using it.
- **One silo per product.** Its own keys, database, quotas and alerts, so one product can
  never break another.
- **Always a way back.** A backup tag before every release, and a tested rollback.
- **Success means delivered.** A green run that delivered nothing counts as a failure.

## Status

Version 0.1: the seven stages, their templates and the `/orbit` command. See
[docs/DESIGN.md](docs/DESIGN.md) for how it works and what comes next.

## License

MIT. See [LICENSE](LICENSE).
