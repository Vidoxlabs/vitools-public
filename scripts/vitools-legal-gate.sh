#!/usr/bin/env bash
# ViTools legal gate — enforce license, origin, and content rules.
# Fails CI if any violation is found in skills/ or agents/.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail=0

# --- 1. skills/ and agents/ must have license frontmatter ---
if [[ -d skills ]]; then
  while IFS= read -r -d '' skill_md; do
    if ! grep -q '^license:' "$skill_md" 2>/dev/null; then
      echo "ERROR: $skill_md missing 'license:' frontmatter"
      fail=1
    fi
  done < <(find skills -name "SKILL.md" -print0 2>/dev/null)
fi

if [[ -d agents ]]; then
  while IFS= read -r -d '' agent_md; do
    if ! grep -q '^license:' "$agent_md" 2>/dev/null; then
      echo "ERROR: $agent_md missing 'license:' frontmatter"
      fail=1
    fi
  done < <(find agents -name "AGENT.md" -print0 2>/dev/null)
fi

# --- 2. No Anthropic branding instructions in first-party skills ---
if [[ -d skills ]]; then
  while IFS= read -r -d '' skill_md; do
    if grep -qi "keep.*anthropic.*branding\|anthropic brand colors\|anthropic's official brand" "$skill_md" 2>/dev/null; then
      echo "ERROR: $skill_md contains Anthropic branding instructions"
      fail=1
    fi
    if grep -q 'publisher: google' "$skill_md" 2>/dev/null; then
      if ! grep -q 'origin: derived' "$skill_md" 2>/dev/null; then
        echo "ERROR: $skill_md has publisher: google without origin: derived"
        fail=1
      fi
      if ! grep -q 'derived_from' "$skill_md" 2>/dev/null; then
        echo "ERROR: $skill_md has publisher: google without derived_from"
        fail=1
      fi
    fi
    name_line=$(grep '^name:' "$skill_md" 2>/dev/null | head -1)
    if echo "$name_line" | grep -qi 'claude\|anthropic'; then
      echo "ERROR: $skill_md has 'claude' or 'anthropic' in name field"
      fail=1
    fi
  done < <(find skills -name "SKILL.md" -print0 2>/dev/null)
fi

# --- 3. No vendor LICENSE.txt in skills/ ---
if [[ -d skills ]]; then
  if find skills -name "LICENSE.txt" -print0 2>/dev/null | grep -q .; then
    echo "ERROR: LICENSE.txt found in skills/"
    find skills -name "LICENSE.txt" -print 2>/dev/null | while read -r f; do
      echo "  - $f"
    done
    fail=1
  fi
fi

# --- 4. Catalog count must match promoted public items ---
if [[ -f catalog/vitools.catalog.json ]]; then
  catalog_count=$(python3 -c "
import json
with open('catalog/vitools.catalog.json') as f:
    d = json.load(f)
print(sum(1 for i in d.get('items', []) if i.get('public', False)))
" 2>/dev/null || echo "0")

  promoted_count=$(python3 -c "
import json
with open('catalog/vitools.catalog.json') as f:
    d = json.load(f)
counts = d.get('counts', {})
print(counts.get('skills', 0) + counts.get('agents', 0))
" 2>/dev/null || echo "0")

  if [[ "$catalog_count" != "$promoted_count" ]]; then
    echo "ERROR: catalog count mismatch"
    fail=1
  fi
fi

if [[ "$fail" -ne 0 ]]; then
  echo ""
  echo "Legal gate: FAILED"
  exit 1
fi

echo "Legal gate: PASSED"