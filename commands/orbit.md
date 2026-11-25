---
description: Show where this product is in Idea to Orbit and continue with the next stage.
argument-hint: "[stage name, or 'status']"
---

# /orbit

You are running Idea to Orbit for the product in the current repository.

1. Read `docs/orbit/STATE.md`.
   - If it does not exist, this is a new product. Create `docs/orbit/` and `STATE.md` from
     the ignite skill's `templates/state.md`, then start the **ignite** stage.
2. If the argument is `status`, or empty and the current stage is waiting for approval,
   show a short status and stop:
   - the product name and the current stage
   - its status, and what is waiting for the owner
   - open questions
   - the next stage
3. If the argument names a stage (ignite, blueprint, assemble, build, test-flight, launch,
   orbit), run that stage's skill. Refuse to start a stage whose previous stage is not
   `approved` in `STATE.md`, and say which gate is open.
4. Otherwise continue the current stage, or start the next one if the current one is
   approved.

Stage order: ignite → blueprint → assemble → build → test-flight → launch → orbit.

Never mark a gate approved without an explicit yes from the owner in this conversation.

Arguments: $ARGUMENTS
