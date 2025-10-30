# Pytest CI/CD Pipeline Optimization Expert

## Metadata

- **Title:** Pytest CI/CD Speed Optimization & Bottleneck Analysis
- **Best for:**
  - Large test suites (500+ tests) with slow CI/CD runtimes
  - Teams blocked by test bottlenecks preventing rapid iteration
  - Migrating from sequential to parallel test execution
- **Recommended model:** Claude Sonnet 4.5 (best balance of analysis depth and speed for large codebases)
- **Use with:** Claude Code (for file analysis and implementation)
- **Estimated tokens:** 8-15K input (codebase analysis), 4-8K output (detailed recommendations)
- **Category:** Code / DevOps / Performance Optimization
- **Related prompts:** github-actions-python-cicd.md, code-review-refactoring.md

---

## The Prompt

```markdown
You are a senior DevOps engineer and pytest optimization specialist with deep expertise in CI/CD pipeline performance tuning. I need you to analyze my slow pytest test suite and provide a concrete, prioritized optimization plan.

## CONTEXT

**Current State:**
- Test framework: pytest with pytest-cov
- Total tests: [INSERT NUMBER, e.g., 1802 tests]
- Current runtime: [INSERT TIME, e.g., 45 minutes]
- Target runtime: [INSERT GOAL, e.g., <15 minutes]
- CI Platform: [INSERT PLATFORM, e.g., GitHub Actions]
- Language/Framework: [INSERT, e.g., Python 3.11, FastAPI]
- Known issues: [INSERT SPECIFICS, e.g., "test_nps_collection.py blocks entire suite"]

**Test execution command:**
```bash
[INSERT COMMAND, e.g., python3 -m pytest --cov=src --cov-report=term-missing]
```

## YOUR ANALYSIS TASKS

### Phase 1: Profile & Identify Bottlenecks (30 minutes)

1. **Examine CI/CD Configuration**
   - Read `.github/workflows/*.yml` (or CI config files)
   - Document current: runner specs, timeout settings, parallelization approach
   - Identify: Are tests running sequentially? What's the runner type?

2. **Analyze Pytest Configuration**
   - Read `pytest.ini`, `pyproject.toml`, or `setup.cfg`
   - Check for: custom markers, timeout configs, coverage settings
   - Document: Which plugins are in use? (pytest-xdist, pytest-timeout, etc.)

3. **Profile Test Suite**
   Execute or simulate:
   ```bash
   pytest --durations=50 --collect-only  # Get test count by file
   pytest --durations=0 > test_durations.txt  # If possible to run
   ```

   Analyze test files to identify:
   - Tests taking >5 seconds (list top 20 slowest)
   - Files with most tests (could benefit from splitting)
   - Tests with external dependencies (DB, API, file I/O)

4. **Deep Dive: Known Slow Tests**
   For the specific slow test file(s) mentioned:
   - **Read the entire file** (e.g., `test_nps_collection.py`)
   - Identify WHY it's slow:
     - [ ] Actual API calls (not mocked)?
     - [ ] Database operations?
     - [ ] Large file operations?
     - [ ] Complex setup/teardown fixtures?
     - [ ] Unnecessary sleeps/waits?
     - [ ] Parametrized tests with too many cases?
   - Provide line-by-line analysis of the bottleneck

5. **Fixture Analysis**
   - Read all `conftest.py` files
   - Identify fixtures with:
     - `scope="function"` that could be `"session"` or `"module"`
     - Heavy setup operations (DB creation, API mocking)
     - Redundant initialization across tests
   - Check for fixture dependency chains

6. **Shared State & Parallelization Safety**
   - Scan for global variables, shared files, singleton patterns
   - Identify tests that CANNOT run in parallel:
     - Database tests without transaction isolation
     - Tests modifying environment variables
     - Tests writing to same file paths
   - Provide list of test files/classes that need `pytest.mark.serial`

### Phase 2: Optimization Recommendations (Prioritized)

For each recommendation, provide:
- **Impact:** Expected speedup (e.g., "3-4x faster")
- **Effort:** Hours to implement (Low: <2h, Medium: 2-8h, High: >8h)
- **Risk:** Low/Medium/High (chance of breaking tests)
- **Implementation:** Exact commands, code changes, or configuration

#### Tier 1: Quick Wins (Implement First)

**1.1 Enable Parallel Execution with pytest-xdist**
```toml
# pyproject.toml addition
[tool.pytest.ini_options]
addopts = "-n auto"  # or specify worker count
```

Provide:
- Optimal worker count for [CI runner type]
- Command: `pytest -n auto --dist loadscope`
- List any tests that need `@pytest.mark.serial` marker
- Expected impact: [X]x speedup

**1.2 Separate Fast/Slow Tests**
Create test markers:
```python
# pytest.ini
[pytest]
markers =
    slow: marks tests as slow (>5s)
    integration: marks tests requiring external services
```

Provide GitHub Actions workflow split:
```yaml
# .github/workflows/tests.yml
jobs:
  fast-tests:
    # Run first for quick feedback
    # pytest -m "not slow and not integration" -n auto

  slow-tests:
    # Run in parallel with fast tests
    # pytest -m "slow or integration" -n auto
```

**1.3 Optimize Coverage Collection**
- Only run coverage on main branch or specific jobs?
- Use `--cov-context=test` to identify expensive coverage operations
- Consider: `pytest --cov=src --cov-report=html` only for PRs, not every push

#### Tier 2: Medium Effort Optimizations

**2.1 Fix Slow Test Fixtures**
For each fixture identified in Phase 1:
```python
# BEFORE (slow)
@pytest.fixture(scope="function")
def database():
    db = create_database()  # Called 100 times!
    yield db
    db.cleanup()

# AFTER (fast)
@pytest.fixture(scope="session")
def database():
    db = create_database()  # Called once!
    yield db
    db.cleanup()

@pytest.fixture(scope="function")
def clean_database(database):
    database.truncate_all()  # Fast cleanup per test
    yield database
```

**2.2 Mock External Dependencies**
For [specific slow test file]:
```python
# test_nps_collection.py - SPECIFIC FIXES
# Line XX: Replace actual API call
@mock.patch('module.api_client.post')
def test_nps_submission(mock_post):
    mock_post.return_value = MockResponse(200)
    # ... test logic
```

**2.3 Implement Test Splitting Across Jobs**
Use pytest-split for intelligent distribution:
```yaml
# .github/workflows/tests.yml
strategy:
  matrix:
    group: [1, 2, 3, 4]
steps:
  - run: pytest --splits 4 --group ${{ matrix.group }}
```

#### Tier 3: Long-Term Improvements

**3.1 Pytest Cache Optimization**
```toml
[tool.pytest.ini_options]
cache_dir = ".pytest_cache"
```

GitHub Actions caching:
```yaml
- uses: actions/cache@v3
  with:
    path: |
      ~/.cache/pip
      .pytest_cache
    key: ${{ runner.os }}-pytest-${{ hashFiles('**/requirements*.txt') }}
