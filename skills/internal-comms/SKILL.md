---
name: internal-comms
description: >-
  Write internal communications: status reports, weekly updates,
  incident reports, FAQs, and leadership updates. Use when
  communicating project status, incidents, or plans to internal
  audiences.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: docs
  tags: [docs, communications, status, incident, reporting, internal]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: internal-comms
    summary: Write clear internal communications for any audience
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Internal Communications

## When to use

Activate when writing status reports, weekly updates, incident
reports, FAQs, leadership updates, or project summaries for internal
audiences. Use when the user says "write a status report", "draft an
incident report", or "send a project update".

## Procedure

1. Identify the communication type: status report, incident report,
   weekly update, FAQ, or leadership brief.
2. Identify the audience and what they need to know or decide.
3. Lead with the most important information: the current state, the
   impact, and the ask.
4. For status reports: what is done, what is in progress, what is
   blocked, and what is next.
5. For incident reports: what happened, when, impact, root cause if
   known, mitigation, and follow-up actions.
6. For weekly updates: highlights, metrics, and carry-over items.
7. Keep it concise. One page maximum for most internal comms.

## Guardrails

- Do not bury the lead. The most important information goes first.
- Do not soften incident reports. State the impact clearly and
  factually.
- Do not include confidential information in a broad distribution.
- Do not write more than one page unless the audience specifically
  requested detail.

## Examples

### Good

> Incident report: "At 14:32 UTC, the API returned 500 errors for
> 12 minutes due to a database connection pool exhaustion. Impact:
> 8% of requests failed. Mitigation: restarted the pool and
> increased max connections. Follow-up: audit connection leak by
> Friday."

### Bad

> "There was an issue with the API earlier today. We're looking into
> it." No time, no impact, no mitigation, no follow-up.

## Verification

- The most important information is in the first paragraph.
- The communication type matches the request.
- It is under one page.
- Impact, mitigation, and follow-up are present for incident reports.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/internal-comms
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: internal-comms
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/internal-comms/raw -o .cursor/skills/internal-comms/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/internal-comms.md and install it as a project skill at skills/internal-comms/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
