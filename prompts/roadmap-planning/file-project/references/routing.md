# Routing a project to a team

## The rule

Route by **product surface, not technical layer**. A request to change how the Invoices page filters belongs to the team that owns Invoices, not to the UI team, even when every line of the work is frontend.

The map below is a starting point that drifts as surfaces move between teams. When the surface is not obvious, or when the map disagrees with your instinct, verify against live data:

```
list_projects(query="<surface noun>", fields=["name","teams","status","updatedAt"], limit=15)
```

Weight the last few months. Disregard old `Completed` projects: a surface noun like "bank feeds" will happily return work from whoever owned it two years ago, and routing confidently to a team that handed the area off is worse than asking.

## Teams

This is an example map for a fictional accounting product. Replace it with your own teams and what they own.

| Team | Owns |
|---|---|
| Integrations | **All third-party integrations.** Also onboarding flows, migration and import tooling, integration observability and testing. |
| Core Records | The record model: entities, vendors, customers, items, accounts, terms, classifications. Tax engines. |
| Close | Period close, reconciliation, journal entries, close checklists. |
| Automation | Automation rules, matching, recurring transactions, workflow triggers. |
| Reporting | Financial reports, report builder, variance analysis, exports. |
| AI | AI features, insights surfaces, agents, natural-language querying. |
| Platform | Infrastructure, auth, permissions, performance, multi-entity plumbing. |
| UI | Design system, shared components, cross-app UI primitives. Rarely the owner of a feature request. |
| Product | Requests that span surfaces or have no eng owner yet. The honest home for something still being shaped. |
| QA | Test infrastructure and coverage work, not product features. |

## Integrations

Default to the Integrations team for anything integration-shaped. Expect exceptions in the live data, such as an integration project sitting on the Product team; those usually reflect a project created before a team picked it up rather than a considered routing decision.

Deviate only when the integration is really a change to a core surface wearing an integration's clothes: a tax-engine addition is Core Records work, because the hard part is the tax engine, not the connector.

## When it spans teams

`addTeams` accepts several teams and some projects legitimately have more than one, like a long-running payments integration project shared by Close, Integrations, and QA.

Resist the urge to reach for this on a new request. Adding three teams to a fresh project distributes ownership to nobody and each of those teams now sees unplanned work in their view. Pick the team that owns the majority of the work; a second team can be added when planning reveals it is needed.

## Non-integration requests

Ask what the customer would be *doing differently* in the product, and route to whoever owns that screen or that model.

- "We need approval chains on bills" → the AP surface, Core Records
- "Our auditors need a change log per journal entry" → Close
- "We want this report grouped by class" → Reporting
- "Can it guess the GL code from the vendor" → Automation or AI, and the recent-project search will tell you which
- "SSO with Okta" → Platform, since auth is infrastructure even though Okta is a third party

That last one is worth internalizing: not everything involving another company's name is an integration.
