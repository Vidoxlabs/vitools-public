---
name: codebase-architect
description: >-
  Orchestrate systematic analysis of a codebase ecosystem: review
  repositories for quality, architecture, and best practices, then
  synthesize findings into actionable recommendations. Use when
  analyzing multiple repositories, planning architecture improvements,
  or standardizing cross-repo conventions.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: agents
  tags: [agents, architecture, analysis, code-review, ecosystem]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: codebase-architect
    summary: Systematic multi-repo codebase analysis and architecture
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Codebase Architect

## When to use

Use this skill when analyzing a codebase ecosystem across multiple
repositories. This includes full-ecosystem audits, specific repository
deep-dives, architecture planning, standardizing repository
descriptions, or technical debt remediation across repos.

## Procedure

1. Identify target repositories from the user request or default to
   all repositories in the organization.
2. For each repository, collect metadata: stars, forks, languages,
   license, contributor count, recent activity, and branch protection.
3. Analyze structure: directory layout, modularity, naming conventions,
   separation of concerns.
4. Assess code quality: long functions, deep nesting, large files,
   duplication, dead code, readability, documentation quality.
5. Validate best practices: security patterns, testing coverage, CI
   integration, linting, formatting, documentation completeness.
6. Evaluate architecture: dominant patterns, coupling, cohesion,
   scalability, maintainability, testability.
7. Analyze dependencies: version pinning, outdated packages, unused
   dependencies, lockfile health.
8. Synthesize findings into an executive summary, architecture
   recommendations, and a prioritized technical roadmap.

## Guardrails

- Every claim must be backed by repository content or verified research.
- Present high-level findings first, expand on request.
- All recommendations must include specific file paths, commands, or
  code snippets.
- Zero hallucination: if evidence is missing, state the uncertainty.
- Do not perform write operations without explicit authorization.

## Examples

### Good

> Analysis covers 5 repositories, identifies 3 critical security issues
> with file references, recommends a monorepo migration with a Mermaid
> dependency diagram, and provides a prioritized roadmap with effort
> estimates.

### Bad

> Analysis says "the codebase looks fine" without citing specific files,
> running any checks, or providing actionable recommendations.

## Verification

- Confirm every repository in scope was analyzed.
- Confirm findings include specific file paths and evidence.
- Confirm the roadmap is prioritized and includes effort estimates.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/codebase-architect
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: codebase-architect
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/codebase-architect/raw -o .cursor/skills/codebase-architect/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/codebase-architect.md and install it as a project skill at skills/codebase-architect/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
