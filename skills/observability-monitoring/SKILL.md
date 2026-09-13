---
name: observability-monitoring
description: >-
  Monitor system health with logs, metrics, traces, and SLOs. Set up dashboards, alerting, and service health checks. Use when establishing observability for a service or diagnosing performance issues.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: infra
  tags: [observability, logging, metrics, traces, slo, dashboards]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: observability-monitoring
    summary: System health monitoring with logs, metrics, and SLOs
  derived_from:
    - name: elastic-observability-logs-slos-edot
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Observability Monitoring

## When to use

Activate when establishing observability for a new service, setting up SLOs, or diagnosing performance issues through logs and metrics.

## Procedure

1. Define service-level indicators (SLIs): latency, error rate, throughput, saturation.
2. Set SLO targets for each SLI (e.g., 99.9% of requests under 200ms).
3. Configure log ingestion: structured logs with correlation IDs, severity levels, and service tags.
4. Set up metrics dashboards: latency percentiles, error rates, queue depth, resource utilization.
5. Configure distributed tracing for request-level visibility across services.
6. Create alerts for SLO burn rate, error budget exhaustion, and anomaly detection.
7. Define runbooks for each alert with diagnostic steps and remediation.

## Guardrails

- Do not alert on raw metrics. Alert on SLO burn rate or error budget.
- Do not log sensitive data (PII, credentials, tokens) in plaintext.
- Do not create dashboards nobody reads. Wire them to on-call workflows.
- Do not skip runbooks. An alert without a runbook is noise.

## Examples

### Good

> Set up 4 SLIs with SLO targets, structured logging with correlation IDs, Grafana dashboards for latency and errors, distributed tracing, burn-rate alerts, and runbooks linked to each alert.

### Bad

> Enabled debug logging on all services, created a dashboard with 50 panels nobody looks at, no SLOs, alerts fire on raw CPU usage.

## Verification

- SLIs and SLOs are defined and documented.
- Logs are structured and do not contain sensitive data.
- Dashboards are linked to on-call workflows.
- Every alert has a runbook with diagnostic steps.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/observability-monitoring
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: observability-monitoring
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/observability-monitoring/raw -o .cursor/skills/observability-monitoring/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/observability-monitoring.md and install it as a project skill at skills/observability-monitoring/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```