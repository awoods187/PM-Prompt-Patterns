---
name: file-issue
description: Files issues that are not bugs, in your issue tracker. Improvement mode files one standalone improvement. Decompose mode breaks a Spec ready project into the user-visible chunks its PRD requires. Not for bugs (/file-bug) or new capabilities (/file-project).
---

# File an issue

> **Setup:** workspace values (statuses, labels, the team map) come from your factory config. See [`factory-config.example.md`](../../../templates/factory-config.example.md). Tool calls below use Linear MCP names as an example of how the issue tracker role is filled.

This skill covers every issue that is not a bug. It runs in one of two modes:

- **Improvement mode:** one standalone issue for something that works as designed but should work differently. A missing column, a confusing label, a default that should change, a flow with too many clicks.
- **Decompose mode:** a set of issues that break an existing project into the pieces its PRD says it must deliver.

Both modes describe **what** the product must do, from the user's side. They never say **how** to build it. Implementation approach, technical design, sizing, estimates, sequencing and assignment belong to engineering. If the source material has an opinion about the build, record it as context ("the customer suggested a nightly CSV"), not as a requirement.

## Step 0: Confirm this is the right skill

| The input describes | Owner |
|---|---|
| Behavior that is wrong compared to what it should do (errors, wrong numbers, broken flows) | `/file-bug` |
| Something that works as designed, where one specific change would fix it and nothing needs shaping first | This skill, improvement mode |
| A request to break a project into issues | This skill, decompose mode |
| A new capability, an integration, anything that needs shaping or should collect demand over time | `/file-project` |

When it is unclear between bug and improvement, ask one question: "Is it doing something it was built not to do, or doing what it was built to do, and that is the problem?" If an improvement turns into several related changes while you draft it, stop and hand off to `/file-project`. Do not file five loosely linked improvements in place of a project.

## Improvement mode

### I-1: Take inventory, then ask only for what is missing

Mine screenshots, recordings and prose the way `/file-bug` does: the address bar for the link, the page header for the org, the surface for routing. Then ask, in one message, for what is still missing. Usually that is the problem in the user's own terms and who it affects. You need the *why* before the *what*, because the fix proposed in a chat message is often one of several reasonable ones.

Never invent a value. Write `Unknown` and say so.

### I-2: Search the tracker once, for three purposes

```
list_issues(query="<surface plus the thing to change>",
            fields=["title","team","status","project","labels","url","createdAt"], limit=15)
```

1. **Duplicates.** If an open issue already asks for this, do not file. Show it to the user and offer to comment on it or attach a customer need to it.
2. **A home project.** If the improvement clearly belongs to an open project (same surface, same goal), file it inside that project. A standalone improvement that is really part of planned work gets lost.
3. **Routing.** Route by product surface, not technical layer. Weight recent issues and ignore old `Done` work. Use `{{TEAM_MAP}}` as a starting point only.

### I-3: Check the template

Call `list_templates()` and look for an improvement or feature template. If one exists, it wins over the structure below. Otherwise use this. Its first four headings match the feature template `/enrich-ticket` uses, so downstream tools read the issue without reformatting it.

```markdown
**Summary:**
[What the user cannot do, or what is slow or confusing today, in their terms, and why changing it matters. Quote them where you can.]

**Current behavior:**
[What happens now, with a link to the exact page.]

**Improved behavior:**
[What the user should be able to see or do instead, as an outcome, not an implementation.]

**Acceptance Criteria:**
- [ ] [One line each. Someone can check it against the built product and answer pass or fail without asking. Include what must be blocked, not only what must work.]

**Who is affected:**
[Customers, internal users or roles. Named customers if known.]

**Open questions:**
[Product questions that need an answer. Leave the section out if there are none.]

**Source:**
[Link to the chat thread, call or ticket.]
```

Title: `Surface | What should change`, written as the outcome. `Bills list | Show due date by default`, not `Customer wants due dates`. Keep it under about 120 characters.

### I-4: Set the fields

- **Status:** `{{TRIAGE_STATUS}}`. Check `list_issue_statuses(team=...)` and fall back to `{{BACKLOG_STATUS}}`.
- **Labels:** call `list_issue_labels(team=...)`. Apply the team's improvement label if it has one, plus `{{FILED_WITH_SKILL_LABEL}}` for the factory retro. Never `{{BUG_LABEL}}`.
- **Project:** set it if I-2 found a home.
- **Priority, assignee, estimate, cycle:** unset.

Run `/anti-ai` (or your writing-cleanup prompt) on the description before showing the draft. Then go to **Approval and filing**.

