---
name: browser-automation-testing
description: >-
  Automate web browser interactions through MCP tools or Playwright. Navigate, extract data, fill forms, click buttons, and take screenshots. Use when automating browser workflows.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: automation
  tags: [browser, automation, mcp, playwright, screenshots]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: browser-automation-testing
    summary: Automate browser interactions via MCP or Playwright
  derived_from:
    - name: cursor-browser-automation
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Browser Automation

## When to use

Activate when automating web browser interactions: navigating pages, extracting data, filling forms, clicking buttons, or taking screenshots.

## Procedure

1. Launch a browser via MCP tools or Playwright.
2. Navigate to the target URL. Wait for page load.
3. Locate elements by role, text, or CSS selector (prefer semantic locators).
4. Perform actions: click, type, select, scroll, screenshot.
5. Extract data: text content, attributes, table data, or full page HTML.
6. Handle authentication: session cookies, login forms, or token injection.
7. Close the browser and clean up the session.

## Guardrails

- Do not use fragile CSS selectors. Prefer role-based or text-based locators.
- Do not skip waiting for page load. Timing-dependent failures are hard to debug.
- Do not store credentials in the automation script. Use env vars or a vault.
- Do not leave browser sessions open. Always clean up.

## Examples

### Good

> Automated a login and data extraction flow: navigated to the login page, filled credentials from env vars, waited for dashboard, extracted the top 10 items from a table, took a screenshot, closed the browser.

### Bad

> Hardcoded credentials in the script, used a CSS selector that changes every deploy, did not wait for page load, left the browser session open.

## Verification

- Browser session is launched and closed cleanly.
- No credentials are in the script source.
- Locators use semantic queries.
- Extracted data matches expectations.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/browser-automation-testing
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: browser-automation-testing
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/browser-automation-testing/raw -o .cursor/skills/browser-automation-testing/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/browser-automation-testing.md and install it as a project skill at skills/browser-automation-testing/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```