# Apply Actions

Use this when Agent Launch Gate produces recommendations. The goal is to turn a report into an executable next step: the user can confirm one scoped follow-up prompt, then the agent can apply the approved optimization plan.

## Rule

Every material recommendation should include a `继续指令` / `Apply prompt`.

The prompt should:

- name the mode
- name the exact change group
- state whether file writes are allowed
- keep external actions blocked unless explicitly requested
- avoid broad wording like "fix everything"
- make it clear that approved changes can be executed after confirmation

## 中杯 Follow-Ups

Use 中杯 follow-ups to move from read-only audit into a scoped hardening plan.

Examples:

```text
用 agent-launch-gate 大杯处理中杯报告里的前 3 个高风险项，先只给补丁草案，不要写文件。
```

```text
用 agent-launch-gate 大杯生成 MCP/tool inventory 和权限清单，写入前先给我看计划。
```

## 大杯 Follow-Ups

Use 大杯 follow-ups to apply a specific approved change group.

Examples:

```text
按大杯方案应用“AGENTS 安全块”和“MCP inventory”两项改动，写入前先列出目标文件。
```

```text
只应用大杯报告里的第 1 项修复，其他建议先不动。
```

```text
把大杯报告里的 target scorecard 转成待办清单，不改文件。
```

## 超大杯 Follow-Ups

Use 超大杯 follow-ups to resolve blockers or produce owner-facing release artifacts.

Examples:

```text
按超大杯报告修复所有 blocker，但发布、上传和外发动作仍然禁止。
```

```text
把超大杯报告里的 accepted residual risk 整理成发布说明，不发布。
```

```text
重新跑超大杯，只验证刚才改过的文件和评分变化。
```

## Output Format

At the end of each report, add:

```markdown
## 可以直接继续的指令

- `...`
- `...`
```

For English reports:

```markdown
## Follow-Up Prompts

- `...`
- `...`
```
