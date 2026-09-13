---
name: figma-plugin-api
description: >-
  Use the Figma Plugin API to execute JavaScript in Figma files. Create, edit, and inspect design nodes programmatically. Use when building Figma plugins or automating design file operations.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: design
  tags: [figma, plugin-api, automation, design-nodes, javascript]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: figma-plugin-api
    summary: Programmatic Figma file manipulation via Plugin API
  derived_from:
    - name: figma-use
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Figma Plugin API

## When to use

Activate when building a Figma plugin or automating operations on Figma files programmatically.

## Procedure

1. Set up the plugin with manifest.json (name, id, main, capabilities).
2. Access the document: figma.currentPage or figma.root.
3. Traverse the node tree with node.children and node.type.
4. Create nodes: figma.createFrame(), createText(), createRectangle().
5. Read and modify text: textNode.characters, loadFontAsync() first.
6. Inspect properties: fills, strokes, effects, cornerRadius.
7. Communicate with UI: figma.ui.postMessage() and figma.ui.onmessage.

## Guardrails

- Do not modify nodes without checking node.type. Operations are type-specific.
- Do not set text characters without loading the font first.
- Do not block the main thread. Use async for I/O.
- Do not assume node IDs are stable across documents.

## Examples

### Good

> Plugin reads all TEXT nodes, loads fonts async, replaces placeholder text with data source values, reports count to UI. Checks node.type before modifying.

### Bad

> Plugin calls node.characters on every node including frames and rectangles. Throws on first non-text node. No font loading.

## Verification

- Plugin runs without throwing on a test file with mixed node types.
- Text modifications only affect TEXT nodes.
- Async operations do not block the main thread.
- UI receives completion or error messages.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/figma-plugin-api
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: figma-plugin-api
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/figma-plugin-api/raw -o .cursor/skills/figma-plugin-api/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/figma-plugin-api.md and install it as a project skill at skills/figma-plugin-api/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```