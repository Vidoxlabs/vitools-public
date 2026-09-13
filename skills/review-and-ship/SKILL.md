---
name: review-and-ship
description: >-
  Review the current branch for bugs, intent fit, and test coverage.
  Run or write tests, commit focused work, open or update a PR. Use
  when ready to ship changes.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: git
  tags: [git, code-review, testing, pull-requests, shipping]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: review-and-ship
    summary: Review, test, commit, and ship a branch through a PR
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Review and Ship

## When to use

Activate when the current branch has uncommitted or unreviewed work
that is intended to ship. Use before opening a PR, after completing
implementation, or when asked to "ship this" or "send this for review."

## Procedure

1. Review the full diff against the base branch. Check for bugs,
   missing error handling, and unintended side effects.
2. Verify the work matches the stated intent of the branch. Flag and
   remove anything that does not belong.
3. Run the existing test suite. If no tests cover the new behavior,
   write at least one test that would fail without the change.
4. If tests fail, fix the code or the tests before proceeding.
5. Stage and commit in focused units with clear messages.
6. Push and open or update the pull request with a description that
   includes what changed, why, and how it was tested.
7. Confirm CI is running. If CI fails, apply the fix-ci procedure.

## Guardrails

- Do not ship without running tests or confirming test coverage for
  new behavior.
- Do not include debug code, commented-out blocks, or TODO markers
  without a linked issue.
- Do not commit secrets, credentials, or environment files.
- Do not force-push over commits that others have reviewed without
  coordination.

## Examples

### Good

> Reviewed diff: found an unhandled promise rejection in the retry
> path. Added a catch handler and a test for it. Committed in two
> units: fix and test. PR description references the bug report and
> lists the test commands run.

### Bad

> Pushed the branch and opened a PR with "done" as the description.
> Tests were not run. A typo in a function name was caught by the
> reviewer.

## Verification

- All tests pass on the branch.
- The PR description lists what, why, and testing steps.
- CI checks are green or actively running.
- No debug artifacts or secrets in the diff.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/review-and-ship
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: review-and-ship
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/review-and-ship/raw -o .cursor/skills/review-and-ship/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/review-and-ship.md and install it as a project skill at skills/review-and-ship/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
