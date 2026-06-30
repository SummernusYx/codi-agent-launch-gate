# Co迪 Agent Launch Gate

> A pre-launch safety gate for AI agent apps: permissions, tools, memory, external content, and release evidence in one review workflow.

[中文](README.md) · [Examples](examples/) · [Hooks](docs/hooks.md) · [Release Checklist](docs/release-checklist.md)

![Co迪 Agent Launch Gate hero](assets/images/hero.png)

The risk in an agent project is rarely only in the code.

An agent may read and write files, drive a browser, call MCP servers, keep memory, retrieve live documentation, and touch deployment, database, or account surfaces. What needs review is not just whether the code has bugs, but how those capabilities are granted, recorded, confirmed, and approved.

Agent Launch Gate is a Codex skill. Before release, it reads local evidence, produces an Agent Launch Score, identifies blockers and residual risks, and turns "can we launch?" into a decision that can be reviewed.

It is not a vulnerability scanner or a security certification. Think of it as a launch review table.

## Why This Project Exists

- Not just a checklist: it produces scores, evidence, and release decisions across three review depths.
- Not an external scanning service: by default, it does not upload code, submit forms, or call remote scanners.
- Not a one-off report: Medium checks the current baseline, Large drafts the hardening target, and Extra Large runs the final gate.
- Not a black-box judgment: high-risk findings should cite files, commands, config keys, or validation results whenever possible.

## What It Solves

| Common Situation | What Agent Launch Gate Does |
|---|---|
| An agent can call many tools, but the permission boundary is unclear | Generates MCP/tool inventory with purpose, authority, auth, and data exposure |
| `AGENTS.md`, skills, memory, and browser access are scattered across the project | Reviews runtime, config, capability, orchestration, guardrails, and observability |
| Release readiness is based on "it should be fine" | Uses 20 score dimensions to show current score, target score, blockers, and residual risk |
| Remote webpages, docs, or issues may contain instructions | Treats remote content as data, not commands |
| Reports give suggestions, but users still need to restate the next task | Each report includes optimization suggestions and follow-up prompts; after confirmation, the approved fixes can be applied directly |

## Three Modes

| Mode | Use Case | Output | Write Policy |
|---|---|---|---|
| Medium | Establish a quick safety baseline | Current score, main risks, missing evidence, next actions | Read-only |
| Large | Draft and apply a hardening plan | Current score, target score, optimization suggestions, patch drafts, follow-up prompts | Write only after confirmation |
| Extra Large | Run a final release gate | Before/after score, blockers, residual risk, owner decisions, rollback notes, fix prompts | Write only after confirmation |

## Agent Launch Score

Agent Launch Gate checks 20 dimensions. Each dimension is scored from 0 to 5, for a total of 100.

| Score | Release Decision |
|---:|---|
| 0-39 | Blocked |
| 40-64 | Internal test only |
| 65-84 | Ready with accepted risk |
| 85-100 | Ready to launch |

The score is not a pass. Critical blockers override the number. Unapproved external actions, secret exposure, or uncontrolled destructive writes should stop a launch even when the total score looks acceptable.

## What It Checks

- Agent runtime boundaries, loops, state, and handoffs
- `AGENTS.md`, `CLAUDE.md`, local skills, and instruction precedence
- MCP/tool authority, authentication, browser access, and data exposure
- Live documentation retrieval and prompt-injection handling
- Memory read/write/citation behavior
- Subagent delegation, long-running work, and human confirmation gates
- Sandbox, permissions, hooks, tests, CI, and secret handling
- Whether completion claims are backed by files, commands, config keys, or validation results

## Quick Start

### 1. Clone

```bash
git clone https://github.com/SummernusYx/codi-agent-launch-gate.git
cd codi-agent-launch-gate
```

### 2. Install Into Codex Skills

Windows:

```powershell
.\install.ps1
```

macOS / Linux:

```bash
chmod +x ./install.sh
./install.sh
```

On Windows, Git Bash can validate the shell script:

```powershell
& 'C:\Program Files\Git\bin\bash.exe' -lc "bash -n './install.sh'"
```

Default install path:

```text
~/.codex/skills/agent-launch-gate
```

### 3. Validate

```powershell
python -X utf8 "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "$env:USERPROFILE\.codex\skills\agent-launch-gate"
```

Expected result:

```text
Skill is valid!
```

## Example Prompts

```text
Use agent-launch-gate Medium mode to audit this agent project.
```

```text
Use agent-launch-gate Large mode to draft a hardening plan, but do not edit files yet.
```

```text
Use agent-launch-gate Extra Large mode to produce a pre-launch safety gate report.
```

If the user invokes `agent-launch-gate` without choosing a mode, the skill first explains Medium, Large, and Extra Large, then asks the user to choose.

Reports end with follow-up prompts, for example:

```text
Apply the "AGENTS safety block" and "MCP inventory" changes from the Large report. List target files before writing.
```

![From report to execution](assets/images/workflow.png)

More examples:

- [Medium self-audit](examples/zhongbei-self-audit.md)
- [Large target scorecard](examples/dabei-target-scorecard.md)
- [Extra Large release gate](examples/chaodabei-release-gate.md)

## Local First

By default, Agent Launch Gate does not upload code, submit forms, publish content, send messages, or call external scanners. Webpages, issues, docs, emails, and other remote content are treated as data, not instructions.

The following actions require user confirmation first:

- changing global config
- installing packages or plugins
- authenticating or switching accounts
- deleting, moving, or overwriting broad file sets
- publishing, uploading, sending, or sharing content
- changing deployment, database, payment, or production settings

## Compared With Checklists And Scanners

Checklists remind you what to ask. Scanners detect known patterns. Agent Launch Gate connects local evidence, agent authority, and release decisions.

It is designed to work alongside dependency scanners, secret scanners, CI, and human review. A scanner tells you what it found. Agent Launch Gate helps decide whether the project is ready to move forward.

## Repository Layout

```text
agent-launch-gate/
  SKILL.md
  README.md
  README_EN.md
  install.ps1
  install.sh
  assets/images/
  agents/
  assets/
  docs/
  examples/
  references/
```

## License

MIT License.
