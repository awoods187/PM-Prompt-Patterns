---
name: "sales-request"
description: Turns a raw Slack message from sales or CX about what a customer or prospect asked for into tracked demand in Linear. Checks the product docs to see whether the capability already shipped, creates the customer if Linear does not have them, finds or creates a project per request via /file-project, attaches a customer need so demand accumulates against the right project, and ends with a copy-paste Slack reply telling the rep what was logged and what to say to the customer. Use this whenever someone pastes or points to a sales, CX, or call note listing integrations, features, or gaps a customer mentioned, even when they do not say "Linear" or "log this" and only say things like "here's what northwind asked for", "notes from the intro call", "these came up on the demo", "can you get these tracked", or just drop the message. Use it especially for a bare list of vendor names attached to a company name. Do not use it for bugs; /file-ticket owns those.
---

# Log a sales feature request into Linear

> **Setup:** replace `[Product]` with your product name and `docs.example.com` with your public docs site. Team names, labels, and examples below are from a fictional workspace; swap in your own.

Sales hears the same six requests in a hundred calls and none of it reaches the roadmap unless somebody does this data entry. That is the whole value here: a message that would have scrolled away becomes demand attached to a project, so that when a PM asks "who wants TravelPerk", the answer is a list of names instead of a shrug.

Getting it wrong is worse than not doing it. A fabricated customer, a duplicate project, or a request logged against the wrong vendor pollutes the exact dataset that prioritization depends on. So the work is mostly careful reading and searching, and only briefly writing.

You act without asking for confirmation. That is deliberate; this runs mid-conversation and a gate would defeat the point. It is also why the checks below matter, and why the two genuinely ambiguous cases in Step 8 stop rather than guess.

## Step 1: Read the message for what it actually says

Pull out:

- **The customer or prospect.** Usually a company name in the first line.
- **What they asked for.** Often a bare comma-separated list of vendor names, sometimes prose with the asks buried in it.
- **Where it came from.** Who wrote it, when, and the Slack permalink if you have it.
- **Deal context.** "On an introduction with" means prospect. "Our QBR with" means live customer. This changes nothing about what you create and a lot about how the description reads.

Sales writes fast and correctly so. Expect lowercase company names, vendor names spelled by ear, and no punctuation. Normalize as you go: `northwind solar` is Northwind Solar, `anaplan` is Anaplan, `travelperk` is TravelPerk. Use the vendor's own capitalization, because a project called `anaplan` is harder to spot in a list and reads as though nobody was paying attention.

Two things to catch while reading:

**Not every named vendor is a request.** "They're moving off Bill.com" and "their FP&A team lives in Anaplan" describe a stack, not an ask. "The following were the integrations they mentioned" is an ask. When the framing is genuinely ambiguous, treat it as an ask and say in your report that you read it that way, since a logged non-request is cheap to close and a missed request is invisible forever.

**Not every ask is an integration.** A list of vendor names usually is. But "they need approval chains on bills" and "SSO with Okta" are product requests that happen to name companies, and they route differently. `/file-project` handles that distinction; just do not assume the whole list is connectors.

## Step 2: Check what already exists before touching Linear

Start from the docs site at `https://docs.example.com/` and work down to an index of every published page (many docs platforms publish one at `/llms.txt`). That index is the fastest way to find out whether [Product] already does the thing being asked for.

You may not be able to jump straight to the index. Some fetch tools only open URLs that appeared in the user's message or in an earlier search or fetch result, and a URL written in this skill counts as neither, so fetching `llms.txt` cold can fail with a permissions error. If so, get there in hops:

1. If the user's message contains any docs link, fetch it. Otherwise web search for your docs site and fetch the homepage or any docs result.
2. Follow the link to the page index from there.
3. If the index is split into sub-indexes (for example, developer docs at the top level and product features one level down), fetch the relevant sub-index and search it for each ask. A vendor missing from the top-level index is not evidence of anything until you have checked the sub-indexes.

If the hops fail, carry on with the rest of the run rather than stopping. Say at the top of the report that the docs check did not run and why, and ask the user to paste the docs URL so you can finish it. Do not fill the gap from a Linear project description. Those are written by a person on one day and can be wrong: a project description may say one payment provider is the only one supported while another has had its own docs page for months.

