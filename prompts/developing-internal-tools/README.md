# Developing Internal Tools

Production-tested prompts for building internal tools, libraries, and development infrastructure.

## Available Prompts

### Code Quality & Standards

- **[CLAUDE.md Generator](./claude-md-generator.md)** - 🔴 Advanced
  - Generate comprehensive CLAUDE.md engineering standards files
  - Establishes development guidelines for Claude Code sessions
  - Customizable for project size, tech stack, and compliance requirements
  - **Production metrics**: 80% reduction in clarifications, 90%+ code quality
  - **Best for**: Project setup, team standardization, compliance enforcement

- **[Code Review & Refactoring](./code-review-refactoring.md)** - 🔴 Advanced
  - Comprehensive code review for open source preparation
  - Security audit, PEP 8 compliance, documentation improvements
  - **Production metrics**: 98% security issue detection, 90%+ documentation coverage
  - **Best for**: Pre-open-source audits, code quality improvements, legacy modernization

### Documentation Generation

- **[Enterprise README Generator](./enterprise-readme-generator.md)** - 🟡 Intermediate
  - Create and optimize professional READMEs for multiple stakeholders
  - Progressive information disclosure (exec summary → quick start → details)
  - **Production metrics**: 60-70% reduction in onboarding time, 40-50% fewer support requests
  - **Best for**: New projects, monorepo standardization, documentation audits

### System Architecture & Infrastructure

- **[Multi-Provider LLM Orchestration System](./llm-orchestration-system.md)** - 🔴 Advanced
  - Build unified Python library for OpenAI, Anthropic, and Gemini integration
  - Adapter pattern with dynamic model discovery and intelligent fallback
  - Comprehensive cost tracking and usage analytics
  - **Production metrics**: 90%+ test coverage, <1% failure rate, 100% cost visibility
  - **Best for**: LLM-powered applications, provider flexibility, cost optimization

## Coming Soon

Planned prompts:
- PRD generation from notes
- API documentation from code
- Technical spec writing assistant
- Architecture decision records
- Release notes generation

See [TODO.md](../../TODO.md) for planned content or [contribute](../../CONTRIBUTING.md) your own!
