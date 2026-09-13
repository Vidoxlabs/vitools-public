---
name: clean-stale-branches
description: >-
  Remove local branches whose remote tracking branch has been deleted. Handle associated worktrees before deletion. Use when the local branch list has grown with merged or abandoned branches.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: git
  tags: [git, branches, cleanup, worktree, maintenance]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: clean-stale-branches
    summary: Remove local branches with no remote tracking branch
  derived_from:
    - name: ce-clean-gone-branches
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Clean Stale Branches

## When to use

Activate when the local branch list has accumulated branches that were merged or abandoned on the remote.

## Procedure

1. Fetch current remote state: git fetch --all --prune.
2. List branches with gone remotes: git branch -vv | grep ': gone]'.
3. For each stale branch, check for associated worktrees.
4. Check for uncommitted work: git log main..<branch> --oneline.
5. Delete the branch: git branch -D <branch>.
6. Prune worktree references: git worktree prune.

## Guardrails

- Do not delete a branch with unmerged commits without confirming they are abandoned.
- Do not delete the branch you are currently on. Switch to main first.
- Do not remove a worktree with uncommitted changes.
- Do not run git fetch --prune on repos with local-only branches that must be preserved.

## Examples

### Good

> Fetched with prune, found three gone branches, confirmed each was merged, deleted all three, pruned worktrees. Branch list is clean.

### Bad

> Deleted a branch with 15 local-only commits because its remote was gone. The commits contained experimental work never merged.

## Verification

- git branch -vv shows no branches with gone status.
- git worktree list shows no stale worktree directories.
- All remaining branches have a valid upstream or a known reason to be local-only.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/clean-stale-branches
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: clean-stale-branches
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/clean-stale-branches/raw -o .cursor/skills/clean-stale-branches/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/clean-stale-branches.md and install it as a project skill at skills/clean-stale-branches/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```