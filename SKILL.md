---
name: agent-launch-gate
description: Tiered safety baseline skill for AI agent applications. Use when the user asks to audit, harden, configure, or release-check an AI agent app, coding agent workflow, MCP setup, local skill package, AGENTS.md/CLAUDE.md policy, sandbox/permissions model, prompt-injection defenses, hooks, memory, live-doc retrieval, or deployment gates. Trigger on requests like "检查这个智能体应用是否安全", "给 agent 项目做安全基线", "发布前安全检查", "检查 MCP 权限", "配置 agent 安全策略", or similar security review intent.
---

# Agent Launch Gate

## Operating Rule

If the user invokes this skill or asks for an agent safety check without naming a mode, do not start auditing immediately. First introduce the three modes and ask the user to choose:

`我可以按三档做安全排查：中杯=只读快速摸底，给当前分数和主要风险；大杯=在中杯基础上给优化建议、目标分和补丁草案，确认后可执行；超大杯=做发布前门禁，给前后分数、blocker、残余风险和发布结论。你想用哪一杯？如果只是先看看，建议中杯。`

Proceed directly only when the user already selected 中杯, 大杯, 超大杯, or clearly asked for a specific depth such as quick audit, hardening plan, or release gate.

Do not send files, logs, secrets, prompts, memory, registry data, browser state, or repository content outside the local machine unless the user explicitly approves the exact action.

## Modes

- `中杯`: Read-only audit. Inspect the project, list risks, produce a prioritized checklist, and avoid edits.
- `大杯`: Hardening pass. Produce concrete config changes, templates, and patches. After user confirmation, apply approved changes and verify them.
- `超大杯`: Release gate. Produce evidence-backed sign-off, blockers, residual risk, incident plan, observability checks, and follow-up tasks. After user confirmation, resolve approved blockers or generate release artifacts.

Read the matching reference only after the mode is chosen:

- `references/modes/zhongbei.md` for 中杯.
- `references/modes/dabei.md` for 大杯.
- `references/modes/chaodabei.md` for 超大杯.

## Baseline Workflow

1. Identify the app boundary: repo root, agent runtime, tools, MCP servers, browser access, memory, deployment surface, and user-facing actions.
2. Inventory policy files: `AGENTS.md`, `CLAUDE.md`, `.codex/`, `.agents/`, MCP configs, hooks, CI gates, env examples, and permission settings.
3. Read `references/framework.md` and map findings onto the six-layer model.
4. Read `references/scorecard.md` and produce a scorecard for the selected mode.
5. Use the selected mode to produce the smallest useful output.
6. Keep evidence local and cite file paths, commands, or config keys for every material finding.
7. Separate confirmed issues from assumptions. Mark anything unverified.

## Outputs

Use `assets/audit-report-template.md` for reports. Include `assets/scorecard-template.md` whenever the user asks for a score, comparison, release readiness, or before/after change. For 大杯 or 超大杯, also consider:

- `assets/AGENTS.security.template.md` for a reusable safety block.
- `assets/mcp-inventory-template.md` for tool and MCP inventory.
- `assets/permissions-checklist-template.md` for local permission review.
- `assets/apply-prompts-template.md` for one-sentence follow-up commands that let the user continue safely.

For self-testing this skill, read `references/self-audit.md` and compare against `examples/zhongbei-self-audit.md`.

For turning recommendations into follow-up actions, read `references/apply-actions.md`.

## Open Source Packaging

For README, positioning, or launch copy, read `references/github-positioning.md` and `references/repo-packaging.md`. Keep the project differentiated as a coding-agent-native safety workflow with tiered modes, not a generic checklist or scanner.
