---
name: community-server-design
description: >-
  Design and operate a community Discord server for an AI or developer
  tools company with role-based access tiers, compartmentalized
  channels, bot integration, and GitHub sync. Use when setting up a
  community platform, designing role hierarchies, or planning bot
  automation for community management.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: agents
  tags: [agents, community, discord, bot, roles, automation]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: community-server-design
    summary: Compartmentalized community server design for AI companies
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Community Server Design

## When to use

Use this skill when designing or operating a community server for an
AI or developer tools company. This includes setting up role
hierarchies, channel categories, bot automation, GitHub webhook
integration, verification flows, and permission management.

## Procedure

1. Define a tiered role hierarchy with least-privilege access:
   - Public tier: all members, read access to public channels, limited
     posting after verification.
   - Contributor tier: trusted members with access to development
     channels and GitHub-synced feeds.
   - Admin tier: server management rights, role grants, moderation.
   - Operator tier: full access including private ops channels and bot
     administration.
2. Create channel categories matching the tier structure:
   - Public category: rules, welcome, announcements, introductions,
     project showcase, contribute, off-topic.
   - Contributor category: dev discussions, GitHub sync, moderation logs.
   - Admin category: admin general, config planning, user management.
   - Operator category: ops general, secrets rotation, coordination.
3. Set permission overwrites per category: public = everyone read and
   limited send; contributor = hidden from public, contributor+ read
   and send; admin and operator = progressively restricted.
4. Add a community bot with minimal scoped permissions: manage roles,
   send messages, embed links, read message history. Never grant
   Administrator.
5. Configure the bot to handle: verification flow, role grants (admin
   approval required), GitHub webhook relay to contributor channels,
   and logging.
6. Require explicit approval for destructive bot actions (mass role
   changes, channel deletion). The bot must request confirmation and
   wait before executing.
7. Seed public channels with initial content: project overview,
   contribution guide, onboarding FAQ, and links to GitHub repos.

## Guardrails

- Never hardcode bot tokens or API keys in code or documentation. Use
  a secrets manager and rotate regularly.
- Bot must operate with least-privilege permissions. Never grant
  Administrator.
- Destructive actions require explicit human confirmation. The bot must
  not execute them autonomously.
- Public content must be accurate and link to canonical documentation.
  Do not over-promise or share internal details.
- Enable audit logs and mirror them to a private operator channel.
- Verification is required before any posting access. Do not allow
  unverified members to post in public channels beyond introductions.

## Examples

### Good

> Server has 4 tier-based roles with color coding, 4 category
> compartments with permission overwrites, a bot with scoped
> permissions (manage roles, send messages, embed links), a
> verification flow requiring admin approval, and GitHub webhooks
> relaying PR activity to contributor channels. All secrets are in a
> secrets manager.

### Bad

> Server has a flat channel list with no categories, everyone has the
> same permissions, the bot has Administrator, tokens are hardcoded in
> the bot source, and there is no verification gate before posting.

## Verification

- Confirm role hierarchy is enforced top-to-bottom in Discord.
- Confirm each category has correct permission overwrites.
- Confirm bot permissions are minimal (no Administrator).
- Confirm destructive bot commands require confirmation.
- Confirm no secrets are hardcoded in code or config.
- Confirm verification flow blocks unverified posting.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/community-server-design
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: community-server-design
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/community-server-design/raw -o .cursor/skills/community-server-design/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/community-server-design.md and install it as a project skill at skills/community-server-design/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
