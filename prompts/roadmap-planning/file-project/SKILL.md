---
name: file-project
description: Creates a well-formed project in your issue tracker from a feature request, integration ask, or chunk of work that has no home yet. Searches for existing projects first so demand consolidates instead of fragmenting, picks the owning team, applies labels, writes a description a PM can act on, and links the source. Use whenever something needs a project, even casually ("we should track this", "is there a project for this", "make a project for the Initech ask", "where does this live"), and especially when a customer or prospect asks for a capability the product does not have yet. Also use it when you are unsure whether a project exists or which team owns it. Not for bugs; /file-bug owns those.
---

# File a project

> **Setup:** workspace values (statuses, labels, the team map, your docs site) come from your factory config. See [`factory-config.example.md`](../../../templates/factory-config.example.md). Tool calls below use Linear MCP names as an example of how the issue tracker role is filled. Vendor and customer names are fictional.

A project is the unit demand accumulates against. Ten customers asking for an Initech Expense integration is a roadmap decision. Ten separate records of the same ask is noise nobody can rank. So the most valuable thing this skill does is not creating a project. It is finding the one that already exists.

Your job is narrow. Produce one correctly named, routed and labeled project, or point to the one that already covers it. You are not scoping the work, estimating it, or deciding when it ships.

## Scope

**In scope:** searching for prior art, judging whether a near match is the same work, naming, routing, labels, status, the description, and linking the source.

**Out of scope:** the issues inside the project, milestones, priority, target dates and the lead. Those belong to whoever plans the work. A guessed target date reads as a commitment nobody made.

## Step 1: Search for prior art, then read what comes back

Search the **bare noun** for the thing being asked for, not the project name you plan to create:

```
list_projects(query="<vendor or feature noun>",
              fields=["id","name","url","status","teams","labels","summary"],
              limit=25)
```

Project names drift in every workspace. `Hooli Pay integration`, `Add Umbrella integration` and plain `Initech` end up side by side. A search for "Initech Integration" finds nothing, and you create a duplicate of a project that has existed for months. A search for "Initech" finds it.

Read every hit and decide whether it is the same work. Substring matches mislead in both directions:

- `Planning Grid (Vandelay style)` matches "Vandelay" but is a planning feature that borrowed a competitor's layout. It is not a Vandelay integration. Creating the integration project is correct.
- `Hooli Pay Integration (misc)` may be a catch-all for bugs and small fixes, not the home for a new capability. Judge by the summary and what is inside it.

Before concluding nothing exists, search obvious aliases: a former product name, the parent company, the abbreviation people say out loud.

**Search issues too.** An issue search finds the specific gap that a project title hides:

```
list_issues(query="<vendor or capability>", fields=["title","team","status","project","url","createdAt","labels"], limit=15)
```

Read identifiers from the `url` values.

An open issue saying an export has no scheduled refresh tells you more than the existence of an export project. Put it in the description. A recently fixed bug matters too. The customer may be asking for something that started working two weeks ago.

**Then check whether it already shipped.** If your docs site publishes a page index (`{{DOCS_INDEX}}`), search it for the capability, not just the vendor. Non-integration features live outside the integrations section, often under settings or configuration. Read the full index, not a marketing page that lists a few headline integrations.

### What to do with what you find

| Finding | Action |
|---|---|
| Shipped, and the ask is a bare vendor name or restates the doc page | No project. Say so and link the page. |
| Shipped, but the ask names something the docs do not cover (a cadence, a direction, a volume, a hard requirement) | Create. Name the shipped capability and say exactly where it falls short. |
| Shipped, and the ask is vaguer than the docs | Create, with the ambiguity as the first open question. |
| Same work, open project | No project. Return the existing one so the caller can attach demand to it. |
| Same work, closed or canceled project | Create. A closed project is a decision already made. New demand hung on it disappears. Link it and say why this ask is different. |
| Near miss on a different surface | Create, and name the near miss. Shared root causes are worth flagging. |
| Nothing | Create. |

A vendor that competes with one of your own modules is still an ordinary request. Whether to replace that product or connect to it is a commercial decision. It is not yours to make from a chat message.

## Step 2: Name it so the next search finds it