```

**3.2 Conditional Test Execution**
Run only tests affected by code changes:
```bash
pytest --testmon  # Requires pytest-testmon
# Or use pytest-picked for git-aware test selection
```

**3.3 Refactor Slow Tests**
For tests that CANNOT be parallelized or optimized:
- Move to nightly test suite
- Run only on main branch merges
- Consider if they're testing the right thing (integration vs e2e)

### Phase 3: Implementation Plan

Provide a week-by-week rollout:

**Week 1: Quick Wins**
- [ ] Day 1: Add pytest-xdist, run with `-n 4` locally
- [ ] Day 2: Mark slow tests, create fast/slow split in CI
- [ ] Day 3: Optimize coverage to run only on main branch
- [ ] Expected: 50% runtime reduction

**Week 2: Medium Effort**
- [ ] Day 1-2: Fix fixture scopes (focus on top 5 heavy fixtures)
- [ ] Day 3-4: Mock external dependencies in [slow test files]
- [ ] Day 5: Implement test splitting across 4 jobs
- [ ] Expected: Additional 30% reduction (total 65% vs baseline)

**Week 3: Long-term & Monitoring**
- [ ] Implement pytest cache in GitHub Actions
- [ ] Set up test duration monitoring (fail if tests >10s without @slow marker)
- [ ] Document parallelization safety guidelines for team

### Phase 4: Validation & Monitoring

**Metrics to track:**
```python
# Add to CI workflow
- name: Test Duration Report
  run: |
    pytest --durations=20 | tee test_durations.txt
    # Fail if any test >10s without @slow marker
