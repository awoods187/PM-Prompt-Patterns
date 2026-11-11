---
name: factory-retro
description: Scheduled retro on the product factory skills. Measures bounced tickets, engineering questions after handoff, spec churn, spec-gap defects and skill adoption, traces repeat failures to the skill step that caused them, and writes exact proposed skill edits into a tracker doc plus a short chat summary. Use for the weekly factory retro, or when asked whether the product skills are working.
---

# Factory retro

> **Setup:** workspace values (labels, teams, cadence, owner) come from your factory config. See [`factory-config.example.md`](../../../templates/factory-config.example.md). Tool calls below use Linear MCP names as an example of how the issue tracker role is filled.

The product skills (file-bug, file-issue, file-project, sales-request, prioritize-demand, write-prd, specify-evals, review-prd, enrich-ticket, accept-against-spec) are the factory. This retro checks whether the factory's output is any good, and fixes the factory, not the tickets. Make each mistake once. When the same failure shows up twice, a skill changes so it cannot happen a third time.

Measure outcomes, not activity. Tickets filed and PRDs written are not success. Tickets that pass the readiness gate, specs engineers build without questions, and releases that pass acceptance are.

It runs unattended on `{{RETRO_CADENCE}}`. Nobody may be there to answer questions, so make reasonable calls and say which ones you made.

## Window

`{{RETRO_WINDOW}}`. By default: the last 7 days, with a trailing 4-week comparison for every metric. A rule changes only when a pattern appears at least twice in the 4-week window.

## Step 1: Collect the signals

Scope: all issues and projects in `{{ENGINEERING_TEAMS}}`, plus `{{PRODUCT_TEAM}}`. Split every metric by origin:
- **Skill-filed:** carries `{{FILED_WITH_SKILL_LABEL}}`, or the project carries `{{DRAFTED_WITH_WRITE_PRD_LABEL}}`.
- **Hand-filed:** everything else.

Collect:

1. **Bounced tickets.** Issues that gained `{{NEEDS_INFO_LABEL}}` in the window, and issues that gained `{{AGENT_READY_LABEL}}`. On each bounced issue, read the readiness check's comment and record which rules failed.
2. **Questions after handoff.** In projects carrying `{{SPEC_READY_LABEL}}`: comments in the window from anyone other than the project lead that ask what to build (scope, behavior, an edge case, a missing value). Skip questions about how to build it. Also count `Question | ...` issues created in those projects.
3. **Spec churn.** Decisions rows added to `PRD | <Project>` documents in the window, and projects that lost `{{SPEC_READY_LABEL}}`.
4. **Spec-gap defects.** From `Acceptance | <Project>` documents updated in the window: HOLD rows and their causes, especially "AC not checkable as written". From bugs filed in the window against Spec ready projects: decide whether the cause is the spec (missing AC, wrong AC, missing edge case, missing invariant) or the build. Count only spec causes.
5. **Adoption.** Projects that moved to in progress in the window: how many carry `{{DRAFTED_WITH_WRITE_PRD_LABEL}}`, and how many carry `{{SPEC_READY_LABEL}}`. Projects decomposed without a PRD.
6. **Last retro's edits.** Read the previous `Factory retro` document. For each proposed edit, check whether the skill text now contains it. List the ones still pending.

## Step 2: Compute the metrics

| Metric | Definition |
| --- | --- |
| Bounce rate | Bounced ÷ (bounced + marked ready), skill-filed vs hand-filed |
| Top failing readiness rules | Count by rule, skill-filed vs hand-filed |
| Questions per handed-off issue | Build questions ÷ issues in Spec ready projects |
| Spec churn | Decisions rows after Spec ready; Spec ready labels removed |
| Spec-gap defects | Acceptance HOLD rows and post-Spec-ready bugs with a spec cause |
| Adoption | Share of projects entering in progress that were drafted with write-prd, and share that were Spec ready |

Show each with this week, the 4-week average, and the direction.

## Step 3: Find causes

For each metric worse than its 4-week average, and any failure seen at least twice in 4 weeks:
1. Find the examples (issue or doc links).
2. Name the skill whose output caused it, and the step or rule in that skill. Read the skill's `SKILL.md` and quote the exact line.
3. Decide the cause type: the skill lacks a rule, the rule is unclear, the skill was not used, or the cause is outside the skills (data, process, a person). Only the first two get a skill edit.

Examples of the trace:
- A visual-reference rule keeps failing on skill-filed bugs → file-bug's upload step does not embed the image → edit file-bug.
- Engineers keep asking which roles may approve → write-prd's Scope gate does not push on approval → edit write-prd.
- Acceptance rows marked "AC not checkable as written" → review-prd's acceptance criteria lens let them through → edit review-prd.

## Step 4: Write the edits

For each cause that needs a skill edit, write it exactly:
- The skill name.
- `old_string`: the current text, quoted exactly from the skill file, unique in that file.
- `new_string`: the replacement.
- The evidence: the examples and counts that justify it.

One edit per cause. Prefer tightening an existing rule over adding a section. Never propose an edit from a single example. If the cause is outside the skills, write a recommendation for the owner instead (for example "Customers in the tracker lack domains; CX to backfill").

Do not apply edits. The report carries them. `{{RETRO_OWNER}}` applies them in an interactive session, where each can be reviewed.

## Step 5: Publish

1. Save a tracker document `Factory retro | Week of <date>` on `{{PRODUCT_TEAM}}`:
   - Headline: the one finding that matters most this week, in one sentence.
   - Metrics table (Step 2).
   - Findings, each with evidence links, the cause, and the proposed edit or recommendation.
   - Proposed skill edits, in full.
   - Pending edits from earlier retros.
   - Data gaps: anything you could not measure, and why.
2. Send `{{RETRO_OWNER}}` a direct message in `{{TEAM_CHAT}}`: the headline, the top three findings in one line each, and the doc link. Under 80 words. No tables.

If nothing is worse than average and nothing repeats, still publish: a short doc with the metrics and "No skill changes proposed", and a one-line message.

## Rules

- Outcomes, not activity. Never report "N tickets filed" as a result.
- Every number links to its examples.
- Never edit tickets, PRDs or skills from this skill. It reads, reports and proposes.
- Never name a person as the cause. The factory is the subject.
