---
name: specify-evals
description: Writes the eval spec for an AI feature, linked from the PRD's Module B. Drafts eval cases in real user wording, including negative and near-miss cases, sets grading rules and the launch gate, and saves an Evals doc on the project for engineering to finalize. Use when a PRD's Module B applies, or when asked to specify evals for an AI feature.
---

# Specify evals (stub)

> **Status: stub.** This skill states its purpose and output so the rest of the factory can link to it. The full step-by-step method is still to be written. See the TODO at the end.

> **Setup:** workspace values come from your factory config. See [`factory-config.example.md`](../../../templates/factory-config.example.md). Engineering owns `{{EVAL_HARNESS}}`. This skill drafts cases for it and never recreates it.

## Purpose

An AI feature is only as good as the cases it is judged against. This skill turns a PRD's AI requirements into an eval spec that engineering can load into its eval harness, and that `/review-prd` and `/accept-against-spec` can check.

## Output

One document on the project, titled `Evals | <Project name>`, linked from the PRD's Module B. It holds:

- **Eval cases in real user wording.** Inputs come from real customer requests, calls, tickets or production failures, not invented phrasing. Each case names its source.
- **Positive, negative and near-miss cases.** Every AI requirement gets at least one case it must handle, and at least one negative or near-miss case it must refuse, route elsewhere, or handle differently.
- **Grading rules.** For each case: what counts as a pass, how it is graded (exact match, rubric, or human review), and who owns the ground truth (a `{{DOMAIN_EXPERT_ROLE}}` for domain cases, the PM otherwise).
- **Launch gate.** Every new case passes on repeated runs, no regressions on existing eval sets, and a feature floor (a minimum share of cases passing) set by the PM.
- **Failure behavior.** What the user sees when the model is wrong or unsure.

## Where it fits

- `/write-prd` offers this skill when Module B applies.
- `/review-prd` errors until the Evals doc is linked and every AI requirement has a positive case and a negative or near-miss case.
- Engineering finalizes the cases in `{{EVAL_HARNESS}}` and posts results.
- `/accept-against-spec` reads the posted results to decide the AI launch gate.

## TODO

- [ ] Write the step-by-step method: gathering real user wording from the call recorder, support tool and production failures; drafting cases per requirement; choosing grading methods; setting the feature floor with the PM.
- [ ] Define the Evals doc template (case table columns, grading rule format).
- [ ] Define the handoff format engineering's eval harness expects.
- [ ] Add an approval gate before saving, matching the other factory skills.
- [ ] Add a fictional worked example.
