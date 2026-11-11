# Factory Retro (Claude Code Skill)

## 🎯 Purpose

**A scheduled retro that checks whether the product factory skills produce good output, and proposes exact edits to the skills that don't.**

Measures outcomes, not activity: bounce rate at the readiness gate, engineering questions after handoff, spec churn, spec-gap defects found in acceptance, and adoption. Splits every metric by skill-filed versus hand-filed. Traces each repeat failure to the skill step that caused it and writes a precise `old_string` / `new_string` edit with evidence. Publishes a tracker doc and a short chat summary. Never edits anything itself.

Part of the [product factory](../../../README.md#-product-factory).

**Business Value**:
- The same mistake gets made once, then a skill changes so it can't recur
- Skill quality is measured by downstream outcomes, not by how many tickets were filed
- Proposed changes arrive ready to review, with the evidence attached

**Use Cases**:
- A weekly scheduled run (for example Monday morning)
- "Are the product skills actually working?"

**Complexity**: 🔴 Advanced

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt. Everything is in [`SKILL.md`](./SKILL.md). Run it on a schedule with a cron-driven Claude Code session or a scheduled cloud agent.

## 🔧 Requirements

- **Issue tracker** connector with issues, projects, labels, comments and documents. The skill uses Linear MCP tool names as an example.
- **Team chat** connector for the summary message
- Read access to the installed factory skills' `SKILL.md` files, so it can quote exact lines
- The factory's adoption labels in use: `{{FILED_WITH_SKILL_LABEL}}` and `{{DRAFTED_WITH_WRITE_PRD_LABEL}}`

## 🚀 Setup

1. Copy this folder to `~/.claude/skills/factory-retro/` (or your project's `.claude/skills/`).
2. Fill in [`factory-config.example.md`](../../../templates/factory-config.example.md): `{{RETRO_CADENCE}}`, `{{RETRO_WINDOW}}`, `{{RETRO_OWNER}}`, `{{ENGINEERING_TEAMS}}` and the labels.
3. Schedule it.

## 💡 Design Notes

- **Two strikes.** No rule changes from a single example.
- **Fix the factory, not the people.** Causes are skill steps, never names.
- **Read, report, propose.** Edits are applied by a person in an interactive session.
- **Always publish.** A quiet week still gets a short doc, so gaps in the series mean something.
