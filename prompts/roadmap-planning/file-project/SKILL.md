---
name: file-project
description: Creates a well-formed Linear project from a feature request, integration ask, or chunk of work that does not yet have a home. Searches for existing projects first so demand consolidates instead of fragmenting, picks the owning team, applies the right labels, writes a description a PM can act on, and links the source. Use this whenever something needs a Linear project or a project-sized piece of work needs logging, even casually ("we should track this", "is there a project for this", "make a project for the TravelPerk ask", "where does this live"), and use it especially when a customer or prospect asks for a capability the product does not have yet. Also use it when you are unsure whether a project already exists or which Eng team would own it. Do not use it for bugs; /file-ticket owns those.
---

# File a Linear project

> **Setup:** replace `[Product]` with your product name, `docs.example.com` with your public docs site, and the team names, label names, and project examples with your workspace's. The ones below are from a fictional workspace.

A Linear project is the unit demand accumulates against. Ten customers asking for TravelPerk is a roadmap decision; ten separate records of one customer asking for TravelPerk is noise nobody can prioritize. So the highest-value thing this skill does is not creating a project. It is finding the one that already exists.

Your job is narrow: one correctly named, correctly routed, correctly labeled project, or a pointer to the one that already covers it. You are not scoping the work, estimating it, or deciding when it ships.

## Scope

**In scope:** searching for prior art, judging whether a near-match is the same work, naming, team routing, labels, status, the description, and linking the source.

**Out of scope:** writing the issues inside the project, milestones, priority, target dates, and picking a lead. Those belong to whoever plans the work. A project arriving with a guessed target date reads as a commitment nobody made.

## Step 1: Search for prior art, then read what comes back

Search the **bare noun** for the thing being asked for, not the project name you intend to create:

```
list_projects(query="<vendor or feature noun>",
              fields=["id","name","url","status","teams","labels","summary"],
              limit=25)
```

Searching the bare noun matters because project naming in most workspaces drifts before anyone standardizes it. Names like `Airbase integration`, `Add Zendesk integration`, `Plaid Integration`, and plain `Coupa` end up living side by side. A search for "Coupa Integration" returns nothing and you would create a duplicate of a project that has existed for months. A search for "Coupa" finds it.

Then read every hit and decide whether it is actually the same work. Substring matches lie in both directions:

- `Planning Grid (Pigment Style)` matches a search for "Pigment" and has nothing to do with integrating Pigment. It is a planning feature that borrowed a competitor's UX. Creating a Pigment integration project is correct here.
- A project like `Square Integration (misc)` might be a catch-all for bugs and small improvements, not the place a net-new capability request belongs. Judge by the summary and what is inside it.

Run a second search on obvious aliases before concluding nothing exists: acquired product names, the parent company, the abbreviation the team actually says out loud. `SFDC` and `Salesforce`, `Bill.com` and `BILL`, `Navan` and `TripActions`.

**Search issues as well as projects.** Work does not only live in projects, and an issue search surfaces the specific gap or limitation that a project title hides:

```
list_issues(query="<vendor or capability>", fields=["title","team","status","project","url","createdAt","labels"], limit=15)
```

There is no `identifier` field on this tool and passing one fails the whole call, so read the identifiers off the `url` values instead.

An open issue saying a data-warehouse export has no scheduled refresh tells you more about what to build than the existence of an export project does, and it belongs in the description of whatever you create. A recently-fixed bug matters too, since a customer may be asking for something that started working two weeks ago.

**Then check whether the capability already shipped.** If your docs publish a page index (for example `https://docs.example.com/llms.txt`), search it for the capability, not just the vendor, because non-integration features ship too and live outside the integrations section: approval workflows are usually documented under configuration or settings. Read the index rather than a marketing-facing getting-started page, which names a handful of marquee integrations and will tell you a vendor is missing when it has shipped docs.

### What to do with what you find

| Finding | Action |
|---|---|
| Shipped, and the ask is a bare vendor name or a plain restatement of the doc page | No project. Say so and link the page. |
| Shipped, but the ask names something the docs do not cover: a cadence, a direction, a volume, or a hard requirement | Create. Name the shipped capability in the description and state exactly where it falls short. |
| Shipped, and the ask is vaguer than the docs | Create, with the ambiguity as the first open question. "Something for consolidation reporting" cannot be checked against a page, and a guess in either direction is worse than a project that says so. |
| Same work, open project | No project. Return the existing one so the caller can attach demand to it. |
| Same work, `Completed` or `Canceled` project | Create. A closed project is a decision already made, and new demand hung on it disappears. Link it and say why this ask is different. |
| Near miss on a different surface | Create, and name the near miss in the description. Shared root causes are worth flagging. |
| Nothing | Create. |

A vendor that competes with one of your own modules is still an ordinary request. If Pigment overlaps your planning module and a shipped project borrowed its UX, file the integration project anyway. Whether you would rather displace that product than connect to it is a commercial decision, and it is not yours to make from a Slack message.

