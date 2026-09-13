---
name: onboarding-flow
description: >-
  Design guided onboarding flows for new users, team members, or agents. Install role-matched tools, connect services, and guide first steps. Use when building onboarding experiences.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: docs
  tags: [onboarding, setup, guided, first-run, welcome]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: onboarding-flow
    summary: Guided onboarding for new users or agents
  derived_from:
    - name: cowork-vibe-work-onboarding-setup
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Onboarding Flow

## When to use

Activate when designing an onboarding experience for new users, team members, or agents. Use when the first-run experience needs to be smooth and guided.

## Procedure

1. Identify the user persona: what role are they, what do they need on day one.
2. Define the critical path: the 3-5 steps a new user must complete to be productive.
3. Detect existing setup: check for existing config, tools, or accounts. Do not reinstall.
4. Guide each step with clear instructions: what to do, what to expect, how to verify.
5. Provide a trial run: let the user complete a small task to confirm setup works.
6. Surface next steps: what to explore after onboarding is complete.
7. Collect feedback: was the onboarding clear, what was missing.

## Guardrails

- Do not force re-installation of existing tools. Detect and skip.
- Do not overwhelm with options. Show the critical path first, advanced config later.
- Do not leave the user without a verification step. Confirm setup works.
- Do not skip the trial run. It catches setup issues before real work begins.

## Examples

### Good

> Onboarding detects existing tools, guides through 4 steps (connect, configure, test, explore), provides a trial task that verifies setup, and surfaces next steps. User completes in 5 minutes.

### Bad

> Onboarding dumps a 50-page README on the user with every possible config option. No guided path, no detection of existing setup, no trial run.

## Verification

- Existing tools are detected and not reinstalled.
- The critical path is 3-5 steps with clear instructions.
- A trial run verifies setup works.
- Next steps are surfaced after onboarding.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/onboarding-flow
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: onboarding-flow
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/onboarding-flow/raw -o .cursor/skills/onboarding-flow/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/onboarding-flow.md and install it as a project skill at skills/onboarding-flow/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```