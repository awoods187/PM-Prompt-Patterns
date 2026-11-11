---
name: review-prd
description: Grades a PRD in your issue tracker against your PRD template and product invariants, reporting errors, warnings and suggestions, and sets Status to Spec ready only when there are zero errors. Use whenever a PRD needs review or a Spec ready check.
---

# Review a PRD

> **Setup:** the PRD template is [`templates/prd-template.md`](../../../templates/prd-template.md). Workspace values (labels, the domain expert role) come from your factory config. See [`factory-config.example.md`](../../../templates/factory-config.example.md). Tool calls below use Linear MCP names as an example of how the issue tracker role is filled.

This skill is the gate between a PRD and the work built from it. Only a run with zero errors sets Status to Spec ready, and decompose will not run until it does. So the review must catch what a PM misses, not just count headers. The gaps that matter most are omissions: a requirement silent on who approves, an acceptance criterion nobody can test. Reviewers miss omissions because nothing on the page is wrong.

You review. You do not rewrite. Offer fixes and apply them only when the PM asks.

## Input

A project or a PRD document (URL, ID or project name). Resolve it to the `PRD | <Project name>` document. If none exists, stop and offer `/write-prd`.

## Step 0: Load

In parallel:
- The PRD document.
- The PRD template. It is the source of truth for sections, guidance and the product invariants table.
- The project and its customer needs, to check the evidence against real demand.

## Step 1: Structural checks

Run these mechanically first. They are cheap and they sharpen the judgment pass.

| Check | Severity if it fails |
| --- | --- |
| Header has Status, Owner, Modules, Mockups, Tech spec | Error |
| Sections 1 to 5 present and not still template placeholders | Error |
| Evidence has a customer-sourced row, or a bold statement that no named customer is asking | Error |
| Outcome names a north star and a metric with a target, or an owner and date for the target | Error |
| Outcome has a kill criterion | Warning |
| Non-goals are not empty | Error |
| Every requirement has an ID matching `<AREA>-<n>`, and IDs are unique | Error |
| Every requirement has at least one acceptance criterion with a matching ID (`AC-<AREA>-<n>.<m>`) | Error |
| Every open question has an owner and a blocking flag | Warning |
| Header modules match the content: changes to records of truth imply Module A, model or AI language implies Module B, a third-party sync implies Module C | Error when a needed module is missing |
| Module A present: the worked example lists the exact records, a tie-out, and a `{{DOMAIN_EXPERT_ROLE}}` sign-off with name and date, not pending | Error |
| Module B present: dataset source, launch gate, failure behavior, and a link to an `Evals | <Project name>` document on the project | Error |
| Module B's Evals doc: every AI requirement has a positive case and a negative or near-miss case, and each case has a source and a named ground-truth owner | Error |
| Module C present: source of truth stated per object, so no field is written by both systems | Error |
| Template guidance notes left in | Suggestion |
| Core runs well past one page | Suggestion |

## Step 2: Judgment lenses

Run each lens against the PRD, the template and the source material only. If you can start subagents, run the lenses in parallel in subagents that have not seen any drafting conversation, so the PRD is not grading itself. Give each its lens and ask for findings in the output format.

**Acceptance criteria.** For every AC: could a tester mark it pass or fail against the built product without asking the PM? Flag vague words (fast, easy, intuitive, seamless, appropriate, as needed, correctly, properly), missing numbers or roles, criteria that describe code instead of behavior, and requirements with only happy-path criteria.
- Untestable AC: Error.
- No negative case on a requirement that involves permissions, money or records of truth: Warning.

**Invariants.** Check every requirement against each product invariant. A conflict that is not listed under invariant exceptions, with a reason and a replacement control, is an Error. A requirement that creates records but says nothing about approval (who prepares, who approves, including when an integration or agent creates them) is an Error. These are omissions, so look for what is not said.

**Worked example.** When Module A is present, recompute the tie-out arithmetic. Check that every record balances where it must, every listed edge case has an AC, and locked-period and reversal behavior is defined.
- Arithmetic or balance error: Error.
- Edge case with no AC: Warning.

**Buildability and agent readiness.** Read the PRD as an engineer, or a coding agent, that has only this document. List every question they would have to ask the PM before building. Each is a Warning. It is an Error when the answer changes what gets built and the PRD guesses an answer that an open question says is unresolved.

**Scope and evidence.** Does the first slice solve the problem in the quoted evidence? Do the project's customer needs support the PRD's claim of demand? Does any requirement contradict a non-goal?
- Scope that does not address the stated problem: Error.
- Demand overstated against the customer needs: Warning.

**What versus how.** Files, classes, SDK calls, endpoints, schema, polling intervals or sequencing belong in the tech spec. Warning, with the passage quoted.

There is no design lens. Mockups live outside the PRD and are reviewed separately.

## Severity rubric

| Severity | Meaning | Effect |
| --- | --- | --- |
| Error | The PRD is incomplete, or would cause a wrong build or an audit problem | Blocks Spec ready |
| Warning | Unclear, thin, or likely to cost a round of questions | Fix unless the PM has a reason |
| Suggestion | Would make it better. Nothing breaks without it | PM's call |

When unsure between two levels, pick the higher one only if the gap could put a wrong value in a record of truth, or let one person both prepare and approve.

## Output

Lead with the verdict in one line: `N errors, N warnings, N suggestions. Spec ready: yes | no.` Then one table per severity, errors first:

| # | Where | Finding | Why it matters | Suggested fix |
| --- | --- | --- | --- | --- |
| E1 | AC-IMP-1.2 | "Shows a helpful error" can't be tested | A tester can't mark pass or fail | "Creates no contacts and names the failing row" |

`Where` is a section name or a requirement or AC ID. Quote the PRD text you flag. Keep each finding to its table row.

Offer to post the findings as a comment on the PRD. Do not post without a yes.

## Gate

If there are zero errors, ask the PM to confirm, then:
- Patch the header: Status to `Spec ready`, and add `Reviewed: <date>, 0 errors / N warnings`.
- Add `{{SPEC_READY_LABEL}}` to the project. Read the current labels first and keep them all. Decompose checks the label, not the header, so set both.

If there are errors and the project already carries `{{SPEC_READY_LABEL}}` (a re-review after changes), remove the label, set the header Status to Draft, and say so.

Never set Spec ready with an error open, and never because the PM asks you to skip a finding. If the PM disagrees with an error, the fix is an explicit, reasoned exception in section 5, which you then re-review.

On a re-review, start from the previous findings. Report which are fixed, which remain, and anything new.

When Spec ready is set, offer `/file-issue` decompose mode in one line.
