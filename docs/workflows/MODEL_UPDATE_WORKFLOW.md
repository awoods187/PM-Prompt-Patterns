# Model Update Workflow

**Purpose**: Standard procedure for updating model versions when providers release new models

**Last Updated**: 2025-10-29

---

## When to Check for Updates

- **Monthly**: Review official provider documentation
- **After Provider Announcements**: Check immediately when new models announced
- **Before Major Releases**: Verify current models before publishing
- **Automated**: Set up weekly CI job to check model registry staleness

---

## Update Procedure

### Step 1: Check Official Documentation

Visit these URLs (links in `ai_models/registry.py`):

1. **Anthropic Claude**:
   https://docs.claude.com/en/docs/about-claude/models

2. **OpenAI GPT**:
   https://platform.openai.com/docs/models

3. **Google Gemini**:
   https://ai.google.dev/gemini-api/docs/models/gemini

### Step 2: Update Model YAML Definitions

Edit files in `ai_models/definitions/{provider}/`:

```yaml
# Example: ai_models/definitions/anthropic/claude-opus-4-1.yaml

schema_version: "1.0.0"
model_id: "claude-opus-4-1"
provider: "anthropic"
name: "Claude Opus 4.1"
api_identifier: "claude-opus-4-1-20250805"  # ← Update if changed

metadata:
  context_window_input: 200000
  context_window_output: null
  knowledge_cutoff: "December 2024"  # ← Update if changed
  release_date: "2025-08-05"  # ← Update if changed
  last_verified: "2025-01-29"  # ← ALWAYS update this to today
  docs_url: "https://docs.claude.com/en/docs/about-claude/models"

pricing:
  input_per_1m: 15.00  # ← Update if changed
  output_per_1m: 75.00  # ← Update if changed
  cache_write_per_1m: 18.75
  cache_read_per_1m: 1.50

# ... update other fields as needed
```

### Step 3: Add New Models

If a provider releases a new model family:

1. Create new YAML file: `ai_models/definitions/{provider}/{model-id}.yaml`
2. Follow existing structure (copy similar model as template)
3. Update provider factory routing in `pm_prompt_toolkit/providers/factory.py`
4. Add to model lists (e.g., `claude_models`, `openai_models`, `gemini_models`)

### Step 4: Test Model Endpoints

Create and run verification script:

```bash
python scripts/verify_current_models.py
```

This will attempt to call each model's API to confirm it's accessible.

### Step 5: Update Documentation

Files to check and update:

1. **README.md** - Model comparison table
2. **MODEL_OPTIMIZATION_GUIDE.md** - Detailed model guide
3. **Prompt files** - Any hardcoded model references
4. **Provider documentation** - Bedrock/Vertex model mappings

### Step 6: Create Verification Report

Document what changed in commit message:

```markdown
## Model Update: 2025-01-29

**Provider**: Anthropic

**Changes**:
- Updated Claude Opus 4.1 API identifier: claude-opus-4-1-20250514 → claude-opus-4-1-20250805
- Verified pricing (no changes)
- Updated last_verified dates for all Anthropic models

**Verified**:
- [x] Endpoint test passed
- [x] Model definitions updated
- [x] Documentation updated
- [x] Tests passing
```

### Step 7: Commit Changes

```bash
git add ai_models/definitions/ README.md MODEL_OPTIMIZATION_GUIDE.md
git commit -m "chore: Update models - Anthropic (2025-01-29)

- Update Claude Opus 4.1 to latest API identifier (20250805)
- Verify all Anthropic model definitions
- Update last_verified dates

Verified from https://docs.claude.com/en/docs/about-claude/models"
```

---

## Automation (Recommended)

### Weekly Staleness Check

Add to CI/CD (`.github/workflows/check-model-staleness.yml`):

```yaml
name: Check Model Staleness

on:
  schedule:
    - cron: '0 0 * * 1'  # Every Monday at midnight UTC
  workflow_dispatch:  # Allow manual trigger

jobs:
  check-staleness:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pyyaml

      - name: Check model verification dates
        run: python scripts/check_staleness.py

      - name: Create issue if stale models found
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Model definitions need verification',
              body: 'Some models have not been verified in 90+ days. Run `python scripts/check_staleness.py` for details.',
              labels: ['maintenance', 'models']
            })
```

### Staleness Check Script

Located at `scripts/check_staleness.py` - checks if models haven't been verified in 90+ days.

---

## Common Scenarios

### Scenario 1: Provider Releases New Model Family

**Example**: Claude Opus 5.0 released

1. Create `ai_models/definitions/anthropic/claude-opus-5-0.yaml`
2. Add to `claude_models` list in `pm_prompt_toolkit/providers/factory.py`
3. Update Bedrock/Vertex mappings if supported on those platforms
4. Update README comparison table
5. Don't immediately deprecate Opus 4.1 (allow transition period)
6. After 6 months, consider marking old version as legacy

