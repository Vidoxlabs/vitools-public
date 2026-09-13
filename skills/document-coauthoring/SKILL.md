---
name: document-coauthoring
description: >-
  Guide users through a structured workflow for co-authoring documentation. Gather context, draft, test with a fresh reader, and iterate. Use when writing docs that need to be clear and complete.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: docs
  tags: [documentation, co-authoring, drafting, review, iteration]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: document-coauthoring
    summary: Structured document co-authoring workflow
  derived_from:
    - name: anthropic-doc-coauthoring
      license: Proprietary
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Document Co-Authoring

## When to use

Activate when co-authoring documentation with a user. Use for technical specs, proposals, decision docs, or any document that needs to be clear and complete.

## Procedure

1. Gather context: the user provides all relevant information while the agent asks clarifying questions.
2. Draft the document: structure first (outline), then fill each section.
3. Test with a fresh reader: read the draft as if seeing it for the first time. Flag blind spots.
4. Iterate: refine based on the reader test. Clarify ambiguities, fill gaps.
5. Finalize: verify the document is complete, accurate, and actionable.
6. Hand off: the user owns the final version.

## Guardrails

- Do not write the document without understanding the audience.
- Do not skip the reader test. A fresh perspective catches blind spots.
- Do not add content the user did not provide or approve.
- Do not over-engineer the structure. Match the document's purpose.

## Examples

### Good

> Gathered context through 3 clarifying questions, drafted a 5-section spec, tested with a fresh read (found 2 gaps), iterated, finalized. User confirmed it was ready for stakeholders.

### Bad

> Wrote a 20-page document from a one-line prompt without asking questions. User could not use it because it assumed the wrong audience.

## Verification

- The audience is identified before drafting.
- A reader test is performed and gaps are addressed.
- The final document is complete and accurate.
- The user owns the final version.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/document-coauthoring
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: document-coauthoring
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/document-coauthoring/raw -o .cursor/skills/document-coauthoring/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/document-coauthoring.md and install it as a project skill at skills/document-coauthoring/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```