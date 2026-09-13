---
name: skill-mining
description: >-
  Mine external skill repositories into Vidoxlabs-native skills. Use when
  adding or converting a reference skill into a first-party Vidoxlabs
  skill with original prose and canonical structure.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: docs
  tags: [skills, mining, intake]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: skill-mining
    summary: Mine external repos into Vidoxlabs-native skills
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Skill Mining From Repos

## When to use

Use this skill when adding a new external skill repository to the
Vidoxlabs catalog or when converting a reference skill into a first-party
Vidoxlabs skill. Also use when reviewing an external skill for potential
intake.

## Procedure

1. Capture the external reference in the catalog inventory with status
   set to reviewing.
2. Review the external skill and extract only the concept: intent,
   triggers, procedural steps, guardrails, and verification approach.
3. Create a new skill file using the canonical template with original
   Vidoxlabs prose. Do not copy body text from the source.
4. Record the external reference in the frontmatter using the
   `derived_from` field when the concept originates from a vendor skill.
5. Keep the skill scoped and agent-agnostic unless it is explicitly
   agent-specific.
6. Run the legal gate to confirm no vendor body text was carried over.
7. Set lifecycle to promoted only after guardrails, examples, and
   verification sections are complete.

## Guardrails

- Do not import vendor-specific assumptions without documenting the
  constraints.
- Do not copy large blobs of text from the source. Extract the reusable
  pattern and rewrite it in original prose.
- Never publish vendored body text as first-party content.
- If the source lacks a clear license, do not derive from it until the
  license is confirmed.

## Examples

### Good

> Reviewed an external skill repo, extracted the 10-step workflow and
> guardrails, wrote original prose with Vidoxlabs framing, linked the
> source via `derived_from`, and passed the legal gate.

### Bad

> Copied the README content wholesale with no internal framing, no
> guardrails, and no verification section.

## Verification

- Confirm the skill can be followed as written without needing the
  original repository open.
- Run the legal gate check on the new skill file.
- Verify that all required sections are present: when to use, procedure,
  guardrails, examples, verification, install.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/skill-mining
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: skill-mining
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/skill-mining/raw -o .cursor/skills/skill-mining/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/skill-mining.md and install it as a project skill at skills/skill-mining/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
