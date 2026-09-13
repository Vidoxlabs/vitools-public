---
name: web-performance
description: >-
  Analyze web performance using Chrome DevTools. Core Web Vitals, render-blocking resources, network optimization, and accessibility gaps. Use when auditing or improving page load and runtime performance.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: web
  tags: [web-performance, core-web-vitals, devtools, lighthouse, a11y]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: web-performance
    summary: Web performance analysis with Chrome DevTools
  derived_from:
    - name: web-perf
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Web Performance

## When to use

Activate when auditing a web page for load performance, runtime performance, or accessibility. Use when Core Web Vitals are below target.

## Procedure

1. Run a Lighthouse audit. Record Core Web Vitals: LCP, CLS, INP.
2. Analyze render-blocking resources in the Network tab.
3. Check Performance tab for long tasks, layout thrashing, forced reflows.
4. Optimize images: WebP/AVIF, loading=lazy, width/height.
5. Reduce JS payload: code-split, tree-shake, audit bundle.
6. Address accessibility: contrast, alt text, keyboard nav, ARIA.
7. Re-run Lighthouse. Compare scores.

## Guardrails

- Do not optimize without a baseline measurement.
- Do not defer critical-path resources. Defer only non-critical.
- Do not ignore INP. It replaced FID as a Core Web Vital.
- Do not fix performance without checking accessibility.

## Examples

### Good

> Baseline: LCP 4.2s, CLS 0.3, INP 300ms. After deferring scripts and lazy-loading: LCP 1.8s, CLS 0.02, INP 120ms. Accessibility 70 to 95.

### Bad

> Inlined all CSS to eliminate render-blocking, but 200 KB CSS blocks initial render. LCP got worse. No accessibility audit.

## Verification

- Lighthouse Performance score improved from baseline.
- Core Web Vitals meet thresholds: LCP < 2.5s, CLS < 0.1, INP < 200ms.
- No render-blocking resources in the critical path.
- Lighthouse Accessibility score is 90 or above.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/web-performance
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: web-performance
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/web-performance/raw -o .cursor/skills/web-performance/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/web-performance.md and install it as a project skill at skills/web-performance/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```