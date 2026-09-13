---
name: skills-reviewer
description: >-
  Validate that a skill follows the required format and conventions.
  Check frontmatter, required sections, license, and content quality.
  Use when reviewing a skill before promotion or auditing skill quality.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: eval
  tags: [eval, skills, review, validation, quality, format]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: skills-reviewer
    summary: Validate skills against required format and conventions
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Skills Reviewer

## When to use

Activate when you need to validate that a skill follows the required
format and conventions. Use before promoting a skill, during skill
audits, or when a contributor asks "is this skill ready?"

## Procedure

1. Read the SKILL.md file and extract the frontmatter.
2. Verify required frontmatter fields: `name` (kebab-case, matches
   directory), `description` (with trigger phrases), `license: MIT`,
   `version`, `metadata.kind`, `metadata.status`, `metadata.origin`,
   `metadata.category` (from controlled vocabulary), `metadata.tags`,
   `metadata.platforms`.
3. Verify required body sections: `# Title`, `## When to use`,
   `## Procedure`, `## Guardrails`, `## Examples` (with Good and Bad),
   `## Verification`, `## Install` (with 4 code blocks).
4. Check content quality: guardrails have at least 3 rules, examples
   have both good and bad, verification describes a concrete check.
5. Check for prohibited content: vendor branding, internal IPs,
  private repo paths, emoji.
6. Produce a pass/fail report listing each check and its result.

## Guardrails

- Do not pass a skill with missing required sections. Each must be
  present.
- Do not pass a skill with a `name` that does not match the directory
  slug.
- Do not pass a skill with `claude` or `anthropic` in the name field.
- Do not pass a skill with `status: promoted` that is missing any
  required section.

## Examples

### Good

> Review of `data-loss-prevention`: all frontmatter fields present,
> all 7 body sections present, guardrails has 4 rules, examples has
> Good and Bad, verification has 3 concrete checks. No prohibited
> content. Result: PASS.

### Bad

> Review of `my-skill`: "looks good." No checklist, no specific
> findings, no pass/fail verdict.

## Verification

- Every frontmatter field was checked.
- Every required section was verified present.
- Content quality checks were run.
- A pass/fail verdict was produced with specific findings.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/skills-reviewer
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: skills-reviewer
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/skills-reviewer/raw -o .cursor/skills/skills-reviewer/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/skills-reviewer.md and install it as a project skill at skills/skills-reviewer/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
