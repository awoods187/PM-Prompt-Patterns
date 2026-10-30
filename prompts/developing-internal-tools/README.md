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

- **[Python PR Code Review](./python-pr-code-review/)** - 🟡 Intermediate
  - Pedantic staff-engineer review of a single Python PR diff
  - Severity-tagged findings (BLOCKER/MAJOR/MINOR/NIT) with file:line and a concrete fix
  - Enforces Google-style docstrings, full type hints, and modern 3.11+ idioms
  - **Best for**: First-pass PR review, CI merge gates, team typing/docstring standards

### CI/CD & DevOps

- **[GitHub Actions CI/CD Pipeline for Python](./github-actions-python-cicd.md)** - 🔴 Advanced
  - Generate production-ready GitHub Actions workflows with comprehensive quality gates
  - Parallel execution: formatting, linting, testing, security scanning, build verification
  - 100% coverage enforcement, PR automation, first-contributor welcome
  - **Production metrics**: 90%+ issue detection before merge, 70% faster PR reviews
  - **Best for**: New Python projects, CI/CD modernization, open source setup

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

### Prompt Engineering & Analysis

- **[Prompt Extraction & Cataloging System](./prompt-extraction-cataloging.md)** - 🔴 Advanced
  - Extract and catalog AI/LLM prompts from GitHub repositories
  - Privacy-aware sanitization with automatic PII/secret redaction
  - Structured JSON output with quality scoring and metadata
  - **Production metrics**: 95%+ extraction accuracy, 100% privacy compliance
  - **Best for**: Prompt library building, repository audits, competitive research

## Coming Soon

Planned prompts:
- PRD generation from notes
- API documentation from code
- Technical spec writing assistant
- Architecture decision records
- Release notes generation

See [TODO.md](../../TODO.md) for planned content or [contribute](../../CONTRIBUTING.md) your own!
