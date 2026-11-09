---
name: file-issue
description: Files Linear issues that are not bugs: small standalone improvements, and the product-level chunks that break a project into what it must deliver. Not for bugs (/file-bug) or new capabilities (/file-project).
---

# File an issue

> **Setup:** this skill shares its team map and media upload flow with `/file-bug`, so set those up there first. Replace the `Surface | What should change` title convention and the improvement label lookup with your workspace's if they differ. If your team keeps an improvement template in Linear, `list_templates()` will find it and it wins over the structure below.

This skill covers every Linear issue that is not a bug. It runs in one of two modes:

- **Improvement mode:** one standalone issue for something that works as designed but should work differently. A missing column, a confusing label, a default that should change, a flow with too many clicks.
- **Decompose mode:** a set of issues that break an existing project into the logical pieces of what it has to deliver.

Both modes describe **what** the product needs to do, from the user's side. They never say **how** to build it. Implementation approach, technical design, sizing, estimates, sequencing, and assignment belong to engineering. An issue that prescribes a build approach takes a decision away from the people best placed to make it, so leave every one of those out, even when the source material has an opinion about them. If it does, record that opinion as context ("the customer suggested a nightly CSV") rather than as a requirement.

## Step 0: Confirm this is the right skill

Three skills share the Linear filing work, and the boundary is what the reporter is describing:

| The input describes | Owner |
|---|---|
| Existing behavior that is wrong compared to what it should do (errors, wrong numbers, broken flows) | `/file-bug` |
| Something that works as designed, where one specific change to the design would fix it and nothing needs shaping first | This skill, improvement mode |
| A request to break an existing project into issues | This skill, decompose mode |
| A new capability, an integration, anything that needs shaping or should collect customer demand over time | `/file-project` |

When it is ambiguous between bug and improvement, ask one question: "Is it doing something it was built not to do, or doing what it was built to do, and that is the problem?" When an improvement turns into several related changes while you draft it, stop and hand off to `/file-project`. Do not file five loosely linked improvement issues in place of a project.

## Improvement mode

### I-1: Take inventory, then ask only for what is missing

Mine screenshots, recordings, and prose the same way `/file-bug` does (address bar for the link, page header for the org, the surface itself for routing). Then ask in one batch for what is still missing. Usually that is the problem in the user's terms and who is affected. You need to know *why* the change matters before *what* the change is, because the fix proposed in a Slack message is often one of several reasonable ones.

Never invent a value. Write `Unknown` and say so.

### I-2: Search Linear once, for three purposes

```
list_issues(query="<surface plus the thing to change>",
            fields=["title","team","status","project","labels","url","createdAt"], limit=15)
```

Read identifiers off the `url` values; there is no `identifier` field.

1. **Duplicates.** If an open issue already asks for this, do not file. Bring it to the user and offer to comment on it or attach a customer need to it.
2. **A home project.** If the improvement clearly belongs to an open project (same surface, same goal), file it inside that project. A standalone improvement that is really part of planned work gets lost in the backlog.
3. **Routing.** Route by product surface, not technical layer, weighting recent issues and ignoring old `Done` work. Use the same team map as `/file-bug`.

### I-3: Check the template

Call `list_templates()` and look for an improvement or feature issue template. If one exists, its fields and order win over the structure below, the same way the bug template wins for bugs. Otherwise use:

```markdown
**Problem:**
[What the user cannot do, or what is slow or confusing today, in their terms. Quote them where you can.]

**Current behavior:**
[What happens now, with a link to the exact page.]

**Desired behavior:**
[What the user should be able to see or do instead, described as an outcome, not an implementation.]

**Who is affected:**
[Customers, internal users, or roles. Named customers if known.]

**Open questions:**
[Product questions that need an answer. Leave the section out if there are none.]

**Source:**
[Link to the Slack thread, call, or ticket.]
```

Title in house style, `Surface | What should change`, written as the outcome: `Bills list | Show due date by default`, not `Customer wants due dates`. Roughly 120 characters or less.

### I-4: Set the fields

- **State:** `Triage`. Call `list_issue_statuses(team=...)` first and fall back to `Backlog` if the team has no Triage state.
- **Labels:** call `list_issue_labels(team=...)` and apply the team's improvement or enhancement label if it has one. Never `Bug`.
- **Project:** set it if I-2 found a home.
- **Priority, assignee, estimate, cycle:** unset.

Run `/anti-ai` on the description before showing the draft.

Then go to **Approval and filing** below.

## Decompose mode

