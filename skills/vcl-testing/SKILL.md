---
name: vcl-testing
description: >-
  Test Fastly VCL locally: lint with falco, simulate with falco serve,
  and write unit tests with assertions. Use when developing VCL and
  needing local verification before deploying to Fastly.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: cloud
  tags: [cloud, vcl, fastly, testing, linting, simulation]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: vcl-testing
    summary: Test and lint Fastly VCL locally with falco
  derived_from:
    - name: fastly-falco
      license: MIT
      url: https://github.com/fastly/falco
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# VCL Testing

## When to use

Use this skill when developing Fastly VCL and needing local
verification before deploying. Covers linting, simulation, and unit
testing.

## Procedure

1. Lint the VCL: `falco lint main.vcl`. Fix any errors before
   proceeding.
2. Simulate locally: `falco simulate main.vcl`. The server listens
   on `localhost:3124` by default.
3. Test with `curl http://localhost:3124/` to verify the VCL
   responds correctly.
4. Write unit tests: create test subroutines with `sub vcl_test_*`
   that assert on response headers, status codes, and body content.
5. Run tests: `falco test main.vcl`. All tests must pass before
   deploying.
6. If using XVCL: compile first with `uvx xvcl main.xvcl -o main.vcl`,
   then lint and test the output.

## Guardrails

- Do not deploy without linting and simulating locally first.
- Do not skip unit tests for routing and header logic — these are
  the most error-prone.
- Do not use `req.url.path` in test subroutines — it is read-only in
  falco. Use `set req.url = "/path"` instead.
- Do not assume the simulation matches production exactly. Edge
  cases around POP selection and shielding may differ.

## Examples

### Good

> Wrote 5 test subroutines: one for each routing rule. Linted with
> `falco lint`, simulated with `falco simulate`, tested with `curl`,
> ran `falco test` — all 5 passed. Deployed to staging first.

### Bad

> Wrote VCL, deployed directly to production, and discovered the
> routing rule for `/api/*` was missing a trailing slash match.

## Verification

- `falco lint` passes with no errors.
- `falco simulate` runs and responds to test requests.
- `falco test` passes all test subroutines.
- VCL deploys without errors to the Fastly staging environment.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/vcl-testing
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: vcl-testing
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/vcl-testing/raw -o .cursor/skills/vcl-testing/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/vcl-testing.md and install it as a project skill at skills/vcl-testing/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
