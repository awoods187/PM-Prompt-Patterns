# GitHub Actions CI/CD Pipeline Generator for Python

**Complexity**: 🔴 Advanced
**Category**: Development Infrastructure / CI/CD
**Model Compatibility**: ✅ Claude Opus (best) | ✅ Claude Sonnet 4 | ⚠️ GPT-5 (may need more guidance)

## Overview

Production-grade prompt for generating comprehensive GitHub Actions CI/CD pipelines for Python applications with strict quality gates, parallel execution, and comprehensive security scanning.

**Business Value**:
- Reduce setup time from 4-8 hours to 10-20 minutes (85-95% savings)
- Catch 90%+ of issues before PR merge through automated quality gates
- Accelerate PR review cycles by 70% with automated checks and clear feedback
- Prevent production bugs with 100% coverage enforcement
- Ensure consistent code quality across all contributors
- Enable safe, confident deploys with comprehensive test and security coverage

**Use Cases**:
- New Python project initialization with production-ready CI/CD
- Modernizing legacy projects without CI/CD or with outdated workflows
- Open source repository setup with community contribution support
- Enterprise projects requiring strict quality gates and compliance
- Multi-package monorepos needing coordinated testing

**Production metrics**:
- Setup time: 10-20 minutes vs 4-8 hours manual
- Issue detection rate: 90%+ before merge
- PR review time reduction: 70% faster
- CI execution time: 1-2 minutes (with caching) vs 2-4 minutes (first run)
- Developer satisfaction: 85%+ prefer automated quality gates

---

---

## Prompt

```
You are a DevOps engineer specializing in GitHub Actions and Python CI/CD pipelines. Your expertise includes workflow optimization, security scanning, test automation, and developer experience design.

## YOUR TASK

Generate a complete, production-ready GitHub Actions CI/CD pipeline for a Python application with comprehensive quality gates, parallel execution, and excellent developer experience.

---

## PROJECT CONTEXT

**Repository Structure**:
<!-- Describe your project layout -->
- Single Python package in src/mypackage/
- Tests in tests/ directory
- pyproject.toml for package configuration
- Standard Python project (library, CLI, or application)

**Python Versions**:
<!-- Specify versions to test against -->
- Primary: Python 3.11
- Additional: Python 3.12
- Matrix testing: Yes

**Quality Requirements**:
- Formatting: Black (line length 100)
- Linting: Ruff with comprehensive ruleset
- Import sorting: isort (black-compatible)
- Test coverage: 100% (strict enforcement)
- Security: Bandit, Safety, Semgrep, pip-audit

**Optional Features**:
<!-- Enable as needed -->
- [ ] PR automation (coverage diff comments, test results)
- [ ] Auto-labeling (docs, tests, dependencies)
- [ ] First-time contributor welcome
- [ ] Semantic versioning and changelog generation
- [ ] Release automation to PyPI
- [ ] Status badges for README
- [ ] Performance benchmarking vs base branch

---

## CI/CD REQUIREMENTS

### Workflow Files to Generate

1. **`.github/workflows/ci.yml`** - Main CI pipeline
   - Triggered on: push to main, all PRs, manual dispatch
   - Jobs: lint, test (matrix), security, build
   - All jobs run in parallel for fast feedback
   - Fail-fast strategy with clear error reporting

2. **`.github/workflows/release.yml`** (if release automation enabled)
   - Triggered on: GitHub release creation or tag push
   - Build wheel and sdist
   - Publish to PyPI using trusted publisher (OIDC)
   - Generate changelog from conventional commits

3. **`.github/dependabot.yml`**
   - Package ecosystem: pip
   - Update schedule: weekly
   - Open PR limit: 5
   - Auto-merge minor/patch updates (if requested)

### Configuration Files to Generate

1. **`.pre-commit-config.yaml`**
   - Must match CI configuration exactly
   - Tools: black, ruff, isort, trailing-whitespace, end-of-file-fixer, check-yaml

2. **`pyproject.toml` Tool Sections**
   - [tool.black]: line-length 100, target Python versions
   - [tool.ruff]: comprehensive select rules (I, F, E, W, C90, N, UP, S, B, A, C4, DTZ, DJ, EM, PIE, PT, Q, RET, SIM, TID, TCH, ARG, PGH, PLE, PLR, PLW, RUF)
   - [tool.isort]: profile="black", line_length 100
   - [tool.coverage.run]: omit patterns (tests/, __pycache__, .venv/)
   - [tool.coverage.report]: fail_under 100, show_missing true

3. **`.github/pull_request_template.md`**
   - Checklist: tests, docs, changelog, CI passing, coverage 100%
   - Link to contributing guidelines

4. **`.github/CODEOWNERS`** (if specified)
   - Define code ownership for auto-review assignment

---

## WORKFLOW STRUCTURE

### Main CI Pipeline (`.github/workflows/ci.yml`)

**Overall Configuration**:
```

---

## Production Patterns

### Pattern 1: Standard Python Library (Single Package)

**Context**: Python library with src-layout, comprehensive tests, publish to PyPI

**Customization**:
```
Repository Structure:
- src/mylib/ (package code)
- tests/ (pytest tests, 100% coverage)
- docs/ (optional)
- pyproject.toml (build system, dependencies, tool configs)

Quality Requirements:
- Black (line length 100)
- Ruff (comprehensive rules)
- pytest with 100% coverage
- Security: Bandit, Safety

Optional Features:
- PR automation (coverage comments)
- Release automation to PyPI
- Status badges
```

