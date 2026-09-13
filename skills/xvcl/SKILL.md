---
name: xvcl
description: >-
  Extend Fastly VCL with loops, functions, constants, macros, and
  conditionals using XVCL — a VCL transpiler that compiles .xvcl files
  into standard VCL. Use when writing any Fastly VCL configuration,
  reducing VCL code duplication, or splitting large VCL into modular
  includes.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: cloud
  tags: [cloud, fastly, vcl, cdn, metaprogramming]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: xvcl
    summary: VCL transpiler with metaprogramming for Fastly
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Writing VCL with XVCL

## When to use

Use this skill when writing VCL for Fastly and needing metaprogramming
features: loops for repetitive backends or routing rules, compile-time
constants instead of magic numbers, reusable functions with return
values, or modular includes. Also use when writing and testing VCL
locally.

## Procedure

1. Write `.xvcl` files using XVCL directives: `#const` for constants,
   `#for` for loops, `#def` for functions, `#if` for conditionals,
   `#inline` for macros, `#include` for modular files.
2. Compile to standard VCL: `uvx xvcl main.xvcl -o main.vcl`.
3. Lint the output: `falco lint main.vcl`.
4. Run locally: `falco simulate main.vcl` (listens on `localhost:3124`).
5. Test with `curl http://localhost:3124/` to verify behavior.

## Guardrails

- Always use `{{NAME}}` template syntax to emit constant values. A bare
  constant name in VCL passes through as a literal string and produces
  invalid VCL.
- Use `F_` prefixed backend names (e.g., `F_origin`). Fastly VCL
  requires this prefix. Never use `backend default`.
- Prefer populating VCL `table` declarations with `#for` loops over
  generating inline if-chains. Tables give O(1) lookups.
- Every VCL subroutine needs `#FASTLY recv` (or the appropriate name) at
  the top.
- Vary header must be set in `vcl_fetch`, not `vcl_deliver`. Setting it
  in deliver is too late — the object is already cached.

## Examples

### Good

> Developer uses `#const REGIONS = [("us", "us.example.com"), ("eu",
> "eu.example.com")]` and a `#for` loop to generate backends. Compiles
> to clean VCL with no duplication. Tests with `falco simulate`.

### Bad

> Developer writes 20 identical `if` statements for URL redirects
> instead of using a `table` populated with `#for`. The VCL is O(n) and
> hard to maintain.

## Verification

- Compile succeeds with no errors.
- `falco lint` passes.
- `falco simulate` runs and responds to test requests.
- No bare constant names in the output VCL.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/xvcl
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: xvcl
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/xvcl/raw -o .cursor/skills/xvcl/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/xvcl.md and install it as a project skill at skills/xvcl/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
