---
name: workers-production
description: >-
  Production patterns for edge Workers: error handling, caching,
  routing, security headers, rate limiting, and observability. Use
  when deploying Workers to production or hardening a development
  Worker.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: cloud
  tags: [cloud, workers, production, caching, security, observability]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: workers-production
    summary: Production patterns for edge Workers
  derived_from:
    - name: cloudflare-workers-best-practices
      license: Apache-2.0
      url: https://developers.cloudflare.com/workers/
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Workers Production Patterns

## When to use

Use this skill when deploying edge Workers to production or hardening
a development Worker. Covers error handling, caching, routing,
security, rate limiting, and observability patterns.

## Procedure

1. Implement error handling: wrap the fetch handler in try/catch.
   Return appropriate HTTP status codes (500 for server errors, 502
   for upstream failures).
2. Configure caching: use the Cache API for explicit caching, or
   rely on `cf.cacheEverything` for static assets. Set appropriate
  `Cache-Control` headers.
3. Set security headers: `Content-Security-Policy`,
   `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`,
   `Strict-Transport-Security`.
4. Implement rate limiting: use a Durable Object or KV counter per
   IP or API key. Return 429 when the limit is exceeded.
5. Add routing: use the URL pathname to route to different handlers.
   Support path parameters and query strings.
6. Set up observability: log requests to the platform's analytics,
   include request ID in responses for debugging.
7. Test with `wrangler dev` before deploying with `wrangler deploy`.

## Guardrails

- Do not expose internal error details to clients. Log internally,
  return a generic message externally.
- Do not cache user-specific content without a `Vary: Authorization`
  header.
- Do not skip the `wrangler dev` test before deploying.
- Do not hardcode secrets. Use `wrangler secret put` or the
  platform's secret manager.

## Examples

### Good

> Worker wraps fetch in try/catch, caches static assets with
> `Cache-Control: public, max-age=3600`, sets security headers,
> rate-limits at 100 req/min per IP via a KV counter, logs request
> IDs, and returns 429 with a `Retry-After` header when exceeded.

### Bad

> Worker has no error handling, no caching, no security headers,
> secrets hardcoded in the source, and was deployed without testing
> locally.

## Verification

- Error responses return correct status codes without internal
  details.
- Static assets are cached with appropriate headers.
- Security headers are present on all responses.
- Rate limiting returns 429 with `Retry-After`.
- No secrets in source code.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/workers-production
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: workers-production
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/workers-production/raw -o .cursor/skills/workers-production/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/workers-production.md and install it as a project skill at skills/workers-production/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
