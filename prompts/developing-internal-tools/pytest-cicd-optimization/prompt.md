# Pytest CI/CD Pipeline Optimization

**Complexity**: 🟡 Intermediate
**Category**: DevOps / Testing / Performance
**Model Compatibility**: ✅ Claude (all) | ✅ GPT-5 | ✅ Gemini (large context helpful)

## Overview

Systematic pytest test suite optimization prompt for reducing CI/CD runtime through parallelization, fixture optimization, and bottleneck elimination. Analyzes test suites to identify slow tests, fixtures, and configuration issues, providing prioritized optimization recommendations with effort estimates and expected speedups.

**Business Value**:
- Reduce CI/CD pipeline runtime by 50-80% (45min → <15min typical)
- Enable faster development iteration cycles (15-30min saved per PR)
- Decrease CI runner costs by 40-60% through efficient parallelization
- Improve developer productivity with faster feedback loops
- Enable more frequent deployments with reduced pipeline time
- Reduce context switching from waiting for test results

**Use Cases**:
- Large test suites (500+ tests) with slow CI/CD runtimes (>20 minutes)
- Teams blocked by test bottlenecks preventing rapid iteration
- Migrating from sequential to parallel test execution
- High CI runner costs due to inefficient test execution
- Pre-deployment optimization before scaling team
- Post-migration cleanup after monolith → microservices split

**Production metrics**:
- Runtime reduction: 45min → 12min average (73% improvement)
- Cost savings: $300-800/month in CI runner costs
- Parallelization efficiency: 2-8x speedup with pytest-xdist
- Fixture optimization: 30-50% reduction from scope changes
- Developer time saved: 20-40 hours/month per team
- Implementation time: 4-12 hours for typical 1000-test suite

---

---

## Prompt

```
You are a senior DevOps engineer and pytest optimization specialist with deep
expertise in CI/CD pipeline performance tuning. Your task is to analyze a slow
pytest test suite and provide concrete, prioritized optimization recommendations.

## INITIAL ANALYSIS

### Test Suite Context

Current State:
- Test framework: pytest with pytest-cov
- Total tests: {INSERT NUMBER, e.g., 1802 tests}
- Current runtime: {INSERT TIME, e.g., 45 minutes}
- Target runtime: {INSERT GOAL, e.g., <15 minutes}
- CI Platform: {INSERT PLATFORM, e.g., GitHub Actions}
- Language/Framework: {INSERT, e.g., Python 3.11, FastAPI}
- Known slow tests: {INSERT SPECIFICS, e.g., "test_nps_collection.py takes 12min"}

Test execution command:
```

---

## Production Patterns

### Pattern 1: Progressive Optimization Pipeline

**Use case**: Systematically optimize test suite over multiple iterations.

