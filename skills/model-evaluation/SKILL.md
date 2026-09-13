---
name: model-evaluation
description: >-
  Evaluate ML models with standardized metrics. Run benchmarks, compare models, and track performance over time. Use when assessing model quality or selecting between candidates.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: eval
  tags: [evaluation, ml, metrics, benchmarks, model-selection]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: model-evaluation
    summary: Standardized ML model evaluation and benchmarking
  derived_from:
    - name: hugging-face-evaluation
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Model Evaluation

## When to use

Activate when evaluating an ML model, comparing candidates, or tracking performance across versions.

## Procedure

1. Define the evaluation task and select metrics (accuracy, F1, BLEU, ROUGE, MRR).
2. Prepare the evaluation dataset. Hold it out from training.
3. Run inference with the model. Use same generation parameters across candidates.
4. Compute metrics with a standardized library.
5. Compare candidates in a table with statistical significance.
6. Record results with model version, dataset version, and timestamp.
7. Analyze failures: inspect worst-performing examples.

## Guardrails

- Do not evaluate on the training set. Verify the split is held out.
- Do not compare models with different generation parameters.
- Do not cherry-pick metrics. Report the full set.
- Do not skip statistical significance for small differences.

## Examples

### Good

> Two models evaluated on same held-out test set with identical parameters. Metrics table shows F1, precision, recall. Results saved to MLflow.

### Bad

> Model evaluated on training data. Only accuracy reported. Compared to another model with different temperature.

## Verification

- Evaluation dataset is documented and held out from training.
- All candidates use the same inference parameters.
- Results recorded with model version and timestamp.
- Failure analysis exists for worst examples.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/model-evaluation
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: model-evaluation
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/model-evaluation/raw -o .cursor/skills/model-evaluation/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/model-evaluation.md and install it as a project skill at skills/model-evaluation/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```