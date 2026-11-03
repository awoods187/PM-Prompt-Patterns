---
name: file-ticket
description: Files a bug ticket in Linear from whatever raw material the user has on hand, including pasted screenshots, screen recordings, error text, Sentry links, or a half-remembered complaint. Fills the team's required bug template, infers the owning Eng team, shows the draft for approval, then creates the issue and uploads the media. Use this whenever the user reports something broken in the product or wants a ticket, issue, or bug filed or logged, even casually ("this page is busted", "can you write this up", "log this for the team", "make a ticket for this"), and use it especially when they paste a screenshot or video of a defect with little or no explanation. Also use it when a ticket needs to be filed and you are unsure which Eng team owns the area.
---

# File a bug ticket

> **Setup:** replace the bug template, label names, and team map below with your workspace's. If your template lives in a Linear issue, put its identifier where this skill says `[TEMPLATE-ISSUE]`.

Bug tickets live or die on one thing: whether the reader can reproduce the bug without asking the reporter a follow-up question. A ticket missing its environment or its steps gets tagged `missing-production-definition` and bounces back, which costs a day. The bug template exists to prevent exactly that, so filling it completely matters more than filling it elegantly.

Your job here is narrow on purpose: take messy input, produce one complete, correctly routed ticket, get approval, file it. You are not diagnosing the bug.

## Scope

**In scope:** extracting facts from screenshots, videos, and prose; filling the bug template; picking the team; uploading media; creating the issue.

**Out of scope:** root cause analysis, reading the codebase, prior art searches, acceptance criteria. That is what `/enrich-ticket` is for, if you have it. Offer it after filing (see step 7) rather than doing it here. Staying out of the code is what makes this skill fast enough to use mid-conversation.

## Step 1: Take inventory of what you were given

Look at everything before asking for anything. Uploaded files may land in an uploads directory such as `/mnt/user-data/uploads`. Screenshots that appear in your context can be read directly. Videos and anything not rendered inline need handling per step 6.

For a video, pull frames with ffmpeg and read those rather than asking the user to describe what they recorded. One frame per second is usually enough to find the moment of failure, and the frame showing the error is often the whole ticket:

```bash
ffmpeg -i recording.mov -vf fps=1 /tmp/frame_%03d.png
```

A single screenshot usually carries three or four template fields on its face. Mine it before you interrogate:

- **Browser address bar** gives you the Link and often the environment.
- **Page header, org switcher, or account menu** gives you the Organization and sometimes the Company.
- **Error toast, modal, or red text** gives you the Actual result, and the exact string belongs in the ticket verbatim.
- **The surface itself** (which page, which record type) drives routing in step 4.

Asking a user for a URL that is legible in the screenshot they just pasted is the fastest way to make this skill feel worse than filing the ticket by hand.

## Step 2: Ask only for what is genuinely missing

After mining, you will typically still be short on: the environment (if the hostname is ambiguous), the impacted user's email, and reliable steps to reproduce. Ask for those in one batch, not one at a time.

Two fields deserve special stubbornness:

- **Production or Development.** This is the field whose absence triggers `missing-production-definition`. If you can infer it from the hostname, state your inference so the user can correct it in passing ("filing this as Production based on the URL") rather than asking outright. If the hostname is ambiguous, ask.
- **Steps to reproduce.** Numbered, starting from a fresh state, not "do what I did". If the user cannot produce steps, a Sentry link or a stack trace is an accepted substitute, so ask for one of those instead of pushing for steps that do not exist.

Never invent a value to fill a slot. An honest `Unknown` in the ticket is recoverable; a plausible fabrication sends someone chasing a repro that was never real.

**One bug per ticket.** If the input describes several unrelated defects, say so and propose a split before drafting. Filing them together guarantees a partial fix.

## Step 3: Fill the template

Use this structure exactly, in this field order. It is the format `/verify-ticket` checks against, if you use it, so deviating creates work downstream. If your team keeps the canonical template in a Linear issue (`[TEMPLATE-ISSUE]`), it is reproduced here so this skill does not need a network call to know the shape. If a field ever looks wrong, read that issue and trust it over this copy.

```markdown
**Domain Context:**

* Link:
* Production or Development:
* Organization:
* Company: (if applicable)
* Email: (user impacted)

**Context:**

* Steps to reproduce:
  1. 
  2. 
* Expected result:
* Actual result:

**Screenshot(s):** (if applicable)

**Video:** (if applicable)
```

What each field is for:

- **Link** is the URL of the exact page or record where the bug happens, not the app's home page.
- **Production or Development** is the field whose absence triggers `missing-production-definition`. It is the single most common reason a ticket bounces.
- **Organization** is the org where it happened, plus **Company** when the org has several and the bug is specific to one.
- **Email** is the impacted user, which is how anyone reproduces against real data rather than a clean test account.
- **Steps to reproduce** are numbered and start from a fresh state. A Sentry link or a stack trace is an accepted substitute when the user cannot produce steps.
- **Expected result** and **Actual result** are separate on purpose. A ticket that only says what broke leaves the reader guessing at intent, and sometimes the disagreement is about the expectation rather than the behavior.

Keep the literal field labels and the bold formatting. An automated checker matches on them, and a ticket that reads well but renames the fields still fails the check.

