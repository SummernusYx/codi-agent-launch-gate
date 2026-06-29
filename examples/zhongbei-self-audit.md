# Example: 中杯 Self-Audit

This is a style example for auditing Agent Launch Gate itself. It is not a fixed expected score.

## Agent Launch Score

| Metric | Before |
|---|---:|
| Total score | 63 / 100 |
| Release gate | Internal test only |

Critical blocker override: none found in skill content.

## Top Findings

| Severity | Area | Finding | Evidence | Action |
|---|---|---|---|---|
| High | Repo packaging | The parent repo may ignore the skill files, so default git/rg views can miss the package. | `.gitignore` allowlist behavior in parent repo | Before publishing, create a clean repo or allowlist this package. |
| Medium | Open source readiness | No public README/LICENSE/SECURITY layer exists yet. | Skill folder contains only skill files and templates. | Add repo-level packaging files outside or around the skill package. |
| Medium | Validation | Skill validation exists, but no repeatable self-test command or CI gate is packaged. | `quick_validate.py` was run manually. | Add release checklist or CI example before public launch. |
| Medium | Examples | Only one self-audit example is present. | `examples/zhongbei-self-audit.md` | Add 大杯 and 超大杯 examples after real runs. |
| Low | Score calibration | 0-5 scoring rubric exists, but no calibration examples for every score level. | `references/scorecard.md` | Add calibration notes if users disagree on scoring. |

## Six-Layer Subtotal

| Layer | Before | Notes |
|---|---:|---|
| Core runtime | 13 / 20 | Scope and mode boundaries are clear; executable runtime is not applicable. |
| Configuration | 12 / 20 | Policy and confirmation rules exist; repo packaging still missing. |
| Capability | 12 / 20 | MCP, docs, memory, and external send are covered as review targets. |
| Orchestration | 10 / 15 | Mode flow and confirmation gates are clear; CI/repeatable self-test is not packaged. |
| Guardrails | 12 / 20 | Prompt injection, secrets, sandbox, and approvals are covered; hooks are only suggested. |
| Observability | 4 / 5 | Evidence-backed completion is explicit. |

## Top Score Gaps

| Priority | Gap | Why It Matters | Suggested Fix |
|---:|---|---|---|
| 1 | Git/repo visibility | Ignored files can disappear from default tooling. | Publish from a clean repo or fix allowlist. |
| 2 | README/LICENSE/SECURITY missing | Public users need install, scope, and reporting guidance. | Add repo-layer docs before GitHub release. |
| 3 | No packaged CI/self-test | Manual validation is easy to forget. | Add a release checklist or CI sample. |
| 4 | Few examples | Users need to understand score outputs. | Add real 中杯/大杯/超大杯 examples. |
| 5 | Score calibration | Different agents may score differently. | Add examples for 0-5 levels. |

## 大杯 Upgrade

Generate repo packaging files, add a release checklist, and add score calibration examples. Do not change global Codex configuration during this step.
