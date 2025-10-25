# Model Definition Schema

This document defines the YAML schema for AI model specifications.

## Schema Version

Current version: `1.0.0`

## Required Fields

```yaml
schema_version: "1.0.0"
model_id: string          # Unique identifier (e.g., "claude-sonnet-4-5")
provider: string          # Provider name: "anthropic" | "openai" | "google"
name: string              # Human-readable name
api_identifier: string    # Exact string used in API calls

metadata:
  context_window_input: integer      # Max input tokens
  context_window_output: integer     # Max output tokens (null if same as input)
  knowledge_cutoff: string           # Training data cutoff (e.g., "January 2025")
  release_date: string              # ISO date (YYYY-MM-DD)
  last_verified: string             # ISO date when spec was last verified
  docs_url: string                  # Official documentation URL

capabilities:
  - text_input              # Basic text processing
  - text_output             # Text generation
  - function_calling        # Tool/function calling support
  - vision                  # Image understanding
  - large_context          # Context >32k tokens
  - prompt_caching         # Prompt caching support
  - streaming              # Streaming responses
  - json_mode              # Structured JSON output
  - code_execution         # Code interpreter
  - search                 # Web search capability

pricing:
  input_per_1m: float      # USD per 1M input tokens
  output_per_1m: float     # USD per 1M output tokens
  cache_write_per_1m: float    # USD per 1M tokens for cache writes (optional)
  cache_read_per_1m: float     # USD per 1M cached tokens read (optional)

optimization:
  recommended_for:         # List of use cases
    - string
  best_practices:          # List of optimization tips
    - string
  cost_tier: string        # "budget" | "mid-tier" | "premium"
  speed_tier: string       # "fast" | "balanced" | "thorough"

notes: string             # Additional information (optional)
```

## Example: Claude Sonnet 4.5

```yaml
schema_version: "1.0.0"
model_id: "claude-sonnet-4-5"
provider: "anthropic"
name: "Claude Sonnet 4.5"
api_identifier: "claude-sonnet-4-5-20250929"

metadata:
  context_window_input: 200000
  context_window_output: null  # Same as input
  knowledge_cutoff: "January 2025"
  release_date: "2025-09-29"
  last_verified: "2025-10-25"
  docs_url: "https://docs.claude.com/en/docs/about-claude/models"

capabilities:
  - text_input
  - text_output
  - function_calling
  - vision
  - large_context
  - prompt_caching
  - streaming
  - json_mode

pricing:
  input_per_1m: 3.00
  output_per_1m: 15.00
  cache_write_per_1m: 3.75
  cache_read_per_1m: 0.30

optimization:
  recommended_for:
    - "Production workhorse applications"
    - "Complex analysis and reasoning"
    - "Long-form content generation"
    - "Code generation and review"
    - "Multi-step instructions"
  best_practices:
    - "Use XML tags for structured prompts"
    - "Enable prompt caching for repeated system prompts"
    - "Leverage 200k context for comprehensive analysis"
    - "Use function calling for structured outputs"
  cost_tier: "mid-tier"
  speed_tier: "balanced"

notes: "RECOMMENDED for most use cases. Training data through July 2025. Extended context window (1M tokens) in beta."
```

## Validation Rules

1. **model_id**: Must be lowercase, use hyphens (not underscores), unique across all providers
2. **provider**: Must be one of: anthropic, openai, google
3. **api_identifier**: Exact match to what provider's API expects
4. **context_window_input**: Must be positive integer, >= 1024
5. **pricing**: All values must be non-negative floats
6. **capabilities**: Must be valid capability identifiers (see enum)
7. **last_verified**: Must be ISO date format (YYYY-MM-DD)
8. **cost_tier**: Must be one of: budget, mid-tier, premium
9. **speed_tier**: Must be one of: fast, balanced, thorough

## Migration from Current Registry

Current `models/registry.py` ModelSpec fields map to YAML as:

| ModelSpec Field | YAML Path |
|----------------|-----------|
| provider | `provider` |
| name | `name` |
| api_identifier | `api_identifier` |
| context_window_input | `metadata.context_window_input` |
| context_window_output | `metadata.context_window_output` |
| input_price_per_1m | `pricing.input_per_1m` |
| output_price_per_1m | `pricing.output_per_1m` |
| knowledge_cutoff | `metadata.knowledge_cutoff` |
| last_verified | `metadata.last_verified` |
| docs_url | `metadata.docs_url` |
| notes | `notes` |
| recommended_for | `optimization.recommended_for` |

New fields added:
- `capabilities` (enum-based feature flags)
- `pricing.cache_*` (prompt caching costs)
- `optimization.best_practices` (extracted from guides)
- `optimization.cost_tier` (categorization)
- `optimization.speed_tier` (categorization)
- `metadata.release_date` (tracking)

## Directory Structure

```
ai_models/
├── definitions/
│   ├── schema.md              # This file
│   ├── anthropic/
│   │   ├── claude-sonnet-4-5.yaml
│   │   ├── claude-haiku-4-5.yaml
│   │   └── claude-opus-4-1.yaml
│   ├── openai/
│   │   ├── gpt-4o.yaml
│   │   └── gpt-4o-mini.yaml
│   └── google/
│       ├── gemini-2-5-pro.yaml
│       ├── gemini-2-5-flash.yaml
│       └── gemini-2-5-flash-lite.yaml
├── registry.py               # Auto-loads YAML files
├── pricing.py                # PricingService
├── capabilities.py           # ModelCapability enum
└── providers.py              # ProviderRegistry
```

## Usage Example

```python
from ai_models import ModelRegistry

# Get model by ID
model = ModelRegistry.get("claude-sonnet-4-5")

# Check capabilities
if model.has_capability("vision"):
    # Process image

# Get pricing
pricing = model.get_pricing()
cost = pricing.calculate(input_tokens=1000, output_tokens=500)

# Get recommendations
if model.optimization.cost_tier == "budget":
    # Use for high-volume tasks
```

## Backward Compatibility

During migration, both systems will coexist:
- `models/registry.py` (old) - Frozen, deprecated
- `ai_models/` (new) - Active development

Migration helpers will redirect old imports to new system with deprecation warnings.
