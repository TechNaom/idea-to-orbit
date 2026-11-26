# Cold read brief

Send this to a fresh agent with every `<...>` filled in, before the Assemble gate (all the
cards of the next milestone) or before a single card goes to a builder. It finds the places
where a builder would have to guess, while fixing them is still one sentence on a card.

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
