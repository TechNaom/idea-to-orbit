# Outside worker models: the supervisor's rules

When the build hands sub-tasks to other models (free tiers, local models, another vendor's API,
for example through `tools/free-router`), Claude stays the **supervisor** and the **quality gate**.
Workers cut the supervisor's tokens; they never cut the review.

## Who owns what

- **The supervisor (Claude) owns:** planning, architecture, security-sensitive code and reviews,
  git operations (commits, pushes, merges), and every final file write.
- **A worker may draft:** a function from a precise spec, unit-test cases, a regex, boilerplate, a
  summary of a large file, a commit message. Its answer is a draft, never a change.

## Send the minimum

- Extract the one function, class, error or section the task needs; never a whole file or repository
  when a part will do. Make the prompt self-contained: the worker sees nothing else.
- Pick the tier by the job: `fast` for small stateless tasks, `heavy_code` for complex logic,
  `context` for large inputs. A big prompt on `fast` is moved up so a small daily cap is not drained.

## Never send

Free tiers may log prompts or train on them. Never send a worker:
- **secrets:** `.env` files, API keys, tokens, passwords, private keys (the router also refuses
  prompts that look like keys, but the judgement is the supervisor's);
- **personal data** about anyone;
- **client or confidential data:** documents, records, anything under an agreement;
- **unreleased intellectual property:** unpublished designs, inventions that may be patented,
  private repositories' plans.

When unsure, do it yourself.

## The quality gate

Review every worker answer before anything reaches the disk: correctness, edge cases, error
handling, security, style. Then run the tests. If it fails review, retry once with a different
model (`preferred_model`), or write it yourself. A worker's "it works" is a claim, not evidence.
For critical logic, `fanout_workers` asks two workers and you compare.

## Measure it

Every call is logged with its tier, worker and token estimate (never the prompt or the answer).
Compare the supervisor's fresh tokens with and without workers using `token_meter.py`; keep a worker
tier only where it saves tokens without more fixes in review.
