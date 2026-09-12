# Discord Onboarding Questions  Vidoxlabs Server

**Purpose**: Use Discord's built-in **Server Onboarding** (Server Settings > Onboarding) to automatically guide new L3 Public members to relevant channels based on their interests in v37 cluster, CRS, Violet Cabinet / agents, development/contributing, ViLabs Studio + Memorix. 

This complements (does not replace) the manual verification questions in #rules for higher-tier (L2) access. Onboarding grants `@Verified` + core public channels automatically. Deeper verification for L2 remains in #rules or via Vibot.

**Guidelines Followed** (from Discord examples):
- Max ~6 options per question.
- Separate questions for off-topic / notifications / profile.
- Important channel-discovery questions are **Required**.
- Concise titles + short descriptions.
- One answer can grant multiple channels + roles.
- Later questions optional (appear in "Channels & Roles" tab after join).
- No rules text inside questions (rules are separate post-join prompt).
- Default Channels (everyone gets on join): #rules, #welcome, #announcements, #introductions, #contribute, #off-topic, #project-showcase.

**Recommended Default Channels** (set these first in Onboarding settings):
- #rules (pinned rules + verification questions)
- #welcome
- #announcements
- #introductions
- #contribute (GitHub + L2 path)
- #off-topic
- #project-showcase

---

## Question 1: Primary Interest (Required  Channels + Role)

**Question Title**: What brings you to Vidoxlabs?

**Description**: Pick your main area of interest. We'll give you access to the most relevant public channels right away.

**Type**: Single choice (or multi-select if Discord allows in your server version)

**Answers** (each grants channels + `@Verified` role):

1. **v37 Cluster & Infrastructure**  
   Description: Proxmox VE, nodes, networking, hardware, CRS (Cluster Relations Systems)  
   Grants: #v37-cluster, #crs-updates, @Verified

2. **Violet Cabinet & Agents**  
   Description: VIs (Violet, Wisteria, Xylia, Yarrow, Zinnia), LAs, Orchestral Autonomous Intelligence  
   Grants: #violet-cabinet, #ama, @Verified

3. **Development & Contributing**  
   Description: GitHub (vilabs org), code, vilabs_cli, agents tooling, PRs/issues  
   Grants: #contribute, #project-showcase, @Verified  
   *Extra prompt in answer description: "Check #contribute for L2 Contributor path via GitHub activity"*

4. **ViLabs Studio + Memorix**  
   Description: Project management, plans, memory framework, ViDocs knowledge base  
   Grants: #project-showcase (already default), relevant future studio channels, @Verified

5. **General Exploration / Learning**  
   Description: Just here to follow updates and learn about sovereign AI infrastructure  
   Grants: Core public channels + @Verified (no extra specific channels)

6. **Other / Multiple Interests**  
   Description: I have interest across several areas  
   Grants: Core public + @Verified; user can explore more in "Channels & Roles" tab later

**Why this works**: Directly maps to our public channel structure and generates interest signals. "Development" answer funnels toward L2 path naturally.

---

## Question 2: Secondary Interests / Off-Topic (Optional  Channels)

**Question Title**: Any other topics you're interested in?

**Description**: These are lower-priority or casual channels. You can always browse more later.

**Type**: Multi-select (recommended)

**Answers** (grant additional channels):

1. **Casual chat & community**  
   Grants: #off-topic (already default, but reinforces)

2. **Showcase & wins** (already default, but good for emphasis)

3. **AMAs & Violet Cabinet discussions** (if not already granted in Q1)

4. **Specific technical deep-dives** (future channel or thread interest)

Keep to 4-5 max. Or make this question only if you have many off-topic channels.

---

## Question 3: Notifications & Updates (Optional  Roles or Channels)

**Question Title**: What updates would you like to follow?

**Description**: Choose pings or channels for important announcements. You can change this anytime in the Channels & Roles tab.

**Type**: Multi-select

