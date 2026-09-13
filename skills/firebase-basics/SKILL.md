---
name: firebase-basics
description: >-
  Core Firebase setup, CLI usage, and service configuration. Auth, Firestore, Hosting, and App Hosting basics. Use when initializing or configuring a Firebase project.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: cloud
  tags: [firebase, cli, auth, firestore, hosting]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: firebase-basics
    summary: Core Firebase setup and service configuration
  derived_from:
    - name: firebase-basics
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Firebase Basics

## When to use

Activate when initializing a new Firebase project, adding Firebase services to an app, or configuring Firebase CLI.

## Procedure

1. Install CLI: npm install -g firebase-tools. Authenticate: firebase login.
2. Initialize: firebase init. Select services.
3. Configure Auth: enable sign-in methods in console or via CLI.
4. Configure Firestore: create database, set security rules in firestore.rules.
5. Configure Hosting: set public directory in firebase.json. Deploy: firebase deploy --only hosting.
6. Configure App Hosting: define backend in apphosting.yaml.
7. Verify: check console for active services.

## Guardrails

- Do not ship Firestore rules in test mode. Lock down before production.
- Do not commit service account keys. Use CLI or Workload Identity.
- Do not use the production project for local development.
- Do not deploy without running firebase emulators:start locally.

## Examples

### Good

> firebase init selected Firestore and Hosting, dev project separate, rules lock writes to authenticated users, emulators tested, deployed to prod.

### Bad

> Used production project for local testing, rules left in test mode, service account key committed to git.

## Verification

- Firebase console shows all intended services enabled.
- firebase emulators:start runs all services locally.
- Firestore rules do not allow unrestricted write access.
- No service account keys in the repository.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/firebase-basics
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: firebase-basics
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/firebase-basics/raw -o .cursor/skills/firebase-basics/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/firebase-basics.md and install it as a project skill at skills/firebase-basics/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```