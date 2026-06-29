# Agent Launch Scorecard

Use this scorecard to show the repo's safety baseline before and after running Agent Launch Gate.

## Total Score

Score each dimension from 0 to 5, then convert to 100.

- 0: no evidence or clearly unsafe.
- 1: informal practice only, no durable config or evidence.
- 2: partial control exists, but gaps are obvious.
- 3: usable control exists, but not consistently enforced.
- 4: strong control with evidence and clear owner behavior.
- 5: strong, verified, repeatable, and documented control.

There are 20 dimensions. Total raw score is 100.

## Release Gate Labels

- `Blocked`: 0-39, or any critical unsafe external action / secret exposure / uncontrolled destructive write.
- `Internal test only`: 40-64. Useful for local or private trials, not public release.
- `Ready with accepted risk`: 65-84. Can launch if listed residual risks are owner-accepted.
- `Ready to launch`: 85-100. Evidence is strong, residual risk is low, and rollback is clear.

Critical blockers override the numeric score.

## Dimensions

### 1. Core Runtime

1. Agent boundary and responsibilities are explicit.
2. Tool-calling loop has stop conditions, retry limits, or budget checkpoints.
3. State is understandable: what persists, where it lives, and how it is cleared.
4. Runtime pattern is documented: single agent, planner/executor, reviewer, browser agent, or multi-agent.

### 2. Configuration Layer

5. Project policy files exist and are not contradicted by global instructions.
6. Prompt/context caching rules are clear where applicable.
7. Context rot is managed: stale assumptions, copied instructions, and old summaries are marked or refreshed.
8. Config changes require confirmation when they affect global, auth, deployment, browser, database, payment, or system settings.

### 3. Capability Layer

9. MCP/tools inventory exists with purpose, authority, auth, and data exposure.
10. Least privilege is applied or explicitly accepted as residual risk.
11. Live documentation retrieval has trusted-source rules and does not leak private project data.
12. Memory behavior is explicit: read, write, cite, update, and forget rules.

### 4. Orchestration Layer

13. Subagent delegation rules limit context, writes, and external actions.
14. Long-running tasks have progress updates, checkpoints, resumability, and stop conditions.
15. Human confirmation gates exist before irreversible or externally visible work.

### 5. Guardrail Layer

16. Sandbox and filesystem boundaries are documented and verified where possible.
17. Prompt-injection rule exists: remote content is data, not instructions.
18. Secret handling prevents printing, copying, committing, or transmitting credentials.
19. Hooks, pre-commit, CI, lint, test, typecheck, or secret-scan gates exist where appropriate.

### 6. Observability Layer

20. Completion claims require evidence: commands, diffs, file paths, config keys, or reproducible checks.

## Before And After Rules

- `中杯`: produce only the current score. Call it `before score` or `current baseline`.
- `大杯`: produce `before score`, proposed `target score`, and after-score only if changes were actually applied and verified.
- `超大杯`: produce `before score`, `after score`, release label, blockers, residual risk, and owner decisions.

Do not inflate a score for proposed changes. A proposed control can increase only the target score, not the after score.

## Output Guidance

Include:

- total score and release gate label
- six-layer subtotal
- top 5 score gaps
- before/target/after table when applicable
- evidence for every score of 4 or 5
- blocker override notes

If evidence is missing, score conservatively.

For calibration examples, read `references/score-calibration.md`.
