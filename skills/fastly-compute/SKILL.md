---
name: fastly-compute
description: >-
  Build Fastly Compute applications with WASM. Covers the Compute API,
  backends, request handling, and deployment. Use when building edge
  services on Fastly Compute for Rust, JavaScript, or other WASM-targeting
  languages.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: cloud
  tags: [cloud, fastly, compute, wasm, edge, rust]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: fastly-compute
    summary: Build Fastly Compute WASM applications
  derived_from:
    - name: fastly-fastlike
      license: MIT
      url: https://github.com/fastly/fastlike
      note: Concept only. Body rewritten.
    - name: fastly-fastly
      license: MIT
      url: https://github.com/fastly/fastly
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Fastly Compute

## When to use

Use this skill when building edge services on Fastly Compute with
WASM. Covers the Compute API, backend configuration, request
handling, and deployment for Rust, JavaScript, or any language that
compiles to WASM.

## Procedure

1. Initialize a project: `fastly compute init` or use the language
   template (`fastly compute init --language rust`).
2. Configure `fastly.toml`: define backends, dictionaries, and
   stores. Each backend your app calls must be listed.
3. Implement the request handler: `on_request` receives the request
   and returns a response. Use the Compute API for backend requests,
   header manipulation, and caching.
4. For Rust: use `cargo build --release --target wasm32-wasi`.
   For JavaScript: use `fastly compute build`.
5. Test locally with Viceroy: `viceroy -C fastly.toml bin/main.wasm`.
6. Deploy: `fastly compute publish`.
7. Verify the service URL responds correctly.

## Guardrails

- Do not call a backend that is not listed in `fastly.toml`. The
  runtime will reject the request.
- Do not block on synchronous I/O. Compute is async — use the
  async API for all backend calls.
- Do not hardcode backend URLs. Define them in `fastly.toml` and
  reference by name in code.
- Do not deploy without testing locally with Viceroy first.

## Examples

### Good

> Built a Compute service in Rust. `fastly.toml` lists two backends:
> `origin` and `api`. Handler routes `/api/*` to the `api` backend
> and everything else to `origin`. Tested with Viceroy on port 7676,
> deployed with `fastly compute publish`.

### Bad

> Hardcoded `https://api.example.com` in the Rust code instead of
> defining a backend in `fastly.toml`. Deployed without local testing.
> The service fails because the backend is not registered.

## Verification

- `fastly compute build` succeeds.
- Viceroy runs the service and responds to test requests.
- `fastly compute publish` succeeds.
- The service URL returns the expected response.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/fastly-compute
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: fastly-compute
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/fastly-compute/raw -o .cursor/skills/fastly-compute/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/fastly-compute.md and install it as a project skill at skills/fastly-compute/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
