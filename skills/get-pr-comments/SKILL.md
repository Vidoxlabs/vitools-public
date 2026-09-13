---
name: get-pr-comments
description: >-
  Fetch and summarize review comments from the active pull request.
  Use when you need a concise, actionable summary of reviewer feedback
  before responding or making changes.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: git
  tags: [git, pull-requests, code-review, feedback, summary]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: get-pr-comments
    summary: Fetch and summarize PR review comments into actionable items
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Get PR Comments

## When to use

Activate when you need to read and summarize review feedback on a pull
request. Use before responding to reviews, when planning changes based
on feedback, or when the user asks "what did the reviewer say?"

## Procedure

1. Identify the active PR from the current branch or a user-provided
   URL. Extract the PR number.
2. Fetch all review comments using `gh pr view <number> --comments` or
   the GitHub API.
3. Fetch inline review comments using `gh api repos/{owner}/{repo}/
   pull_requests/{number}/comments`.
4. Categorize each comment: blocking, suggestion, question, nit, or
   approve.
5. Summarize: list blocking items first, then suggestions, then
   questions. Include file and line references.
6. For each blocking item, note the specific change requested.

## Guardrails

- Do not dismiss or filter out blocking comments. All must be
  addressed.
- Do not paraphrase a comment without checking you understood it.
  Quote the key point if ambiguous.
- Do not skip inline comments. They often contain the most actionable
  feedback.
- Do not mark a comment as resolved without making the requested
  change.

## Examples

### Good

> Fetched 8 comments. 2 blocking (missing test in `api.ts:42`,
> security concern in `auth.ts:15`), 3 suggestions, 2 questions, 1
> approve. Summary leads with the 2 blocking items and their exact
> locations.

### Bad

> "The reviewer left some comments." No categories, no file
> references, no distinction between blocking and non-blocking.

## Verification

- All review comments were fetched and categorized.
- Blocking items are listed first with file and line references.
- The summary is concise and actionable.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/get-pr-comments
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: get-pr-comments
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/get-pr-comments/raw -o .cursor/skills/get-pr-comments/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/get-pr-comments.md and install it as a project skill at skills/get-pr-comments/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
