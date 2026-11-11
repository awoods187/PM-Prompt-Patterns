# Specify Evals (Claude Code Skill)

## 🎯 Purpose

**Write the eval spec for an AI feature: cases in real user wording, a grader per case, and a launch gate, linked from the PRD's AI module.**

Reads the PRD's AI requirements and collects real user wording from customer needs, calls, chat and support tickets. Then asks the PM about the task, the approver, ground truth, failure behavior and the never-cases. Writes positive, negative and near-miss cases for each requirement, picks a deterministic grader wherever one fits, drafts machine-readable cases for engineering's eval harness, and sets the launch gate. Saves an `Evals | <Project name>` doc and patches the PRD's Module B.

Part of the [product factory](../../../README.md#-product-factory).

**Business Value**:
- AI features are judged against real customer wording, not invented prompts
- Negative and near-miss cases catch the confident wrong answer before launch
- Product, engineering and acceptance all read the same launch gate

**Use Cases**:
- A PRD whose Module B (AI evals) applies
- "Specify evals for the auto-categorization feature"
- Updating cases after a PRD requirement changes

**Complexity**: 🔴 Advanced

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt. Everything is in [`SKILL.md`](./SKILL.md).

## 🔧 Requirements

- **Issue tracker** connector with projects, documents and customer needs. The skill uses Linear MCP tool names as an example.
- Optional: call recorder, team chat and support tool connectors, as sources of real user wording
- Engineering's eval harness, which runs the cases. This skill only drafts them.
- Companion skills: [`/write-prd`](../write-prd/), [`/review-prd`](../review-prd/), [`/accept-against-spec`](../../roadmap-planning/accept-against-spec/)

## 🚀 Setup

1. Copy this folder to `~/.claude/skills/specify-evals/` (or your project's `.claude/skills/`).
2. Fill in [`factory-config.example.md`](../../../templates/factory-config.example.md): `{{EVAL_HARNESS}}`, `{{EVAL_REGRESSION_SOURCE}}` and `{{DOMAIN_EXPERT_ROLE}}`.
3. Map the grader names in Step 3 to your harness's answer types.

## 💡 Design Notes

- **Real wording only.** Synthetic cases are labeled and count as gaps.
- **Both sides.** Every AI requirement gets a case it must handle and a case it must not.
- **Deterministic first.** A model judge is the last resort and needs a stated reason.
- **Engineering owns the harness.** Cases start as drafts. Only engineering promotes them.
- **The PM sets the floor.** The skill asks for the pass-rate floor and never suggests one.