```

**Success Criteria:**
- [ ] Total runtime < [TARGET, e.g., 15 minutes]
- [ ] Coverage remains >=[THRESHOLD]%
- [ ] No flaky tests introduced by parallelization
- [ ] Fast tests give feedback in <5 minutes

## OUTPUT FORMAT

Provide your analysis as:

### 1. Executive Summary
- Current runtime: [X] minutes
- Target runtime: [Y] minutes
- Top 3 bottlenecks identified
- Recommended approach & expected outcome

### 2. Bottleneck Analysis
**Slowest Tests (Top 20):**
| Test File | Test Name | Duration | Root Cause | Fix Complexity |
|-----------|-----------|----------|------------|----------------|
| test_nps_collection.py | test_create_survey | 45s | Real API calls | Low (add mocks) |

**Fixture Issues:**
- [List fixtures with scope problems]

**Parallelization Blockers:**
- [List tests requiring serial execution]

### 3. Prioritized Recommendations
For each tier (1-3), provide:
- Recommendation name
- Impact (speedup estimate)
- Effort (hours)
- Risk level
- Exact implementation (code/config)

### 4. Implementation Timeline
Week-by-week plan with:
- Tasks
- Expected cumulative impact
- Validation steps

### 5. Code Changes
Provide ready-to-use:
- pytest.ini or pyproject.toml updates
- GitHub Actions workflow modifications
- Fixture refactoring examples
- Mock implementation for slow tests

### 6. Monitoring & Maintenance
- Metrics to track
- CI checks to prevent regression
- Team guidelines for writing fast tests

## CONSTRAINTS

- Do NOT suggest removing tests or reducing coverage goals
- Do NOT recommend solutions requiring paid CI runners unless marked as "optional"
- Do prioritize solutions that work on standard GitHub Actions runners
- Do provide exact commands/code, not just concepts
- Do validate that parallel execution won't break existing tests before recommending it

## SPECIFIC QUESTIONS TO ANSWER

1. **For the known slow test file ([INSERT FILE]):**
   - What is the root cause of slowness? (Provide line numbers)
   - Is it fixable with mocking/fixture changes? (Provide code)
   - If not fixable, should it be isolated? (Provide strategy)

2. **Parallelization safety:**
   - List all tests that CANNOT run in parallel
   - Provide markers/configuration to handle them
   - Estimate speedup with X workers

3. **Coverage overhead:**
   - How much time is coverage adding? (Benchmark if needed)
   - Can we reduce it without losing visibility?

4. **CI workflow:**
   - Should we split into multiple jobs? (Provide workflow YAML)
   - What's the optimal job matrix?

Start by reading the CI configuration and pytest config, then dive into the slowest test files. Provide concrete, copy-paste-ready solutions.
```

---

## Customization Tips

### For Different Test Counts
- **Small suites (<200 tests):** Focus on Tier 1 only, parallel execution likely sufficient
- **Large suites (>2000 tests):** Add Tier 4 for test sharding across 8+ jobs
- **Massive suites (>5000 tests):** Consider pytest-split with duration-based distribution

### For Different CI Platforms
- **GitHub Actions:** Use matrix strategy examples as provided
- **GitLab CI:** Replace with `parallel: 4` and `CI_NODE_INDEX`
- **Jenkins:** Focus on Jenkins Pipeline parallelization with `parallel` blocks
- **CircleCI:** Use CircleCI test splitting with timing data

### For Different Test Types
- **Unit test heavy:** Aggressive parallelization (8-16 workers), minimal mocking needed
- **Integration test heavy:** Focus on fixture optimization, database transaction isolation
- **E2E test heavy:** Separate into nightly suite, optimize critical path only

### For Different Coverage Requirements
- **High coverage enforcement (>90%):** Keep coverage in main workflow, optimize collection only
- **Moderate coverage (<80%):** Run coverage weekly or on main branch only
- **Coverage for specific modules:** Use `--cov=src/critical_module` to reduce overhead

