# Project Structure

**Last Updated:** 2025-11-01
**Version:** 1.0.0

---

## Overview

This document describes the organization and structure of the PM Prompt Patterns repository. The project follows Python best practices with a clear separation of concerns between source code, documentation, tests, and configuration.

---

## Directory Structure

```
PM-Prompt-Patterns/
├── .github/                    # GitHub-specific files
│   ├── workflows/             # GitHub Actions CI/CD workflows
│   │   ├── ci.yml            # Main CI pipeline (tests, linting, security)
│   │   ├── auto-update-models.yml  # Automated model updates
│   │   └── check-model-staleness.yml  # Weekly staleness checks
│   ├── ISSUE_TEMPLATE/        # Issue templates (future)
│   ├── CONTRIBUTING.md        # Contribution guidelines
│   ├── CODE_OF_CONDUCT.md     # Community code of conduct
│   ├── SECURITY.md            # Security policy and vulnerability reporting
│   └── ROADMAP.md             # Project roadmap and feature planning
│
├── ai_models/                  # Model registry and definitions
│   ├── __init__.py
│   ├── capabilities.py        # Model capability definitions
│   ├── pricing.py             # Pricing calculations
│   ├── registry.py            # Central model registry
│   └── definitions/           # YAML model definitions by provider
│       ├── __init__.py
│       ├── schema.md          # YAML schema documentation
│       ├── anthropic/         # Claude model definitions
│       │   ├── __init__.py
│       │   └── *.yaml
│       ├── google/            # Gemini model definitions
│       │   ├── __init__.py
│       │   └── *.yaml
│       └── openai/            # GPT model definitions
│           ├── __init__.py
│           └── *.yaml
│
├── config/                     # Configuration files
│   └── model_sources.yaml     # Model source configuration for updater
│
├── docs/                       # Documentation
│   ├── advanced_techniques.md # Advanced prompt engineering techniques
│   ├── cost_optimization.md   # Cost optimization strategies
│   ├── getting_started.md     # Getting started guide
│   ├── quality_evaluation.md  # Quality evaluation frameworks
│   ├── model_update_system.md # Model update system documentation
│   ├── attribution.md         # Attribution and credits
│   ├── content_license.md     # Content licensing information
│   ├── license_faq.md         # License FAQ
│   ├── prompt_design_principles.md  # Prompt design principles
│   ├── python_package_readme.md     # Python package documentation
│   ├── project_structure.md   # This file
│   └── workflows/             # Workflow documentation
│       └── MODEL_UPDATE_WORKFLOW.md
│
├── examples/                   # Usage examples
│   ├── basic_example.py       # Basic usage example
│   └── epic-categorization/   # Production epic categorization system
│       └── README.md
│
├── pm_prompt_toolkit/          # Main Python package (source code)
│   ├── __init__.py            # Package initialization and public API
│   ├── config/                # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py        # Pydantic settings with env var support
│   ├── optimizers/            # Optimization utilities (future)
│   │   └── __init__.py
│   ├── providers/             # LLM provider implementations
│   │   ├── __init__.py
│   │   ├── base.py           # Base provider interface
│   │   ├── claude.py         # Anthropic Claude provider
│   │   ├── openai.py         # OpenAI GPT provider
│   │   ├── gemini.py         # Google Gemini 2.5 Provider
│   │   ├── bedrock.py        # AWS Bedrock provider
│   │   ├── vertex.py         # Google Vertex AI provider
│   │   ├── mock.py           # Mock provider for testing
│   │   └── factory.py        # Provider factory with routing logic
│   └── utils/                 # Utility functions
│       └── __init__.py
│
├── prompts/                    # Production prompt library
│   ├── analytics/             # Analytics and reporting prompts
│   │   ├── README.md
│   │   ├── investigation/
│   │   ├── monitoring/
│   │   └── reporting/
│   ├── customer-research/     # Customer research prompts
│   │   └── README.md
│   ├── developing-internal-tools/  # Internal tooling prompts
│   │   ├── README.md
│   │   ├── claude-md-generator.md
│   │   ├── code-review-refactoring.md
│   │   ├── enterprise-readme-generator.md
│   │   ├── llm-orchestration-system.md
│   │   ├── prompt-extraction-cataloging.md
│   │   ├── pytest-cicd-optimization.md
│   │   └── python-80-percent-test-coverage.md
│   ├── product-strategy/      # Product strategy prompts
│   │   ├── README.md
│   │   ├── meta-prompt-designer.md
│   │   └── opus-code-execution-pattern.md
│   ├── roadmap-planning/      # Roadmap planning prompts
│   │   └── README.md
│   └── stakeholder-communication/  # Stakeholder communication
│       ├── README.md
│       ├── executive-deck-review.md
│       └── remove-ai-writing-patterns.md
│
├── scripts/                    # Utility scripts
│   ├── __init__.py
│   ├── README.md              # Scripts documentation
│   ├── check_staleness.py     # Check model verification dates
│   ├── verify_current_models.py  # Verify model configurations
│   └── model_updater/         # Automated model update system
│       ├── __init__.py
│       ├── main.py            # Main orchestrator
│       ├── change_detector.py # Detect changes in model definitions
│       ├── pr_creator.py      # Create GitHub PRs
│       ├── validator.py       # Validate model data
│       └── fetchers/          # Model fetchers by provider
│           ├── __init__.py
│           ├── base_fetcher.py
│           ├── anthropic_fetcher.py
│           ├── openai_fetcher.py
│           ├── google_fetcher.py
│           ├── bedrock_fetcher.py
│           └── vertex_fetcher.py
│
├── templates/                  # Prompt engineering templates
│   ├── chain-of-thought.md    # Chain-of-thought prompting
│   ├── few-shot-examples.md   # Few-shot learning examples
│   ├── meta-prompting.md      # Meta-prompting techniques
│   └── structured-output.md   # Structured output templates
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── README.md              # Testing documentation
│   ├── mocks/                 # Test fixtures and mocks
│   │   ├── __init__.py
│   │   └── future_models.yaml
│   ├── test_model_updater/    # Model updater tests
│   │   ├── __init__.py
│   │   ├── test_main.py
│   │   ├── test_anthropic_fetcher.py
│   │   ├── test_openai_fetcher.py
│   │   ├── test_google_fetcher.py
│   │   ├── test_change_detection.py
│   │   ├── test_fetchers.py
│   │   └── test_validator.py
│   ├── test_ai_models.py      # AI models registry tests
│   ├── test_bedrock_basic.py  # Bedrock provider tests
│   ├── test_capabilities_coverage.py
│   ├── test_claude_provider_coverage.py
│   ├── test_factory_coverage.py
│   ├── test_factory_routing.py
│   ├── test_mock_provider.py
│   ├── test_model_endpoints.py
│   ├── test_pricing_coverage.py
│   ├── test_providers_base.py
│   ├── test_providers_stubs.py
│   ├── test_registry_coverage.py
│   └── test_settings_config.py
│
├── .env.example                # Environment variable template
├── .gitignore                  # Git ignore rules
├── .pre-commit-config.yaml     # Pre-commit hooks configuration
├── .ruff.toml                  # Ruff linter configuration
├── LICENSE                     # MIT License
├── pyproject.toml              # Python project configuration (PEP 518)
├── pytest.ini                  # Pytest configuration
├── README.md                   # Main project README
└── requirements.txt            # Production dependencies

```

