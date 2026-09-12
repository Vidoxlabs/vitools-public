**Cookbooks = external implementation references.** This page collects high-signal repositories and guides (examples, patterns, prompt techniques, agent scaffolds) that we mine into Vidoxlabs-native skills/plugins/agents.

**Reference intake is now unified.** Add new Cookbook references in **ViTools References** (Category = Cookbooks). Legacy Cookbooks reference DBs are in Archive (Legacy).

</aside>

## What this contains

- **Canonical intake database:** References → Cookbooks
- A curated database of **repo/path links** (one row per reference).
- Lightweight metadata so we can filter quickly:
    - **Vendor** (who maintains it)
    - **Artifact Type** (cookbook, awesome-list, research, etc.)
    - **Topic / Tags** (agents, prompts, tooling, evals, etc.)
    - **Status** (Inbox → Reviewing → Mined → Integrated → Archived)
    - **Review date** (when to revisit)

## How to use it (operating loop)

1. **Capture**: add a repo/path link, set **Status = Inbox**.
2. **Triage**: scan in **By Status** / **By Vendor** views.
3. **Mine**: open the row and record what to extract (prompt patterns, tool conventions, evaluation approach).
4. **Integrate**: once patterns are implemented internally, move to **Integrated** and link to the internal work.

## Conventions

- Prefer **canonical links** (repo root) unless a subpath is the meaningful unit (then store the subpath as its own row).
- Notes should be **actionable** (“extract X template”, “good eval harness”), not generic praise.

---

Cookbooks Database