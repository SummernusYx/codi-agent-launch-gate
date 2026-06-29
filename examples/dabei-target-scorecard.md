# Example: 大杯 Target Scorecard

This example shows the distinction between current score, proposed target score, and verified after score.

## Agent Launch Score

| Metric | Before | Target | After |
|---|---:|---:|---:|
| Total score | 63 / 100 | 78 / 100 | Not calculated |
| Release gate | Internal test only | Ready with accepted risk | Not calculated |

Critical blocker override: none in the skill content. Repo publishing is not ready until packaging files are created.

## Proposed Changes

| Change | Score Area | Expected Impact | Why It Is Target Only |
|---|---|---:|---|
| Add repo-level README, LICENSE, and SECURITY notes | Configuration / Observability | +5 | Not written or reviewed yet. |
| Add clean publishing repo or allowlist files in `.gitignore` | Configuration | +4 | Current parent repo still ignores the package. |
| Add CI or release checklist for `quick_validate.py` | Guardrails / Observability | +4 | Validation is manual until CI/checklist exists. |
| Add 大杯 and 超大杯 real examples | Observability | +2 | Example quality improves after real runs. |

## Rule

Do not copy target values into after values until the changes exist and have evidence.
