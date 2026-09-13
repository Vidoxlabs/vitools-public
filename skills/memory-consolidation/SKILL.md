---
name: memory-consolidation
description: >-
  Consolidate and maintain agent memory files: merge duplicates, fix stale facts, prune the index, and separate durable preferences from dated information. Use when cleaning up accumulated memory.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: docs
  tags: [memory, consolidation, maintenance, preferences, agent-memory]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: memory-consolidation
    summary: Consolidate and maintain agent memory files
  derived_from:
    - name: cowork-consolidate-memory-update-start
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Memory Consolidation

## When to use

Activate when memory files have grown stale, duplicated, or disorganized. Use during periodic cleanup or when switching project contexts.

## Procedure

1. Inventory all memory files: list every file and its last modified date.
2. Identify duplicates: files covering the same topic or preference.
3. Merge duplicates into a single file, keeping the most accurate and recent information.
4. Separate durable from dated: preferences, working style, and relationships are durable. Specific projects, deadlines, and one-off tasks are dated.
5. Retire dated files whose time has passed. Fold lasting takeaways into durable files.
6. Update the index: remove dead links, add new files, fix stale references.
7. Verify: read the consolidated set and confirm it is coherent.

## Guardrails

- Do not delete memory without reading it first. Check for lasting takeaways.
- Do not merge files that serve different purposes. Keep concerns separate.
- Do not leave the index stale. Every file should be linked and accurate.
- Do not consolidate without a backup of the original files.

## Examples

### Good

> Consolidated 15 memory files into 8: merged 3 duplicate preference files, retired 4 dated project files (folded lasting takeaways into durable ones), updated the index with accurate links. Memory set is now coherent.

### Bad

> Deleted 10 memory files because they looked old. Lost a durable preference that was in a dated project file. Index still points to deleted files.

## Verification

- No duplicate topics remain across memory files.
- Dated information is retired or folded into durable files.
- The index is accurate with no dead links.
- The consolidated set reads coherently.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/memory-consolidation
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: memory-consolidation
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/memory-consolidation/raw -o .cursor/skills/memory-consolidation/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/memory-consolidation.md and install it as a project skill at skills/memory-consolidation/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```