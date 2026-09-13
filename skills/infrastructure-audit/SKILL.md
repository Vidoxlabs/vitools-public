---
name: infrastructure-audit
description: >-
  Audit infrastructure for security, compliance, and operational health. Review access controls, network exposure, resource configurations, and monitoring coverage. Use when assessing infrastructure readiness or preparing for compliance reviews.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: infra
  tags: [infrastructure, audit, security, compliance, monitoring]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: infrastructure-audit
    summary: Infrastructure security and compliance audit
  derived_from:
    - name: elastic-elasticsearch-kibana-observability-security
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Infrastructure Audit

## When to use

Activate when auditing infrastructure for security posture, compliance gaps, or operational health. Use before compliance reviews, after architecture changes, or when investigating incidents.

## Procedure

1. Inventory all infrastructure components: servers, containers, databases, networks, and APIs.
2. Check access controls: who has admin access, are MFA and least-privilege enforced, are service accounts scoped.
3. Review network exposure: open ports, public endpoints, missing TLS, firewall gaps.
4. Audit resource configurations: disk encryption, backup status, auto-scaling policies, log retention.
5. Verify monitoring coverage: are alerts configured for CPU, memory, disk, uptime, and security events.
6. Produce a report with findings by severity: critical, high, medium, low.

## Guardrails

- Do not run active exploitation or penetration tests without authorization.
- Do not expose credentials or secrets in the audit report.
- Do not skip any infrastructure component. Complete coverage is required.
- Do not mark a finding as resolved without verifying the fix.

## Examples

### Good

> Audited 12 servers and 3 databases. Found 2 critical (open SSH port on public IP, no disk encryption on DB), 3 high (stale access keys, no log retention, missing alerts). Report includes remediation steps.

### Bad

> Ran a quick scan of 3 servers, said everything looks fine, no report produced.

## Verification

- Every infrastructure component is inventoried.
- Findings are categorized by severity with remediation steps.
- No secrets are exposed in the report.
- Monitoring coverage gaps are identified.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/infrastructure-audit
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: infrastructure-audit
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/infrastructure-audit/raw -o .cursor/skills/infrastructure-audit/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/infrastructure-audit.md and install it as a project skill at skills/infrastructure-audit/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```