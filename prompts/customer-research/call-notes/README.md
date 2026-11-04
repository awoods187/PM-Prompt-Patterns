# Product Feedback Call Notes (Claude Code Skill)

## 🎯 Purpose

**Turn a customer or prospect call transcript into internal product feedback notes, with every feature ask linked to its Linear project.**

Reads the whole transcript, leads with the hardest fact (why we lost, where things stand, why they're churning), captures likes, weaknesses, the wishlist, things they asked for that already exist, their stack, and next steps, then delivers the notes as a Google Doc.

**Business Value**:
- Call feedback becomes product input that people who weren't on the call can skim and trust
- Feature asks with no Linear project surface as findings instead of disappearing
- "Already supported" asks expose messaging gaps, not just product gaps

**Use Cases**:
- Lost-deal, churn, win-back, and advisory board calls
- Writing up a recorded call by name from a call recorder (Attention, Gong, etc.)

**Complexity**: 🟡 Intermediate

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt:

| File | Contents |
|------|----------|
| [`SKILL.md`](./SKILL.md) | The skill: inputs, workflow, what to extract, doc structure, voice, output |
| [`references/example-lost-deal.md`](./references/example-lost-deal.md) | Fictional closed-lost write-up |
| [`references/example-advisory-board.md`](./references/example-advisory-board.md) | Fictional advisory board write-up |

## 🔧 Requirements

- **Linear MCP server** (`list_projects`, `list_issues`) for linking asks
- **Google Drive connector** (`create_file`) for delivery; falls back to a local `.md` file
- **Call recorder MCP** (optional) for fetching transcripts by name
- [Remove AI Writing Patterns](../../stakeholder-communication/remove-ai-writing-patterns/) for the edit pass.
- Optional hand-offs: [`/file-project`](../../roadmap-planning/file-project/) and [`/sales-request`](../../roadmap-planning/sales-request-intake/)

## 🚀 Setup

1. Copy this folder to `~/.claude/skills/call-notes/` (or your project's `.claude/skills/`).
2. Swap the call-recorder tool names in `SKILL.md` for your recorder's.
3. Once you have two write-ups you like, replace the fictional exemplars in `references/` with them. The exemplars set the register more than the instructions do.

## 💡 Design Notes

- **Hardest fact first.** The opening section is the one a skimmer reads.
- **Never invent a URL.** A missing Linear project is reported as a finding.
- **Call weaknesses what they are.** "The second demo came across as clunky" is the register.
