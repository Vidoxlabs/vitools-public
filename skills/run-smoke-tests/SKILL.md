---
name: run-smoke-tests
description: >-
  Run end-to-end smoke tests, debug failures, and verify fixes before
  shipping. Use when you need fast verification that core user flows
  still work after changes.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: automation
  tags: [testing, smoke-tests, e2e, playwright, automation, ci]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: run-smoke-tests
    summary: Run smoke tests, debug failures, and verify fixes
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Run Smoke Tests

## When to use

Activate when you need end-to-end smoke verification before or after
changes. Use when shipping a feature, verifying a fix, or running a
quick health check on core user flows.

## Procedure

1. Identify the smoke test suite: Playwright tests tagged as smoke,
   a dedicated `smoke` script in `package.json`, or a test directory
   with smoke tests.
2. Run the smoke tests with the appropriate test runner command.
3. If all pass, report green. If any fail, proceed to debugging.
4. For each failure, read the test output: assertion error, timeout,
   element not found, or network error.
5. Determine whether the failure is caused by the code change or a
   pre-existing issue. Compare against the main branch if uncertain.
6. Fix the code or update the test if the test expectation is stale.
7. Re-run the smoke tests. Confirm all pass before reporting done.

## Guardrails

- Do not skip or delete a failing smoke test. Fix the code or mark
  the test as skipped with a reason and a follow-up issue.
- Do not increase the timeout to make a flaky test pass. Investigate
  the root cause.
- Do not run only a subset of smoke tests unless the user explicitly
  scopes the request.
- Do not report green without re-running after a fix.

## Examples

### Good

> Ran 12 smoke tests. 1 failed: login flow timed out at the password
> step. Found a CSS selector change in the auth component. Fixed the
> selector in the test, re-ran, all 12 passed.

### Bad

> Ran smoke tests, saw a failure, increased the timeout from 5s to
> 30s, and reported green without investigating why the test was
> slow.

## Verification

- All smoke tests pass on the final run.
- No tests were deleted or skipped without a documented reason.
- Failures were traced to a specific code or test issue.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/run-smoke-tests
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: run-smoke-tests
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/run-smoke-tests/raw -o .cursor/skills/run-smoke-tests/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/run-smoke-tests.md and install it as a project skill at skills/run-smoke-tests/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
