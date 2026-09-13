---
name: structured-debugging
description: >-
  Systematic debugging methodology: reproduce, isolate, hypothesize, test, and fix. Use when investigating bugs, crashes, or unexpected behavior that resists a quick fix.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: automation
  tags: [debugging, methodology, investigation, root-cause, testing]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: structured-debugging
    summary: Systematic debugging from reproduce to verified fix
  derived_from:
    - name: ce-debug
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Structured Debugging

## When to use

Activate when a bug, crash, or unexpected behavior resists a quick fix. Use when the cause is not immediately obvious from the error message or when the issue is intermittent or environment-dependent.

## Procedure

1. Reproduce the issue reliably. Record the exact steps, inputs, environment, and error output.
2. Isolate the scope. Binary search through code, config, and data to narrow down where the behavior diverges from expected.
3. Form a hypothesis. Write a one-sentence theory about the root cause and the evidence supporting it.
4. Test the hypothesis. Make the smallest possible change that would confirm or refute it.
5. If the hypothesis is wrong, discard it and form a new one. Do not accumulate partial fixes.
6. Once confirmed, implement the fix. Run the full test suite.
7. Add a regression test that captures the original failure mode.

## Guardrails

- Do not apply fixes without a confirmed root cause. Masking symptoms creates harder bugs later.
- Do not skip the reproduction step. Unreproducible bugs cannot be verified as fixed.
- Do not make multiple changes at once during isolation. One variable at a time.
- Do not delete logs or error paths to silence the error. Fix the cause, not the messenger.

## Examples

### Good

> Reproduced the crash with a minimal test case, isolated it to a null check missing in the parser, wrote a hypothesis, confirmed with a one-line fix, added a regression test, full suite passes.

### Bad

> Added a try/catch around the failing code, error stopped appearing, shipped it. The same null value caused silent data corruption two weeks later.

## Verification

- The original reproduction case no longer triggers the issue.
- A regression test exists and passes.
- The full test suite passes.
- The fix is minimal and targeted to the confirmed root cause.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/structured-debugging
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: structured-debugging
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/structured-debugging/raw -o .cursor/skills/structured-debugging/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/structured-debugging.md and install it as a project skill at skills/structured-debugging/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```