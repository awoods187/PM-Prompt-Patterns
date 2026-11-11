# Write PRD (Claude Code Skill)

## 🎯 Purpose

**Draft or update a one-page PRD that engineering can build from and acceptance can test line by line.**

Gathers evidence from the issue tracker, call recorder, team chat and support tool first. Then interrogates the PM through five hard gates (problem, evidence, outcome, scope, modules) and refuses to draft while any gate is open. Proposes an outline, drafts from the [PRD template](../../../templates/prd-template.md) with stable requirement IDs and one-line pass/fail acceptance criteria, and saves it as a project document.

Part of the [product factory](../../../README.md#-product-factory).

**Business Value**:
- PRDs arrive with real customer evidence and a measurable outcome, not a feature wish
- Acceptance criteria are testable, so decompose and acceptance have something to work from
- Requirement IDs stay stable, so issues and test results trace back to the spec

**Use Cases**:
- "Write the PRD for the Initech Expense integration project"
- Updating a Spec ready PRD after a decision changes scope
- Turning a top-ranked project from [Prioritize Demand](../../roadmap-planning/prioritize-demand/) into a spec

**Complexity**: 🔴 Advanced

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt. Everything is in [`SKILL.md`](./SKILL.md).

## 🔧 Requirements

- **Issue tracker** connector with projects, documents, templates and customer needs. The skill uses Linear MCP tool names as an example.
- Optional: call recorder, team chat, support tool and wiki connectors for evidence. The skill works with fewer sources and says which were missing.
- The [PRD template](../../../templates/prd-template.md) stored in your tracker
- Companion skills: [`/file-project`](../../roadmap-planning/file-project/), [`/review-prd`](../review-prd/), [`/specify-evals`](../specify-evals/), [Remove AI Writing Patterns](../../stakeholder-communication/remove-ai-writing-patterns/)

## 🚀 Setup

1. Copy this folder to `~/.claude/skills/write-prd/` (or your project's `.claude/skills/`).
2. Add [`templates/prd-template.md`](../../../templates/prd-template.md) to your tracker as a document template named "PRD". Replace the example product invariants with your own.
3. Fill in [`factory-config.example.md`](../../../templates/factory-config.example.md): north stars, `{{USER_ROLES}}`, `{{DOMAIN_EXPERT_ROLE}}`, `{{SHIP_CHECKLIST}}` and the PRD labels.

## 💡 Design Notes

- **Gather before asking.** The PM never retypes what a call or ticket already says.
- **Hard gates.** No draft while the problem, evidence, outcome, scope or modules are unanswered, even if the PM asks.
- **What, not how.** Build detail belongs in engineering's tech spec.
- **Never sets Spec ready.** Only a clean review-prd run does.
- **Adoption label.** Every saved PRD tags its project so the factory retro can measure usage.
