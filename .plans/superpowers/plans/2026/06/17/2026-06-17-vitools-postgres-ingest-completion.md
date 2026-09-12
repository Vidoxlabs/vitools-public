---
name: vitools-postgres-ingest-completion
title: ViTools Postgres Ingest + Hybrid Retrieval Completion
type: doc
date: 2026-06-17
status: completed
author: Gavin Lafferty (Vioxniv)
project: vitools
tags:
  - vitools
  - memorix
  - postgres
  - hybrid-retrieval
---

# ViTools Postgres Ingest + Hybrid Retrieval — Completion

**Date:** 2026-06-17 **Follow-up to:**
[2026-06-17-vitools-memorix-integration.md](./2026-06-17-vitools-memorix-integration.md)

## Delivered

1. **Postgres ingest pipeline** — `tools/vitools_canonical/postgres_ingest.py` builds batch
   manifests from `canonical_index.json` and calls `ingest_worker.ingest_batch()`.
2. **Stable doc_ids** — `vitools/canonical/{skill|concept|mcp}/{slug}` in Memorix working set.
3. **CLI + MCP** — `vilabs memorix vitools ingest-postgres` / `memorix.vitools.ingest_postgres`.
4. **Hybrid retrieval** — `recommend --hybrid` merges local JSON index with Postgres/pgvector hits;
   `memorix_mcp/retrieval.py` applies vitools canonical authority boost.
5. **Graph projection** — synapse-lite `:Document` edges (`TAGGED_WITH`, `USES`) via
   `projection_extra` payload; Neo4j one-hop expansion includes `USES`.
6. **Tests** — manifest mapping, dry-run ingest, golden recommend queries, hybrid degradation.

## Validation

```bash
export VITOOLS_ROOT=~/Repositories/vitools MEMORIX_STATE_ROOT=~/.memorix
cd vilabs/tools/vilabs_mcp/vitools/tools/vitools_canonical
pytest tests/ -q
vilabs memorix vitools index
vilabs memorix vitools ingest-postgres --dry-run --force
# With v37/local backend:
vilabs memorix vitools ingest-postgres --apply --force
vilabs memorix vitools recommend "web research citations" --hybrid --kind skill
```

## Limitations / follow-ups

- Skills with `legal_gate_status=unknown` require `--force` until legal gate runs on each skill.
- MCP ↔ skill `USES` edges not auto-derived from skill content yet (manual projection_extra only).
- Studio UI cards for ingest status and hybrid recommend not implemented.
- Full 7-horizon temporal decay deferred; usage signals captured in index only.

## Key files

| File                                         | Role                                            |
| -------------------------------------------- | ----------------------------------------------- |
| `tools/vitools_canonical/postgres_ingest.py` | Manifest builder + ingest orchestration         |
| `tools/vitools_canonical/POSTGRES_INGEST.md` | Mapping spec                                    |
| `memorix/ingest_worker.py`                   | vitools git_sha, chunk_tokens, projection_extra |
| `memorix/memorix_mcp/paths.py`               | `vitools/canonical` working-set prefix          |
| `memorix/memorix_mcp/retrieval.py`           | Vitools canonical score boost                   |
| `memorix/memorix_mcp/graph_projection.py`    | Vitools graph edges                             |
