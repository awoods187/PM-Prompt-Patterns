# PM Prompt Toolkit - Python Package

**Last Updated:** 2025-11-01
**Status:** Production Ready
**Version:** 0.2.0

**Production-grade prompt engineering toolkit for AI-native product managers**

This Python package implements all the patterns and systems documented in this repository's guides, providing ready-to-use classifiers, model registry, and multi-cloud provider support for building production LLM systems.

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/awoods187/PM-Prompt-Patterns.git
cd PM-Prompt-Patterns

# Install the package
pip install -e .

# Or install with specific cloud providers
pip install -e ".[bedrock]"  # AWS Bedrock support
pip install -e ".[vertex]"   # Google Vertex AI support
pip install -e ".[all]"      # All cloud providers

# Or install with development dependencies
pip install -e ".[dev]"
```

### Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```bash
# Anthropic Claude (direct API) - REQUIRED for basic usage
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Optional: OpenAI models (NOT IMPLEMENTED YET - model definitions only)
# OPENAI_API_KEY=sk-your-key-here

# Optional: Google Gemini (NOT IMPLEMENTED YET - model definitions only)
# GOOGLE_API_KEY=your-key-here

# Optional: AWS Bedrock (requires boto3 and AWS credentials)
# ENABLE_BEDROCK=true
# AWS_ACCESS_KEY_ID=your-key
# AWS_SECRET_ACCESS_KEY=your-secret
# AWS_REGION=us-east-1

# Optional: Google Vertex AI (requires anthropic[vertex] and GCP credentials)
# ENABLE_VERTEX=true
# GCP_PROJECT_ID=your-project-id
# GCP_REGION=us-central1
```

3. Configure optional settings in `.env` (see `.env.example` for all options)

---

## 📚 Package Overview

### What's Included

The toolkit provides two main components:

1. **AI Models Registry** (`ai_models/`) - Centralized model definitions with pricing, capabilities, and metadata
2. **Provider System** (`pm_prompt_toolkit/providers/`) - Abstract provider interface with multiple implementations

---

## 🎯 Usage Examples

### 1. Using the AI Models Registry (Recommended)

The simplest and most powerful way to work with models:

```python
from ai_models import get_model, list_models, filter_by_capability

# List all available models
models = list_models()
print(f"Available models: {len(models)}")  # 8 models

# Get a specific model
model = get_model("claude-sonnet-4-5")
print(f"Model: {model.name}")
print(f"Provider: {model.provider}")
print(f"Context: {model.metadata.context_window_input:,} tokens")
print(f"Input cost: ${model.pricing.input_per_1m}/1M tokens")
print(f"Output cost: ${model.pricing.output_per_1m}/1M tokens")

# Filter by capability
vision_models = filter_by_capability("vision")
print(f"Models with vision: {[m.model_id for m in vision_models]}")

# Find budget-friendly models
budget_models = [m for m in models if m.pricing.cost_tier == "budget"]
print(f"Budget models: {[m.model_id for m in budget_models]}")

# Calculate costs
from ai_models import calculate_cost
cost = calculate_cost(
    model_id="claude-sonnet-4-5",
    input_tokens=1000,
    output_tokens=500
)
print(f"Cost for request: ${cost:.4f}")
```

**Available models:**
- `claude-haiku-4-5` (budget, fast)
- `claude-sonnet-4-5` (balanced, recommended)
- `claude-opus-4-1` (premium, highest quality)
- `gpt-4o` (provider not implemented yet)
- `gpt-4o-mini` (provider not implemented yet)
- `gemini-2-5-flash` (provider not implemented yet)
- `gemini-2.5-pro` (provider not implemented yet)

### 2. Using Providers for Classification

For classification tasks using implemented providers:

```python
from pm_prompt_toolkit.providers import get_provider

# Use Claude (Anthropic direct API)
provider = get_provider("claude:claude-sonnet-4-5")
result = provider.classify("We need SSO integration before Q4 rollout")

print(f"Category: {result.category}")
print(f"Confidence: {result.confidence:.2f}")
print(f"Cost: ${result.cost:.4f}")

# Use AWS Bedrock (if configured)
bedrock_provider = get_provider("bedrock:claude-sonnet-4-5")
result = bedrock_provider.classify("Dashboard is slow")

