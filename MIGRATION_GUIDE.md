# Migration Guide: Old Registry → New AI Models System

This guide helps migrate code from the old `models/registry.py` to the new `ai_models/` system.

## Quick Start

### Old Way (Deprecated)
```python
from models.registry import ModelRegistry

# Get model
spec = ModelRegistry.CLAUDE_SONNET_4_5

# Use fields
api_id = spec.api_identifier
price = spec.input_price_per_1m
```

### New Way (Recommended)
```python
from ai_models import get_model

# Get model
model = get_model("claude-sonnet-4-5")

# Use fields
api_id = model.api_identifier
price = model.pricing.input_per_1m

# New capabilities!
if model.has_capability("vision"):
    process_image()
```

## Migration Mapping

### Import Changes

| Old Import | New Import |
|-----------|------------|
| `from models.registry import ModelRegistry` | `from ai_models import ModelRegistry` |
| `from models.registry import ModelSpec` | `from ai_models import Model` |
| `from models.registry import Provider` | Provider enum removed (use string) |

### Field Changes

| Old Field | New Field | Notes |
|-----------|-----------|-------|
| `spec.provider` (enum) | `model.provider` (string) | Now a string: "anthropic", "openai", "google" |
| `spec.api_identifier` | `model.api_identifier` | ✅ Same |
| `spec.context_window_input` | `model.metadata.context_window_input` | Moved to metadata |
| `spec.input_price_per_1m` | `model.pricing.input_per_1m` | Moved to pricing object |
| `spec.output_price_per_1m` | `model.pricing.output_per_1m` | Moved to pricing object |
| `spec.knowledge_cutoff` | `model.metadata.knowledge_cutoff` | Moved to metadata |
| `spec.last_verified` | `model.metadata.last_verified` | Moved to metadata |
| `spec.docs_url` | `model.metadata.docs_url` | Moved to metadata |
| `spec.recommended_for` (tuple) | `model.optimization.recommended_for` (list) | Moved + type change |
| N/A | `model.capabilities` (set) | ✨ NEW! |
| N/A | `model.optimization.best_practices` | ✨ NEW! |
| N/A | `model.optimization.cost_tier` | ✨ NEW! |

### Method Changes

| Old Method | New Method | Notes |
|-----------|------------|-------|
| `ModelRegistry.CLAUDE_SONNET_4_5` | `ModelRegistry.get("claude-sonnet-4-5")` | Attributes → methods |
| `ModelRegistry.get_all_current_models()` | `ModelRegistry.get_all()` | Simpler name |
| `ModelRegistry.get_spec(name)` | `ModelRegistry.get(model_id)` | Renamed parameter |
| `ModelRegistry.get_by_provider(Provider.ANTHROPIC)` | `ModelRegistry.get_by_provider("anthropic")` | String instead of enum |

## Step-by-Step Migration

### Step 1: Update Imports

**Before:**
```python
from models.registry import ModelRegistry, CLAUDE_SONNET_4_5
```

**After:**
```python
from ai_models import ModelRegistry, get_model
```

### Step 2: Change Model Access

**Before:**
```python
# Direct attribute access
spec = ModelRegistry.CLAUDE_SONNET_4_5
api_id = spec.api_identifier
```

**After:**
```python
# Method-based access
model = ModelRegistry.get("claude-sonnet-4-5")
api_id = model.api_identifier

# Or use convenience function
model = get_model("claude-sonnet-4-5")
```

### Step 3: Update Field Access

**Before:**
```python
spec = ModelRegistry.CLAUDE_HAIKU_4_5
price = spec.input_price_per_1m
context = spec.context_window_input
```

**After:**
```python
model = get_model("claude-haiku-4-5")
price = model.pricing.input_per_1m
context = model.metadata.context_window_input
```

### Step 4: Use New Capabilities

**New feature - capability checking:**
```python
model = get_model("claude-sonnet-4-5")

if model.has_capability("vision"):
    # Process images
    result = process_image_with_model(model)

if model.has_capability("function_calling"):
    # Use tools
    result = call_with_tools(model)

# Check multiple capabilities
if model.has_all_capabilities(["vision", "large_context"]):
    # Process large documents with images
    pass
```

### Step 5: Use Cost Calculation

**Before (manual calculation):**
```python
from models.registry import ModelRegistry

spec = ModelRegistry.CLAUDE_HAIKU_4_5
input_cost = (input_tokens / 1_000_000) * spec.input_price_per_1m
output_cost = (output_tokens / 1_000_000) * spec.output_price_per_1m
total = input_cost + output_cost
```

**After (built-in method):**
```python
from ai_models import get_model

model = get_model("claude-haiku-4-5")
cost = model.calculate_cost(
    input_tokens=input_tokens,
    output_tokens=output_tokens,
    cached_input_tokens=cached_tokens  # New! Caching support
)
```

## Common Migration Patterns

### Pattern 1: Provider Filtering

**Before:**
```python
from models.registry import ModelRegistry, Provider

models = ModelRegistry.get_by_provider(Provider.ANTHROPIC)
```

**After:**
```python
from ai_models import ModelRegistry

models = ModelRegistry.get_by_provider("anthropic")
```

