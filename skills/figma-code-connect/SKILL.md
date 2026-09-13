---
name: figma-code-connect
description: >-
  Connect Figma components to code components. Map design properties to code props for a single source of truth. Use when syncing design systems with frontend component libraries.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: design
  tags: [figma, code-connect, design-system, components, sync]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: figma-code-connect
    summary: Connect Figma components to code components
  derived_from:
    - name: figma-code-connect
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Figma Code Connect

## When to use

Activate when connecting a Figma component to its code implementation. Use when design properties need to map to code props.

## Procedure

1. Identify the Figma component: note its key from the API or URL.
2. Identify the code component that implements the same contract.
3. Write the Code Connect config file with component key and import path.
4. Map Figma variants and properties to code props with matching names.
5. Map instance properties (boolean, text, instance swap) explicitly.
6. Validate: open in Figma Dev Mode. Code preview must reflect selected variant.
7. Publish the Code Connect file.

## Guardrails

- Do not map properties that do not exist in both Figma and code.
- Do not use different names for the same concept.
- Do not skip variant mappings. Unmapped variants produce incorrect code.
- Do not publish without validating in Dev Mode.

## Examples

### Good

> Button component mapped: Figma size maps to code size, Figma state maps to disabled boolean. Dev Mode shows correct code. Generated code compiles.

### Bad

> Mapped a color property to a theme prop with different value names. Dev Mode shows broken code. Half the variants unmapped.

## Verification

- Every Figma variant has a corresponding code prop mapping.
- Figma Dev Mode shows correct, compilable code for each variant.
- Property names match between Figma and code.
- Generated code compiles without modification.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/figma-code-connect
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: figma-code-connect
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/figma-code-connect/raw -o .cursor/skills/figma-code-connect/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/figma-code-connect.md and install it as a project skill at skills/figma-code-connect/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```