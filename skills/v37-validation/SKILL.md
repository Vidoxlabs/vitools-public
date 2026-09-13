---
name: v37-validation
description: >-
  Validate changes against operational expectations using
  evidence-governed verification. Use before merging changes that affect
  infrastructure, orchestration, or operational safety, and when
  investigating suspected regressions.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: safety
  tags: [safety, validation, infra]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: v37-validation
    summary: Validate changes against operational expectations
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# V37 Validation

## When to use

Use this skill before merging changes that affect infrastructure
verification, orchestration, or operational safety. Also use when
investigating a suspected regression in system behavior.

## Procedure

1. Identify the affected surface: runtime mode, host verification,
   diagnostics, or infrastructure assumptions.
2. Run the relevant checks: unit tests, integration tests, linters, and
   CI gates.
3. Verify behavior against documented operational invariants. Do not
   invent workflows or assume untested behavior.
4. Capture evidence: links to logs, diffs, and failing checks. Record
   summary findings with pass or fail for each check.
5. If any check cannot be run, document which check was skipped and why.

## Guardrails

- Do not mark a change as validated without running at least one
  concrete verification step.
- Prefer evidence-backed conclusions. If evidence is missing, document
  the unknown explicitly.
- Do not skip a failing check by rationalizing it. Either fix the issue
  or document the deviation with a justification.
- Never suppress or delete evidence of a failed check.

## Examples

### Good

> CI passed. Host verification now enforces the new check. Logs show
> the expected behavior across three test runs. No regressions
> observed. One optional lint check was skipped because the linter is
> not installed in this environment; documented in the PR description.

### Bad

> Looks fine. Did not run the checks because the change is small and
> unlikely to break anything.

## Verification

- Confirm all required checks are green. For any check that was not
  run, confirm the skip is documented with a reason.
- Re-read the change summary and confirm it matches the evidence
  collected.

## Install

Repository installers (`npx skills add`, Claude marketplace) are not advertised for this revision: they follow GitHub default `main`, which is not this curated set.

```bash
curl -fsSL https://vidoxlabs.dev/vitools/raw/skills/v37-validation.md -o .cursor/skills/v37-validation/SKILL.md
```

```text
Fetch https://vidoxlabs.dev/vitools/raw/skills/v37-validation.md and install it as a project skill at skills/v37-validation/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
