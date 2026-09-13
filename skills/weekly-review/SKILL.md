---
name: weekly-review
description: >-
  Produce a weekly synthesis of authored commits with highlights by
  bugfix, tech debt, and net-new work. Use when summarizing a week
  of work for standup, status report, or retrospective.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: docs
  tags: [docs, reporting, weekly, summary, commits, standup]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: weekly-review
    summary: Weekly synthesis of commits by category
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Weekly Review

## When to use

Activate when summarizing a week of work for a standup, status
report, or team retrospective. Use when the user asks "what did I do
this week" or needs a weekly summary for stakeholders.

## Procedure

1. Identify the date range: default to the last 7 days, or use the
   user-specified range.
2. Fetch all commits authored by the user in the range across all
   relevant repositories. Use `git log --author --since --until`.
3. Categorize each commit: bugfix, feature, tech debt, docs, test,
   refactor, or chore.
4. Group commits by project or repository if working across multiple.
5. Highlight the most impactful changes: what shipped, what was fixed,
   what was improved.
6. Note any blockers or unfinished work carried into the next week.
7. Produce a summary with three sections: highlights, details by
   category, and carry-over items.

## Guardrails

- Do not list every commit verbatim. Synthesize and summarize.
- Do not omit bugs fixed — they are often the most visible impact.
- Do not inflate the summary with trivial commits (merge commits,
  formatting only).
- If working across repos, clearly label which repo each item came
  from.

## Examples

### Good

> This week: shipped the auth refactor (3 commits in `api`), fixed
> the login timeout bug (2 commits in `web`), and paid down tech debt
> by removing the legacy config loader (1 commit in `core`). Carrying
> over: the rate limiter tests are still failing.

### Bad

> Listed 47 raw commit messages with no categorization, no
> highlights, and no summary.

## Verification

- The date range is correct and explicit.
- Commits are categorized, not listed verbatim.
- Highlights focus on impact, not volume.
- Carry-over items are clearly marked.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/weekly-review
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: weekly-review
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/weekly-review/raw -o .cursor/skills/weekly-review/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/weekly-review.md and install it as a project skill at skills/weekly-review/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
