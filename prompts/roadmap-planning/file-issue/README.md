# File Issue (Claude Code Skill)

## 🎯 Purpose

**File the issues that are not bugs: one standalone improvement, or the user-visible chunks that break a Spec ready project into what its PRD requires.**

Improvement mode mines screenshots and prose, searches once for duplicates, a home project and the owning team, then drafts one issue that describes the problem and the outcome. Decompose mode runs only after the PRD passes review. It cuts chunks from the PRD's requirement IDs, copies acceptance criteria by ID, checks that every requirement is covered exactly once, and turns open questions into question issues. Both modes describe **what** the product must do and leave **how**, sizing and sequencing to engineering.

Part of the [product factory](../../../README.md#-product-factory).

**Business Value**:
- Improvements stop getting filed as bugs or as stray projects
- Project breakdowns trace to PRD requirements, so nothing is dropped and nothing is invented
- Open product questions become trackable issues instead of guesses baked into the work

**Use Cases**:
- "The bills list should show due date by default" plus a screenshot
- "Break the Initech Expense integration project into issues" after review-prd passes
- Handing off a non-bug from [File Bug](../file-bug/)

**Not for**: defects ([File Bug](../file-bug/)) or new capabilities that need shaping ([File Project](../file-project/)).

**Complexity**: 🟡 Intermediate

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt. Everything is in [`SKILL.md`](./SKILL.md).

## 🔧 Requirements

- **Issue tracker** connector. The skill uses Linear MCP tool names as an example (`list_issues`, `get_project`, `get_document`, `list_templates`, `list_issue_statuses`, `list_issue_labels`, `save_issue`, `save_customer_need`).
- **curl** for media upload
- Companion skills: [`/file-bug`](../file-bug/), [`/file-project`](../file-project/), [`/write-prd`](../../product-strategy/write-prd/), [`/review-prd`](../../product-strategy/review-prd/), [`/enrich-ticket`](../enrich-ticket/). Prose goes through the [Remove AI Writing Patterns](../../stakeholder-communication/remove-ai-writing-patterns/) prompt (`/anti-ai`).

## 🚀 Setup

1. Copy this folder to `~/.claude/skills/file-issue/` (or your project's `.claude/skills/`).
2. Fill in [`factory-config.example.md`](../../../templates/factory-config.example.md): statuses, labels, `{{SPEC_READY_LABEL}}` and `{{TEAM_MAP}}`.
3. Store the [PRD template](../../../templates/prd-template.md) in your tracker so decompose can read PRDs that follow it.

## 💡 Design Notes

- **What, never how.** A suggested build approach in the source becomes context, not a requirement.
- **Spec ready gate.** Decompose refuses to run until review-prd has passed.
- **Coverage both ways.** Every requirement ID lands in exactly one chunk, and no chunk delivers anything the PRD does not require.
- **Questions become issues.** Open product questions get `Question | ...` issues instead of guesses.
- **Approval gate.** The draft is shown and the skill stops. `save_issue` runs only after approval of that exact draft.
