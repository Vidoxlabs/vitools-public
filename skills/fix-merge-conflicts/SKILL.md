---
name: fix-merge-conflicts
description: >-
  Resolve merge conflicts non-interactively by reading both sides,
  understanding the intent, and producing a correct merged result.
  Validate build and tests after resolution. Use when git reports
  merge conflicts.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: git
  tags: [git, merge, conflicts, resolution, branching]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: fix-merge-conflicts
    summary: Resolve merge conflicts non-interactively with validated results
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Fix Merge Conflicts

## When to use

Activate when git reports merge conflicts during a merge, rebase, or
cherry-pick. Use when conflict markers are present in the working tree
and the user needs them resolved without interactive tooling.

## Procedure

1. Run `git status` to identify all files with conflicts.
2. For each conflicted file, read the full diff including both sides
   of the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
3. Understand the intent of each side. Determine whether the changes
   are additive (both should be kept), mutually exclusive (one should
   be chosen), or overlapping (a merged version is needed).
4. Edit the file to produce the correct result. Remove all conflict
   markers.
5. Stage the resolved file: `git add <file>`.
6. After all conflicts are resolved, run the build and test suite to
   validate the merge result.
7. If the merge was a rebase, continue with `git rebase --continue`.
   If a merge, complete it with `git commit` (or let the merge commit
   proceed).

## Guardrails

- Do not pick one side blindly. Read and understand both sides before
  resolving.
- Do not leave conflict markers in the file. All must be removed.
- Do not skip the build and test validation after resolution.
- Do not use `git checkout --theirs` or `--ours` without understanding
  what is being discarded.

## Examples

### Good

> Two branches both modified `src/config.ts`. Side A added a new
> config key. Side B renamed an existing key. Resolution: kept both
> changes — the new key from A and the renamed key from B. Build
> passed.

### Bad

> Ran `git checkout --theirs .` on all conflicted files without reading
> any of them. The build failed because a needed change from the other
> branch was lost.

## Verification

- `git diff --check` shows no conflict markers.
- Build passes.
- Test suite passes.
- `git status` shows all conflicts resolved.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/fix-merge-conflicts
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: fix-merge-conflicts
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/fix-merge-conflicts/raw -o .cursor/skills/fix-merge-conflicts/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/fix-merge-conflicts.md and install it as a project skill at skills/fix-merge-conflicts/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
