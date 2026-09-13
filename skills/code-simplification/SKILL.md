---
name: code-simplification
description: >-
  Simplify code without changing behavior. Remove indirection, inline single-use helpers, reduce nesting, and eliminate dead code. Use when reviewing or refactoring for clarity and maintainability.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: eval
  tags: [refactoring, clarity, dead-code, simplification, review]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: code-simplification
    summary: Simplify code without changing behavior
  derived_from:
    - name: ce-simplify-code
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Code Simplification

## When to use

Activate when reviewing a diff or refactoring a module for clarity. Use when code has excessive indirection, deep nesting, single-use helpers, or dead code paths.

## Procedure

1. Read the full function or module. Identify its single responsibility.
2. List every instance of: single-use helpers, nesting deeper than three levels, dead code paths, redundant conditionals.
3. Inline single-use helpers where the inlined version is clearer.
4. Flatten nesting with early returns or guard clauses.
5. Remove dead code. Confirm with a test run.
6. Run the test suite. Behavior must be identical.

## Guardrails

- Do not change behavior. Simplification is refactoring, not feature work.
- Do not inline helpers used by multiple callers. Check references before removing.
- Do not remove error handling paths. Simplify them, do not delete them.
- Do not merge conceptually distinct steps into one block.

## Examples

### Good

> Inlined a format_name helper called once, replaced 4-level nesting with guard clauses, removed dead branch. Tests pass, diff is 30 lines smaller.

### Bad

> Inlined a helper used by four other modules, merged two distinct validation steps, deleted an error path that was a fallback for a different input type.

## Verification

- Tests pass before and after simplification.
- The diff is smaller, not larger.
- A reader can trace the main logic path without jumping to helper definitions.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/code-simplification
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: code-simplification
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/code-simplification/raw -o .cursor/skills/code-simplification/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/code-simplification.md and install it as a project skill at skills/code-simplification/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```