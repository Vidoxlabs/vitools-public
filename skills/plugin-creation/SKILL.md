---
name: plugin-creation
description: >-
  Create and scaffold plugin directories for agent platforms with valid manifests, component directories, and marketplace entries. Use when building a new plugin for an agent ecosystem.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: automation
  tags: [plugin, creation, scaffold, manifest, marketplace]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: plugin-creation
    summary: Create plugins for agent platforms
  derived_from:
    - name: openai-codex-plugin-creator-hatch-pet
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Plugin Creation

## When to use

Activate when creating a new plugin for an agent platform. Use when scaffolding a plugin with the correct manifest, directory structure, and marketplace entry.

## Procedure

1. Identify the target platform and its plugin format (plugin.json, manifest, directory structure).
2. Create the plugin directory with the required structure: skills/, agents/, rules/ as needed.
3. Write the manifest with name, version, description, author, and capabilities.
4. Scaffold the entry skill or agent with a template.
5. Add marketplace entry: install path, discovery config, version tracking.
6. Validate the manifest against the platform schema.
7. Test installation locally: does the plugin load and function?

## Guardrails

- Do not hardcode absolute paths in the manifest.
- Do not skip manifest validation. Invalid manifests are rejected.
- Do not include secrets or credentials in the plugin scaffold.
- Do not submit to the marketplace without local testing.

## Examples

### Good

> Created a plugin for an agent platform: manifest validates, directory structure matches, entry skill works, local install test passes. Ready for marketplace submission.

### Bad

> Created a plugin with no manifest, no validation, no testing. Marketplace rejects it.

## Verification

- Plugin manifest validates against the platform schema.
- Directory structure matches platform expectations.
- Local installation test passes.
- No secrets or hardcoded paths in the scaffold.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/plugin-creation
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: plugin-creation
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/plugin-creation/raw -o .cursor/skills/plugin-creation/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/plugin-creation.md and install it as a project skill at skills/plugin-creation/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```