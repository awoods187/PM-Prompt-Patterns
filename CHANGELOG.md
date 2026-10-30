# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Model definitions verified 2026-10-30 (#41)
- **Added** definitions for Claude Fable 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5; GPT-6 Astra, GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Luna; Gemini 4 Argon, 3.8 Flash, 3.5 Flash-Lite
- **Changed** defaults: Claude `claude-sonnet-4-5` → `claude-sonnet-5-5` (and the `claude-sonnet`/`claude-opus`/`claude-haiku` aliases now resolve to the 5.5 models), OpenAI `gpt-5` → `gpt-6.1-sol`, Gemini `gemini-2-5-flash` → `gemini-3-8-flash`
- **Deprecated** in the registry, with replacement and shutdown dates: Claude Sonnet 4.5 (retires 2026-11-30), Claude Opus 4.1 (retired 2026-08-05), o4-mini (shut down 2026-10-23), GPT-5/GPT-5 mini/o3 (shut down 2026-12-11), GPT-4.1/GPT-4.1 mini/GPT-4o/GPT-4o mini (shut down 2027-01-14)
- **Fixed** pricing for every OpenAI and Gemini model, context windows for GPT-5, GPT-4.1, o3, o4-mini, and Gemini 2.5, and API identifiers that did not exist (`gemini-2.5-pro-002`, `gpt-4.1-2025-04`, Bedrock `anthropic.claude-*-v2:0`, Vertex `@2024*` snapshots)
- **Fixed** `get_provider("claude-sonnet-5-5")` (full Claude IDs previously raised `ValueError`; only aliases worked)
- **Fixed** Claude cost estimates to use each model's cache read rate instead of a flat 10%
- **Fixed** the model updater's static fallback specs, which were stale and would have proposed reverting corrected definitions
- **Removed** `o4-mini-high` from the OpenAI provider (not an API model)

### Added
- **Comprehensive documentation overhaul** - 8,000+ lines of production-ready documentation:
  - `docs/advanced_techniques.md` (1,093 lines) - XML prompts, provider patterns, meta-prompting
  - `docs/cost_optimization.md` (1,104 lines) - ROI calculations, 85% cost reduction strategies
  - `docs/quality_evaluation.md` (866 lines) - Testing framework, CI/CD, validation
  - `docs/getting_started.md` (438 lines) - Complete beginner guide with troubleshooting
  - `docs/prompt_design_principles.md` (916 lines) - Production patterns with security
  - `docs/python_package_readme.md` (575 lines) - API documentation
- `DOCUMENTATION_REVIEW_REPORT.md` - Comprehensive 15,000-word review of all documentation
- Comprehensive `docs/project_structure.md` documenting repository organization
- Missing `__init__.py` files for proper Python package structure:
  - `ai_models/definitions/__init__.py`
  - `ai_models/definitions/anthropic/__init__.py`
  - `ai_models/definitions/google/__init__.py`
  - `ai_models/definitions/openai/__init__.py`
  - `scripts/model_updater/fetchers/__init__.py`
  - `tests/mocks/__init__.py`
- `.github/` directory for GitHub-specific files
- `.gitignore` entries for `.ruff_cache/` and `.mypy_cache/`
- This CHANGELOG.md file

### Changed
- **Standardized documentation filenames** - All docs now use lowercase_with_underscores:
  - 12 files renamed for consistency (e.g., `ATTRIBUTION.md` → `attribution.md`)
  - Updated 100+ cross-references across all documentation
- **Repository structure reorganization** - Professional organization following Python best practices
  - Moved documentation files to `docs/`:
    - `attribution.md` → `docs/attribution.md`
    - `content_license.md` → `docs/content_license.md`
    - `license_faq.md` → `docs/license_faq.md`
    - `prompt_design_principles.md` → `docs/prompt_design_principles.md`
    - `python_package_readme.md` → `docs/python_package_readme.md`
  - Moved GitHub files to `.github/`:
    - `SECURITY.md` → `.github/SECURITY.md`
    - `CONTRIBUTING.md` → `.github/CONTRIBUTING.md`
    - `CODE_OF_CONDUCT.md` → `.github/CODE_OF_CONDUCT.md`
    - `TODO.md` → `.github/ROADMAP.md` (renamed for clarity)
  - Workflows already in `.github/workflows/` (no change needed)
- **Consolidated documentation** - Merged `docs/workflows/MODEL_UPDATE_WORKFLOW.md` into `docs/model_update_system.md`

### Fixed
- **Critical: Corrected model IDs** across all documentation:
  - `claude-haiku-4-0` → `claude-haiku-4-5`
  - `claude-opus-4-0` → `claude-opus-4-1`
  - `gemini-2.0-flash-exp` → `gemini-2-5-flash`
  - Impact: All code examples now reference actual models in registry
- Import sorting in 5 test files (isort compliance)
- All CI quality gates now passing (Black, isort, Ruff, pytest)
- Broken links to moved/renamed files

### Removed
- `docs/documentation_status.md` - Outdated tracking file (replaced by CHANGELOG)
- Build and cache artifacts (not tracked in git):
  - `htmlcov/` (HTML coverage reports)
  - `dist/` (distribution packages)
  - `.mypy_cache/` (mypy cache)
  - `.ruff_cache/` (Ruff linter cache)
  - `pm_prompt_toolkit.egg-info/` (build metadata)