**Expected Output**:
- Main CI workflow (~120 lines)
- Release workflow (~60 lines)
- Pre-commit config (~40 lines)
- pyproject.toml tool sections (~50 lines)
- PR template, Dependabot config

**Timeline**: CI runs in 1-2 minutes with caching

**Example Project**: Standard library like `requests`, `click`, `pydantic`

---

### Pattern 2: Application with Service Dependencies

**Context**: Python application requiring database, Redis, or other services for integration tests

**Customization**:
```
Repository Structure:
- src/myapp/ (application code)
- tests/unit/ (fast unit tests, 100% coverage)
- tests/integration/ (require PostgreSQL, 95% total coverage)
- docker-compose.yml (local development)

Testing Requirements:
- Unit tests: No dependencies, 100% coverage
- Integration tests: PostgreSQL 15 service container
- Combined coverage: 95%

Services:
- PostgreSQL 15
- Redis 7 (optional)
```

**Expected Output**:
- CI workflow with service containers (~180 lines)
- Separated unit and integration test jobs
- Service health checks and proper startup
- Conditional coverage calculation

**Example service configuration**:
```yaml
test-integration:
  runs-on: ubuntu-latest
  services:
    postgres:
      image: postgres:15
      env:
        POSTGRES_PASSWORD: postgres
      options: >-
        --health-cmd pg_isready
        --health-interval 10s
        --health-timeout 5s
        --health-retries 5
      ports:
        - 5432:5432
```

**Timeline**: Unit tests 30s, integration tests 60-90s (with service startup)

**Example Project**: Django/Flask application, FastAPI with database

---

### Pattern 3: Monorepo with Multiple Packages

**Context**: Multiple related Python packages in single repository

**Customization**:
```
Repository Structure:
- packages/package-a/ (with own src/, tests/)
- packages/package-b/ (with own src/, tests/)
- packages/shared/ (common utilities)
- Shared tooling at root (pyproject.toml, .pre-commit-config.yaml)

Testing Strategy:
- Test each package separately
- Aggregate coverage across packages
- Path filtering (only test changed packages)

Matrix:
- Package x Python version (2D matrix)
```

**Expected Output**:
- CI workflow with package matrix (~150 lines)
- Path filtering to detect changed packages
- Aggregated coverage reporting
- Conditional job execution

**Example matrix strategy**:
```yaml
test:
  strategy:
    matrix:
      package: [package-a, package-b, shared]
      python-version: ['3.11', '3.12']
  steps:
    - name: Test ${{ matrix.package }}
      working-directory: packages/${{ matrix.package }}
      run: pytest --cov=src --cov-report=xml
```

**Timeline**: Parallel package testing, 2-3 minutes total

**Example Project**: Internal tooling suite, microservices monorepo

---

### Pattern 4: Open Source with Community Features

**Context**: Public repository accepting external contributions

**Customization**:
```
Repository Type: Open Source (public)

Optional Features:
- First-time contributor welcome message
- Auto-labeling (dependencies, docs, tests, bug, feature)
- Semantic versioning from conventional commits
- Automated changelog generation
- Release automation to PyPI
- Integration with Read the Docs
- CLA bot (if needed)

Community:
- CODEOWNERS for auto-review assignment
- PR template with comprehensive checklist
- Contribution guidelines link
```

**Expected Output**:
- Main CI workflow (~150 lines)
- Release workflow with changelog (~100 lines)
- First-contributor welcome workflow (~30 lines)
- PR labeler configuration
- Enhanced PR template

**Example labeler config** (`.github/labeler.yml`):
```yaml
dependencies:
  - pyproject.toml
  - requirements*.txt

docs:
  - docs/**/*
  - '**/*.md'

tests:
  - tests/**/*
```

**Timeline**: Same CI speed, plus community automation overhead

**Example Project**: Popular OSS like `httpx`, `typer`, `rich`

---

### Pattern 5: Enterprise / High-Security Requirements

**Context**: Projects with strict security, compliance, or audit requirements (HIPAA, SOC2, FINRA)

**Customization**:
```
Security Requirements:
- SAST: Bandit, Semgrep with OWASP ruleset
- SCA: Safety, pip-audit (strict mode)
- Secret scanning: TruffleHog, detect-secrets
- License compliance checking
- SBOM generation (CycloneDX, SPDX)
- Signed commits required

Compliance:
- Audit logs for all deployments
- Two-reviewer approval required
- No admin bypass on branch protection
- Automated security report generation
- Vulnerability disclosure workflow
```

**Expected Output**:
- Enhanced security workflow (~200 lines)
- Compliance reporting job
- SBOM generation on release
- Security report artifacts
- Stricter branch protection guidance

**Example Semgrep configuration**:
```yaml
security:
  steps:
    - name: Semgrep SAST
      run: |
        semgrep --config=p/owasp-top-ten \
                 --config=p/python \
                 --config=p/security-audit \
                 --error \
                 --json > semgrep-results.json

    - name: Upload Security Results
      uses: actions/upload-artifact@v4
      with:
        name: security-scan-results
        path: |
          semgrep-results.json
          bandit-report.json
          safety-report.json
```

**Timeline**: Security scans add 1-2 minutes, total 3-4 minutes

**Example Project**: Healthcare platform, financial services, government

---
