---
name: technical-planning
description: >-
  Create structured technical plans for multi-step engineering tasks. Define
  what to build, break down into phases, estimate effort, and identify
  dependencies. Use when planning features, migrations, or refactors.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: automation
  tags: [planning, architecture, phases, dependencies, estimation]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: technical-planning
    summary: Structured technical plans for multi-step tasks
  derived_from:
    - name: ce-plan
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Technical Planning

## When to use

Activate before starting any multi-step engineering task: new features,
migrations, refactors, or infrastructure changes. Use when the work
spans multiple files, sessions, or team members and needs a written
plan to avoid drift.

## Procedure

1. Define the objective in one sentence. State what success looks like
   and what is explicitly out of scope.
2. Inventory the current state. List relevant files, services, data
   models, and external dependencies.
3. Break the work into phases. Each phase should be independently
   verifiable and deployable.
4. For each phase, list the concrete tasks, estimated effort (S/M/L),
   and dependencies on prior phases.
5. Identify risks: what could block a phase, what is the fallback.
6. Write the plan to a markdown file in the repo or project docs.
7. Review the plan against the objective. Cut anything that does not
   serve the stated goal.

## Guardrails

- Do not skip the scope-out section. Vague plans produce scope creep.
- Do not estimate without reading the relevant code. Guesses waste time.
- Do not plan more than three phases of detail ahead. Later phases
  will change once earlier ones land.
- Do not proceed to implementation without a written plan file.

## Examples

### Good

> Plan has a one-line objective, three phases with concrete tasks,
> each phase lists dependencies and a verification step. Effort
> estimates are S/M/L. Risks section names two blockers and their
> fallbacks.

### Bad

> "We will improve the auth system" with no phases, no file
> references, no dependencies, and no verification steps. Team
> members disagree on what "improve" means.

## Verification

- The plan file exists and is readable by a new team member.
- Each phase has at least one concrete verification step.
- Dependencies form a DAG with no cycles.
- Estimated effort sums to a realistic timeline.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/technical-planning
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: technical-planning
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/technical-planning/raw -o .cursor/skills/technical-planning/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/technical-planning.md and install it as a project skill at skills/technical-planning/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```