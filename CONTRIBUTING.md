# Contributing

Issues and pull requests are welcome.

- **Found a problem?** Open an issue with what you ran, what you expected and what happened.
  If a stage produced a wrong document, attach the relevant part of `docs/orbit/`.
- **Changing a stage?** Edit `skills/<stage>/SKILL.md` and its templates together, and
  update `docs/stages.md` and the sample in `examples/repo-pulse/` if the output changes.
- **Changing a rule or a red flag?** Add or change a case in `evals/` that would have caught
  the old behaviour, watch it fail, then change the skill. See [Testing](docs/testing.md).
- **Before a pull request:** run `python tests/check.py`. CI runs it too.
- **Writing docs?** Plain words, short sentences, and a real example wherever one helps.
- Keep each pull request to one change, and describe why it is needed.
- **Releases:** each version gets a CHANGELOG entry, the same version in `plugin.json`,
  `marketplace.json`, the README and the design doc (the offline check compares them), and a
  git tag `v<version>` on its commit. Eval results for a release go in `docs/eval-results.md`.
- **Security problems:** see [SECURITY.md](SECURITY.md); do not open a public issue.
