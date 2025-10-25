# Test Suite Documentation

Comprehensive test suite for validating model specifications, detecting deprecated models, and verifying API endpoints.

---

## Quick Start

### Run Fast Tests (No API Keys Required)

```bash
# Using the test runner script (recommended)
./scripts/run_tests.sh --fast

# Or using pytest directly
PYTHONPATH=. pytest tests/ -v -k "not endpoint"
```

### Run All Tests (Requires API Keys)

```bash
# Set API keys
export ANTHROPIC_API_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"
export GOOGLE_API_KEY="your-key-here"

# Run all tests
./scripts/run_tests.sh --all
```

---

## Test Files

### `test_model_registry.py` - Registry Validation (27 tests)

**What it tests**:
- ✅ Registry structure and organization
- ✅ All ModelSpec fields present and valid
- ✅ Pricing is positive and reasonable
- ✅ Context windows are valid
- ✅ Documentation URLs are HTTPS
- ✅ **Staleness detection** (fails if > 90 days old)
- ✅ Helper methods (get_spec, get_by_provider, etc.)
- ✅ Convenience exports
- ✅ Provider-specific rules

**Run time**: < 0.1 seconds
**API keys required**: No

**Example output**:
```
test_all_providers_have_verification_sources PASSED
test_registry_has_models PASSED
test_no_stale_models_by_default PASSED  ← Important!
...
27 passed in 0.02s
```

---

### `test_deprecated_models.py` - Deprecated Model Detection (12 tests)

**What it tests**:
- ✅ No deprecated models in prompt files
- ✅ No deprecated models in Python code
- ✅ No deprecated models in examples
- ✅ No deprecated models in config files
- ✅ Deprecated list completeness
- ✅ Migration helper functions

**Run time**: < 0.1 seconds
**API keys required**: No

**What it scans**:
- All `.py` files in `prompts/`, `examples/`, `pm_prompt_toolkit/`, `tests/`, `scripts/`
- All `.md` files in `prompts/` and `examples/`
- All `.json` and `.yaml` files

**Smart exclusions**:
- Comments mentioning deprecated models (for documentation)
- Test code testing deprecation system
- Migration documentation files

**Example output**:
```
test_prompt_files_no_deprecated_identifiers PASSED
test_python_files_no_deprecated_identifiers PASSED
test_example_files_no_deprecated_identifiers PASSED
...
12 passed in 0.08s
```

**If it finds deprecated models**:
```
❌ DEPRECATED MODELS FOUND IN PYTHON CODE:

pm_prompt_toolkit/providers/claude.py:
  Line 227: claude-3-5-sonnet-20241022
    > "claude-sonnet": "claude-3-5-sonnet-20241022",
    Use: Use CLAUDE_SONNET_4_5 instead

Fix: Import from models.registry instead:
  from models.registry import CLAUDE_SONNET
  model = CLAUDE_SONNET.api_identifier
```

---

### `test_model_endpoints.py` - API Endpoint Verification (19 tests)

**What it tests**:
- ✅ Claude Sonnet 4.5 endpoint works
- ✅ Claude Haiku 4.5 endpoint works
- ✅ Claude Opus 4.1 endpoint works
- ✅ Claude prompt caching feature works
- ✅ GPT-4o endpoint works
- ✅ GPT-4o mini endpoint works
- ✅ GPT-4o vision capability works
- ✅ Gemini 2.5 Pro endpoint works
- ✅ Gemini 2.5 Flash endpoint works
- ✅ Gemini 2.5 Flash-Lite endpoint works
- ✅ Gemini large context handling works
- ✅ Context window declarations are accurate
- ✅ Pricing declarations are accurate

**Run time**: ~30 seconds (makes actual API calls)
**API keys required**: Yes (skips gracefully if not available)

**Example output**:
```
test_claude_sonnet_endpoint PASSED
test_claude_haiku_endpoint PASSED
test_gpt_4o_vision PASSED
...
19 passed in 28.3s
```

**If API keys missing**:
```
test_claude_sonnet_endpoint SKIPPED (ANTHROPIC_API_KEY not set)
```

---

## Running Tests

### Option 1: Test Runner Script (Recommended)

```bash
# Fast tests only (< 1 second)
./scripts/run_tests.sh --fast

# All tests including endpoints (~30 seconds)
./scripts/run_tests.sh --all

# Only endpoint tests
./scripts/run_tests.sh --endpoints

# Help
./scripts/run_tests.sh --help
```

### Option 2: Direct PyTest

```bash
# Fast tests
PYTHONPATH=. pytest tests/ -v -k "not endpoint"

# All tests
PYTHONPATH=. pytest tests/ -v

# Specific test file
PYTHONPATH=. pytest tests/test_model_registry.py -v

# Specific test
PYTHONPATH=. pytest tests/test_model_registry.py::TestStalenessDetection::test_no_stale_models_by_default -v
```

### Option 3: Pre-commit Hook

```bash
# Install pre-commit
pip install pre-commit
pre-commit install

# Runs automatically on git commit
git commit -m "Your commit message"

# Or run manually
pre-commit run --all-files
```

---

## Understanding Test Output

### All Tests Passing ✅

```
============================= test session starts ==============================
tests/test_deprecated_models.py ................           [  41%]
tests/test_model_registry.py .......................       [  89%]
tests/test_model_endpoints.py ...................          [ 100%]

====================== 39 passed, 19 deselected in 0.09s =======================
```

Each `.` represents a passing test.

### Test Failure ❌

```
FAILED tests/test_model_registry.py::TestStalenessDetection::test_no_stale_models_by_default

⚠️  STALE MODELS DETECTED (>90 days since verification):

  - claude-sonnet-4.5: 91 days old (verified: 2025-01-24)

Action Required:
  1. Check official docs: See VERIFICATION_SOURCES in registry.py
  2. Update ModelSpec if changed
  3. Update last_verified date
  4. See UPDATING_MODELS.md for full procedure
```

