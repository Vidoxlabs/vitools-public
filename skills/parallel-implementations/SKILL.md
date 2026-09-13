---
name: parallel-implementations
description: >-
  Implement a task multiple ways in parallel and pick the best. Spawn subagents in isolated worktrees, evaluate candidates, and apply the winner. Use when multiple approaches are viable and the best is unclear.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: automation
  tags: [parallel, subagents, worktrees, evaluation, best-of-n]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: parallel-implementations
    summary: Run parallel implementations and pick the best
  derived_from:
    - name: cursor-best-of-n
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Parallel Implementations

## When to use

Activate when multiple implementation approaches are viable and the best is unclear. Use when the cost of trying N approaches is less than the cost of choosing wrong.

## Procedure

1. Define the task and the evaluation criteria: correctness, performance, readability, simplicity.
2. Spawn N subagents (default 3) in isolated git worktrees. Each implements independently.
3. Run the test suite on each candidate. Eliminate any that fail tests.
4. Evaluate surviving candidates against the criteria. Score each.
5. Select the winner. Apply it to the main branch.
6. Clean up the losing worktrees.

## Guardrails

- Do not spawn more than 5 subagents. Diminishing returns and resource cost.
- Do not skip the test suite. A candidate that fails tests is disqualified.
- Do not pick the winner subjectively. Use the pre-defined criteria.
- Do not leave losing worktrees after selection. Clean up.

## Examples

### Good

> Spawned 3 subagents for a sorting algorithm task. All passed tests. Candidate B scored highest on performance (1.2x faster) and readability. Applied B. Cleaned up A and C worktrees.

### Bad

> Spawned 5 subagents. Did not run tests. Picked the one that looked shortest. It had a bug that tests would have caught.

## Verification

- All candidates are tested. Failing ones are eliminated.
- Evaluation criteria are defined before implementation.
- The winner is selected by score, not preference.
- Losing worktrees are cleaned up.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/parallel-implementations
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: parallel-implementations
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/parallel-implementations/raw -o .cursor/skills/parallel-implementations/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/parallel-implementations.md and install it as a project skill at skills/parallel-implementations/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```