---
name: fix-ci
description: >-
  Find and fix failing CI checks by inspecting logs, identifying root cause,
  and applying focused fixes. Use when CI is red on a branch or PR.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: git
  tags: [ci, debugging, github, pull-requests, fixes]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: fix-ci
    summary: Diagnose and fix failing CI checks with focused root-cause fixes
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Fix CI

## When to use

Activate when a CI check is failing on a branch or pull request and the
root cause is not yet known. Use when logs show red, a status check is
blocked, or a merge is gated by a failing job.

## Procedure

1. Fetch the failing check name, job ID, and direct log URL from the PR
   status panel or CI CLI output.
2. Read the full log for the failing job, not just the final error line.
   Capture the failing command, the exit code, and any diff in output
   from prior green runs.
3. Classify the failure: code error, environment or dependency change,
   flaky test, config drift, or timeout.
4. For code errors, reproduce locally with the same command the CI ran.
   For environment issues, compare the CI runner config against the last
   known green run.
5. Apply the smallest fix that resolves the root cause. Avoid bundling
   unrelated cleanup into the same commit.
6. Push and confirm the targeted check turns green. If a new check
   fails, repeat from step 2 for that check only.

## Guardrails

- Do not disable or skip a failing test to make CI green. Fix it or
  quarantine it with a visible skip marker and a follow-up issue.
- Do not re-run a flaky job without recording the flake. Note the
  failure type so it is actionable later.
- Do not broaden the fix beyond the failing check unless another
  check is also red.
- Do not amend or force-push to a shared branch to hide a failed run.

## Examples

### Good

> Lint check failed on `src/utils/date.ts:42` — the `formatDate` export
> was renamed in a prior commit but callers were not updated. Re-added
> the old name as a re-export alias and pushed.

### Bad

> CI was red so I re-ran the job three times until it passed. No code
> change, no flake documented.

## Verification

- The previously failing check shows green on the new commit.
- No other checks regressed from green to red.
- The fix commit message references the check name and root cause.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/fix-ci
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: fix-ci
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/fix-ci/raw -o .cursor/skills/fix-ci/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/fix-ci.md and install it as a project skill at skills/fix-ci/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
