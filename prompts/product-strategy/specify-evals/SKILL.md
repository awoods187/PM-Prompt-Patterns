---
name: specify-evals
description: Writes the eval spec for an AI feature in a PRD. Drafts cases in real user wording, including negative and near-miss cases, picks a grader per case, drafts machine-readable cases for engineering's eval harness, and sets the launch gate. Saves an Evals doc linked from the PRD's Module B. Use when a PRD's Module B applies, or when asked to specify evals for an AI feature.
---

# Specify evals for an AI feature

> **Setup:** workspace values (tools, the domain expert role, the eval harness, where regressions are reported) come from your factory config. See [`factory-config.example.md`](../../../templates/factory-config.example.md). Tool calls below use Linear MCP names as an example of how the issue tracker role is filled. Engineering owns `{{EVAL_HARNESS}}`. This skill drafts cases for it and never recreates it.

An AI requirement is only provable if it has cases. This skill turns a PRD's AI requirements into an eval spec engineering can load into its eval harness without asking the PM what "good" means. Product owns outcome evals: what the user asked, what the right answer is, and what must never happen. Engineering owns technical evals and finalizes the cases.

`/review-prd` errors on Module B until the `Evals | <Project name>` doc exists, is linked, and every AI requirement has a positive case and a negative or near-miss case.

## Scope

**In scope:** one `Evals | <Project name>` document per project, with draft machine-readable cases inside it.

**Out of scope:**
- No PRD yet, or Module B is missing: run `/write-prd` first.
- Loading cases into the harness, writing code, or changing graders: engineering.
- Production monitoring (online evaluators on live traffic): a later phase. Note it as a follow-up, never as a launch requirement.

## Step 1: Gather

Run in parallel:
- **Issue tracker:** the project and its documents. Read the `PRD | <Project name>` doc in full. Note every requirement and acceptance criterion where the model decides or produces something. If an `Evals |` doc already exists, switch to **update mode**.
- **Real user wording:** the project's customer needs, `{{CALL_RECORDER}}`, `{{TEAM_CHAT}}` and `{{SUPPORT_TOOL}}`. Collect what users actually typed or said when asking for this. Real wording is the dataset. Keep each source link.
- **Recent regressions:** if the feature extends an existing AI capability, check `{{EVAL_REGRESSION_SOURCE}}` for recent regressions in that area. Those eval sets are the blast radius for the launch gate.

Never invent user wording. A case without a real source is marked `source: synthetic`. It counts as a gap, not as coverage.

## Step 2: Interrogate

Ask only what Step 1 did not answer. At most four questions per round. Open with what you found.

- **Task:** what exactly does the model decide or produce? One sentence per requirement.
- **Human approver:** which role approves the output before it changes a record of truth? If none, that is a product invariant question (approval coverage, agent identity). Raise it.
- **Ground truth:** who confirms each expected answer? A `{{DOMAIN_EXPERT_ROLE}}` for domain cases, the PM otherwise. Name a person per case group, never "TBD".
- **Failure behavior:** when the model is unsure or wrong, what does the user see? "It asks", "it refuses" and "it shows a draft for approval" are answers. "It works" is not.
- **Never:** what must the model never do here (save without approval, call a write tool, guess a value)? Each one becomes a negative case.

## Step 3: Write the cases

For each AI requirement, write at least:
- **Positive cases:** the request in real user wording, and the exact expected result.
- **Negative cases:** requests the feature must refuse, ask about, or hand to a human.
- **Near-miss cases:** requests that look similar but belong to a different feature or need a different answer. They catch the model doing the right thing for the wrong question.

Vary the wording across cases: terse, wordy, with typos, with the wrong term an expert would still use. No requirement gets only happy paths.

Pick a grader per case. Prefer deterministic graders. Map these to whatever answer types your harness supports:

| Grader | Use when |
| -- | -- |
| Numeric match | The answer is a number (amount, count, balance) |
| Table match | The answer is rows (a report, a list of records) |
| Tool-trajectory match | What matters is which tools ran, in what order. List forbidden tools for the never-cases |
| Handoff match | The right behavior is to stop and ask, or hand to a human |
| Model judge | Only when nothing deterministic fits. Say why in the case. Engineering decides whether to accept it |

## Step 4: Draft machine-readable cases

One JSON line per case, for engineering to finalize. If you can read existing cases in the harness, match their fields. Otherwise use these keys and engineering will map them:

```
{"id": "<PROJECT>-<REQ>-<n>", "requirement": "<REQ ID>", "question": "<real wording>", "grader": "<grader>", "expected": <value>, "forbidden_tools": [], "ground_truth_owner": "<name>", "source": "real | synthetic", "source_link": "<call, ticket or chat link>", "status": "draft"}
```

Every case starts as `status: draft`. Engineering promotes it once it runs in the harness. Never promote a case yourself.

## Step 5: Launch gate

Write the gate the PRD's Module B will link:
- Every new case passes on every one of several repeated runs (for example 5 of 5).
- No regressions on the blast-radius eval sets named in Step 1.
- Feature floor: the minimum share of cases that must pass. The PM sets it. Ask for the number. Do not suggest one without the PM's input.

## Step 6: Show, then save

Show the full Evals doc:
- Task and approver per requirement.
- The case table: ID, requirement, wording, grader, expected, ground truth owner, source.
- The JSON lines.
- The launch gate and failure behavior.
- Gaps: requirements without a real-sourced case, unnamed owners.

Run `/anti-ai` (the [Remove AI Writing Patterns](../../stakeholder-communication/remove-ai-writing-patterns/) prompt) on the prose first. Wait for approval.

Then:
1. Save the document on the project as `Evals | <Project name>`.
2. Patch the PRD's Module B: the Evals doc link, case counts (N cases, M negative or near-miss), dataset source, ground truth, launch gate, failure behavior. Edit nothing else in the PRD.
3. Report the Evals doc URL and offer `/review-prd` in one line.

## Update mode

Read the existing Evals doc. Add cases for new or changed requirements. Retire cases for deleted requirements and keep their IDs retired. Never reuse an ID. Update the Module B counts. If the PRD is Spec ready, add a Decisions row in the PRD for any change to the launch gate.
