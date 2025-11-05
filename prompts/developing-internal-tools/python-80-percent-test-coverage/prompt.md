# Python 80% Test Coverage Achievement

**Complexity**: 🔴 Advanced
**Category**: Code Quality / Testing / Python
**Model Compatibility**: ✅ Claude (all) | ✅ GPT-4 | ⚠️ Gemini (large context needed)

## Overview

Systematic test generation prompt for achieving 80% code coverage across Python codebases. Works module-by-module to generate staff engineer-level pytest tests with comprehensive edge case coverage, mocking strategies, and refactoring recommendations for untestable code.

**Business Value**:
- Reduce production bugs by 60-80% with comprehensive test coverage
- Enable safe refactoring with confidence in test suite
- Meet deployment quality gates (80%+ coverage requirements)
- Reduce manual testing effort by ~40 hours per month
- Improve onboarding with self-documenting test examples
- Catch regressions before production deployment

**Use Cases**:
- Legacy codebases requiring test coverage before deployment
- Pre-open-source quality improvement
- Meeting compliance requirements (SOC2, ISO 27001)
- Technical debt reduction initiatives
- CI/CD pipeline quality gates
- Preparing code for team handoff

**Production metrics**:
- Coverage improvement: 0-30% → 80-95% systematically
- Test generation speed: ~50-100 tests per module (5-10 min)
- Edge case coverage: 90%+ (boundaries, None, empty, invalid types)
- Refactoring recommendations: ~3-5 per module for untestable code
- False positive rate: <5% (tests that don't validate behavior)

---

---

## Prompt

```
You are a staff-level Python test engineer specializing in systematic test coverage
improvement. Your expertise includes pytest, unittest, mocking strategies, and
test-driven development patterns.

## YOUR TASK

Systematically generate high-quality Python tests to achieve 80% code coverage
across an entire codebase, working module by module, while maintaining staff
engineer-level test quality and design.

---

## INITIAL SETUP

### Coverage Infrastructure

Check for existing coverage configuration:
- `.coveragerc`, `pyproject.toml[tool.coverage]`, or `setup.cfg[coverage]`
- Test framework in use (pytest, unittest, nose)
- Existing test patterns and conventions

If no coverage configuration exists, create `.coveragerc`:

[run]
source = .
omit =
    */tests/*
    */test_*.py
    */__pycache__/*
    */venv/*
    setup.py

[report]
precision = 2
show_missing = True
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:

[html]
directory = htmlcov

### Framework Selection

Primary: pytest (fixtures, parametrization, plugins)
Alternative: unittest (standard library only)
Mocking: unittest.mock or pytest-mock

Match existing framework. Default to pytest if none exists.

---

## ANALYSIS PHASE

### 1. Codebase Assessment

Run baseline coverage:
pytest --cov=src --cov-report=term-missing --cov-report=html

Generate module inventory:

Module                    | Lines | Coverage | Branch | Priority
--------------------------|-------|----------|--------|----------
src/auth/service.py      |   245 |     23%  |   18%  | SECURITY
src/payment/processor.py |   189 |     12%  |    8%  | BUSINESS
src/utils/validators.py  |    67 |     45%  |   40%  | COMPLEX

### 2. Prioritization Strategy

Test modules in this order:

1. SECURITY - Authentication, authorization, encryption, input validation
2. BUSINESS_LOGIC - Revenue-impacting, user-facing features, critical workflows
3. COMPLEX - High cyclomatic complexity (>10), algorithmic code
4. LOW_COVERAGE - Biggest coverage gaps (maximize ROI)
5. UTILITY - Helpers, validators, formatters (quick wins)

---

## TEST GENERATION STRATEGY

### Coverage Goals

Code Type           | Line Coverage | Branch Coverage
--------------------|---------------|----------------
Security-critical   | 100%          | 100%
Business logic      | 90%+          | 85%+
Complex algorithms  | 85%+          | 80%+
Utility functions   | 80%+          | 75%+

### Test Quality Requirements

1. NAMING CONVENTION

def test_<function_name>_<scenario>_<expected_behavior>():
    """One-line description of what this test validates."""

Examples:
- test_authenticate_with_valid_credentials_returns_token
- test_process_payment_when_insufficient_funds_raises_payment_error
- test_calculate_discount_with_expired_coupon_returns_zero

2. TEST STRUCTURE (AAA Pattern)

def test_calculate_discount_with_vip_customer_returns_twenty_percent():
    """Test that VIP customers receive 20% discount on all orders."""
    # Arrange - Set up test data and dependencies
    customer = Customer(status="VIP", lifetime_value=50000)
    order = Order(items=[Item(price=100.00)], customer=customer)
    calculator = DiscountCalculator()

    # Act - Execute the behavior being tested
    discount = calculator.calculate_discount(order)

    # Assert - Verify expected outcomes
    assert discount == 20.0
    assert order.discount_applied is True

3. EDGE CASE COVERAGE MATRIX

Category              | Test Cases
----------------------|-----------------------------------------------------
Boundary values       | min, max, zero, negative, overflow, underflow
Null/None             | None, null, undefined
Empty collections     | [], {}, "", set()
Invalid types         | string when int expected, None when object expected
State mutations       | Object state before/after, idempotency
Error conditions      | Network failures, timeouts, permission denied

4. MOCK STRATEGY

Mock all I/O operations:
- Database (mock connections, queries)
- Filesystem (mock open, read, write)
- Network (mock requests, API calls)
- Time-dependent (datetime.now(), time.sleep())
- Randomness (random, uuid) for deterministic tests

5. PARAMETRIZED TESTING

Use parametrization for behavior variations:

@pytest.mark.parametrize("email,expected_valid", [
    ("user@example.com", True),
    ("user.name+tag@example.co.uk", True),
    ("invalid.email", False),
    ("@example.com", False),
    ("", False),
    (None, False),
])
def test_email_validator_handles_various_formats(email, expected_valid):
    assert is_valid_email(email) == expected_valid

---

## OUTPUT FORMAT PER MODULE

Generate test file with this structure:

"""
Tests for module: <module_path>

Coverage Target: 80%
Current Coverage: <X>%
Priority: [SECURITY | BUSINESS_LOGIC | COMPLEX | LOW_COVERAGE | UTILITY]
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Any

# Import module under test
from src.<module_path> import <ClassOrFunction>

# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_database():
    """Provide mocked database connection."""
    db = Mock()
    db.query.return_value = []
    return db

# ============================================================================
# CLASS-BASED TESTS
# ============================================================================

class TestAuthService:
    """Test suite for AuthService class."""

    def test_init_with_valid_dependencies_succeeds(self, mock_database):
        """Test successful initialization with valid dependencies."""
        # Arrange & Act
        service = AuthService(db=mock_database)

        # Assert
        assert service.db == mock_database

    @pytest.mark.parametrize("username,password,expected_error", [
        (None, "password", ValueError),
        ("", "password", ValueError),
    ])
    def test_authenticate_with_invalid_input_raises_error(
        self, mock_database, username, password, expected_error
    ):
        """Test that invalid credentials raise appropriate errors."""
        service = AuthService(db=mock_database)

        with pytest.raises(expected_error):
            service.authenticate(username, password)

# ============================================================================
# FUNCTION-BASED TESTS
# ============================================================================

@pytest.mark.parametrize("input_value,expected_output", [
    (0, 0),
    (1, 1),
    (-1, 1),
])
def test_absolute_value_handles_various_inputs(input_value, expected_output):
    assert absolute_value(input_value) == expected_output

---

## REFACTORING RECOMMENDATIONS

When encountering untestable code, document refactoring suggestions:

# ❌ UNTESTABLE: Hard-coded database connection
class UserService:
    def get_user(self, user_id: int):
        db = DatabaseConnection("localhost", "prod_db")  # Hard-coded!
        return db.query(f"SELECT * FROM users WHERE id = {user_id}")

# REFACTORING NEEDED:
# 1. Dependency Injection - Pass database as constructor parameter
# 2. Repository Pattern - Separate data access from business logic
# 3. Parameterized Queries - Prevent SQL injection
# Benefit: Enables unit testing with mock database, improves security

# ✅ TESTABLE: Dependency injection
class UserService:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def get_user(self, user_id: int):
        return self.db.query("SELECT * FROM users WHERE id = ?", user_id)

---

## COVERAGE REPORT INTEGRATION

After each module, provide:

## Coverage Summary: auth/service.py

**Target:** 80% | **Achieved:** 82% ✅

### Line Coverage: 82.5% (156/189 lines)
Missing lines:
- Lines 45-47: Error handling for rate limiting (edge case, low priority)
- Line 89: Deprecated method fallback (scheduled for removal)

### Branch Coverage: 75.0% (48/64 branches)
Missing branches:
- 67->69: Exception path when external service unavailable
- 123->exit: Early return for cache hit (difficult to mock, low value)

### Next Steps to Reach 85%:
1. Add integration test for external service failure (lines 45-47)
2. Add test for cache hit scenario (branch 123->exit)
3. Document lines 89 as acceptable gap with `# pragma: no cover`

---

## ANTI-PATTERNS TO AVOID

DO NOT:

❌ Test implementation instead of behavior:
def test_get_user_calls_database():
    mock_db = Mock()
    service = UserService(mock_db)
    service.get_user(1)
    mock_db.query.assert_called_once()  # Only tests that mock was called!

❌ Write assertion-less tests:
def test_process_order():
    process_order(order_id=123)
    # No assertions! What are we testing?

❌ Multiple unrelated assertions in one test:
def test_user_service():
    assert service.get_user(1).name == "Alice"
    assert service.create_user("Bob") is not None
    assert service.delete_user(1) is True
    # These should be 3 separate tests!

DO:

✅ Test observable behavior:
def test_get_user_returns_user_with_correct_name():
    mock_db = Mock()
    mock_db.query.return_value = {"id": 1, "name": "Alice"}
    service = UserService(mock_db)

    result = service.get_user(1)

    assert result["name"] == "Alice"  # Tests real behavior

---

## MODULE COMPLETION CHECKLIST

- [ ] Coverage targets met (≥80% line, ≥75% branch)
- [ ] Security paths covered (100% for auth, validation, encryption)
- [ ] Edge cases tested (boundaries, None, empty, invalid types)
- [ ] Mocks properly scoped (narrow dependencies, cleaned up)
- [ ] Performance acceptable (unit tests <100ms per test)
- [ ] No test interdependencies (can run in any order)
- [ ] Clear failure messages (assertions provide context)
- [ ] Refactoring documented (untestable code patterns identified)

---

MODULE TO TEST:

{paste_module_code_here}
```

---

## Production Patterns

### Pattern 1: Module-by-Module Coverage Improvement

**Use case**: Systematically improve coverage for large codebase over time.

```python
from pathlib import Path
import subprocess
import json
from typing import Dict, List

class CoverageImprovementPipeline:
    """
    Systematic test generation pipeline for coverage improvement.

    Approach:
    1. Baseline coverage measurement
    2. Identify lowest-coverage modules
    3. Generate tests for priority modules
    4. Validate coverage improvement
    5. Iterate until target reached
    """

    def __init__(self, src_dir: Path, tests_dir: Path, target_coverage: float = 80.0):
        self.src_dir = src_dir
        self.tests_dir = tests_dir
        self.target_coverage = target_coverage
        self.baseline_coverage = None

    def run_pipeline(self) -> Dict:
        """Run complete coverage improvement pipeline."""

        print("=" * 70)
        print("COVERAGE IMPROVEMENT PIPELINE")
        print("=" * 70)

        # Step 1: Baseline measurement
        print("\n📊 Step 1: Measuring baseline coverage...")
        self.baseline_coverage = self.measure_coverage()
        print(f"   Current coverage: {self.baseline_coverage['overall']}%")

        if self.baseline_coverage['overall'] >= self.target_coverage:
            print(f"   ✅ Already at target ({self.target_coverage}%)")
            return {"status": "COMPLETE", "coverage": self.baseline_coverage}

        # Step 2: Identify low-coverage modules
        print("\n🔍 Step 2: Identifying low-coverage modules...")
        low_coverage_modules = self.identify_low_coverage_modules()
        print(f"   Found {len(low_coverage_modules)} modules below target")

        # Step 3: Generate tests for lowest-coverage modules first
        print("\n🔨 Step 3: Generating tests...")
        for module, coverage in low_coverage_modules[:10]:  # Top 10 priority
            print(f"\n   Module: {module} (current: {coverage}%)")
            self.generate_tests_for_module(module)

        # Step 4: Measure improvement
        print("\n📊 Step 4: Measuring coverage improvement...")
        new_coverage = self.measure_coverage()
        improvement = new_coverage['overall'] - self.baseline_coverage['overall']

        print(f"\n✅ Coverage improved by {improvement:.1f}%")
        print(f"   Before: {self.baseline_coverage['overall']}%")
        print(f"   After:  {new_coverage['overall']}%")

        if new_coverage['overall'] >= self.target_coverage:
            print(f"\n🎉 Target coverage achieved! ({self.target_coverage}%)")
            return {
                "status": "COMPLETE",
                "baseline": self.baseline_coverage,
                "final": new_coverage,
                "improvement": improvement
            }
        else:
            gap = self.target_coverage - new_coverage['overall']
            print(f"\n⚠️  Still {gap:.1f}% below target")
            print(f"   Run pipeline again to continue improvement")
            return {
                "status": "IN_PROGRESS",
                "baseline": self.baseline_coverage,
                "current": new_coverage,
                "improvement": improvement,
                "gap": gap
            }

    def measure_coverage(self) -> Dict:
        """Measure current code coverage."""

        # Run pytest with coverage
        result = subprocess.run(
            [
                "pytest",
                str(self.tests_dir),
                f"--cov={self.src_dir}",
                "--cov-report=json",
                "--cov-report=term"
            ],
            capture_output=True,
            text=True
        )

        # Parse coverage.json
        with open(".coverage.json") as f:
            coverage_data = json.load(f)

        # Calculate per-module coverage
        module_coverage = {}
        for file_path, file_data in coverage_data['files'].items():
            module_name = Path(file_path).stem
            coverage_pct = file_data['summary']['percent_covered']
            module_coverage[file_path] = coverage_pct

        overall = coverage_data['totals']['percent_covered']

        return {
            "overall": overall,
            "by_module": module_coverage
        }

    def identify_low_coverage_modules(self) -> List[tuple[str, float]]:
        """Identify modules below target coverage."""

        low_coverage = []
        for module, coverage in self.baseline_coverage['by_module'].items():
            if coverage < self.target_coverage:
                low_coverage.append((module, coverage))

        # Sort by coverage (lowest first)
        low_coverage.sort(key=lambda x: x[1])

        return low_coverage

    def generate_tests_for_module(self, module_path: str) -> None:
        """Generate tests for specific module."""

        # Determine priority based on module name
        priority = "UTILITY"
        if "auth" in module_path or "security" in module_path:
            priority = "SECURITY"
        elif "payment" in module_path or "order" in module_path:
            priority = "BUSINESS_LOGIC"

        # Generate tests (using previous function)
        result = generate_test_suite(Path(module_path), priority)

        # Write test file
        module_name = Path(module_path).stem
        test_file = self.tests_dir / f"test_{module_name}.py"

        if test_file.exists():
            # Append to existing test file
            with open(test_file, "a") as f:
                f.write("\n\n# Additional tests\n")
                f.write(result['test_code'])
        else:
            # Create new test file
            test_file.write_text(result['test_code'])

        print(f"      ✅ Generated {result['test_count']} tests")


# Example usage
if __name__ == "__main__":
    pipeline = CoverageImprovementPipeline(
        src_dir=Path("src"),
        tests_dir=Path("tests"),
        target_coverage=80.0
    )

    result = pipeline.run_pipeline()

    if result['status'] == 'COMPLETE':
        print(f"\n🎉 Success! Coverage: {result['final']['overall']}%")
    else:
        print(f"\n⚠️  Continue: {result['gap']}% to target")
```

### Pattern 2: Pre-Commit Coverage Enforcement

**Use case**: Prevent commits that reduce test coverage.

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔍 Checking test coverage..."

# Run tests with coverage
pytest --cov=src --cov-report=term --cov-fail-under=80

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Coverage below 80% threshold"
    echo ""
    echo "Generate tests for new code:"
    echo "  python scripts/generate_tests.py path/to/new_module.py"
    echo ""
    echo "Or skip this check (not recommended):"
    echo "  git commit --no-verify"
    echo ""
    exit 1
fi

echo "✅ Coverage check passed"
```

---

---

## Quality Evaluation

### Before (No Tests)

**Codebase state**:
- ❌ 0% test coverage
- ❌ No confidence in refactoring
- ❌ Manual testing only
- ❌ Frequent production bugs
- ❌ Unclear edge case handling
- ❌ Difficult onboarding (no test examples)

**Risk**:
- Cannot safely refactor code
- Regressions reach production
- Manual testing takes 2-3 hours per release
- Bugs discovered by customers

### After (80% Coverage)

**Codebase state**:
- ✅ 80-95% test coverage
- ✅ Confident refactoring
- ✅ Automated testing (1-2 min CI)
- ✅ Regressions caught in CI
- ✅ Edge cases documented in tests
- ✅ Self-documenting test examples

**Benefits**:
- Safe refactoring with test safety net
- Regressions caught before production (90%+)
- Automated testing saves ~40 hours/month
- Tests serve as usage documentation
- New developers onboard faster (learn from tests)

---

---

## Cost Comparison

| Model | Context | Cost/Module | Speed | Coverage | Quality | Notes |
|-------|---------|-------------|-------|----------|---------|-------|
| **Claude Haiku** | 200K | $0.05 | Fast | 75-85% | Good | Misses edge cases |
| **Claude Sonnet** | 200K | $0.10-0.30 | Medium | 80-95% | Excellent | **Recommended** |
| **Claude Opus** | 200K | $0.50-1.00 | Slow | 90-98% | Exceptional | Overkill for most |
| **GPT-4o** | 128K | $0.20-0.50 | Medium | 75-90% | Very Good | Good structured output |
| **GPT-4o** | 128K | $0.10-0.25 | Fast | 70-85% | Good | Fast iteration |
| **Gemini Pro 1.5** | 2M | $0.08-0.20 | Medium | 70-85% | Good | Large modules |

**Module = ~100-500 lines of code**

**Recommendation**:
- **Claude Sonnet 3.5**: Best balance for most projects (comprehensive tests, good edge case coverage)
- **GPT-4o**: Faster iteration when time is critical, acceptable quality
- **Claude Opus**: Security-critical modules requiring exceptional coverage

**ROI Calculation**:
- Manual test writing: ~2-4 hours per module (15-30 tests)
- LLM-generated tests: ~5-10 minutes per module (50-100 tests)
- Cost: $0.10-0.30 per module
- **Time savings: 1.5-4 hours per module**
- **Payback: Immediate (first module)**

---

---

## Common Issues & Fixes

### Issue 1: Tests Pass But Don't Validate Behavior

**Problem**: Generated tests only check mocks, not actual behavior.

**Symptom**:
```python
# BAD: Only tests that mock was called
def test_save_user():
    mock_db = Mock()
    service = UserService(mock_db)
    service.save_user(User(id=1))
    mock_db.save.assert_called_once()  # Doesn't test behavior!
```

**Fix**: Add to prompt:
```xml
<guideline>
Tests must verify observable behavior, not just mock interactions:
- Return values (correct data returned)
- State changes (object state before/after)
- Side effects (database writes, file modifications)
- Exception handling (correct exceptions raised)

Mock assertions are supplementary, not primary validation.
</guideline>
```

**Example**:
```python
# GOOD: Tests actual behavior
def test_save_user_returns_saved_user_with_id():
    mock_db = Mock()
    mock_db.save.return_value = User(id=1, name="Alice", created_at=datetime.now())
    service = UserService(mock_db)

    result = service.save_user(User(name="Alice"))

    assert result.id == 1
    assert result.name == "Alice"
    assert result.created_at is not None
```

### Issue 2: Flaky Tests (Time-Dependent)

**Problem**: Tests fail intermittently due to time dependencies.

**Symptom**:
```python
# FLAKY: Depends on current time
def test_token_expires_after_one_hour():
    token = generate_token(user_id=1)
    time.sleep(3601)  # Sleep for 1 hour + 1 second
    assert is_expired(token) is True  # Flaky!
```

**Fix**: Use mocking for time-dependent code:
```python
from freezegun import freeze_time
from datetime import datetime, timedelta

@freeze_time("2024-01-01 12:00:00")
def test_token_expires_after_one_hour():
    """Test token expiration using frozen time."""
    token = generate_token(user_id=1)

    # Move time forward 1 hour + 1 second
    with freeze_time("2024-01-01 13:00:01"):
        assert is_expired(token) is True

@freeze_time("2024-01-01 12:00:00")
def test_token_valid_within_one_hour():
    """Test token validity within expiration window."""
    token = generate_token(user_id=1)

    # Move time forward 59 minutes
    with freeze_time("2024-01-01 12:59:00"):
        assert is_expired(token) is False
```

### Issue 3: Coverage Achieved But Low Quality

**Problem**: 80% coverage but tests are brittle or unclear.

**Symptom**:
- Tests break on minor refactoring
- Unclear what behavior is being tested
- No edge cases covered

**Fix**: Emphasize test quality in prompt:
```xml
<quality_criteria>
  <maintainability>
    - Tests should survive refactoring (test behavior, not implementation)
    - Clear test names describing scenario and expectation
    - AAA pattern clearly visible (Arrange, Act, Assert)
  </maintainability>

  <comprehensiveness>
    - Happy path + edge cases + error conditions
    - Boundary value testing (min, max, zero, negative)
    - All documented error conditions tested
  </comprehensiveness>

  <clarity>
    - Docstrings explain what behavior is being validated
    - Single assertion per test (or related assertions)
    - Minimal setup (use fixtures for reusable setup)
  </clarity>
</quality_criteria>
```

---

---

## Related Prompts

- [Code Review & Refactoring](./code-review-refactoring.md) - Prepare code for testing
- [GitHub Actions Python CI/CD](./github-actions-python-cicd.md) - Enforce coverage in CI
- [CLAUDE.md Generator](./claude-md-generator.md) - Establish testing standards

---

**Production Checklist** before considering module "done":

- [ ] Coverage ≥ 80% line, ≥ 75% branch
- [ ] All security-critical paths tested (100%)
- [ ] Edge cases documented and tested (None, empty, boundaries)
- [ ] Mocks properly scoped and cleaned up (fixtures)
- [ ] Tests run in < 100ms per test (unit tests)
- [ ] No test interdependencies (can run in any order)
- [ ] Clear failure messages (descriptive assertions)
- [ ] Refactoring recommendations documented (if untestable code found)
- [ ] AAA pattern followed (Arrange, Act, Assert)
- [ ] Parametrization used for input variations

**Estimated effort**:
- Small module (< 200 LOC): 10-20 minutes with LLM generation
- Medium module (200-500 LOC): 20-40 minutes
- Large module (500+ LOC): 40-90 minutes
- Manual equivalent: 2-8 hours per module

**Time savings: 80-90% compared to manual test writing**
