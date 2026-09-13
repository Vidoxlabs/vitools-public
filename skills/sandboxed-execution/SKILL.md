---
name: sandboxed-execution
description: >-
  Build sandboxed code execution environments for AI code interpreters,
  CI systems, or untrusted code. Covers isolation, resource limits,
  file system access, and preview URLs. Use when building tools that
  execute user-provided or AI-generated code safely.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: cloud
  tags: [cloud, sandbox, security, code-execution, isolation, edge]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: sandboxed-execution
    summary: Build sandboxed code execution environments
  derived_from:
    - name: cloudflare-sandbox-sdk
      license: Apache-2.0
      url: https://developers.cloudflare.com/sandbox/
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Sandboxed Execution

## When to use

Use this skill when building systems that execute user-provided or
AI-generated code in isolation. This includes AI code interpreters,
CI/CD systems, interactive development environments, or any tool
that runs untrusted code.

## Procedure

1. Choose the isolation mechanism: WASM sandbox (edge), container
   isolation (Docker/gVisor), or VM isolation (Firecracker).
2. Define resource limits: CPU time, memory, disk, and network
   access. Set timeouts for all operations.
3. Configure file system access: mount only the working directory.
   Use read-only mounts for shared dependencies.
4. Implement network policies: allow-list egress domains, block
   internal network ranges, and rate-limit outbound requests.
5. For code interpreters: support stdin/stdout piping, install
   dependencies on demand, and capture execution output.
6. For preview URLs: generate ephemeral URLs that serve the sandbox's
   output. Expire them after a timeout.
7. Clean up: destroy the sandbox and all its state after execution
   completes or times out.

## Guardrails

- Do not grant network access to internal services. Use an allow-list
  for external domains only.
- Do not skip resource limits. Without them, a single execution can
  exhaust the host.
- Do not persist sandbox state between executions. Each run starts
  clean.
- Do not expose the sandbox filesystem to the host without isolation.

## Examples

### Good

> Built a code interpreter on edge WASM. Each execution gets 256MB
> RAM, 5s CPU, no network, a temp working directory, and auto-cleanup
> after 60s. Dependencies installed on demand from a cached registry.

### Bad

> Ran user code in a Docker container with no resource limits, full
> network access, and a persistent volume. A malicious script mined
> crypto for hours.

## Verification

- Resource limits are enforced (CPU, memory, timeout).
- Network access is restricted to allowed domains.
- Sandbox state is destroyed after execution.
- No host filesystem exposure.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/sandboxed-execution
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: sandboxed-execution
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/sandboxed-execution/raw -o .cursor/skills/sandboxed-execution/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/sandboxed-execution.md and install it as a project skill at skills/sandboxed-execution/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
