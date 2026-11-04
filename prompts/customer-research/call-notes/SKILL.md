---
name: call-notes
description: Turns a call transcript (pasted, uploaded, or found in a call recorder such as Attention or Gong) into internal product feedback notes delivered as a Google Doc, in a consistent house style, with feature asks linked to real Linear projects. Use this whenever the user shares or points to a transcript of a customer, prospect, advisory board, churn, or lost-deal call and wants it written up, even casually ("write notes on this call", "summarize this transcript", "write this up", "notes like the usual format", or just dropping a transcript and saying "notes"). Also use it when the user names a call to fetch from the call recorder ("write up yesterday's call with Acme"). Do not use it for the outbound thank-you email to the buyer; /closed-lost-thank-you owns that. Do not use it for internal team meetings with no customer or prospect on the call.
---

# Product feedback call notes

> **Setup:** the call-recorder tool names below (`search_calls`, `get_call_details`) are from the Attention MCP server; swap in your recorder's equivalents or drop that input path. The exemplars in `references/` are fictional; replace them with two of your own best write-ups once you have them.

These notes are how customer and prospect feedback stops being a transcript and starts being product input. They get shared internally, they get skimmed by people who were not on the call, and their links get clicked, so every claim needs to be concrete and every feature ask needs to point at where it lives in Linear (or say plainly that it does not live anywhere yet, which is itself a finding).

The author is always the user, head of product, and the doc signs off with their first name. Write in first person plural ("we") for the company and by name for everyone on the call.

## Inputs

The transcript can arrive three ways. Handle whichever shows up without asking about format:

1. Pasted or uploaded directly (most common).
2. Named but not provided ("write up the Northwind call"). Search the call recorder with `search_calls` (title search plus transcript search for the company or participant name), then pull the transcript with `get_call_details`.
3. Already summarized earlier in the conversation. Reuse what is in context rather than re-reading.

If more than one call matches a search, list the candidates and ask which one rather than guessing.

## Workflow

1. Read the whole transcript before writing anything. Identify who is who, what kind of call it was (lost deal, advisory board, win-back, churn, discovery), and what the single most important takeaway is. That takeaway shapes the first section.
2. Extract material into the buckets below. Keep the speaker's own phrasing where it is vivid; "it's ugly, but inventory ties out every month and she won't risk that mid-season" beats "satisfied with incumbent".
3. Enrich with Linear. For every feature ask, integration, and named gap, search `Linear:list_projects` (fall back to `Linear:list_issues` for smaller items) and link the real project inline on the feature name. Never invent a URL. If nothing exists, say so in the doc; a missing project is signal, not an omission to paper over.
4. Get the call link. If the transcript came from the call recorder or a call can be found there, link the call from the doc title the way the exemplars do. Only use a URL that actually came back from a tool. If none exists, leave the title unlinked.
5. Draft the doc using the template below. Match it against the exemplars in `references/` (read at least one before your first draft in a session).
6. Run the draft through the [Remove AI Writing Patterns](../../stakeholder-communication/remove-ai-writing-patterns/) prompt, and fix what it flags before the user sees anything. Notes full of generated-sounding filler will not get read, and worse, will not get trusted.
7. Deliver as a Google Doc (see Output).

Step 6 is not optional.

## What to extract

Keep:
- Deal or relationship status, stated plainly: what is blocking, what renewed, what the switching constraint is, whether we are still in consideration
- Specific likes, with the reason ("bank rules much easier to set up than in QuickBooks", not "liked bank rules")
- Weaknesses in our product or our pitch, including how a demo landed
- Feature asks and wishlist items, each mapped to Linear
- Things they asked for that we already support, flagged as such (these are messaging failures, not product gaps, and the exemplars keep them in their own subsection)
- Their stack: what we integrate with today versus not yet
- Concrete numbers, dates, entity names, seat counts, match rates, close-day constraints
- Repetition as emphasis ("she raised it three separate times" is data)
- Committed next steps, who owns them, and stated availability

Leave out:
- Small talk, scheduling back-and-forth, screen-share fumbling
- Anything about internal team members that is not an action item
- Verbatim rambling; compress to what they meant

## Doc structure

Title: `# Product feedback call: [Name] ([Company]), [call type]`, with the name linked to the recorded call when a real link exists.

Sections, in order, using H2 headings:

1. **Opening status section.** Header adapts to the call: "Why we lost the deal" for a loss, "Where things stand" for advisory or win-back, "Why they're churning" for churn. Two to four short paragraphs of prose covering the blocker or constraint, the decision status, and anything that gates a future deal. This is the section a skimmer reads, so the hardest fact goes first.
2. **What they liked.** Bullets with substance, one to two sentences each.
3. **What felt weak** (or "What felt weak or missing"). Same shape. Include demo and pitch problems, not just product gaps.
4. **Feature wishlist.** Bullets. Lead each with the ask, link the Linear project inline, and note status (backlog, planned, in progress, shipped). If they asked for something we already have, break those into a short "already supported" run with a note on why the message did not land.
5. **Their stack** (only when a stack came up). Split "Supported today" from "Not yet supported", with Linear links on the not-yet items.
6. **Next steps.** Numbered when there are discrete commitments. Include their availability if they gave it, and close out any action items that were resolved live on the call.

Sign off with the user's first name on its own line. Omit any section with nothing real in it rather than padding.

## Voice rules

- Prose first. Bullets carry full sentences with a fact and a reason, never bolded label-colon fragments.
- No em dashes. Use periods, commas, or parentheses.
- Specific over general, always. Names, numbers, product names, quotes-in-paraphrase.
- One color note is welcome when it is useful intel (a model switch, a tool they hate, a peer evaluating us). More than one starts to read like gossip.
- Call our own weaknesses what they are. "The demo spent twenty minutes on multi-entity, which they don't need, and never got to inventory" is the house register; do not soften it.
- Never speculate on why they said something. Report what they said and what it maps to.
- Keep the whole doc under roughly a page and a half. If it runs long, cut the likes before you cut the gaps.

## Output

Deliver as a Google Doc:

1. Create it with `Google Drive:create_file`, passing the notes as `textContent` with `contentMimeType: text/markdown` so Drive converts it to a native Doc with headings and links intact. Title the file the same as the doc's H1 minus the "# ".
2. Give the user the Doc link.
3. If Drive is unavailable or the upload fails, fall back to a local `.md` file presented to the user, and say why.

After the link, add two or three lines flagging what the user should act on: feature asks with no Linear project (offer /file-project), a customer with no Linear customer record (offer /sales-request), or a claim in the doc worth double-checking. Do not narrate the Remove AI Writing Patterns pass or the Linear searches.

## Exemplars

Two finished docs live in `references/`. Read one before drafting; they are the ground truth for register and structure.

- `references/example-lost-deal.md`: a closed-lost writeup. Note how the blocker leads, how "she mentioned, but we already largely support" gets its own run, and how every gap carries a Linear link.
- `references/example-advisory-board.md`: an advisory board session. Note the adapted opening header, the resolved-live action item in next steps, and the flagged absence of a Linear project as a finding.
