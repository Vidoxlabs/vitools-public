Meeting Preparation Skill

When to use

Activate when the user mentions preparing for meetings, wants a briefing for their day, or references an upcoming meeting by name.

Approach

Step 1: Get the meetings





Use available calendar connector to list the target day's events



For each event, extract: title, time, attendees, description, any links



Skip events that are clearly non-prep-worthy (focus time, OOO, all-day reminders)



Ask the user which meetings to prep for if there are many, or prep all if they said "prep me for today"

Step 2: Classify each meeting

Infer the meeting type from the title, attendees, and description:







Type



Signals



Priority sources





Internal 1:1



2 attendees, same domain



Slack DMs/threads, recent project updates





Team sync



Multiple colleagues, recurring



Project status, task boards, relevant Slack channel





Customer / partner



External domains, "demo"/"review"/"call"



Email threads with attendee, shared docs, web research on their company





Exec review



Senior leadership, "review"/"strategy"



Docs under review, milestone status, recent discussions





Product/design review



"Review"/"feedback", designer or lead



PRDs, design files linked in description, related tickets





Interview



"Interview" in title, candidate name



Web search for candidate, link from description





Unknown



No clear signals



Lightweight prep — surface recent context with attendees

Step 3: Gather context (parallelize where possible)

For each meeting, query the relevant sources based on type and available connectors:





Calendar: event description, links, attachments



Slack/Teams (if available): recent threads involving attendees or meeting topic



Email (if available): recent threads with external attendees



Drive/SharePoint (if available): docs linked in event or shared with attendees



Project management (if available): status of relevant projects, blockers



Web search (for external meetings): company info, candidate profiles

Adapt to whatever connectors the user has — calendar is the only hard requirement.

Step 4: Produce the prep brief

For each meeting, output this structure:

[Time] — [Meeting Title]
With: [attendees, with roles if known]
Type: [inferred type]

Context:
[2-4 bullet points — what's been discussed recently, what's changed, what's pending]

Your goal:
[What the user likely needs FROM this meeting — a decision, alignment, information]

Key points to raise:





[Point 1]



[Point 2]

Open questions:





[Question that needs answering]



[Decision that needs to be made]

Links:





Relevant doc



Slack thread

Quality standards





Brevity over completeness — this is a prep brief, not a research report. 1 screen per meeting max.



Links are critical — surface and organize them, don't reproduce their content.



Don't fabricate context. "No recent context found" is a valid output.



Prioritize recency — recent threads > old docs.



Flag conflicts if you find contradicting information across sources.

