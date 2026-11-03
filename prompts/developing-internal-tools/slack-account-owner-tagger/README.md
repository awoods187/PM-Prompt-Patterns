# Slack Account Owner Tagger

## 🎯 Purpose

**Unattended agent that tags the right account owners on bot-posted customer questions in Slack.**

Twice a day it reads new posts in a channel, looks up each org's HubSpot company owner and Pylon account owner, classifies the org as customer or prospect, and replies in the thread tagging the owners. It rate-limits per org (weekly for customers, per run for prospects), skips personal-email users and dev posts, and tags an admin when no owner can be matched.

**Business Value**:
- Customer questions reach the account owner within hours
- No over-pinging: customers are tagged at most once a week
- Every post ends with a clear outcome in the run summary

**Use Cases**:
- Routing in-product AI assistant questions to account owners
- Any bot-fed Slack channel where each post names a customer org

**Complexity**: 🔴 Advanced

## 📦 Format

A single base prompt, [`prompt.md`](./prompt.md), written for an agentic Claude run with MCP connectors. There are no OpenAI or Gemini variants because it depends on tool use against Slack, HubSpot, and Pylon.

## 🔧 Requirements

- **Slack** connector: `slack_read_channel`, `slack_read_thread`, `slack_search_users`, `slack_send_message`
- **HubSpot** connector: `search_crm_objects`, `search_owners`
- **Pylon** connector (optional): `search_accounts`, `get_account`, `get_user`
- A scheduler: a scheduled cloud agent, or cron running Claude Code headless

## 🚀 Setup

1. Fill in every `{{PLACEHOLDER}}` listed in the Configuration table in `prompt.md`.
2. Schedule it for two runs a day. If you change the run times, update the window cutoffs in Step 1.
3. Run it once by hand and read the summary before trusting the schedule.

## 💡 Design Notes

- **Customer/prospect split comes from Pylon's account type.** No Pylon match means prospect.
- **"Handled" is read from the threads themselves**, so the automation is stateless across runs.
- **Graceful degradation:** with no Pylon connector it falls back to HubSpot only and the stricter weekly rule.
