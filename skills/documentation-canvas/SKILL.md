---
name: documentation-canvas
description: >-
  Render documentation as a visual canvas: architecture notes, API references, and onboarding guides in a single interactive view. Use when creating visual documentation for complex systems.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: docs
  tags: [documentation, canvas, visual, architecture, interactive]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: documentation-canvas
    summary: Visual documentation canvas for complex systems
  derived_from:
    - name: cursor-docs-canvas
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Documentation Canvas

## When to use

Activate when creating visual, interactive documentation for a complex system. Use when a single README is insufficient and stakeholders need a navigable canvas.

## Procedure

1. Identify the documentation sections: overview, architecture, API reference, onboarding, troubleshooting.
2. Design the canvas layout: sections as panels, connected by visual relationships.
3. Render each section as a markdown panel with embedded diagrams (Mermaid).
4. Add navigation: table of contents, section links, and search.
5. Include interactive elements: expandable sections, code examples with syntax highlighting.
6. Export as a single HTML file or deploy to a documentation host.
7. Verify all links resolve and diagrams render.

## Guardrails

- Do not make the canvas a wall of text. Use visual hierarchy and diagrams.
- Do not skip the search. Large canvases need it.
- Do not embed sensitive information in the canvas.
- Do not forget mobile. Test at 768px width.

## Examples

### Good

> Built a canvas with 6 panels: overview, architecture diagram (Mermaid), API reference (expandable), onboarding guide, troubleshooting, and search. Single HTML file, 120 KB, mobile-responsive.

### Bad

> Created a 50-page README with no visual structure, no navigation, no search. Nobody reads past page 5.

## Verification

- Canvas has visual hierarchy with panels and diagrams.
- Navigation and search work.
- All links resolve and diagrams render.
- Mobile layout is tested.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/documentation-canvas
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: documentation-canvas
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/documentation-canvas/raw -o .cursor/skills/documentation-canvas/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/documentation-canvas.md and install it as a project skill at skills/documentation-canvas/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```