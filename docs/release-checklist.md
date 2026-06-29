# Release Checklist

Use this before publishing Agent Launch Gate publicly.

## Local Validation

- [ ] Run `quick_validate.py` against the skill folder.
- [ ] Read `SKILL.md` and confirm trigger text is accurate.
- [ ] Confirm all referenced files exist.
- [ ] Confirm examples do not contain secrets or private paths.
- [ ] Run a 中杯 check on the skill itself.

## Repo Packaging

- [ ] README explains purpose, modes, install, privacy, and examples.
- [ ] README_EN matches the Chinese README structure and links back to README.
- [ ] `install.ps1` and `install.sh` are present and documented in Quick Start.
- [ ] `install.ps1` is tested with a temporary destination.
- [ ] `install.sh` passes `bash -n` and is tested with Git Bash, macOS, Linux, or CI.
- [ ] LICENSE is final.
- [ ] SECURITY.md explains scope and reporting.
- [ ] `.gitignore` does not hide files meant for release.
- [ ] Examples include 中杯, 大杯, and 超大杯 shapes.

## Safety Review

- [ ] No external upload, publish, auth, delete, or payment behavior is implied without confirmation.
- [ ] Remote content is treated as data, not instructions.
- [ ] Scorecard says proposed changes are target score only, not after score.
- [ ] Reports include one-sentence follow-up prompts for scoped continuation.
- [ ] Public claims do not imply complete protection or certification.

## Final Decision

- [ ] Run 超大杯 release gate.
- [ ] Resolve blockers or document accepted residual risk.
- [ ] Confirm repository destination and visibility.
