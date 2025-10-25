# Model Update Workflow

**Purpose**: Standard procedure for updating model versions when providers release new models

**Last Updated**: 2025-01-24

---

## When to Check for Updates

- **Monthly**: Review official provider documentation
- **After Provider Announcements**: Check immediately when new models announced
- **Before Major Releases**: Verify current models before publishing
- **Automated**: Set up weekly CI job to check model registry staleness

---

## Update Procedure

### Step 1: Check Official Documentation

Visit these URLs (links in `models/registry.py`):

1. **Anthropic Claude**:
   https://docs.claude.com/en/docs/about-claude/models

2. **OpenAI GPT**:
   https://platform.openai.com/docs/models

3. **Google Gemini**:
   https://ai.google.dev/gemini-api/docs/models/gemini

### Step 2: Update ModelRegistry

Edit `models/registry.py`:

```python
# 1. Update existing ModelSpec if changed
CLAUDE_SONNET_4_5 = ModelSpec(
    provider=Provider.ANTHROPIC,
    name="Claude Sonnet 4.5",
    api_identifier="claude-sonnet-4-5-20250929",  # ← Check if changed
    # ... update other fields as needed
    last_verified=date(2025, 1, 24),  # ← ALWAYS update this
)

# 2. Add new models if announced
CLAUDE_SONNET_5_0 = ModelSpec(...)  # Example new model

# 3. Move deprecated models to _DEPRECATED dict
_DEPRECATED = {
    "claude-sonnet-4-5-20250929": "Use CLAUDE_SONNET_5_0 instead",
}
```

### Step 3: Test Model Endpoints

Create `tests/verify_current_models.py`:

```python
import anthropic
import openai
import google.generativeai as genai
from models import ModelRegistry

def test_claude_models():
    client = anthropic.Anthropic()
    for model in ModelRegistry.get_by_provider(Provider.ANTHROPIC).values():
        try:
            response = client.messages.create(
                model=model.api_identifier,
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )
            print(f"✅ {model.name}: {model.api_identifier}")
        except Exception as e:
            print(f"❌ {model.name}: {e}")

# Similar for OpenAI and Gemini...
```

Run: `python tests/verify_current_models.py`

### Step 4: Update Documentation

1. Run migration script if model identifiers changed:
   ```bash
   # See MIGRATION_MAP.md for patterns
   ./scripts/migrate_models.sh  # Auto-update all files
   ```

2. Manually update:
   - `MODEL_OPTIMIZATION_GUIDE.md` - Comparison tables
   - `MIGRATION_MAP.md` - Add new mappings
   - Prompt files - Any hardcoded references

### Step 5: Create Verification Report

Document what changed:

```markdown
## Model Update: [Date]

**Provider**: [Anthropic/OpenAI/Google]

**Changes**:
- New model: [name] - [identifier]
- Deprecated: [old identifier] → [new identifier]
- Price change: [details]

**Verified**:
- [x] Endpoint test passed
- [x] ModelRegistry updated
- [x] Documentation updated
- [x] Migration map updated
```

### Step 6: Commit Changes

```bash
git add models/registry.py MIGRATION_MAP.md MODEL_OPTIMIZATION_GUIDE.md
git commit -m "Update models: [provider] [date]

- Add [new model name]
- Deprecate [old model name]
- Update pricing for [model name]

Verified from [official docs URL]"
```

---

## Automation (Recommended)

### Weekly Staleness Check

Add to CI/CD (`.github/workflows/check-models.yml`):

```yaml
name: Check Model Staleness

on:
  schedule:
    - cron: '0 0 * * 1'  # Every Monday

jobs:
  check-staleness:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check model verification dates
        run: python scripts/check_staleness.py
```

### Staleness Check Script

Create `scripts/check_staleness.py`:

```python
from datetime import date, timedelta
from models import ModelRegistry

STALE_DAYS = 90  # Warn if not verified in 90 days

for key, spec in ModelRegistry.get_all_current_models().items():
    days_old = (date.today() - spec.last_verified).days

    if days_old > STALE_DAYS:
        print(f"⚠️  {spec.name} not verified in {days_old} days")
        print(f"   Check: {spec.docs_url}")
        print()

# Exit 1 if any models stale
if any((date.today() - spec.last_verified).days > STALE_DAYS
       for spec in ModelRegistry.get_all_current_models().values()):
    exit(1)
```

---

## Common Scenarios

### Scenario 1: Provider Releases New Model

Example: Claude Sonnet 5.0 released

1. Add to `models/registry.py`:
   ```python
   CLAUDE_SONNET_5_0 = ModelSpec(...)
   ```

2. Update `MIGRATION_MAP.md`:
   ```markdown
   | claude-sonnet-4-5-* | claude-sonnet-5-0-* | New generation |
   ```

3. Don't immediately deprecate old model (allow transition period)

4. Update docs to recommend new model

5. After 3-6 months, move old to `_DEPRECATED`

### Scenario 2: Model Identifier Changes

Example: New date suffix on existing model

1. Update `api_identifier` in ModelSpec

2. Add old identifier to `_DEPRECATED`

3. Run migration script to update all files

4. Test all code examples

### Scenario 3: Pricing Changes

Example: Model cost increases/decreases

1. Update `input_price_per_1m` and `output_price_per_1m`

2. Update `last_verified` date

3. Update cost comparison tables in docs

4. Add note in model `notes` field about pricing change

5. Alert users if significant increase (>25%)

---

## Validation Checklist

Before committing model updates:

- [ ] Checked official provider documentation
- [ ] Updated all ModelSpec fields
- [ ] Updated `last_verified` dates
- [ ] Tested model endpoints (if possible)
- [ ] Updated deprecation list if needed
- [ ] Ran migration script for identifier changes
- [ ] Updated MODEL_OPTIMIZATION_GUIDE.md
- [ ] Updated MIGRATION_MAP.md
- [ ] Verified no hardcoded old identifiers remain
- [ ] Committed with descriptive message

---

## Warning Signs

**Check models immediately if you see**:

- Provider announcement of new model family
- "Model not found" errors in production
- Unexpected cost changes
- Performance degradation
- New capabilities announced (vision, function calling, etc.)

---

## Best Practices

1. **Verify, Don't Assume**: Always check official docs, never guess versions

2. **Update Registry First**: Single source of truth prevents inconsistencies

3. **Test Endpoints**: Confirm models work before updating docs

4. **Communicate Changes**: Note breaking changes clearly

5. **Maintain Deprecation Period**: Don't immediately remove old models

6. **Document Reasoning**: Explain why changes were made

7. **Automate Checks**: Use CI to catch stale verifications

---

## Contact & Support

**Issues**: Open GitHub issue with "model-update" label

**Questions**: Check model registry comments and official docs first

**Emergency**: If production breaks due to deprecated model, check `_DEPRECATED` dict for replacement

---

**Remember**: This library is a living document. Models evolve rapidly. Regular updates are critical to maintaining accuracy and usefulness.
