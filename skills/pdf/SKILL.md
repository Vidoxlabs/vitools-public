---
name: pdf
description: >-
  Read, create, and review PDF files where rendering and layout matter.
  Prefer visual checks by rendering pages with Poppler. Use Python
  tools (reportlab, pdfplumber, pypdf) for generation and extraction.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: docs
  tags: [docs, pdf, reportlab, pdfplumber, extraction, generation]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: pdf
    summary: Read, create, and review PDF files with Python tools
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# PDF

## When to use

Activate when tasks involve reading, creating, or reviewing PDF files
where rendering and layout matter. Use for PDF generation, text
extraction, form filling, or visual verification of PDF output.

## Procedure

1. For reading or extraction, use `pdfplumber` for text and tables,
   `pypdf` for metadata and page manipulation.
2. For generation, use `reportlab` for programmatic PDF creation with
   precise layout control.
3. For visual verification, render pages to images with Poppler
   (`pdftoppm` or `pdf2image`) and inspect the output.
4. For form filling, use `pypdf` to fill AcroForm fields.
5. Always verify the output by rendering at least the first and last
   page to confirm layout is correct.

## Guardrails

- Do not assume text extraction is perfect. Verify extracted text
  against the rendered page for critical content.
- Do not generate a PDF without verifying the visual output. Text
  layout in PDFs does not always match what the code produces.
- Do not use `pdfplumber` and `pypdf` interchangeably. They have
  different strengths: `pdfplumber` for text/tables, `pypdf` for
  structure/metadata.
- Do not forget to handle encrypted or password-protected PDFs
  gracefully.

## Examples

### Good

> Generated a 10-page report with `reportlab`, rendered each page
> to PNG with `pdftoppm`, confirmed the table on page 3 is aligned and
> the footer on page 10 is present. Extracted text from a separate
> PDF with `pdfplumber` and verified the first paragraph matches.

### Bad

> Generated a PDF with `reportlab` and shipped it without rendering.
> The table overflowed the page margin and the footer was cut off.

## Verification

- For generated PDFs: at least first and last page rendered and
  visually checked.
- For extraction: extracted text matches a sample from the rendered
  page.
- No pages are blank or missing content.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/pdf
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: pdf
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/pdf/raw -o .cursor/skills/pdf/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/pdf.md and install it as a project skill at skills/pdf/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
