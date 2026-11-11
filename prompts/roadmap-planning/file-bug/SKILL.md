---
name: file-bug
description: Files a bug ticket in your issue tracker from screenshots, recordings, error text, error-monitoring links, or a vague complaint, using your team's required bug template. Use whenever something in the product is broken. Not for improvements or project work; /file-issue and /file-project own those.
---

# File a bug ticket

> **Setup:** workspace values (statuses, labels, the team map, the template reference) come from your factory config. See [`factory-config.example.md`](../../../templates/factory-config.example.md). Tool calls below use Linear MCP names as an example of how the issue tracker role is filled.

A bug ticket lives or dies on one thing. Can the reader reproduce the bug without asking the reporter a follow-up question? A ticket missing its environment or its steps gets `{{NEEDS_INFO_LABEL}}` and bounces back. That costs a day. The bug template exists to prevent it, so filling it completely matters more than filling it elegantly.

Your job is narrow on purpose. Take messy input, produce one complete, correctly routed ticket, get approval, file it. You are not diagnosing the bug.

## Scope

**In scope:** pulling facts from screenshots, videos and prose; filling the bug template; picking the team; uploading media; creating the issue.

**Out of scope:** root cause analysis, reading the codebase, prior-art research. Engineering does those after triage. Staying out of the code keeps this skill fast enough to use mid-conversation.

**The gate downstream:** `{{TICKET_READINESS_CHECK}}` grades engineering bugs against this same template. A ticket filed by this skill should pass as filed. The rules that most often trip are called out below.

**Not a bug:** if the thing works as designed and the design should change (a missing column, a confusing default, a slow flow), it is an improvement. Hand it to `/file-issue`. If it is a capability the product does not have, hand it to `/file-project`. When you cannot tell, ask one question: "Is it doing something it was built not to do, or doing what it was built to do, and that is the problem?"

## Step 1: Take inventory of what you were given

Look at everything before asking for anything. Screenshots in your context can be read directly. Uploaded files may sit in an uploads folder.

For a video, pull frames with ffmpeg and read those. Do not ask the user to describe what they recorded. One frame per second is usually enough. The frame that shows the error is often the whole ticket.

```bash
ffmpeg -i recording.mov -vf fps=1 /tmp/frame_%03d.png
```

One screenshot usually fills three or four template fields. Mine it first:

- **Address bar:** the Link, and often the environment.
- **Page header, org switcher or account menu:** the Organization.
- **Error toast, modal or red text:** the Actual result. Copy the exact string.
- **The surface itself** (which page, which record type): drives routing in Step 4.

Asking for a URL that is readable in the screenshot the user just pasted makes this skill worse than filing by hand.

## Step 2: Ask only for what is missing

After mining you will usually still lack some of: the environment (if the hostname is unclear), the affected user's email, and steps to reproduce. Ask for all of them in one message.

Two fields need extra care:

- **Production or Development.** Its absence is the most common reason a ticket bounces. If the hostname makes it clear, state your inference so the user can correct it ("Filing as Production, based on the URL."). If not, ask.
- **Steps to reproduce.** Numbered, from a fresh state. Not "do what I did". If the user has no steps, an error-monitoring link or a stack trace is an accepted substitute.

Never invent a value. An honest `Unknown` is recoverable. A plausible guess sends someone chasing a repro that never existed.

**One bug per ticket.** If the input describes several unrelated defects, say so and propose a split before drafting.

## Step 3: Fill the template

Use this structure exactly, in this order. If your team keeps the canonical template in the tracker (`{{BUG_TEMPLATE_REF}}`), this is a copy so the skill needs no network call to know the shape. If a field ever looks wrong, read the canonical one and trust it.

```markdown
**Domain Context:**

* Link:
* Production or Development:
* Organization:
* Company: (if applicable)
* Email: (user impacted)

**Context:**

* Steps to reproduce:
  1. 
  2. 
* Expected result:
* Actual result:

**Screenshot(s):** (if applicable)

**Video:** (if applicable)
```

What each field is for:

- **Link:** the exact page or record where the bug happens. Not the home page.
- **Production or Development:** the field that most often sends a ticket back.
- **Organization**, plus **Company** when an org has several and the bug is specific to one.
- **Email:** the affected user, so someone can reproduce against real data.
- **Steps to reproduce:** numbered, from a fresh state. An error-monitoring link or stack trace can stand in.
- **Expected result** and **Actual result:** separate on purpose. Sometimes the disagreement is about the expectation, not the behavior.

