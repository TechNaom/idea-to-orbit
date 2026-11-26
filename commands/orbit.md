---
description: Show where this product is in Idea to Orbit and continue with the next stage.
argument-hint: "[stage name, or 'status']"
---

# /orbit

You are running Idea to Orbit for the product in the current repository.

1. Read `docs/orbit/STATE.md`.
   - If it does not exist and the repository is empty or has no product code, this is a new
     product. Create `docs/orbit/` and `STATE.md` from the ignite skill's
     `templates/state.md`, then start the **ignite** stage.
   - If it does not exist but the repository already has code, this is an existing product.
     Do not start from a blank page: follow the ignite skill's **Existing product** steps,
     which catch the documents up from the code.
2. If the argument is `status`, or empty and the current stage is waiting for approval,
   show a short status and stop:
   - the product name and the current stage
   - its status, and what is waiting for the owner
   - the work in flight (each lane and its step)
   - open questions
   - the Settings, in one line (code host, work branch, builders, profile)
   - the next stage
3. If the argument names a stage (ignite, blueprint, assemble, build, test-flight, launch,
   orbit), run that stage's skill (the orbit stage's skill is **keep-running**, so it does not
   clash with this command). Refuse to start a stage whose previous stage is not
   `approved` in `STATE.md`, and say which gate is open.
4. If the owner asks for a feature, a fix or a hotfix on a product that is past Build, use a
   **lane** (below) instead of moving the whole product back a stage. A request to add,
   improve, "ramp up", "catch up with" or "make it like" another product or design is a
   **feature** lane: start with its ignite (the ignite skill, "A feature lane"), never with a
   list of build steps.
5. Otherwise continue the current stage, or start the next one if the current one is
   approved.

Stage order: ignite → blueprint → assemble → build → test-flight → launch → orbit.

## Lanes

A product is often live while new work goes on. A lane runs one piece of work through the
same rules with only the steps it needs, beside the product's stage. Record each one under
**In flight** in `STATE.md`, with its lane and current step, and in `JOURNAL.md` when done.

| Lane | For | Steps | Gate |
|---|---|---|---|
| Feature | New behaviour | A short ignite for the feature only (problem, requirement IDs, acceptance checks, out of scope); a blueprint note or ADR if the design changes; cards and a cold read; the build loop with both checks; the test-flight lines it touches; then the launch steps it touches | The owner's yes on the feature's requirements, then before it goes live |
| Fix | A bug, not urgent | The debug skill to a known cause; a failing test for the cause; the build loop with both checks; then release it: the launch steps it touches (Promotion, backup tag, smoke test) | The owner's yes before it reaches the live product |
| Hotfix | Users affected now | Stabilise first (roll back to the last known good tag); then the fix lane; then an RCA | The owner's yes before touching the live product, and the RCA |

Several lanes can be in flight at once when they change different files, as with parallel
tasks. The rules do not change in a lane: test first, cause before fix, evidence before
claims, and the owner's yes.

Inside every stage and lane, use the helper skills: **review** before any change is merged,
**debug** when something fails, **verify** before any status you report, and **learn** at the
end of a milestone or after an incident.

Never mark a gate approved without an explicit yes from the owner in this conversation.

Arguments: $ARGUMENTS
