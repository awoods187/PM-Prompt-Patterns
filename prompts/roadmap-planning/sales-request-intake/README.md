# Sales Request Intake (Claude Code Skill)

## 🎯 Purpose

**Turn a raw sales or CX Slack message into tracked demand in Linear.**

Reads a message like "on an intro with Acme they mentioned Coupa, Anaplan, ADP", checks your public docs for what already shipped, finds or creates the customer, finds or creates one project per request, attaches a customer need so demand accumulates on the right project, and drafts a Slack reply the rep can paste back.

**Business Value**:
- Requests that would scroll away in Slack become countable demand on projects
- Duplicate projects and duplicate needs are avoided, so the counts prioritization relies on stay trustworthy
- Reps get an immediate answer, including a docs link when the capability already exists

**Use Cases**:
- Logging integrations a prospect named on an intro call or demo
- Logging feature gaps raised in a QBR
- Answering "do we already support X?" for a rep while recording the ask

**Complexity**: 🔴 Advanced

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt:

| File | Contents |
|------|----------|
| [`SKILL.md`](./SKILL.md) | The skill: ten steps from reading the message to the Slack reply |
| [`references/worked-example.md`](./references/worked-example.md) | One message with six vendors walked end to end, including the traps |

## 🔧 Requirements

- **Linear MCP server** (`list_issues`, `list_customers`, `save_customer`, `save_customer_need`)
- **Web search and fetch** for the docs check
- Companion skills it calls by name: [`/file-project`](../file-project/) (project search, naming, routing), [`/file-ticket`](../file-ticket/) (bugs). Run prose through the [Remove AI Writing Patterns](../../stakeholder-communication/remove-ai-writing-patterns/) prompt. Install both skills alongside this one.

## 🚀 Setup

1. Copy this folder to `~/.claude/skills/sales-request/` (or your project's `.claude/skills/`).
2. In `SKILL.md`, replace `[Product]` and `docs.example.com` with your product and docs site.
3. Replace the fictional team names (`Integrations`, `Reporting`, `Product` triage) and labels (`Customer Gap`, `Sales Request`) with your workspace's.

## 💡 Design Notes

- **Acts without confirmation**, and stops for only two cases: ambiguous customer matches and messages with no identifiable customer or ask.
- **Docs before Linear.** A shipped capability gets no project; the rep gets the doc link instead. When the ask is more specific than the docs, the need goes on the nearest open project with the gap spelled out.
- **Bare-noun search.** Projects are often named inconsistently (`Coupa` vs `Coupa Integration`), and substring hits can be unrelated work.
- **Need priority is binary** (`0`/`1`) and is set to `1` only when the message uses blocker language.