The output is a map of what the project has to deliver, cut into pieces that each make sense on their own. Engineering takes that map and decides how to build it. They may split a chunk further, merge two, or reorder everything, and none of that means the breakdown was wrong.

### D-1: Read the project before splitting it

```
get_project(<id or name>)
list_issues(project=<id>, fields=["title","team","status","url","labels"], limit=100)
```

Read the description, the customer asks, the open questions, linked documents, and every existing issue. Existing issues are pieces someone already wrote. Your breakdown fills the gaps around them and never duplicates or rewrites them. If no project exists yet, stop and hand off to `/file-project` first.

If the user gave you more material (a spec, a call transcript, a design file), read that too. The breakdown is only as good as what you know about the scope.

### D-2: Draft the chunks

A good chunk:

- **Is a capability someone could see or use.** Write it from the user's side: "A user can map TravelPerk categories to GL accounts", not "Build category mapping table" or "Add mapping endpoint". If a chunk only makes sense to an engineer, it is a technical task and does not belong in this breakdown.
- **Makes sense on its own.** Someone reading only that issue understands what it delivers and why it is part of the project.
- **Has a "Done when" stated as a user-observable outcome.** One or two lines describing what is true for the user when the chunk is finished. Never a technical test, a coverage requirement, or a performance number unless the customer stated that number.

Do not size chunks, estimate them, or split them to fit a cycle. A chunk is one logical piece of what the project delivers, however large it turns out to be.

**Open questions become question issues**, titled `Question | <the question>`, done when the answer is written into the project description. Use them for product questions the source material leaves open (which statuses to sync, whether a field is required, who should have access). Never resolve a question with a plausible guess in the chunks that depend on it, and never prescribe how the question should be investigated.

**Dependencies:** note one only when it follows from the product itself, meaning the user could not possibly do B before A exists (you cannot map categories before an account is connected). Do not order chunks by risk, priority, or build convenience. List them in the order a user would naturally meet them, and leave sequencing to planning.

If the breakdown passes about twelve chunks, say so in your draft. The project may really be two projects, and the user should decide that.

Use this body for each chunk, unless `list_templates()` returns a team template that fits:

```markdown
**What this delivers:**
[The capability, from the user's side, in one or two sentences.]

**Done when:**
[What is true for the user when this is finished.]

**Not included:**
[Only when a neighboring chunk covers something a reader might expect here. Leave it out otherwise.]

**Depends on:**
[Another chunk, only when the product requires it. Leave it out otherwise.]

**Context:**
[Customer quotes or source details specific to this chunk, if any. Leave it out otherwise.]
```

Keep chunk descriptions short. The project description carries the full context, and each chunk links back to it by living in the project.

### D-3: Set the fields

- **Project:** always the parent project.
- **Team:** the project's team. Do not re-route individual chunks; engineering will move one if another team should own it.
- **State:** `Backlog`. Check `list_issue_statuses(team=...)`.
- **Labels:** whatever the team uses for feature work, from `list_issue_labels(team=...)`. Never `Bug`.
- **Sub-issues:** do not create them. Chunks are top-level issues in the project, and further splitting is engineering's call.
- **Priority, assignee, estimate, cycle, milestone:** unset.

## Approval and filing (both modes)

### Show the draft and stop

Improvement mode: show the full issue as it will appear, with title, team, state, labels, project, and body.

Decompose mode: show a table first (title, what it delivers, done when, depends on), then each full body. Call out any existing issue you deliberately left alone, and any place where the source material was too thin to tell what a chunk should cover.

Then wait for approval. Do not call `save_issue` in the same turn as the draft, and do not treat approval of an earlier breakdown as approval of a revised one. If the user changes the breakdown, show the revised table again.

### Create

Create issues with `save_issue` and no `id`. Create any chunk that others depend on first, so later issues can reference its identifier in a blocking relation. Check the `save_issue` schema for the relation field names before the first call. If a customer asked for an improvement, offer to attach a customer need to the issue with `save_customer_need`.

Upload any media after the issue exists, using the same three-step upload flow as `/file-bug` (prepare, PUT within 60 seconds with headers verbatim, create attachment from upload), one file at a time.

If a call fails partway through a decomposition, stop, report which issues were created and which were not, and do not retry the whole batch, since that duplicates what already landed.

### Report and hand off

Report each identifier and URL (a table for decompositions). Say what you left unset and that engineering owns how the chunks get built, split, and sequenced. Then offer `/enrich-ticket` in one line for any issue that needs more context. Do not start enriching unprompted.
