# Self-Audit Procedure

Use this when Agent Launch Gate audits its own skill folder or another skill package.

## Scope

Check only the skill package unless the user explicitly asks to inspect the parent repository.

## Read Order

1. `SKILL.md`
2. selected mode file under `references/modes/`
3. `references/framework.md`
4. `references/scorecard.md`
5. `agents/openai.yaml`
6. templates under `assets/`
7. examples under `examples/`, if present

## Checks

- Frontmatter has only valid, useful trigger metadata.
- Trigger phrases are specific enough to avoid accidental use.
- First response asks for mode unless the user already chose one.
- Mode files do not contradict each other.
- Scorecard rules match the mode behavior.
- Templates do not ask agents to leak secrets, upload files, publish, or bypass confirmation.
- Outputs require evidence for completion claims.
- Missing README, LICENSE, `.gitignore`, CI, or examples are treated as repo-packaging gaps, not skill-validity blockers.

## Scoring Notes

For a skill package, score runtime dimensions based on the instructions it gives future agents, not on executable code.

Examples:

- "Agent boundary" means whether the skill explains its scope and what it should inspect.
- "Loop stop conditions" means whether the workflow has mode boundaries, confirmation gates, and evidence requirements.
- "State" means whether memory, logs, browser state, and persistent context are addressed.
- "Hooks/tests/CI" can be low for a local draft, but should be called out before open source release.

## Output

Return:

- Agent Launch Score and release label.
- Top findings.
- Six-layer subtotal.
- Top 5 score gaps.
- 大杯 upgrade plan.

Use `examples/zhongbei-self-audit.md` as a style reference, not as fixed truth.
