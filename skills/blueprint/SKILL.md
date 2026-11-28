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
   **Prior art:** for each capability the product needs, look for existing open-source projects
   and managed services first, and check each one live (it exists, it is active, its licence fits
   the owner's use, its price). Judge by measurement, not reputation: for anything that runs
   on the user's side, measure the cost the user pays (download size, start time, memory) and
   check its activity live (last release, open issues). Where one fits, it is an option in that decision's ADR next to
   building it; building what already exists needs a reason.
2. For each big decision, compare at least two real options on: fit to the requirements,
   cost per month at the expected load, operating effort, lock-in, and failure behaviour.
   Check current facts (prices, free-tier limits, versions) instead of relying on memory.
   Write one ADR per decision in `docs/orbit/adr/NNNN-<slug>.md` from `templates/adr.md`.
   **Start from what the owner already uses:** before hosting, data, storage or scheduling
   options, list the platforms and accounts the owner already uses (from `STATE.md`, the
   brief, or ask). Option A in each such ADR uses them; a new vendor, account or bill has to
   win against it on the facts.
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
   - **AI** (when the product calls a model): see below.
   - **Screens** (when the product has a UI): see below.
   - **What the product changes on its own at run time** (quality levels, retries, fallbacks,
     caching, feature switches by device): list each one and how a test pins it. A test
     browser or a CI runner is the slowest, oddest device there is; without a pin, every test
     sees the fallback and passes for the wrong reason.
   - **Observability for tests:** how a test reads the product's state (attributes, a status
     endpoint, a test-mode flag), so tests assert on state instead of guessing from pixels or
     timings.
   Use Mermaid for every diagram so it renders on GitHub, GitLab and most editors.
4. Apply the defaults of the product's **profile** (`STATE.md`), unless the PRD or the owner
   says otherwise. See below.
5. **Mockup,** when the product has screens: see Screens below.
6. **Cold read of the design.** Send `prd.md` and `architecture.md` to a fresh agent with the
   review skill's `cold-read.md` (the design version). It lists where someone planning the
   tasks would have to guess. Answer every important question in the documents themselves,
   not in chat.
7. Run the gate.

## Profiles

| | startup | enterprise |
|---|---|---|
| Hosting | Scales to zero, free tier where possible | Scales to zero where it can; managed databases and private networks where the data needs them, each justified in an ADR |
| Secrets | A gitignored `.env` locally, the provider's secret store in CI and production; a committed `.env.example` | A managed secret store (for example AWS Secrets Manager) everywhere, rotated; nothing secret in a `.env` on a shared machine or in CI variables in plain text |
| Isolation | One silo per product: own keys, database, quotas, alerts | The same, plus one silo per tenant's data where customers share the product |
| Compliance | Note any law that applies | A control mapping (for example DPDP, GDPR, ISO 27001, SOC 2) in `architecture.md`; data classification; audit log with opaque user IDs; no personal data or secrets in logs |
| Release | `main` deploys | A work branch, then staging, then prod after a manual approval (the **Promotion** setting) |

A secret in a plain-text file that other people or machines can read is a finding in either
profile: say so, and keep it out of the design.

## AI

When the product calls a model, `architecture.md` also covers:

- **Which model for which job,** with at least two options weighed in an ADR: quality on
  this task, cost per call and per month at the expected load, latency, and where the data
  goes.
- **Guardrails:** what the model may never decide (money, ratings, approvals, anything with
  legal weight), how its output is checked in code (numbers against the source, citations
  that resolve, banned judgements), and what the user sees when a check fails.
- **Evals:** the cases, the scorer or judge, and the bars a release must meet (for example
  figures 1.00, groundedness 0.95). The bars are requirements in `prd.md`, with IDs; if
  Ignite did not set them, add them to the PRD and mark ignite `needs review` in `STATE.md`.
- **Metering:** every call recorded with tokens and cost, a budget per tenant or per day,
  and what happens when it is reached.

## Screens

When the product has a UI, `architecture.md` also has a **screen list**: every screen, its
route, its heading, which roles may open it and which see a refusal, and its key controls.
It is the source for the browser tests in build and the owner's checklist in test flight,
so keep it in a form both can read (a table, or a `screens.yaml` the tests load).

