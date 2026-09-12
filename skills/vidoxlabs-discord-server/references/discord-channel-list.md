# Discord Channel List Reference

**Full proposed structure for Vidoxlabs server.** Use as checklist when creating in Discord UI or via Vibot.

## Public Category (L3+)
1. **#rules**  Pinned server rules, tier explanations (L0-L3), verification process, links to GitHub (vilabs), contribute guide, ViDocs, vidoxlabs.dev (future). Vibot posts welcome embed here on join.
2. **#welcome**  Vibot automated welcome + onboarding instructions. Links to #rules #introductions #contribute.
3. **#announcements**  Curated high-signal updates (v37 status, CRS releases, new agent drops, Violet Cabinet decisions). Vibot + L1/L2 post here. Existing #public-announcements renamed/enhanced.
4. **#introductions**  New members introduce themselves. L3 can post after rules reaction or verification.
5. **#project-showcase**  Community + core team posts wins, screenshots, demos from v37 cluster, CRS, ViLabs Studio, Memorix, agent interactions. High visual interest driver.
6. **#contribute**  How to get involved: GitHub org, issue/PR workflow, local dev setup (Proxmox v37, vilabs_cli), earning L2 role via contributions. Links to AGENTS.md, masternote.
7. **#v37-cluster**  Public updates on v37 Hub-and-Spoke, node status (redacted), CRS consolidation metrics (e.g. 914 tests pass). Links to docs.
8. **#crs-updates**  Cluster Relations Systems news, vilabs_cli.crs namespace changes, import updates.
9. **#violet-cabinet**  Educational content + scheduled AMAs about VIs (Violet Chair, Wisteria Narrative, Xylia Risk, Yarrow Coherence, Zinnia Execution). LAs delegation examples.
10. **#ama**  Ask Me Anything channel. Vibot routes or schedules sessions with appropriate VI context or human.
11. **#off-topic**  Casual community chat to build interest and retention.

## L2 Private Category (L2+ only  hidden from L3)
12. **#l2-dev-general**  Developer and moderator discussion, cross-repo coordination.
13. **#l2-github-sync**  Vibot/GitHub webhook relay of issues, PRs, commits from vilabs/* repos. Moderated discussion. Curated highlights pushed to public #announcements.
14. **#l2-moderation**  Mod queue, user reports, action logs (Vibot + human).
15. **#l2-vibot-ops**  Vibot-specific: command usage stats, config changes, bug reports, feature requests for the bot itself.

## L1 Private Category (L1+)
16. **#l1-admin-general**  Discord admin coordination.
17. **#l1-discord-config**  Planning and discussion of channel/role/permission changes before execution.
18. **#l1-user-management**  Verification requests queue, manual L2 grants, user notes.

## L0 Private Category (L0 only  highest isolation)
19. **#l0-ops-general**  High-level operational coordination.
20. **#l0-secrets-rotation**  References to Infisical only. DLP redacted notes. Never paste actual secrets.
21. **#l0-cluster-coordination**  v37 cluster high-level (links, status summaries, maintenance windows). No credentials or sensitive config.
22. **#l0-vibot-admin**  Full Vibot administration, token rotation planning, advanced command approval. Still requires Violet ratification simulation for destructive actions.

## Additional Future Channels
- #l2-mcp-bridge (when MCP/Discord integration live)
- #vidoxlabs-dev-updates (when vidoxlabs.dev launches, L2 sync)
- Voice channels: Public community voice, L2 dev voice (optional)

**Permission Notes**:
- Categories set base deny for lower tiers.
- Individual channels can override (e.g. #ama allows L3 send).
- Vibot role has explicit allow on channels it manages, but never Administrator permission.
- Audit all overwrites with Discord permission simulator before applying.

**Creation Order Recommendation**:
Roles first (hierarchy) ’ Categories (with base perms) ’ Channels inside categories (fine-tune) ’ Test with test accounts at each tier ’ Seed content ’ Invite Vibot ’ Verify.

*Cross-reference with SKILL.md for full context. Update this file when server structure changes.*
