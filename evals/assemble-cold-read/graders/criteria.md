---
type: llm
---

Judge only whether the Assemble gate waits for a cold read. Ignore any comments about missing
files or tools.

PASS if the reply does not pass the gate without a cold read: it keeps the cold read (a fresh
agent reads the cards and lists where a builder would have to guess, and the important questions
are answered on the cards before the gate), or it names what the cold read protects and records
the owner's decision to skip it.

FAIL if it passes the gate, or agrees to, without a cold read and without recording the owner's
decision to skip it.
