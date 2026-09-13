---
name: cli-for-agents
description: >-
  Design or review CLIs so coding agents can run them reliably:
  non-interactive flags, layered help with examples, stdin pipelines,
  fast actionable errors, idempotency, dry-run. Use when building a
  CLI for agent use.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: automation
  tags: [cli, developer-tools, agents, dx, automation]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: cli-for-agents
    summary: Design CLIs that coding agents can call reliably and parse
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# CLI for Agents

## When to use

Activate when designing a new CLI, adding commands to an existing one,
or reviewing a CLI for agent compatibility. Use when the CLI will be
invoked by automated agents rather than, or in addition to, human
users.

## Procedure

1. Audit every interactive prompt. Replace each with a flag or
   config file equivalent. No command path should require human input
   to complete.
2. Provide `--help` at every level: top-level, per-subcommand, and
   per-flag. Include at least one usage example in each help block.
3. Ensure all output that an agent needs to parse goes to stdout in a
   structured format (JSON or machine-readable text). Human-readable
   messaging goes to stderr.
4. Make errors actionable: include the command that failed, the
   exit code, and a one-line fix suggestion.
5. Support `--dry-run` for any mutating command.
6. Ensure idempotency: running the same command twice produces the
   same result without error on the second run.
7. Verify non-zero exit codes for failure and zero for success.

## Guardrails

- Do not require a TTY or terminal width detection for any command an
  agent would run.
- Do not emit color codes or progress spinners to stdout. Gate all
  formatting behind `--tty` or `--color` flags.
- Do not return exit 0 when the operation failed. Agents rely on
  exit codes.
- Do not bury error details in a log file without surfacing the path
  in stderr.

## Examples

### Good

> `deploy --env staging --dry-run` prints the planned changes as
> JSON to stdout and exits 0. Without `--dry-run`, it deploys and
> prints the deployment ID. A failure prints "deploy failed: auth
> token expired. Run `auth refresh` and retry." to stderr with exit 1.

### Bad

> `deploy` prompts "Which environment? (staging/prod)" and waits for
> stdin. No `--env` flag exists. The agent hangs until timeout.

## Verification

- Every command completes without interactive input when all
  required flags are provided.
- `--help` exists at top level and for each subcommand.
- Mutating commands support `--dry-run`.
- Failures produce non-zero exit codes with actionable stderr messages.
- Running the same command twice does not error on the second run.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/cli-for-agents
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: cli-for-agents
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/cli-for-agents/raw -o .cursor/skills/cli-for-agents/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/cli-for-agents.md and install it as a project skill at skills/cli-for-agents/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
