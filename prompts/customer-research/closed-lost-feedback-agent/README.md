# Closed-Lost Feedback Agent

## 🎯 Purpose

**Weekly unattended agent that drafts product-led feedback emails to buyers from newly closed-lost deals.**

Pulls last week's closed-lost deals from HubSpot, qualifies them against your ICP rules, gathers the real loss reasons from call recordings, Slack, and CRM notes, and creates Gmail drafts (never sends) from the product lead asking for a 15-minute feedback call. Logs every draft so nobody is contacted twice within 90 days.

**Business Value**:
- A steady supply of loss interviews without manual deal review
- Emails verify what the buyer already told you instead of asking them to repeat it
- A human approves every email, and Sales is never CC'd

**Use Cases**:
- Product-led closed-lost outreach playbooks
- Feeding loss interviews into discovery and roadmap work

**Complexity**: 🔴 Advanced

## 📦 Format

A single base prompt, [`prompt.md`](./prompt.md), written for an agentic Claude run with MCP connectors and local file access. It has no OpenAI or Gemini variants because it depends on tool use.

## 🔧 Requirements

- **HubSpot** connector (deal, contact, and company search)
- **Gmail** connector (`create_draft`)
- **Slack** connector (`slack_search_public_and_private`, `slack_read_thread`, `slack_read_channel`)
- **Call recorder** connector (optional; the prompt uses Attention's `ask_attention` and `search_calls`)
- Local access to the four config files described in `prompt.md`

## 🚀 Setup

1. Fill in the placeholders in the Configuration table in `prompt.md`.
2. Create `{{CONFIG_DIR}}` with `agent-instructions.md`, `persona-brief.md`, `icp-criteria.md`, and a `sent-log.csv` that has only the header row.
3. Schedule it weekly. Run it once by hand and review the drafts and the "needs your call" list before trusting the schedule.

## 💡 Design Notes

- **Config files over a long prompt.** The scheduled prompt stays short and stable; tuning happens in the files the agent reads every run.
- **Slack beats CRM when it's more specific.** Closing notes in Slack are often the most candid record of why a deal was lost.
- **Fail closed.** No playbook file means stop. A borderline deal goes on a list for a human instead of getting a draft.
