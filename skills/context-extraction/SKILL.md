---
name: context-extraction
description: >-
  Generate or improve a company-specific data analysis skill by extracting tribal knowledge from analysts. Capture domain context, SQL patterns, and data conventions. Use when building custom analysis skills.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: data
  tags: [context, extraction, tribal-knowledge, analysis, domain]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: context-extraction
    summary: Extract domain knowledge for custom analysis skills
  derived_from:
    - name: anthropic-data-context-extractor
      license: Proprietary
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Context Extraction

## When to use

Activate when extracting tribal knowledge from domain experts to build a custom data analysis skill. Use when onboarding new analysts or codifying domain expertise.

## Procedure

1. Interview the domain expert: what data sources they use, what questions they answer, what patterns they look for.
2. Document the data sources: tables, schemas, joins, and known quirks.
3. Capture SQL patterns: common queries, filters, aggregations, and dialect-specific syntax.
4. Record conventions: naming, date handling, timezone, and business logic.
5. Structure the extracted knowledge as a skill file with the domain context embedded.
6. Test the skill: can a new analyst follow it to answer a standard question?
7. Iterate based on the test results.

## Guardrails

- Do not skip the interview. Tribal knowledge is not in documentation.
- Do not record the expert's personal preferences as universal rules.
- Do not embed credentials or connection strings in the skill.
- Do not skip the test step. An untested skill is a guess.

## Examples

### Good

> Interviewed 2 analysts, documented 3 data sources and 5 common SQL patterns, captured timezone and naming conventions, built a skill file. A new analyst used it to answer a standard question without help.

### Bad

> Read the analyst's wiki page and built a skill from it. The wiki was 2 years out of date. The skill told new analysts to query a table that no longer exists.

## Verification

- Domain expert is interviewed, not just documentation read.
- Data sources and SQL patterns are documented.
- The skill is tested with a new analyst.
- No credentials are embedded in the skill.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/context-extraction
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: context-extraction
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/context-extraction/raw -o .cursor/skills/context-extraction/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/context-extraction.md and install it as a project skill at skills/context-extraction/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```