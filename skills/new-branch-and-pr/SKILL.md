---
name: new-branch-and-pr
description: >-
  Create a fresh branch, complete work, and open a pull request with a
  clean description. Use when starting work that should ship through a
  branch+PR workflow.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: git
  tags: [git, branching, pull-requests, workflow]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: new-branch-and-pr
    summary: Branch, work, and open a clean PR in one workflow
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# New Branch and PR

## When to use

Activate when you are about to start a piece of work that should go
through a branch-and-pull-request workflow. Use when the task involves
code changes that need review before merging into the main branch.

## Procedure

1. Verify you are on the default branch and the working tree is clean.
   Pull latest changes.
2. Create a descriptively named branch from the default branch using a
   consistent prefix convention (e.g. `feat/`, `fix/`, `docs/`).
3. Complete the work. Commit in focused, logical units with messages
   that explain why, not just what.
4. Push the branch to the remote.
5. Open a pull request. Write a description that includes:
   - A one-line summary of the change.
   - A bullet list of what changed and why.
   - Any testing steps the reviewer should follow.
   - Links to related issues or tickets.
6. Request review from the appropriate reviewer or team.

## Guardrails

- Do not branch from a stale default branch. Always pull before
  branching.
- Do not bundle unrelated changes into a single PR. Split into
  separate branches if scope grows.
- Do not push directly to the default branch.
- Do not open a PR without a description or with a generic
  auto-generated body.

## Examples

### Good

> Branch `fix/auth-token-refresh` created from `main`. Two focused
> commits: one fixing the refresh logic, one adding a test. PR
> description explains the token expiry bug, lists the fix, and
> provides reproduction steps.

### Bad

> Branch `misc-changes` with 8 commits spanning auth, logging, and
> README formatting. PR description is "various fixes".

## Verification

- The branch is based on the latest default branch commit.
- Each commit message describes a single logical change.
- The PR description includes a summary, change list, and testing
  steps.
- CI checks are running or have passed on the PR.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/new-branch-and-pr
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: new-branch-and-pr
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/new-branch-and-pr/raw -o .cursor/skills/new-branch-and-pr/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/new-branch-and-pr.md and install it as a project skill at skills/new-branch-and-pr/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
