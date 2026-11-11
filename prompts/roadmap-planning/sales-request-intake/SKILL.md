---
name: sales-request
description: Turns a raw team chat message from sales or CX about what a customer or prospect asked for into tracked demand in your issue tracker. Checks your docs for whether the capability already shipped, creates the customer if needed, finds or creates a project per request via /file-project, attaches a customer need so demand accumulates on the right project, and ends with a paste-ready reply telling the rep what was logged and what to tell the customer. Use whenever someone pastes or points to a sales, CX or call note listing integrations, features or gaps a customer mentioned, even if they only say "here's what acme asked for", "notes from the intro call", "can you get these tracked", or just drop the message. Use it especially for a bare list of vendor names next to a company name. Not for bugs; /file-bug owns those.
---

# Log a sales request as demand

> **Setup:** workspace values (labels, teams, your docs site, your team chat) come from your factory config. See [`factory-config.example.md`](../../../templates/factory-config.example.md). Tool calls below use Linear MCP names as an example of how the issue tracker role is filled. Every company and vendor name here is fictional.

Sales hears the same six requests in a hundred calls. None of it reaches the roadmap unless someone logs it. That is the value here. A message that would have scrolled away becomes demand on a project. When a PM asks "who wants Initech Expense?", the answer is a list of names.

Getting it wrong is worse than not doing it. A made-up customer, a duplicate project, or a request logged against the wrong vendor pollutes the data that `/prioritize-demand` ranks. So the work is mostly careful reading and searching, and only briefly writing.

You act without asking for confirmation. This runs mid-conversation, and a gate would defeat the point. That is why the checks below matter, and why the two truly ambiguous cases in Step 8 stop instead of guessing.

## Step 1: Read the message for what it actually says

Pull out:

- **The customer or prospect.** Usually a company name in the first line.
- **What they asked for.** Often a bare list of vendor names. Sometimes prose with the asks buried inside.
- **Where it came from.** Who wrote it, when, and the message link if you have it.
- **Deal context.** "On an intro with" means prospect. "Our quarterly review with" means live customer.

Sales writes fast. Expect lowercase names, vendors spelled by ear, no punctuation. Normalize as you go, using each vendor's own capitalization.

Watch for two things:

**Not every vendor named is a request.** "They're moving off Hooli Pay" describes their stack. "The integrations they mentioned were..." is an ask. When the framing is unclear, treat it as an ask and say so in your report. A logged non-request is cheap to close. A missed request is invisible forever.

**Not every ask is an integration.** "They need approval chains on bills" and "single sign-on with their identity provider" are product requests that happen to name companies. `/file-project` handles that. Just do not assume the whole list is connectors.

## Step 2: Check what already exists

Start with your docs site (`{{DOCS_SITE}}`). If it publishes a page index (`{{DOCS_INDEX}}`), use it. It is the fastest way to learn whether the product already does the thing.

Some fetch tools only open URLs that appeared in the conversation or in an earlier search result. If so, get there in hops: search for the docs site, open a docs page, then follow its link to the index. Some indexes are nested. Check every level before deciding a vendor is missing.

If the docs check fails, carry on. Say at the top of the report that it did not run and why, and ask the user to paste a docs link. Do not fill the gap from a project description in the tracker. Those are written by one person on one day and can be wrong.

Read the full index, not a getting-started page. Marketing pages list a few headline integrations and will tell you a shipped vendor is missing.

Search the docs for **every** ask, not only vendor names. Product features ship too, often under settings or configuration.

Then search tracker **issues**, not only projects:

```
list_issues(query="<vendor or capability>", fields=["title","team","status","project","url","createdAt","labels"], limit=15)
```

Open and recently closed issues change the answer. A capability can have a doc page while an open issue records the exact limit the customer will hit. A feature can look missing because of a bug fixed two weeks ago. The rep needs both.

### Does "shipped" settle it?

A doc page usually means no project and no need. It goes in the report with the link, because the rep may be about to tell a customer "not yet".

But a doc page proves a capability exists, not that it covers what this customer meant. Compare how specific the ask is with how specific the docs are:

