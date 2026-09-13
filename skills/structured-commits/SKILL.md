---
name: structured-commits
description: >-
  Write focused commits with clear messages that explain why. Stage logically grouped changes and avoid mixing unrelated work. Use when preparing changes for review or history clarity.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: git
  tags: [git, commits, messages, staging, history]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: structured-commits
    summary: Focused commits with messages that explain why
  derived_from:
    - name: ce-commit
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Structured Commits

## When to use

Activate when staging changes for a commit. Use when the working tree has multiple unrelated changes that should be split into separate commits.

## Procedure

1. Review the full diff. Understand every change before staging.
2. Group changes by logical concern. A commit should do one thing.
3. Stage each group separately using git add -p for partial-file staging.
4. Write the commit message: imperative mood, under 72 chars, explain why not what.
5. Commit: git commit -m "<subject>" -m "<body>".
6. Repeat for each logical group.

## Guardrails

- Do not mix unrelated changes in one commit. Split them.
- Do not write commit messages that restate the diff. Explain the reasoning.
- Do not commit broken code. Each commit should build and pass tests.
- Do not use vague subjects like "fix" or "update."

## Examples

### Good

> Two commits: one fixing a null pointer (body explains the input path), one bumping pytest (body lists breaking changes). Each builds and passes tests.

### Bad

> One commit: "various fixes" containing a bug fix, a dependency bump, whitespace, and a new feature. Reviewer cannot bisect.

## Verification

- Each commit message has a specific subject and a body explaining why.
- git log --oneline reads as a narrative of changes.
- Each commit individually builds and passes tests.
- No commit mixes unrelated concerns.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/structured-commits
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: structured-commits
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/structured-commits/raw -o .cursor/skills/structured-commits/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/structured-commits.md and install it as a project skill at skills/structured-commits/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```