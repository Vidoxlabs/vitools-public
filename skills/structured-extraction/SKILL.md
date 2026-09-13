---
name: structured-extraction
description: >-
  Extract structured data from unstructured text: emails, documents,
  PDFs, or web pages. Convert to tables, JSON, or typed records. Use
  when parsing documents, pulling key fields, or converting free text
  to structured format.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: data
  tags: [data, extraction, parsing, json, structured, unstructured]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: structured-extraction
    summary: Extract structured data from unstructured text
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Structured Extraction

## When to use

Activate when the user needs to extract key information from
unstructured text and convert it to a structured format. Use for
parsing emails, documents, PDFs, web pages, or any free text into
tables, JSON, or typed records.

## Procedure

1. Identify the target schema: what fields are needed and what types
   are expected (string, number, date, boolean, array).
2. Read the source text and identify where each field's value appears.
3. Extract each field. Handle missing values explicitly — do not
   fabricate data.
4. Normalize values: trim whitespace, parse dates to ISO 8601,
   standardize phone numbers, and convert units.
5. Validate the extracted record against the schema. Flag any type
   mismatches or missing required fields.
6. Output in the requested format: JSON, CSV, or a typed record.
7. If processing multiple documents, produce a consistent array of
   records with the same schema.

## Guardrails

- Do not fabricate values for missing fields. Use `null` or an
  explicit "not found" marker.
- Do not assume a field's location is consistent across documents.
  Verify for each.
- Do not skip validation. Type mismatches and missing required fields
  must be flagged.
- Do not alter the source text meaning during extraction. Quote
  verbatim when the value is ambiguous.

## Examples

### Good

> Extracted 5 fields from an email: sender, date, subject, action
> items (array), and deadline. Dates normalized to ISO 8601. Missing
> deadline field set to null with a "not found" flag. Output as
> JSON with schema validation passing.

### Bad

> "Extracted the important parts of the email." No schema, no
> validation, missing fields silently omitted, dates left in
> inconsistent formats.

## Verification

- Every field in the schema is present in the output (or explicitly
  null).
- Types match the schema (dates are ISO 8601, numbers are numbers).
- No values were fabricated for missing fields.
- Output format matches the request (JSON, CSV, or typed record).

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/structured-extraction
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: structured-extraction
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/structured-extraction/raw -o .cursor/skills/structured-extraction/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/structured-extraction.md and install it as a project skill at skills/structured-extraction/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
