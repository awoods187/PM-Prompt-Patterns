# GitHub Actions CI/CD Workflows

This directory contains automated workflows for continuous integration and quality assurance.

## Workflows

### 🧪 tests.yml - Main Test Suite
**Triggers:** Push/PR to main or develop branches

**What it does:**
- Runs on Python 3.9, 3.10, 3.11, 3.12
- Linting (Black, Ruff)
- Fast unit tests (no API calls required)
- Coverage reporting (uploads to Codecov)
- API endpoint tests (main branch only, requires secrets)

**Duration:** ~3-5 minutes

### 🔒 security.yml - Security Scanning
**Triggers:** Push/PR, weekly schedule

**What it does:**
- Bandit security linter (finds common security issues)
- Safety check (dependency vulnerability scanning)
- pip-audit (PyPI package vulnerabilities)
- TruffleHog (secret scanning)

**Duration:** ~2-3 minutes

### ✨ lint.yml - Code Quality
**Triggers:** Push/PR to main or develop branches

**What it does:**
- Black formatting check
- Ruff linting
- mypy type checking

**Duration:** ~1-2 minutes

## Setup Instructions

### 1. Enable GitHub Actions
GitHub Actions should be enabled automatically for the repository.

### 2. Add Repository Secrets (Optional)
For API endpoint testing on main branch:

Go to: Settings → Secrets and variables → Actions → New repository secret

Add:
- `ANTHROPIC_API_KEY` - For Claude endpoint tests
- `OPENAI_API_KEY` - For GPT endpoint tests
- `GOOGLE_API_KEY` - For Gemini endpoint tests

**Note:** These are optional. Tests will skip if not present.

### 3. Enable Codecov (Optional)
For coverage reporting:
1. Go to https://codecov.io/
2. Sign in with GitHub
3. Add your repository
4. Coverage reports will appear automatically

## Running Locally

You can test workflows locally using [act](https://github.com/nektos/act):

```bash
# Install act
brew install act

# Run tests workflow
act -j test

# Run security workflow
act -j security

# Run lint workflow
act -j lint
```

## Workflow Configuration

### Test Strategy
- **Fast tests:** Run on all PRs (no API keys needed)
- **API tests:** Run only on main branch (requires secrets)
- **Coverage:** Tracked and reported on all test runs

### Security Strategy
- **On every PR:** Bandit, dependency checks
- **Weekly:** Full security scan of all dependencies
- **Secret scanning:** TruffleHog checks entire git history

### Performance
- **Caching:** pip dependencies cached for faster runs
- **Matrix testing:** Parallel runs across Python versions
- **Conditional execution:** API tests only when secrets available

## Badges

Add these to your README.md:

```markdown
[![Tests](https://github.com/awoods187/PM-Prompt-Patterns/actions/workflows/tests.yml/badge.svg)](https://github.com/awoods187/PM-Prompt-Patterns/actions/workflows/tests.yml)
[![Security](https://github.com/awoods187/PM-Prompt-Patterns/actions/workflows/security.yml/badge.svg)](https://github.com/awoods187/PM-Prompt-Patterns/actions/workflows/security.yml)
[![Lint](https://github.com/awoods187/PM-Prompt-Patterns/actions/workflows/lint.yml/badge.svg)](https://github.com/awoods187/PM-Prompt-Patterns/actions/workflows/lint.yml)
```

## Troubleshooting

### Tests failing locally but passing in CI?
- Check Python version (CI runs 3.9-3.12)
- Verify all dependencies installed: `pip install -e ".[dev,test]"`

### Security workflow failing?
- Bandit may find new issues - review and add `# nosec` comments if false positives
- Dependency vulnerabilities - update requirements.txt

### Lint workflow failing?
- Run `black .` to auto-format
- Run `ruff check --fix .` to auto-fix linting issues
- Type errors are currently warnings (won't fail build)

## Future Enhancements

Potential additions:
- [ ] Deploy documentation on release
- [ ] Publish package to PyPI on tag
- [ ] Integration tests with larger test data
- [ ] Performance benchmarking
- [ ] Dependabot for automated dependency updates