# Use Google Vertex AI (if configured)
vertex_provider = get_provider("vertex:claude-sonnet-4-5")
result = vertex_provider.classify("Can we get a quote?")
```

### 3. Provider Auto-Selection

Let the factory choose the best available provider:

```python
from pm_prompt_toolkit.providers import get_provider

# Auto-selects based on .env configuration
# Priority: Vertex (if enabled) > Bedrock (if enabled) > Anthropic direct
provider = get_provider("claude-sonnet")

result = provider.classify("Dashboard won't load, getting 500 errors")
print(f"Provider used: {provider.__class__.__name__}")
print(f"Category: {result.category}")
```

### 4. Cost Optimization with Model Registry

```python
from ai_models import get_model, calculate_cost

# Compare costs across models
models_to_compare = ["claude-haiku-4-5", "claude-sonnet-4-5", "claude-opus-4-1"]

print("Cost comparison for 1M input + 100K output tokens:")
for model_id in models_to_compare:
    cost = calculate_cost(model_id, input_tokens=1_000_000, output_tokens=100_000)
    model = get_model(model_id)
    print(f"  {model.name}: ${cost:.2f}")

# Output:
# Claude Haiku 4.0: $1.25
# Claude Sonnet 4.5: $4.00
# Claude Opus 4.0: $18.00
```

### 5. Batch Processing with Metrics

```python
from pm_prompt_toolkit.providers import get_provider

provider = get_provider("claude:claude-haiku-4-5")  # Use cheapest model

signals = [
    "We need SSO integration",
    "Dashboard is broken",
    "Can we get quote for 100 more seats?",
    "Product is too slow",
    "Love the new feature!",
]

results = []
for signal in signals:
    result = provider.classify(signal)
    results.append(result)
    print(f"{signal[:30]:30} -> {result.category:20} ${result.cost:.4f}")

# Calculate totals
total_cost = sum(r.cost for r in results)
avg_latency = sum(r.latency_ms for r in results) / len(results)

print(f"\nTotal cost: ${total_cost:.4f}")
print(f"Average latency: {avg_latency:.0f}ms")
```

---

## 📊 Package Structure

```
pm_prompt_toolkit/
├── __init__.py                  # Main package exports
├── config/                      # Configuration management
│   ├── __init__.py
│   └── settings.py             # Pydantic settings with env vars
├── providers/                   # LLM provider implementations
│   ├── __init__.py
│   ├── base.py                 # ✅ Abstract base classes
│   ├── claude.py               # ✅ Anthropic Claude (IMPLEMENTED)
│   ├── bedrock.py              # ✅ AWS Bedrock (IMPLEMENTED)
│   ├── vertex.py               # ✅ Google Vertex AI (IMPLEMENTED)
│   ├── mock.py                 # ✅ Mock provider for testing (IMPLEMENTED)
│   ├── openai.py               # 🚧 OpenAI GPT (stub - raises NotImplementedError)
│   ├── gemini.py               # 🚧 Google Gemini (stub - raises NotImplementedError)
│   └── factory.py              # ✅ Provider factory with routing
├── optimizers/                  # (Empty - future feature)
│   └── __init__.py
└── utils/                       # (Empty - future feature)
    └── __init__.py

ai_models/
├── __init__.py                  # ✅ Public API (get_model, list_models, etc.)
├── capabilities.py              # ✅ Capability validation and filtering
├── pricing.py                   # ✅ Cost calculations
├── registry.py                  # ✅ Central model registry
└── definitions/                 # ✅ YAML model definitions
    ├── anthropic/              # Claude models (3 models)
    ├── google/                 # Gemini models (2 models - definitions only)
    └── openai/                 # GPT models (3 models - definitions only)
