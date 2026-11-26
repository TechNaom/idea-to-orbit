# Cold read brief

Send this to a fresh agent with every `<...>` filled in: before the Blueprint gate (the PRD
and the architecture), before the Assemble gate (all the cards of the next milestone), or
before a single card goes to a builder. It finds the places where the next person would have
to guess, while fixing them is still one sentence in a document.

For the design, use the short version at the end of this file.

---

You are a capable <language or stack> developer. You have been handed the task cards below
and asked to build them. You have never seen this product and you cannot ask the person who
wrote them.

## The cards

<the full cards, as the builder will get them>

## Context the builder will also get

<the requirement text and the part of architecture.md each card names; nothing more>

## What to report

Only the questions you would need answered before you could build these well: places where
you would have to guess, and a wrong guess would matter. For each one:

1. The card and the line.
2. The question.
3. Why the answer changes what you would build.

Rank them by importance. Skip anything a card leaves to the builder on purpose, anything you
could reasonably decide yourself, and wording nitpicks.

Then list, for each card:

- **Files:** any file you would need to change that the card does not name. Search the
  whole repository for code and tests that read or import each named file, not only the
  folders you expect.
- **Commands:** any command on the card that you could not run as written on <OS and shell>.

## Report

```
Questions:
1. <card> <line>: <question>. Changes: <what>
Files not named: <card: path, why>, or "none"
Commands that would not run: <card: command, why>, or "none"
```

---

## The design version

Send this before the Blueprint gate, with every `<...>` filled in.

---

You are a capable <language or stack> developer. You have been handed the requirements and the
architecture below and asked to break the work into small tasks, each with exact files,
interfaces and a test. You have never seen this product and you cannot ask the person who
wrote them.

## The documents

<prd.md and architecture.md, in full>

## What to report

Only the questions you would need answered before you could plan the tasks well: places where
you would have to guess, and a wrong guess would matter. For each: the document and section,
the question, and why the answer changes the plan. Rank them by importance. Skip what you could
reasonably decide yourself, and wording nitpicks.

Then list any part, interface, data field or failure path a task would need that the design
does not name.

```
Questions:
1. <document> <section>: <question>. Changes: <what>
Not named in the design: <part, interface, field or failure path>, or "none"
```
