# Worked example: the Northwind Solar message

This message is a good teaching case because six vendors produce three different outcomes and two of them are traps. The company, rep, workspace, and project history are fictional.

## Input

```
Sam  [5:48 PM]
On an introduction with northwind Solar today, the following were the
integrations they mentioned:
Coupa, Pigment, anaplan, airbase, travelperk, adp.
```

## Reading it

Customer is **Northwind Solar**, normalized from `northwind Solar`. "On an introduction with" makes them a **prospect**, not a live customer.

"The following were the integrations they mentioned" is explicitly an ask, so all six count. Six vendors, normalized to their own capitalization: **Coupa, Pigment, Anaplan, Airbase, TravelPerk, ADP**.

Source is Sam's message. Get the permalink if you have it; if the message was pasted with no link, record it as `Slack: Sam, Aug 21` and say in the report that the source link is missing.

## Docs check

Following the hops in Step 2 (docs homepage, then the page index, then the product-features sub-index), the index lists **ADP** under Payroll and HR. It shipped.

That is the entire outcome for ADP: no project, no need, no Linear write of any kind. It appears in the report with the doc link, because Sam is about to answer a prospect and the useful thing to hand them is proof it already works.

ADP is the clean case, and it is clean **because the ask is a bare vendor name**. Northwind said "ADP" in a list, the docs say ADP, and there is nothing left to reconcile. Had Sam written "they need ADP syncing per-employee, not one consolidated JE", the doc page would no longer settle it, because the shipped integration posts one consolidated entry per pay run. Read the ask against the page, not just the vendor against the index.

The other five have no doc page. Note that **Airbase does not**, even though **Divvy** does. Both are spend-management tools and the temptation is to read the category as covered. Match the vendor.

An issue search is worth running on the shipped one too. If ADP has open issues about sync reliability, Sam should know before promising it, and one line in the report saves a bad conversation later.

## Customer

`list_customers(query="Northwind", includeNeeds=true)` returns nothing. Create:

```
save_customer(name="Northwind Solar", status="Prospect")
```

No domain, because none was given and `northwind.com` would be a guess. A wrong domain silently breaks the CRM matching that populates these records later, which is worse than a blank field.

## The five projects

**Coupa**: searching `Coupa` returns a project named exactly `Coupa`, in Backlog, on the Product triage team, labeled `Customer Gap`. Open and the same work, so no new project. This is the case that makes the bare-noun search rule earn its keep: a search for "Coupa Integration" returns nothing and you would have duplicated a project that already exists.

Do not rename it to fit the convention. Renaming other people's projects as a side effect of logging a request is a surprise nobody asked for.

**Airbase**: searching `Airbase` returns `Airbase integration`, Backlog, Integrations team, `Customer Gap`. Same work. Attach the need.

**Pigment**: searching `Pigment` returns `Planning Grid (Pigment Style)`: Completed, Reporting team. Read it and it is a planning feature built in the style of a competitor's UX, with nothing to do with connecting to Pigment. Different work, so **create** `Pigment Integration`.

Mention the near miss in the new project's description anyway. Somebody who knows that history should get the chance to say the two are related.

Pigment is also a partial competitor: it does planning and forecasting, which overlaps the product's own planning module. That is not a reason to withhold the project or to write a paragraph asking whether Northwind really wants a connector. Log the request they made. If product decides the better answer is to sell them the native module, they can decide that from a project that exists.

**Anaplan**: no hits. Create `Anaplan Integration`.

**TravelPerk**: no hits. Create `TravelPerk Integration`.

All three new ones go to the **Integrations** team, `Backlog`, labels `Customer Gap` and `Sales Request`. No priority, no lead, no dates, no release label.

## A new project's description

```markdown
## What is being asked for
Sync between [Product] and Anaplan so the FP&A team can pull actuals
without a manual export.

## Who is asking
Northwind Solar, prospect. Named Anaplan among six integrations they
would want in place, on an intro call 21 Aug 2026. Not stated as a
deal blocker.

## What we know about scope
Direction unknown. Anaplan is FP&A, so the likely shape is a one-way
export of actuals and dimensions, but the call notes do not say.

## Open questions
- Read-only export, or does Anaplan need to write budgets back?
- Which dimensions do they plan on: entity, class, department?
- Is this a requirement for the deal or a nice-to-have?

## Source
Slack, Sam, 21 Aug 2026, [permalink]
```

The open questions carry most of the value. Three honest unknowns are what a PM needs; three invented answers send an engineer down the wrong path with false confidence.

## A customer need body

On the Coupa project:

> Northwind Solar (prospect) named Coupa among six integrations they would
> need, on an intro call 21 Aug 2026. No detail yet on whether they need PO
> sync, invoice sync, or both.

Not `"Coupa integration"`. The project name already says that. The body exists to carry who, when, how firm, and what is still unknown.

`priority` stays unset. Six vendors listed conversationally on an intro call is not six blockers, and marking them so drains the field of meaning for the requests that really are.

## Report

```markdown
**Northwind Solar**, new prospect, created in Linear

| Request | Status | Action taken |
|---|---|---|
| ADP | Already shipped | None. Docs: /integrations/payroll-and-hr/adp |
| Coupa | Existing project | Need attached to Coupa |
| Airbase | Existing project | Need attached to Airbase integration |
| Pigment | New | Created Pigment Integration, need attached |
| Anaplan | New | Created Anaplan Integration, need attached |
| TravelPerk | New | Created TravelPerk Integration, need attached |

ADP already works, so Northwind can be told that today.

One judgment call: searching Pigment surfaced Planning Grid (Pigment
Style), a completed planning feature that borrowed Pigment's UX. I read
that as different work and created a separate integration project. Worth
a look if you know that history.

Nothing has a priority, lead, target date, or release label. All three
new projects sit in the Integrations backlog for a PM to triage.
```

## Slack reply

```text
Logged, thanks Sam. Five of the six are on the roadmap now, and ADP already works.
• ADP: works today. https://docs.example.com/integrations/payroll-and-hr/adp
• Coupa: already on the roadmap, Northwind added: <Linear URL>
• Airbase: already on the roadmap, Northwind added: <Linear URL>
• Pigment: newly logged: <Linear URL>
• Anaplan: newly logged: <Linear URL>
• TravelPerk: newly logged: <Linear URL>
What you can tell Northwind: ADP connects today and posts each pay run as journal entries. The other five aren't built yet, and their requests are logged against their account.
```

The ADP line carries the docs link because it is the one Sam can act on today. The rest tell Sam where the request lives without dressing it up.

## What makes this case hard

Five vendors, five different reasons for the outcome:

- ADP: shipped, and a getting-started page would have said otherwise
- Coupa: exists under a name the obvious search misses
- Airbase: exists, and its category neighbor being shipped is a red herring
- Pigment: a search hit that is not the same work
- Anaplan and TravelPerk: the easy path

A run that creates six projects has failed. So has one that creates two and skips Pigment because something matched.
