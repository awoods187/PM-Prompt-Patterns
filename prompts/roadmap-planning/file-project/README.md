# File Project (Claude Code Skill)

## 🎯 Purpose

**Create one well-formed project for a feature or integration request, or find the one that already exists.**

Searches projects, issues and your docs for prior art, decides whether a near match is the same work, then names, routes, labels and describes the project. Demand consolidates on it instead of spreading across duplicates.

Part of the [product factory](../../../README.md#-product-factory).

**Business Value**:
- Demand from many customers lands on one project instead of scattered duplicates
- New projects arrive with a description, source link and open questions instead of a bare title
- No guessed priority, lead or dates, so nothing reads as a commitment nobody made

**Use Cases**:
- "Is there a project for this?" / "Make a project for the Initech ask"
- Called by [Sales Request Intake](../sales-request-intake/) once per request in a sales message
- Routing a request when you are unsure which team owns the surface

**Complexity**: 🟡 Intermediate

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt. Everything is in [`SKILL.md`](./SKILL.md).

## 🔧 Requirements

- **Issue tracker** connector. The skill uses Linear MCP tool names as an example (`list_projects`, `list_issues`, `list_project_labels`, `save_project`).
- **Web fetch** for the docs check (optional, skipped if your docs have no page index)
- [Remove AI Writing Patterns](../../stakeholder-communication/remove-ai-writing-patterns/) for the description pass

## 🚀 Setup

1. Copy this folder to `~/.claude/skills/file-project/` (or your project's `.claude/skills/`).
2. Fill in [`factory-config.example.md`](../../../templates/factory-config.example.md): `{{TEAM_MAP}}`, `{{INTEGRATIONS_TEAM}}`, `{{PRODUCT_TEAM}}`, the project labels and `{{DOCS_INDEX}}`.

## 💡 Design Notes

- **Search the bare noun.** `Initech` finds the project that `Initech Integration` misses.
- **Closed projects don't absorb new demand.** A closed match means create a new project and link the old one.
- **Route by product surface, not technical layer**, and trust recent projects over the static team map.
- **One team per new project.** Planning can add a second.
