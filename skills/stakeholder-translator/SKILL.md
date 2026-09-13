---
name: stakeholder-translator
description: >-
  Communicate the same technical information to different audiences
  by reframing substance without changing facts. Use when adapting a
  message for executives, engineers, or non-technical stakeholders.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: docs
  tags: [communication, documentation, audience, technical-writing]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: stakeholder-translator
    summary: Reframe technical substance for different audiences without altering facts
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Stakeholder Translator

## When to use

Activate when the same technical finding, decision, or status needs
to be communicated to audiences with different backgrounds —
executives who need business impact, engineers who need technical
detail, or non-technical stakeholders who need plain-language context.

## Procedure

1. Identify the core facts. These do not change across versions.
   Write them down first so every version refers to the same
   substance.
2. For each audience, determine what they need to decide or do with
   the information. The version is shaped by the action, not the
   audience's job title.
3. Draft the executive version: lead with the decision or impact,
   support with at most three key points, end with the ask. Keep it
   under one page.
4. Draft the engineer version: include architecture, trade-offs,
   risks, and testing steps. Link to code, configs, or logs.
5. Draft the non-technical version: use plain language, avoid jargon,
   and explain any term that has no everyday equivalent. Lead with
   what changes for them.
6. Cross-check all three versions against the core facts. If any
   version contradicts, omits a material fact, or adds a fact not in
   the source, fix it.

## Guardrails

- Do not soften bad news for executives. Reframe for clarity, not for
  comfort.
- Do not omit risks from the engineer version to make the plan look
  cleaner.
- Do not add technical depth to the executive version that the reader
  cannot act on.
- Do not change the facts between versions. Same substance, different
  frame.

## Examples

### Good

> Core fact: the migration will take two weeks and requires a
> four-hour maintenance window. Executive version: "Two-week
> migration, four-hour downtime, no data loss, decision needed by
> Friday." Engineer version: "Migration steps, rollback plan, test
> checklist, timeline with dependencies." Non-technical: "Your
> dashboard will be unavailable for four hours on Saturday. After
> that, reports will load faster."

### Bad

> Executive version says "minor maintenance." Engineer version says
> "full database migration with data loss risk." Non-technical
> version says "system upgrade." Three different stories for the
> same event.

## Verification

- All versions state the same core facts without contradiction.
- Each version is actionable for its intended audience.
- No version adds facts not present in the source material.
- The executive version is under one page and leads with the
  decision.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/stakeholder-translator
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: stakeholder-translator
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/stakeholder-translator/raw -o .cursor/skills/stakeholder-translator/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/stakeholder-translator.md and install it as a project skill at skills/stakeholder-translator/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
