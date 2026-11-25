---
name: blueprint
description: "Idea to Orbit stage 2. Design the architecture for an approved PRD: weigh options for each big decision, record them as ADRs, define components, data model, interfaces, security, cost and failure modes, and draw Mermaid diagrams. Use after ignite is approved, or when the owner asks to design or review a product's architecture."
---

# Blueprint: the architecture

Goal: a design the owner understands and approves, where every big decision shows the
options considered and why one was chosen.

## Inputs

The approved `docs/orbit/prd.md`. Check `STATE.md`: ignite must be `approved`.

## Steps

1. Read the PRD. List the decisions the design needs, for example: hosting, data store,
   interfaces, model providers, authentication, background jobs, how it is triggered.
2. For each big decision, compare at least two real options on: fit to the requirements,
   cost per month at the expected load, operating effort, lock-in, and failure behaviour.
   Check current facts (prices, free-tier limits, versions) instead of relying on memory.
   Write one ADR per decision in `docs/orbit/adr/NNNN-<slug>.md` from `templates/adr.md`.
3. Write `docs/orbit/architecture.md` from `templates/architecture.md`:
   - **Context diagram:** the product, its users and the outside systems.
   - **Container diagram:** the deployable parts and how they talk.
   - **Key flows:** a sequence diagram for each important path, including one failure path.
   - **Data model:** entities, fields, relationships, who owns each.
   - **Interfaces:** every API, event, queue and file format, with its contract.
   - **Security:** secrets, auth, data protection, least privilege.
   - **Cost:** the expected monthly cost per part, and the spending cap.
   - **Failure modes:** what breaks, how it is detected, how it recovers.
   - **Traceability:** which parts satisfy which requirement IDs.
   Use Mermaid for every diagram so it renders on GitHub.
4. Apply the defaults unless the PRD or the owner says otherwise: scale to zero, one silo
   per product (its own keys, database, quotas and alerts), budget guard before deploy,
   secrets in `.env` with a committed `.env.example`.
5. Run the gate.

## Red flags: stop if you think

| Thought | What to do instead |
|---|---|
| "There's only one sensible option." | Write down at least one other and why it loses. That is what the ADR is for. |
| "We'll use what I know best." | Choose from the PRD's needs: budget, scale, the owner's skills and accounts. |
| "Cost can be worked out at launch." | Cost decides the design. Estimate it now, per part, at expected and ten times the load. |
| "It won't fail, it's a managed service." | Every outside call fails sometimes. Write its detection and recovery. |
| "A diagram is enough, no need for interfaces." | Builders need the contracts: inputs, outputs, errors, limits. |
| "Let me start some code to test the idea." | A spike is allowed only if the owner agrees, it is thrown away, and its result goes into an ADR. |

## Gate

Exit list:
- [ ] Every big decision has an ADR with at least two options and a reason.
- [ ] Context, container and key-flow diagrams exist and match the text.
- [ ] Every requirement ID from the PRD maps to at least one part.
- [ ] The monthly cost is estimated and within the PRD's budget.
- [ ] Each failure mode has detection and recovery.
- [ ] Nothing in the design needs an always-on server unless an ADR justifies it.

Show the owner the container diagram, the decisions in one line each, the monthly cost and
any open questions, and ask for approval. Record an explicit yes in `STATE.md` and say that
**assemble** is next.