Title conventions:

- `Surface | What is wrong` works well, for example `Invoices | Status filter "Exclude" toggle does not exclude matching records`.
- Put the literal error string in quotes when there is one. It makes the ticket searchable and dedupes against existing reports.
- Prefix `[FE]` or `[BE]` only when the layer is genuinely known.
- Skip a "Bug:" prefix. The `Bug` label already says that.
- Aim for something that reads completely in a Linear list view, roughly 120 characters or less.

## Step 4: Search Linear once, for two purposes

One search answers both "has this already been filed" and "who owns this". Run it before drafting is final:

```
list_issues(query="<the error string, or the surface plus symptom>",
            fields=["title","team","status","labels","url","createdAt"], limit=10)
```

### Duplicates first

Search the literal error string when you have one, since that is what makes an existing report findable. If something looks like the same defect, do not file on top of it. Bring it to the user with the identifier, status, and your read on whether it is the same bug or a different symptom of one cause, and let them decide between commenting on the existing ticket, filing as related, or filing fresh.

Near misses are common and worth flagging even when you file anyway: the same error on a different surface usually shares a root cause, and saying so in the description saves the engineer the rediscovery. Link it with `relatedTo`.

### Then routing

The core rule is that tickets route by **product surface, not by technical layer**: a broken button on the Invoices page belongs to the team that owns Invoices, not to the UI team, even though the defect is in the frontend.

Whichever team already owns *recent* issues about that surface is your answer, and recency is load bearing. Areas move between teams, and a surface noun like "vendor credits" will happily return a pile of closed tickets from whoever owned it two years ago. Weight the last few months and disregard old `Done` work. The list below is an example prior for a fictional product, not an authority; replace it with your own, and a fresh search beats it every time.

| Team | Owns |
|---|---|
| Core Records | The record model: entities, vendors, customers, items, accounts, terms, classifications. Tax engines. |
| Close | Period close, reconciliation, journal entries, approval workflows, close checklists. |
| Automation | Automation rules, matching, recurring transactions, workflow triggers. |
| Integrations | All third-party integrations, onboarding flows, migration and import tooling. |
| Reporting | Financial reports, report builder, variance analysis, exports. |
| AI | AI assistant, AI features, insights surfaces, anomaly detection. |
| Platform | Infrastructure, auth, permissions, performance, multi-entity plumbing. |
| UI | Design system and shared components. Rarely the owner of a user-visible bug. |
| Product | Where a bug lands when no eng surface clearly owns it. |

Then set the rest:

- **State:** `Triage`. Call `list_issue_statuses(team=...)` first, since not every team has that state, and fall back to `Backlog` if it is absent.
- **Labels:** always `Bug`. Add a layer label only if you know the layer. Label names are often team-scoped, so call `list_issue_labels(team=...)` and use what comes back rather than guessing between near-duplicates like `Backend` and `BE`. Do not apply review-process labels such as `missing-production-definition` yourself; those belong to the review process.
- **Priority:** leave unset unless the user signalled severity. Triage decides, and a guessed priority is noise.

## Step 5: Show the draft and stop

Present the complete ticket in chat as markdown: title, team, state, labels, and the full description body exactly as it will appear. List any attachments you are about to upload, and call out any field you had to leave as `Unknown`.

Then stop and wait for approval. Do not call `save_issue` in the same turn as the draft, and do not treat an earlier "yes go ahead" about filing tickets in general as approval for this specific one. The review gate exists because a wrong ticket in a triage queue wastes several people's attention, not just yours.

If they ask for changes, revise and show it again.

## Step 6: Create the issue, then attach the media

Order matters: Linear cannot accept an upload until the issue exists.

1. `save_issue(title, team, description, labels, state)` with no `id` parameter.
2. Upload each screenshot or video, one file at a time:
   - `prepare_attachment_upload(issue, filename, contentType, size)` where `size` is the exact byte count.
   - `PUT` the raw bytes to the returned `uploadRequest.url` with `curl -X PUT --data-binary @file`, sending every header in `uploadRequest.headers` verbatim, casing included. They are part of the signed request and altering or omitting one returns a 403. Do not base64-encode or otherwise transform the bytes.
   - `create_attachment_from_upload(issue, assetUrl)` to create the attachment row.

   Two things bite here. The signed URL expires after **60 seconds**, and preparing several uploads before starting the PUTs will expire the earlier ones, so finish each file completely before preparing the next. There is also a `create_attachment` tool that takes base64 directly; it is a deprecated fallback for tiny files and needs a SHA-256 of the decoded bytes, so prefer the three-step flow.
3. If media is now attached, update the description so the Screenshot(s) and Video lines point at it, using `patch` rather than rewriting the whole description.

Report back the identifier and URL. If an upload failed, say which one failed and that the ticket itself is fine, so the user can drag the file into Linear directly instead of wondering whether anything landed.

## Step 7: Offer the handoff

Close by offering `/enrich-ticket` on the new issue, which is where root cause, prior art, and acceptance criteria get added. One line is enough. Do not start enriching unprompted, and if that skill is not available, say what enrichment would add rather than treating its absence as a problem. The ticket is already complete without it.