## Decompose mode

The output is a map of what the project must deliver, cut into pieces that each make sense alone. Engineering takes the map and decides how to build it. They may split a chunk, merge two, or reorder everything. None of that means the breakdown was wrong.

### D-1: Read the project before splitting it

```
get_project(<id or name>)
list_issues(project=<id>, fields=["title","team","status","url","labels"], limit=100)
```

Read the description, the customer asks, the open questions, linked documents and every existing issue. Existing issues are pieces someone already wrote. Fill the gaps around them. Never duplicate or rewrite them. If there is no project, stop and hand off to `/file-project`.

**Spec ready gate.** Decompose runs only on a project that carries `{{SPEC_READY_LABEL}}`. If it is missing, stop. Say the PRD has not passed review. Offer `/write-prd` if there is no `PRD | <Project name>` document, or `/review-prd` if there is one. Do not decompose from the project description alone. Do not skip the gate because the user asks.

When the gate passes, read the PRD with `get_document`. Its numbered requirements and acceptance criteria are what the chunks are cut from. Read any other material the user gives you too.

### D-2: Draft the chunks

A good chunk:

- **Is something a user can see or use.** "An admin can map expense categories to accounts", not "Build mapping table" or "Add mapping endpoint". A chunk that only makes sense to an engineer is a technical task and does not belong here.
- **Makes sense alone.** A reader of that issue alone understands what it delivers and why it is in the project.
- **Has user-observable acceptance criteria**, copied by ID from the PRD. Never a technical test, a coverage target, or a performance number the customer did not state.

Do not size, estimate, or split chunks to fit a cycle.

**Cover every requirement.** Each PRD requirement ID belongs to exactly one chunk. A chunk usually delivers a few related requirements. Before showing the draft, check both ways: every requirement is in some chunk, and no chunk delivers anything the PRD does not require. Report gaps. Do not fill them with guesses.

**Open questions become question issues**, titled `Question | <the question>`, done when the answer is written into the project. Never resolve a question with a guess in the chunks that depend on it.

**Dependencies:** note one only when the product forces it. The user cannot do B before A exists. Do not order by risk, priority or build convenience. List chunks in the order a user would meet them.

If the breakdown passes about twelve chunks, say so. The project may really be two projects.

Use this body for each chunk, unless `list_templates()` returns a team template that fits:

```markdown
**Summary:**
[The capability, from the user's side, in one or two sentences, including who it is for.]

**Requirements:**
[The PRD requirement IDs this chunk delivers, e.g. IMP-1, IMP-2.]

**Acceptance Criteria:**
- [ ] [Copied by ID from the PRD, one per line. Add none of your own.]

**Not included:**
[Only when a neighboring chunk covers something a reader might expect here.]

**Depends on:**
[Another chunk, only when the product requires it.]

**Context:**
[Customer quotes or source details specific to this chunk, if any.]
```

Keep chunk descriptions short. The project and the PRD carry the full context.

### D-3: Set the fields

- **Project:** always the parent project.
- **Team:** the project's team. Do not re-route chunks. Engineering moves one if another team should own it.
- **Status:** `{{BACKLOG_STATUS}}`.
- **Labels:** the team's feature label, plus `{{FILED_WITH_SKILL_LABEL}}`. Never `{{BUG_LABEL}}`.
- **Sub-issues:** none. Chunks are top-level issues in the project. Further splitting is engineering's call.
- **Priority, assignee, estimate, cycle, milestone:** unset.

## Approval and filing (both modes)

### Show the draft and stop

Improvement mode: show the full issue with title, team, status, labels, project and body.

Decompose mode: show a table first (title, what it delivers, requirement IDs, depends on), then each full body. Call out any existing issue you left alone, and any place where the material was too thin to tell what a chunk should cover.

Then wait. Do not call `save_issue` in the same turn as the draft. Approval of an earlier breakdown is not approval of a revised one.

### Create

Create issues with `save_issue` and no `id`. Create chunks that others depend on first, so later issues can reference them. Check the `save_issue` schema for relation field names before the first call. If a customer asked for an improvement, offer to attach a customer need with `save_customer_need`.

Upload media after the issue exists, one file at a time, with the same flow as `/file-bug`.

If a call fails partway through a decomposition, stop. Report which issues were created and which were not. Do not retry the whole batch.

### Report and hand off

Report each identifier and URL (a table for decompositions). Say what you left unset, and that engineering owns how the chunks get built, split and sequenced. Offer `/enrich-ticket` in one line for any issue that needs more context. Do not start it unprompted.