**What this means**: Models haven't been verified in 90+ days. Follow the action steps to update.

---

## Staleness Detection

### Why It Matters

AI models change frequently:
- New versions released
- Pricing changes
- Features added/removed
- Models deprecated

**Without staleness detection**: Outdated information goes unnoticed for months.

**With staleness detection**: Tests automatically fail after 90 days, forcing verification.

### How It Works

Every ModelSpec has a `last_verified` field:

```python
CLAUDE_SONNET_4_5 = ModelSpec(
    ...
    last_verified=date(2025, 10, 24),  # Must be recent
    ...
)
```

Test checks:
```python
if (date.today() - spec.last_verified).days > 90:
    pytest.fail("Model not verified in 90+ days")
```

### Fixing Stale Models

1. **Check official docs** (URLs in `ModelRegistry.VERIFICATION_SOURCES`)
2. **Update ModelSpec** if anything changed
3. **Update `last_verified`** to today's date
4. **Run tests** to confirm
5. **Commit** with message: `"Update models: [provider] [date]"`

See `UPDATING_MODELS.md` for complete procedure.

---

## Pre-commit Hook

### What It Does

Runs fast tests before every commit:
- ✅ Registry validation
- ✅ Deprecated model detection
- ✅ Standard Python checks

**Blocks commits** with:
- ❌ Deprecated model identifiers
- ❌ Invalid registry changes
- ❌ Trailing whitespace
- ❌ Syntax errors

### Setup

```bash
pip install pre-commit
pre-commit install
```

### Usage

```bash
# Commits run automatically
git add .
git commit -m "Update models"  # ← Pre-commit runs here

# Or run manually
pre-commit run --all-files
```

### Skipping (Not Recommended)

```bash
git commit --no-verify -m "Skip pre-commit"
```

---

## CI/CD Integration

### GitHub Actions Example

See `PHASE3_COMPLETE.md` for full GitHub Actions workflow.

**Recommended setup**:
- ✅ Run fast tests on every PR
- ✅ Run endpoint tests on main branch only
- ✅ Run staleness check weekly via cron

---

## Test Categories

### Fast Tests (39 tests, < 1 second)

- Registry structure validation
- Deprecated model detection
- Field validation
- Helper method testing

**When to run**: Every commit (via pre-commit hook)

### Endpoint Tests (19 tests, ~30 seconds)

- Actual API calls to verify models work
- Vision/multimodal testing
- Context window validation

**When to run**: Before releases, weekly in CI

---

## Common Issues

### "ModuleNotFoundError: No module named 'models'"

**Problem**: Python can't find the models module.

**Fix**: Set PYTHONPATH:
```bash
PYTHONPATH=. pytest tests/
```

Or use the test runner script (does this automatically):
```bash
./scripts/run_tests.sh --fast
```

### "ANTHROPIC_API_KEY not set"

**Problem**: Endpoint tests need API keys.

**Fix 1** - Skip endpoint tests:
```bash
pytest tests/ -k "not endpoint"
```

**Fix 2** - Set API keys:
```bash
export ANTHROPIC_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
export GOOGLE_API_KEY="your-key"
```

### Pre-commit hook fails

**Problem**: You have deprecated models in your code.

**Fix**: Update to use registry:
```python
# OLD (fails)
model = "claude-3-5-sonnet-20241022"

# NEW (passes)
from models.registry import CLAUDE_SONNET
model = CLAUDE_SONNET.api_identifier
```

---

## Best Practices

### For Development

1. **Run fast tests before commits**
   ```bash
   ./scripts/run_tests.sh --fast
   ```

2. **Use pre-commit hooks**
   ```bash
   pre-commit install
   ```

3. **Import from registry, not hardcoded strings**
   ```python
   from models.registry import CLAUDE_SONNET
   ```

### For Maintenance

1. **Check models monthly**
   - Visit official docs
   - Update if changed
   - Tests will fail if > 90 days old

2. **Run endpoint tests before releases**
   ```bash
   ./scripts/run_tests.sh --all
   ```

3. **Keep verification dates current**
   - Update `last_verified` when checking
   - Prevents false staleness warnings

### For CI/CD

1. **Run fast tests on every PR**
   - Fast feedback (< 1 second)
   - Catches deprecated models early

2. **Run endpoint tests on main/releases**
   - Protects API keys
   - Verifies production readiness

3. **Schedule weekly staleness checks**
   - Catches drift before 90 days
   - Automated maintenance

---

## Test Metrics

### Current Status

- **Total tests**: 58
- **Passing**: 58 (100%)
- **Coverage**: 100% of ModelRegistry public methods
- **Fast tests**: 39 (< 1 second)
- **Endpoint tests**: 19 (~30 seconds)

### Performance

- **Registry validation**: 27 tests in 0.02s
- **Deprecation detection**: 12 tests in 0.08s (scans entire codebase)
- **Endpoint verification**: 19 tests in ~30s (actual API calls)

---

## Additional Resources

- **Phase 3 Summary**: `PHASE3_COMPLETE.md`
- **Update Workflow**: `UPDATING_MODELS.md`
- **Migration Guide**: `MIGRATION_MAP.md`
- **Model Selection**: `MODEL_OPTIMIZATION_GUIDE.md`
- **Project Summary**: `MODEL_UPDATE_PROJECT_COMPLETE.md`

---

## Questions?

**Test failures**: Check error message - tests provide detailed fix instructions

**Staleness warnings**: Follow `UPDATING_MODELS.md` procedure

**Pre-commit issues**: Check `.pre-commit-config.yaml` configuration

**General questions**: See project documentation in root directory