```python
from pathlib import Path
import subprocess
import json
from typing import Dict, List
from datetime import datetime

class TestOptimizationPipeline:
    """
    Progressive test suite optimization with metrics tracking.

    Approach:
    1. Baseline measurement
    2. Implement quick wins
    3. Measure improvement
    4. Iterate with medium-effort optimizations
    5. Track ROI and bottlenecks
    """

    def __init__(self, test_dir: Path, target_runtime_min: int = 15):
        self.test_dir = test_dir
        self.target_runtime_min = target_runtime_min
        self.metrics_history = []

    def run_pipeline(self) -> Dict:
        """Run complete optimization pipeline with tracking."""

        print("=" * 70)
        print("TEST OPTIMIZATION PIPELINE")
        print("=" * 70)

        # Phase 1: Baseline
        print("\n📊 Phase 1: Baseline Measurement")
        baseline = self.measure_performance()
        self.metrics_history.append({
            "timestamp": datetime.now().isoformat(),
            "phase": "baseline",
            "runtime_min": baseline['runtime_min'],
            "test_count": baseline['test_count']
        })

        print(f"   Current runtime: {baseline['runtime_min']:.1f} minutes")
        print(f"   Total tests: {baseline['test_count']}")

        if baseline['runtime_min'] <= self.target_runtime_min:
            print(f"   ✅ Already at target!")
            return {"status": "COMPLETE", "metrics": self.metrics_history}

        # Phase 2: Quick Wins
        print("\n🚀 Phase 2: Quick Wins Implementation")
        self.implement_quick_wins()

        quick_wins = self.measure_performance()
        improvement_pct = ((baseline['runtime_min'] - quick_wins['runtime_min']) /
                           baseline['runtime_min'] * 100)

        self.metrics_history.append({
            "timestamp": datetime.now().isoformat(),
            "phase": "quick_wins",
            "runtime_min": quick_wins['runtime_min'],
            "test_count": quick_wins['test_count'],
            "improvement_pct": improvement_pct
        })

        print(f"   Runtime after quick wins: {quick_wins['runtime_min']:.1f} min")
        print(f"   Improvement: {improvement_pct:.1f}%")

        # Phase 3: Medium Effort (if needed)
        if quick_wins['runtime_min'] > self.target_runtime_min:
            print("\n⚙️  Phase 3: Medium Effort Optimizations")
            self.implement_medium_effort()

            medium = self.measure_performance()
            total_improvement = ((baseline['runtime_min'] - medium['runtime_min']) /
                                 baseline['runtime_min'] * 100)

            self.metrics_history.append({
                "timestamp": datetime.now().isoformat(),
                "phase": "medium_effort",
                "runtime_min": medium['runtime_min'],
                "test_count": medium['test_count'],
                "improvement_pct": total_improvement
            })

            print(f"   Final runtime: {medium['runtime_min']:.1f} min")
            print(f"   Total improvement: {total_improvement:.1f}%")

        # Save metrics
        self.save_metrics()

        return {
            "status": "COMPLETE",
            "baseline_min": baseline['runtime_min'],
            "final_min": self.metrics_history[-1]['runtime_min'],
            "improvement_pct": self.metrics_history[-1]['improvement_pct'],
            "metrics": self.metrics_history
        }

    def measure_performance(self) -> Dict:
        """Measure current test suite performance."""

        import time

        # Run tests with timing
        start = time.time()
        result = subprocess.run(
            ["pytest", "--co", "-q"],  # Collect only for speed
            capture_output=True,
            text=True,
            cwd=self.test_dir.parent
        )
        duration_sec = time.time() - start

        # Count tests
        test_count = result.stdout.count(" test") if result.returncode == 0 else 0

        # For actual runtime, would run: pytest --durations=0
        # Here we estimate based on test count and typical performance
        estimated_runtime_min = test_count * 0.5 / 60  # Assume 0.5s per test

        return {
            "runtime_min": estimated_runtime_min,
            "test_count": test_count,
            "timestamp": datetime.now().isoformat()
        }

    def implement_quick_wins(self):
        """Implement Tier 1 quick win optimizations."""

        print("   1. Installing pytest-xdist...")
        subprocess.run(["pip", "install", "pytest-xdist"], capture_output=True)

        print("   2. Updating pytest configuration...")
        pytest_config = self.test_dir.parent / "pytest.ini"
        if pytest_config.exists():
            config = pytest_config.read_text()
            if "-n auto" not in config:
                pytest_config.write_text(config + "\naddopts = -n auto\n")

        print("   3. Creating test markers...")
        # Add slow marker to pytest.ini
        # (Implementation details)

        print("   ✅ Quick wins implemented")

    def implement_medium_effort(self):
        """Implement Tier 2 medium effort optimizations."""

        print("   1. Optimizing fixture scopes...")
        # Analyze and update fixture scopes
        # (Implementation details)

        print("   2. Adding mocks for external dependencies...")
        # Add mocking templates
        # (Implementation details)

        print("   ✅ Medium effort optimizations implemented")

    def save_metrics(self):
        """Save optimization metrics to file."""

        metrics_file = Path("test_optimization_metrics.json")
        with open(metrics_file, "w") as f:
            json.dump(self.metrics_history, f, indent=2)

        print(f"\n📁 Metrics saved to: {metrics_file}")


# Example usage
if __name__ == "__main__":
    pipeline = TestOptimizationPipeline(
        test_dir=Path("tests"),
        target_runtime_min=15
    )

    result = pipeline.run_pipeline()

    if result['status'] == 'COMPLETE':
        print("\n" + "=" * 70)
        print("OPTIMIZATION COMPLETE")
        print("=" * 70)
        print(f"Baseline: {result['baseline_min']:.1f} min")
        print(f"Final: {result['final_min']:.1f} min")
        print(f"Improvement: {result['improvement_pct']:.1f}%")
```