**The mockup.** Before the gate, show the owner what each screen will look like, so they react
to a picture instead of a description:

1. First describe each screen in a few lines of text (what is on it, for whom, the main
   action). If the owner declines a drawn mockup, say what it protects, and record their
   decision as a Skipped rule row in `JOURNAL.md`.
2. Make one static HTML page with every screen from the screen list on it, in the product's
   colours and fonts, with the real labels and example data from the PRD (never lorem ipsum),
   and the refusal each role sees where a role may not open a screen. No framework and no
   server: one file the owner opens in a browser or receives as a shared page. When motion is
   the point (3D, animation, scroll-driven screens), make it a **live mockup**: the same single
   page, with the motion running on example data, since a still picture hides what the owner is
   deciding on.
3. Walk the owner through it, screen by screen. Write each change they ask for into the screen
   list and the page, and show it again.
4. Record in `architecture.md` where the mockup is and the date the owner agreed it.

A screen changed in a mockup costs minutes; the same change after it is built costs a task, its
tests and a review.

## Red flags: stop if you think

| Thought | What to do instead |
|---|---|
| "There's only one sensible option." | Write down at least one other and why it loses. That is what the ADR is for. |
| "We'll use what I know best." | Choose from the PRD's needs: budget, scale, the owner's skills and accounts. |
| "Cost can be worked out at launch." | Cost decides the design. Estimate it now, per part, at expected and ten times the load. |
| "It won't fail, it's a managed service." | Every outside call fails sometimes. Write its detection and recovery. |
| "A diagram is enough, no need for interfaces." | Builders need the contracts: inputs, outputs, errors, limits. |
| "The model will handle it, it's smart." | Write what the model may never decide, the check in code on its output, and the eval bar. |
| "We'll design the screens while building." | List every screen and role now, and agree a mockup. Browser tests and the owner's checklist come from that list. |
| "The owner can picture it from the description." | Show the mockup. People agree to descriptions and reject the screens. |
| "The design is clear, a cold read is overkill." | You wrote it; you read what you meant. A fresh agent finds the guesses in minutes. |
| "A `.env` file is fine for the secrets." | Fine on a laptop in the startup profile. Anywhere shared, or in enterprise, use the secret store. |
| "It runs from the repo, so it will find its files." | Write how the code finds its own files, config and secrets on every install path and place it runs (a plugin, a script install, a container, a function, a notebook). |
| "One run is obvious: it starts, does the work, finishes." | Write what starts and ends one run, what state survives between runs, and what happens to a run left half done (retry, resume, never twice). |
| "The summary lists the new service, so one yes covers it." | A one yes to a long summary hides a new vendor, account or bill. Ask about each one on its own, in plain words. |
| "Let me start some code to test the idea." | A spike is allowed only if the owner agrees, it is thrown away, and its result goes into an ADR (see `/orbit`, Spikes). |

## Gate

Exit list:
- [ ] Every big decision has an ADR with at least two options and a reason.
- [ ] Context, container and key-flow diagrams exist and match the text.
- [ ] Every requirement ID from the PRD maps to at least one part.
- [ ] The monthly cost is estimated and within the PRD's budget.
- [ ] Each failure mode has detection and recovery.
- [ ] Nothing in the design needs an always-on server unless an ADR justifies it.
- [ ] The profile's defaults are applied, or an ADR says why not.
- [ ] If the product calls a model: model choice, guardrails, eval bars and metering are written.
- [ ] If the product has a UI: the screen list exists and the owner agreed a mockup of every
  screen, with the date recorded, or declined it in a recorded Skipped rule row.
- [ ] The cold read's important questions are answered in `prd.md` or `architecture.md`.

- [ ] Every ADR that adds a new vendor, a paid service, a new account or a change of where the
  product runs has its own yes from the owner, recorded in `STATE.md`.

Show the owner the container diagram, the decisions in one line each, the monthly cost and
any open questions. Then list every new vendor, paid service, new account and change of
where the product runs, each as its own plain question (for example "This adds a new cloud
account with its own bill. OK?"), and ask for its own yes, separate from the yes to the
whole design. A busy owner approves summaries; these are the choices that must not hide in
one. Then ask for approval. Record an explicit yes in `STATE.md` and say that
**assemble** is next.
