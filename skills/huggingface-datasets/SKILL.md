---
name: huggingface-datasets
description: >-
  Create and manage datasets on Hugging Face Hub. Initialize repos, define configs, stream updates, and run SQL-based querying. Use when publishing or consuming datasets on the Hub.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: data
  tags: [huggingface, datasets, hub, streaming, sql]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: huggingface-datasets
    summary: Create and manage datasets on Hugging Face Hub
  derived_from:
    - name: hugging-face-datasets
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Hugging Face Datasets

## When to use

Activate when publishing a dataset to the Hugging Face Hub, consuming a dataset, or managing dataset versions.

## Procedure

1. Install: pip install datasets huggingface_hub. Authenticate with huggingface-cli login.
2. Initialize a dataset repo on the Hub.
3. Define the config in README.md with YAML frontmatter: configs, data_files, splits.
4. Load data: load_dataset("username/dataset-name"). Use streaming=True for large datasets.
5. Push updates: dataset.push_to_hub("username/dataset-name").
6. Query with SQL or filter and select for server-side filtering.

## Guardrails

- Do not publish datasets with PII without consent and documentation.
- Do not use a stale token. Re-authenticate if push fails with 401.
- Do not load large datasets into memory. Use streaming.
- Do not omit the dataset card. License and column docs are required.

## Examples

### Good

> Created a dataset repo with config, pushed 50k rows, card documents license and columns. Streaming works for consumers.

### Bad

> Uploaded a CSV with no config, no card, no license. Contains user email addresses.

## Verification

- load_dataset succeeds and returns expected splits.
- Dataset card is present with license, description, and column docs.
- Streaming works without loading full dataset into memory.
- No PII without consent documentation.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/huggingface-datasets
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: huggingface-datasets
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/huggingface-datasets/raw -o .cursor/skills/huggingface-datasets/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/huggingface-datasets.md and install it as a project skill at skills/huggingface-datasets/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```