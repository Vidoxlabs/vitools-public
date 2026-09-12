**Plugins = agent tool surfaces.** This page tracks plugin ecosystems, registries, and templates we mine into Vidoxlabs-native tools (plugins, MCP servers, OpenAPI surfaces) with explicit safety gates and repeatable deployment.

**Reference intake is now unified.** Add new Plugin sources in **ViTools References** (Category = Plugins). Legacy Plugin reference DBs are in Archive (Legacy).

</aside>

## What this contains

- **Canonical internal artifacts:** Internal Artifacts → By Type (filter Type = Plugin Spec)
- **Canonical reference intake:** References → Plugin Sources
- A curated database of **plugin-related repos/paths** (one row per reference).
- Metadata for fast filtering and review:
    - **Vendor** (who maintains it)
    - **Artifact Type** (plugins repo, awesome list, community, official, template, subpath)
    - **Topic / Tags** (plugins, copilot, claude, codex, tooling)
    - **Status** (Inbox → Reviewing → Mined → Integrated → Archived)
    - **Review date** (when to revisit)

## How to use it (operating loop)

1. **Capture**: add a repo/path link, set **Status = Inbox**.
2. **Review**: identify the plugin model (OpenAPI/function-calling/MCP), auth patterns, and hosting assumptions.
3. **Mine**: extract schemas/manifests, tool definition conventions, and evaluation/testing approaches.
4. **Integrate**: once implemented internally, set **Integrated** and link the internal implementation.

## Conventions

- Store **subpaths** as their own rows when they represent a distinct plugin catalog.
- Notes should record the **contract**: input/output schema, auth, rate limits, and failure behavior.

---

Plugins Database