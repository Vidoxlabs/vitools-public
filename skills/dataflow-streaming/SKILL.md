---
name: dataflow-streaming
description: >-
  Streaming and batch data processing with Apache Beam and Dataflow. Windowing, triggers, and watermarks. Use when building unified pipelines that handle real-time and bounded data.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: data
  tags: [dataflow, apache-beam, streaming, windowing, watermarks]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: dataflow-streaming
    summary: Streaming and batch processing with Beam and Dataflow
  derived_from:
    - name: gcp-dataflow
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Dataflow Streaming

## When to use

Activate when building pipelines that process real-time or bounded data with Apache Beam on Dataflow.

## Procedure

1. Define the pipeline: read from source, apply transforms, write to sink.
2. Choose windowing: fixed, sliding, or session windows.
3. Set the watermark with withAllowedLateness for late data.
4. Configure triggers: watermark, processing-time, or custom.
5. Handle stream-to-batch unification.
6. Deploy: python pipeline.py --runner=DataflowRunner.
7. Monitor: Dataflow UI for lag, throughput, and errors.

## Guardrails

- Do not use global windows for unbounded data. The pipeline will never complete.
- Do not set allowed lateness too high without understanding state cost.
- Do not ignore backpressure. Configure autoscaling.
- Do not mix accumulative and discarding modes without intent.

## Examples

### Good

> Pipeline uses 5-minute fixed windows with 10-second allowed lateness, autoscaling enabled. Backlog stays flat.

### Bad

> Pipeline uses global window for a Pub/Sub stream. Window never fires, no output, state grows unbounded.

## Verification

- Pipeline produces output at the expected window cadence.
- Backlog metrics do not grow unbounded.
- Late data within allowed lateness is incorporated.
- Pipeline survives a worker restart without data loss.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/dataflow-streaming
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: dataflow-streaming
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/dataflow-streaming/raw -o .cursor/skills/dataflow-streaming/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/dataflow-streaming.md and install it as a project skill at skills/dataflow-streaming/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```