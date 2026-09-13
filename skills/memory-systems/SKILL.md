---
name: memory-systems
description: >-
  Design and maintain agent memory systems: working memory for session context, persistent memory for cross-session knowledge, and index management for retrieval. Use when building agent memory architectures.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: docs
  tags: [memory, agent, persistent, working-memory, index]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: memory-systems
    summary: Agent memory system design and maintenance
  derived_from:
    - name: anthropic-memory-management-schedule
      license: Proprietary
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Memory Systems

## When to use

Activate when designing or maintaining an agent's memory system. Use when building memory architectures for agents that need cross-session context.

## Procedure

1. Define the memory tiers: working memory (session-scoped, ephemeral), persistent memory (cross-session, durable), and index (retrieval metadata).
2. Choose storage: in-context for working memory, files or KV for persistent, an index file for retrieval.
3. Define what goes where: conversation state in working, preferences and facts in persistent, tags and timestamps in index.
4. Implement write paths: when does memory get updated, who triggers it, what gets written.
5. Implement read paths: when does memory get loaded, how is it scoped, what gets retrieved.
6. Define the cleanup policy: when is working memory cleared, when is persistent memory pruned.
7. Test: verify memory persists across sessions and does not leak between users.

## Guardrails

- Do not store secrets in memory files. Use a secrets manager.
- Do not let memory grow unbounded. Define a pruning policy.
- Do not mix working and persistent memory. They have different lifecycles.
- Do not skip the index. Without it, retrieval is O(n).

## Examples

### Good

> Built a 2-tier memory system: working memory in session context, persistent memory in a JSON file with an index for retrieval. Pruning policy removes entries older than 90 days. Tested across 3 sessions.

### Bad

> Stored everything in a single growing file with no structure. After 100 sessions the file is 50 MB and retrieval takes 5 seconds.

## Verification

- Memory tiers are defined and separated.
- Write and read paths are documented.
- Pruning policy is defined and tested.
- No secrets are stored in memory files.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/memory-systems
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: memory-systems
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/memory-systems/raw -o .cursor/skills/memory-systems/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/memory-systems.md and install it as a project skill at skills/memory-systems/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```