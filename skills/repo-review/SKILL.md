---
name: repo-review
description: >-
  Review a GitHub repository for code quality, best practices,
  security, architecture, documentation, and maintainability. Use
  when auditing a repo, evaluating a dependency, or improving code
  health across an organization.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: git
  tags: [git, code-review, audit, security, architecture, quality]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: repo-review
    summary: Structured repository review for quality, security, and architecture
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Repository Review

## When to use

Activate when reviewing a GitHub repository for quality, security,
architecture, or maintainability. Use when evaluating a dependency,
auditing a repo before adoption, or improving code health across an
organization.

## Procedure

1. Collect repository metadata: stars, forks, license, languages,
   contributor count, last commit date, and open issue/PR counts.
2. Analyze structure: directory layout, modularity, naming conventions,
   and separation of concerns.
3. Assess code quality: large files, long functions, duplication, dead
   code, and documentation coverage.
4. Check security: hardcoded credentials, dangerous patterns, missing
   `.gitignore` entries, and dependency vulnerabilities.
5. Evaluate testing: test presence, organization, coverage, and CI
   integration.
6. Review documentation: README completeness, API docs, inline docs,
   and contribution guides.
7. Evaluate architecture: patterns, coupling, cohesion, scalability,
   and maintainability.
8. Produce a report with findings categorized by severity (critical,
   high, medium, low) and actionable recommendations.

## Guardrails

- Every finding must include a specific file path and line reference.
- Do not report stylistic preferences as issues. Focus on correctness,
  security, and maintainability.
- Do not run destructive commands against the repository. Read-only
  analysis only.
- Prioritize security and reliability findings over style.

## Examples

### Good

> Report identifies 2 critical security issues (hardcoded API key in
> `config.ts:15`, no `.gitignore` for `.env`), 3 high issues (no
> tests, no CI, missing LICENSE), and 4 medium issues. Each has a
> file reference and a recommended fix.

### Bad

> Report says "the repo looks OK" with no specific findings, no file
> references, and no severity categorization.

## Verification

- Every finding has a file path and line reference.
- Findings are categorized by severity.
- Recommendations are specific and actionable.
- No destructive commands were run during the review.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/repo-review
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: repo-review
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/repo-review/raw -o .cursor/skills/repo-review/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/repo-review.md and install it as a project skill at skills/repo-review/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