Read the index, not a getting-started page, even when a search lands you there on the way. Getting-started pages tend to feature a handful of marquee integrations, so checking one will tell you a vendor is missing when it has a shipped doc page.

Search it for **every** ask, not just the vendor names. Non-integration requests ship too and they live outside the integrations section: approval chains and multi-entity consolidation are usually documented under configuration or settings pages. Skipping the docs on a product request is how you end up filing a project for something that shipped last quarter.

Then search Linear **issues** too, not only projects:

```
list_issues(query="<vendor or capability>", fields=["title","team","status","project","url","createdAt","labels"], limit=15)
```

There is no `identifier` field on this tool and passing one fails the whole call, so read the identifiers off the `url` values instead.

This is worth the extra call because in-flight and recently-closed issues change the answer in ways a project search cannot see. A capability can have a doc page while an open issue records the exact limitation the customer is about to hit, and a feature can look broken to a customer because of a bug fixed two weeks ago rather than because it does not exist. Both are things the rep needs.

### Does "shipped" settle it?

A published doc page usually means do nothing in Linear: no project, no need. It goes in the report with the doc link, because the rep is often about to tell a customer "not yet" and the useful thing to hand them is the page proving otherwise.

But a doc page proves a capability exists, not that it covers what this customer meant. So compare the **specificity of the ask against the specificity of the docs**:

- **The ask is a bare vendor name and the docs cover that vendor.** Shipped settles it. ADP in a list of six vendor names, with an ADP doc page, is done. Report and move on.
- **The ask is more specific than the docs.** The customer named a cadence, a direction, a volume, or called it a hard requirement, and the doc page does not speak to that. Shipped does not settle it. Say a data-warehouse export has a doc page, and an open issue says the export runs once with no scheduled refresh and no customer-facing trigger: a prospect calling that export a hard requirement is asking for something that does not exist yet.
- **The ask is vaguer than the docs.** "Something for multi-entity consolidation reporting" is not a claim you can check against a page that describes consolidated statements. The vagueness is the point: either they are already covered or they are pointing at a gap nobody has named, and you cannot tell which from a Slack message.

In both of the unsettled cases, attach a need to the nearest **open** project and say in your report exactly where the shipped capability and the ask diverge. A need on an open project costs nothing and closes in one click; a hard requirement on a live deal that left no trace anywhere is unrecoverable.

If the only matching project is `Completed` or `Canceled`, do not attach the need there. A closed project is a decision that was already made, and hanging new demand on it hides the demand. That situation is evidence this is new work, so hand it to `/file-project` as a fresh request and say why in the description.

Two traps in this step:

**Category adjacency.** Airbase is not shipped just because Divvy is, even though both are spend-management tools. Match the vendor, not the category.

**Competitors are ordinary requests.** Some vendors overlap a module of your own. If a prospect asks for a connector to a planning tool that competes with your planning module, and a shipped project called `Planning Grid (Pigment Style)` borrowed that tool's UX, log it as a request anyway, like any other vendor. Whether you would rather replace that product than connect to it is a commercial call that belongs to product, and turning the ask into a philosophical question in your report costs the rep a round trip to learn nothing.

## Step 3: Find or create the customer

```
list_customers(query="<company name>", includeNeeds=true)
```

Search the distinctive word rather than the full legal name: "Northwind" finds more than "Northwind Solar Inc." Then search the domain if you have one, since the same company sometimes exists under a shorter name.

Read the results before matching. Records like `Acme` and `acmeinc` can be two separate customer records, and near-identical names can be genuinely different companies. When there is exactly one plausible hit, use it. When a hit shares a domain with the request, that settles it.

No match means create:

```
save_customer(name="<Proper Name>", domains=["<domain>"], status="Prospect" or "Active")
```

`Prospect` when the message describes an intro, a demo, or an evaluation. `Active` when they are a live customer.

Set `domains` if you can establish the real one, and web search for it rather than assuming the obvious form. A company's domain is often not just its short name plus `.com`, and the domain is what CRM sync matches on later, so a blank field quietly breaks that matching and a guessed one breaks it worse. If a search does not settle it, leave it blank and say so.

Do not invent revenue or size.

