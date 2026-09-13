---
name: work-verification
description: >-
  Verify completed work with a dedicated subagent that reviews diffs, runs builds, checks tests, and confirms compliance with project instructions. Use when validating work before shipping.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: eval
  tags: [verification, review, build, tests, compliance]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: work-verification
    summary: Verify work with a dedicated subagent before shipping
  derived_from:
    - name: anthropic-check-work
      license: Proprietary
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Work Verification

## When to use

Activate when verifying completed work before shipping. Use when a second set of eyes is needed to catch issues the author missed.

## Procedure

1. Spawn a verification subagent with read-only access to the repository.
2. The subagent reviews the full diff against the base branch.
3. It runs the build and test suite to confirm they pass.
4. It checks compliance with AGENTS.md and project conventions.
5. It reports: pass or fail, with specific findings.
6. If fail, the author addresses each finding before re-verifying.
7. Only ship after the verification subagent reports pass.

## Guardrails

- Do not let the verification subagent modify code. It reports, not fixes.
- Do not skip the build and test step. They are the primary signal.
- Do not ignore findings. Each must be addressed or explicitly dismissed.
- Do not use the same context as the author. Fresh eyes catch blind spots.

## Examples

### Good

> Verification subagent reviewed the diff, ran build and tests (all pass), checked 3 AGENTS.md rules (1 violation found: missing guardrail). Author fixed the guardrail. Re-verified: pass. Shipped.

### Bad

> Author self-reviewed the diff and said it looks good. Tests were not run. An AGENTS.md rule was violated. Shipped anyway.

## Verification

- Verification subagent reviewed the diff independently.
- Build and test suite pass.
- AGENTS.md compliance is checked.
- All findings are addressed before shipping.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/work-verification
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: work-verification
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/work-verification/raw -o .cursor/skills/work-verification/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/work-verification.md and install it as a project skill at skills/work-verification/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```