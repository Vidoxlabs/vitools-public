---
name: what-did-i-get-done
description: >-
  Summarize authored commits over a user-specified time period into a
  concise update. Use when preparing a status update, daily standup,
  or end-of-sprint summary.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: docs
  tags: [docs, reporting, summary, commits, standup, status]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: what-did-i-get-done
    summary: Summarize commits into a concise status update
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# What Did I Get Done

## When to use

Activate when the user needs a concise summary of what they
accomplished over a time period. Use for daily standups, end-of-day
updates, sprint summaries, or when asked "what did you do today?"

## Procedure

1. Determine the time range: default to today, or use the
   user-specified range.
2. Fetch all commits authored by the user in the range using
   `git log --author --since --until --oneline`.
3. If working across multiple repos, gather commits from each.
4. Group commits by theme: features shipped, bugs fixed, improvements
   made, and infrastructure or tooling.
5. Write a 3-5 bullet summary. Lead with the most impactful work.
6. Include a one-line note on what is in progress or blocked if
   relevant.

## Guardrails

- Do not list raw commit hashes. Translate to human-readable
  descriptions.
- Do not include merge commits or trivial formatting changes unless
  they were the only work done.
- Keep the summary concise: 3-5 bullets for a day, 5-10 for a week.
- Do not fabricate work. If no commits were found, say so.

## Examples

### Good

> Today: shipped the password reset flow (3 commits), fixed the
> pagination bug in the user list (1 commit), and updated the API
  docs for the new auth endpoints (1 commit). In progress: the
  rate limiter is still failing tests.

### Bad

> a1b2c3d fix typo
> d4e5f6g merge main
> h7i8j9k wip
> k0l1m2n merge main
> (raw commit log with no summary)

## Verification

- The time range is correct.
- Commits are summarized as human-readable bullets, not hashes.
- The summary is concise and leads with the most impactful work.
- In-progress or blocked items are noted if relevant.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/what-did-i-get-done
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: what-did-i-get-done
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/what-did-i-get-done/raw -o .cursor/skills/what-did-i-get-done/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/what-did-i-get-done.md and install it as a project skill at skills/what-did-i-get-done/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
