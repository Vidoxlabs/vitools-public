---
name: project-planning-visual
description: >-
  Generate a visual project plan board from a PRD or feature description. Interactive flow: research, propose sections, deep research per section, create the board. Use when visualizing project plans.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: design
  tags: [project-planning, visual, board, figjam, prd]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: project-planning-visual
    summary: Visual project plan from a PRD
  derived_from:
    - name: figma-generate-project-plan
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Visual Project Planning

## When to use

Activate when creating a visual project plan from a PRD, feature description, or requirements doc. Use when stakeholders need a visual board to understand scope.

## Procedure

1. Read the PRD or feature description. Extract the key deliverables and milestones.
2. Propose sections for the board: each section represents a workstream or phase.
3. For each section, do a brief deep research: what does this workstream involve, what are the dependencies.
4. Present the proposed sections to the user for confirmation.
5. Generate the visual board: sections as columns or panels, with cards for each deliverable.
6. Add timeline estimates and dependency arrows.
7. Export or share the board.

## Guardrails

- Do not generate the board without user confirmation of the sections.
- Do not include more than 8 sections. The board becomes unreadable.
- Do not skip dependencies. They are the most valuable part of the visual.
- Do not forget timeline estimates. They drive prioritization.

## Examples

### Good

> Read a 5-page PRD, proposed 6 sections (research, design, backend, frontend, testing, launch), confirmed with user, generated a visual board with cards and dependency arrows. Shared as an image.

### Bad

> Generated a board with 15 sections from a one-line feature description. No user confirmation. No dependencies. No timeline.

## Verification

- Sections are confirmed by the user before board generation.
- Board has 8 or fewer sections.
- Dependencies are shown.
- Timeline estimates are included.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/project-planning-visual
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: project-planning-visual
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/project-planning-visual/raw -o .cursor/skills/project-planning-visual/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/project-planning-visual.md and install it as a project skill at skills/project-planning-visual/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```