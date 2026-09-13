---
name: verify-this
description: >-
  Verify a claim with fresh local evidence: restate it falsifiably,
  capture baseline and treatment, compare artifacts, return VERIFIED,
  NOT VERIFIED, or INCONCLUSIVE. Use when a claim needs proof.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: eval
  tags: [verification, testing, evidence, claims, debugging]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: verify-this
    summary: Prove or disprove a claim with fresh local evidence
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Verify This

## When to use

Activate when someone makes a claim about system behavior,
performance, correctness, or configuration that needs to be confirmed
or refuted with evidence. Use when a decision depends on a factual
claim and you need proof rather than assertion.

## Procedure

1. Restate the claim as a falsifiable statement. Define what evidence
   would prove it true and what would prove it false.
2. Capture a baseline: the current state before any change. Record
   the exact command, output, version, timestamp, and environment.
3. Apply the treatment: make the change or run the test that the
   claim predicts will produce a specific outcome.
4. Capture the treatment result with the same command and format as
   the baseline.
5. Compare the two artifacts. Note whether the treatment result
   matches the claim's prediction.
6. Return one of three verdicts: VERIFIED, NOT VERIFIED, or
   INCONCLUSIVE.
7. Attach the baseline and treatment artifacts to the verdict.

## Guardrails

- Do not return VERIFIED without a captured artifact. A reasoning
  chain is not evidence.
- Do not reuse prior results as baseline. Capture fresh each time.
- Do not change more than one variable between baseline and treatment.
- Do not skip the falsifiability step. If you cannot state what would
  disprove the claim, you cannot verify it.

## Examples

### Good

> Claim: "The cache reduces query time by 50 percent." Baseline:
> query takes 200 ms without cache. Treatment: enable cache, same
> query takes 95 ms. Verdict: VERIFIED. Artifacts attached.

### Bad

> Claim: "The cache makes queries faster." Verdict: VERIFIED. No
> measurements captured, no baseline recorded.

## Verification

- The claim is restated as a falsifiable statement.
- Baseline and treatment artifacts are both captured and attached.
- The verdict is one of VERIFIED, NOT VERIFIED, or INCONCLUSIVE.
- Only one variable changed between baseline and treatment.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/verify-this
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: verify-this
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/verify-this/raw -o .cursor/skills/verify-this/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/verify-this.md and install it as a project skill at skills/verify-this/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
