---
name: pr-walkthrough
description: >-
  Generate an interactive PR review walkthrough as an HTML page. Fetch PR data, categorize changes, add annotations, and render diffs with moved-code detection. Use when preparing a PR for visual review.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: git
  tags: [pull-requests, review, walkthrough, visual, diff]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: pr-walkthrough
    summary: Interactive PR review walkthrough
  derived_from:
    - name: compound-engineering-pr-review-canvas
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# PR Walkthrough

## When to use

Activate when preparing a pull request for visual review. Use when a reviewer needs a guided walkthrough of the changes.

## Procedure

1. Fetch PR data via gh API: files changed, diff content, commit history.
2. Categorize files: core changes vs mechanical changes (formatting, imports).
3. Generate the HTML page with: file list, diff viewer, and reviewer annotations.
4. Add moved-code detection: highlight code that was moved, not modified.
5. Include a summary section: what changed, why, risk areas.
6. Render as a self-contained HTML file with embedded CSS and JS.
7. Share with the reviewer.

## Guardrails

- Do not include unrelated changes in the walkthrough. Focus on the PR scope.
- Do not skip the risk areas section. Reviewers need to know where to focus.
- Do not make the HTML file huge. Minimize embedded content.
- Do not forget to test in a browser before sharing.

## Examples

### Good

> Generated an HTML walkthrough for a 12-file PR: categorized 8 core changes and 4 mechanical, detected 2 moved-code blocks, added annotations on 3 risk areas. Reviewer used it to focus their review.

### Bad

> Sent the reviewer a raw git diff URL. No categorization, no annotations, no risk areas. Reviewer spent 30 minutes just understanding the scope.

## Verification

- PR data is fetched and categorized.
- Moved-code is detected and highlighted.
- Risk areas are annotated.
- HTML file opens in any browser.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/pr-walkthrough
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: pr-walkthrough
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/pr-walkthrough/raw -o .cursor/skills/pr-walkthrough/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/pr-walkthrough.md and install it as a project skill at skills/pr-walkthrough/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```