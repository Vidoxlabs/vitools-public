# Design System Adherence — Visual Assets

Domain: Tools
Lifecycle: Intake
Owner: Vioxniv
Skill Type: Policy/Guardrail, Procedure
Source URL: https://github.com/Vidoxlabs/design_system
Version: v0.1

<aside>
🎨

This skill enforces **canonical visual consistency** by requiring agents to consult the design system repository before proposing or producing any visual asset.

</aside>

## Summary

- Ensures all visual assets (icons, logos, banners, social posts, images, agent profiles, etc.) adhere to canonical design standards.
- Primary source of truth: [https://github.com/Vidoxlabs/design_system](https://github.com/Vidoxlabs/design_system)

## When to Use (Triggers)

- Any request to **design, generate, or refine**:
    - Icons, logos, marks, badges
    - Banners, headers, thumbnails, social tiles
    - Agent avatars / profile images
    - Illustrations, diagrams, UI mock visuals
    - Brand visual exploration / ideation
- Any time a user asks for “match our style”, “consistent branding”, or similar.

## Inputs

- Asset request (purpose, platform, dimensions, format, constraints)
- Intended audience + context (internal/external)
- Existing asset(s) to match (if any)
- Repo path(s) consulted + specific guidance extracted (tokens, components, rules)
- **Constraints manifest** (required; JSON or YAML; included in every iteration + final package)
- **Provenance** (required; repo URL, branch, commit SHA, file paths consulted, timestamp; included in every deliverable)

## Outputs

- A design proposal (style-conformant) and/or generated visual asset(s)
- Explicit references to the **design-system constraints used** (what was followed)
- A short “consistency checklist” confirmation (see Automated Verification)

### **Provenance** (required in every deliverable)

**Format (JSON example):**

```json
{
  "repo_url": "https://github.com/Vidoxlabs/design_system",
  "branch": "main",
  "commit_sha": "abcdef1234567890abcdef1234567890abcdef12",
  "paths_consulted": [
    "/foundations/color",
    "/iconography/grid",
    "/tokens/"
  ],
  "timestamp_iso8601": "2026-06-06T06:43:57-04:00"
}
```

### **Constraints manifest** (required in every iteration + final asset package)

- Provide as `constraints-manifest.json` or `constraints-manifest.yaml` alongside the assets.
- The manifest must be included in every iteration (drafts/variants) and in the final asset package.

### **Consistency report** (required; one per asset family: icons, avatars, banners)

- Provide as `consistency-report.md` alongside the assets.

### **Exception** (required only when non-canonical output is approved)

- **Exception record fields (required):** rationale, stakeholder approver (name/email), scope, expiration date (ISO-8601).

## Procedure / Steps

1. **Locate canonical guidance in the design system repo**
    - **Validate repo access** (mandatory pre-flight)
        - Must perform an automated check for **read access** and **presence of canonical paths**:
            - `/foundations/color`
            - `/iconography/grid`
            - `/tokens/` (or equivalent; if different, record the discovered equivalent path in **Provenance**)
        - If the check fails: mark the task **Blocked** and present these fallback options (exactly three):
            - (a) request GitHub access
            - (b) request the relevant files pasted into the workspace
            - (c) request explicit permission to proceed with labeled assumptions
        - **Access-check snippet (CLI + HTTP examples):**

```bash
# CLI option (recommended)
git ls-remote https://github.com/Vidoxlabs/design_system.git HEAD

# If readable, perform a shallow clone (or equivalent) so paths can be validated
REPO_URL="https://github.com/Vidoxlabs/design_system.git"
BRANCH="main"
WORKDIR="$(mktemp -d)"
git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$WORKDIR/design_system"

# Confirm required canonical paths exist
test -d "$WORKDIR/design_system/foundations/color"
test -d "$WORKDIR/design_system/iconography/grid"
test -d "$WORKDIR/design_system/tokens" || echo "tokens missing; locate equivalent and record it"

# Capture commit SHA for provenance
(cd "$WORKDIR/design_system" && git rev-parse HEAD)
```

```bash
# Optional HTTP check (when git is unavailable)
curl -I https://raw.githubusercontent.com/Vidoxlabs/design_system/main/README.md
```

- Identify the relevant sections: brand, iconography, typography, color, spacing, layout, composition rules, export guidance, do/don’t examples.
- Prefer the most “canonical” / root docs (README, foundations, tokens) over ad-hoc examples.
1. **Extract constraints before creating**
    - Replace informal notes with a required **Constraints manifest** (machine-readable; JSON or YAML).
    - **Constraints manifest template (JSON example):**

```json
{
  "repo_url": "https://github.com/Vidoxlabs/design_system",
  "branch": "main",
  "commit_sha": "abcdef1234567890abcdef1234567890abcdef12",
  "timestamp_iso8601": "2026-06-06T06:43:57-04:00",
  "paths_consulted": [
    "/foundations/color",
    "/iconography/grid",
    "/tokens/"
  ],
  "palette_tokens": {
    "background": "color.bg.default",
    "foreground": "color.fg.default",
    "accent": "color.brand.primary",
    "accent_alt": "color.brand.secondary"
  },
  "typography_tokens": {
    "family": "type.family.sans",
    "scale": "type.scale.md",
    "weight_regular": "type.weight.regular",
    "weight_bold": "type.weight.bold"
  },
  "icon_grid": {
    "grid_px": 24,
    "keyline_px": 20,
    "padding_px": 2,
    "alignment": "pixel"
  },
  "stroke_weight": {
    "value_px": 2,
    "tolerance_px": 0.25
  },
  "corner_radius": {
    "value_px": 4,
    "tolerance_px": 0.5
  },
  "safe_area_px": 16,
  "export_presets": [
    {
      "name": "icon_svg",
      "format": "svg",
      "sizes_px": [24, 32, 48],
      "background": "transparent"
    },
    {
      "name": "banner_png",
      "format": "png",
      "sizes_px": [1200, 628],
      "background": "color.bg.default"
    }
  ]
}
```

- If guidance is missing or ambiguous: treat as **Blocked** and ask for clarification or propose an explicit assumption (clearly labeled) **only if the user selects fallback (c)**.
1. **Design within the system**
    - Keep shapes, line weights, visual density, and composition consistent with the repo’s rules.
    - Avoid novel styles that conflict with canonical guidance.
    - **Accessibility + localization checks (required while designing):**
        - Contrast ratio must meet **WCAG AA**:
            - Normal text: **≥ 4.5:1**
            - Large text (≥ 18pt regular or ≥ 14pt bold): **≥ 3:1**
        - Text scaling: verify readability and layout stability at **200%** scaling (where applicable).
        - RTL support (where applicable): confirm mirrored/layout-safe composition and directional iconography rules.
        - Record accessible color pairs used as **token IDs** in the consistency report; flag failures.
2. **Generate + iterate**
    - Produce outputs in the requested formats/sizes per `export_presets`.
    - Iterate using the same constraints; do not drift stylistically across revisions.
    - Each iteration must ship with:
        - updated **Constraints manifest**
        - updated **Provenance**
        - updated **Consistency report** (for the relevant asset family)
3. **Document what was followed**
    - Include a short “Design System references used” section (paths/filenames + key rules applied).
    - Include required **Provenance** in the exact metadata format (see Outputs).

## Guardrails

- Do **not** invent new brand rules when canonical guidance exists.
- If the design system repo cannot be accessed (no connection, permission, or missing files), **do not proceed** with final asset generation. Ask to connect GitHub or request the relevant files pasted into the workspace.
- If the user requests a style that conflicts with the repo, propose an alternative that complies, or explicitly document the exception as “non-canonical”.
- Keep outputs **consistent across asset families** (e.g., a set of icons must share the same grid, corner radius, stroke weight, and optical balance).
- **Provenance metadata is required in every final deliverable** (repo URL, branch, commit SHA, paths consulted, timestamp).

### CI / pre-commit integration idea (optional guidance)

Validate exported SVG/PNG against the constraints manifest and repo tokens:

- exported color hex ∈ token hex set for `commit_sha`
- stroke weight within tolerance
- icon grid alignment

Example command (pseudo):

```bash
node scripts/verify-design-assets.mjs \
  --manifest constraints-manifest.json \
  --assets ./exports \
  --report ./consistency-report.md
```

### **Exception** (non-canonical request handling)

- **Step A (required):** Offer a canonical-compliant alternative with 1–2 example variants.
- **Step B (only if user insists):** Require an **exception record** capturing:
    - rationale
    - stakeholder approver (name/email)
    - scope
    - expiration date (ISO-8601)
- If exception is approved, label outputs clearly as **Non-canonical (Exception)** and include the exception record in the deliverable.

## Examples

### Icons (asset family)

#### Good (annotated)

- Good #1: “24px grid; 2px stroke; uses `color.brand.primary`; padding matches grid; exports include SVG + 24/32/48 PNG; manifest + provenance attached.”
- Good #2: “Icon set of 6 items: consistent corner radius and optical balance; all fills/strokes match token hex list; contrast checks documented when placed on `color.bg.default`.”

#### Bad (annotated)

- Bad #1: “Mixed stroke weights (1px/2px/3px) across the set; no manifest; colors chosen by eye; cannot be validated.”
- Bad #2: “Uses an off-token gradient + drop shadow not present in design system; breaks consistency; no exception record.”

### Avatars (asset family)

#### Good (annotated)

- Good #1: “Avatar background uses `color.bg.default`; accent ring uses `color.brand.primary`; safe area respected; exports include 1x/2x; provenance includes commit SHA.”
- Good #2: “Batch of avatars share identical framing, lighting/contrast treatment, and typography token usage for initials; RTL-safe composition considered where initials appear.”

#### Bad (annotated)

- Bad #1: “Different framing and background treatments per avatar; inconsistent accent colors; no accessible contrast check for initials.”
- Bad #2: “Introduces new typography style for initials not defined in tokens; no exception record.”

### Banners (asset family)

#### Good (annotated)

- Good #1: “Uses canonical typography scale tokens; contrast verified at ≥ 4.5:1 for body text; exports include platform sizes; report includes hex + token IDs.”
- Good #2: “Variant A/B share layout system and spacing; only token-level changes between variants; constraints manifest updated each iteration.”

#### Bad (annotated)

- Bad #1: “Text overlays fail contrast ratio; no documented accessible color pairs; report omitted.”
- Bad #2: “One-off visual style drift between banner variants; inconsistent spacing; assets can’t be reproduced from tokens.”

## Automated Verification

- Acceptance criteria must be machine-checkable and tied to explicit token IDs / example values.
- Minimum acceptance criteria (include in each consistency report as pass/fail):
    - **Repo access validated:** `git ls-remote` succeeded and required paths found (`/foundations/color`, `/iconography/grid`, `/tokens/` or recorded equivalent).
    - **Provenance present:** `repo_url`, `branch`, `commit_sha`, `paths_consulted[]`, `timestamp_iso8601` present in deliverable metadata JSON.
    - **Constraints manifest present:** `palette_tokens`, `typography_tokens`, `icon_grid.grid_px`, `stroke_weight.value_px`, `corner_radius.value_px`, `safe_area_px`, `export_presets[]` present and non-empty.
    - **Token IDs valid:** every referenced token ID exists in the design-system tokens at `commit_sha`.
    - **Export sizes valid:** exported sizes match `export_presets[].sizes_px`.
    - **Color hex values valid:** extracted asset hex values are a subset of allowed hex values for the referenced color tokens at `commit_sha`.
    - **Stroke weight within tolerance:** detected stroke widths within `stroke_weight.value_px ± stroke_weight.tolerance_px`.
    - **Icon grid alignment:** viewBox/artboard aligns to `icon_grid.grid_px` and `icon_grid.padding_px` rules.
    - **Corner radius within tolerance:** radii match `corner_radius.value_px ± corner_radius.tolerance_px` where applicable.
    - **Accessibility:** contrast meets WCAG AA (≥ 4.5:1 normal, ≥ 3:1 large); text scaling at 200% verified where applicable; RTL behavior validated where applicable.
    - **No stylistic drift:** within an asset family set, the same manifest keys remain stable across variants unless explicitly changed and noted.

## Consistency report (template; required per asset family)

**Consistency Report — <asset_family>**

**Provenance (required)**

```json
{
  "repo_url": "https://github.com/Vidoxlabs/design_system",
  "branch": "main",
  "commit_sha": "abcdef1234567890abcdef1234567890abcdef12",
  "paths_consulted": [
    "/foundations/color",
    "/iconography/grid",
    "/tokens/"
  ],
  "timestamp_iso8601": "2026-06-06T06:43:57-04:00"
}
```

**Constraints manifest (required)**

- Attached: `constraints-manifest.json`

**Checks (pass/fail)**

- Repo access validated: PASS/FAIL
- Required paths present: PASS/FAIL
- Provenance complete: PASS/FAIL
- Manifest complete: PASS/FAIL
- Token IDs exist at commit: PASS/FAIL
- Export sizes match presets: PASS/FAIL
- Color hex values match tokens: PASS/FAIL
- Stroke weight within tolerance: PASS/FAIL
- Icon grid alignment: PASS/FAIL
- Corner radius within tolerance: PASS/FAIL
- Contrast (WCAG AA): PASS/FAIL
- Text scaling @ 200% (where applicable): PASS/FAIL
- RTL support (where applicable): PASS/FAIL

**Token IDs used**

- Colors:
    - `color.bg.default` → `#________`
    - `color.fg.default` → `#________`
    - `color.brand.primary` → `#________`
- Typography:
    - `type.family.sans`
    - `type.scale.md`
    - `type.weight.bold`
- Icon grid:
    - `icon.grid.24` (or equivalent token/path)

**Accessible color pairs used (token IDs)**

- Pair 1: `color.fg.default` on `color.bg.default` → contrast `___.__ : 1` (PASS/FAIL)

**Exports**

- Sizes produced: `___`
- Formats: `___`
- Filenames: `___`

**Failures / exceptions**

- List failures with remediation steps.
- If non-canonical: include **Exception record** (rationale, approver name/email, scope, expiration date).

## Sources / Evidence (Optional)

- [https://github.com/Vidoxlabs/design_system](https://github.com/Vidoxlabs/design_system)
- (Add specific file paths from the repo once known / validated)

## Example files (commit-ready)

**File: `constraints-manifest.example.json`**

```json
{
  "repo_url": "https://github.com/Vidoxlabs/design_system",
  "branch": "main",
  "commit_sha": "abcdef1234567890abcdef1234567890abcdef12",
  "timestamp_iso8601": "2026-06-06T06:43:57-04:00",
  "paths_consulted": [
    "/foundations/color",
    "/iconography/grid",
    "/tokens/"
  ],
  "palette_tokens": {
    "background": "color.bg.default",
    "foreground": "color.fg.default",
    "accent": "color.brand.primary",
    "accent_alt": "color.brand.secondary"
  },
  "typography_tokens": {
    "family": "type.family.sans",
    "scale": "type.scale.md",
    "weight_regular": "type.weight.regular",
    "weight_bold": "type.weight.bold"
  },
  "icon_grid": {
    "grid_px": 24,
    "keyline_px": 20,
    "padding_px": 2,
    "alignment": "pixel"
  },
  "stroke_weight": {
    "value_px": 2,
    "tolerance_px": 0.25
  },
  "corner_radius": {
    "value_px": 4,
    "tolerance_px": 0.5
  },
  "safe_area_px": 16,
  "export_presets": [
    {
      "name": "icon_svg",
      "format": "svg",
      "sizes_px": [24, 32, 48],
      "background": "transparent"
    },
    {
      "name": "avatar_png",
      "format": "png",
      "sizes_px": [256, 512],
      "background": "color.bg.default"
    },
    {
      "name": "banner_png",
      "format": "png",
      "sizes_px": [1200, 628],
      "background": "color.bg.default"
    }
  ]
}
```

**File: `consistency-report.example.md`**

```markdown
# Consistency Report — icons

## Provenance (required)
Provenance JSON:
{
  "repo_url": "https://github.com/Vidoxlabs/design_system",
  "branch": "main",
  "commit_sha": "abcdef1234567890abcdef1234567890abcdef12",
  "paths_consulted": [
    "/foundations/color",
    "/iconography/grid",
    "/tokens/"
  ],
  "timestamp_iso8601": "2026-06-06T06:43:57-04:00"
}

## Constraints manifest (required)
- Attached: `constraints-manifest.json`
- Icon grid: 24px (keyline 20px, padding 2px)
- Stroke weight: 2px ± 0.25px
- Corner radius: 4px ± 0.5px
- Export presets: icon_svg (24/32/48)

## Checks (pass/fail)
- Repo access validated: PASS
- Required paths present: PASS
- Provenance complete: PASS
- Manifest complete: PASS
- Token IDs exist at commit: PASS
- Export sizes match presets: PASS
- Color hex values match tokens: FAIL (found non-token color `#00FFAA`)
- Stroke weight within tolerance: PASS
- Icon grid alignment: PASS
- Corner radius within tolerance: PASS
- Contrast (WCAG AA): PASS
- Text scaling @ 200% (where applicable): N/A
- RTL support (where applicable): N/A

## Token IDs used
### Colors
- `color.bg.default` → `#0B0D12`
- `color.fg.default` → `#E9ECF2`
- `color.brand.primary` → `#6C5CE7`

### Typography
- N/A (icons)

### Icon grid
- `icon.grid.24` (equivalent)

## Accessible color pairs used (token IDs)
- `color.fg.default` on `color.bg.default` → contrast `12.1:1` (PASS)

## Exports
- Sizes produced: 24, 32, 48
- Formats: svg, png
- Filenames:
  - `exports/icons/search_24.svg`
  - `exports/icons/search_32.png`
  - `exports/icons/search_48.png`

## Failures / remediation
- FAIL: Non-token color detected (`#00FFAA`) in `exports/icons/search_24.svg`
  - Fix: replace with token-mapped hex for `color.brand.primary` and re-export.
```

## Runbook (access check + report generation)

1. Run the pre-flight access check (`git ls-remote …`), then shallow-clone (or equivalent) and validate required paths exist.
2. Capture and record **branch** and **commit SHA**, plus **paths consulted** and **timestamp** in **Provenance** JSON.
3. Create/update `constraints-manifest.json` for the asset family, then generate assets using only the manifest tokens/presets.
4. Run the verification routine to populate `consistency-report.md` with pass/fail checks, token IDs, hex values, and export sizes; attach it with the assets.