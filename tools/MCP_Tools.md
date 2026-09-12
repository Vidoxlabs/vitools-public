**MCP Tools = governed tool interfaces for agents.** This page tracks MCP servers, catalogs, deployment blueprints, and integration patterns that we mine into Vidoxlabs-native tool surfaces (typed schemas, explicit safety gates, repeatable deployment).

**Reference intake is now unified.** Add new MCP tool sources in **ViTools References** (Category = MCP Tools). Legacy MCP Tool reference DBs are in Archive (Legacy).

## What this contains

- **Canonical internal artifacts:** Internal Artifacts → By Type (filter Type = MCP Tool Spec)
- **Canonical reference intake:** References → MCP Tool Sources
- A curated database of **MCP tool references** (one row per repo/link/path/doc).
- Metadata to support fast evaluation and implementation:
    - **Vendor** (who maintains it)
    - **Artifact Type** (MCP server, tool catalog, template, deployment blueprint, docs, examples)
    - **Transport** (stdio / http+sse / websocket)
    - **Auth** (none / api-key / oauth / jwt)
    - **Topic / Tags** (security, deployment, open-webui, etc.)
    - **Status** (Inbox → Reviewing → Mined → Integrated → Archived)
    - **Review date** (when to revisit)

## How to use it (operating loop)

1. **Capture**: add a reference, set **Status = Inbox**.
2. **Review**: identify transport + auth model, security posture, and operational assumptions.
3. **Mine**: extract tool schemas, deployment patterns, and integration constraints.
4. **Integrate**: once implemented internally, set **Integrated** and link the internal implementation/spec.

## Conventions

- Store **subpaths** as their own rows when the unit of adoption is a specific server/package.
- Notes should record the **contract**: tool surface, auth, failure behavior, observability hooks, and deployment requirements.

---

MCP Tools Database