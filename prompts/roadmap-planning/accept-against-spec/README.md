# Accept Against Spec (Claude Code Skill)

## 🎯 Purpose

**Product's half of the release gate: test every acceptance criterion in the PRD on staging, with evidence, and approve only when all of them pass.**

Builds a test plan with one row per acceptance criterion per surface (UI, API, CLI, agent), plus the worked example, the product invariants the feature touches, and the AI launch gate. Runs it on staging in a dedicated acceptance org, records pass, fail, untested or N/A with evidence, files one bug per defect, and reports PASS or HOLD.

Part of the [product factory](../../../README.md#-product-factory).

**Business Value**:
- Releases ship against the spec that was agreed, not against a Done column
- Every surface is held to the same criteria, so API and agent users don't get a lesser feature
- Spec gaps ("AC not checkable as written") surface as data for the factory retro

**Use Cases**:
- Before promoting a release from staging to production
- Rerunning acceptance after fixes land on a new build

**Complexity**: 🔴 Advanced

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt. Everything is in [`SKILL.md`](./SKILL.md).

## 🔧 Requirements

- **Issue tracker** connector with projects, documents and file upload. The skill uses Linear MCP tool names as an example.
- Access to the staging environment on each surface: a browser for UI, an API key for API, your product CLI, and an agent connector
- Companion skills: [`/file-bug`](../file-bug/), [`/review-prd`](../../product-strategy/review-prd/), [`/write-prd`](../../product-strategy/write-prd/)

## 🚀 Setup

1. Copy this folder to `~/.claude/skills/accept-against-spec/` (or your project's `.claude/skills/`).
2. Fill in the Environments section of [`factory-config.example.md`](../../../templates/factory-config.example.md). Set `{{PRODUCTION_HOSTS}}` carefully. The skill stops before any call to them.
3. Write your `{{ACCEPTANCE_ENV_DOC}}`: staging addresses, the acceptance org, flag setup, and where the staging key is stored (never the key itself).

## 💡 Design Notes

- **Never production.** Any host that resolves to production stops the run.
- **Evidence or it didn't happen.** No evidence means untested.
- **Fails can't be waived.** Only untested rows can, with a written reason.
- **Full rerun of the risky rows.** The worked example and invariant tests rerun in full before any final PASS.
