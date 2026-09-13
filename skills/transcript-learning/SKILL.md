---
name: transcript-learning
description: >-
  Extract durable working preferences and patterns from chat transcripts and convert them into skills, rules, or workflow docs. Use when mining past conversations for reusable guidance.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: automation
  tags: [transcript, learning, preferences, mining, workflows]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: transcript-learning
    summary: Extract durable preferences from chat transcripts
  derived_from:
    - name: cursor-continual-learning-workflow-from-chats
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Transcript Learning

## When to use

Activate when mining past chat transcripts for reusable patterns, preferences, or workflow guidance. Use when building a knowledge base from conversation history.

## Procedure

1. Collect transcripts from the specified time range (default: last 7 days).
2. Read parent transcripts and relevant subagent transcripts. Use subagent content as evidence.
3. Extract durable preferences: working style, tool preferences, code conventions, recurring workflows.
4. Distinguish durable from ephemeral: preferences are durable, specific tasks are ephemeral.
5. Convert each durable preference into a skill, rule, or workflow doc.
6. Do not expose private chat content, secrets, or personal data in the extracted output.
7. Save the extracted patterns to the project's rules or skills directory.

## Guardrails

- Do not expose private chat content, secrets, or customer data.
- Do not extract ephemeral task details as durable patterns.
- Do not cite subagent transcripts directly. Use them as evidence only.
- Do not skip the durable vs ephemeral distinction.

## Examples

### Good

> Mined 7 days of transcripts, extracted 5 durable preferences (code style, testing approach, git workflow, review priorities, documentation format), saved as rules in the project. No private data exposed.

### Bad

> Summarized all chat transcripts into a document including private conversations and specific task details. Mixed durable and ephemeral information.

## Verification

- Only durable patterns are extracted, not ephemeral tasks.
- No private content, secrets, or personal data is in the output.
- Extracted patterns are saved as reusable rules or skills.
- The source transcript range is documented.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/transcript-learning
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: transcript-learning
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/transcript-learning/raw -o .cursor/skills/transcript-learning/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/transcript-learning.md and install it as a project skill at skills/transcript-learning/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```