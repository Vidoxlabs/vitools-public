---
name: meeting-preparation
description: >-
  Prepare for meetings by gathering context, defining agenda, identifying decisions needed, and pre-drafting outcomes. Use when preparing for important meetings or reviews.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: docs
  tags: [meeting, preparation, agenda, context, decisions]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: meeting-preparation
    summary: Prepare meetings with context and clear outcomes
  derived_from:
    - name: cowork-meeting-prep
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Meeting Preparation

## When to use

Activate when preparing for a meeting, review, or presentation. Use when the user needs to walk into a meeting with full context and a clear agenda.

## Procedure

1. Identify the meeting type: decision, status update, brainstorm, or review.
2. Gather context: relevant docs, metrics, prior decisions, and open action items.
3. Define the agenda: 3-5 topics max, each with a time allocation and desired outcome.
4. List decisions needed: what must be decided by the end of the meeting.
5. Pre-draft outcomes: what the ideal result looks like for each decision.
6. Identify stakeholders: who needs to attend, who is optional, who needs pre-read.
7. Send pre-read material 24 hours before the meeting.

## Guardrails

- Do not schedule a meeting without an agenda. If there is no agenda, it is a chat.
- Do not include more than 5 topics. Time-box each one.
- Do not skip the pre-read. Attendees who arrive cold waste everyone's time.
- Do not leave a meeting without documenting decisions and action items.

## Examples

### Good

> Prepared a 30-minute decision meeting: agenda has 3 topics, pre-read sent 24h before, 2 decisions are pre-drafted with options, stakeholders identified with required vs optional. Meeting produced 2 decisions and 4 action items.

### Bad

> Scheduled a 60-minute meeting with no agenda. Attendees arrived cold. Discussed 8 topics, decided nothing, no action items documented.

## Verification

- Agenda exists with time-boxed topics and desired outcomes.
- Pre-read is sent 24 hours before the meeting.
- Decisions and action items are documented during the meeting.
- Meeting length matches the agenda scope.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/meeting-preparation
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: meeting-preparation
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/meeting-preparation/raw -o .cursor/skills/meeting-preparation/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/meeting-preparation.md and install it as a project skill at skills/meeting-preparation/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```