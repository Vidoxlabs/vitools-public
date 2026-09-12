# Repository Scaffolding Checklist

Universal layers plus Vidoxlabs layer 6 (always applied).

## Layer 1 — Repo Metadata & Community

- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `.github/ISSUE_TEMPLATE/feature_request.yml`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/CODEOWNERS` (optional)
- `.github/FUNDING.yml` (optional)
- `.github/SECURITY.md`
- `CONTRIBUTING.md`

## Layer 2 — Development Environment

- `.devcontainer/devcontainer.json` (optional)
- `.vscode/settings.json`
- `.vscode/extensions.json`
- `.vscode/launch.json` (optional)
- `.vscode/tasks.json` (optional)
- `.editorconfig`

## Layer 3 — Code Quality & Style

- `.gitignore`
- `.gitattributes`
- Language-specific linter configs (`.eslintrc.json`, `ruff.toml`, `.golangci.yml`, etc.)

## Layer 4 — CI/CD & Automation

- `.github/workflows/ci.yml`
- `.github/workflows/release.yml` (optional)
- `Dockerfile` (optional)
- `docker-compose.yml` (optional)
- `Makefile` (optional)

## Layer 5 — License & Legal

- `LICENSE`
- `NOTICE` (optional)

## Layer 6 — Vidoxlabs (always applied)

- `AGENTS.md`
- `.plans/README.md`
- `.plans/NAVIGATION.md`
- `.plans/INDEX.md`
- `.plans/templates/plan-template.md`
- `.plans/templates/decision-template.md`
- `.plans/templates/spec-template.md`
- `.plans/templates/task-template.md`
- `.plans/superpowers/plans/YYYY/MM/DD/initial.md`

## Overwrite policy

| Status | Action |
| ------ | ------ |
| Missing | `create` |
| Exists but incomplete (< 32 bytes or stub) | `update` (flag for review) |
| Exists and complete | `skip` — never overwrite |
