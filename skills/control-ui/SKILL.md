---
name: control-ui
description: >-
  Build or adapt a local browser or CDP harness to drive and inspect
  a web, IDE, or Electron UI. Use for local UI verification,
  screenshots, accessibility snapshots, perf profiles, visual diffs,
  or reproducing UI bugs.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: automation
  tags: [automation, ui, browser, cdp, testing, screenshots, accessibility]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: control-ui
    summary: Drive and inspect web UIs with a local browser harness
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Control UI

## When to use

Activate when you need to programmatically drive and inspect a web UI,
IDE, or Electron app for testing or debugging. Use for UI verification,
screenshot capture, accessibility snapshots, performance profiling,
visual diff comparison, or bug reproduction.

## Procedure

1. Launch a browser with CDP (Chrome DevTools Protocol) using
   Playwright or Puppeteer.
2. Navigate to the target URL or launch the Electron app.
3. For screenshots: capture the full page or specific elements.
4. For accessibility: capture the accessibility tree and verify
   semantic structure.
5. For performance: capture a trace with `page.tracing.start()` and
   analyze the profile for long tasks and layout shifts.
6. For visual diffs: capture a screenshot and compare against a
   baseline using pixelmatch or similar.
7. For bug reproduction: drive the exact user flow, capture the console
   output, network requests, and DOM state at the failure point.

## Guardrails

- Do not test against a production URL unless explicitly authorized.
  Use a local dev server or staging.
- Do not capture screenshots without setting a consistent viewport
  size. Different sizes produce different layouts.
- Do not skip waiting for page load. Use `waitForSelector` or
  `networkidle` before capturing.
- Do not ignore console errors during UI testing. Capture and report
  them.

## Examples

### Good

> Launched Playwright with a 1280x720 viewport, navigated to
> `localhost:3000`, waited for `networkidle`, captured a full-page
> screenshot and accessibility tree. Found a missing ARIA label on
> the submit button and a console error about a failed font load.

### Bad

> Opened the URL in a browser, took a screenshot, and reported "looks
> fine." No viewport set, no wait for load, no accessibility check,
> no console capture.

## Verification

- Screenshots are captured at a consistent viewport size.
- Accessibility tree is captured and semantic issues are reported.
- Console errors are captured.
- Performance trace shows no unexpected long tasks.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/control-ui
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: control-ui
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/control-ui/raw -o .cursor/skills/control-ui/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/control-ui.md and install it as a project skill at skills/control-ui/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
