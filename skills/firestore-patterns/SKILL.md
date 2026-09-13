---
name: firestore-patterns
description: >-
  Firestore data modeling, querying patterns, security rules, and offline persistence. Use when designing Firestore schemas, writing queries, or configuring security rules.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: cloud
  tags: [firestore, data-modeling, queries, security-rules, offline]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: firestore-patterns
    summary: Firestore data modeling, queries, and security
  derived_from:
    - name: firebase-firestore-standard
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Firestore Patterns

## When to use

Activate when designing a Firestore data model, writing queries, configuring security rules, or setting up offline persistence.

## Procedure

1. Model entities as top-level collections. Use subcollections for unbounded one-to-many.
2. Use arrays or maps for bounded one-to-many relationships.
3. Design queries around composite indexes.
4. Write security rules: validate data shape, restrict by auth.uid.
5. Enable offline persistence (default on mobile, enable for web).
6. Paginate with cursor-based queries: startAfter(lastDoc).

## Guardrails

- Do not use arrays for unbounded lists. Each element counts against 1 MB limit.
- Do not write queries that scan entire collections. Always filter on indexed fields.
- Do not leave security rules open in production.
- Do not rely on document size staying under 1 MB without measuring.

## Examples

### Good

> Users with subcollections for orders. Query filters on userId and status with composite index. Rules validate status and restrict to owning user.

### Bad

> All orders stored as array inside user document. After 500 orders exceeds 1 MB. Query scans all users. Rules allow anyone to read.

## Verification

- All queries use indexed fields and composite indexes where needed.
- Security rules check request.auth and validate data shape.
- No document approaches the 1 MB limit.
- Pagination uses cursor-based queries, not offset.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/firestore-patterns
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: firestore-patterns
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/firestore-patterns/raw -o .cursor/skills/firestore-patterns/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/firestore-patterns.md and install it as a project skill at skills/firestore-patterns/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```