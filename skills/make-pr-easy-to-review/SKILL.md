---
name: make-pr-easy-to-review
description: >-
  Prepare PRs for review by cleaning noisy history, improving
  descriptions, and adding reviewer guidance without changing
  behavior. Use when a PR needs to be made reviewable.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: git
  tags: [git, pull-requests, code-review, history, cleanup]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: make-pr-easy-to-review
    summary: Clean history and description so reviewers can focus on substance
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Make PR Easy to Review

## When to use

Activate when a pull request is open but hard to review — noisy commit
history, vague description, large diff with mixed concerns, or no
reviewer guidance. Use before requesting review or when a reviewer
flags a PR as difficult to follow.

## Procedure

1. Read the PR diff end to end. Note unrelated changes, debug
   artifacts, formatting noise, and leftover comments.
2. If commit history is noisy, rebase to produce clean, logical
   commits. Each commit should build and pass tests independently.
3. Rewrite the PR description with:
   - A clear summary line.
   - A numbered breakdown of changes grouped by concern.
   - The risk surface: what could break and how it was tested.
   - Reviewer guidance: which files to focus on and in what order.
4. Remove any changes that do not belong in this PR. Move them to a
   separate branch or stash.
5. Push the cleaned history and update the PR.
6. Add inline PR comments on complex or non-obvious sections.

## Guardrails

- Do not change behavior while cleaning history. The final tree must
  be byte-identical to the pre-clean state.
- Do not squash everything into one commit unless the PR is trivially
  small.
- Do not rewrite history on a branch that other contributors have
  already pulled without coordination.
- Do not remove reviewer comments or dismiss review feedback during
  cleanup.

## Examples

### Good

> PR had 12 commits including typo fixes, debug logging, and the real
> change. Rebased into 3 clean commits: add utility, update caller,
> add test. Description lists files in review order with risk notes.

### Bad

> Squashed 12 commits into 1 called "misc" and left the description
> blank because "the code speaks for itself."

## Verification

- `git diff main...HEAD` is unchanged before and after history cleanup.
- The PR description includes a summary, change breakdown, risk
  surface, and reviewer guidance.
- Every commit in the cleaned history builds and passes tests.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/make-pr-easy-to-review
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: make-pr-easy-to-review
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/make-pr-easy-to-review/raw -o .cursor/skills/make-pr-easy-to-review/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/make-pr-easy-to-review.md and install it as a project skill at skills/make-pr-easy-to-review/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
