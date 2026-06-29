# GitHub Positioning

This project should not compete as another generic AI security checklist. Position it as a local, coding-agent-native workflow that turns security review into a repeatable skill.

## Differentiators

- Tiered execution: 中杯, 大杯, 超大杯.
- Local-first by default: no uploads, no external scanning unless approved.
- Agent-aware: covers `AGENTS.md`, local skills, MCP, browser control, memory, permissions, hooks, and prompt injection.
- Evidence-first: findings cite local files, commands, and config keys.
- Human confirmation gates: write, publish, auth, delete, install, and external-send actions require explicit approval.

## README Spine

1. Name the pain: AI agents can act across files, browser, tools, memory, and remote docs; most projects do not have one place to review that authority.
2. Show the promise: choose 中杯 for a quick check, 大杯 for hardening, 超大杯 for release sign-off.
3. Show a tiny example: before/after risk table.
4. Explain local-first safety.
5. Document installation and invocation.
6. Include comparison with scanners and checklists: this skill complements scanners by creating a workflow and decision trail.

## Naming Tone

Prefer concrete names over dramatic security branding. Good directions:

- guardrail
- launch gate
- safety radar
- safety kit
- release check

Avoid names that imply perfect protection.
