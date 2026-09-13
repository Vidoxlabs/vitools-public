---
name: agent-compatibility-check
description: >-
  Run a full compatibility pass on a repository for agent readiness: scanner score, startup path, validation loop, and docs reliability. Use when preparing a repo for agent-assisted development.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: eval
  tags: [agent, compatibility, readiness, validation, docs]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: agent-compatibility-check
    summary: Check repository readiness for agent-assisted development
  derived_from:
    - name: cursor-check-agent-compatibility
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Agent Compatibility Check

## When to use

Activate when evaluating whether a repository is ready for agent-assisted development. Use before onboarding a repo to an agent workflow.

## Procedure

1. Scan the repo structure: is there an AGENTS.md, clear entry points, and a build command?
2. Test the startup path: can an agent clone, install dependencies, and run the project?
3. Run the validation loop: does the test suite pass? Are there lint and type-check commands?
4. Check docs reliability: do README instructions work? Are they current?
5. Score each category: pass, partial, or fail.
6. Produce a report with the overall score and specific remediation steps.

## Guardrails

- Do not mark a repo as ready if the startup path fails. Fix it first.
- Do not skip the docs check. Stale docs mislead agents.
- Do not use a single subagent for all checks. Parallelize.
- Do not ignore partial scores. They indicate gaps that will cause issues.

## Examples

### Good

> Scanned repo: AGENTS.md present, startup path works (clone, npm install, npm test all pass), docs are current. Score: 4/4 pass. Ready for agent-assisted development.

### Bad

> Said the repo looks fine without running any checks. Agent later failed to install dependencies because the README had the wrong command.

## Verification

- All 4 categories are checked and scored.
- Startup path is verified by actually running it.
- Docs instructions are tested for accuracy.
- A report with remediation steps is produced.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/agent-compatibility-check
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: agent-compatibility-check
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/agent-compatibility-check/raw -o .cursor/skills/agent-compatibility-check/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/agent-compatibility-check.md and install it as a project skill at skills/agent-compatibility-check/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```