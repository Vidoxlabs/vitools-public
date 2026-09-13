---
name: skill-creation
description: >-
  Interactively create a new skill from scratch: gather requirements, define triggers, write the procedure, add guardrails, examples, and verification. Use when building a new skill interactively.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: automation
  tags: [skill, creation, interactive, scaffold, authoring]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: skill-creation
    summary: Interactively create new skills from scratch
  derived_from:
    - name: grok-create-skill-help
      license: MIT
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Skill Creation

## When to use

Activate when a user wants to create a new skill from scratch. Use when interactively building a skill with proper structure and all required sections.

## Procedure

1. Ask the user what the skill should do and when it should activate.
2. Draft the frontmatter: name, description with trigger phrases, category, tags.
3. Write the body sections: When to use, Procedure, Guardrails, Examples, Verification, Install.
4. Review with the user: does the procedure match their intent? Are the guardrails correct?
5. Save to skills/<slug>/SKILL.md.
6. Run the catalog builder and legal gate to validate.
7. Report the result.

## Guardrails

- Do not create a skill without understanding the user's intent. Ask questions.
- Do not skip the review step. The user must confirm the content.
- Do not omit any required section. All 7 are mandatory.
- Do not save without passing the legal gate.

## Examples

### Good

> Asked the user 3 questions about intent, drafted frontmatter and body, reviewed together (user refined 2 guardrails), saved, passed legal gate. Skill is in the catalog.

### Bad

> Generated a skill from a one-line prompt with no questions asked, no review, no validation. Skill is missing 3 required sections.

## Verification

- User intent is confirmed through questions before drafting.
- All 7 required sections are present.
- User reviewed and approved the content.
- Legal gate passes.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/skill-creation
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: skill-creation
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/skill-creation/raw -o .cursor/skills/skill-creation/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/skill-creation.md and install it as a project skill at skills/skill-creation/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```