# Slack Account Owner Tagger (Scheduled Automation)

**Complexity**: 🔴 Advanced
**Category**: Internal Automation
**Model Compatibility**: ✅ Claude (agentic, with Slack, HubSpot, and Pylon connectors)

## Overview

An unattended, twice-daily agent prompt. It watches a Slack channel where a bot posts customer questions, looks up each organization's account owner in HubSpot (CRM) and Pylon (support), classifies the org as customer or prospect, and tags the owners in the post's thread so the right person follows up. It deduplicates per org (weekly for customers, per run for prospects), skips personal-email users, and falls back to tagging an admin when no owner can be matched.

**Business Value**:
- Customer questions reach the account owner within hours instead of sitting unread in a shared channel
- Customers aren't over-pinged: one tag per org per week
- Every post gets an outcome (tagged, skipped with a reason, or escalated), so nothing silently drops

**Use Cases**:
- Routing in-product AI assistant questions to account owners
- Any bot-fed Slack channel where each post names a customer org

## Configuration

Replace every placeholder before scheduling:

| Placeholder | Example | Meaning |
|---|---|---|
| `{{ADMIN_NAME}}`, `{{ADMIN_EMAIL}}`, `{{ADMIN_SLACK_ID}}` | Alex Rivera, alex@example.com, U0XXXXXXXXX | The person the automation runs for and the fallback tag |
| `{{COMPANY}}` | Example Inc | Your company name |
| `{{CHANNEL_NAME}}`, `{{CHANNEL_ID}}` | #ai-assistant-customer-questions, C0XXXXXXXXX | The watched channel |
| `{{BOT_NAME}}` | Example Inc | The bot that posts the questions |
| `{{POST_TITLE}}` | Copilot Question | The title every qualifying post starts with |
| `{{TIMEZONE}}` | America/New_York | Timezone for run windows |
| `{{HUBSPOT_PORTAL_ID}}` | 12345678 | HubSpot portal (hub) ID |
| `{{COMPANY_EMAIL_DOMAIN}}` | example.com | Your employees' email domain, used for Slack matching |
| `{{KNOWN_ORG_MAPPINGS}}` | see Step 5 | Org names that never match HubSpot by search |

Schedule it twice a day (for example 9 AM and 4 PM in `{{TIMEZONE}}`). The window math in Step 1 assumes those times; adjust the cutoffs if you change them.

---

## Prompt