### Optional Additions
Add section for:
- **Test data management:** If tests use large fixtures or databases
- **Docker optimization:** If tests run in containers (layer caching, multi-stage builds)
- **Flaky test detection:** Add `pytest-rerunfailures` configuration
- **Test result caching:** Implement `pytest-testmon` for incremental testing

---

## Usage Examples

### Example 1: Large Django Application (2000+ tests)

**Input:**
```markdown
**Current State:**
- Test framework: pytest with pytest-cov and pytest-django
- Total tests: 2,147 tests
- Current runtime: 52 minutes
- Target runtime: <15 minutes
- CI Platform: GitHub Actions (ubuntu-latest)
- Language/Framework: Python 3.11, Django 4.2
- Known issues: "API integration tests in test_external_apis.py take 15+ minutes"
```

**Expected Output:**
- Analysis identifies 23 tests hitting real Stripe API (no mocking)
- Recommends `pytest-xdist -n 8` for 4.5x speedup (52min → 11.5min)
- Provides fixture refactoring for `django_db` scope issues
- Delivers GitHub Actions workflow with 4-job matrix
- Shows how to mock Stripe API calls with `responses` library

### Example 2: FastAPI Microservice (500 tests)

**Input:**
```markdown
**Current State:**
- Test framework: pytest with httpx async tests
- Total tests: 487 tests
- Current runtime: 18 minutes
- Target runtime: <5 minutes
- CI Platform: GitHub Actions
- Language/Framework: Python 3.12, FastAPI, async tests
- Known issues: "All tests seem slow, no obvious bottleneck"
```

**Expected Output:**
- Discovers fixture with `scope="function"` creating Redis connection 487 times
- Recommends `scope="session"` + flush between tests for 8x speedup on fixtures
- Identifies 12s spent on coverage overhead, suggests `--cov-report=` to skip terminal output
- Provides async-safe parallelization config (`pytest-xdist` with `--dist loadgroup`)
- Final runtime: 4.2 minutes with `-n 4`

### Example 3: Data Pipeline (300 tests, very slow)

**Input:**
```markdown
**Current State:**
- Test framework: pytest with pyspark tests
- Total tests: 312 tests
- Current runtime: 89 minutes
- Target runtime: <20 minutes
- CI Platform: GitHub Actions
- Language/Framework: Python 3.10, PySpark, pandas
- Known issues: "test_pipeline_transformations.py takes 67 minutes alone"
```

**Expected Output:**
- Identifies that PySpark session is created per-test (should be session-scoped)
- Discovers tests processing 50MB CSV files that could use 1KB samples
- Recommends test data reduction: `@pytest.fixture` with `spark.read.csv('data/sample_1k.csv')`
- Provides `conftest.py` with session-scoped SparkSession
- Suggests splitting slow PySpark tests to nightly suite (run daily, not per-commit)
- Final runtime: 12 minutes for fast tests, 67-minute tests moved to nightly

---

## Testing Checklist

