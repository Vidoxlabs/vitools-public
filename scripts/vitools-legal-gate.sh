#!/usr/bin/env bash
# ViTools legal gate — block archive/vendor content from agent-facing paths.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail=0

# No symlinks from .agents into archive/vendor
if find .agents -type l 2>/dev/null | while read -r link; do
  target="$(readlink "$link" || true)"
  if [[ "$target" == *archive/vendor* ]]; then
    echo "ERROR: symlink from .agents to archive/vendor: $link -> $target"
    exit 1
  fi
done; then
  :
else
  fail=1
fi

# platforms/ must not symlink into archive/vendor (doc links in emitted skills are OK)
if [[ -d platforms ]] && find platforms -type l -lname '*archive/vendor*' 2>/dev/null | grep -q .; then
  echo "ERROR: platforms/ contains symlink into archive/vendor"
  fail=1
fi

# .agents/ must not contain explicit archive/vendor path strings in authored files
if grep -rq "archive/vendor" .agents/ 2>/dev/null; then
  # Allow only in README documentation explaining the policy
  if ! grep -rq "archive/vendor" .agents/README.md .agents/AGENTS.md 2>/dev/null; then
    echo "ERROR: unexpected archive/vendor reference in .agents/"
    fail=1
  fi
fi

if [[ "$fail" -ne 0 ]]; then
  exit 1
fi

echo "Legal gate: no archive-to-agent path violations detected"