Keep the literal field labels and the bold. The readiness check matches on them.

Title rules:

- `Surface | What is wrong`. For example: `Invoices | Status filter "Exclude" toggle does not exclude matching records`.
- Quote the literal error string when there is one. It makes the ticket searchable and helps catch duplicates.
- Use at least six words. Short titles fail the readiness check.
- Avoid "add", "implement", "introduce", "build" and "support for". They read as a feature dressed as a bug. Describe what is broken.
- Prefix `[FE]` or `[BE]` only when the layer is known.
- Skip a "Bug:" prefix. The label says that.
- Keep it under about 120 characters.

## Step 4: Search the tracker once, for two purposes

One search answers "is this already filed?" and "who owns this?".

```
list_issues(query="<the error string, or the surface plus symptom>",
            fields=["title","team","status","labels","url","createdAt"], limit=10)
```

### Duplicates first

Search the literal error string when you have one. If something looks like the same defect, do not file on top of it. Show the user the identifier, its status, and whether you think it is the same bug or a different symptom of one cause. Let them choose: comment on the existing ticket, file as related, or file fresh.

Flag near misses even when you file anyway. The same error on a different surface often shares a root cause. Link it with `relatedTo`.

### Then routing

Route by **product surface, not technical layer**. A broken button on the Invoices page belongs to the team that owns Invoices, not the UI team.

The team that owns *recent* issues on that surface is your answer. Recency matters. Areas move between teams, and a surface search will return old closed tickets from a former owner. Weight the last few months. Ignore old `Done` work. Use `{{TEAM_MAP}}` from the factory config as a starting point only. A fresh search beats it.

Then set the rest:

- **Status:** `{{TRIAGE_STATUS}}`. Call `list_issue_statuses(team=...)` first. Fall back to `{{BACKLOG_STATUS}}` if the team has no triage status.
- **Labels:** always `{{BUG_LABEL}}` and `{{FILED_WITH_SKILL_LABEL}}`. The weekly factory retro uses the second one to compare skill-filed and hand-filed tickets. Add a layer label only if you know the layer. Labels are often team-scoped, so call `list_issue_labels(team=...)` and use exact names. Never add `{{NEEDS_INFO_LABEL}}` or any other review-process label yourself.
- **Priority:** leave unset unless the user signalled severity. Triage decides.

## Step 5: Show the draft and stop

Show the full ticket in chat: title, team, status, labels, and the description exactly as it will appear. List the files you will upload. Call out every field left as `Unknown`.

Then stop and wait. Do not call `save_issue` in the same turn as the draft. An earlier "go ahead" about tickets in general is not approval for this one. A wrong ticket in a triage queue wastes several people's time.

If the user asks for changes, revise and show it again.

## Step 6: Create the issue, then attach the media

Order matters. The tracker cannot accept an upload until the issue exists.

1. `save_issue(title, team, description, labels, state)` with no `id`.
2. Upload each file, one at a time:
   - `prepare_attachment_upload(issue, filename, contentType, size)` with the exact byte count.
   - `PUT` the raw bytes to the returned URL with `curl -X PUT --data-binary @file`. Send every returned header exactly as given, casing included. A changed or missing header returns a 403. Do not encode or transform the bytes.
   - `create_attachment_from_upload(issue, assetUrl)`.

   Signed upload URLs expire fast (about 60 seconds in this example). Finish each file before preparing the next.
3. Update the description so the Screenshot(s) and Video lines point at the media. Use a patch, not a full rewrite. Embed screenshots as images in the description, not only as attachments. Readiness checks often require a visual reference for frontend bugs. If the bug has no visual part, write "no UI change" on the Screenshot(s) line.

Report the identifier and URL. If an upload failed, say which one, and that the ticket itself is fine.

## Step 7: Offer the next step

Offer `{{TICKET_READINESS_CHECK}}` on the new issue in one line. It either marks the ticket ready (`{{AGENT_READY_LABEL}}`) or lists what is missing. `/enrich-ticket` then fills the gaps. Do not run either unprompted. If they are not installed, say so and stop. The ticket is complete without them.

If your readiness check skips some tickets (for example anything in Backlog, or tickets on the product team), say that instead of offering it.
