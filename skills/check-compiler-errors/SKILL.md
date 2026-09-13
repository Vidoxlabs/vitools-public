---
name: check-compiler-errors
description: >-
  Run compile and type-check commands, parse the output, and report
  failures with file, line, and fix suggestions. Use when build or
  type-check failures are blocking local validation or CI.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: git
  tags: [build, type-check, compiler, debugging, ci]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: check-compiler-errors
    summary: Run compile and type-check commands and report failures
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Check Compiler Errors

## When to use

Activate when compile or type-check failures are blocking local
validation or CI. Use when the user reports build errors, type errors,
or when a lint or compile step fails during development.

## Procedure

1. Identify the build system and the correct compile or type-check
   command (from `package.json` scripts, `Makefile`, `pyproject.toml`,
   or `Cargo.toml`).
2. Run the command and capture the full output.
3. Parse the output for errors: file path, line number, error message,
   and error code.
4. Group errors by file to minimize context switching.
5. For each error, identify the root cause: missing import, type
   mismatch, syntax error, or missing dependency.
6. Apply fixes in file order. Re-run the compile command after each
   fix to confirm the error is resolved.

## Guardrails

- Do not suppress type errors with `any` or `@ts-ignore` without a
  linked issue explaining why.
- Do not skip the compile step. Running it is the only way to confirm
  the fix worked.
- Do not fix errors in files unrelated to the task unless they block
  the build.
- Do not guess the build command. Read the manifest file to find it.

## Examples

### Good

> Ran `tsc --noEmit`, found 3 errors in `src/api.ts`. Fixed a missing
> return type on line 42, a wrong import on line 8, and a null check
> on line 67. Re-ran `tsc` — all 3 resolved.

### Bad

> Ran `tsc --noEmit`, saw errors, added `// @ts-ignore` to each line
> without investigating the root cause.

## Verification

- The compile or type-check command exits 0.
- No `@ts-ignore`, `any`, or equivalent suppression was added.
- Each fix addresses the root cause, not the symptom.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/check-compiler-errors
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: check-compiler-errors
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/check-compiler-errors/raw -o .cursor/skills/check-compiler-errors/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/check-compiler-errors.md and install it as a project skill at skills/check-compiler-errors/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
