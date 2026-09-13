---
name: plugin-scaffolding
description: >-
  Create and scaffold plugin directories with valid manifests, component directories, and marketplace wiring. Use when creating new plugins for agent platforms.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: automation
  tags: [plugin, scaffold, manifest, marketplace, component]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: plugin-scaffolding
    summary: Scaffold plugins for agent platforms
  derived_from:
    - name: cursor-create-plugin-scaffold-review-submission
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Plugin Scaffolding

## When to use

Activate when creating a new plugin for an agent platform (Cursor, Claude Code, Codex). Use when bootstrapping a plugin with a valid manifest and directory structure.

## Procedure

1. Choose the target platform: Cursor, Claude Code, Codex, or generic.
2. Create the plugin directory structure: skills/, agents/, rules/ as needed.
3. Write the manifest: plugin.json or equivalent with name, version, description, author.
4. Scaffold the entry skill or agent with a template SKILL.md or AGENT.md.
5. Add marketplace wiring: install paths, discovery config, and version tracking.
6. Validate the manifest against the platform's schema.
7. Test installation locally before submitting to the marketplace.

## Guardrails

- Do not hardcode absolute paths in the manifest. Use relative paths.
- Do not skip the validation step. Invalid manifests fail marketplace submission.
- Do not submit without local installation testing.
- Do not include secrets or credentials in the scaffold.

## Examples

### Good

> Created a Cursor plugin with plugin.json, skills/ directory, one template skill, marketplace wiring, and validated the manifest. Local install test passed.

### Bad

> Created a plugin directory with no manifest, no validation, submitted to marketplace. Rejected for invalid structure.

## Verification

- Plugin manifest validates against the platform schema.
- Directory structure matches the platform's expectations.
- Local installation test passes.
- No secrets or hardcoded paths in the scaffold.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/plugin-scaffolding
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: plugin-scaffolding
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/plugin-scaffolding/raw -o .cursor/skills/plugin-scaffolding/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/plugin-scaffolding.md and install it as a project skill at skills/plugin-scaffolding/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```