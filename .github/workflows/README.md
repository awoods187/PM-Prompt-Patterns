# GitHub Actions CI/CD Workflows

This directory contains the production-ready CI/CD pipeline for the PM Prompt Toolkit project.

## Workflows

### 🚀 ci.yml - Unified CI Pipeline
**Triggers:** Push to main, all PRs, manual dispatch

**What it does (all jobs run in parallel):**

1. **Lint** - Code quality and formatting
   - Black formatting verification
   - isort import sorting
   - Ruff linting
   - mypy type checking

2. **Test** - Comprehensive testing matrix
   - Python versions: 3.9, 3.10, 3.11, 3.12
   - Full test suite with coverage
   - Codecov integration
   - Coverage artifact uploads

3. **Security** - Multi-layer security scanning
   - Bandit (Python security linter)
   - Safety (dependency vulnerabilities)
   - pip-audit (supply chain security)
   - Semgrep (SAST)
   - TruffleHog (secret scanning)

4. **Build** - Package verification
   - Build wheel and sdist
   - Validate with twine
   - Test installation in clean venv

5. **Test Endpoints** - Live API testing (conditional)
   - Runs on main branch or manual trigger
   - Requires API secrets
   - Tests real Claude/GPT/Gemini endpoints

**Duration:** 2-3 minutes (with cache)

**Performance features:**
- Intelligent caching per job
- Concurrency control (cancels outdated runs)
- Path filtering (skips docs-only changes)

## Setup Instructions

### 1. Repository Settings

#### Branch Protection for `main`
Navigate to: **Settings → Branches → Add rule**

Required status checks:
- ✓ lint
- ✓ test (3.9, 3.10, 3.11, 3.12)
- ✓ security
- ✓ build

Settings:
- ☑ Require PR reviews (1 approval)
- ☑ Require status checks to pass
- ☑ Require branches to be up to date
- ☑ Dismiss stale reviews
- ☑ Include administrators

#### GitHub Secrets (Optional)
Navigate to: **Settings → Secrets and variables → Actions**

For API endpoint testing:
- `ANTHROPIC_API_KEY` - Claude endpoint tests
- `OPENAI_API_KEY` - GPT endpoint tests
- `GOOGLE_API_KEY` - Gemini endpoint tests
- `PYPI_API_TOKEN` - PyPI releases (future)

#### Enable Security Features
Navigate to: **Settings → Code security and analysis**

Enable:
- ☑ Dependency graph
- ☑ Dependabot alerts
- ☑ Dependabot security updates
- ☑ Secret scanning

### 2. Local Development Setup

#### Install Pre-commit Hooks
```bash
pip install pre-commit
pre-commit install

# Test hooks
pre-commit run --all-files
```

#### Install Dependencies
```bash
pip install -e ".[dev,test]"
```

#### Run Checks Locally (matches CI)
```bash
# Formatting
black --check --diff .
black .  # auto-fix

# Import sorting
isort --check-only --diff .
isort .  # auto-fix

# Linting
ruff check .
ruff check --fix .  # auto-fix

# Type checking
mypy pm_prompt_toolkit/ ai_models/

# Tests with coverage
pytest --cov=pm_prompt_toolkit --cov=ai_models --cov-report=html --cov-report=term-missing

# Build package
python -m build
twine check dist/*
```

### 3. Testing the Pipeline

#### Option A: Create Test Branch
```bash
git checkout -b test-ci
echo "# CI Test" >> test.txt
git add test.txt
git commit -m "test: Verify CI configuration"
git push -u origin test-ci
# Open PR and watch workflows run
```

#### Option B: Manual Workflow Dispatch
1. Go to **Actions** tab
2. Select **CI** workflow
3. Click **Run workflow**
4. Select branch and run

## Workflow Architecture

### Caching Strategy
Each job caches dependencies independently:
```
${{ runner.os }}-pip-{job}-{python-version}-${{ hashFiles('pyproject.toml') }}
```

**Benefits:**
- Faster CI runs (2-3 min vs 4-6 min cold)
- Independent job caches
- Automatic invalidation on dependency changes

### Path Filtering
CI skips when ONLY these change:
- Markdown files (`**.md`)
- Documentation (`docs/**`)
- License file

### Concurrency Control
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```
Cancels outdated runs when new commits pushed.

## Tool Configuration

All tools configured in `pyproject.toml`:

**Black:** Line length 100, targets Python 3.9-3.12
**isort:** Black-compatible profile, line length 100
**Ruff:** Comprehensive ruleset (30+ categories), line length 100
**Coverage:** Branch coverage enabled, HTML reports in `htmlcov/`

**Pre-commit matches CI exactly** - see `.pre-commit-config.yaml`

## Status Badges

Add to README.md:

```markdown
![CI](https://github.com/awoods187/PM-Prompt-Patterns/workflows/CI/badge.svg)
![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
```

## Troubleshooting

### Pre-commit hooks failing
```bash
# Update hooks
pre-commit autoupdate

# Clear cache
pre-commit clean
pre-commit run --all-files
```

### CI failing but local passes
**Causes:**
1. Different Python version - test all 3.9-3.12
2. Missing dependency - check `pyproject.toml`
3. Cached dependencies - clear GitHub cache
4. Path differences - use relative paths

**Debug:**
```bash
# Test in clean environment
python -m venv fresh_env
source fresh_env/bin/activate
pip install -e ".[dev,test]"
pytest
```

### Security scan false positives
Add `# nosec B101` with justification:
```python
# nosec B101 - Assert acceptable in tests
assert result == expected
```

## Maintenance

### Dependency Updates
Dependabot runs weekly (Monday 9am UTC).

**Manual update:**
```bash
pre-commit autoupdate
pip install -e ".[dev,test]" --upgrade
pre-commit run --all-files
pytest
```

## Performance Metrics

**With cache:**
- Lint: 30-45s
- Test (per version): 60-90s
- Security: 60-90s
- Build: 30-45s
- **Total: 2-3 minutes**

**Without cache:** 4-6 minutes
