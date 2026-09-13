---
name: statistical-analysis
description: >-
  Apply statistical methods including descriptive stats, trend
  analysis, outlier detection, and hypothesis testing. Use when
  analyzing distributions, testing for significance, detecting
  anomalies, computing correlations, or interpreting results.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: data
  tags: [data, statistics, hypothesis-testing, distributions, scipy]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: statistical-analysis
    summary: Apply statistical methods with proper interpretation
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Statistical Analysis

## When to use

Activate when analyzing distributions, testing for statistical
significance, detecting anomalies or outliers, computing
correlations, or interpreting statistical results for stakeholders.

## Procedure

1. Identify the question: is this a comparison (A vs B), a
   distribution analysis, a correlation, or an anomaly detection?
2. Compute descriptive statistics: mean, median, standard deviation,
   quartiles, and sample size for each group.
3. Check assumptions: normality (Shapiro-Wilk), equal variance
   (Levene), and independence. Choose the test based on whether
   assumptions hold.
4. Apply the appropriate test: t-test for two-group comparison,
   ANOVA for three or more, Mann-Whitney for non-parametric,
   chi-square for categorical.
5. Report the test statistic, p-value, effect size, and confidence
   interval. State whether the result is significant at the chosen
   alpha level.
6. Interpret the result in context. Statistical significance does
   not imply practical significance.

## Guardrails

- Do not run a test without checking its assumptions. Using a
  parametric test on non-normal data produces invalid results.
- Do not report only the p-value. Include effect size and confidence
  interval.
- Do not interpret p > 0.05 as "no effect." It means insufficient
  evidence to reject the null, not proof of no effect.
- Do not run multiple comparisons without correction (Bonferroni,
  Tukey, or FDR).

## Examples

### Good

> Compared conversion rates for two landing page variants. Variant
> A: 12% (n=500), Variant B: 15% (n=500). Ran a two-proportion
> z-test: p=0.04, effect size h=0.09, 95% CI [0.1%, 5.9%]. Conclusion:
> statistically significant at alpha=0.05, but the effect size is
> small.

### Bad

> "The p-value was 0.03 so variant B is better." No effect size,
> no confidence interval, no assumption check, no context.

## Verification

- Assumptions for the chosen test were checked and documented.
- Test statistic, p-value, effect size, and confidence interval are
  all reported.
- The interpretation distinguishes statistical from practical
  significance.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/statistical-analysis
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: statistical-analysis
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/statistical-analysis/raw -o .cursor/skills/statistical-analysis/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/statistical-analysis.md and install it as a project skill at skills/statistical-analysis/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
