---
name: viceroy
description: >-
  Run Fastly Compute WASM applications locally with Viceroy for Rust and
  Component Model projects. Use when starting a local dev server,
  configuring fastly.toml for backends and stores, running tests against
  the Compute runtime, or troubleshooting local Compute issues.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: cloud
  tags: [cloud, fastly, wasm, edge, testing]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: viceroy
    summary: Local Fastly Compute WASM runtime for Rust development
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Viceroy — Local Fastly Compute Runtime

## When to use

Use this skill when developing or testing Fastly Compute applications
locally with Viceroy. This includes starting a local dev server,
configuring `fastly.toml` for local backends and stores, running Rust
unit tests against the Compute runtime, adapting WASM modules to the
Component Model, or troubleshooting local testing issues.

## Procedure

1. Install Viceroy: `cargo install --locked viceroy`.
2. Build your Compute app: `fastly compute build`.
3. Ensure `fastly.toml` has a `[local_server]` section with backends,
   stores, and overrides listed.
4. Start the local server: `viceroy -C fastly.toml bin/main.wasm`
   (default: `127.0.0.1:7676`).
5. For Rust testing, use `cargo-nextest` with the Compute runtime to
   validate service behavior.
6. When adapting core WASM modules to the Component Model, verify the
   build pipeline produces a compatible WASM output.

## Guardrails

- Dictionaries and ConfigStores are configured differently in
  `fastly.toml` — dictionaries go under `[local_server.dictionaries]`,
  ConfigStores under `[local_server.config_stores]`.
- `fastly.toml` must have a `[local_server]` section. Without it,
  Viceroy will not know about backends or stores.
- Default port is 7676, not 5000.
- Backends should point to local servers when developing locally. Do
  not proxy to remote production origins to prevent leaking request data.

## Examples

### Good

> Developer configures `[local_server.backends]` with a local API server
> at `127.0.0.1:3000`, starts Viceroy on port 7676, and tests the Compute
> app end-to-end without touching production.

### Bad

> Developer runs `viceroy` without a `[local_server]` section. Viceroy
> crashes because it cannot find backend definitions. The developer
> assumes the tool is broken.

## Verification

- Confirm Viceroy starts and responds at `http://127.0.0.1:7676`.
- Confirm all backends in `fastly.toml` are reachable.
- Run `cargo-nextest` and confirm tests pass against the Compute runtime.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/viceroy
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: viceroy
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/viceroy/raw -o .cursor/skills/viceroy/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/viceroy.md and install it as a project skill at skills/viceroy/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
