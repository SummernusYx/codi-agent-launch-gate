# 超大杯 Mode

Goal: produce a release-grade safety gate with evidence and owner decisions.

## Steps

1. Run or reuse 大杯 hardening.
2. Calculate `before score`, `after score`, and release gate label.
3. Build an evidence table for every high and medium risk.
4. Classify each item:
   - blocker
   - must-fix before release
   - accepted residual risk
   - follow-up
5. Verify available tests, lint, typecheck, build, secret checks, and policy checks.
6. Produce an incident response and rollback note for unsafe agent behavior.

## Scorecard

Use 超大杯 to answer: "Can this be released?"

- Include full before/after scorecard.
- Include release label: Blocked, Internal test only, Ready with accepted risk, or Ready to launch.
- Critical blockers override the numeric score.
- Require owner decisions for accepted residual risks.
- Use `assets/scorecard-template.md` and `assets/audit-report-template.md` together.

## Required Sections

- Executive decision: ship, ship with accepted risk, or do not ship.
- Agent Launch Score before and after.
- Scope and assumptions.
- Evidence-backed findings.
- Config and permission review.
- Prompt-injection review.
- Secret and data exposure review.
- Tool/MCP least-privilege review.
- Observability and rollback plan.
- Residual risk owner decisions.
- One-sentence prompts for fixing blockers, accepting residual risk, or producing a release note.

## Rules

- Do not claim release readiness without evidence.
- If a critical control cannot be verified, mark it as a blocker or explicit owner acceptance.
- Keep the final report actionable enough for a new maintainer to reproduce.
- Keep release, publish, upload, and external-send actions behind explicit user confirmation.
