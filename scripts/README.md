# Scripts

Utility scripts for maintaining the PM Prompt Toolkit.

## Model Maintenance Scripts

### model_updater/ - Automated Model Update System

**Automated system for fetching, validating, and updating AI model definitions.**

**Quick Start:**
```bash
# Dry run (no changes)
python scripts/model_updater/main.py --dry-run

# Full run with PR creation
python scripts/model_updater/main.py
```

**Key Features:**
- ✅ Automated weekly updates via GitHub Actions
- ✅ Multi-provider support (Anthropic, OpenAI, Google)
- ✅ Intelligent change detection (pricing, capabilities, metadata)
- ✅ Comprehensive validation with sanity checks
- ✅ Auto-PR creation with detailed changelogs
- ✅ Auto-merge when tests pass
- ✅ Deprecation tracking for removed models
- ✅ 29 tests with 100% critical path coverage

**Environment Variables:**
- `GITHUB_TOKEN`: Required for PR creation (auto-provided in Actions)
- `OPENAI_API_KEY`: Optional, for OpenAI API access
- `ANTHROPIC_API_KEY`: Optional, for Anthropic API access
- `GOOGLE_API_KEY`: Optional, for Google API access

**Automation:**
- **Schedule**: Every Sunday at 2am UTC
- **Workflow**: `.github/workflows/auto-update-models.yml`
- **Action**: Creates PR with updates if changes detected

**Complete Documentation:** [docs/model_update_system.md](../docs/model_update_system.md)

**Testing:**
```bash
# Run all model updater tests
pytest tests/test_model_updater/ -v

# Test with future mock models
python -c "import yaml; print(yaml.safe_load(open('tests/mocks/future_models.yaml')))"
```

### check_staleness.py

Check if model definitions need verification based on `last_verified` dates.

**Usage:**
```bash
# Check all models (90-day threshold)
python scripts/check_staleness.py

# Custom staleness threshold
python scripts/check_staleness.py --days 60

# Check specific provider only
python scripts/check_staleness.py --provider anthropic

# Quiet mode (only output if stale models found)
python scripts/check_staleness.py --quiet
```

**Exit codes:**
- `0`: All models current
- `1`: Stale models found
- `2`: Error occurred

**Output:**
```
================================================================================
MODEL STALENESS REPORT - 2025-10-29
================================================================================

Staleness Threshold: 90 days
Stale if not verified since: 2025-07-31

Total Models: 8
  Current: 8
  Stale:   0

✅ All models are current!
```

### verify_current_models.py

Test model API endpoints to confirm they're accessible and working.

**Usage:**
```bash
# Test all models
python scripts/verify_current_models.py

# Test specific provider
python scripts/verify_current_models.py --provider anthropic

# Test specific model
python scripts/verify_current_models.py --model claude-sonnet-4-5
```

**Requirements:**
- API keys set in `.env` or environment:
  - `ANTHROPIC_API_KEY`
  - `OPENAI_API_KEY`
  - `GOOGLE_API_KEY`
- Provider packages installed:
  - `anthropic`
  - `openai`
  - `google-generativeai`

**Exit codes:**
- `0`: All tested models passed
- `1`: Some models failed
- `2`: Setup error (missing dependencies/keys)

**Output:**
```
Testing claude-sonnet-4-5 (claude-sonnet-4-5-20250929)... ✅ PASS
Testing gpt-4o (gpt-4o)... ✅ PASS
Testing gemini-2-5-pro (gemini-2.5-pro)... ✅ PASS

================================================================================
MODEL VERIFICATION SUMMARY
================================================================================

Total Models: 3
  ✅ Passed:  3
  ❌ Failed:  0
  ⏭️  Skipped: 0
```

## Automated Checks

The `check_staleness.py` script runs automatically via GitHub Actions:

- **Schedule**: Every Monday at midnight UTC
- **Workflow**: `.github/workflows/check-model-staleness.yml`
- **Action**: Creates GitHub issue if stale models detected

## Related Documentation

- [Model Update Workflow](../docs/workflows/MODEL_UPDATE_WORKFLOW.md) - Complete update procedure
- [Contributing Guide](../CONTRIBUTING.md) - How to contribute changes

## Troubleshooting

### "ModuleNotFoundError: No module named 'yaml'"

Install PyYAML:
```bash
pip install pyyaml
```

### "ANTHROPIC_API_KEY not set"

Create `.env` file in project root:
```bash
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

Or export environment variables:
```bash
export ANTHROPIC_API_KEY=your_key_here
```

### "Model not found" errors

The model may have been deprecated or renamed by the provider. Check:
1. Official provider documentation
2. Model YAML file's `api_identifier` field
3. Provider-specific model mappings in `pm_prompt_toolkit/providers/`

## Development

### Adding New Scripts

1. Create script in `scripts/` directory
2. Add shebang: `#!/usr/bin/env python3`
3. Make executable: `chmod +x scripts/your_script.py`
4. Add usage documentation to this README
5. Add to relevant CI workflows if needed

### Testing Scripts Locally

```bash
# Run with Python
python scripts/check_staleness.py

# Or make executable and run directly
chmod +x scripts/check_staleness.py
./scripts/check_staleness.py
```
