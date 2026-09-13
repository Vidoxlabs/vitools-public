---
name: browser-testing
description: >-
  Browser-based testing with Playwright. Page interactions, assertions, screenshots, and cross-browser coverage. Use when writing or running end-to-end tests against a live web application.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: automation
  tags: [testing, playwright, browser, e2e, screenshots]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: browser-testing
    summary: Browser-based end-to-end testing with Playwright
  derived_from:
    - name: ce-test-browser
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Browser Testing

## When to use

Activate when writing or running end-to-end tests that exercise a web application through a real browser.

## Procedure

1. Install Playwright: npm init playwright@latest.
2. Write a test that navigates, performs actions, and asserts outcomes.
3. Use resilient locators: getByRole, getByLabel, getByText.
4. Add assertions with expect() from @playwright/test.
5. Capture screenshots on failure with --trace on.
6. Run across browsers: npx playwright test --project=chromium --project=firefox.
7. Add to CI: npx playwright test --reporter=github.

## Guardrails

- Do not use arbitrary timeouts (page.waitForTimeout). Use auto-waiting locators.
- Do not test third-party services. Mock external calls.
- Do not skip browsers in CI to save time.
- Do not rely on test order. Each test must be independent.

## Examples

### Good

> Test uses getByRole, asserts with expect(), captures trace on failure, runs across chromium and firefox in CI.

### Bad

> Test uses page.waitForTimeout(2000) then clicks a CSS class. Fails when class name changes. Skips webkit.

## Verification

- Tests pass on all configured browsers.
- No waitForTimeout calls in the test code.
- Locators use semantic queries, not CSS selectors.
- CI runs the full suite and reports failures with traces.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/browser-testing
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: browser-testing
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/browser-testing/raw -o .cursor/skills/browser-testing/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/browser-testing.md and install it as a project skill at skills/browser-testing/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```