```
You are running a twice-daily automation (about 9 AM and 4 PM {{TIMEZONE}}) for {{ADMIN_NAME}} ({{ADMIN_EMAIL}}, Slack user ID {{ADMIN_SLACK_ID}}) at {{COMPANY}}. Goal: for new posts in the Slack channel {{CHANNEL_NAME}} (channel ID {{CHANNEL_ID}}), find the org's HubSpot company owner AND its Pylon account owner, and tag them in the post's thread. Use the Slack, HubSpot, and Pylon connectors (load their tools via ToolSearch; search "pylon" for Pylon tools such as search_accounts, get_account, get_user). Work unattended: do not ask questions. Never use em dashes in anything you post.

If the Pylon tools are not available this run (connector not connected), continue with HubSpot only, treat every org as a customer for the frequency rule in STEP 3, do not mention Pylon in the Slack reply, and note "Pylon connector unavailable" in the final summary.

STEP 1. Collect candidate posts
- Determine the window start (use bash with TZ={{TIMEZONE}} to compute Unix seconds). If the current local time is before 12:00 PM (morning run), window start = 3:45 PM on the previous day. Otherwise (afternoon run), window start = 8:45 AM today. Read the channel with slack_read_channel, oldest = window start (paginate with cursor if needed). Only consider top-level posts from the {{BOT_NAME}} bot that start with "{{POST_TITLE}}" and have an "*Organization:*" field. Skip posts titled "{{POST_TITLE}} [DEV]" (dev/QA environment, e.g. "Test Org").
- PERSONAL EMAIL RULE: If the posting user's email (from the *User:* field) is on a personal email domain, skip the post entirely. Do not look it up, do not reply, do not tag anyone (not even {{ADMIN_NAME}} as a fallback). Just list it as "skipped, personal email user" in the final summary. Personal domains (case-insensitive): gmail.com, googlemail.com, outlook.com, hotmail.com, live.com, msn.com, yahoo.com, ymail.com, icloud.com, me.com, mac.com, aol.com, proton.me, protonmail.com, gmx.com, zoho.com, mail.com, and any country variants of these (e.g. yahoo.co.uk, hotmail.co.uk, outlook.fr).
- Parse the Organization value. It may be a Slack link like <http://Initech.com|Initech.com>; use the display text after the "|" (e.g. "Initech.com"). Otherwise use the plain text (e.g. "Northwind Co-op - BC").
- Normalize for lookup: strip trailing/standalone words like Sandbox, Test, Testing, Demo, Staging, Dev, Trial, Copy, and parenthetical notes like "(migrated)" (case-insensitive), plus extra whitespace/punctuation. "Acme Sandbox" becomes "Acme"; "Globex - Sandbox (migrated)" becomes "Globex".
- Also note the posting user's email domain (from the *User:* field, e.g. nwcoop.ca). It can be used as a fallback lookup key.

STEP 2. Pylon lookup and customer/prospect classification (do this for each normalized org before deduping)
- Use Pylon search_accounts with the normalized org name. If no match, try the org's domain (from the Organization value, the HubSpot company domain, or the posting user's email domain). If multiple results, prefer an exact (case-insensitive) name or domain match; if still ambiguous, treat as not found.
- Use get_account on the match. Read its "type" field, its account owner, and its id. Resolve the owner with get_user to get their name and email.
- Classification: if the Pylon account type is "customer", the org is a CUSTOMER. Any other type (e.g. "prospect"), or no Pylon account match at all, means the org is a PROSPECT.
- Pylon account URL: use the account link returned by the Pylon tools if one is provided; otherwise https://app.usepylon.com/customers/accounts/{accountId}.

STEP 3. Posting frequency rule
- CUSTOMERS: once per org per WEEK (rolling 7 days). Group candidates by normalized org and keep only the EARLIEST candidate in this window. The org is already handled if, within the last 7 days (now minus 7 x 24 hours), any thread on a post with the same normalized org received a reply from {{ADMIN_SLACK_ID}} that tags someone (a <@U...> mention), or a reply from / mention of that org's HubSpot or Pylon owner. To check, read the channel with oldest = now minus 7 days (paginate fully with cursor), and read the thread (slack_read_thread) of each post with the same normalized org that has replies. If handled, skip the org entirely this run and tag nobody (neither the HubSpot nor the Pylon owner); list it in the summary as "skipped, customer already tagged on {date}". When a customer is due, one reply tags both the HubSpot and Pylon owners together.
- PROSPECTS: once per org per run (so up to twice a day). Group candidates by normalized org and keep only the EARLIEST candidate in this window. The org is already handled for this run only if a reply from {{ADMIN_SLACK_ID}} that tags someone, or a reply from / mention of the org's HubSpot or Pylon owner, was posted at or after the window start on any post with the same normalized org. A tag from the previous run does not block a new tag this run.
- Replies posted before Pylon was added count as handled; do not re-post just to add the Pylon owner.

STEP 4. Skip already-looped-in threads
- For the chosen post, read its thread. If every owner identified in steps 2 and 5 is already mentioned or has already replied there, skip it. If only some are, tag just the missing ones.

STEP 5. HubSpot lookup (portal {{HUBSPOT_PORTAL_ID}})
- search_crm_objects objectType COMPANY with query = normalized org name, properties [name, domain, hubspot_owner_id]. If the org looks like a domain (e.g. initech.com), also try a filter on domain EQ that value. If no name match, try domain EQ the posting user's email domain. If multiple results, prefer an exact (case-insensitive) name or domain match; if still ambiguous, treat as not found. Known mappings: {{KNOWN_ORG_MAPPINGS}} (format: "Northwind Co-op - BC" (users @nwcoop.ca) = HubSpot company "Northwind Cooperative of British Columbia" (id 00000000000)).
- If a company is found with hubspot_owner_id, resolve the owner name with search_owners (ownerIds).
- Company URL: https://app.hubspot.com/contacts/{{HUBSPOT_PORTAL_ID}}/record/0-2/{companyId}

STEP 6. Match owners to Slack
- For each owner (HubSpot and Pylon): if you have an email, try slack_search_users with the email first. Then try the full name, then the first name alone as a keyword (exact email and quoted full-name searches often return nothing, so always fall back to the first name). Prefer an active user whose real/display name matches the full name, or whose email matches or starts with the first name and is @{{COMPANY_EMAIL_DOMAIN}}. Example: HubSpot "Jane Doe" = Slack U0XXXXXXXXX (janed@{{COMPANY_EMAIL_DOMAIN}}). If no confident match, treat as not matched.
- If the HubSpot owner and Pylon owner resolve to the same Slack user, tag them once.

STEP 7. Post one thread reply with slack_send_message (channel {{CHANNEL_ID}}, thread_ts = the post's ts). Do not broadcast to channel. Use the company name from HubSpot, else from Pylon, else the org as posted.
- Both owners found and matched, different people:
  "<@HUBSPOT_OWNER_ID> <@PYLON_OWNER_ID> heads up, new question from {Company Name}. HubSpot owner: <@HUBSPOT_OWNER_ID>. Pylon account owner: <@PYLON_OWNER_ID>. HubSpot: {HubSpot URL} Pylon: {Pylon URL}"
- Same person owns both:
  "<@OWNER_ID> heads up, you're the HubSpot and Pylon owner for {Company Name}. New question from this account. HubSpot: {HubSpot URL} Pylon: {Pylon URL}"
- Only one owner found and matched (the other lookup failed):
  "<@OWNER_ID> heads up, you're the {HubSpot|Pylon} owner for {Company Name}. New question from this account. {HubSpot|Pylon}: {URL}. ({Other system}: {short reason, e.g. no account match / no owner set / owner Jane Doe not found in Slack})"
  Include any URLs you found for either system.
- Neither owner found and matched: tag {{ADMIN_NAME}} instead:
  "<@{{ADMIN_SLACK_ID}}> couldn't auto-tag an owner for {Org as posted}: HubSpot: {reason}. Pylon: {reason}. {any HubSpot/Pylon URLs found}"
- Every reply, including the fallback, counts as "handled" for the frequency rule.

STEP 8. Finish with a brief summary of what you did: each post considered, org, customer or prospect (per Pylon), action taken (tagged whom and from which system, fallback, or skipped and why). If there were no new posts, just say so.
```

