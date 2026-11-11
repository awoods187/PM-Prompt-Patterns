---
name: write-prd
description: Drafts or updates a PRD as a project document in your issue tracker, from your PRD template, after gathering evidence from the tracker, call recorder, team chat and support tool and interrogating the PM on what is missing. Refuses to draft while the problem, evidence, outcome, scope or modules are unanswered. Use for any PRD or spec request on a project.
---

# Write a PRD

> **Setup:** the PRD template is [`templates/prd-template.md`](../../../templates/prd-template.md). Workspace values (north stars, roles, labels, tools) come from your factory config. See [`factory-config.example.md`](../../../templates/factory-config.example.md). Tool calls below use Linear MCP names as an example of how the issue tracker role is filled.

A PRD says what we are building, for whom, and how we will know it is done. Engineering builds from it. `/review-prd` grades it. `/file-issue` decompose cuts issues from its requirement IDs. `/accept-against-spec` checks each criterion against the built product. A vague PRD fails all four.

A PRD skill that drafts too early produces documents nobody uses. This one earns the draft. It gathers everything it can, interrogates the PM on what is missing, and refuses to draft while the core is empty. The PM owns the PRD. You are the interviewer and the drafter, not the author of its decisions.

## Scope

**In scope:** one PRD per project, stored as a project document titled `PRD | <Project name>`. New drafts and updates.

**Out of scope:**
- No project yet: run `/file-project` first.
- Breaking the PRD into issues: `/file-issue` decompose mode, after review passes.
- Grading the PRD: `/review-prd`.
- How it gets built (files, schema, endpoints, sequencing): engineering's tech spec. Record build opinions as context, never as requirements.
- Mockups: link them. Never describe screens in the PRD.

## Step 0: Load the template

Load the PRD template from your tracker (for example `get_template("PRD")`). It is the source of truth for section names, order, guidance and the product invariants table. If it differs from this skill, the template wins. If you cannot find it, stop and say so. Do not work from memory.

## Step 1: Gather before you ask

The PM should never have to tell you something your tools already know. Run these in parallel:

- **Issue tracker:** the project (description, team, labels, status, linked docs), its documents (if a `PRD |` doc exists, switch to **update mode**), its customer needs with the customers' words, and its issues.
- **Call recorder** (`{{CALL_RECORDER}}`): search calls for the customers named in the needs and for the capability. Pull verbatim quotes about the problem, not the solution.
- **Team chat** (`{{TEAM_CHAT}}`) and **support tool** (`{{SUPPORT_TOOL}}`): search for the capability and the customer names.
- **Wiki** (`{{WIKI}}`): earlier specs on the same area, for context only. Never edit them.

Keep a source list. Every quote in the PRD must trace to one of these, word for word. Never paraphrase a customer into a quote.

## Step 2: Interrogate

Ask only about what Step 1 did not answer. Ask in rounds of at most four questions. Use a multiple-choice question tool when the answer is a choice. Open each round with what you already found, so the PM corrects instead of retyping.

The five gates. Do not draft until each has a real answer:

| Gate | A real answer | Push back when |
| --- | --- | --- |
| Problem | What is wrong today, for whom, and what it costs them | It describes a solution ("we need a sync"), not a pain |
| Evidence | At least one customer-sourced row, or an explicit "no named customer" | Every source is internal: code, docs, other projects, an opinion |
| Outcome | Which north star it moves (`{{NORTH_STAR_1}}`, `{{NORTH_STAR_2}}`), a measurable metric, a kill criterion | The metric is activity ("ship X") or the target is "TBD" with no owner and date |
| Scope | Who it is for (roles from `{{USER_ROLES}}`), goals, non-goals, what ships first | Non-goals are empty, or "ships first" is the whole project |
| Modules | Does it change records of truth? Use AI? Integrate a third party? | The PM is unsure. Ask what happens to existing records when the feature runs |

