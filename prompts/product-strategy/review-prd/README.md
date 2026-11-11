# Review PRD (Claude Code Skill)

## 🎯 Purpose

**Grade a PRD against your template and product invariants, and set Spec ready only when there are zero errors.**

Runs mechanical structure checks first, then six judgment lenses: acceptance criteria, invariants, the worked example, buildability, scope and evidence, and what-versus-how. The lenses can run as independent subagents so the PRD is not grading itself. Reports errors, warnings and suggestions in one table each, and is the only thing allowed to mark a PRD Spec ready.

Part of the [product factory](../../../README.md#-product-factory).

**Business Value**:
- Catches omissions (silent approval rules, untestable criteria) that human reviewers miss
- One explicit gate between spec and build, so decompose never runs on an unreviewed PRD
- Disagreements turn into written, reasoned exceptions instead of quiet skips

**Use Cases**:
- "Review the PRD for the Initech Expense integration"
- A Spec ready check before engineering starts
- Re-reviewing after a PRD update

**Complexity**: 🟡 Intermediate

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt. Everything is in [`SKILL.md`](./SKILL.md).

## 🔧 Requirements

- **Issue tracker** connector with projects, documents, templates, labels and customer needs. The skill uses Linear MCP tool names as an example.
- The [PRD template](../../../templates/prd-template.md) stored in your tracker, with your own product invariants
- Optional: subagents for independent lens reviews
- Companion skills: [`/write-prd`](../write-prd/), [`/specify-evals`](../specify-evals/), [`/file-issue`](../../roadmap-planning/file-issue/)

## 🚀 Setup

1. Copy this folder to `~/.claude/skills/review-prd/` (or your project's `.claude/skills/`).
2. Replace the example product invariants in the PRD template with your own.
3. Fill in [`factory-config.example.md`](../../../templates/factory-config.example.md): `{{SPEC_READY_LABEL}}` and `{{DOMAIN_EXPERT_ROLE}}`.

## 💡 Design Notes

- **Review, don't rewrite.** Fixes are offered, applied only on request.
- **Look for what's missing.** The invariants lens hunts omissions, not errors on the page.
- **No skipped findings.** Disagreement becomes a written exception, then a re-review.
- **Label and header both.** Decompose checks the project label, so the gate sets both.
