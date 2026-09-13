---
name: skills-template
description: >-
  Canonical formatting standard for Vidoxlabs skills. Defines required
  sections, frontmatter fields, and quality gates. Use when creating or
  rewriting a skill to ensure consistency and agent-consumability.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: docs
  tags: [skills, template, format]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: skills-template
    summary: Canonical formatting standard for Vidoxlabs skills
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Skills Formatting Standard

## When to use

Use this skill when creating a new skill file or when refactoring an
existing skill for consistency and portability. This standard ensures
every skill is scannable, agent-consumable, and passes the catalog
validation gate.

## Procedure

1. Start with the YAML frontmatter block. Set `name`, `description`,
   `license`, `version`, and the `metadata` block with all required
   fields.
2. Use the canonical section headings in order: When to use, Procedure,
   Guardrails, Examples, Verification, Install.
3. Write original prose for every section. Do not copy from vendor
   sources.
4. Ensure the Guardrails section has at least three rules.
5. Ensure the Examples section has both a good and a bad example.
6. Ensure the Verification section describes at least one concrete check.
7. Include the Install section with all four installation code blocks.
8. Set review dates in the frontmatter when promoting.

## Guardrails

- Do not promote a skill without Guardrails, Examples, and Verification
  sections.
- Keep the skill body in the markdown file. Use frontmatter properties
  for filtering and routing, not for content.
- Do not use emoji in skill body text.
- Do not reference internal hostnames, IP addresses, or private
  repository paths.

## Examples

### Good

> The skill uses canonical headings, has three guardrail rules, a good
> and bad example, a verification step, and the four install blocks. It
> passes the catalog builder without warnings.

### Bad

> The skill is a wall of text with no section headings, no guardrails,
> and no install instructions. The catalog builder fails validation.

## Verification

- Run the catalog builder against the skill file and confirm zero
  validation errors.
- Quick scan: can a person execute this skill without needing extra
  context?

## Install

Repository installers (`npx skills add`, Claude marketplace) are not advertised for this revision: they follow GitHub default `main`, which is not this curated set.

```bash
curl -fsSL https://vidoxlabs.dev/vitools/raw/skills/skills-template.md -o .cursor/skills/skills-template/SKILL.md
```

```text
Fetch https://vidoxlabs.dev/vitools/raw/skills/skills-template.md and install it as a project skill at skills/skills-template/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
