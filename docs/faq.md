# FAQ

**Do I have to use all seven stages?**
No. You can run any stage on its own, as long as the stage before it is approved, or you
confirm reconstructed docs for it (see [Existing projects](existing-projects.md)). For a
small change, a short Ignite and a short Blueprint take minutes.

**Can I skip a gate?**
A gate passes only on your explicit yes, so you are always in control of the pace. If you
want to move fast, read the summary and say "approved". What the gate does not do is assume
your yes.

**What counts as approval?**
Clear words like "approved", "go", "yes, proceed". A question, a comment, "looks good but..."
or silence is treated as feedback, and the stage continues.

**Where are the documents kept?**
In your product's repository, under `docs/orbit/`. Commit them with the code.

**Can I edit the documents myself?**
Yes. They are plain Markdown. If you change an approved document, tell Claude, or run
`/orbit`: later stages that depend on it are marked `needs review`.

**Does it work with any language or cloud?**
Yes. The stages are about the work, not the stack. The defaults (serverless, scale to zero,
free tiers) are a starting point that Blueprint weighs against other options for each
product.

**Does it spend money on my behalf?**
Not without asking. Launch sets a spending cap before creating anything, and asks before
any step that costs money or needs a payment method.

**Does it deploy from my laptop?**
No. Deploys run from CI, so any machine can repeat them and nothing depends on your laptop.

**How is it different from just asking Claude to build something?**
The same Claude does the work. Idea to Orbit adds the order, the written decisions, the
tests first, the release gate, the budget guard and the operations, so the result is a
product that keeps running, not just code that ran once.

**Can more than one Claude session work on the same product?**
Yes. Each task is its own branch, and every session pulls and rebases before it edits.
`STATE.md` is the shared record of where things are.
