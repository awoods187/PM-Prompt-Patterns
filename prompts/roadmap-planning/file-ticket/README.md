# File Ticket (Claude Code Skill)

## 🎯 Purpose

**Turn a screenshot, screen recording, error string, or vague complaint into one complete, correctly routed Linear bug ticket.**

Mines screenshots and video frames for the link, environment, org, and error text before asking for anything, fills a fixed bug template, checks for duplicates and the owning team in one search, shows the draft for approval, then files the issue and uploads the media.

**Business Value**:
- Tickets arrive reproducible, so they don't bounce back for a missing environment or steps
- Duplicates get caught before they hit the triage queue
- Filing a bug takes one pasted screenshot instead of a form

**Use Cases**:
- "This page is busted" plus a screenshot
- A screen recording of a defect with no explanation
- Handing off a suspected defect from [Sales Request Intake](../sales-request-intake/)

**Complexity**: 🟡 Intermediate

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt. Everything is in [`SKILL.md`](./SKILL.md).

## 🔧 Requirements

- **Linear MCP server** (`list_issues`, `list_issue_statuses`, `list_issue_labels`, `save_issue`, `prepare_attachment_upload`, `create_attachment_from_upload`)
- **ffmpeg** and **curl** for video frames and media upload
- Optional companions: `/verify-ticket` (template checker) and `/enrich-ticket` (root cause and acceptance criteria). The skill works without them.

## 🚀 Setup

1. Copy this folder to `~/.claude/skills/file-ticket/` (or your project's `.claude/skills/`).
2. Replace the bug template in Step 3 with your team's, and set `[TEMPLATE-ISSUE]` if the canonical copy lives in Linear.
3. Replace the example team map in Step 4 and the `missing-production-definition` label name with your workspace's.

## 💡 Design Notes

- **Mine before you ask.** Never ask for a URL that's legible in the screenshot.
- **Never invent a value.** An honest `Unknown` beats a plausible fabrication.
- **Approval gate.** The draft is shown and the skill stops; `save_issue` runs only after explicit approval for that ticket.
- **Upload one file at a time.** Signed upload URLs expire after 60 seconds.