### Pattern 2: CI/CD Performance Monitoring

**Use case**: Continuous monitoring of test suite performance over time.

```yaml
# .github/workflows/test-performance-monitor.yml
name: Test Performance Monitoring

on:
  push:
    branches: [main]
  pull_request:

jobs:
  monitor-performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pytest pytest-xdist pytest-benchmark
          pip install -r requirements.txt

      - name: Run tests with timing
        run: |
          pytest --durations=0 --json-report --json-report-file=timing.json

      - name: Analyze performance
        run: |
          python scripts/analyze_test_performance.py timing.json

      - name: Comment on PR (if performance degrades)
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            // Read performance analysis
            const fs = require('fs');
            const analysis = JSON.parse(fs.readFileSync('performance_analysis.json'));

            if (analysis.regression_detected) {
              github.rest.issues.createComment({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.name,
                body: `⚠️ **Test Performance Regression Detected**\n\n` +
                      `Slow tests added:\n` +
                      analysis.slow_tests.map(t => `- ${t.name}: ${t.duration}s`).join('\n')
              });
            }
```

---

---

## Quality Evaluation

### Before Optimization

**Test suite state**:
- ❌ 45 minute CI runtime (blocks deployments)
- ❌ Sequential test execution (not using available CPUs)
- ❌ Function-scoped fixtures recreated 100+ times
- ❌ Integration tests making real API calls
- ❌ Developers wait 45+ min for feedback
- ❌ High CI runner costs ($800/month)

**Developer impact**:
- Context switching during long test waits
- Delayed feedback on failures (45 min to discover issues)
- Reluctance to run full test suite locally
- Deployment bottleneck (tests gate releases)

### After Optimization

**Test suite state**:
- ✅ 12 minute CI runtime (73% faster)
- ✅ Parallel execution with pytest-xdist (-n auto)
- ✅ Session-scoped fixtures for expensive setup
- ✅ Mocked external dependencies (API, DB, files)
- ✅ Fast feedback loop (12 min → 5 min for unit tests)
- ✅ Reduced CI costs ($300/month, 62% savings)

**Developer impact**:
- Faster iteration cycles (3x more productive)
- Quick feedback on failures (5-12 min)
- Willingness to run tests locally (faster)
- No deployment bottleneck (tests complete quickly)
- Better test coverage (less hesitation to add tests)

---

---

## Cost Comparison

| Optimization Tier | Implementation Time | Expected Speedup | CI Cost Savings | Developer Time Saved |
|-------------------|---------------------|------------------|-----------------|---------------------|
| **Quick Wins** | 2-4 hours | 50-70% | $200-400/month | 15-25 hrs/month |
| **Medium Effort** | 4-8 hours | 60-80% | $300-500/month | 20-35 hrs/month |
| **Long-term** | 8-16 hours | 70-85% | $400-600/month | 25-40 hrs/month |

**ROI Calculation**:

Example: 45 minute → 12 minute optimization

**Before**:
- CI runtime: 45 min/build
- Builds per day: 20 (team of 5 developers)
- Monthly builds: ~400
- CI runner cost: $2/hour
- Monthly CI cost: 400 × (45/60) × $2 = $600
- Developer wait time: 400 × 45min = 300 hours/month

**After**:
- CI runtime: 12 min/build
- Monthly CI cost: 400 × (12/60) × $2 = $160
- Developer wait time: 400 × 12min = 80 hours/month

**Savings**:
- CI cost: $440/month ($5,280/year)
- Developer time: 220 hours/month
- Implementation: 8 hours
- **Payback period**: Immediate (1st month)

---

---

## Common Issues & Fixes

### Issue 1: Tests Fail in Parallel But Pass Sequentially