Push back directly, one challenge per weak answer:
- "Which customer said that? I can't find it in the needs or calls."
- "That's the solution. What does the user do today, and what does it cost them?"
- "'Faster' isn't measurable. How long does it take today, and what's the target?"
- "What would a reader expect this to include that it doesn't?"

The gates are hard. If any gate is open, do not draft, even if the PM asks. Say which gates are open, what would satisfy each, and where the answer probably lives (a customer to call, a metric to pull, an expert to ask). A PRD without these answers produces work nobody can verify.

If Module A applies, ask who the `{{DOMAIN_EXPERT_ROLE}}` is. They write or sign off the worked example. Never invent records the PM and expert have not confirmed. Draft them as a proposal and mark the sign-off `pending @name`.

## Step 3: Propose the outline, then stop

Before drafting, show:
- The modules that apply, and why.
- The requirement areas with their ID prefixes (for example `IMP`, `APR`, `SYNC`) and one line per requirement.
- The open questions you will carry, marked blocking or not.

Wait for approval. A wrong outline costs a full redraft.

## Step 4: Draft

Fill the template in order. Delete its guidance notes and any module that does not apply.

**Requirements and acceptance criteria** are the core. Spend the words there.
- Each requirement gets a stable ID (`<AREA>-<n>`) that is never reused, even after deletion.
- Each acceptance criterion is one line. Someone can check it against the built product and answer pass or fail without asking the PM.
- Use numbers, states and roles. Never "fast", "easy", "intuitive", "seamless", "appropriate" or "as needed".
- Include what must be blocked: permissions, invalid input, locked periods, duplicates.
- Describe what the user sees or what gets recorded, never how the code does it.

**Invariants.** Check every requirement against the template's product invariants table. If a requirement conflicts with one, do not quietly rewrite it. Raise it with the PM. Either the requirement changes, or it becomes a listed exception with its reason and the control that replaces it.

**Ship checklist.** `{{SHIP_CHECKLIST}}` covers surfaces, flags, telemetry, QA and acceptance. List only exceptions (for example, the agent surface ships in a later phase, and why).

**Never invent.** No made-up numbers, customers, quotes, dates or owners. A missing fact is `<TBD: owner>` plus an open question.

**Length.** The core runs about one page. If it runs long, the cause is usually build detail or prose that belongs in an acceptance criterion. Cut those first.

Run `/anti-ai` (the [Remove AI Writing Patterns](../../stakeholder-communication/remove-ai-writing-patterns/) prompt) on the prose sections before showing the draft.

## Step 5: Show the draft and stop

Show the full PRD as it will appear. Then list the sources used, the open questions, and any invariant or checklist exceptions. Do not save in the same turn. Revise until the PM approves.

## Step 6: Save

Save the document on the project as `PRD | <Project name>` (for example `save_document(title=..., project=..., content=...)`). Set Status to Draft. Never set Spec ready. Only a clean `/review-prd` run does that.

Then add the project label `{{DRAFTED_WITH_WRITE_PRD_LABEL}}`. Read the project's current labels first and keep them all, because setting labels usually replaces the whole set. The label is how the factory retro measures adoption, so never skip it.

Report the document URL. If Module B applies, offer `/specify-evals` first, because review-prd errors until the Evals doc exists. Otherwise offer `/review-prd`. One line either way.

## Update mode

When a PRD already exists:
1. Read it in full.
2. Ask what changed and why, or read the source the PM points to.
3. Edit with a patch, never by resending the whole document.
4. If the status is Spec ready: add a row to Decisions (date, decision, who, requirement IDs changed), edit the affected requirements in place, set Status back to Draft, and remove `{{SPEC_READY_LABEL}}` from the project, keeping every other label. Never append changes as dated sections at the top or bottom.
5. Offer `/review-prd` to restore Spec ready.

Deleted requirements keep their ID, retired. Note them in Decisions so decompose and acceptance know they are gone.
