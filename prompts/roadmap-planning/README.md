# Roadmap Planning

## Available Prompts

These skills are part of the [product factory](../../README.md#-product-factory). Workspace values come from [`factory-config.example.md`](../../templates/factory-config.example.md).

- **[Sales Request Intake](./sales-request-intake/)** - 🔴 Advanced (Claude Code skill)
  - Turns a sales or CX chat message into customer needs on projects in your issue tracker
  - Checks the docs for shipped capabilities first, avoids duplicate projects and needs
  - Ends with a paste-ready reply for the rep
  - **Best for**: Capturing integration and feature asks from intro calls, demos and customer reviews

- **[File Project](./file-project/)** - 🟡 Intermediate (Claude Code skill)
  - Finds the existing project for a request, or creates one well-formed project
  - Bare-noun prior-art search, surface-based team routing, labels and a scoped description
  - **Best for**: Consolidating demand instead of creating duplicate projects

- **[File Bug](./file-bug/)** - 🟡 Intermediate (Claude Code skill)
  - Turns screenshots, recordings or error text into a complete bug ticket
  - Fills a fixed bug template, checks for duplicates, routes by surface, uploads media after approval
  - **Best for**: Fast, reproducible bug reports from messy input

- **[File Issue](./file-issue/)** - 🟡 Intermediate (Claude Code skill)
  - Files one standalone improvement, or cuts a Spec ready project into chunks from its PRD
  - Describes what the product must do and leaves how, sizing and sequencing to engineering
  - **Best for**: Improvements to existing behavior and project breakdowns

- **[Prioritize Demand](./prioritize-demand/)** - 🔴 Advanced (Claude Code skill)
  - Ranks open demand projects by customer needs, lost deals and open pipeline
  - Transparent weighted formula, evidence per project, delivered as a read-only spreadsheet
  - **Best for**: Cycle and quarterly planning

- **[Enrich Ticket](./enrich-ticket/)** - 🟡 Intermediate (Claude Code skill)
  - Completes a ticket against its template, from context first and the user second
  - Copies feature acceptance criteria by ID from the PRD
  - **Best for**: Fixing tickets that failed your readiness check

- **[Accept Against Spec](./accept-against-spec/)** - 🔴 Advanced (Claude Code skill)
  - Tests every acceptance criterion on every surface in staging, with evidence
  - Files bugs and holds Product's approval until everything passes
  - **Best for**: Product's half of a staging-to-production release gate

- **[Factory Retro](./factory-retro/)** - 🔴 Advanced (scheduled Claude Code skill)
  - Measures bounced tickets, questions after handoff, spec churn, spec-gap defects and adoption
  - Traces repeat failures to a skill step and proposes exact edits
  - **Best for**: Keeping the product skills improving week over week

## Coming Soon

Planned prompts:
- Feature prioritization (RICE, ICE frameworks)
- Epic breakdown and estimation
- Dependency mapping
- Quarterly planning
- Roadmap narrative generation

See [TODO.md](../../TODO.md) for planned content.

Check back soon or [contribute](../../CONTRIBUTING.md)!
