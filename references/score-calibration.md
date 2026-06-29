# Score Calibration

Use this when scores feel subjective. The purpose is consistency, not false precision.

## General Pattern

- 0: absent or unsafe.
- 1: mentioned in conversation, but not written down.
- 2: written down, but incomplete or not connected to workflow.
- 3: usable and connected to workflow, but not verified or enforced.
- 4: verified by local evidence and clear enough for another agent to follow.
- 5: verified, repeatable, automated or strongly gated, and documented with owner behavior.

## Example: Prompt Injection Defense

- 0: remote webpages or docs can influence instructions without any warning.
- 1: the user has said "be careful", but no policy exists.
- 2: a policy says remote content is untrusted, but it is not connected to browsing or doc retrieval workflows.
- 3: policy exists and the workflow reminds the agent to treat remote content as data.
- 4: policy exists, workflow references it, and reports must cite evidence when remote content is used.
- 5: all of the above plus repeatable tests or review gates for remote-content handling.

## Example: MCP/Tool Inventory

- 0: tools are used without inventory.
- 1: a few tools are known informally.
- 2: inventory exists, but authority/auth/data exposure are missing.
- 3: inventory includes purpose, authority, auth, and local/remote behavior.
- 4: inventory is tied to least-privilege decisions and risk notes.
- 5: inventory is versioned, reviewed, and checked during release.

## Example: Evidence-Backed Completion

- 0: outputs say "done" without proof.
- 1: proof is sometimes mentioned but inconsistent.
- 2: reports have an evidence column but it is often vague.
- 3: material findings cite files, commands, or config keys.
- 4: completion claims include validation output or reproducible checks.
- 5: validation is automated or enforced before release claims.

## Caution

Do not increase a score because a fix is easy. Score only what exists or has been applied and verified.
