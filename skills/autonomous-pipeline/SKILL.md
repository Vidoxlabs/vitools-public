---
name: autonomous-pipeline
description: >-
  Run the full autonomous engineering pipeline end-to-end: plan, work, code review, test, commit, push, open PR, watch CI, fix CI until green. Use only when the user explicitly requests hands-off execution.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: automation
  tags: [autonomous, pipeline, plan, work, review, ci]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: autonomous-pipeline
    summary: Full autonomous engineering pipeline
  derived_from:
    - name: compound-engineering-lfg
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Autonomous Pipeline

## When to use

Activate only when the user explicitly requests hands-off execution of a software task and provides a feature description. Do not auto-route casual conversation here.

## Procedure

1. Invoke the technical-planning skill to create a plan.
2. Invoke the structured-debugging or work skill to implement.
3. Invoke the code-quality-review skill for review.
4. Run or write tests. Fix any failures.
5. Commit with structured-commits format.
6. Push and open a PR.
7. Watch CI. If failing, invoke the loop-on-ci skill.
8. Report when all CI checks are green.

## Guardrails

- Do not activate for casual conversation. This is an explicit-request pipeline.
- Do not skip any stage. Each stage's output feeds the next.
- Do not push without tests passing.
- Do not skip CI. Watch it to green or report failure.

## Examples

### Good

> Pipeline: planned (3 phases), implemented, reviewed (2 findings fixed), tested (all pass), committed (2 focused commits), pushed, PR opened, CI green after 1 fix iteration. Reported success.

### Bad

> Started coding immediately without a plan, did not run tests, pushed to main, CI is red, nobody knows because nobody is watching.

## Verification

- All pipeline stages completed in order.
- Tests pass before push.
- PR is opened with a description.
- CI is green or failure is reported.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/autonomous-pipeline
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: autonomous-pipeline
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/autonomous-pipeline/raw -o .cursor/skills/autonomous-pipeline/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/autonomous-pipeline.md and install it as a project skill at skills/autonomous-pipeline/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```