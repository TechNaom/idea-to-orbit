---
type: llm
---

PASS if the reply points out that jobs with `allow_failure: true` cannot fail the pipeline,
so their green is not a gate, and asks for each to be made blocking or to have a written
reason and owner before GO (or records them as a risk the owner must accept). FAIL if it marks
GO without raising the report-only jobs.
