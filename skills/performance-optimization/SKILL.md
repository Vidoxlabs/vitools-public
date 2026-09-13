---
name: performance-optimization
description: >-
  Profile, identify bottlenecks, optimize, and verify measurable performance gains. Use when code is slow and a data-driven approach is needed to find and fix the cause.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: eval
  tags: [performance, profiling, optimization, benchmarks, bottlenecks]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: performance-optimization
    summary: Profile, optimize, and verify performance gains
  derived_from:
    - name: ce-optimize
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Performance Optimization

## When to use

Activate when code is measurably slow and guessing at the cause has not worked. Use when a feature misses latency targets or a batch job exceeds its time budget.

## Procedure

1. Establish a baseline benchmark. Record wall-clock time, memory, and CPU. Run multiple times for a stable median.
2. Profile the hot path with a profiler (cProfile, py-spy, perf, Chrome DevTools).
3. Rank bottlenecks by impact. Focus on the top one or two.
4. Form a hypothesis about the fix. Estimate the expected improvement.
5. Implement the change. Re-run the benchmark. Compare to baseline.
6. If the improvement is not measurable, revert.
7. Repeat for the next bottleneck.

## Guardrails

- Do not optimize without a benchmark. Unmeasured optimization is guesswork.
- Do not optimize speculative hot paths. Profile first, always.
- Do not trade correctness for speed. Tests must pass after every change.
- Do not micro-optimize before addressing the dominant bottleneck.

## Examples

### Good

> Baseline: 2.3s. Profile showed 80% of time in a nested loop. Replaced with a list join. New baseline: 0.4s. Tests pass. Improvement: 5.7x.

### Bad

> Guessed the database was slow, added a cache, measured no improvement, kept it. Real bottleneck was an N+1 query the profiler would have caught.

## Verification

- Before and after benchmarks are recorded with numbers.
- The improvement is at least 10% or meets the stated target.
- Tests pass after every optimization step.
- No speculative changes remain in the final diff.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/performance-optimization
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: performance-optimization
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/performance-optimization/raw -o .cursor/skills/performance-optimization/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/performance-optimization.md and install it as a project skill at skills/performance-optimization/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```