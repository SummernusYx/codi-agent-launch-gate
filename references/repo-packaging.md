# Repository Packaging Notes

Use this only when preparing Agent Launch Gate for GitHub or another public repository.

## Do Not Confuse Two Layers

- Skill package: the files Codex loads and follows.
- Open-source repository: README, license, examples, contribution notes, release notes, and demo assets.

Keep the skill package concise. Put public-facing explanations in the repo layer when possible.

## Minimum Public Repo

- `README.md`: what it does, when to use 中杯/大杯/超大杯, install/use examples, local-first privacy note.
- `LICENSE`: choose before publishing.
- `examples/`: at least one 中杯 report and one 大杯 before/target scorecard.
- `.gitignore`: allowlist the files intended for release.
- `SECURITY.md`: how to report security issues and what the tool does not guarantee.

## README Spine

1. One-sentence promise: "A local-first release gate for AI agent apps."
2. Why it exists: agent apps now combine code, browser, MCP, memory, live docs, and permissions.
3. Three modes:
   - 中杯: read-only baseline score
   - 大杯: hardening plan and target score
   - 超大杯: release sign-off
4. Scorecard example.
5. Local-first safety guarantees.
6. Comparison with checklists and scanners.
7. Installation and invocation.

## Public Claims Boundary

Avoid claiming complete protection. Say it helps create repeatable safety review, evidence, and release decisions.
