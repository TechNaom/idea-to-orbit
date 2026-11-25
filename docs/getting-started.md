# Getting started

This takes about ten minutes, and ends with an approved brief for your product.

## 1. Install

Idea to Orbit is a Claude Code plugin. The easy way is to ask Claude in any session:
"Install the Claude Code plugin from https://github.com/TechNaom/idea-to-orbit". Or type:

```text
/plugin marketplace add TechNaom/idea-to-orbit
/plugin install idea-to-orbit@idea-to-orbit
```

Restart Claude Code if it asks you to. Check it is there:

```text
/plugin
```

You should see `idea-to-orbit` in the list.

From now on, every session started in a product repository begins with the product's stage
and the rules Claude follows, so you never have to remind it.

## 2. Open your product's repository

Make an empty repository for the new product (or open an existing one, see
[Existing projects](existing-projects.md)) and start Claude Code inside it:

```text
$ mkdir repo-pulse && cd repo-pulse && git init
$ claude
```

Lines starting with `$` go in your terminal. Everything else in these docs goes in the
Claude Code chat.

## 3. Start

```text
You: /orbit

AI:  No docs/orbit/STATE.md here, so this is a new product.
     Created docs/orbit/STATE.md. Starting stage 1, Ignite.

     Tell me the idea in your own words. A sentence is enough to begin.
```

Describe your idea. Claude asks questions a few at a time: the problem, who it is for, the
smallest first version, how you will know it works, budget and deadline. Answer what you
know. Anything you cannot answer yet becomes an open question; nothing is made up.

## 4. Approve the first gate

When the brief and PRD are written, Claude stops and shows a summary:

```text
AI:  Ignite is ready for your approval.

     Problem:  I miss new issues and stars on my repos for days.
     Users:    me, then other people with several small repos
     First version: one email every Monday with new stars, issues
                    and failed CI runs across my repos
     Success:  I read it 4 Mondays in a row; I fix one missed issue
               within a day of the email
     Open:     none

     Files: docs/orbit/brief.md, docs/orbit/prd.md (7 requirements)
     Approve Ignite and move to Blueprint?

You: approved
```

Only an explicit yes passes a gate. Anything else is treated as feedback, and Claude keeps
working on the stage.

## 5. Keep going

Run `/orbit` again whenever you come back. It reads `docs/orbit/STATE.md` and continues
where you left off. `/orbit status` shows where the product is without changing anything.

## Next

- See a whole product built this way: [Examples](examples.md).
- See every file that run produced: [examples/repo-pulse](../examples/repo-pulse/).