---

## Key Directories Explained

### Source Code (`pm_prompt_toolkit/`)

The main Python package containing all production source code. Follows standard Python package structure with proper `__init__.py` files for package discovery.

**Key modules:**
- `config/` - Settings management with Pydantic
- `providers/` - LLM provider implementations with factory pattern
- `utils/` - Shared utility functions

### Model Registry (`ai_models/`)

Centralized model registry with YAML-based model definitions. Each provider has its own subdirectory with individual YAML files per model.

**Features:**
- Model capability tracking
- Pricing calculations
- Automated updates via GitHub Actions
- Version control for model metadata

### Documentation (`docs/`)

Comprehensive documentation including:
- Getting started guides
- Advanced techniques
- Cost optimization strategies
- System architecture documentation

### Tests (`tests/`)

Complete test suite with 80%+ code coverage:
- Unit tests for all modules
- Integration tests for providers
- Model updater system tests
- Mock fixtures for testing without API calls

### Configuration (`config/`)

Configuration files separate from code:
- Model source definitions
- Update automation settings

### GitHub Integration (`.github/`)

GitHub-specific files:
- CI/CD workflows (tests, linting, security scans)
- Automated model updates
- Community health files (CONTRIBUTING, CODE_OF_CONDUCT, SECURITY)
- Project roadmap

---

## File Naming Conventions

### Python Files
- `lowercase_with_underscores.py` for modules
- `test_*.py` for test files
- `__init__.py` for package initialization

### Documentation
- `UPPERCASE.md` for important docs (README, LICENSE, CONTRIBUTING)
- `lowercase-with-hyphens.md` for general documentation
- `Title_Case.md` for specific topics

### Configuration
- `.lowercase` for dotfiles (.gitignore, .env)
- `lowercase.toml` for configuration (pyproject.toml, ruff.toml)
- `lowercase.yaml` for data files

---

## Package Structure

### Entry Points

Defined in `pyproject.toml`:
- `pm-classify` - Classification CLI
- `pm-cost-calc` - Cost calculator CLI

### Python Package Discovery

Uses `setuptools` with automatic package discovery:
```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["pm_prompt_toolkit*"]
exclude = ["tests*", "docs*", "examples*"]
```

