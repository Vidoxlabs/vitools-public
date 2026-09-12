---
name: repo-scaffold
description: Scaffold missing dot-directories and configuration files for any GitHub repository with Vidoxlabs conventions always applied. Activate when bootstrapping a new repo, adding AGENTS.md and .plans/ structure, generating CI/CD workflows, or standardizing cross-repository configuration.
---

# Repository Scaffold

Scaffold all **missing** dot-directories and configuration files for a GitHub repository.
Vidoxlabs ecosystem conventions (AGENTS.md + `.plans/` skeleton) are **always** applied.

Complements read-only `repo-review` with a write-capable bootstrap workflow.

## When to use

- Bootstrapping a new or incomplete repository
- Adding Vidoxlabs cross-repository standardization (AGENTS.md, `.plans/`)
- Generating CI/CD, editor config, community files from detected stack
- Preparing a repo for agent-compatibility scoring

## Preparation — Discover project identity

1. List top-level files and directories.
2. Read manifest files: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`.
3. Read existing dotfiles: `.gitignore`, `.github/workflows/*`, `.editorconfig`, `AGENTS.md`.
4. Determine:
   - Primary language(s) and frameworks
   - Build system and package manager
   - Testing framework and **exact** commands (from scripts/Makefile)
   - Linting/formatting tools and config paths
   - Existing dot directories (do not overwrite complete files)
5. Detect monorepo signals: `workspaces`, `pnpm-workspace.yaml`, `go.work`.

When on v37-dev with CLI access, prefer:

```bash
vilabs vicode scaffold --root . --dry-run
```

## Plan gate (required before generating files)

Output `## Scaffolding Plan` with:

- Detected languages and frameworks
- Build system and package manager
- Testing framework and exact commands
- Linter/formatter and config paths
- CI/CD requirements
- Missing categories from checklist (see `references/checklist.md`)
- Files to create (with rationale) — exclude complete existing files
- Files to skip

**Do not generate file content until the plan is presented.**

## Checklist layers

| Layer | Targets |
| ----- | ------- |
| 1. Repo Metadata | `.github/ISSUE_TEMPLATE/`, PR template, SECURITY.md, CONTRIBUTING.md |
| 2. Dev Environment | `.devcontainer/`, `.vscode/`, `.editorconfig` |
| 3. Code Quality | `.gitignore`, `.gitattributes`, linter configs |
| 4. CI/CD | `.github/workflows/ci.yml`, Dockerfile (when applicable) |
| 5. License | `LICENSE`, `NOTICE` |
| 6. Vidoxlabs (always) | `AGENTS.md`, `.plans/{README,NAVIGATION,INDEX,templates/*}` |

## Generation rules

- **No destructive overwrites** — only create missing files; flag incomplete for human review
- **Exact CI commands** — use discovered test/lint commands, never invent alternatives
- **Vidoxlabs layer 6 always** — include AGENTS.md and `.plans/` skeleton when missing
- **Placeholders** — `[REPO_OWNER]`, `[CURRENT_YEAR]`, `[MAINTAINER]` when metadata unavailable
- **Contextual comments** — explain non-obvious settings in generated YAML/JSON
- **Monorepo** — root composite workflow; per-package configs only when missing

## Output format

Prefer JSON envelope:

```json
{
  "scaffolding_plan": { "detected_stack": {}, "files_to_create": [], "files_to_skip": [], "manual_steps": [] },
  "proposals": [{ "path": ".github/workflows/ci.yml", "action": "create", "content": "..." }],
  "setup_md": "# Scaffold Setup\n..."
}
```

Fallback: fenced blocks with explicit paths:

```markdown
### .github/workflows/ci.yml
```yaml
content
```
```

## Verification

After scaffolding:

```bash
# On v37-dev LXC
v37-workspace-validate

# Via CLI
vilabs vicode scaffold --root . --verify
```

Run agent-compatibility pass to score repository readiness.

## References

- [checklist.md](references/checklist.md) — full file checklist
- [AGENTS.md Quick Start](../../../../AGENTS.md) — ecosystem conventions
- [Universal Scaffold Spec](../../../../.plans/projects/repo-scaffolding/2026-07-08-universal-scaffold-spec.md)
