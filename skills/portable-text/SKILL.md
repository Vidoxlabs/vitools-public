---
name: portable-text
description: >-
  Convert and render Portable Text: HTML to Portable Text, Markdown to Portable Text, and Portable Text to React, Vue, Astro, or plain text. Use when working with Sanity Portable Text format.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: design
  tags: [portable-text, sanity, conversion, rendering, serialization]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: portable-text
    summary: Portable Text conversion and rendering
  derived_from:
    - name: sanity-portable-text-conversion-serialization
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Portable Text

## When to use

Activate when converting between Portable Text and other formats, or rendering Portable Text to a frontend framework.

## Procedure

1. For HTML to Portable Text: use @portabletext/block-tools htmlToBlocks with the correct block schema.
2. For Markdown to Portable Text: use @portabletext/markdown markdownToPortableText.
3. For Portable Text to React: use @portabletext/react with component overrides for custom block types.
4. For Portable Text to plain text: strip formatting and concatenate text blocks.
5. Handle custom block types: define serializers for each custom type in your content model.
6. Preserve metadata: image alt text, link attributes, and annotation data.
7. Test: verify the conversion preserves all content and formatting.

## Guardrails

- Do not lose formatting during conversion. Test with rich content.
- Do not skip custom block serializers. Unknown blocks will not render.
- Do not hardcode block type names. Use the content model's definitions.
- Do not forget to handle inline annotations (links, marks).

## Examples

### Good

> Converted an HTML article to Portable Text: headings, paragraphs, lists, images, and links all preserved. Rendered to React with custom block components for callouts and code blocks.

### Bad

> Converted HTML to Portable Text but lost all image alt text and link attributes. Custom blocks silently dropped. No testing performed.

## Verification

- All content and formatting is preserved in the conversion.
- Custom block types have serializers defined.
- Inline annotations are handled.
- The conversion is tested with rich content.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/portable-text
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: portable-text
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/portable-text/raw -o .cursor/skills/portable-text/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/portable-text.md and install it as a project skill at skills/portable-text/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```