## Step 4: Find or create a project per request

For each remaining request, invoke **`/file-project`**. It owns the searching, naming, routing, labeling, and description, including the two traps that bite hardest here: projects named inconsistently (plain `Coupa` exists, so a search for "Coupa Integration" finds nothing) and substring matches that are different work (`Planning Grid (Pigment Style)` is not a Pigment integration).

Pass it the customer, the verbatim ask, the deal context, and the source link, and tell it the request came from sales so it applies `Sales Request` and `Customer Gap`.

When `/file-project` finds an existing open project, use it. That is the good outcome, not a failure: the second customer asking for Airbase is the signal that moves it up a roadmap, and it only registers if it lands on the same project as the first.

## Step 5: Attach the customer need

This is the step that makes the whole thing worth doing. A project with no needs attached looks like one person's idea; a project with six needs attached is a business case.

```
save_customer_need(customer=<customer>, project=<project>,
                   body="<the ask, in their words, plus context>",
                   source="<Slack permalink>")
```

Write the body as what the customer said and why, not as a restatement of the project name. `"Coupa integration"` on the Coupa project tells a reader nothing they did not already know. Something closer to: *"Named Coupa among six integrations they'd need in place. Prospect, intro call Aug 21, evaluating alongside their existing procurement stack. Not yet clear whether they need PO sync or invoice sync."*

Keep the customer's phrasing where you have it, and keep the uncertainty. "Not yet clear whether" is more useful to whoever scopes this than a confident guess about which direction the sync runs.

A customer need's `priority` has exactly two values: `0` is Not important and `1` is Important. It is not the 0-to-4 issue priority scale, so there is no Urgent and no High here, and describing a need as Urgent in your report misrepresents what you set.

Use `1` only when the message says the deal depends on it, in words like "blocker", "requirement", "must have before", "can't move forward without". A prospect listing six integrations conversationally is not signalling that all six are blockers, and marking them so makes the field meaningless. When only one of several asks carries that language, only that one gets `1`.

Before attaching, check `includeNeeds=true` from Step 3: if this customer already has a need on this project, update it rather than adding a second. Duplicate needs inflate the count that prioritization runs on, which is the one number this whole workflow exists to make trustworthy.

## Step 6: Land what you learned, not just what was asked for

Checking the docs and the issues turns up findings nobody requested: a capability that works but is undocumented, a doc page that describes something the product does not do, a limitation the next customer will also hit. These are the most valuable things this workflow produces and they are the easiest to lose, because the obvious home for them is a paragraph in your report, and a paragraph in a report is gone by tomorrow.

So give each finding somewhere to live before you write the report:

- **The docs are wrong or silent about something that works.** Say a card connector attaches receipts to synced bills but its doc page mentions only line items, which is why a customer asked for a feature they already have. That is a docs defect. Note it in the need body and say plainly in your report that the doc page caused the confusion, so the next rep is not surprised by the same thing.
- **You suspect a defect rather than a missing feature.** Say so, name the evidence, and hand it to `/file-ticket`. Do not file it yourself; that skill exists because bug tickets need a repro and an environment you do not have. What you can do is stop the request being logged as a feature gap when it is probably broken, which is the expensive mistake.
- **A limitation that will hit others.** Say a payroll connector supports one entity per connection. If the customer's multi-entity setup makes that a blocker, that belongs in the need body as a stated constraint rather than as a conditional you leave for the rep to resolve.

The test is whether the finding survives you not being asked a follow-up question. If it only exists as "let me know and I'll file it", it does not survive.

Two things stay off limits. Do not edit, reprioritize, reroute, or clear dates on issues and projects that belong to other people, even when you are confident they are wrong; surface it and let the owner decide. And do not rename someone's existing project to match a convention.

## Step 7: Run authored prose through Remove AI Writing Patterns

Everything you wrote in your own voice gets the pass: project descriptions and summaries, customer need bodies, your report, and the Slack reply from Step 10. Apply the diffs before saving.

Two carve-outs. Verbatim customer quotes stay exactly as the customer said them, even when they are clumsy, because the quote's value is that it is theirs. And structured fields (names, labels, statuses) are not prose.

