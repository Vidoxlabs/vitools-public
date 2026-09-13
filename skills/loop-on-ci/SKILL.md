---
name: loop-on-ci
description: >-
  Monitor PR checks and iteratively fix failures until all required
  checks are green. Use when CI is failing and needs a hands-off
  fixing loop.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: automation
  tags: [ci, automation, pull-requests, iteration, debugging]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: loop-on-ci
    summary: Iteratively fix CI failures until all required checks pass
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Loop on CI

## When to use

Activate when a pull request has one or more failing required checks
and you want an automated fixing loop: inspect, fix, push, wait, and
repeat until all required checks are green.

## Procedure

1. List all checks on the PR. Identify which are required and which
   are currently failing or pending.
2. For the first failing required check, apply the fix-ci procedure:
   read logs, classify the failure, apply the smallest fix.
3. Commit and push the fix with a message naming the check resolved.
4. Wait for CI to report on the new commit. Poll the check status
   until it completes.
5. If the check is green, move to the next failing required check and
   repeat from step 2. If it failed again, re-read logs and apply a
   new fix.
6. When all required checks are green, stop. Report a summary of what
   was fixed and how many iterations were needed.
7. If the loop exceeds 5 iterations on a single check without
   progress, stop and surface the situation for human review.

## Guardrails

- Do not bypass required checks by marking them optional or removing
  them from branch protection.
- Do not push more than one fix at a time between CI runs. Each
  iteration should target a single check.
- Do not continue looping if a check is failing for environmental
  reasons outside the repository. Surface it.
- Do not suppress, skip, or delete failing tests during the loop.
- Cap iterations at 5 per check; escalate if no progress is made.

## Examples

### Good

> Iteration 1: fixed import error in `src/api.ts`. Pushed. Check
> passed. Iteration 2: fixed type error in `src/types.ts`. Pushed.
> Check passed. All required checks green after 2 iterations.

### Bad

> Kept pushing speculative fixes and re-running CI hoping for green
> without reading logs between attempts.

## Verification

- All required checks on the latest commit show green.
- A summary lists each fix, the check it resolved, and the iteration
  count.
- No required checks were skipped, disabled, or removed during the
  loop.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/loop-on-ci
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: loop-on-ci
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/loop-on-ci/raw -o .cursor/skills/loop-on-ci/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/loop-on-ci.md and install it as a project skill at skills/loop-on-ci/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