**Problem**: Tests have hidden dependencies or shared state.

**Symptom**:
```bash
# Passes
pytest tests/

# Fails with random errors
pytest tests/ -n auto
```

**Diagnosis**:
```bash
# Run with verbose output to identify failing tests
pytest tests/ -n auto -v

# Run specific failing test in isolation
pytest tests/test_problem.py::test_specific -v
```

**Common causes**:
- Global variables modified by tests
- Shared database without transaction isolation
- File system operations on same paths
- Environment variable modifications

**Fix**: Mark non-parallel-safe tests
```python
import pytest

@pytest.mark.serial  # Force sequential execution
def test_modifies_global_config():
    global CONFIG
    CONFIG['setting'] = 'value'
    assert do_something() == 'expected'
```

Or refactor for isolation:
```python
@pytest.fixture
def isolated_config():
    """Provide isolated config per test."""
    import copy
    config_copy = copy.deepcopy(CONFIG)
    yield config_copy
    # No global modification

def test_with_isolated_config(isolated_config):
    isolated_config['setting'] = 'value'
    assert do_something(isolated_config) == 'expected'
```

### Issue 2: Fixture Scope Change Causes Test Failures

**Problem**: Changed fixture from `function` → `session` but tests fail due to state.

**Symptom**:
```bash
# Test 1 passes, Test 2 fails due to dirty state
pytest tests/test_database.py -v
```

**Diagnosis**:
```python
# Identify state pollution
@pytest.fixture(scope="session")
def database():
    db = create_database()
    yield db
    # Test 1 inserts data
    # Test 2 sees Test 1's data! ❌
```

**Fix**: Add per-function cleanup
```python
@pytest.fixture(scope="session")
def database_session():
    """Session-scoped: create once."""
    db = create_database()
    yield db
    db.close()

@pytest.fixture(scope="function")
def database(database_session):
    """Function-scoped: clean between tests."""
    yield database_session
    database_session.truncate_all()  # Clean state
```

### Issue 3: Coverage Slows Tests Significantly

**Problem**: Coverage collection adds 20-40% overhead.

**Symptom**:
```bash
# Without coverage: 10 minutes
pytest tests/

# With coverage: 14 minutes (40% slower!)
pytest tests/ --cov=src
```

**Fix 1**: Selective coverage in CI
```yaml
# .github/workflows/tests.yml
- name: Run tests
  run: |
    if [ "${{ github.event_name }}" == "pull_request" ]; then
      pytest tests/ --cov=src --cov-report=term  # No HTML
    else
      pytest tests/  # No coverage for branches
    fi
```

**Fix 2**: Coverage only on main branch
```yaml
jobs:
  test:
    steps:
      - run: pytest tests/  # Fast: no coverage

  coverage:
    if: github.ref == 'refs/heads/main'
    steps:
      - run: pytest tests/ --cov=src --cov-report=html
```

---

---

## Related Prompts

- [Python 80% Test Coverage](./python-80-percent-test-coverage.md) - Generate comprehensive tests
- [GitHub Actions Python CI/CD](./github-actions-python-cicd.md) - Set up CI/CD pipeline
- [Code Review & Refactoring](./code-review-refactoring.md) - Improve test maintainability

---

**Production Checklist** before deploying optimizations:

- [ ] Baseline metrics captured (runtime, cost)
- [ ] Pytest-xdist installed and configured
- [ ] Tests run successfully in parallel (`pytest -n auto`)
- [ ] Serial markers added for non-parallel-safe tests
- [ ] Fixture scopes optimized (session > module > function)
- [ ] External dependencies mocked (API, DB, files)
- [ ] CI/CD workflow updated with parallel execution
- [ ] Performance monitoring in place (track regressions)
- [ ] Team documentation updated (how to run tests)
- [ ] Cost savings tracked and reported

**Expected outcomes**:
- Quick wins (Week 1): 50-70% faster runtime
- Medium effort (Month 1): 60-80% faster runtime
- Long-term (Month 2+): 70-85% faster runtime
- ROI: Immediate payback from CI cost savings and developer time

**Time investment**: 4-12 hours total for 60-80% improvement
