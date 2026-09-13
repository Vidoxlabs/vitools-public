---
name: data-loss-prevention
description: >-
  Halt before any command that causes irreversible data loss. Require
  explicit user consent. Use when running DROP, TRUNCATE, DELETE without
  WHERE, rm -rf, git reset --hard, or any destructive operation.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: safety
  tags: [safety, git, cloud, confirmation]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: data-loss-prevention
    summary: Halt and confirm before destructive commands
  derived_from:
    - name: google-accidental-data-loss-prevention
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Data Loss Prevention

## When to use

Use this skill before executing any command that produces irreversible
data loss. This includes but is not limited to:

- SQL: `DROP TABLE`, `DROP DATABASE`, `TRUNCATE`, `DELETE` without a
  `WHERE` clause or with `WHERE 1=1`.
- Filesystem: `rm -rf` targeting directories, `rm` without confirmation.
- Git: `git reset --hard`, `git push --force`, `git clean -fd`.
- Cloud: deleting storage buckets, destroying infrastructure resources,
  deleting secrets, or destroying encryption keys.
- Any command with a destructive flag that cannot be undone.

## Procedure

1. Halt. Do not execute the command.
2. Identify the scope of impact: what data is affected, whether it is
   recoverable, and what the blast radius is.
3. Explain the impact to the user. State what the command does, why it
   is being considered, and what the consequences are if it runs.
4. Request explicit consent. Ask the user to confirm they want to
   proceed.
5. Wait. Do not proceed until the user provides clear, affirmative
   consent in the conversation.
6. If consent is given, execute the command and report the result.
7. If consent is denied or unclear, do not execute. Propose a safer
   alternative if one exists.

## Guardrails

- Never execute a destructive command without explicit user consent.
- Prefer reversible operations over irreversible ones. If a reversible
  path exists, propose it first.
- Do not bundle multiple destructive operations into a single consent
  request. Each destructive action requires its own confirmation.
- Do not execute a destructive command based on assumed or implied
  consent. The user must say yes explicitly.

## Examples

### Good

> The user asked to remove a directory. The agent halted, explained
> that `rm -rf /data/project` will permanently delete the directory and
> all contents, noted that no backup exists, and asked for
> confirmation. The user confirmed. The agent executed the command and
> reported the result.

### Bad

> The agent encountered a table that needed to be dropped. It ran
> `DROP TABLE production_users` without asking, because the task
> description said to clean up old tables. The table was still in use.

## Verification

- Confirm the user provided affirmative consent before the command was
  executed.
- Confirm the command executed matches what the user consented to. If
  the user consented to `DROP TABLE staging_users`, do not run
  `DROP TABLE production_users`.
- After execution, confirm the result matches expectations. If
  something unexpected was deleted, report it immediately.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/data-loss-prevention
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: data-loss-prevention
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/data-loss-prevention/raw -o .cursor/skills/data-loss-prevention/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/data-loss-prevention.md and install it as a project skill at skills/data-loss-prevention/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
