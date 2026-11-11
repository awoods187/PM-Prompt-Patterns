# Product Factory Config (Example)

Every product factory skill reads its workspace-specific values from this file instead of hardcoding them. Copy it to `factory-config.md` next to your installed skills, replace each `{{PLACEHOLDER}}` value, and keep it current. When a skill says "see the factory config", this is the file it means.

Values below are examples for a fictional company (Acme Co). Replace all of them.

## Tools

Each tool is a role. The vendor is up to you. MCP tool names in the skills (for example `list_issues` or `save_project`) show how a role is filled with one common setup. Map them to whatever your connectors expose.

| Placeholder | Example | What it is |
|---|---|---|
| `{{ISSUE_TRACKER}}` | Linear | Issue tracker that holds projects, issues, customers and documents (for example Linear or Jira). |
| `{{CALL_RECORDER}}` | Gong | Call recorder with searchable transcripts of customer and prospect calls. |
| `{{SUPPORT_TOOL}}` | Zendesk | Support tool that holds customer tickets and conversations. |
| `{{CRM}}` | HubSpot | CRM that holds companies, deals, stages and loss reasons (for example HubSpot or Salesforce). |
| `{{TEAM_CHAT}}` | Slack | Team chat where sales and CX post requests and where the retro sends its summary. |
| `{{WIKI}}` | Notion | Wiki or doc store with older specs, read for context only. |
| `{{SPREADSHEET}}` | Google Sheets | Where read-only rankings are delivered. An .xlsx file works too. |
| `{{DOCS_SITE}}` | docs.example.com | Your public docs site. |
| `{{DOCS_INDEX}}` | docs.example.com/llms.txt | A machine-readable index of every published docs page, if your docs site has one. |
| `{{PRODUCT_CLI}}` | acme | Your product's command-line tool, if it has one. |

## Issue tracker setup

| Placeholder | Example | What it is |
|---|---|---|
| `{{BUG_TEMPLATE_REF}}` | PROJ-123 | The tracker item that holds the canonical bug template, if you keep one there. |
| `{{TRIAGE_STATUS}}` | Triage | Status for new, unreviewed issues. |
| `{{BACKLOG_STATUS}}` | Backlog | Status for accepted but unplanned work, and the fallback when a team has no triage status. |
| `{{BUG_LABEL}}` | Bug | Label every bug carries. |
| `{{NEEDS_INFO_LABEL}}` | needs-info | Label your review process adds when a ticket is missing required fields. Skills remove it after fixing the ticket and never add it. |
| `{{AGENT_READY_LABEL}}` | agent-ready | Label your ticket-readiness check adds when a ticket passes. Skills never add it themselves. |
| `{{FILED_WITH_SKILL_LABEL}}` | filed-with-skill | Label skill-filed issues carry, so the retro can compare them with hand-filed ones. |
| `{{DRAFTED_WITH_WRITE_PRD_LABEL}}` | drafted-with-write-prd | Project label added when write-prd saves a PRD. Measures adoption. |
| `{{SPEC_READY_LABEL}}` | Spec ready | Project label set only by a clean review-prd run. Decompose checks it. |
| `{{CUSTOMER_GAP_LABEL}}` | customer-gap | Project label for work a named customer or prospect wants. |
| `{{ORIGIN_LABELS}}` | sales-request, cx-request | Project labels that record where a request came from. |
| `{{DEAL_LABELS}}` | deal-request, deal-sprint | Optional labels that say whether a deal ask is logged for later or judged small enough to sprint. Default to the "later" one. |
| `{{PARTNERSHIP_LABEL}}` | partnership | Project label for work that needs a commercial agreement with another vendor. |
| `{{RELEASE_LABELS}}` | release-2027-q1 | Release cohort labels a PM assigns during planning. Skills never set them. |

## Teams and routing

| Placeholder | Example | What it is |
|---|---|---|
| `{{TEAM_MAP}}` | See the table below | Which team owns which product surface. A starting point only: skills check recent tracker data before trusting it. |
| `{{INTEGRATIONS_TEAM}}` | Integrations | Default owner for third-party integration projects. |
| `{{PRODUCT_TEAM}}` | Product | The product and design team. Home for work that spans surfaces or has no engineering owner yet. Owns PRDs and the retro doc. |
| `{{ENGINEERING_TEAMS}}` | Every team except Product and QA | Which teams count as engineering for the retro's metrics. |

Example `{{TEAM_MAP}}`:

| Team | Owns |
|---|---|
| Records | The core data model: accounts, contacts, items, settings. |
| Workflows | Approvals, automation rules, scheduled jobs. |
| Integrations | Third-party integrations, onboarding, imports and migrations. |
| Reporting | Reports, dashboards, exports. |
| AI | AI features and agents. |
| Platform | Auth, permissions, performance, infrastructure. |
| UI | Design system and shared components. Rarely owns a user-visible bug. |
| Product | Anything not yet shaped or with no clear owner. |

## Environments

| Placeholder | Example | What it is |
|---|---|---|
| `{{STAGING_ENV}}` | staging | The pre-production environment where acceptance runs. |
| `{{STAGING_APP_URL}}` | https://staging.example.com | Staging app address. |
| `{{STAGING_API_URL}}` | https://api.staging.example.com | Staging API address. |
| `{{PRODUCTION_HOSTS}}` | app.example.com, api.example.com | Production hosts. Acceptance stops before any call that resolves to one of these. |
| `{{BUILD_STATUS_ENDPOINT}}` | /status | A staging endpoint that reports the deployed build or commit. |
| `{{ACCEPTANCE_ORG}}` | Acme Acceptance | The staging org or tenant where acceptance tests write data. |
| `{{PROTECTED_ORGS}}` | QA automation orgs | Staging orgs that other test suites depend on. Never write to them. |
| `{{ACCEPTANCE_ENV_DOC}}` | "Acceptance environment" doc | Where staging URLs, the acceptance org, flag setup and the location of the staging API key are written down. Never put the key itself in a doc. |
| `{{SURFACES}}` | UI, API, CLI, agent | Every surface a feature can ship on. Acceptance tests each one the PRD includes. |

## Strategy

| Placeholder | Example | What it is |
|---|---|---|
| `{{NORTH_STAR_1}}` | Win rate in the core segment | First north-star metric a PRD can say it moves. |
| `{{NORTH_STAR_2}}` | Time to first value | Second north-star metric. Add more if you have them. |
| `{{PRIORITY_SEGMENT}}` | Mid-market | The customer segment whose deals weigh more in prioritize-demand. |
| `{{DEEPEN_AREAS}}` | Module X, Module Y | Shipped areas where finishing what exists beats starting something new. prioritize-demand gives these a multiplier. |
| `{{USER_ROLES}}` | admin, approver, operator | The roles PRDs use in "Who" and in acceptance criteria. |
| `{{DOMAIN_EXPERT_ROLE}}` | Domain expert | Who signs off a worked example for features that change records of truth. |
| `{{PRODUCT_INVARIANTS}}` | The table at the end of `templates/prd-template.md` | Rules every feature must hold. review-prd checks every requirement against them. |
| `{{SHIP_CHECKLIST}}` | "Feature ship checklist" doc | Your standard ship requirements (surfaces, flags, telemetry, QA, acceptance). PRDs list only exceptions to it. |

## CRM fields

prioritize-demand reads these. Use your CRM's real field names.

| Placeholder | Example | What it is |
|---|---|---|
| `{{CRM_SEGMENT_FIELD}}` | industry | Field that identifies `{{PRIORITY_SEGMENT}}` deals. |
| `{{CRM_LOST_REASON_FIELD}}` | lost_reason | Field that records why a deal was lost. |
| `{{CRM_PRODUCT_LOSS_REASONS}}` | Missing feature, Missing integration, Competitor | Loss reasons that count as product reasons. |
| `{{CRM_LOST_DETAIL_FIELD}}` | lost_detail | Free-text detail on a lost deal, including competitor features the buyer preferred. |
| `{{CRM_AMOUNT_FIELD}}` | amount | Deal amount in one currency. |
| `{{CRM_WEIGHTED_AMOUNT_FIELD}}` | weighted_amount | Probability-weighted amount for open deals. |

## Engineering-owned pieces

These belong to engineering. The skills call them by role and never recreate them.

| Placeholder | Example | What it is |
|---|---|---|
| `{{TICKET_READINESS_CHECK}}` | /verify-ticket | Your ticket-readiness check. It grades a ticket against its template and applies `{{AGENT_READY_LABEL}}` when it passes. |
| `{{EVAL_HARNESS}}` | Engineering's eval harness | Where engineering stores and runs eval cases and posts results. |
| `{{AGENT_HANDOFF}}` | /ticket-to-pr | The step that hands a ready ticket to a coding agent, if you have one. |

## Review cadence

| Placeholder | Example | What it is |
|---|---|---|
| `{{RETRO_CADENCE}}` | Weekly, Monday 9am | When factory-retro runs. |
| `{{RETRO_WINDOW}}` | 7 days, compared with the trailing 4 weeks | The window each retro measures. |
| `{{RETRO_OWNER}}` | Jane PM | Who reads the retro and applies its proposed skill edits. |
