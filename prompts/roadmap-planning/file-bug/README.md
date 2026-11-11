# File Bug (Claude Code Skill)

## 🎯 Purpose

**Turn a screenshot, screen recording, error string, or vague complaint into one complete, correctly routed bug ticket.**

Pulls the link, environment, org and error text out of screenshots and video frames before asking for anything. Fills a fixed bug template, checks for duplicates and the owning team in one search, shows the draft for approval, then files the issue and uploads the media.

Part of the [product factory](../../../README.md#-product-factory).

**Business Value**:
- Tickets arrive reproducible, so they don't bounce back for a missing environment or steps
- Duplicates get caught before they reach the triage queue
- Titles and screenshots are shaped to pass your ticket-readiness check as filed

**Use Cases**:
- "This page is busted" plus a screenshot
- A screen recording of a defect with no explanation
- A suspected defect handed off from [Sales Request Intake](../sales-request-intake/) or [Accept Against Spec](../accept-against-spec/)

**Not for**: improvements to things that work as designed ([File Issue](../file-issue/)) or new capabilities ([File Project](../file-project/)).

**Complexity**: 🟡 Intermediate

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt. Everything is in [`SKILL.md`](./SKILL.md).

## 🔧 Requirements

- **Issue tracker** connector. The skill uses Linear MCP tool names as an example (`list_issues`, `list_issue_statuses`, `list_issue_labels`, `save_issue`, `prepare_attachment_upload`, `create_attachment_from_upload`).
- **ffmpeg** and **curl** for video frames and media upload
- Companion skills: [`/file-issue`](../file-issue/), [`/file-project`](../file-project/), and optionally [`/enrich-ticket`](../enrich-ticket/) and your ticket-readiness check.

## 🚀 Setup

1. Copy this folder to `~/.claude/skills/file-bug/` (or your project's `.claude/skills/`).
2. Fill in [`factory-config.example.md`](../../../templates/factory-config.example.md): statuses, labels, `{{TEAM_MAP}}` and `{{BUG_TEMPLATE_REF}}`.
3. If your bug template differs, replace the one in Step 3.

## 💡 Design Notes

- **Mine before you ask.** Never ask for a URL that's readable in the screenshot.
- **Never invent a value.** An honest `Unknown` beats a plausible guess.
- **Approval gate.** The draft is shown and the skill stops. `save_issue` runs only after explicit approval for that ticket.
- **Upload one file at a time.** Signed upload URLs expire fast.
