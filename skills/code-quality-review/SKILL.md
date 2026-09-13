---
name: code-quality-review
description: >-
  Run an extremely strict maintainability review for abstraction quality, giant files, and spaghetti-code growth. Use for deep code quality audits or harsh maintainability reviews.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: eval
  tags: [code-review, quality, maintainability, abstraction, audit]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: code-quality-review
    summary: Strict maintainability and code quality review
  derived_from:
    - name: compound-engineering-code-review-thermo-nuclear
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Code Quality Review

## When to use

Activate when a deep, strict code quality review is needed. Use for audits, pre-merge reviews, or when maintainability concerns have been raised.

## Procedure

1. Read the full diff or module. Identify every function, class, and file.
2. Check abstraction quality: are there unnecessary layers, single-use interfaces, or premature generalizations?
3. Check file sizes: any file over 300 lines should be scrutinized. Over 500 is a finding.
4. Check coupling: are modules tightly coupled? Can they be tested independently?
5. Check naming: do names describe behavior or implementation?
6. Check for code judo: restructurings that preserve behavior while making the code dramatically simpler.
7. Report findings with file paths, line numbers, and specific recommendations.

## Guardrails

- Do not report stylistic preferences as quality issues. Focus on maintainability.
- Do not suggest changes without explaining the benefit.
- Do not skip the code judo check. Look for simplification opportunities.
- Do not review only the diff. Read surrounding context.

## Examples

### Good

> Reviewed a 450-line module: found 2 single-use abstractions, 1 file over 500 lines, 3 naming issues, and 1 code judo opportunity (merge two functions into one, removing 40 lines). Report includes file paths and recommendations.

### Bad

> Reviewed the diff and said the code looks good. No specific findings, no file references, no recommendations.

## Verification

- Every finding has a file path and line number.
- Findings focus on maintainability, not style.
- Code judo opportunities are identified.
- Recommendations are specific and actionable.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/code-quality-review
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: code-quality-review
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/code-quality-review/raw -o .cursor/skills/code-quality-review/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/code-quality-review.md and install it as a project skill at skills/code-quality-review/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```