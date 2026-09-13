---
name: control-cli
description: >-
  Build or adapt a local harness to drive, inspect, and profile an
  interactive CLI or TUI without external services. Use for CLI UX
  checks, startup regressions, memory leaks, hangs, prompt flows, or
  terminal demos.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: automation
  tags: [automation, cli, tui, testing, profiling, harness]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: control-cli
    summary: Drive and inspect interactive CLIs with a local harness
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Control CLI

## When to use

Activate when you need to drive an interactive CLI or TUI
programmatically for testing, profiling, or demonstration. Use for
startup regression checks, prompt flow verification, memory leak
detection, or terminal-based UX testing.

## Procedure

1. Identify the CLI binary, its arguments, and the interactive prompts
   it presents.
2. Build a harness using `pty` (pseudo-terminal) or `pexpect` to spawn
   the CLI and drive its stdin.
3. For startup regression: measure time from spawn to first prompt.
   Compare against a baseline.
4. For prompt flow: send expected inputs and capture the response at
   each step. Verify the prompt sequence matches the expected flow.
5. For memory profiling: monitor RSS of the CLI process over time
   using `psutil` or `/proc/<pid>/status`.
6. For hangs: set a timeout on each interaction. If the CLI does not
   respond within the timeout, capture the state and report.
7. Produce a report with timing, memory, and flow results.

## Guardrails

- Do not use a real terminal for automated testing. Use `pty` or
  `pexpect` to ensure reproducibility.
- Do not assume prompt text is stable across versions. Capture and
  verify the actual prompt text.
- Do not skip the timeout. A hang without a timeout will block the
  harness indefinitely.
- Do not test against a production endpoint unless explicitly
  authorized.

## Examples

### Good

> Built a `pexpect` harness for `myapp init`. Drove the 5-step prompt
> flow, verified each response, measured startup at 1.2s (baseline
> 1.1s — within tolerance), and confirmed RSS stayed flat over 60s.

### Bad

> Manually typed inputs into the CLI and eyeballed the output. No
> timing, no memory check, no automation.

## Verification

- The harness drives the CLI without manual intervention.
- Timing results are recorded and compared against a baseline.
- Memory profile shows no unexpected growth.
- All prompt steps are verified against the expected flow.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/control-cli
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: control-cli
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/control-cli/raw -o .cursor/skills/control-cli/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/control-cli.md and install it as a project skill at skills/control-cli/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