## Step 2: Name it so the next search finds it

For integrations, use `<Vendor> Integration`. For everything else, a short noun phrase naming the outcome, not the request: `Multi-currency bank feed reconciliation`, not `Customer wants multi-currency`.

The vendor's own capitalization is the right capitalization. Sales messages arrive as "anaplan" and "travelperk" and copying that through makes the project look careless and, worse, makes it harder to spot in a list. Anaplan, TravelPerk, Coupa, AvidXchange.

Keep it legible in a Linear list view, roughly 60 characters. Skip prefixes like "Add" or "Build" that add no information, and skip the requesting customer's name entirely. The customer belongs in the description and in a customer need, because the project will outlive their particular ask and a second customer asking for the same thing should not have to work out that `TravelPerk for Northwind` is where their request goes.

## Step 3: Route it to a team

Integrations go to your **Integrations** team, if one owns them.

For everything else, route by **product surface, not technical layer**, the same rule `/file-ticket` uses: a reporting request goes to the Reporting team even if the work is mostly backend. `references/routing.md` has an example surface-to-team map to replace with your own.

The map drifts, so verify against live data when the surface is not obvious. Whichever team owns *recent* projects on that surface is your answer:

```
list_projects(query="<surface noun>", fields=["name","teams","status","updatedAt"], limit=15)
```

Weight the last few months and disregard old `Completed` work, because surfaces move between teams and a stale match will route confidently to the wrong place. When a request spans surfaces or has no clear eng owner yet, your **Product** triage team is the honest home; it is where shaping happens before a team takes it.

## Step 4: Set the fields

**Status:** `Backlog`. New requests have not been planned, and any other status makes a claim about intent.

**Labels** come in two kinds. One says who is blocked, one says where the ask came from. Call `list_project_labels()` and use exact names rather than guessing between near-duplicates. An example set:

- `Customer Gap` when a named customer or prospect wants this. This is the label that makes a project show up in gap reviews, so it carries real weight.
- An origin label such as `Sales Request` or `CX Request`. If your workspace distinguishes "logged for later assessment" from "judged small enough to sprint", default to the former unless you have been told the work is small and scoped. Guessing the sprintable label puts a promise in front of a deal team.
- `Partnerships` when shipping this needs a commercial relationship with the vendor, not just engineering time.

Leave release labels alone. Those are cohorts a PM assigns during planning, and adding one silently puts unplanned work in a release.

**Priority, lead, dates:** unset. See Scope.

**Links:** attach the source. A Slack permalink, call recording, or ticket is what lets an engineer six weeks from now find out what the customer actually meant. Pass it in `links` as `{url, title}` with a title naming the origin, like `Slack: #sales-feedback, Sam, Aug 21`.

## Step 5: Write a description worth reading

Many integration projects get created with empty descriptions, which means every one of them costs someone a round of archaeology before it can be scoped. A few sentences of real context is the cheapest quality win available here.

Use this structure:

```markdown
## What is being asked for
[One or two sentences in plain terms. What would the customer be able to do that they cannot do today.]

## Who is asking
[Customer or prospect names, with deal context if known: prospect vs live customer, and what the ask blocks.]

## What we know about scope
[Direction of sync, objects involved, whether the vendor has a public API, whatever the source actually said. Only what is known.]

## Open questions
[What someone needs to answer before this can be scoped.]

## Source
[Where this came from, with a link.]
```

Two habits keep this honest. Quote the customer verbatim where you have their words, because a paraphrase of a paraphrase is how requirements drift. And keep the open questions section rather than resolving it with plausible guesses: "unclear whether they need bill sync or just expense categories" is useful, while a confidently invented answer sends someone building the wrong thing.

Set `summary` too, in one line under 255 characters. It is what shows in list views and it is the only thing most people will read.

## Step 6: Run the prose through Remove AI Writing Patterns

The description and summary are prose a human will read, and text that pattern-matches to generated filler gets skimmed rather than read, which defeats the point of writing it. Run the [Remove AI Writing Patterns](../../stakeholder-communication/remove-ai-writing-patterns/) prompt on both before saving and apply the diffs.

Watch particularly for the tells this kind of writing attracts: bolded list lead-ins in the scope section, "it's not just X, it's Y" framing about why the request matters, and three-beat parallel sentences about customer pain. Structured fields, titles, and labels do not need the pass.

## Step 7: Create it

```
save_project(name, addTeams=[<team>], description, summary,
             labels=[...], state="Backlog", links=[{url, title}])
```

Then report the project name, URL, team, and labels, and say plainly what you did not set and why, so the caller knows a PM still needs to look at it.

If you found existing prior art and created anyway, name it in your report. The caller may know something that makes them the same project after all, and they can only tell you that if you show your work.

## Reference files

- `references/routing.md` — example surface-to-team map, and how to verify it against live Linear data
