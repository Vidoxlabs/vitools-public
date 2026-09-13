---
name: content-modeling
description: >-
  Design structured content models for headless CMSs: schema design, content architecture, content reuse, references vs embedding, and taxonomies. Use when designing or refactoring content types.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: design
  tags: [content, modeling, cms, schema, architecture, taxonomy]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: content-modeling
    summary: Structured content model design for headless CMS
  derived_from:
    - name: sanity-content-modeling-best-practices
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Content Modeling

## When to use

Activate when designing or refactoring a content model for a headless CMS. Use when creating content types, defining fields, or planning content architecture.

## Procedure

1. Identify the content types: what distinct entities does the system manage?
2. Define fields for each type: name, type (string, number, date, reference, array, rich text), and validation.
3. Decide references vs embedding: use references for shared or reusable content, embedding for one-to-one.
4. Design the taxonomy: categories, tags, and classification systems.
5. Plan content reuse: which fields and types are shared across types?
6. Document the model with a schema diagram and field descriptions.
7. Validate: can the model express all required content without duplication?

## Guardrails

- Do not over-normalize. Some denormalization is fine for readability.
- Do not use arrays for unbounded references. Use a separate type.
- Do not skip validation rules. Each field should have constraints.
- Do not forget the editorial workflow. Content models must be editable by non-developers.

## Examples

### Good

> Designed a content model with 5 types (Article, Author, Category, Tag, Page), references between Article and Author, embedded summary in Article, taxonomy with Categories and Tags. Schema diagram and field docs included.

### Bad

> Created a single content type with 40 fields including everything. No references, no reuse, no taxonomy. Editors cannot find anything.

## Verification

- Content types are distinct and non-overlapping.
- References vs embedding decisions are documented.
- Taxonomy is defined.
- The model is validated against content requirements.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/content-modeling
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: content-modeling
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/content-modeling/raw -o .cursor/skills/content-modeling/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/content-modeling.md and install it as a project skill at skills/content-modeling/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```