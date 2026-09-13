---
name: durable-objects-patterns
description: >-
  Build stateful, coordinated applications using Durable Objects or
  equivalent edge-state primitives. Covers chat rooms, multiplayer
  coordination, booking systems, rate limiting, and real-time
  collaboration. Use when multiple clients need shared state with strong
  consistency at the edge.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: cloud
  tags: [cloud, durable-objects, stateful, coordination, realtime, edge]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: durable-objects-patterns
    summary: Stateful coordination patterns for edge applications
  derived_from:
    - name: cloudflare-durable-objects
      license: Apache-2.0
      url: https://developers.cloudflare.com/durable-objects/
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Durable Objects Patterns

## When to use

Use this skill when building applications that need shared, strongly
consistent state across multiple clients at the edge. This includes
chat rooms, multiplayer games, booking systems, rate limiters,
real-time collaboration, and any pattern where multiple clients
coordinate through a single stateful entity.

## Procedure

1. Identify the coordination unit: what entity needs shared state?
   (a room, a session, a counter, a queue).
2. Define the Durable Object class with `state` storage and
   `fetch`/`webSocket` handlers.
3. Implement the state machine: what transitions are valid, who can
   trigger them, and what happens on conflict.
4. For real-time: accept WebSocket connections in the `webSocket`
   handler. Broadcast state changes to all connected clients.
5. For persistence: use `state.storage.put()` for durable state and
   `state.storage.get()` for reads.
6. For alarm-based scheduling: use `state.storage.setAlarm()` for
   time-based actions.
7. Route requests to the correct Durable Object instance using a
   stable ID from the URL or request.

## Guardrails

- Do not store large data in a single Durable Object. Each has
  storage limits. Shard by ID for large datasets.
- Do not perform expensive computation in the constructor. Lazy-load
  state on first request.
- Do not assume global visibility. Each Durable Object instance is
  single-threaded and region-specific.
- Do not forget to handle WebSocket disconnects. Clean up state
  when a client leaves.

## Examples

### Good

> Built a chat room as a Durable Object. Each room has a stable ID.
> Clients connect via WebSocket, messages broadcast to all connected
> clients, state persists across reconnections, and the alarm cleans
> up inactive rooms after 24 hours.

### Bad

> Stored all chat rooms in a single global Durable Object. Every
> message from every room goes through one instance, creating a
> bottleneck and exceeding storage limits.

## Verification

- State persists across reconnections.
- Multiple clients receive updates in real time.
- Disconnected clients are cleaned up.
- Each coordination unit has its own Durable Object instance.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/durable-objects-patterns
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: durable-objects-patterns
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/durable-objects-patterns/raw -o .cursor/skills/durable-objects-patterns/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/durable-objects-patterns.md and install it as a project skill at skills/durable-objects-patterns/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
