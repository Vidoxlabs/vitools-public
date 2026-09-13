---
name: edge-agents
description: >-
  Build stateful AI agents that run on edge compute platforms (Cloudflare
  Workers, Fastly Compute). Covers the Agents SDK pattern for durable,
  real-time, scheduled, and tool-calling agents at the edge. Use when
  building agents that need persistent state, WebSocket connections, or
  scheduled tasks on edge infrastructure.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: cloud
  tags: [cloud, agents, edge, workers, websocket, stateful]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: edge-agents
    summary: Build stateful AI agents on edge compute platforms
  derived_from:
    - name: cloudflare-building-ai-agent-on-cloudflare
      license: Apache-2.0
      url: https://github.com/cloudflare/agents
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Edge Agents

## When to use

Use this skill when building AI agents that run on edge compute
platforms. This includes agents that need persistent state, real-time
WebSocket connections, scheduled tasks, tool calling, or chat
capabilities deployed globally at the edge.

## Procedure

1. Choose the edge platform: Cloudflare Workers with the Agents SDK
   or Fastly Compute with WASM.
2. Define the agent class with state management: `onStart`,
   `onConnect`, `onMessage`, and `onClose` lifecycle methods.
3. Implement state persistence using the platform's key-value or
   Durable Objects storage.
4. For real-time: establish WebSocket connections and handle
   bidirectional messaging.
5. For scheduled tasks: use the platform's cron trigger or scheduling
   API.
6. For tool calling: define tools as methods and expose them via the
   agent's RPC interface.
7. Deploy with the platform CLI (`wrangler deploy` or `fastly compute
   publish`).

## Guardrails

- Do not store secrets in agent state. Use the platform's secret
  manager.
- Do not block the event loop. Edge runtimes are single-threaded —
  use async for all I/O.
- Do not assume state is shared across edge regions. Each region may
  have its own state replica.
- Do not skip the deployment config validation before publishing.

## Examples

### Good

> Built a chat agent on Workers with the Agents SDK. State persists
> via Durable Objects, WebSocket handles real-time messages, a cron
> trigger runs daily summaries. Deployed with `wrangler deploy`.

### Bad

> Built an agent that stores user data in a global variable. State
> is lost on every request because edge workers are stateless between
> invocations.

## Verification

- Agent state persists across requests (verified by reconnecting
  and checking state).
- WebSocket connection handles multiple concurrent clients.
- Scheduled tasks execute at the configured interval.
- No secrets are in the source code.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/edge-agents
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: edge-agents
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/edge-agents/raw -o .cursor/skills/edge-agents/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/edge-agents.md and install it as a project skill at skills/edge-agents/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
