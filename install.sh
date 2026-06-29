#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESTINATION="${1:-$HOME/.codex/skills/agent-launch-gate}"

mkdir -p "$DESTINATION"

if command -v rsync >/dev/null 2>&1; then
  rsync -a \
    --exclude ".git" \
    --exclude ".github" \
    "$SOURCE_DIR/" "$DESTINATION/"
else
  find "$SOURCE_DIR" -mindepth 1 -maxdepth 1 \
    ! -name ".git" \
    ! -name ".github" \
    -exec cp -R {} "$DESTINATION/" \;
fi

echo "Installed Agent Launch Gate to $DESTINATION"

VALIDATOR="$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py"
if [[ -f "$VALIDATOR" ]]; then
  PYTHON_BIN=""
  if command -v python3 >/dev/null 2>&1 && python3 --version >/dev/null 2>&1; then
    PYTHON_BIN="python3"
  elif command -v python >/dev/null 2>&1 && python --version >/dev/null 2>&1; then
    PYTHON_BIN="python"
  fi

  if [[ -n "$PYTHON_BIN" ]]; then
    "$PYTHON_BIN" -X utf8 "$VALIDATOR" "$DESTINATION"
  else
    echo "Python was not found or is not executable."
    echo "Install completed, but validation was skipped."
  fi
else
  echo "Validator not found at $VALIDATOR"
  echo "Install completed, but validation was skipped."
fi