```

---

## ✅ Implemented Features

### AI Models Registry
- ✅ **8 model definitions** across 3 providers (Anthropic, OpenAI, Google)
- ✅ **Complete metadata** (context windows, pricing, capabilities, release dates)
- ✅ **Cost calculations** with caching support
- ✅ **Capability filtering** (vision, function calling, prompt caching, etc.)
- ✅ **Type-safe API** with full type hints

### Provider System
- ✅ **Claude provider** (Haiku, Sonnet, Opus via Anthropic direct API)
- ✅ **Bedrock provider** (Claude models via AWS Bedrock)
- ✅ **Vertex provider** (Claude models via Google Vertex AI)
- ✅ **Mock provider** (for testing without API calls)
- ✅ **Provider factory** with automatic routing
- ✅ **Configuration management** with Pydantic Settings
- ✅ **Security best practices** (env vars, validation, no logging of secrets)

### Testing & Quality
- ✅ **507 passing tests** (80%+ code coverage)
- ✅ **Type checking** with mypy
- ✅ **Linting** with Ruff and Black
- ✅ **Security scanning** with Bandit
- ✅ **CI/CD** with GitHub Actions

---

## 🚧 Not Yet Implemented

### Provider Limitations

**OpenAI Provider:**
- ✅ Model definitions exist in registry (gpt-4o, gpt-4o-mini, gpt-3.5-turbo)
- ❌ Provider implementation raises `NotImplementedError`
- 📝 Planned features: GPT-4o, JSON mode, function calling
- 🤝 Contributions welcome! See [CONTRIBUTING.md](../.github/CONTRIBUTING.md)

**Google Gemini Provider:**
- ✅ Model definitions exist in registry (gemini-2-5-flash, gemini-2.5-pro)
- ❌ Provider implementation raises `NotImplementedError`
- 📝 Planned features: Gemini Pro, Gemini Flash, 1M+ token context
- 🤝 Contributions welcome! See [CONTRIBUTING.md](../.github/CONTRIBUTING.md)

**Workaround:**
You can still use OpenAI and Google models:
1. Access model definitions via `ai_models` registry
2. Use the pricing/capability data for planning
3. Call the APIs directly (not through this toolkit)

---

## 🔒 Security Best Practices

### ✅ What We Do

- ✅ **Never hardcode credentials** - All API keys from environment variables
- ✅ **Comprehensive validation** - Settings validate API keys before use
- ✅ **Type safety** - Full type hints throughout codebase (mypy checked)
- ✅ **Immutable settings** - Configuration cannot be changed after init
- ✅ **Secure logging** - API keys never logged or exposed
- ✅ **.gitignore configured** - .env file excluded from version control
- ✅ **Security scanning** - Bandit checks in CI/CD
- ✅ **Input validation** - XML escaping for Claude prompts

### 🛡️ Security Checklist

- [ ] Copy `.env.example` to `.env` (never commit `.env`)
- [ ] Set real API keys in `.env`
- [ ] Never log or print API keys
- [ ] Rotate keys if accidentally exposed
- [ ] Use different keys for dev/staging/production
- [ ] Consider secrets manager in production (AWS Secrets Manager, HashiCorp Vault, etc.)

### Example: Validating Configuration

```python
from pm_prompt_toolkit.config import get_settings

settings = get_settings()

# Validate Anthropic configuration
try:
    settings.validate_provider_config('anthropic')
    print("✅ Anthropic configured correctly")
except ValueError as e:
    print(f"❌ Configuration error: {e}")
    # Will print: "ANTHROPIC_API_KEY not found in environment.
    #              Please set it in your .env file."

# Validate Bedrock configuration (if enabled)
if settings.enable_bedrock:
    settings.validate_bedrock_config()
    print("✅ AWS Bedrock configured correctly")

# Validate Vertex AI configuration (if enabled)
if settings.enable_vertex:
    settings.validate_vertex_config()
    print("✅ Google Vertex AI configured correctly")
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=pm_prompt_toolkit --cov=ai_models --cov-report=html

# Run specific test file
pytest tests/test_ai_models.py -v

# Run tests for a specific module
pytest tests/test_factory_routing.py -v

# Run with detailed output
pytest -vv --tb=short

# Run only fast tests (skip API endpoint tests)
pytest -m "not endpoint"

# View coverage report
open htmlcov/index.html
```

**Current test status:** ✅ 507 passing, 19 skipped (API tests)

---

## 🎯 Design Principles

### 1. Security First

All credentials from environment variables. Comprehensive validation. Never expose secrets. Security scanning in CI.

### 2. Type Safety

Full type hints using Python 3.9+ features. Validated with mypy in strict mode.

### 3. Production Ready

Real metrics tracking. Error handling. Logging. Documentation. 80%+ test coverage.

### 4. Cost Conscious

Model registry with accurate pricing. Cost calculations. Provider comparison. Budget-friendly defaults.

### 5. Developer Experience

Clear error messages. Comprehensive docs. Consistent API. Type hints for IDE support. Multiple cloud options.

---

## 📖 Examples

See the repository for complete working examples:

### Available Examples

- **[examples/basic_example.py](../examples/basic_example.py)** - Simple signal classification with metrics
- **[examples/epic-categorization/](../examples/epic-categorization/)** - Complete production system with 95% accuracy

### Example Output

```bash
$ python examples/basic_example.py

