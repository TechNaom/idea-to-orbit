# Sample product: Repo Pulse

A complete, illustrative run of Idea to Orbit, with every document filled in as the seven
stages produce it. Repo Pulse is a sample product made for this example; its dates, numbers
and outputs show what a real run looks like, and are not records of a live service.

**The product:** one email every Monday at 08:00 IST listing new issues, failed CI runs and
new stars across all the GitHub repositories of one account.

The session that produced these files is in [docs/examples.md, recipe 1](../../docs/examples.md#recipe-1-a-new-product-start-to-finish).

## The files, in the order the stages write them

| Stage | File |
|---|---|
| All | [STATE.md](docs/orbit/STATE.md) |
| 1. Ignite | [brief.md](docs/orbit/brief.md), [prd.md](docs/orbit/prd.md) |
| 2. Blueprint | [architecture.md](docs/orbit/architecture.md), [ADR 0001 hosting](docs/orbit/adr/0001-hosting.md), [ADR 0002 email](docs/orbit/adr/0002-email-delivery.md) |
| 3. Assemble | [tasks.md](docs/orbit/tasks.md) |
| 5. Test flight | [release.md](docs/orbit/release.md) |
| 6. Launch | [deploy-plan.md](docs/orbit/deploy-plan.md) |
| 7. Orbit | [runbook.md](docs/orbit/runbook.md), [incident 2026-12-14](docs/orbit/rca/2026-12-14-token-expired.md) |

Stage 4, Build, produces code and pull requests rather than a document; its progress shows
in `tasks.md` and `STATE.md`.
