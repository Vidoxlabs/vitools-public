---
name: repo-scaffold
description: >-
  Scaffold missing configuration files and directories for a GitHub
  repository based on detected stack. Use when bootstrapping a new repo,
  adding CI/CD, editor config, community files, or standardizing
  cross-repository configuration.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: git
  tags: [git, devops, scaffolding, ci-cd, bootstrap]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: repo-scaffold
    summary: Scaffold missing config files for any GitHub repository
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Repository Scaffold

## When to use

Use this skill when bootstrapping a new repository, adding missing
configuration files to an incomplete repo, generating CI/CD workflows,
or standardizing cross-repository configuration.

## Procedure

1. List top-level files and directories to understand the project.
2. Read manifest files (`package.json`, `pyproject.toml`, `go.mod`,
   `Cargo.toml`) to detect the stack.
3. Read existing dotfiles (`.gitignore`, `.github/workflows/*`,
   `.editorconfig`) to avoid overwriting.
4. Determine: primary languages, build system, package manager, testing
   framework, linting tools, and CI requirements.
5. Present a scaffolding plan listing files to create and files to skip.
6. Generate only missing files. Never overwrite complete existing files.
7. Use exact test and lint commands from the detected stack — never
   invent alternatives.

## Guardrails

- No destructive overwrites. Only create missing files. Flag
  incomplete existing files for human review.
- Use exact CI commands from the detected stack. Never guess test or
  lint commands.
- Include contextual comments in generated YAML and JSON to explain
  non-obvious settings.
- For monorepos, create a root composite workflow and per-package
  configs only when missing.
- Always include AGENTS.md and a LICENSE when missing.

## Examples

### Good

> Skill detects `pyproject.toml` with `pytest` and `ruff`, reads
> existing `.gitignore` (complete), creates `.github/workflows/ci.yml`
> with the exact `pytest` and `ruff check` commands, adds
> `.editorconfig` and `CONTRIBUTING.md`, skips `.gitignore` since it
> already exists.

### Bad

> Skill creates a `ci.yml` with `npm test` for a Python project because
> it guessed the stack from the directory name instead of reading
> `pyproject.toml`.

## Verification

- Confirm no existing files were overwritten.
- Confirm generated CI commands match the detected testing and linting
  tools.
- Confirm all generated files are valid YAML or JSON.
- Run the generated CI workflow locally or in a dry-run to verify it
  parses.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/repo-scaffold
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: repo-scaffold
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/repo-scaffold/raw -o .cursor/skills/repo-scaffold/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/repo-scaffold.md and install it as a project skill at skills/repo-scaffold/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