- **Bare vendor name, and the docs cover that vendor.** Shipped settles it. Report and move on.
- **The ask is more specific than the docs.** The customer named a cadence, a direction, a volume, or called it a hard requirement, and the docs do not cover that. Shipped does not settle it.
- **The ask is vaguer than the docs.** "Something for consolidated reporting" cannot be checked against a page. They may be covered, or they may be pointing at a gap nobody has named.

In both unsettled cases, attach a need to the nearest **open** project and say exactly where the shipped capability and the ask differ. A need on an open project costs nothing. A hard requirement on a live deal that left no trace is gone.

If the only match is a closed or canceled project, do not attach the need there. Hand it to `/file-project` as new work and say why.

Two traps:

**Category adjacency.** One expense tool being supported does not mean another is. Match the vendor, not the category.

**Competitors are ordinary requests.** A vendor that overlaps one of your modules still gets logged like any other. Whether to replace it or connect to it is a product call. Do not turn the ask into a strategy debate in the report.

## Step 3: Find or create the customer

```
list_customers(query="<distinctive word from the company name>", includeNeeds=true)
```

Search the distinctive word, not the full legal name. Then search the domain if you have one. Read results before matching. Near-identical names can be different companies. One plausible hit means use it. A hit that shares a domain with the request settles it.

No match means create:

```
save_customer(name="<Proper Name>", domains=["<domain>"], status="Prospect" or "Active")
```

`Prospect` for an intro, demo or evaluation. `Active` for a live customer.

Set the domain only if you can confirm it with a web search. Do not assume the obvious form. The domain is what CRM sync matches on later. A guessed domain breaks that matching. If you cannot confirm it, leave it blank and say so.

Do not invent revenue or size.

## Step 4: Find or create a project per request

For each remaining request, invoke **`/file-project`**. It owns searching, naming, routing, labels and the description, including inconsistent project names and misleading substring matches.

Pass it the customer, the verbatim ask, the deal context and the source link. Tell it the request came from sales, so it applies the sales origin label and `{{CUSTOMER_GAP_LABEL}}`.

When it finds an existing open project, use it. That is the good outcome. The second customer asking for the same thing is the signal that moves it up the roadmap, and it only counts if it lands on the same project.

## Step 5: Attach the customer need

This step makes the rest worth doing. A project with no needs looks like one person's idea. A project with six needs is a business case.

```
save_customer_need(customer=<customer>, project=<project>,
                   body="<the ask, in their words, plus context>",
                   source="<message link>")
```

Write the body as what the customer said and why. Not a restatement of the project name. For example: *"Named Initech Expense among five integrations they'd need. Prospect, intro call Aug 21. Not yet clear whether they need bill sync or only receipt import."*

Keep their phrasing and keep the uncertainty.

Need priority in this example tracker is binary: `0` is not important, `1` is important. It is not the issue priority scale. Use `1` only when the message says the deal depends on it ("blocker", "requirement", "can't move forward without"). A prospect listing five integrations in passing is not calling all five blockers.

Before attaching, check the needs returned in Step 3. If this customer already has a need on this project, update it. Duplicate needs inflate the count that prioritization runs on.

## Step 6: Record what you learned, not only what was asked

Checking docs and issues turns up findings nobody asked for: a capability that works but is undocumented, a doc page that describes something the product does not do, a limit the next customer will also hit. These are easy to lose, because their obvious home is a paragraph in your report.

Give each finding a home:

- **The docs are wrong or silent about something that works.** Note it in the need body. Say plainly in the report that the docs caused the confusion.
- **You suspect a defect, not a missing feature.** Say so, name the evidence, and hand it to `/file-bug`. Do not file it yourself. A request logged as a feature gap when the feature is broken is the expensive mistake.
- **A limit that will hit others.** Write it into the need body as a stated constraint.

Do not edit, reprioritize, reroute or rename other people's issues and projects, even when you think they are wrong. Surface it and let the owner decide.

## Step 7: Clean up the prose

Run `/anti-ai` (the [Remove AI Writing Patterns](../../stakeholder-communication/remove-ai-writing-patterns/) prompt) on everything you wrote in your own voice: project descriptions, need bodies, the report, and the reply in Step 10. Leave verbatim customer quotes exactly as said. Names, labels and statuses are not prose.