---

## [0.2.0] - 2025-10-31

### Added
- Google Vertex AI support to model update system
- Comprehensive `SECURITY.md` with vulnerability reporting process
- Security best practices documentation for:
  - API key management
  - Input validation
  - Cloud provider security (AWS Bedrock, Google Vertex AI)
  - Compliance considerations (GDPR, SOC 2, ISO 27001)
- `scripts/model_updater/fetchers/vertex_fetcher.py` for automated Vertex AI model updates
- AWS Bedrock support to model updater
- Vertex AI configuration to `config/model_sources.yaml`

### Changed
- Updated model updater to include all 5 fetchers (Anthropic, OpenAI, Google, Bedrock, Vertex)
- Enhanced test coverage to 80.51% (exceeds 80% target)
- Updated tests to reflect 5 fetchers (was 3)

### Fixed
- Removed exposed API keys from `.env` file (replaced with placeholders)
- Security vulnerabilities identified in code review

### Security
- **CRITICAL:** Replaced real API keys in `.env` with placeholders
- Added comprehensive security audit and documentation
- Improved input validation and XML injection prevention

---

## [0.1.0] - 2025-10-27

### Added
- Initial release of PM Prompt Patterns toolkit
- Multi-cloud LLM provider support:
  - Anthropic Claude (direct API)
  - OpenAI GPT (direct API)
  - Google Gemini (direct API)
  - AWS Bedrock (Claude models)
  - Google Vertex AI (Claude models)
- Automated model update system with GitHub Actions
- Model registry with YAML-based definitions
- Factory pattern for provider selection
- Cost calculation and optimization
- Capability-based model filtering
- Comprehensive test suite (80%+ coverage)
- CI/CD with GitHub Actions:
  - Automated testing across Python 3.9-3.12
  - Linting (Ruff, Black)
  - Type checking (mypy)
  - Security scanning (Bandit)
- Documentation:
  - Getting started guide
  - Advanced techniques
  - Cost optimization strategies
  - Quality evaluation frameworks
- Production-grade prompts library:
  - Analytics and reporting
  - Customer research
  - Developing internal tools
  - Product strategy
  - Roadmap planning
  - Stakeholder communication
- Example systems:
  - Epic categorization
  - Basic usage examples
- Templates for prompt engineering:
  - Chain-of-thought
  - Few-shot examples
  - Meta-prompting
  - Structured output

---

## Release Notes

### [Unreleased] - Repository Reorganization

This release focuses on improving the repository structure to follow Python best practices and industry standards.

**Key improvements:**
- Clean separation of concerns (source, docs, tests, config)
- Professional GitHub organization (.github/ directory)
- Improved discoverability for contributors
- Better package structure for PyPI distribution
- Comprehensive structure documentation

**No breaking changes** - All imports and functionality remain unchanged.

### [0.2.0] - Security & Cloud Provider Support

This release adds comprehensive security documentation and expands cloud provider support.

**Key improvements:**
- Vertex AI integration
- Security policy and best practices
- Enhanced test coverage
- Multi-cloud model updates

**Breaking changes:** None

### [0.1.0] - Initial Release

First production-ready release of the PM Prompt Patterns toolkit.

**Key features:**
- Multi-cloud LLM support
- Automated model updates
- Cost optimization
- Production prompts library

---

## Migration Guide

### Unreleased → 0.2.0

**Documentation file locations changed:**

| Old Location | New Location |
|--------------|--------------|
| `SECURITY.md` | `.github/SECURITY.md` |
| `CONTRIBUTING.md` | `.github/CONTRIBUTING.md` |
| `CODE_OF_CONDUCT.md` | `.github/CODE_OF_CONDUCT.md` |
| `TODO.md` | `.github/ROADMAP.md` |
| `attribution.md` | `docs/attribution.md` |
| `content_license.md` | `docs/content_license.md` |
| `license_faq.md` | `docs/license_faq.md` |
| `prompt_design_principles.md` | `docs/prompt_design_principles.md` |
| `python_package_readme.md` | `docs/python_package_readme.md` |

**No code changes required** - Python imports and functionality unchanged.

### 0.1.0 → 0.2.0

**API key security:**
- Update your `.env` file if you copied keys from repository
- Rotate any exposed API keys immediately

**Vertex AI support:**
- If using Vertex AI, set `ENABLE_VERTEX=true` in `.env`
- Configure `GCP_PROJECT_ID` and `GCP_REGION`

**No code changes required** - Backward compatible.

---

## Support

- **Issues:** [GitHub Issues](https://github.com/awoods187/PM-Prompt-Patterns/issues)
- **Security:** See [SECURITY.md](.github/SECURITY.md)
- **Contributing:** See [CONTRIBUTING.md](.github/CONTRIBUTING.md)

---

[Unreleased]: https://github.com/awoods187/PM-Prompt-Patterns/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/awoods187/PM-Prompt-Patterns/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/awoods187/PM-Prompt-Patterns/releases/tag/v0.1.0
