---
name: challenge-my-thinking
description: >-
  Stress-test a plan, proposal, or decision with Socratic questioning
  before sharing with stakeholders. Use when a decision needs to be
  validated before commitment.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: eval
  tags: [decision-making, socratic, review, validation, planning]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: challenge-my-thinking
    summary: Socratic stress-test for plans and decisions before commitment
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Challenge My Thinking

## When to use

Activate before committing to a plan, proposal, architecture decision,
or product direction. Use when the stakes of being wrong are high
enough that a blind spot could cost time, money, or trust.

## Procedure

1. State the plan or decision in one paragraph. Identify the core
   assumption on which everything else depends.
2. Ask: what would have to be true for this to be the wrong choice?
   List at least three failure scenarios.
3. For each scenario, assess how likely it is and what the blast
   radius would be if it occurred.
4. Identify the weakest link in the plan. What assumption, if
   invalidated, collapses the entire approach?
5. Steelman the strongest alternative you rejected. Restate it as
   charitably as possible and compare it to your plan on the same
   criteria.
6. Decide: proceed, adjust, or abandon. If proceeding, note which
   assumptions are load-bearing and should be monitored.

## Guardrails

- Do not skip the steelman step. If you cannot articulate why the
  best alternative is worse, you have not finished the analysis.
- Do not use this skill to manufacture doubt after a decision is
  already committed. It is a pre-commitment tool.
- Do not list trivial failure scenarios. Focus on plausible,
  high-impact ones.
- Do not conflate "no objections found" with "this is correct."

## Examples

### Good

> Plan: migrate to a new queue system. Core assumption: the new
> system handles our peak throughput. Failure scenario: it does not.
> Likelihood: moderate. Blast radius: full outage during peak.
> Weakest link: no load test has been run. Adjusted plan: run a load
> test before migration, proceed only if it passes.

### Bad

> Plan: migrate to a new queue system. Failure scenarios listed:
> "someone trips over a cable." Proceeded without testing peak
> throughput.

## Verification

- At least three plausible failure scenarios are documented.
- The strongest rejected alternative is restated charitably.
- The weakest link in the plan is explicitly named.
- The decision to proceed, adjust, or abandon is stated with
  reasoning.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/challenge-my-thinking
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: challenge-my-thinking
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/challenge-my-thinking/raw -o .cursor/skills/challenge-my-thinking/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/challenge-my-thinking.md and install it as a project skill at skills/challenge-my-thinking/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
