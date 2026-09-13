---
name: design-system-adherence
description: >-
  Enforce canonical visual consistency by requiring agents to consult a
  design system repository before producing any visual asset. Use when
  designing icons, logos, banners, social posts, or any branded visual
  that must match established design tokens and guidelines.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: design
  tags: [design, branding, visual, tokens, accessibility, consistency]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: design-system-adherence
    summary: Enforce design system consistency for visual assets
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Design System Adherence

## When to use

Use this skill when designing, generating, or refining visual assets
that must adhere to a design system. This includes icons, logos,
banners, social posts, agent avatars, illustrations, and any branded
visual output. Also use when a user asks to "match our style" or
"keep branding consistent."

## Procedure

1. Validate access to the design system repository. Run `git ls-remote`
   to confirm read access and check for canonical paths
   (`/foundations/color`, `/iconography/grid`, `/tokens/`).
2. Extract constraints into a machine-readable manifest (JSON or YAML):
   palette tokens, typography tokens, icon grid, stroke weight, corner
   radius, safe area, and export presets.
3. Record provenance: repo URL, branch, commit SHA, paths consulted,
   and timestamp.
4. Design within the system: keep shapes, line weights, visual density,
   and composition consistent with the repo's rules.
5. Verify accessibility: contrast ratios must meet WCAG AA (4.5:1 for
   normal text, 3:1 for large text). Verify readability at 200% scaling.
6. Generate outputs in requested formats and sizes per export presets.
7. Produce a consistency report with pass/fail checks for each
   acceptance criterion.

## Guardrails

- Do not invent new brand rules when canonical guidance exists.
- If the design system repo is inaccessible, do not proceed with final
  asset generation. Request access or ask for the relevant files.
- If the user requests a style that conflicts with the repo, propose a
  compliant alternative or document the exception with a rationale,
  approver, scope, and expiration date.
- Provenance metadata is required in every final deliverable.
- Keep outputs consistent across asset families within a set.

## Examples

### Good

> Agent validates repo access, extracts color and typography tokens,
> generates an icon set on a 24px grid with 2px stroke, exports SVG and
> PNG at 24/32/48px, attaches a constraints manifest and consistency
> report with all checks passing, including WCAG AA contrast.

### Bad

> Agent generates icons with mixed stroke weights (1px/2px/3px), no
> manifest, colors chosen by eye, no provenance, and no accessibility
> check. The assets cannot be validated against the design system.

## Verification

- Repo access validated: `git ls-remote` succeeded and canonical paths
  found.
- Provenance present: repo URL, branch, commit SHA, paths, timestamp.
- Constraints manifest present and complete.
- Token IDs referenced in the manifest exist at the recorded commit.
- Export sizes match the presets in the manifest.
- Color hex values in outputs are a subset of allowed token hex values.
- Contrast ratios meet WCAG AA.
- No stylistic drift within an asset family set.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/design-system-adherence
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: design-system-adherence
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/design-system-adherence/raw -o .cursor/skills/design-system-adherence/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/design-system-adherence.md and install it as a project skill at skills/design-system-adherence/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