For integrations, use `<Vendor> Integration`. For everything else, a short noun phrase that names the outcome, not the request: `Multi-currency bank feed matching`, not `Customer wants multi-currency`.

Use the vendor's own capitalization. Requests arrive as "initech" or "hooli pay". Copying that makes the project look careless and harder to spot.

Keep it under about 60 characters. Skip "Add" or "Build". Leave the customer's name out. The customer belongs in the description and in a customer need. The project will outlive their ask, and the next customer should not have to guess that `Initech for Acme Co` is where their request goes.

## Step 3: Route it to a team

Integrations go to `{{INTEGRATIONS_TEAM}}`, if one team owns them. Deviate only when the integration is really a change to a core surface. A tax-engine connector is mostly tax-engine work, so it goes to the team that owns the tax engine.

Everything else routes by **product surface, not technical layer**, the same rule `/file-bug` uses. A reporting request goes to the reporting team even if the work is mostly backend. Ask what the customer would do differently in the product, and route to whoever owns that screen or model. Not everything that names another company is an integration. Single sign-on with an identity provider is platform work.

`{{TEAM_MAP}}` in the factory config is a starting point. It drifts. When the surface is not obvious, check live data:

```
list_projects(query="<surface noun>", fields=["name","teams","status","updatedAt"], limit=15)
```

The team that owns *recent* projects on that surface is your answer. Ignore old completed work. When a request spans surfaces or has no clear owner, `{{PRODUCT_TEAM}}` is the honest home. Shaping happens there before a team takes it.

Pick one team. Adding several teams to a fresh project gives ownership to nobody. Planning can add a second team later.

## Step 4: Set the fields

**Status:** `{{BACKLOG_STATUS}}`. Any other status claims an intent nobody stated.

**Labels:** call `list_project_labels()` and use exact names.

- `{{CUSTOMER_GAP_LABEL}}` when a named customer or prospect wants this. This label puts the project in gap reviews and in `/prioritize-demand`.
- One of `{{ORIGIN_LABELS}}` for where the ask came from.
- If you use `{{DEAL_LABELS}}`, default to the "logged for later" label. Picking the "sprintable" one puts a promise in front of a deal team.
- `{{PARTNERSHIP_LABEL}}` when shipping needs a commercial agreement with the vendor.

Never set `{{RELEASE_LABELS}}`. A PM assigns those during planning.

**Priority, lead, dates:** unset.

**Links:** attach the source as `{url, title}`, with a title that names the origin, for example `Chat: sales channel, Sam, Aug 21`. The link is how an engineer finds out later what the customer meant.

## Step 5: Write a description worth reading

An empty description costs someone a round of digging before the work can be scoped. A few sentences of real context is the cheapest quality win here.

```markdown
## What is being asked for
[One or two plain sentences. What could the customer do that they cannot do today?]

## Who is asking
[Customer or prospect names, with deal context if known: prospect or live customer, and what the ask blocks.]

## What we know about scope
[Sync direction, objects involved, whether the vendor has a public API. Only what the source said.]

## Open questions
[What someone must answer before this can be scoped.]

## Source
[Where this came from, with a link.]
```

Quote the customer word for word where you can. A paraphrase of a paraphrase is how requirements drift. Keep open questions open. "Unclear whether they need bill sync or only expense categories" is useful. A confident guess sends someone building the wrong thing.

Set `summary` too: one line, under 255 characters. It is what most people will read.

## Step 6: Clean up the prose

Run `/anti-ai` (the [Remove AI Writing Patterns](../../stakeholder-communication/remove-ai-writing-patterns/) prompt) on the description and summary and apply the changes. Watch for bolded list lead-ins, "it's not just X, it's Y" framing, and three-part sentences about customer pain. Names, labels and other structured fields do not need the pass.

## Step 7: Create it

```
save_project(name, addTeams=[<team>], description, summary,
             labels=[...], state="{{BACKLOG_STATUS}}", links=[{url, title}])
```

Report the name, URL, team and labels. Say what you did not set and why, so the caller knows a PM still needs to look at it.

If you found prior art and created anyway, name it in the report. The caller may know it is the same project after all.

Once a project is ready to be specified, the next step is `/write-prd`.
