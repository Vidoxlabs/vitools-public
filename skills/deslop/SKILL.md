---
name: deslop
description: >-
  Remove AI-generated code slop from a diff: unnecessary comments,
  redundant abstractions, placeholder text, and inconsistent style.
  Use when cleaning up AI-generated code.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: eval
  tags: [code-quality, cleanup, ai-output, style, review]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: deslop
    summary: Strip AI-generated code slop from diffs before review
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Deslop

## When to use

Activate after generating or receiving AI-produced code that will be
committed or reviewed. Use when the diff contains obvious AI patterns:
verbose obvious comments, over-abstracted wrappers, placeholder
strings, inconsistent naming, or code that restates the obvious.

## Procedure

1. Read the full diff and flag every instance of: comments that
   restate what the code already says, redundant single-call wrappers,
   placeholder text like `TODO: implement this`, inconsistent style,
   and verbose error messages that add no debugging value.
2. Remove or rewrite each flagged item. Prefer no comment over a
   useless one. Prefer inline code over a one-line helper.
3. Check that removals do not change behavior. Run tests after cleanup.
4. Verify the diff now reads as if written by a developer who
   understands the codebase.

## Guardrails

- Do not remove comments that explain non-obvious business logic or
  regulatory requirements.
- Do not delete error handling. Replace empty catches with proper
  handling, not removal.
- Do not flatten meaningful abstractions used by multiple callers.
- Do not change behavior while deslopping — style only.

## Examples

### Good

> Removed a 4-line comment above `return result`, deleted a
> `DataProcessor` wrapper that called `process_data` once, replaced
> `// TODO: handle errors` with a real try/except. Diff is now
> smaller and behavior is identical.

### Bad

> Deleted a comment explaining a regulatory rounding rule because it
> "restated the code." Reviewer had to ask why the rounding was
> unusual.

## Verification

- Tests pass before and after deslopping.
- The diff is smaller after cleanup, not larger.
- A second reader can understand the code without asking what a
  section does.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/deslop
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: deslop
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/deslop/raw -o .cursor/skills/deslop/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/deslop.md and install it as a project skill at skills/deslop/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