---

## Development Workflow

### Local Development

1. **Setup environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -e ".[dev]"
   ```

2. **Run tests:**
   ```bash
   pytest                    # Run all tests
   pytest -v --cov          # With coverage
   pytest tests/test_*.py   # Specific test file
   ```

3. **Code quality:**
   ```bash
   ruff check .             # Lint
   black .                  # Format
   mypy pm_prompt_toolkit   # Type check
   ```

4. **Pre-commit hooks:**
   ```bash
   pre-commit install       # Install hooks
   pre-commit run --all-files  # Run manually
   ```

### Adding New Features

1. **Add source code:** `pm_prompt_toolkit/`
2. **Add tests:** `tests/test_*.py`
3. **Add documentation:** `docs/`
4. **Add examples:** `examples/` (if applicable)
5. **Update README:** Link to new features

---

## Build and Distribution

### Building the Package

```bash
python -m build          # Creates wheel and source distribution in dist/
```

### Installing Locally

```bash
pip install -e .         # Editable install (for development)
pip install .            # Standard install
```

### Publishing (Maintainers Only)

```bash
python -m build
twine check dist/*
twine upload dist/*      # Upload to PyPI
```

---

## Continuous Integration

### GitHub Actions Workflows

**CI Pipeline** (`.github/workflows/ci.yml`):
- Linting (Ruff, Black)
- Type checking (mypy)
- Security scanning (Bandit)
- Tests (pytest) across Python 3.9-3.12
- Code coverage reporting

**Model Updates** (`.github/workflows/auto-update-models.yml`):
- Automated weekly model updates
- Creates PRs with changes
- Auto-merges if tests pass

**Staleness Checks** (`.github/workflows/check-model-staleness.yml`):
- Checks model verification dates
- Creates issues for stale models

---

## Best Practices

### Code Organization

✅ **DO:**
- Keep source code in `pm_prompt_toolkit/`
- Keep tests in `tests/`
- Use `__init__.py` for all Python packages
- Follow PEP 8 naming conventions
- Add type hints to all functions
- Write docstrings (Google style)

❌ **DON'T:**
- Mix source code and tests
- Commit build artifacts (dist/, *.egg-info/)
- Commit cache directories (__pycache__/, .mypy_cache/)
- Hardcode credentials
- Skip tests for new features

### Documentation

✅ **DO:**
- Document all public APIs
- Include usage examples
- Maintain this project_structure.md
- Update README when adding features
- Link between related documents

❌ **DON'T:**
- Leave TODOs in documentation
- Include outdated information
- Write implementation details in user docs
- Duplicate content across files

### Testing

✅ **DO:**
- Maintain 80%+ code coverage
- Test happy paths and edge cases
- Use mocks for external dependencies
- Write descriptive test names
- Group tests in classes by feature

❌ **DON'T:**
- Skip tests for "simple" code
- Test implementation details
- Make tests depend on each other
- Commit failing tests
- Use real API keys in tests

---

## Migration Log

**2025-11-01: Repository Reorganization**
- Created `.github/` directory for GitHub-specific files
- Moved `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` to `.github/`
- Moved `TODO.md` to `.github/ROADMAP.md`
- Moved documentation files to `docs/`:
  - `attribution.md`
  - `content_license.md`
  - `license_faq.md`
  - `prompt_design_principles.md`
  - `python_package_readme.md`
- Added missing `__init__.py` files:
  - `ai_models/definitions/__init__.py`
  - `ai_models/definitions/anthropic/__init__.py`
  - `ai_models/definitions/google/__init__.py`
  - `ai_models/definitions/openai/__init__.py`
  - `scripts/model_updater/fetchers/__init__.py`
  - `tests/mocks/__init__.py`
- Updated `.gitignore` to exclude `.ruff_cache/` and `.mypy_cache/`
- Removed build artifacts: `htmlcov/`, `dist/`, `.mypy_cache/`, `.ruff_cache/`, `pm_prompt_toolkit.egg-info/`
- Created this documentation file

---

## Future Structure Considerations

### Potential Additions

- `notebooks/` - Jupyter notebooks for analysis and tutorials
- `benchmarks/` - Performance benchmark scripts
- `docker/` - Docker configurations
- `docs/api/` - Auto-generated API documentation (mkdocs)

### Not Recommended

- `src/` folder - Current flat structure is standard for single-package repos
- Splitting `pm_prompt_toolkit/` - Package is well-organized as-is
- Moving `config/` into package - Keep config separate from code

---

## Questions?

- **Documentation issues?** Open an issue or PR
- **Structure questions?** See [CONTRIBUTING.md](../.github/CONTRIBUTING.md)
- **Need help?** Open a discussion on GitHub

---

**Maintained by:** Andy Woods
**Last Review:** 2025-11-01
**Next Review:** 2025-12-01
