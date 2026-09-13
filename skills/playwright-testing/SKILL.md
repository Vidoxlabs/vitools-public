---
name: playwright-testing
description: >-
  End-to-end testing with Playwright. Browser automation, page objects, assertions, screenshots, and CI integration. Use when writing or running E2E tests for web applications.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: automation
  tags: [playwright, e2e-testing, browser-automation, ci, page-objects]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: playwright-testing
    summary: End-to-end testing with Playwright
  derived_from:
    - name: playwright
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Playwright Testing

## When to use

Activate when writing end-to-end tests for web applications with Playwright. Use when setting up a test suite or integrating E2E tests into CI.

## Procedure

1. Install Playwright: npm init playwright@latest.
2. Create a test file. Import test and expect from @playwright/test.
3. Write the test: navigate, perform actions with locators, assert on visible state.
4. Create page objects for reusable flows.
5. Capture screenshots on failure with --screenshot=only-on-failure.
6. Configure CI: npx playwright test. Install browsers with npx playwright install --with-deps.
7. Run: npx playwright test, --grep to filter, --project for browser.

## Guardrails

- Do not use page.waitForTimeout. Use auto-waiting locators and expect().
- Do not share state between tests. Each test starts fresh.
- Do not test on production data. Use test database or mock.
- Do not skip the trace viewer. --trace on makes failures debuggable.

## Examples

### Good

> Page object LoginPage encapsulates navigation and interaction. Tests use it, assert on dashboard URL, capture trace. CI runs chromium and firefox.

### Bad

> Test calls page.waitForTimeout(3000) then clicks CSS class. Shares login state with next test. CI runs only chromium.

## Verification

- All tests pass on at least two browsers.
- No waitForTimeout calls in the test code.
- Page objects encapsulate reusable flows.
- CI captures traces on failure.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/playwright-testing
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: playwright-testing
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/playwright-testing/raw -o .cursor/skills/playwright-testing/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/playwright-testing.md and install it as a project skill at skills/playwright-testing/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```