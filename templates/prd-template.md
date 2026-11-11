# PRD Template

A one-page product requirements document that engineering can build from, review-prd can grade, decompose can cut into issues, and acceptance can test line by line. Used by the [product factory](../README.md#-product-factory) skills: [write-prd](../prompts/product-strategy/write-prd/), [review-prd](../prompts/product-strategy/review-prd/) and [specify-evals](../prompts/product-strategy/specify-evals/).

Store it as a template in your issue tracker so the skills can load it. Placeholders like `{{NORTH_STAR_1}}` are defined in [`factory-config.example.md`](./factory-config.example.md).

---

> **How to use this template.** Create the PRD as a document on the project, titled `PRD | <Project name>`. The PM owns it. Fill the header and sections 1 to 5. Add a module only when it applies. Delete these guidance notes as you go.
>
> | Part | When | Length |
> | -- | -- | -- |
> | Header and sections 1 to 5 | Always | About 1 page |
> | Module A: Worked example | The feature changes records of truth (ledger, inventory, billing, ...) | Half a page, or an appendix |
> | Module B: AI evals | The feature uses AI | Half a page, plus a linked eval doc |
> | Module C: Integration mapping | The feature is a third-party integration | Tables only |
>
> Three things live outside the PRD and are linked from the header: **mockups**; **how it gets built** (files, schema, endpoints and sequencing belong in engineering's tech spec); and **ship requirements** (surfaces, flags, telemetry, QA), which `{{SHIP_CHECKLIST}}` covers. The PRD lists only exceptions to it.

**Status:** Draft | Spec ready | Superseded
**Owner:** @PM · **Domain expert sign-off:** @name, date | Not needed
**Modules:** Worked example | AI | Integration | None
**Mockups:** link | None · **Tech spec:** link | Not yet

> Only a review-prd run with no errors sets Status to Spec ready.

## 1. Problem and evidence

> Use customer evidence, not code links. If no named customer is asking, say so in bold.

<2 to 4 sentences: what is wrong today, for whom, and what it costs them.>

| Source | Customer | What they said or did | Link |
| -- | -- | -- | -- |
| Call |  | "<quote>" |  |

**Demand:** <N> customer needs on the project · <M> deals lost or stalled

## 2. Outcome

> Name one north star and one measurable metric. A deferred target needs an owner and a date.

**Moves:** {{NORTH_STAR_1}} | {{NORTH_STAR_2}} | Neither, because <reason>
**Metric:** <measurable> · baseline <x> · target <y> by <date>
**Kill criteria:** turn it off if <what must never happen>.

## 3. Scope

> Write non-goals down. Nobody can infer scope from what is missing.

**Who:** <roles from {{USER_ROLES}}>

**Goals**

* G1. <user-observable outcome>

**Non-goals**

* <what a reader might expect, and where it lives instead>

**Ships first:** <smallest end-to-end slice> · **Later:** <next, and what gates it>

## 4. Requirements and acceptance criteria

> This section gets most of the page. Each requirement has a stable ID that is never reused. Each acceptance criterion is:
> - **short:** one line.
> - **provable:** someone can check it against the built product and answer pass or fail without asking the PM.
> - **specific:** numbers, states and roles. Never "fast" or "easy".
> - **two-sided:** it covers what must be blocked, not only what must work.
>
> Example:
> **IMP-1** An admin can import contacts from a CSV file.
>
> * AC-IMP-1.1 A valid 100-row file creates 100 contacts.
> * AC-IMP-1.2 A file with a duplicate contact ID creates no contacts and names the failing row.
> * AC-IMP-1.3 A user without contact-create permission cannot start an import.

**<AREA-1>** <requirement>

* AC-<AREA-1>.1 <one line, pass or fail>

## 5. Exceptions, questions, decisions

> List only what departs from the defaults. Most PRDs have no exceptions. Once the PRD is Spec ready, record every change in Decisions and edit the affected requirement in place.

**Invariant exceptions:** <invariant, why, and the control that replaces it> | None
**Ship checklist exceptions:** <item, why, and when it will be met> | None

**Open questions**

| # | Question | Owner | Blocking? |
| -- | -- | -- | -- |
| Q1 |  |  |  |

**Decisions**

| Date | Decision | By | Requirements changed |
| -- | -- | -- | -- |
|  |  |  |  |

---

## Module A. Worked example for features that change records of truth (ledger, inventory, billing, ...)

> Use when the feature creates, changes or reverses records that other numbers depend on. Write one dated scenario with the exact records it produces and a tie-out, signed off by a domain expert. Each edge case gets an acceptance criterion in section 4.

**Scenario:** <starting state: tenant, currency or unit, settings, existing records>

| # | Date | Who | Action | Record created or changed |
| -- | -- | -- | -- | -- |
| 1 |  |  |  | <record, fields and values> |

**Tie-out:** <what must reconcile afterward, with the arithmetic>
**Edge cases:** partial, reversal, locked period, currency or unit conversion, multiple tenants or entities, rounding

## Module B. AI evals

> Use when the feature uses AI. Run /specify-evals to write the eval spec. It saves an `Evals | <Project name>` doc on the project and drafts the cases. Engineering finalizes them in engineering's eval harness. review-prd errors until the Evals doc is linked here.

**Task:** <what the model decides or produces> · **Human approver:** <role>
**Evals doc:** <link to Evals | Project name> · <N> cases, including <M> negative or near-miss cases
**Dataset source:** <real customer requests, calls, tickets or production failures> · **Ground truth:** <domain expert for domain cases, PM otherwise>
**Launch gate:** every new case passes on repeated runs · no regressions on existing eval sets · feature floor <x>% of cases passing
**When it fails:** <what the user sees>

## Module C. Integration mapping

> Use for third-party integrations. State which system owns each object, so no field is written by both.

**Source of truth:** <system> owns <objects>; <system> owns <objects>

| Our object | Direction | Provider object | Notes |
| -- | -- | -- | -- |
|  | → ← ↔ |  |  |

| Our field | Provider field | Rule |
| -- | -- | -- |
|  |  |  |

---

> **Product invariants.** Every feature holds these. review-prd checks each requirement against them. Delete this table from your PRD.
>
> The rows below are **examples**. Replace them with your own product's invariants and keep the IDs stable once you do.
>
> | # | Invariant | Status |
> | -- | -- | -- |
> | I-1 | Separation of duties: no one person both prepares and approves the same change. | Example. Replace. |
> | I-2 | Approval policy covers every record the feature creates, including records created by integrations and agents. | Example. Replace. |
> | I-3 | Audit trail is append-only. Records of truth are never edited in place. Changes are new, dated, linked records. | Example. Replace. |
> | I-4 | Agents act under their own identity, and a named human is accountable for each agent. | Example. Replace. |
> | I-5 | Permissions are identical across UI, API, CLI and agent surfaces. | Example. Replace. |
