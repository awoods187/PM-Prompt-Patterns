# Prioritize Demand (Claude Code Skill)

## 🎯 Purpose

**Rank every open demand project by customer needs, lost deals and open pipeline, with a formula anyone can recompute.**

Joins customer needs in your issue tracker with won, lost and open deals in your CRM. Scores each project with visible weights, flags lost deals whose demand never reached the tracker, and delivers a read-only spreadsheet with the evidence behind every score.

Part of the [product factory](../../../README.md#-product-factory).

**Business Value**:
- Planning runs on evidence instead of whoever spoke last
- Every score is a sum of visible columns, so disagreements are about weights, not data
- Data-quality gaps (missing domains, missing loss reasons) surface as a fix list

**Use Cases**:
- Cycle or quarterly planning
- "What should we build next?"
- Checking whether a planned project has any demand behind it

**Complexity**: 🔴 Advanced

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt. Everything is in [`SKILL.md`](./SKILL.md).

## 🔧 Requirements

- **Issue tracker** connector with projects, customers and customer needs. The skill uses Linear MCP tool names as an example (`list_projects`, `list_customer_needs`, `list_customers`).
- **CRM** connector with companies and deals (for example HubSpot or Salesforce)
- A spreadsheet tool, or the ability to write an .xlsx file
- Companion skill: [`/sales-request`](../sales-request-intake/) to attach demand found only in the CRM

## 🚀 Setup

1. Copy this folder to `~/.claude/skills/prioritize-demand/` (or your project's `.claude/skills/`).
2. Fill in [`factory-config.example.md`](../../../templates/factory-config.example.md): `{{NORTH_STAR_1}}`, `{{PRIORITY_SEGMENT}}`, `{{DEEPEN_AREAS}}` and every `{{CRM_*}}` field name.
3. Tune the weights in the formula table. Change the table and nothing else.

## 💡 Design Notes

- **Read-only.** It recommends. People decide.
- **No invented matches.** A customer without a confident CRM match gets no deal points.
- **In-progress work is listed, not ranked**, so new work doesn't start while committed work stalls.
- **Sanity check.** Three scores are recomputed by hand before anything is shown.