### Before Implementation
- [ ] Run `pytest --durations=50` locally to confirm slow tests
- [ ] Check if tests currently pass 100% (don't optimize broken tests)
- [ ] Review CI logs for actual bottlenecks (download time, test time, etc.)
- [ ] Verify pytest version supports recommended plugins (pytest>=7.0 for most)

### Validate Parallelization Safety
- [ ] Run `pytest -n 4` locally and verify all tests pass
- [ ] Check for flaky tests (run 10 times: `pytest --count=10`)
- [ ] Verify no race conditions on file writes, DB operations
- [ ] Test with `--dist loadscope`, `--dist loadfile`, `--dist loadgroup` to find optimal

### After Quick Wins (Tier 1)
- [ ] CI runtime reduced by at least 30%
- [ ] No new test failures introduced
- [ ] Coverage percentage unchanged (within ±1%)
- [ ] Fast tests provide feedback in <5 minutes

### After Medium Effort (Tier 2)
- [ ] CI runtime reduced by 50-70% total
- [ ] No flaky tests detected over 50 runs
- [ ] Team can run tests locally in <3 minutes
- [ ] Slow tests properly marked and isolated

### Edge Cases to Consider
- [ ] Tests with `@pytest.mark.parametrize` creating 100+ test cases (consider splitting)
- [ ] Tests requiring specific execution order (use `pytest-order` or mark as serial)
- [ ] Tests that modify global state (environment variables, logging config)
- [ ] Tests with time-based assertions (may fail with parallelization)
- [ ] Tests creating files in shared directories (use `tmp_path` fixture)

### Quality Criteria for Outputs
The analysis should:
- [ ] Identify at least 80% of runtime bottleneck by specific file/function
- [ ] Provide copy-paste-ready code for top 3 optimizations
- [ ] Include exact pytest commands to validate each change
- [ ] Show before/after runtime estimates with confidence ranges
- [ ] Link to pytest plugin documentation for recommended tools

### Common Failure Modes & Fixes

**Issue:** Parallel tests fail with database errors
- **Cause:** Tests sharing database without transaction isolation
- **Fix:** Use `pytest-django` with `--reuse-db` and `transaction=True`

**Issue:** Coverage drops after parallelization
- **Cause:** pytest-cov incompatible with xdist
- **Fix:** Use `pytest-cov>=4.0` with `--cov-append` or use `coverage combine`

**Issue:** Tests slower with xdist than sequential
- **Cause:** Too many workers for test count, or heavy fixture overhead
- **Fix:** Reduce workers (`-n 2` instead of `-n auto`), fix fixture scopes

**Issue:** Random test failures with parallelization
- **Cause:** Shared global state, race conditions
- **Fix:** Mark flaky tests with `@pytest.mark.serial`, isolate state

**Issue:** GitHub Actions still slow despite local speedup
- **Cause:** Runner CPU limits, cold cache
- **Fix:** Add dependency caching, use `ubuntu-latest-4-cores` runner type

---

## Production Metrics & Validation

### Success Stories (Expected Results)

**Typical outcomes by test suite size:**
- **500 tests:** 15min → 4min (73% reduction) with xdist + fixture optimization
- **1000 tests:** 30min → 9min (70% reduction) with xdist + test splitting
- **2000 tests:** 52min → 13min (75% reduction) with xdist + mocking + splitting
- **5000+ tests:** 2h+ → <20min (85% reduction) with aggressive splitting + test selection

### Cost/Benefit Analysis

**Time Investment:**
- Tier 1 (Quick Wins): 4-6 hours → 50% speedup
- Tier 2 (Medium Effort): 16-24 hours → 70% speedup
- Tier 3 (Long-term): 40+ hours → 85% speedup

**ROI Calculation:**
For a 10-person team with tests running 20x/day:
- Before: 30min/run × 20 runs × 10 people = 100 hours/day waiting
- After (70% reduction): 9min/run × 20 runs × 10 people = 30 hours/day waiting
- **Saved: 70 engineering hours/day** (8.75 FTE freed up!)

### Anti-Patterns to Avoid

❌ **Don't:** Skip tests to make CI faster
✅ **Do:** Mark slow tests and run them less frequently

❌ **Don't:** Remove coverage to save time
✅ **Do:** Run coverage on PRs only, not every commit

❌ **Don't:** Parallelize without checking for shared state
✅ **Do:** Audit for race conditions first, mark unsafe tests

❌ **Don't:** Increase worker count beyond CPU core count
✅ **Do:** Use `-n auto` or `-n <cores>` for optimal distribution

❌ **Don't:** Mock everything to make tests fast
✅ **Do:** Mock external dependencies, keep business logic integration real

---

## Related Patterns & Workflows

### Use This Prompt With:

1. **github-actions-python-cicd.md** - For comprehensive CI/CD setup after optimization
2. **code-review-refactoring.md** - For reviewing test code quality during refactoring
3. **python-80-percent-test-coverage.md** - For maintaining coverage while optimizing speed

### Follow-Up Prompts:

**After optimization, run:**
- "Implement pytest-testmon for incremental testing on our optimized suite"
- "Create test duration monitoring dashboard for our CI/CD pipeline"
- "Design flaky test detection and quarantine system for parallel execution"

### Integration Points:

- **Pre-commit hooks:** Run fast tests only locally (`-m "not slow"`)
- **PR validation:** Run full suite with coverage
- **Main branch:** Run full suite + slow tests + coverage
- **Nightly:** Run E2E tests, performance tests, security scans

---

## Troubleshooting Guide

### Issue: "My tests are still slow after parallelization"

**Debug steps:**
```bash
# 1. Profile with timing data
pytest --durations=0 -n 4 > parallel_durations.txt
pytest --durations=0 > sequential_durations.txt
diff parallel_durations.txt sequential_durations.txt

# 2. Check worker distribution
pytest -n 4 -v  # Watch which worker runs which test

# 3. Test different distribution strategies
pytest -n 4 --dist loadscope
pytest -n 4 --dist loadfile
pytest -n 4 --dist loadgroup
```

**Common causes:**
- Heavy fixture running on every worker → Fix scope
- Tests not evenly distributed → Use `--dist loadscope`
- Too many workers for test count → Reduce worker count

### Issue: "Coverage is broken after adding xdist"

**Solution:**
```toml
# pyproject.toml
[tool.coverage.run]
parallel = true
concurrency = ["multiprocessing"]

[tool.pytest.ini_options]
addopts = "--cov --cov-report=html --cov-report=term -n auto"
```

Then in CI:
```bash
pytest -n auto
coverage combine
coverage report
```

### Issue: "Some tests fail only in parallel mode"

**Root cause identification:**
```bash
# Run suspect test in isolation
pytest path/to/test.py::test_name -v

# Run with different worker counts
pytest -n 1 path/to/test.py
pytest -n 2 path/to/test.py
pytest -n 4 path/to/test.py

# Check for shared state
grep -r "global " tests/
grep -r "os.environ" tests/
grep -r "open(" tests/
```

**Fix pattern:**
```python
# Mark problematic tests
@pytest.mark.serial
def test_modifies_global_state():
    ...

# Or fix the test to be parallel-safe
def test_uses_tmp_path(tmp_path):
    output_file = tmp_path / "output.txt"  # Unique per test worker
```

---

## Advanced Optimizations (For Power Users)

### Conditional Test Execution
```yaml
# Only run tests affected by code changes
- name: Get changed files
  id: changed
  uses: tj-actions/changed-files@v39

- name: Run affected tests
  run: |
    if [[ "${{ steps.changed.outputs.all_changed_files }}" == *"src/"* ]]; then
      pytest tests/unit/
    fi
```

### Test Result Caching
```python
# pytest.ini
[pytest]
cache_dir = .pytest_cache

# GitHub Actions
- uses: actions/cache@v3
  with:
    path: .pytest_cache
    key: pytest-${{ github.sha }}
    restore-keys: pytest-
```

### Dynamic Worker Scaling
```python
# conftest.py
def pytest_configure(config):
    import os
    import multiprocessing

    if os.getenv("CI"):
        # GitHub Actions: use all cores
        workers = multiprocessing.cpu_count()
    else:
        # Local: leave some cores free
        workers = max(1, multiprocessing.cpu_count() - 2)

    config.option.numprocesses = workers
```

---

## Version Compatibility

**Tested with:**
- pytest: 7.0+ (8.0+ recommended)
- pytest-xdist: 3.0+
- pytest-cov: 4.0+
- Python: 3.9, 3.10, 3.11, 3.12
- GitHub Actions: ubuntu-20.04, ubuntu-22.04, ubuntu-latest

**Known issues:**
- pytest <7.0: `--dist loadgroup` not available
- pytest-cov <4.0: Incompatible with pytest-xdist parallelization
- Python 3.8: Some async test parallelization issues

---

## License & Attribution

This prompt pattern is optimized for:
- GitHub Actions workflows (primary)
- GitLab CI (adaptable)
- Jenkins Pipeline (adaptable)
- CircleCI (adaptable)

Based on production testing optimization patterns from:
- pytest-xdist documentation
- pytest-dev/pytest best practices
- Real-world optimizations of 1000+ test suites

**Last updated:** 2025-10-29
**Prompt version:** 1.0.0