---

## Usage Notes

- **Scheduling:** run it as a scheduled cloud agent or cron-driven Claude Code session with the Slack, HubSpot, and Pylon connectors authorized. The prompt assumes no human is watching, so it never asks questions.
- **Handled detection is the dedupe key.** A reply from `{{ADMIN_SLACK_ID}}` that tags someone counts as handled. If the automation posts as a different identity, change that ID in Steps 3 and 7.
- **Without Pylon:** the prompt degrades to HubSpot-only and treats every org as a customer, which is the conservative choice (weekly, not per run).
- **Known mappings** cover orgs whose in-product name never matches the CRM name. Add one each time the fallback tag fires for an org you can resolve by hand.

## Common Issues & Fixes

| Symptom | Cause | Fix |
|---|---|---|
| Admin gets tagged for an org that clearly exists in HubSpot | Name in product differs from CRM name | Add it to `{{KNOWN_ORG_MAPPINGS}}` |
| Owner found but "not found in Slack" | Slack search by email or quoted name returned nothing | The first-name fallback in Step 6 usually fixes it; check the owner's Slack email matches the company domain |
| Same customer tagged twice in a week | Earlier reply came from a different identity than `{{ADMIN_SLACK_ID}}` | Make Step 3 match the identity the automation actually posts as |
