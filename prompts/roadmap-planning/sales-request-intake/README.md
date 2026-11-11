# Sales Request Intake (Claude Code Skill)

## 🎯 Purpose

**Turn a raw sales or CX chat message into tracked demand in your issue tracker.**

Reads a message like "on an intro with Acme Co they mentioned Initech Expense, Hooli Payroll, Umbrella Planning". Checks your docs for what already shipped, finds or creates the customer, finds or creates one project per request, attaches a customer need so demand accumulates on the right project, and drafts a reply the rep can paste back.

Part of the [product factory](../../../README.md#-product-factory).

**Business Value**:
- Requests that would scroll away in chat become countable demand on projects
- No duplicate projects or needs, so the counts that [Prioritize Demand](../prioritize-demand/) ranks stay trustworthy
- Reps get an immediate answer, including a docs link when the capability already exists

**Use Cases**:
- Logging integrations a prospect named on an intro call or demo
- Logging feature gaps raised in a customer review
- Answering "do we already support X?" for a rep while recording the ask

**Complexity**: 🔴 Advanced

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt. Everything is in [`SKILL.md`](./SKILL.md), including a short fictional worked example.

## 🔧 Requirements

- **Issue tracker** connector. The skill uses Linear MCP tool names as an example (`list_issues`, `list_customers`, `save_customer`, `save_customer_need`).
- **Web search and fetch** for the docs check
- Companion skills: [`/file-project`](../file-project/), [`/file-bug`](../file-bug/), [`/file-issue`](../file-issue/). Prose goes through the [Remove AI Writing Patterns](../../stakeholder-communication/remove-ai-writing-patterns/) prompt.

## 🚀 Setup

1. Copy this folder to `~/.claude/skills/sales-request/` (or your project's `.claude/skills/`).
2. Fill in [`factory-config.example.md`](../../../templates/factory-config.example.md): `{{DOCS_SITE}}`, `{{DOCS_INDEX}}`, `{{TEAM_CHAT}}`, `{{PRODUCT_TEAM}}` and the project labels.

## 💡 Design Notes

- **Acts without confirmation.** It stops for only two cases: unclear customer matches, and messages with no identifiable customer or ask.
- **Docs before the tracker.** A shipped capability gets no project. The rep gets the doc link. When the ask is more specific than the docs, the need goes on the nearest open project with the gap spelled out.
- **Bare-noun search.** Project names drift, and substring hits can be unrelated work.
- **Need priority is set only on blocker language.**
