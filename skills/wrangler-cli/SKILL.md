---
name: wrangler-cli
description: >-
  Use Wrangler CLI for Cloudflare Workers development, testing, and
  deployment. Covers dev server, secrets, environment management,
  tailing logs, and deployment configuration. Use when developing or
  deploying Workers applications.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: cloud
  tags: [cloud, wrangler, cli, cloudflare, deployment, dev-server]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: wrangler-cli
    summary: Wrangler CLI for Workers development and deployment
  derived_from:
    - name: cloudflare-wrangler
      license: Apache-2.0
      url: https://developers.cloudflare.com/workers/wrangler/
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Wrangler CLI

## When to use

Use this skill when developing or deploying Cloudflare Workers
applications with Wrangler. Covers the dev server, secrets management,
environment configuration, log tailing, and deployment.

## Procedure

1. Initialize a new project: `npm create cloudflare@latest` or
   `wrangler init`.
2. Configure `wrangler.toml`: set the name, main entry point,
   compatibility date, and environment-specific bindings (KV, R2,
   Durable Objects, D1).
3. Run the dev server: `wrangler dev` (local) or `wrangler dev --
   remote` (on the edge).
4. Manage secrets: `wrangler secret put <name>` to set, `wrangler
   secret list` to view. Never commit secrets to `wrangler.toml`.
5. Deploy: `wrangler deploy`. Verify the deployment URL responds.
6. Tail logs: `wrangler tail` to see live requests and console
   output.
7. Rollback if needed: `wrangler rollback` to revert to the
   previous deployment.

## Guardrails

- Do not commit secrets in `wrangler.toml`. Use `wrangler secret
  put` for all sensitive values.
- Do not deploy without testing locally first with `wrangler dev`.
- Do not use a stale compatibility date. Set it to the current date
  to access the latest runtime features.
- Do not forget to configure environment-specific bindings for
  staging and production.

## Examples

### Good

> `wrangler dev` tested locally, `wrangler secret put API_KEY` set
> the secret, `wrangler deploy` deployed to production, `wrangler
> tail` confirmed requests are arriving. Rollback available if
> needed.

### Bad

> Hardcoded `API_KEY` in `wrangler.toml`, committed to git, deployed
> without local testing, no way to see production logs.

## Verification

- `wrangler dev` runs without errors.
- `wrangler deploy` succeeds and the URL responds.
- `wrangler tail` shows incoming requests.
- No secrets in `wrangler.toml` or source code.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/wrangler-cli
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: wrangler-cli
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/wrangler-cli/raw -o .cursor/skills/wrangler-cli/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/wrangler-cli.md and install it as a project skill at skills/wrangler-cli/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
