# File Issue (Claude Code Skill)

## 🎯 Purpose

**File the Linear issues that are not bugs: one standalone improvement, or the set of product-level chunks that break an existing project into what it must deliver.**

Runs in two modes. Improvement mode mines screenshots and prose, searches once for duplicates, a home project, and the owning team, then drafts a single issue describing the problem and the desired outcome. Decompose mode reads an existing project and its issues, then drafts user-visible chunks with a "Done when" for each and turns open questions into question issues. Both modes describe **what** the product needs to do and leave **how**, sizing, and sequencing to engineering.

**Business Value**:
- Improvements stop getting filed as bugs (or as stray projects)
- Project breakdowns read as capabilities users will see, not engineering tasks
- Open product questions become trackable issues instead of guesses baked into the spec

**Use Cases**:
- "The bills list should show due date by default" plus a screenshot
- "Break the TravelPerk project into issues"
- Handing off a non-bug from [File Bug](../file-bug/)

**Not for**: defects ([File Bug](../file-bug/)) or new capabilities that need shaping or should collect customer demand ([File Project](../file-project/)).

**Complexity**: 🟡 Intermediate

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt. Everything is in [`SKILL.md`](./SKILL.md).

## 🔧 Requirements

- **Linear MCP server** (`list_issues`, `get_project`, `list_templates`, `list_issue_statuses`, `list_issue_labels`, `save_issue`, `save_customer_need`, `prepare_attachment_upload`, `create_attachment_from_upload`)
- **curl** for media upload
- Companion skills it calls by name: [`/file-bug`](../file-bug/) (bugs, team map, upload flow) and [`/file-project`](../file-project/) (new capabilities). Run prose through the [Remove AI Writing Patterns](../../stakeholder-communication/remove-ai-writing-patterns/) prompt (`/anti-ai`).
- Optional: `/enrich-ticket` for adding context after filing. The skill works without it.

## 🚀 Setup

1. Copy this folder to `~/.claude/skills/file-issue/` (or your project's `.claude/skills/`), alongside `file-bug` and `file-project`.
2. Set up the team map in `/file-bug` first; this skill reuses it.
3. Adjust the `Surface | What should change` title style and the default issue body if your team uses a different convention, or add an improvement template in Linear.

## 💡 Design Notes

- **What, never how.** Implementation approach, estimates, sequencing, and assignment belong to engineering. A suggested approach in the source becomes context, not a requirement.
- **One search, three jobs.** The same Linear search catches duplicates, finds a home project, and picks the owning team.
- **Chunks are user-visible.** If a chunk only makes sense to an engineer, it's a technical task and stays out of the breakdown.
- **Questions become issues.** Open product questions get `Question | ...` issues instead of plausible guesses.
- **Approval gate.** The draft is shown and the skill stops; `save_issue` runs only after explicit approval of that exact draft.
