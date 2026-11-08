# Roadmap Planning

## Available Prompts

- **[Sales Request Intake](./sales-request-intake/)** - 🔴 Advanced (Claude Code skill)
  - Turns a sales or CX Slack message into customer needs on Linear projects
  - Checks the docs for shipped capabilities first, avoids duplicate projects and needs
  - Ends with a paste-ready Slack reply for the rep
  - **Best for**: Capturing integration and feature asks from intro calls, demos, and QBRs

- **[File Project](./file-project/)** - 🟡 Intermediate (Claude Code skill)
  - Finds the existing Linear project for a request, or creates one well-formed project
  - Bare-noun prior-art search, surface-based team routing, labels, and a scoped description
  - **Best for**: Consolidating demand instead of creating duplicate projects

- **[File Bug](./file-bug/)** - 🟡 Intermediate (Claude Code skill)
  - Turns screenshots, recordings, or error text into a complete Linear bug ticket
  - Fills a fixed bug template, checks for duplicates, routes by surface, uploads media after approval
  - Hands improvements and new capabilities off to File Issue and File Project
  - **Best for**: Fast, reproducible bug reports from messy input

- **[File Issue](./file-issue/)** - 🟡 Intermediate (Claude Code skill)
  - Files non-bug issues: one standalone improvement, or the chunks that break a project into what it delivers
  - Describes what the product must do and leaves how, sizing, and sequencing to engineering
  - **Best for**: Improvements to existing behavior and project breakdowns

## Coming Soon

Planned prompts:
- Feature prioritization (RICE, ICE frameworks)
- Epic breakdown and estimation
- Dependency mapping
- Quarterly planning
- Roadmap narrative generation

See [TODO.md](../../TODO.md) for planned content.

Check back soon or [contribute](../../CONTRIBUTING.md)!
