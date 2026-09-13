---
name: fastly-cli-ngwaf
description: >-
  Use the Fastly CLI for service management and configure Fastly NGWAF
  (Next-Generation WAF) rules. Covers service creation, version
  management, and WAF rule deployment. Use when managing Fastly
  services or configuring WAF protection.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: cloud
  tags: [cloud, fastly, cli, waf, security, deployment]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: fastly-cli-ngwaf
    summary: Fastly CLI and NGWAF configuration
  derived_from:
    - name: fastly-fastly-cli
      license: MIT
      url: https://github.com/fastly/cli
      note: Concept only. Body rewritten.
    - name: fastly-fastly-ngwaf
      license: MIT
      url: https://github.com/fastly/ngwaf
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Fastly CLI and NGWAF

## When to use

Use this skill when managing Fastly services with the CLI or
configuring Next-Generation WAF (NGWAF) protection. Covers service
creation, version management, WAF rule deployment, and security
posture verification.

## Procedure

1. Authenticate: `fastly profile create` with your API token. Verify
   with `fastly profile list`.
2. For service management: `fastly service create` to create,
   `fastly service list` to view, `fastly version clone` to create
   a new version for changes.
3. For NGWAF: create a WAF configuration on the service version.
   Enable rulesets (OWASP, custom rules).
4. Configure rule actions: log, block, or challenge. Start with
   `log` to observe before switching to `block`.
5. Deploy the version: `fastly version activate`.
6. Monitor: check WAF analytics for blocked requests and false
   positives. Adjust rules as needed.
7. Rollback if false positives spike: `fastly version activate
   <previous_version>`.

## Guardrails

- Do not activate a new version without testing on staging first.
- Do not switch WAF rules from `log` to `block` without observing
  traffic for at least 24 hours.
- Do not deploy NGWAF rules without understanding the application's
  legitimate traffic patterns.
- Do not leave the API token in environment variables permanently.
  Use a secrets manager.

## Examples

### Good

> Created a new service version, added NGWAF with OWASP ruleset set
> to `log` mode. Observed traffic for 48 hours, identified 3 false
> positives, added exceptions, then switched to `block` mode and
> activated.

### Bad

> Enabled NGWAF with all rules set to `block` and activated
> immediately. Legitimate API traffic was blocked and the service
> went down.

## Verification

- Service version is active and responding.
- NGWAF rules are deployed with the correct action mode.
- WAF analytics show expected traffic patterns.
- No legitimate traffic is being blocked.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/fastly-cli-ngwaf
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: fastly-cli-ngwaf
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/fastly-cli-ngwaf/raw -o .cursor/skills/fastly-cli-ngwaf/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/fastly-cli-ngwaf.md and install it as a project skill at skills/fastly-cli-ngwaf/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