The tells this particular writing attracts are worth knowing in advance: bolded lead-ins in the scope sections, "this isn't just about X, it's about Y" framing on why a request matters, and three-part parallel sentences about customer pain. If the description reads like a pitch rather than a note, it will get skimmed, and a skimmed description is the same as an empty one.

## Step 8: Stop only for these two things

You are otherwise acting without confirmation. Two cases are worth a question, because both create records that are annoying to unwind and neither can be resolved by looking harder:

1. **Several plausible customer matches, none decisive.** Creating a duplicate customer splits that company's history in two. Show the candidates and ask which.
2. **You cannot tell who the customer is at all**, or the message has no identifiable asks in it. Say what you see and ask, rather than inventing a subject.

Everything else you decide and report. If you are unsure whether something is an ask, log it and flag it. If you are unsure which team owns a request, `/file-project` routes it to your default triage team, which is the designed answer for "not yet shaped".

## Step 9: Report what happened

One table, one row per requested vendor, so the reader can see every branch at a glance:

```markdown
**Northwind Solar**, new prospect, created in Linear

| Request | Status | Action taken |
|---|---|---|
| ADP | Already shipped | None. Docs: <link> |
| Airbase | Existing project | Need attached to Airbase integration <link> |
| Coupa | Existing project | Need attached to Coupa <link> |
| Pigment | New | Created Pigment Integration <link>, need attached |
| Anaplan | New | Created Anaplan Integration <link>, need attached |
| TravelPerk | New | Created TravelPerk Integration <link>, need attached |
```

Use a `Shipped, with a gap` status for the unsettled cases from Step 2, and say in one line what the gap is: *"Warehouse export ships but runs once with no scheduled refresh (<issue link>). They called this a hard requirement, so need attached."* That sentence is the whole reason the row exists.

Then, briefly:

- anything you read as an ask that might not be one
- any near-miss project you decided was different work, and why
- any open issue you found that changes what the rep should say, like a limitation the customer will hit or a bug fixed recently enough that they may have concluded the feature does not work
- what no human has set yet: priority, lead, dates, release label

Close by naming the shipped ones in a sentence the rep can use with the customer, with the caveats attached where there are any. "ADP connects today, single-entity only" is useful. "ADP works" sets up a broken promise.

## Step 10: Draft the Slack reply

End with a message the user can paste straight into the rep's thread. The report is for whoever ran this skill; the Slack reply is for the rep, who needs to know two things: that it is logged, and what to say to the customer. Put it in a fenced `text` code block so it copies as raw text with nothing for Slack to mangle.

Write it to the rep in plain words, the way a colleague would reply in a thread:

- One opening line saying it is logged, and naming anything surprising, such as the request already being tracked.
- One `•` line per request: the vendor, the outcome in plain words (works today, already on the roadmap, newly logged), and the Linear or docs URL.
- One line starting `What you can tell <Customer>:` with the customer-safe sentence from Step 9, caveats included.
- At most one question back to the rep, and only if the answer would change the scoping, such as which direction a sync runs. Skip it if there is nothing worth asking.

Keep it under about 120 words. Slack does not render tables or headers, and `<url|text>` link syntax does not survive a paste into the composer, so use bare URLs, `•` bullets, and no bold beyond Slack's single-asterisk `*bold*` if anything needs it. Leave out the internal detail from the report (need IDs, unset priority and lead, label names); the rep cannot act on it. Never imply a timeline. "On the roadmap backlog" is accurate; "coming soon" is a promise nobody made.

Run it through Remove AI Writing Patterns with everything else in Step 7. For a request that was already tracked:

```text
Logged, thanks. GoCardless was already tracked for Harbor Clinics from the Sept 9 demo, so no new project.
• GoCardless: not supported today. In the roadmap backlog with Harbor Clinics attached: https://linear.app/your-workspace/project/gocardless-integration-<id>
What you can tell Harbor Clinics: we don't connect to GoCardless yet. Payments come into AR through Stripe today, and their request is logged against their account.
One question if it comes up: do they need payment collection only, or payouts and fees too?
```

## Worked example

`references/worked-example.md` walks the Northwind Solar message end to end, including why Pigment gets a new project despite a search hit and why ADP gets nothing at all. Read it when a message has a mix of outcomes in it, which most do.