======================================================================
PM Prompt Toolkit - Basic Example
======================================================================

📦 Initializing SignalClassifier...
   Model: claude-sonnet-4-5
   Keyword filter: True

🔍 Classifying signals...

1. Signal: "We need SSO integration before Q4 rollout"
   → Category: feature_request
   → Confidence: 0.95
   → Method: llm
   → Cost: $0.0008
   → Latency: 342ms

...

📊 Metrics Summary
Total requests: 5
Total cost: $0.0024
Average cost: $0.0005
Average latency: 156ms
💡 Cost Savings: 2/5 signals caught by keyword filter (FREE)
```

---

## 🐛 Troubleshooting

### "API key not configured"

```
ValueError: ANTHROPIC_API_KEY not found in environment.
Please set it in your .env file.
```

**Solution:**
```bash
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY=your-real-key-here
```

### "anthropic package is required"

```
ImportError: anthropic package is required.
Install with: pip install anthropic
```

**Solution:**
```bash
pip install -e .  # Installs all dependencies from pyproject.toml
```

### "Provider not implemented"

```
NotImplementedError: OpenAI provider not yet implemented.
Use ClaudeProvider instead.
```

**Solution:** Use an implemented provider:
```python
# ✅ Use Claude (fully implemented)
from pm_prompt_toolkit.providers import get_provider
provider = get_provider("claude:claude-sonnet-4-5")

# ✅ Use Bedrock (fully implemented, requires AWS config)
provider = get_provider("bedrock:claude-sonnet-4-5")

# ✅ Use Vertex AI (fully implemented, requires GCP config)
provider = get_provider("vertex:claude-sonnet-4-5")

# ❌ OpenAI not implemented yet
# provider = get_provider("openai:gpt-4o")  # Raises NotImplementedError
```

### "Model not found"

```
ValueError: Model 'xyz' not found in registry
```

**Solution:** List available models:
```python
from ai_models import list_models

models = list_models()
for model in models:
    print(f"  {model.model_id} ({model.provider})")
```

---

## 🤝 Contributing

We welcome contributions! Especially for:

- 🎯 **High Priority:** Implementing OpenAI and Gemini providers
- 📊 **Medium Priority:** Adding cost optimization utilities
- 🧪 **Medium Priority:** Expanding test coverage
- 📚 **Low Priority:** Adding more examples and documentation

See [CONTRIBUTING.md](../.github/CONTRIBUTING.md) for guidelines.

---

## 📝 License

MIT License - see [LICENSE](../LICENSE) for details.

---

## 🔗 Related Documentation

### Package Documentation
- [Getting Started Guide](./getting_started.md) - Beginner's guide
- [Project Structure](./project_structure.md) - Repository organization
- [API Documentation](./api/) - (Coming soon)

### Guides & Best Practices
- [Prompt Design Principles](./prompt_design_principles.md) - Core patterns
- [Advanced Techniques](./advanced_techniques.md) - Production patterns
- [Cost Optimization](./cost_optimization.md) - ROI strategies
- [Quality Evaluation](./quality_evaluation.md) - Testing methodologies

### System Documentation
- [Model Update System](./model_update_system.md) - Automated model updates
- [Security Policy](../.github/SECURITY.md) - Vulnerability reporting

### Project Information
- [Main README](../README.md) - Repository overview
- [Changelog](../CHANGELOG.md) - Version history
- [Roadmap](../.github/ROADMAP.md) - Planned features

---

## 📧 Support

- **Issues:** [GitHub Issues](https://github.com/awoods187/PM-Prompt-Patterns/issues)
- **Discussions:** [GitHub Discussions](https://github.com/awoods187/PM-Prompt-Patterns/discussions)
- **Security:** [Security Policy](../.github/SECURITY.md)

---

**Built with ❤️ for AI-native product managers**

**Last Updated:** 2025-11-01
**Version:** 0.2.0
**Status:** Production Ready (with provider limitations noted above)
