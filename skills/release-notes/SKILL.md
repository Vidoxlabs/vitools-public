---
name: release-notes
description: >-
  Generate release notes from commit history between two tags. Categorize by features, fixes, and breaking changes. Use when cutting a release or producing a changelog.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: docs
  tags: [docs, release, changelog, commits, versioning]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: release-notes
    summary: Generate release notes from commit history
  derived_from:
    - name: ce-release-notes
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Release Notes

## When to use

Activate when cutting a release tag or producing a changelog from commit history.

## Procedure

1. Identify the range: git log <last-tag>..HEAD --oneline.
2. Read every commit message. Note the subject and body.
3. Categorize: Features, Fixes, Breaking Changes, Other.
4. Write a summary for each category. Group related commits.
5. Add a migration section if breaking changes require user action.
6. Write to CHANGELOG.md or release description.

## Guardrails

- Do not list every commit verbatim. Synthesize into user-facing impact.
- Do not omit breaking changes. These must be prominent.
- Do not include internal-only changes unless they affect performance.
- Do not invent features not in the commit history.

## Examples

### Good

> Three sections: Breaking Changes (1 item with migration steps), Features (2 items from 5 commits), Fixes (3 items).

### Bad

> Copy-pasted all 40 commit subjects into a flat list. Breaking change buried at line 23.

## Verification

- Every breaking change from the diff is in the Breaking Changes section.
- The notes are categorized, not a flat commit log.
- A user can read the notes and know what to do when upgrading.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/release-notes
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: release-notes
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/release-notes/raw -o .cursor/skills/release-notes/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/release-notes.md and install it as a project skill at skills/release-notes/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```