**Answers** (can grant roles like @Announcements or specific channels):

1. **Major announcements & releases** (v37, CRS, new agents/tools)  
   Grants: Notification role or highlights in #announcements

2. **GitHub activity & contributions** (issues, PRs, L2 sync highlights via Vibot)  
   Grants: Access to #l2-github-sync discussion (if L2 later) or curated pings

3. **AMA & Violet Cabinet sessions**  
   Grants: Event pings or #ama highlights

4. **No pings / Mute for now**  
   Grants: Nothing extra (respects quiet members)

**Note**: For true role-based pings, create notification roles (e.g. @v37-updates) and grant them here. Vibot can later enhance with custom commands.

---

## Question 4: Profile & Self-Expression (Optional  Profile / Future Roles)

**Question Title**: Tell us a bit about yourself (optional)

**Description**: This helps the community and future Vibot features personalize your experience. Answers appear in your profile or server insights.

**Type**: Short answer or multiple choice (pronouns, skills)

**Example Answers / Fields**:
- Pronouns (he/him, she/her, they/them, etc.)
- Primary skills/interests: Python, TypeScript/JS, Infrastructure/Proxmox, AI Agents, Documentation, Project Management, Hardware, Other
- GitHub username (optional, for future L2 auto-suggestions)
- How did you hear about Vidoxlabs? (GitHub, X/Twitter, friend, search, other)

**Benefit**: Builds community data. Future Vibot or Memorix integration could use this for smart channel suggestions or L2 fast-track signals (e.g. GitHub username present + dev interest from Q1).

---

## Question 5: Quick Feedback / Source (Optional  Analytics)

**Question Title**: How did you discover Vidoxlabs?

**Description**: Helps us understand growth channels (one-time question).

**Answers**:
- GitHub (vilabs org or specific repo)
- X / Twitter or other social
- Friend or community recommendation
- Search / vidoxlabs.dev (future)
- Other

**Use**: Purely for internal tracking. No channel/role grants needed.

---

## Setup Instructions in Discord

1. Go to **Server Settings > Onboarding**.
2. Set your **Default Channels** (the ones everyone sees immediately  see list above).
3. Add the questions in order (Q1 first as Required).
4. For each answer, configure the exact **Channels** and **Roles** it grants.
5. Enable "Ask members before they join" only for the most important questions (Q1). Others can be answered later in the Channels & Roles tab.
6. Preview the full flow.
7. Publish / Enable Onboarding.

**Testing**:
- Use incognito or alt accounts.
- Complete onboarding as different "personas" (infra person, agent-curious person, dev/contributor).
- Verify they land in the right channels and get @Verified.
- Check that private categories remain hidden.

**Integration with Existing Verification**:
- Onboarding handles quick channel discovery + basic @Verified.
- Direct users (in welcome embed or #rules) to answer the deeper verification questions (in skill references/verification-questions.md) if they want L2 Contributor access (GitHub sync, dev channels).
- Vibot can later bridge the two (e.g. `/verify` command that checks onboarding completion + asks deeper questions).

**Maintenance**:
- Review answers periodically via server insights or Vibot logs.
- Update questions when new public channels launch (e.g. new ViLabs Studio category).
- Keep total questions to 4-5 max for best completion rates.

**Vidoxlabs Alignment**:
- Directly supports public interest generation (project-showcase, contribute, v37, violet-cabinet).
- Respects compartmentalization (only public channels granted here).
- Feeds L2 path naturally via "Development & Contributing" answer + #contribute channel.
- Concise, scannable, evidence-backed (tied to our actual public channel structure and VIs/projects from masternote.md).

---

**Files Updated in Skill**:
- This document added to references/.
- Complements rules-template.md, verification-questions.md, welcome-embed.md, and discord-channel-list.md.

Update the master plan in .plans/ when you implement these questions live. Run validation before major changes.

*This setup turns new members into engaged community members aligned with Vidoxlabs vision from minute one.*
