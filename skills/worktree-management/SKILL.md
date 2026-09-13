---
name: worktree-management
description: >-
  Manage git worktrees for parallel development branches. Create, list, and clean up worktrees without contaminating the main checkout. Use when working on multiple branches simultaneously.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: git
  tags: [git, worktree, branching, parallel-development, workflow]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: worktree-management
    summary: Manage git worktrees for parallel branches
  derived_from:
    - name: ce-worktree
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Worktree Management

## When to use

Activate when working on multiple branches in parallel. Use when switching branches would disrupt in-progress work or when running builds against different branches simultaneously.

## Procedure

1. List existing worktrees: git worktree list.
2. Create a worktree: git worktree add ../project-feature feature-branch.
3. Work in the worktree directory. Build, test, and commit as normal.
4. When done, merge or push the branch from the worktree.
5. Remove the worktree: git worktree remove ../project-feature.
6. Prune stale references: git worktree prune.

## Guardrails

- Do not nest worktrees inside the main checkout. Use sibling directories.
- Do not remove a worktree with uncommitted changes.
- Do not create worktrees on detached HEAD without knowing the commit.
- Do not leave stale worktree directories. Remove and prune after merging.

## Examples

### Good

> Created worktree for hotfix branch, fixed the bug, committed, pushed, merged. Removed worktree and pruned. Main checkout was never disturbed.

### Bad

> Created worktree inside the main checkout. Build tooling picked up nested files. Left the directory after merging.

## Verification

- git worktree list shows only intended active worktrees.
- No worktree directory contains uncommitted changes before removal.
- git worktree prune reports nothing to prune.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/worktree-management
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: worktree-management
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/worktree-management/raw -o .cursor/skills/worktree-management/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/worktree-management.md and install it as a project skill at skills/worktree-management/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```