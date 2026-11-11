# Enrich Ticket (Claude Code Skill)

## 🎯 Purpose

**Fill in an incomplete ticket, from context first and the user second, until it meets its template.**

Classifies the ticket (bug, feature, chore or spike) and applies the matching template. For features in a project with a Spec ready PRD, it copies acceptance criteria by ID from the PRD instead of asking anyone to invent them. Bugs, chores and spikes finish when your ticket-readiness check passes. Features finish when they pass the skill's own checks.

Part of the [product factory](../../../README.md#-product-factory).

**Business Value**:
- Tickets reach engineering complete, without a round of follow-up questions
- Feature acceptance criteria stay identical to the PRD, so acceptance tests what was specified
- Bounced tickets get fixed in one guided pass instead of a back-and-forth

**Use Cases**:
- `/enrich-ticket PROJ-123` after your readiness check fails a ticket
- Adding PRD acceptance criteria to a decomposed chunk
- Cleaning up a hand-filed ticket before it goes to a coding agent

**Complexity**: 🟡 Intermediate

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt. Everything is in [`SKILL.md`](./SKILL.md).

## 🔧 Requirements

- **Issue tracker** connector with issues, comments, documents and labels. The skill uses Linear MCP tool names as an example.
- Your ticket-readiness check (`{{TICKET_READINESS_CHECK}}`). Engineering usually owns it.
- Companion skills: [`/file-bug`](../file-bug/) (shared bug template), [`/write-prd`](../../product-strategy/write-prd/), [`/review-prd`](../../product-strategy/review-prd/)

## 🚀 Setup

1. Copy this folder to `~/.claude/skills/enrich-ticket/` (or your project's `.claude/skills/`).
2. Fill in [`factory-config.example.md`](../../../templates/factory-config.example.md): `{{TICKET_READINESS_CHECK}}`, `{{NEEDS_INFO_LABEL}}`, `{{AGENT_READY_LABEL}}`, `{{SPEC_READY_LABEL}}` and `{{AGENT_HANDOFF}}`.
3. If your templates differ, replace the ones in Phase 3.

## 💡 Design Notes

- **Two finish lines.** Features use their own checks so the loop ends even when the readiness check skips them.
- **The PRD wins.** Acceptance criteria are copied by ID, never re-invented.
- **Out-of-spec asks stop the skill.** A ticket that asks for more than the PRD requires goes back to the PRD or out of scope.
- **Approval gate.** Nothing is saved without an explicit yes.
