---
name: content-experimentation-best-practices
description: >-
  Content experimentation and A/B testing guidance covering experiment
  design, hypotheses, metrics, sample size, statistical foundations,
  and common analysis pitfalls. Use when planning experiments, setting
  up variants, choosing success metrics, or interpreting results.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: web
  tags: [web, experimentation, ab-testing, cms, analytics, statistics]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: content-experimentation-best-practices
    summary: Design and analyze content A/B experiments
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Content Experimentation Best Practices

## When to use

Activate when planning content experiments, setting up A/B variants,
choosing success metrics, interpreting statistical results, or
building experimentation workflows in a CMS or frontend stack.

## Procedure

1. Define the hypothesis: what change, what expected outcome, and
   what metric will prove or disprove it.
2. Calculate the required sample size based on the baseline
   conversion rate, minimum detectable effect, significance level
   (alpha), and power (1 - beta).
3. Set up variants: control (A) and treatment (B). Ensure random
   assignment and no cross-contamination.
4. Define primary and secondary metrics. Guardrail metrics should
   detect regressions (e.g., bounce rate, page load time).
5. Run the experiment until the sample size is reached. Do not peek
   at results early — it inflates false positives.
6. Analyze: compute the effect, confidence interval, and p-value.
   Check for segment-level differences.
7. Decide: ship, iterate, or kill. Document the result either way.

## Guardrails

- Do not run an experiment without a pre-registered hypothesis and
  sample size. Post-hoc rationalization invalidates results.
- Do not stop early because the result looks significant. Peeking
  inflates the false positive rate.
- Do not run too many variants at once. Multiple comparisons require
  correction.
- Do not ignore guardrail metrics. A win on the primary metric with
  a regression on a guardrail is not a ship.

## Examples

### Good

> Hypothesis: adding a customer testimonial below the CTA will
> increase click-through by 5%. Baseline CTR: 8%. MDE: 3%. Sample
> size: 12,000 per variant. Ran to completion. Result: 8.7% CTR
> (treatment) vs 8.1% (control). p=0.03, 95% CI [0.2%, 1.0%].
> Decision: ship.

### Bad

> "Let's try two different headlines and see which one does better."
> No hypothesis, no sample size, peeked at results after 2 days and
> declared a winner.

## Verification

- Hypothesis and sample size were pre-registered before launch.
- Experiment ran to the required sample size.
- Primary, secondary, and guardrail metrics are reported.
- Decision is documented with evidence.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/content-experimentation-best-practices
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: content-experimentation-best-practices
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/content-experimentation-best-practices/raw -o .cursor/skills/content-experimentation-best-practices/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/content-experimentation-best-practices.md and install it as a project skill at skills/content-experimentation-best-practices/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
