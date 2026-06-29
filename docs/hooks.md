# Hooks

Agent Launch Gate ships with two guardrails for project work.

## 1. Commit Preview Hook

Before committing, the Git hook generates a local HTML preview of staged changes:

```text
.git/commit-preview/index.html
```

It opens the page and asks for:

```text
APPROVE
```

Only then does the commit continue.

### Enable

```powershell
git config core.hooksPath .githooks
```

### Bypass

Use only when you intentionally do not need the preview:

```powershell
$env:SKIP_COMMIT_PREVIEW = "1"
git commit -m "message"
Remove-Item Env:\SKIP_COMMIT_PREVIEW
```

## 2. Long Request Planning Hook

This one is not a Git hook. It happens before coding work starts.

When a user request is longer than roughly 200 tokens, the agent should first switch into a planning posture:

1. restate the goal
2. extract constraints
3. split the work into steps
4. identify confirmation points
5. ask for approval before implementation

The reusable local skill is:

```text
E:\codex\.agents\skills\long-request-planner
```

Git cannot enforce this because Git only sees repository operations, not chat input. Codex skill routing can.
