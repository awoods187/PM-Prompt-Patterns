---
name: accept-against-spec
description: Acceptance-tests a project on the staging environment against its PRD. Runs every acceptance criterion on every surface the PRD names, records pass, fail or untested with evidence, files bugs, and holds Product's approval unless everything passes. Use before promoting a release from staging to production.
---

# Accept against spec

> **Setup:** workspace values (staging URLs, the acceptance org, surfaces, protected orgs) come from your factory config. See [`factory-config.example.md`](../../../templates/factory-config.example.md). Tool calls below use Linear MCP names as an example of how the issue tracker role is filled.

Promotion from staging to production needs two approvals: QA and Product. This skill is Product's half. It runs every acceptance criterion in the PRD against the real build on staging, records what happened with evidence, and approves only when every criterion passes. A release that fails or skips its own acceptance criteria does not ship.

You test what the PRD says, on the surfaces it names, in a real environment. You do not grade code, read diffs, or trust a ticket's Done status.

## Scope

**In scope:** one project with a Spec ready PRD, deployed to `{{STAGING_ENV}}`. Every acceptance criterion, the Module A worked example, the product invariants the feature touches, and the AI launch gate when Module B applies.

**Out of scope:**
- Production. Never run against `{{PRODUCTION_HOSTS}}`. If any host or org resolves to production, stop before the first call.
- QA's regression suite and QA's sign-off. QA owns those.
- Fixing bugs. File them with `/file-bug` and stop.

## Environment

All testing happens on `{{STAGING_ENV}}` in `{{ACCEPTANCE_ORG}}`. Never write into `{{PROTECTED_ORGS}}`. Other test suites depend on their data.

`{{ACCEPTANCE_ENV_DOC}}` lists the staging app and API addresses, the acceptance org, how to turn on feature flags for it, and where the staging API key is stored. Read it first. Never put a key in a tracker doc, a comment or chat. Fetch it at run time from where that doc says it lives.

A cloud workspace often cannot reach staging. If so, run API and CLI checks from the user's computer and UI checks in their browser.

## Step 0: Preconditions

Check all of these before testing anything. Stop at the first failure and say what is needed.

1. The project carries `{{SPEC_READY_LABEL}}`, and `PRD | <Project name>` exists. Otherwise offer `/review-prd`.
2. The feature is on staging. Read `{{BUILD_STATUS_ENDPOINT}}` on staging for the deployed build or commit and record it. Ask the PM or engineering lead to confirm the project's work is in that build.
3. The feature flag is on for `{{ACCEPTANCE_ORG}}`, if the PRD names one.
4. Every surface the test needs is reachable. `{{SURFACES}}` lists them. For example:
   - **UI:** a browser signed in to staging as a user in the acceptance org.
   - **API:** the staging API key, sent to `{{STAGING_API_URL}}`.
   - **CLI:** `{{PRODUCT_CLI}}` installed on the user's computer, pointed at staging, with a staging login.
   - **Agent:** an agent connector pointed at staging, or the in-app agent through the browser.

   An unreachable surface is not a reason to stop. Its checks become **untested**, with the reason.

## Step 1: Build the test plan

Read the PRD and the project's issues. Build one row per acceptance criterion, per surface:

- **Surfaces:** each AC runs on every surface in the PRD's scope. `{{SHIP_CHECKLIST}}` sets the default surfaces unless section 5 of the PRD lists an exception. An excepted surface is **N/A** with the PRD's reason, not untested.
- **Module A:** add the worked example as its own test. Run the dated scenario in the acceptance org and compare every record it creates, and the tie-out, with the PRD exactly. A record that differs is a fail, even if the screen looks right.
- **Invariants:** add a test for each invariant the feature touches. At minimum, when the feature creates records: the preparer cannot approve their own record, and the same action is refused the same way for a user without permission on every surface.
- **Module B:** read the `Evals | <Project name>` doc. The AI launch gate passes only with results engineering has posted from its eval harness: every new case passing, no regressions, and the PM's feature floor met. You cannot run the harness yourself. If no results are posted, the gate is **untested**.

For each row, write the steps, the test data you will create, and the expected result from the AC. Show the plan to the PM before running. A plan error costs a full rerun.

## Step 2: Run it

Run each row on staging and record what actually happened:

| Result | Means |
| --- | --- |
| **Pass** | The observed result matches the AC exactly, with evidence |
| **Fail** | The observed result differs from the AC. Record expected and actual |
| **Untested** | The check could not run: a surface was unreachable, data could not be set up, or the AC cannot be checked as written. Record why |
| **N/A** | The PRD excepts this surface, with a reason |

Rules:
- **Evidence for every pass and fail:** a screenshot of the UI, the API request and response, the CLI command and output, the agent transcript, or the created record. No evidence means untested.
- **Fresh data.** Create the records each test needs in the acceptance org. Name them with the project key and date so runs do not collide.
- **Test the AC, not your idea of the feature.** If an AC is ambiguous on staging, mark it untested with "AC not checkable as written" and point to the PRD line. That is a spec gap, not a pass.
- **Do not retry a fail until it passes.** Run a failing check twice to rule out a flake. Two fails is a fail.
- Every write stays inside the acceptance org on staging.

## Step 3: Decide

- **PASS:** every row is pass or N/A, and the AI gate passes when Module B applies.
- **HOLD:** any fail, or any untested row. The PM can waive an untested row only with a written reason recorded in the Acceptance doc. A fail cannot be waived here. It needs a fix, or a PRD change through `/write-prd` update mode.

## Step 4: Record

Show the results to the PM before writing anything to the tracker.

1. **Acceptance doc.** Save or update `Acceptance | <Project name>` on the project:
   - Run header: date, tester, staging build, org, surfaces reached.
   - Verdict: PASS or HOLD, with counts.
   - Results table: AC ID, surface, result, expected, actual, evidence link, bug link.
   - Waivers, each with its reason and who gave it.

   Embed screenshots. Keep earlier runs below the newest one.
2. **Bugs.** File one bug per defect with `/file-bug`: environment staging, the acceptance org, the steps you ran, expected from the AC, actual from the run. Link each bug to the project and its rows. If several rows fail for one cause, file once and link them all.
3. **Definition of done.** If the project tracks per-surface verification or sign-offs in issues, tick the surfaces whose rows all passed or are N/A, and tick Product's acceptance sign-off only on PASS. Never tick a sign-off for another person. Comment on each with the verdict and a link to the Acceptance doc.

## Step 5: Report the gate

- **PASS:** "Acceptance passed on staging build <build>. Product approves promotion to production." Link the Acceptance doc. QA's approval is still required.
- **HOLD:** "Product does not approve promotion." List the failing and untested rows, the bugs filed, and what would clear each one.

On PASS, offer to start the docs update for the shipped feature.

## Rerun

After fixes reach staging, rerun on the new build. Rerun every failed and untested row, and every row on the surfaces the fixes touched. Before a final PASS on a new build, rerun the Module A worked example and the invariant tests in full. A fix in one place can break rows that passed before. Close a bug in the Acceptance doc only when its rows pass.
