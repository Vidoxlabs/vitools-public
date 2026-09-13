---
name: gcp-data-pipelines
description: >-
  Build data pipelines on GCP: orchestration, scheduling, and monitoring with Cloud Composer and Dataflow. Use when designing or operating batch or streaming pipelines on Google Cloud.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: data
  tags: [gcp, data-pipeline, airflow, dataflow, orchestration]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: gcp-data-pipelines
    summary: Build and operate data pipelines on GCP
  derived_from:
    - name: gcp-data-pipelines
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# GCP Data Pipelines

## When to use

Activate when designing or operating data pipelines on GCP. Use when orchestrating batch or streaming workflows with Cloud Composer or Dataflow.

## Procedure

1. Define pipeline stages: extraction, transformation, loading, notification.
2. Choose orchestration: Cloud Composer for complex DAGs, Dataflow for unified batch/stream.
3. Write DAG or pipeline code with clear task IDs and explicit dependencies.
4. Set up scheduling: Airflow schedule_interval or Cloud Scheduler.
5. Configure monitoring: Cloud Logging, Cloud Monitoring, alerting policies.
6. Deploy and test with a small dataset.

## Guardrails

- Do not hardcode service credentials. Use Workload Identity.
- Do not skip idempotency. Pipeline re-runs must not duplicate data.
- Do not ignore backpressure in streaming pipelines.
- Do not deploy without alerting.

## Examples

### Good

> Airflow DAG with 5 tasks, retries set to 3, failure alerts on Slack. Dataflow pipeline uses autoscaling, processes 10 GB in 4 minutes.

### Bad

> Cron job with hardcoded credentials, no retries, no alerting. Reruns duplicate rows.

## Verification

- Pipeline produces correct output on a test dataset.
- Re-running does not duplicate data.
- Alerting fires on task failure.
- Logs are queryable in Cloud Logging.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/gcp-data-pipelines
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: gcp-data-pipelines
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/gcp-data-pipelines/raw -o .cursor/skills/gcp-data-pipelines/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/gcp-data-pipelines.md and install it as a project skill at skills/gcp-data-pipelines/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```