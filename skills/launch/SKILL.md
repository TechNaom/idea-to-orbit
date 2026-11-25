---
name: launch
description: "Idea to Orbit stage 6. Deploy a product that passed its release gate: set the spending cap and alerts first, take a backup tag, deploy to scale-to-zero hosting in its own silo, smoke-test the live product and keep the rollback ready. Use after test-flight is approved, or when the owner asks to deploy or release a product."
---

# Launch: a budget-safe deploy

Goal: the product is live, costs no more than agreed, sleeps when idle, and can be rolled
back in one step.

## Inputs

The release commit, `docs/orbit/release.md` with a **go**, and `architecture.md`.
Test flight must be `approved` in `STATE.md`.

## Steps, in this order

Write `docs/orbit/deploy-plan.md` from `templates/deploy-plan.md` first, and show it to the
owner before running anything that creates resources or costs money.

1. **Budget guard first.** Before any resource exists: a monthly spending cap, alerts at 25,
   50, 80 and 100 percent plus a forecast alert, sent to the owner. Where the provider
   allows it, an action that stops the product's compute at 100 percent. Check the account's
   plan, credits and their expiry.
2. **Own silo.** The product gets its own keys, database or database project, quotas and
   alert channel. Nothing is shared with another product that could take it down.
3. **Secrets** go into the provider's secret store or the CI secrets, never into the
   repository. `.env.example` lists every one.
4. **Backup tag.** Tag the current production commit (`stable-<YYYY-MM-DD>`) before the
   deploy, so there is a known way back.
5. **Deploy** from CI, not from a laptop, so any machine can repeat it. Hosting scales to
   zero: serverless functions, scheduled triggers and managed services with free tiers by
   default. Set concurrency limits and timeouts on everything.
6. **Smoke test** the live product: the main flow end to end, plus a health check. If it
   fails, roll back to the backup tag at once and tell the owner.
7. **Confirm delivery, not just success.** Check the product actually did its job (the
   message was sent, the post was published, the record was written), not only that the
   run was green.
8. Record the live URL, the version, the backup tag and the cost guard in `deploy-plan.md`.

Ask the owner before any step that spends money, needs a payment method, or changes a
product that is already live.

## Gate

Exit list:
- [ ] Spending cap and alerts existed before the first resource.
- [ ] Backup tag taken and rollback command written down.
- [ ] Deployed from CI; the smoke test passes on the live product.
- [ ] Delivery confirmed, not just a green run.
- [ ] Nothing runs when idle, or an ADR says why it must.

Show the owner the live URL, the smoke test result, the cost guard and the rollback command,
and ask for approval. Record an explicit yes in `STATE.md` and say that **orbit** is next.
