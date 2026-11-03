# File Project (Claude Code Skill)

## 🎯 Purpose

**Create one well-formed Linear project for a feature or integration request, or find the one that already exists.**

Searches projects, issues, and your docs for prior art, decides whether a near-match is the same work, then names, routes, labels, and describes the project so demand consolidates on it instead of fragmenting across duplicates.

**Business Value**:
- Demand from many customers lands on one project instead of scattered duplicates
- New projects arrive with a description, source link, and open questions instead of a bare title
- No guessed priority, lead, or dates, so nothing reads as a commitment nobody made

**Use Cases**:
- "Is there a project for this?" / "Make a project for the TravelPerk ask"
- Called by [Sales Request Intake](../sales-request-intake/) once per request in a sales message
- Routing a request when you are unsure which Eng team owns the surface

**Complexity**: 🟡 Intermediate

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt:

| File | Contents |
|------|----------|
| [`SKILL.md`](./SKILL.md) | The skill: prior-art search, naming, routing, fields, description, creation |
| [`references/routing.md`](./references/routing.md) | Example surface-to-team map and how to verify it against live Linear data |

## 🔧 Requirements

- **Linear MCP server** (`list_projects`, `list_issues`, `list_project_labels`, `save_project`)
- **Web fetch** for the docs check (optional; skipped if your docs have no page index)
- `/anti-ai` for the description pass. This is the [Remove AI Writing Patterns](../../stakeholder-communication/remove-ai-writing-patterns/) prompt installed as a skill.

## 🚀 Setup

1. Copy this folder to `~/.claude/skills/file-project/` (or your project's `.claude/skills/`).
2. Replace `[Product]` and `docs.example.com` in `SKILL.md`.
3. Replace the example team map in `references/routing.md` and the label names in Step 4 with your workspace's.

## 💡 Design Notes

- **Search the bare noun.** `Coupa` finds the project that `Coupa Integration` misses.
- **Closed projects don't absorb new demand.** A `Completed` match means create a new project and link the old one.
- **Route by product surface, not technical layer**, and trust recent projects over the static map.
