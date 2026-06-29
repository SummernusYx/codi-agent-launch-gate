# 中杯 Mode

Goal: produce a useful read-only safety snapshot quickly.

## Steps

1. Inspect the repo structure and policy files.
2. Identify agent entrypoints, tool configs, MCP configs, browser usage, memory usage, and deployment surface.
3. Map findings to `references/framework.md`.
4. Read `references/scorecard.md` and calculate the current baseline score.
5. Return a concise table:
   - area
   - confirmed evidence
   - risk
   - severity
   - score impact
   - recommended next action

## Scorecard

Use 中杯 to answer: "Where are we right now?"

- Produce `before score` only.
- Do not produce an after score.
- Do not count proposed improvements as completed.
- Include six-layer subtotal and top 5 score gaps.
- Use `assets/scorecard-template.md` when the user asks for a formal scorecard.

## Rules

- Do not edit files.
- Do not install dependencies.
- Do not call external services unless the user asks for live verification.
- Prefer `rg`, `rg --files`, and targeted file reads.
- If evidence is missing, mark it as unknown and score conservatively.

## Output Shape

Start with:

1. Agent Launch Score, release gate label, and blocker override if any.
2. Highest-risk findings.
3. Six-layer score summary.
4. Missing evidence.
5. Short "大杯 upgrade" section describing which configs would be generated if the user continues.
6. One or more one-sentence follow-up prompts from `references/apply-actions.md`.
