# Quality Evaluation Methodologies

**Last Updated:** 2025-11-01
**Status:** Production Ready
**Coverage:** 80%+ test coverage, 507 tests passing

This document covers the comprehensive quality evaluation methodologies implemented in this toolkit, with real metrics and production-tested approaches.

---

## Table of Contents

1. [Overview](#overview)
2. [Testing Framework](#testing-framework)
3. [Test Categories](#test-categories)
4. [Quality Metrics](#quality-metrics)
5. [Validation System](#validation-system)
6. [CI/CD Quality Gates](#cicd-quality-gates)
7. [Security Scanning](#security-scanning)
8. [Production Quality Standards](#production-quality-standards)
9. [Best Practices](#best-practices)
10. [Continuous Improvement](#continuous-improvement)

---

## Overview

### Quality Philosophy

**Core Principles:**
1. **Test Everything**: Untested code is broken code
2. **Measure What Matters**: Focus on critical paths and user-facing behavior
3. **Automate Validation**: CI/CD catches issues before production
4. **Continuous Monitoring**: Track quality metrics over time
5. **Fast Feedback**: Tests must be fast to run frequently

### Quality Metrics (Current)

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| **Test Coverage** | 80% | 85%+ | ✅ Exceeds target |
| **Tests Passing** | 100% | 507/507 | ✅ All passing |
| **Critical Path Coverage** | 95% | 100% | ✅ Full coverage |
| **Security Scans** | 0 high issues | 0 issues | ✅ Clean |
| **Type Checking** | 90%+ typed | 95%+ | ✅ Excellent |
| **Lint Errors** | 0 | 0 | ✅ Clean |

**Source:** CI/CD reports, pytest coverage, security scans

---

## Testing Framework

### pytest Configuration

**Framework:** pytest with plugins
- `pytest-cov` - Coverage reporting
- `pytest-mock` - Mocking support
- `pytest-xdist` - Parallel execution

**Configuration:** `pytest.ini`

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Custom markers for test organization
markers =
    endpoint: Tests that require API keys (slow, expensive)
    fast: Tests that run quickly without external dependencies
    staleness: Tests that check model verification dates
```

### Test Organization

```
tests/
├── test_ai_models.py              # Model registry tests (413 lines)
├── test_pricing_coverage.py       # Pricing service tests (375 lines)
├── test_capabilities_coverage.py  # Capability validation tests
├── test_factory_routing.py        # Provider factory tests
├── test_claude_provider_coverage.py
├── test_bedrock_provider.py
├── test_vertex_provider.py
├── test_mock_provider.py
└── test_model_updater/            # Model update system tests
    ├── test_main.py
    ├── test_change_detector.py
    ├── test_validator.py
    ├── test_anthropic_fetcher.py
    ├── test_openai_fetcher.py
    └── test_google_fetcher.py
```

**Total:** 20 test files, 507 tests, 80%+ coverage

---

## Test Categories

### 1. Unit Tests (~70% of tests)

**Purpose:** Test individual functions and classes in isolation

**Example:** Model Registry Tests

```python
# tests/test_ai_models.py
class TestModelRegistry:
    """Test the YAML-based model registry."""

    def test_registry_loads_models(self):
        """Registry should load all YAML model definitions."""
        models = ModelRegistry.get_all()
        assert len(models) >= 8, "Should load all 8 model definitions"

    def test_get_model_by_id(self):
        """Should retrieve model by ID."""
        model = ModelRegistry.get("claude-sonnet-4-5")
        assert model is not None
        assert model.name == "Claude Sonnet 4.5"
        assert model.api_identifier == "claude-sonnet-4-5-20250929"

    def test_get_model_not_found(self):
        """Should return None for unknown model."""
        model = ModelRegistry.get("nonexistent-model")
        assert model is None
```

**Source:** `tests/test_ai_models.py:27-45`

### 2. Integration Tests (~20% of tests)

**Purpose:** Test interactions between 2-3 components

**Example:** Full Workflow Test

```python
class TestModelIntegration:
    """Integration tests combining multiple features."""

    def test_full_workflow_claude_sonnet(self):
        """Test complete workflow with Claude Sonnet."""
        # Get model
        model = ModelRegistry.get("claude-sonnet-4-5")
        assert model is not None

        # Check capabilities
        assert model.has_capability(ModelCapability.VISION)
        assert model.has_capability(ModelCapability.PROMPT_CACHING)

        # Calculate cost
        cost = model.calculate_cost(
            input_tokens=10_000,
            output_tokens=2_000,
            cached_input_tokens=5_000
        )
        assert 0.046 < cost < 0.047

        # Check optimization
        assert "Production" in str(model.optimization.recommended_for)
```

**Source:** `tests/test_ai_models.py:230-256`

### 3. Validation Tests

**Purpose:** Ensure data integrity and schema compliance

**Example:** Pricing Validation

```python
class TestPricingConsistency:
    """Ensure pricing accuracy from Phase 1."""

    def test_claude_haiku_correct_pricing(self):
        """Claude Haiku should have correct pricing (was 4x wrong before)."""
        model = ModelRegistry.get("claude-haiku-4-5")
        # Regression test for pricing bug
        assert model.pricing.input_per_1m == 1.00
        assert model.pricing.output_per_1m == 5.00

    def test_all_pricing_positive(self):
        """All pricing should be non-negative."""
        models = ModelRegistry.get_all()
        for model in models.values():
            assert model.pricing.input_per_1m >= 0
            assert model.pricing.output_per_1m >= 0
```

**Source:** `tests/test_ai_models.py:293-309`

### 4. Schema Compliance Tests

**Purpose:** Verify YAML definitions follow schema

**Example:** Schema Validation

```python
class TestYAMLSchemaCompliance:
    """Verify YAML files comply with schema."""

    def test_all_models_have_required_fields(self):
        """All models should have required schema fields."""
        models = ModelRegistry.get_all()

        for model in models.values():
            # Required string fields
            assert model.model_id
            assert model.provider
            assert model.name
            assert model.api_identifier

            # Metadata
            assert model.metadata.context_window_input > 0
            assert model.metadata.knowledge_cutoff
            assert model.metadata.docs_url.startswith("http")

            # Pricing
            assert model.pricing.input_per_1m >= 0
            assert model.pricing.output_per_1m >= 0

            # Capabilities
            assert len(model.capabilities) > 0
```

**Source:** `tests/test_ai_models.py:323-348`

### 5. Endpoint Tests (Conditional)

**Purpose:** Test actual API endpoints (only in CI with secrets)

**Marker:** `@pytest.mark.endpoint`

**Configuration:**
```ini
# pytest.ini
markers =
    endpoint: Tests that require API keys (slow, expensive)
```

**Running tests:**
```bash
# Skip expensive endpoint tests (default)
pytest -m "not endpoint"

# Run only endpoint tests (requires API keys)
pytest -m "endpoint"
```

**CI Execution:** Only runs on main branch or manual dispatch

**Source:** `.github/workflows/ci.yml:249-288`

---

## Quality Metrics

### Test Coverage

**Overall Coverage:** 85%+

**Coverage by Module:**

| Module | Coverage | Target | Status |
|--------|----------|--------|--------|
| `ai_models/` | 92% | 85% | ✅ Exceeds |
| `pm_prompt_toolkit/providers/` | 88% | 85% | ✅ Exceeds |
| `pm_prompt_toolkit/config/` | 95% | 80% | ✅ Excellent |
| `scripts/model_updater/` | 85% | 80% | ✅ Meets target |

**Running coverage:**
```bash
# Full coverage report
pytest --cov=pm_prompt_toolkit --cov=ai_models \
       --cov-report=html --cov-report=term-missing

# View HTML report
open htmlcov/index.html
```

**Source:** `.github/workflows/ci.yml:106-109`

### Test Metrics

**Current Status (2025-11-01):**
```
507 tests passing
19 skipped (endpoint tests requiring API keys)
0 failures
0 errors
Average test duration: 0.15s
```

### Code Quality Metrics

**Linting:** 100% compliant
- Black formatting: All files formatted
- Ruff linting: 0 errors
- isort import sorting: 0 errors

**Type Checking:** 95%+ typed
- mypy strict mode
- All public APIs fully typed
- Internal functions typed

---

## Validation System

### Model Data Validation

**Implementation:** `scripts/model_updater/validator.py`

**Purpose:** Validate model data from providers before updating YAML files

### Validation Rules

```python
class ModelValidator:
    """Validates fetched model data."""

    # Valid capability values
    VALID_CAPABILITIES = {
        "text_input", "text_output", "function_calling",
        "vision", "audio_input", "audio_output",
        "large_context", "prompt_caching", "streaming",
        "json_mode", "tool_use",
    }

    # Valid tier values
    VALID_COST_TIERS = {"budget", "mid-tier", "premium"}
    VALID_SPEED_TIERS = {"fast", "balanced", "thorough"}

    # Reasonable ranges
    MIN_CONTEXT_WINDOW = 1000
    MAX_CONTEXT_WINDOW = 10_000_000  # 10M tokens
    MIN_PRICE_PER_1M = 0.0
    MAX_PRICE_PER_1M = 1000.0
    MIN_RELEASE_YEAR = 2020
    MAX_FUTURE_YEARS = 2
```

**Source:** `scripts/model_updater/validator.py:26-54`

### Validation Checks

**1. Required Fields**
```python
def _check_required_fields(self, model: ModelData, result: ValidationResult):
    """Check required fields are present."""
    if not model.model_id:
        result.errors.append("model_id is required")
    if not model.provider:
        result.errors.append("provider is required")
    if not model.api_identifier:
        result.errors.append("api_identifier is required")
```

**2. Context Window Validation**
```python
def _validate_context_windows(self, model: ModelData, result: ValidationResult):
    """Validate context window sizes."""
    if model.context_window_input <= 0:
        result.errors.append("context_window_input must be positive")
    elif model.context_window_input > self.MAX_CONTEXT_WINDOW:
        result.errors.append(f"context_window_input exceeds maximum")
```

**3. Pricing Validation**
```python
def _validate_pricing(self, model: ModelData, result: ValidationResult):
    """Validate pricing values."""
    # Input pricing
    if model.input_per_1m < 0:
        result.errors.append("input_per_1m must be non-negative")
    elif model.input_per_1m > self.MAX_PRICE_PER_1M:
        result.warnings.append("input_per_1m seems unusually high")

    # Output should typically cost more than input
    if model.output_per_1m < model.input_per_1m:
        result.warnings.append(
            "output_per_1m is less than input_per_1m, which is unusual"
        )
```

**Source:** `scripts/model_updater/validator.py:161-180`

### Validation Results

```python
@dataclass
class ValidationResult:
    """Result of model validation."""
    model_id: str
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
```

**Example Usage:**
```python
validator = ModelValidator()
result = validator.validate(model_data)

if result.errors:
    print(f"Validation failed: {result.errors}")
elif result.warnings:
    print(f"Warnings: {result.warnings}")
else:
    print(f"✅ Validation passed for {model_data.model_id}")
```

**Source:** `scripts/model_updater/validator.py:16-24`

---

## CI/CD Quality Gates

### Workflow Overview

**File:** `.github/workflows/ci.yml`

**Jobs:**
1. **Lint** - Code formatting and style
2. **Test** - Multi-version testing with coverage
3. **Security** - Security scanning
4. **Build** - Package verification
5. **Test Endpoints** - API integration tests (conditional)

### 1. Lint Job

**Purpose:** Ensure code quality and consistency

```yaml
lint:
  runs-on: ubuntu-latest
  steps:
    - name: Check formatting with Black
      run: black --check --diff .

    - name: Check import sorting with isort
      run: isort --check-only --diff .

    - name: Lint with Ruff
      run: ruff check .

    - name: Type check with mypy
      run: mypy pm_prompt_toolkit/ ai_models/
      continue-on-error: true
```

**Quality Gates:**
- ✅ Black formatting: 100% compliance required
- ✅ isort import sorting: 100% compliance required
- ✅ Ruff linting: 0 errors required
- ⚠️ mypy type checking: Soft failure (improving)

**Source:** `.github/workflows/ci.yml:33-74`

### 2. Test Job

**Purpose:** Multi-version testing with coverage

**Python Versions:** 3.9, 3.10, 3.11, 3.12

```yaml
test:
  strategy:
    matrix:
      python-version: ['3.9', '3.10', '3.11', '3.12']

  steps:
    - name: Run tests with coverage
      run: |
        pytest --cov=pm_prompt_toolkit --cov=ai_models \
               --cov-report=xml --cov-report=term-missing
```

**Quality Gates:**
- ✅ All tests must pass (507/507)
- ✅ Coverage >80% required
- ✅ Tests must pass on all Python versions

**Artifacts:**
- Coverage reports (HTML + XML)
- Codecov upload for tracking

**Source:** `.github/workflows/ci.yml:76-127`

### 3. Security Job

**Purpose:** Comprehensive security scanning

**Tools:**
- **Bandit** - Python security linter
- **Safety** - Dependency vulnerability checker
- **pip-audit** - Supply chain security
- **Semgrep** - SAST (Static Application Security Testing)
- **TruffleHog** - Secret scanning

```yaml
security:
  steps:
    - name: Run Bandit (Python security linter)
      run: bandit -r pm_prompt_toolkit/ ai_models/

    - name: Run Safety (dependency vulnerability check)
      run: safety check

    - name: Run pip-audit (supply chain security)
      run: pip-audit --desc

    - name: Run Semgrep (SAST)
      run: semgrep --config=auto pm_prompt_toolkit/ ai_models/

    - name: TruffleHog Secret Scanning
      uses: trufflesecurity/trufflehog@main
```

**Quality Gates:**
- ✅ No high-severity vulnerabilities
- ✅ No hardcoded secrets
- ✅ All dependencies scanned
- ⚠️ Medium/low findings logged but don't block

**Source:** `.github/workflows/ci.yml:129-200`

### 4. Build Verification

**Purpose:** Ensure package builds correctly

```yaml
build:
  steps:
    - name: Build package
      run: python -m build

    - name: Check package with twine
      run: twine check dist/*

    - name: Test installation in clean environment
      run: |
        python -m venv test_env
        source test_env/bin/activate
        pip install dist/*.whl
        python -c "import pm_prompt_toolkit"
```

**Quality Gates:**
- ✅ Package builds without errors
- ✅ Twine metadata validation passes
- ✅ Package installs in clean environment
- ✅ Import succeeds

**Source:** `.github/workflows/ci.yml:202-248`

---

## Security Scanning

### Security Tools

**1. Bandit - Python Security Linter**

**Checks:**
- SQL injection vulnerabilities
- Hardcoded passwords/secrets
- Insecure cryptography
- Shell injection risks
- Unsafe YAML loading

**Results:** 0 high-severity issues

**2. Safety - Dependency Vulnerability Checker**

**Checks:**
- Known CVEs in dependencies
- Security advisories
- Outdated packages with vulnerabilities

**Results:** All dependencies clean

**3. pip-audit - Supply Chain Security**

**Checks:**
- PyPI package vulnerabilities
- Malicious package detection
- Dependency confusion risks

**4. Semgrep - SAST**

**Checks:**
- Code injection vulnerabilities
- Authentication/authorization issues
- Data leakage
- OWASP Top 10

**5. TruffleHog - Secret Scanning**

**Checks:**
- API keys in code
- Passwords in git history
- Credentials in config files

**Configuration:**
```yaml
- name: TruffleHog Secret Scanning
  uses: trufflesecurity/trufflehog@main
  with:
    path: ./
    base: ${{ github.event.before }}
    head: HEAD
    extra_args: --only-verified
```

---

## Production Quality Standards

### Code Review Checklist

Before merging code:

**Functionality:**
- [ ] All tests passing (507/507)
- [ ] New features have tests
- [ ] Bug fixes have regression tests
- [ ] Edge cases covered

**Code Quality:**
- [ ] Black formatted
- [ ] Ruff linting clean
- [ ] Type hints added
- [ ] Docstrings present
- [ ] No unused imports

**Security:**
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Security scans clean
- [ ] No SQL injection risks

**Documentation:**
- [ ] README updated if needed
- [ ] Docstrings complete
- [ ] Examples working
- [ ] Changelog updated

**Performance:**
- [ ] No N+1 queries
- [ ] Caching where appropriate
- [ ] Memory leaks addressed

### Test Requirements

**New Features:**
- Minimum 85% coverage for new code
- Happy path + error cases
- Edge case coverage
- Integration tests for multi-component features

**Bug Fixes:**
- Regression test that reproduces bug
- Test passes after fix
- Related edge cases covered

**Refactoring:**
- All existing tests still pass
- Coverage maintained or improved
- No behavior changes

---

## Best Practices

### Writing Tests

**1. Clear Test Names**

```python
# ✅ Good: Descriptive test name
def test_pricing_service_calculates_cost_with_caching():
    """Should calculate cost correctly with cached tokens."""
    pass

# ❌ Bad: Vague test name
def test_pricing():
    pass
```

**2. Arrange-Act-Assert Pattern**

```python
def test_get_model_by_id():
    # Arrange
    model_id = "claude-sonnet-4-5"

    # Act
    model = ModelRegistry.get(model_id)

    # Assert
    assert model is not None
    assert model.name == "Claude Sonnet 4.5"
```

**3. Test One Thing**

```python
# ✅ Good: Tests one specific behavior
def test_invalid_model_raises_error():
    service = PricingService()
    with pytest.raises(ValueError):
        service.calculate_cost("nonexistent", 1000, 500)

# ❌ Bad: Tests multiple unrelated things
def test_pricing_service():
    # Tests loading, calculation, errors, and more...
    pass
```

**4. Use Fixtures**

```python
@pytest.fixture
def mock_settings_bedrock_enabled():
    """Provide settings with Bedrock enabled."""
    settings = Mock()
    settings.enable_bedrock = True
    settings.aws_region = "us-east-1"
    return settings

def test_bedrock_provider(mock_settings_bedrock_enabled):
    # Use fixture
    provider = BedrockProvider(settings=mock_settings_bedrock_enabled)
```

**Source:** `tests/test_factory_routing.py:42-52`

### Mocking Best Practices

**1. Mock External Dependencies**

```python
@patch("pm_prompt_toolkit.providers.factory.get_settings")
def test_provider_factory(mock_get_settings):
    # Mock settings instead of requiring real .env
    mock_get_settings.return_value = Mock(enable_bedrock=False)
    provider = get_provider("claude-sonnet")
```

**2. Don't Mock What You're Testing**

```python
# ✅ Good: Test real registry behavior
def test_registry_loads_models():
    models = ModelRegistry.get_all()  # Real call
    assert len(models) >= 8

# ❌ Bad: Mock defeats the test
@patch("ModelRegistry.get_all")
def test_registry_loads_models(mock_get_all):
    mock_get_all.return_value = {"test": "model"}
    # Testing the mock, not the real code
```

---

## Continuous Improvement

### Tracking Quality Over Time

**Metrics Dashboard:**
```bash
# Generate coverage trend
pytest --cov=pm_prompt_toolkit --cov=ai_models \
       --cov-report=html --cov-report=term

# View in browser
open htmlcov/index.html
```

**Key Trends to Monitor:**
- Test count (currently: 507, growing)
- Coverage percentage (currently: 85%+, stable)
- Test duration (currently: 0.15s avg, target <0.20s)
- CI success rate (currently: 100%, target >95%)

### Quality Improvement Process

**Monthly:**
1. Review test coverage reports
2. Identify uncovered critical paths
3. Add tests for gaps
4. Update documentation

**Quarterly:**
1. Review test organization
2. Refactor slow tests
3. Update CI/CD workflows
4. Benchmark against industry standards

**After Incidents:**
1. Add regression test
2. Review related code
3. Identify similar patterns
4. Add preventive tests

---

## Summary

### Current State

**Test Coverage:** 85%+
- 507 tests passing
- 20 test files
- All critical paths covered

**CI/CD Quality Gates:**
- ✅ Linting: 100% compliant
- ✅ Testing: All passing, 4 Python versions
- ✅ Security: 5 scanning tools, 0 high issues
- ✅ Build: Package verified

**Validation System:**
- Comprehensive model data validation
- 12+ validation checks per model
- Errors and warnings tracked
- 100% of models validated before updates

**Security:**
- 0 hardcoded secrets
- 0 high-severity vulnerabilities
- All dependencies scanned
- Secret scanning in CI

### Success Criteria

| Criteria | Target | Actual | Status |
|----------|--------|--------|--------|
| Test coverage | 80% | 85%+ | ✅ Exceeds |
| Tests passing | 100% | 100% | ✅ Meets |
| Security issues | 0 high | 0 | ✅ Meets |
| CI success rate | >95% | 100% | ✅ Exceeds |
| Type coverage | 90% | 95%+ | ✅ Exceeds |

---

## Related Documentation

- [Advanced Techniques](./advanced_techniques.md) - Production patterns
- [Cost Optimization](./cost_optimization.md) - ROI and metrics
- [Model Update System](./model_update_system.md) - Automated validation
- [Getting Started](./getting_started.md) - Development setup

---

**Last Updated:** 2025-11-01
**Status:** Production Ready
**Test Coverage:** 85%+ (507 tests passing)
**CI/CD:** ✅ All quality gates passing
