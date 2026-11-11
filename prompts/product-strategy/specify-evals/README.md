# Specify Evals (Claude Code Skill, stub)

## 🎯 Purpose

**Write the eval spec for an AI feature: cases in real user wording, grading rules and a launch gate, linked from the PRD's AI module.**

> **Status: stub.** The purpose and output are defined so the rest of the factory can link to it. The step-by-step method is a TODO in [`SKILL.md`](./SKILL.md).

Part of the [product factory](../../../README.md#-product-factory).

**Business Value**:
- AI features are judged against real customer wording, not invented prompts
- Negative and near-miss cases catch the confident wrong answer before launch
- One launch gate that product, engineering and acceptance all read the same way

**Use Cases**:
- A PRD whose Module B (AI evals) applies
- "Specify evals for the auto-categorization feature"

**Complexity**: 🔴 Advanced

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt. Everything is in [`SKILL.md`](./SKILL.md).

## 🔧 Requirements

- **Issue tracker** connector with project documents
- Engineering's eval harness, which owns running the cases. This skill only drafts them.
- Companion skills: [`/write-prd`](../write-prd/), [`/review-prd`](../review-prd/), [`/accept-against-spec`](../../roadmap-planning/accept-against-spec/)

## 🚀 Setup

1. Copy this folder to `~/.claude/skills/specify-evals/` (or your project's `.claude/skills/`).
2. Fill in `{{EVAL_HARNESS}}` and `{{DOMAIN_EXPERT_ROLE}}` in [`factory-config.example.md`](../../../templates/factory-config.example.md).
3. Complete the TODO list in `SKILL.md` before relying on it.

## 💡 Design Notes

- **Real wording only.** Every case names its source.
- **Both sides.** Every AI requirement gets a case it must handle and a case it must not.
- **Engineering owns the harness.** This skill writes the spec, not the runner.