### Scenario 2: Model Identifier Changes

**Example**: New date suffix on existing model (like we found for Opus 4.1)

1. Update `api_identifier` in YAML file
2. Update `last_verified` date
3. Test endpoint to confirm old identifier still works or if breaking change
4. If breaking: add migration note to CHANGELOG.md
5. If compatible: update silently

### Scenario 3: Pricing Changes

**Example**: Model cost increases/decreases

1. Update `input_per_1m` and `output_per_1m` in YAML
2. Update `last_verified` date
3. Add note in `notes` field about pricing change with date
4. Update cost comparison tables in README and optimization guide
5. If >25% increase: add CHANGELOG entry and consider user notification

### Scenario 4: New Capability Added

**Example**: Model gains vision or function calling support

1. Add capability to `capabilities` list in YAML
2. Update `notes` field to highlight new capability
3. Update optimization guidance if relevant
4. Test new capability with verification script
5. Update examples/documentation showcasing new capability

---

## Validation Checklist

Before committing model updates:

- [ ] Checked official provider documentation
- [ ] Updated all relevant YAML fields
- [ ] Updated `last_verified` dates to today
- [ ] Tested model endpoints (if API keys available)
- [ ] Updated factory routing if new models added
- [ ] Updated README.md model table
- [ ] Updated MODEL_OPTIMIZATION_GUIDE.md if needed
- [ ] Verified no hardcoded old identifiers remain
- [ ] All tests passing (`pytest tests/`)
- [ ] Committed with descriptive message

---

## Warning Signs

**Check models immediately if you see**:

- Provider announcement of new model family
- "Model not found" errors in production or tests
- Unexpected cost changes in billing
- Performance degradation reports
- New capabilities announced (vision, function calling, extended context, etc.)
- Provider deprecation notices

---

## Best Practices

1. **Verify, Don't Assume**: Always check official docs, never guess versions

2. **YAML is Source of Truth**: All model info lives in YAML files, registry loads from them

3. **Test Endpoints When Possible**: Confirm models work before updating docs

4. **Communicate Changes**: Breaking changes need CHANGELOG entries and clear migration guidance

5. **Maintain Backwards Compatibility**: Don't immediately remove old model support

6. **Document Reasoning**: Explain why changes were made in commit messages

7. **Automate Checks**: Use CI to catch stale verifications before they cause issues

8. **Update Last Verified**: Even if no changes, update `last_verified` to show it was checked

---

## File Structure

```
PM-Prompt-Patterns/
├── ai_models/
│   ├── registry.py              # Loads YAML definitions
│   └── definitions/             # Model definitions
│       ├── anthropic/
│       │   ├── claude-sonnet-4-5.yaml
│       │   ├── claude-haiku-4-5.yaml
│       │   └── claude-opus-4-1.yaml
│       ├── openai/
│       │   ├── gpt-4o.yaml
│       │   └── gpt-4o-mini.yaml
│       └── google/
│           ├── gemini-2-5-pro.yaml
│           ├── gemini-2-5-flash.yaml
│           └── gemini-2-5-flash-lite.yaml
├── scripts/
│   ├── check_staleness.py       # Check for stale models
│   └── verify_current_models.py # Test model endpoints
├── docs/workflows/
│   └── MODEL_UPDATE_WORKFLOW.md # This document
└── .github/workflows/
    └── check-model-staleness.yml # Weekly automation
```

---

## Contact & Support

**Issues**: Open GitHub issue with "model-update" or "maintenance" label

**Questions**: Check model YAML comments and official provider docs first

**Emergency**: If production breaks due to model changes, check:
1. Provider status pages
2. Model YAML `api_identifier` field
3. Provider factory routing in `pm_prompt_toolkit/providers/factory.py`

---

## Appendix: Provider-Specific Notes

### Anthropic Claude

- Models use date-based identifiers (e.g., `claude-sonnet-4-5-20250929`)
- New identifiers released periodically even for same model version
- Old identifiers typically supported for 6 months
- Check: https://docs.claude.com/en/docs/about-claude/models

### OpenAI GPT

- Models typically use simple identifiers (e.g., `gpt-4o`, `gpt-4o-mini`)
- Sometimes add date suffixes for versioning
- Deprecation notices given 3-6 months in advance
- Check: https://platform.openai.com/docs/models

### Google Gemini

- Models use version-based identifiers (e.g., `gemini-2.5-pro`)
- Experimental versions available with different identifiers
- Production vs experimental clearly marked
- Check: https://ai.google.dev/gemini-api/docs/models/gemini

---

**Remember**: This library serves production systems. Regular model updates are critical to maintaining accuracy, performance, and cost-effectiveness.
