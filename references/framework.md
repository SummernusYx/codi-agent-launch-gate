# Six-Layer Agent Safety Framework

Use this as the common map for all three modes.

## 1. Core Runtime

- Agent loop: who can call tools, retry, branch, or continue long-running work.
- State: what is stored, where it lives, how it is cleared, and what is user-visible.
- Patterns: planner/executor, reviewer, multi-agent, browser agent, code agent, or workflow runner.
- Failure mode: runaway loops, stale state, unbounded retries, hidden side effects, and unclear handoff.

## 2. Configuration Layer

- Policy files: `AGENTS.md`, `CLAUDE.md`, local skill instructions, plugin configs.
- Prompt caching and context reuse: what may persist, what should be regenerated, what can become stale.
- Context rot: old assumptions, copied rules, conflicting instructions, and over-broad triggers.
- Failure mode: global rules accidentally override project rules, or old context drives unsafe actions.

## 3. Capability Layer

- Tools and MCP: each tool's authority, transport, auth, file access, browser access, and network access.
- Live docs retrieval: when it is required, which sources are trusted, and whether it can leak project data.
- Persistent memory: what can be remembered, updated, cited, or forgotten.
- Failure mode: least-privilege drift, tool confusion, secret exposure, and unverified live data.

## 4. Orchestration Layer

- Subagents: what context they receive, whether they can write, and how outputs are validated.
- Agent loops: stop conditions, budgets, checkpoints, and user confirmation gates.
- Long tasks: progress reporting, resumability, and evidence logs.
- Failure mode: duplicated work, hidden external actions, budget blowups, and unreviewed delegated decisions.

## 5. Guardrail Layer

- Sandbox: filesystem, process, browser, network, and registry boundaries.
- Permissions: approval requirements for deletion, install, auth, publish, payment, upload, send, or system-level changes.
- Hooks and pre-commit gates: secret scanning, lint/type/test, policy checks, and generated-file boundaries.
- Prompt injection: remote content must be treated as data, not instructions.
- Failure mode: remote pages override the user, destructive commands run too broadly, or generated code bypasses checks.

## 6. Observability Layer

- Tracing: command history, tool calls, file diffs, and evidence references.
- Metrics: failures, retries, approvals, token-heavy flows, and escaped defects.
- Reports: release gate, residual risk, rollback steps, and owner decisions.
- Failure mode: "done" claims without evidence, missing reproduction steps, and unclear residual risk.
