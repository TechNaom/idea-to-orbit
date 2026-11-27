# Idea to Orbit

[![check](https://github.com/TechNaom/idea-to-orbit/actions/workflows/check.yml/badge.svg)](https://github.com/TechNaom/idea-to-orbit/actions/workflows/check.yml)

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
| 3. **Assemble** | The plan becomes small, ordered tasks, each with exact files, steps and commands | `tasks.md`, GitHub issues |
| 4. **Build** | Each task built test-first by a fresh agent, then checked by two more | Code, tests, pull requests |
| 5. **Test flight** | The release gate: tests, risks, security, cost, rollback | `release.md` |
| 6. **Launch** | A budget-guarded deploy that sleeps when idle, with a backup first | `deploy-plan.md`, a live product |
| 7. **Orbit** | Watchdog, alerts, self-healing within limits, root cause on failure | `runbook.md`, `rca/` |

Every stage ends at a **gate**: Claude shows what it made and waits for you to say go.
Nothing moves forward on a guess.

## The rules it holds to

Four rules, with no exceptions written in. If you choose to skip one, Claude says what it
protects, follows your decision and records it.

| Rule | What it means |
|---|---|
| **No production code without a failing test first** | The test is written, run and seen to fail before the code exists. A one-line fix too. |
| **No fix without a known cause** | Bugs are reproduced and traced to their cause before anything changes. After two failed fixes, stop and question the design. |
| **No claim without fresh evidence** | "Done", "fixed" and "passing" come with the command and its output, run after the last change. |
| **No gate without your yes** | "Looks good, but..." is feedback, not approval. |

How they hold:

- **At the start of every session** a hook tells Claude the product's stage, its open
  questions and these rules, before your first message.
- **Every skill lists its red flags**: the thoughts that come just before a shortcut, such as
  "it's only a typo" or "the agent said the tests pass", with what to do instead.
- **The writer never approves its own work.** Each task is built by a fresh agent from a task
  card, then checked by two more: one against the card, one for code quality. Each
  milestone gets a review as a whole.

## Helper skills

| Skill | Use it when |
|---|---|
| **review** | A change needs checking by someone who did not write it, or review feedback arrives |
| **debug** | Something breaks, a test fails unexpectedly, or a fix did not work |
| **verify** | Before saying anything is done, fixed, passing or deployed |
| **learn** | At the end of a milestone or after an incident: turn repeated trouble into checks |

The stages call them for you. You can also ask for one directly: "debug this failing test".

## Install

The easy way: in any Claude Code session, ask

```
Install the Claude Code plugin from https://github.com/TechNaom/idea-to-orbit
```

Or type the commands yourself:

```
/plugin marketplace add TechNaom/idea-to-orbit
/plugin install idea-to-orbit@idea-to-orbit
```

Restart Claude Code afterwards so the skills and the session-start hook load.

### No `/plugin` command? Use the install script

Some Claude Code surfaces (for example the VS Code extension) do not offer `/plugin`. Clone the
repository and run the installer; it works on every surface:

```bash
git clone https://github.com/TechNaom/idea-to-orbit
./idea-to-orbit/install.sh             # macOS, Linux, Git Bash
.\idea-to-orbit\install.ps1            # Windows PowerShell
```

It copies the skills and `/orbit` into your Claude config folder (`~/.claude`, or
`$CLAUDE_CONFIG_DIR`) and adds the session-start hook to its `settings.json`, keeping your own
settings. Run it again to update. `--uninstall` removes exactly what it added. It never
overwrites a skill of yours that happens to share a name; it stops and tells you instead.

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
  STATE.md            current stage, settings, gate approvals, work in flight, open questions
  JOURNAL.md          every change, fix in review and roadblock, with its cause and lesson
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

## Docs and examples

- [Getting started](docs/getting-started.md): install and run your first stage in ten minutes.
- [Examples](docs/examples.md): real sessions, start to finish, showing what you type and
  what you get back.
- [Sample product: Repo Pulse](examples/repo-pulse/): every document a full run produces,
  from the brief to an incident report.
- [Concepts](docs/concepts.md), [Stage reference](docs/stages.md),
  [Existing projects](docs/existing-projects.md), [FAQ](docs/faq.md),
  [Troubleshooting](docs/troubleshooting.md), [Testing the plugin](docs/testing.md).

## Principles

- **The owner decides.** Each gate needs an explicit yes. Silence is not approval.
- **Docs before code.** The brief, PRD and architecture are approved before any code.
- **Test first.** A task is done when its tests pass, not when the code is written.
- **Fresh eyes.** Nothing reaches main checked only by the one who wrote it.
- **Evidence, not claims.** Every status comes with the output that proves it.
- **Small steps.** Small commits, pushed often, each one working.
- **Budget first.** A spending cap and alerts exist before anything is deployed.
- **Learn from trouble.** Every roadblock is written down with its cause; patterns become checks.
- **Scale to zero.** Nothing runs when nobody is using it.
- **One silo per product.** Its own keys, database, quotas and alerts, so one product can
  never break another.
- **Always a way back.** A backup tag before every release, and a tested rollback.
- **Success means delivered.** A green run that delivered nothing counts as a failure.

## Status

Version 0.8: the seven stages and four helper skills, the session-start hook, install scripts
for surfaces without `/plugin`, catch-up steps for products that already have code, a build
stage with fresh-agent checks on every task, a bounded fix loop and support for outside
builders (Cursor, Kiro), a cold read of the design and of the cards, a mockup step for screens,
GitHub or GitLab, startup and enterprise profiles, checks for AI features, lanes for work on a
live product, a journal and a learn skill that also reads past sessions, red flags in every
skill, 29 pressure scenarios and an offline check that runs in CI. The docs and a complete sample product. See [CHANGELOG.md](CHANGELOG.md) for changes and [docs/DESIGN.md](docs/DESIGN.md)
for how it works and what comes next.

## License

MIT. See [LICENSE](LICENSE).
