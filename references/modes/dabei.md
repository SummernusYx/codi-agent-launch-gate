# 大杯 Mode

Goal: turn the read-only audit into concrete hardening proposals.

## Steps

1. Run the 中杯 audit first or reuse a recent 中杯 report.
2. Calculate the `before score` from current evidence.
3. Draft changes for the smallest set of files that materially reduce risk.
4. Estimate a `target score` for the proposed changes, without treating them as completed.
5. Prefer templates in `assets/` before inventing new policy text.
6. Show planned file edits before writing when the target is global config, auth, deployment, registry, database, browser profile, or system-level settings.
7. If the user approves and changes are applied, run the smallest meaningful validation available.
8. Calculate an `after score` only for changes that were actually applied and verified.

## Scorecard

Use 大杯 to answer: "What would improve if we harden this?"

- Always include `before score`.
- Include `target score` for proposed changes.
- Include `after score` only after implemented and verified changes.
- Keep score changes tied to evidence. A template proposal can raise target score, not after score.
- Use `assets/scorecard-template.md` for before/target/after comparison.

## Typical Artifacts

- `AGENTS.md` safety block.
- MCP inventory and least-privilege notes.
- Permission checklist.
- Pre-commit or CI gate suggestions.
- Release checklist for prompt injection, secrets, browser state, and external actions.
- One-sentence apply prompts for each proposed change group.

## Rules

- Ask before modifying global files.
- Ask before installing packages.
- Ask before publishing, uploading, sending, or sharing anything.
- Keep diffs scoped. Do not refactor unrelated project structure.
- Preserve user edits and dirty worktrees.
- Do not apply proposed changes just because they appear in the report. Wait for an explicit follow-up prompt or confirmation.