### Pattern 2: Getting All Models

**Before:**
```python
all_models = ModelRegistry.get_all_current_models()
for name, spec in all_models.items():
    print(f"{name}: {spec.api_identifier}")
```

**After:**
```python
all_models = ModelRegistry.get_all()
for model_id, model in all_models.items():
    print(f"{model_id}: {model.api_identifier}")
```

### Pattern 3: Checking Model Properties

**Before:**
```python
spec = ModelRegistry.CLAUDE_SONNET_4_5
if "Production" in spec.recommended_for:
    use_for_production(spec)
```

**After:**
```python
model = get_model("claude-sonnet-4-5")
if any("Production" in rec for rec in model.optimization.recommended_for):
    use_for_production(model)

# Or use new cost tier feature
if model.optimization.cost_tier in ["mid-tier", "premium"]:
    use_for_production(model)
```

## New Features Available

### 1. Capability Checking
```python
from ai_models import ModelCapability, CapabilityValidator

# Check single capability
if CapabilityValidator.has_capability("gpt-4o", ModelCapability.VISION):
    print("Supports vision!")

# Get all models with a capability
vision_models = ModelRegistry.filter_by_capability(ModelCapability.VISION)

# Convenience functions
from ai_models import has_vision, has_function_calling, has_prompt_caching

if has_prompt_caching("claude-sonnet-4-5"):
    enable_caching()
```

### 2. Cost Tier Filtering
```python
# Get budget-friendly models
budget_models = ModelRegistry.filter_by_cost_tier("budget")
# Returns: Haiku, 4o-mini, Flash, Flash-Lite

# Get premium models
premium_models = ModelRegistry.filter_by_cost_tier("premium")
# Returns: Opus
```

### 3. Pricing Service
```python
from ai_models import PricingService

service = PricingService()

# Get pricing
pricing = service.get_pricing("claude-haiku-4-5")
print(f"Input: ${pricing.input_per_1m}/1M tokens")
print(f"Cache read: ${pricing.cache_read_per_1m}/1M tokens")

# Calculate cost directly
cost = service.calculate_cost(
    "claude-sonnet-4-5",
    input_tokens=10_000,
    output_tokens=2_000,
    cached_input_tokens=5_000
)
```

### 4. Optimization Guidance
```python
model = get_model("claude-haiku-4-5")

# Get recommendations
for rec in model.optimization.recommended_for:
    print(f"- {rec}")

# Get best practices
for practice in model.optimization.best_practices:
    print(f"✓ {practice}")

# Check tiers
print(f"Cost tier: {model.optimization.cost_tier}")
print(f"Speed tier: {model.optimization.speed_tier}")
```

## Backward Compatibility

The old `models/registry.py` will remain available during the transition period with deprecation warnings. However, it's recommended to migrate as soon as possible.

### Coexistence Strategy

Both systems can coexist:
```python
# Old system (will work but show warnings)
from models.registry import ModelRegistry as OldRegistry
old_spec = OldRegistry.CLAUDE_SONNET_4_5

# New system (recommended)
from ai_models import get_model
new_model = get_model("claude-sonnet-4-5")

# They reference the same underlying data
assert old_spec.api_identifier == new_model.api_identifier
```

## Testing Your Migration

Run these tests to verify your migration:

```bash
# Test old system still works
PYTHONPATH=. pytest tests/test_model_registry.py -v

# Test new system works
PYTHONPATH=. pytest tests/test_ai_models.py -v

# Test pricing consistency
PYTHONPATH=. pytest tests/test_pricing_consistency.py -v

# Run all fast tests
./scripts/run_tests.sh --fast
```

## Breaking Changes

### 1. Provider is now a string
**Before:** `Provider.ANTHROPIC` (enum)
**After:** `"anthropic"` (string)

### 2. Model access is now method-based
**Before:** `ModelRegistry.CLAUDE_SONNET_4_5` (attribute)
**After:** `ModelRegistry.get("claude-sonnet-4-5")` (method)

### 3. Fields are reorganized
**Before:** Flat structure (spec.input_price_per_1m)
**After:** Nested (model.pricing.input_per_1m)

### 4. recommended_for type changed
**Before:** tuple
**After:** list

## Troubleshooting

### Issue: Import error for ModelSpec
```python
# Old (error)
from models.registry import ModelSpec

# New (fixed)
from ai_models import Model
```

### Issue: Attribute error on model.input_price_per_1m
```python
# Old (error)
price = model.input_price_per_1m

# New (fixed)
price = model.pricing.input_per_1m
```

### Issue: Provider enum not found
```python
# Old (error)
from models.registry import Provider
models = ModelRegistry.get_by_provider(Provider.ANTHROPIC)

# New (fixed)
models = ModelRegistry.get_by_provider("anthropic")
```

## Support

If you encounter issues during migration:

1. Check this guide for common patterns
2. Look at `tests/test_ai_models.py` for examples
3. See `ai_models/` docstrings for API documentation
4. File an issue if you find bugs

## Timeline

- **Now - Q1 2026**: Both systems coexist
- **Q2 2026**: Old system shows deprecation warnings
- **Q3 2026**: Old system removed

Migrate early to benefit from new features!
