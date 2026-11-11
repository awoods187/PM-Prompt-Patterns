---
name: enrich-ticket
description: Interactively completes a ticket in your issue tracker against its template. Bugs, chores and spikes finish when your ticket-readiness check passes. Features finish when they pass this skill's own checks, with acceptance criteria copied by ID from the project's PRD. Use for /enrich-ticket PROJ-123, or to clean up, fill in or template a ticket.
---

# Enrich a ticket

> **Setup:** workspace values (labels, the readiness check, the agent handoff) come from your factory config. See [`factory-config.example.md`](../../../templates/factory-config.example.md). Tool calls below use Linear MCP names as an example of how the issue tracker role is filled.

Takes an incomplete ticket and fills it in, from context first and from the user second, until it meets its template. It is the human-in-the-loop partner to `{{TICKET_READINESS_CHECK}}`.

Two paths, because readiness checks often grade only some ticket types:
- **Bugs, chores and spikes** finish when `{{TICKET_READINESS_CHECK}}` passes.
- **Features and improvements** finish when they pass this skill's own feature checks. If your readiness check skips features, re-running it would never pass and the loop would never end.

## Inputs

`/enrich-ticket PROJ-123`, or "enrich", "clean up", "fill in" or "template" with a ticket ID or URL. If none is given, ask once.

## Phase 1: Fetch and classify

1. Get the issue: title, description, status, team, labels, creator, project.
2. Read its comments for context.
3. Classify:
   - Bug label, or the description starts with `Bug:`, `Error:`, `Crash:` or `Regression:` → **bug**
   - Chore, tech debt, cleanup or refactor labels → **chore**
   - Spike, research or investigation labels → **spike**
   - Otherwise → **feature** (includes improvements)

   If it is unclear, ask: "Is this a bug (broken behavior) or a feature or improvement (new or better behavior)?"

## Phase 2: Load the PRD (features only)

If the ticket belongs to a project, look for the project's `PRD | <Project name>` document.

- **PRD exists and the project carries `{{SPEC_READY_LABEL}}`:** the PRD is the source of truth for acceptance criteria. Find the requirement IDs this ticket delivers, from a `**Requirements:**` line or by matching the ticket to the PRD's requirements and asking the user to confirm. Copy those requirements' acceptance criteria word for word, with their AC IDs.
- **PRD exists but is not Spec ready:** say so, offer `/review-prd`, and continue. Copy criteria where they exist, and flag that they may still change.
- **The ticket asks for something the PRD does not require:** stop. Do not invent criteria to cover it. Ask whether the PRD needs updating (`/write-prd` update mode) or the ticket is out of scope.
- **No project or no PRD:** ask the user for acceptance criteria.

Never ask the user to invent criteria that a Spec ready PRD already states.

## Phase 3: Find the gaps

Compare the ticket with its template and list the missing fields.

### Bug template

Same template as `/file-bug`.

```
**Domain Context:**

- Link:
- Production or Development:
- Organization:
- Company: (if applicable)
- Email: (user impacted)

**Context:**

- Steps to reproduce:
  1. ...
- Expected result:
- Actual result:

**Screenshot(s):** (if applicable)

**Video:** (if applicable)
```

Required: Link, Production or Development, Organization, Steps to reproduce (or an error-monitoring link or stack trace), Expected result, Actual result.

### Feature template

```
**Summary:**

(What it is, who it is for, and why it matters to them)

**Current behavior:**

- ...

**Improved behavior:**

- ...

**Requirements:** (only when a PRD exists)

IMP-1, IMP-2

**Acceptance Criteria:**

- [ ] AC-IMP-1.1 ...

**Screenshot(s):** (if applicable)

**Video:** (if applicable)
```

Required: Summary, Current behavior, Improved behavior, Acceptance Criteria. Requirements is required when a PRD exists.

### Chore template

```
**Why now:**

**Scope:**

- ...

**Definition of done:**

- [ ] ...
```

### Spike template

```
**Question to answer:**

**Deliverable:**

**Time-box:**
```

## Phase 4: Ask the user

Ask for every missing field in one numbered message. Do not pad. Do not invent values. If a reply is unclear, follow up on that field only. "I don't know" on an optional field means N/A.

If a comment fills a gap, surface it: "A comment by X mentions [info]. Use this for [field]?" Do not pull comment content into the description without a yes.

Loop until every required field is filled.

## Phase 5: Draft and confirm

Build the description in the right template:
- Keep the meaning. Restructure the reporter's words. Do not editorialize.
- Copy embeds, attachment links, PR links and signed URLs exactly.
- Move any walkthrough-video section or transcript block, unchanged, to the bottom.
- Do not touch comments.
- Use the template's exact headings.
- Acceptance criteria copied from a PRD keep their AC IDs and exact wording.

Show the full draft and ask: "Confirm and I'll update the ticket."

## Phase 6: Update the ticket and check

After an explicit yes:

1. Save the new description. Pass the full current label set minus `{{NEEDS_INFO_LABEL}}`. In many trackers the labels field replaces the whole set, so pass every other label.
2. Change nothing else (title, status, assignee, priority) unless the user asked.
3. Check the result. The check depends on the type.

**Bug, chore or spike:** run `{{TICKET_READINESS_CHECK}}`.
- Passes → done. The check applies `{{AGENT_READY_LABEL}}`.
- Fails → show the failed rules and go back to Phase 4 for those fields only.
- Skipped (for example the ticket is in Backlog, or on a team the check ignores) → stop and say why it was not graded. Do not loop.

**Feature:** do not run the readiness check if it skips features. Run these checks yourself:

| Check | Passes when |
| --- | --- |
| Title | At least six words |
| Summary | Present, and names who benefits (a user, a customer, a role, or a "so that") |
| Behavior | Current behavior and Improved behavior both present |
| Acceptance criteria | At least one. Each is one line and checkable as pass or fail against the built product |
| PRD link | If a PRD exists: Requirements lists real requirement IDs, and every AC is copied from the PRD by ID |
| Length | Description is at least 200 characters |

- All pass → done. Do not apply `{{AGENT_READY_LABEL}}` yourself. Feature tickets go through human review.
- Any fail → show which, and go back to Phase 4 for those fields only.

If the user says "stop" or "skip" at any point, stop. If the ticket has not been saved yet, leave it as it was.

## Phase 7: Next step

- Bug, chore or spike that passed: `<ID> enriched and verified. Next: {{AGENT_HANDOFF}} <ID>.` (Leave out the next step if you have no agent handoff.)
- Feature that passed: `<ID> enriched. Acceptance criteria [copied from the PRD | provided by you]. Ready for engineering review.`

## Edge cases

- **No description:** ask for every template field.
- **Already matches the template:** "Already matches the template. Re-apply anyway, or skip?"
- **Already marked ready:** "Already verified. Re-enrich anyway?"
- **Type still unclear:** ask.

## Tone

No apologies, no filler. Short and direct. Say what is missing, ask, move on.
