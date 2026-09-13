---
name: image-generation-guidance
description: >-
  Guide image generation and editing: when to use AI-generated images, prompt crafting, reference-first handling, factual grounding, and asset consistency. Use when generating or editing images with AI.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: design
  tags: [image-generation, ai, prompting, reference, consistency]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: image-generation-guidance
    summary: Guidance for AI image generation and editing
  derived_from:
    - name: grok-imagine
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Image Generation Guidance

## When to use

Activate when generating or editing images with AI tools. Use when deciding whether to generate vs build with code, crafting prompts, or ensuring visual consistency.

## Procedure

1. Decide: is an AI-generated bitmap the right output, or should the visual be built with code (SVG, HTML, canvas)?
2. If generating: craft a prompt that describes the subject, style, composition, lighting, and mood.
3. For reference-based generation: provide the reference image and describe what to change while keeping what works.
4. Ensure factual grounding: do not generate images of real people without consent. Do not fabricate screenshots.
5. Maintain asset consistency: use the same style, palette, and composition across a set.
6. Review the output: does it meet the request? Is it appropriate? Is it consistent?
7. Iterate if needed, keeping the same constraints.

## Guardrails

- Do not generate images of real people without explicit consent.
- Do not fabricate screenshots or UI that could be mistaken for real products.
- Do not use copyrighted styles or logos.
- Do not skip the consistency check when generating a set.

## Examples

### Good

> Generated a set of 5 icons with the same style, palette, and grid. Prompt specified subject, style, and composition. Output is consistent and appropriate.

### Bad

> Generated 5 icons with different styles and palettes. No consistency. One icon used a copyrighted logo style.

## Verification

- AI generation is the right choice (vs code-built visuals).
- Prompt specifies subject, style, and composition.
- Generated set is consistent in style and palette.
- No real people, copyrighted styles, or fabricated screenshots.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/image-generation-guidance
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: image-generation-guidance
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/image-generation-guidance/raw -o .cursor/skills/image-generation-guidance/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/image-generation-guidance.md and install it as a project skill at skills/image-generation-guidance/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```