## Step 8: Stop only for these two things

1. **Several plausible customer matches, none decisive.** A duplicate customer splits that company's history. Show the candidates and ask.
2. **You cannot tell who the customer is**, or the message has no identifiable asks. Say what you see and ask.

Decide everything else and report it. Unsure whether something is an ask? Log it and flag it. Unsure which team owns it? `/file-project` routes it to `{{PRODUCT_TEAM}}`.

## Step 9: Report what happened

One table, one row per request:

```markdown
**Acme Co**, new prospect, created in the tracker

| Request | Status | Action taken |
|---|---|---|
| Hooli Payroll | Already shipped | None. Docs: <link> |
| Initech Expense | Existing project | Need attached to Initech Expense Integration <link> |
| Umbrella Planning | New | Created Umbrella Planning Integration <link>, need attached |
```

Use `Shipped, with a gap` for the unsettled cases from Step 2, and say what the gap is in one line: *"Warehouse export ships but runs once, with no scheduled refresh (PROJ-123). They called this a hard requirement, so need attached."*

Then, briefly:

- anything you read as an ask that might not be one
- any near-miss project you judged to be different work, and why
- any open issue that changes what the rep should say
- what no human has set yet: priority, lead, dates, release label

Close with one sentence the rep can use with the customer, caveats included. "Hooli Payroll connects today, one entity per connection" is useful. "Hooli Payroll works" sets up a broken promise.

## Step 10: Draft the reply for the rep

End with a message the user can paste into the rep's thread in `{{TEAM_CHAT}}`. The report is for whoever ran this skill. The reply is for the rep, who needs to know two things: it is logged, and what to tell the customer. Put it in a fenced `text` block so it pastes as plain text.

- One opening line: it is logged, plus anything surprising, such as the request already being tracked.
- One `•` line per request: the vendor, the outcome in plain words (works today, already on the roadmap, newly logged), and the link.
- One line starting `What you can tell <Customer>:` with the sentence from Step 9.
- At most one question back, only if the answer would change scoping. Skip it if there is nothing worth asking.

Keep it under about 120 words. Chat tools often do not render tables or headers, so use bare URLs and `•` bullets. Leave out internal detail (need IDs, unset fields, label names). Never imply a timeline. "In the roadmap backlog" is accurate. "Coming soon" is a promise nobody made.

## Worked example (fictional)

Input:

```text
Sam [4:12 PM]
intro call with acme co today. integrations they mentioned:
initech expense, hooli payroll, umbrella planning. initech is a must have before they sign
```

Reading it: the customer is **Acme Co**, a **prospect** ("intro call"). "Integrations they mentioned" is an explicit ask, so all three count. Only Initech Expense carries blocker language ("must have before they sign"), so only its need gets priority `1`.

Docs check: the index lists **Hooli Payroll**. It shipped, and the ask is a bare vendor name, so shipped settles it. No project, no need. It goes in the report with the doc link. An issue search shows an open limit of one entity per connection, so the rep hears that caveat.

Customer: `list_customers(query="Acme")` returns nothing. Create `Acme Co` as a Prospect. A web search confirms the domain, so set it.

Projects: `/file-project` searches "Initech" and finds an open `Initech Expense Integration` project. Attach the need there. It searches "Umbrella" and finds `Planning Grid (Umbrella style)`, a planning feature that borrowed a layout, not an integration. That is a near miss, not the same work, so it creates `Umbrella Planning Integration` and names the near miss in the description.

Reply:

```text
Logged, thanks. Initech Expense was already tracked, so Acme Co is now attached to that project.
• Initech Expense: on the roadmap backlog, Acme Co attached as a must-have: <project link>
• Hooli Payroll: works today, one entity per connection: <docs link>
• Umbrella Planning: newly logged: <project link>
What you can tell Acme Co: Hooli Payroll connects today for one entity per connection. Initech Expense and Umbrella Planning are logged against their account.
One question if it comes up: does Acme need Initech bill sync, or only receipt import?
```
