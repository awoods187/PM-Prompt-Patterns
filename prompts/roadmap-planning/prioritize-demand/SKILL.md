---
name: prioritize-demand
description: Ranks open demand projects in your issue tracker by customer needs, lost deals and open pipeline from your CRM, using a transparent weighted formula with evidence per project, delivered as a read-only spreadsheet. Use for roadmap planning, cycle planning, or "what should we build next".
---

# Prioritize demand

> **Setup:** workspace values (labels, north stars, the priority segment, CRM field names) come from your factory config. See [`factory-config.example.md`](../../../templates/factory-config.example.md). Tool calls below use Linear and HubSpot MCP names as an example of how the issue tracker and CRM roles are filled. Weights are examples to tune.

Demand piles up in the issue tracker as customer needs. Money moves in the CRM as won and lost deals. Nobody reads the two together, so planning runs on whoever spoke last. This skill joins them and ranks every open demand project by a formula anyone can check.

It serves `{{NORTH_STAR_1}}`. A gap that loses deals in `{{PRIORITY_SEGMENT}}` outranks one that only annoys a prospect.

The ranking is an input to planning, not the plan. You recommend. The PM and product leadership decide. This skill never edits the tracker or the CRM.

## Scope

**Ranks:** every project in a planned or backlog status that has at least one customer need, or carries `{{CUSTOMER_GAP_LABEL}}` or a sales origin label, across all teams.

**Listed, not ranked:** projects already in progress that have customer needs. Finishing a started feature beats starting a new one, so show these in their own section with their demand. Nobody should start something new while these stall.

**Out of scope:** changing project priority, status or labels; attaching customer needs (that is `/sales-request`); estimating effort.

## The formula

Each project gets points from the sources below, then at most one principle multiplier. Show every component in the output so anyone can recompute the score.

| Source | Points (example weights) |
| --- | --- |
| Active customer with a need on the project | 5 each |
| Prospect with a need and no matched open or lost deal | 1 each |
| Lost `{{PRIORITY_SEGMENT}}` deal (product reason, last 12 months) | 4 each, plus 1 per $25k of deal amount |
| Lost deal in any other segment (same rules) | 2 each, plus 1 per $50k |
| Open `{{PRIORITY_SEGMENT}}` deal whose company has a need on the project | 3 each, plus 1 per $25k of weighted amount |
| Open deal in any other segment (same rules) | 1.5 each, plus 1 per $50k of weighted amount |

**Principle multiplier (×1.5, at most one):** the project finishes the missing part of an area you already ship, listed in `{{DEEPEN_AREAS}}`. "Deepen before you widen." State the reason in one line. Everything else is ×1.0.

**Definitions** (field names come from the factory config):

- **Priority segment deal:** `{{CRM_SEGMENT_FIELD}}` marks it as `{{PRIORITY_SEGMENT}}`.
- **Lost deal:** closed lost, close date in the last 12 months and not in the future, and `{{CRM_LOST_REASON_FIELD}}` is one of `{{CRM_PRODUCT_LOSS_REASONS}}`.
- **Open deal:** not closed. Use `{{CRM_WEIGHTED_AMOUNT_FIELD}}`.
- **Amounts:** use `{{CRM_AMOUNT_FIELD}}` in one currency. Round each per-dollar component down.
- A deal counts once per project. If one company has needs on several projects, its deal counts toward each, and the output says so.

To change a weight, change this table and nothing else.

## Step 1: Pull the projects and demand

1. `list_projects` for planned and backlog statuses, then again for in progress. Keep id, name, team, lead, status, labels, summary.
2. For each project, `list_customer_needs(project=...)`. Keep the customer, the need text, the source link and the date.
3. For each customer, read its status (active or prospect) and domains with `list_customers`.

## Step 2: Match customers to the CRM

For each customer, find the CRM company, then its deals:

1. **Domain match (high confidence):** a CRM company whose domain equals a tracker customer domain.
2. **Name match (low confidence):** exact company name, when there is no domain. Mark it low.
3. **No match:** the customer scores as active or prospect, with no deal points.

For matched companies, pull their deals with the fields in the definitions above, plus the deal name, stage, close date and `{{CRM_LOST_DETAIL_FIELD}}`.

A lost deal counts toward a project only if its loss reason is a product reason. If the lost detail names something unrelated to the project, still count it, but note it. The PM may decide the deal was lost for another gap.

## Step 3: Find demand not yet in the tracker

Search lost deals (same definition) whose `{{CRM_LOST_DETAIL_FIELD}}` mentions a project's capability, where the company has no need on that project. Do not score these. List them as "demand not yet in the tracker" and offer `/sales-request` to attach them. This is how the ranking gets more honest over time.

## Step 4: Score and rank

Apply the formula. Sort by score, highest first. Break ties by priority-segment lost-deal points.

Write one recommendation line per project from the evidence. For example: "Top 5 and unscheduled: consider for the next cycle." "Demand is one low-confidence prospect: validate before scheduling." "Scheduled but low demand: confirm why it is planned."

Before showing anything, recompute three projects by hand from their component columns and confirm the totals match.

## Step 5: Deliver as a spreadsheet

Create a read-only sheet in `{{SPREADSHEET}}`, or an .xlsx file if that is not available. Tabs:

1. **Ranking:** rank, project (linked), team, lead, status, score, multiplier and reason, active customers, prospects, lost priority-segment deals (count and $), other lost deals, open priority-segment pipeline (count and weighted $), other open pipeline, match confidence, recommendation.
2. **In progress:** committed projects with their demand, not ranked.
3. **Evidence:** one row per need and deal: project, customer, need text, source link, CRM company, deal, stage, amount, loss reason, segment, match method and confidence.
4. **Not yet in the tracker:** the unlinked lost deals from Step 3.
5. **Data quality:** customers with no domain, low-confidence name matches, deals with no segment, lost deals with no reason. Each is a fix for whoever owns that data.
6. **Weights:** the formula table, the definitions and the run date.

Then reply with the top ten in a short table, the three biggest data-quality gaps, and the link.

## Rules

- Read-only. Never change the tracker or the CRM.
- Never invent a match. A customer without a confident match gets no deal points.
- Show your work. Every score is the sum of visible columns.
- Customer names and deal amounts are internal. The sheet stays private unless the user shares it.
- The top-ranked projects go next to `/write-prd`.
