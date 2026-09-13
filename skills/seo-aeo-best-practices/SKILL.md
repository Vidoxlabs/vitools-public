---
name: seo-aeo-best-practices
description: >-
  SEO and AEO best practices for metadata, Open Graph, sitemaps,
  robots.txt, hreflang, JSON-LD structured data, and content optimized
  for search engines and AI answer surfaces. Use when implementing
  page SEO, technical SEO, schema markup, or AI-overview readiness.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: web
  tags: [web, seo, aeo, structured-data, metadata, sitemaps]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: seo-aeo-best-practices
    summary: SEO and AI-answer-engine optimization best practices
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# SEO and AEO Best Practices

## When to use

Activate when implementing page SEO, technical SEO, schema markup,
international SEO, or improving content for search engines and AI
answer surfaces (Google, ChatGPT, Perplexity).

## Procedure

1. Audit the page's metadata: title tag (under 60 chars), meta
   description (under 155 chars), canonical URL, and Open Graph tags.
2. Verify structured data: JSON-LD with the correct schema type
   (Article, Product, FAQ, HowTo). Test with the Rich Results Test.
3. Check technical SEO: sitemap.xml exists and is submitted, robots.txt
   allows indexing of public pages, hreflang tags for multi-language.
4. Verify heading structure: one H1, hierarchical H2-H6, no skipped
   levels.
5. Check page speed signals: Core Web Vitals (LCP, CLS, INP), image
   optimization, and render-blocking resources.
6. For AEO: ensure content answers questions directly, uses clear
   headings, and includes structured data that AI surfaces can parse.

## Guardrails

- Do not keyword stuff. Write for humans first, search engines second.
- Do not use black-hat techniques: hidden text, cloaking, or paid
  links.
- Do not forget the canonical tag on duplicate content pages.
- Do not skip the mobile check. Google uses mobile-first indexing.

## Examples

### Good

> Audited a product page: title tag is 55 chars and descriptive, meta
> description is 150 chars, JSON-LD Product schema is present and
> valid, sitemap includes the page, Core Web Vitals are green. One
> H1, logical H2 structure.

### Bad

> Page has a 120-char title, no meta description, no structured data,
> 4 H1 tags, no canonical, and a 5-second LCP. Sitemap is missing.

## Verification

- Title tag under 60 characters, meta description under 155.
- JSON-LD structured data validates.
- One H1, hierarchical heading structure.
- Core Web Vitals are green.
- Sitemap includes the page.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/seo-aeo-best-practices
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: seo-aeo-best-practices
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/seo-aeo-best-practices/raw -o .cursor/skills/seo-aeo-best-practices/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/seo-aeo-best-practices.md and install it as a project skill at skills/seo-aeo-best-practices/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
