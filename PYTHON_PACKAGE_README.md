# PM Prompt Toolkit - Python Package

**Production-grade prompt engineering toolkit for AI-native product managers**

This Python package implements all the patterns and systems documented in this repository's guides, providing ready-to-use classifiers, optimizers, and utilities for building production LLM systems.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/awoods187/PM-Prompt-Patterns.git
cd PM-Prompt-Patterns

# Install the package
pip install -e .

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
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-key-here  # Optional, not yet implemented
GOOGLE_API_KEY=your-key-here      # Optional, not yet implemented
```

3. Configure optional settings in `.env` (see `.env.example` for all options)

### Basic Usage

```python
from pm_prompt_toolkit import SignalClassifier

# Initialize classifier (uses default settings from .env)
classifier = SignalClassifier()

# Classify a customer signal
result = classifier.classify("We need SSO integration ASAP")

# View results
print(f"Category: {result.category}")
print(f"Confidence: {result.confidence:.2f}")
print(f"Cost: ${result.cost:.4f}")
print(f"Method: {result.method}")

# Output:
# Category: feature_request
# Confidence: 0.96
# Cost: $0.0008
# Method: claude-sonnet
```

### With Keyword Filtering (70% Cost Savings)

```python
# Keyword filtering is enabled by default
classifier = SignalClassifier(enable_keyword_filter=True)

# This will use free keyword matching
result = classifier.classify("Dashboard is broken and won't load")

print(f"Method: {result.method}")  # "keyword" (FREE)
print(f"Cost: ${result.cost}")     # $0.00

# This will escalate to LLM (no keyword match)
result = classifier.classify("Just checking if there are alternatives...")

print(f"Method: {result.method}")  # "claude-sonnet"
print(f"Cost: ${result.cost:.4f}") # $0.0008
```

### Using Different Models

```python
# Use faster, cheaper model
classifier = SignalClassifier(model="claude-haiku")

# Use highest quality model
classifier = SignalClassifier(model="claude-opus")

# Or specify at provider level
from pm_prompt_toolkit.providers import ClaudeProvider

provider = ClaudeProvider(model="claude-sonnet", enable_caching=True)
result = provider.classify("We need SSO integration")
```

### Metrics and Cost Tracking

```python
classifier = SignalClassifier()

# Classify multiple signals
signals = [
    "We need SSO integration",
    "Dashboard is broken",
    "Can we get quote for 100 more seats?",
]

for signal in signals:
    result = classifier.classify(signal)
    print(f"{result.category}: ${result.cost:.4f}")

# Get aggregate metrics
metrics = classifier.get_metrics()
print(f"Total requests: {metrics['total_requests']}")
print(f"Average cost: ${metrics['average_cost']:.4f}")
print(f"Cache hit rate: {metrics['cache_hit_rate']:.1%}")
```

## 📚 Package Structure

```
pm_prompt_toolkit/
├── __init__.py                  # Main package exports
├── config/                      # Configuration management
│   ├── __init__.py
│   └── settings.py             # Pydantic settings with env vars
├── providers/                   # LLM provider implementations
│   ├── __init__.py
│   ├── base.py                 # Abstract base classes
│   ├── claude.py               # ✅ Anthropic Claude (implemented)
│   ├── openai.py               # 🚧 OpenAI GPT (coming soon)
│   ├── gemini.py               # 🚧 Google Gemini (coming soon)
│   └── factory.py              # Provider factory
├── classifiers/                 # Pre-built classifiers
│   ├── __init__.py
│   └── signal_classifier.py    # ✅ Customer signal classifier
├── optimizers/                  # 🚧 Cost optimization strategies
│   └── __init__.py
└── utils/                       # 🚧 Utility functions
    └── __init__.py
```

## 🔒 Security Best Practices

### ✅ What We Do

- ✅ **Never hardcode credentials** - All API keys from environment variables
- ✅ **Comprehensive validation** - Settings validate API keys before use
- ✅ **Type safety** - Full type hints throughout codebase
- ✅ **Immutable settings** - Configuration cannot be changed after init
- ✅ **Secure logging** - API keys never logged or exposed
- ✅ **.gitignore configured** - .env file excluded from version control

### 🛡️ Security Checklist

- [ ] Copy `.env.example` to `.env` (never commit `.env`)
- [ ] Set real API keys in `.env`
- [ ] Never log or print API keys
- [ ] Rotate keys if accidentally exposed
- [ ] Use different keys for dev/staging/production
- [ ] Consider secrets manager in production (AWS Secrets Manager, etc.)

### Example: Validating Configuration

```python
from pm_prompt_toolkit.config import get_settings

settings = get_settings()

# This validates that the key is configured
try:
    settings.validate_provider_config('anthropic')
    print("✅ Anthropic configured correctly")
except ValueError as e:
    print(f"❌ Configuration error: {e}")
    # Will print: "API key not configured for anthropic.
    #              Please set ANTHROPIC_API_KEY in your .env file."
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=pm_prompt_toolkit --cov-report=html

# Run specific test
pytest tests/test_signal_classifier.py -v

# Run with different log level
pytest --log-cli-level=DEBUG
```

## 📊 Current Implementation Status

### ✅ Implemented

- ✅ **Configuration management** with Pydantic Settings
- ✅ **Base provider classes** with full type hints and documentation
- ✅ **Claude provider** (Haiku, Sonnet, Opus)
- ✅ **Signal classifier** with hybrid keyword + LLM strategy
- ✅ **Metrics tracking** (cost, latency, cache hit rate)
- ✅ **Security best practices** (env vars, validation, logging)

### 🚧 In Progress (See TODO.md)

- 🚧 OpenAI GPT provider (GPT-3.5, GPT-4)
- 🚧 Google Gemini provider (Pro, Flash)
- 🚧 Cost optimization strategies (caching, cascading, batching)
- 🚧 Utilities (cost calculator, metrics evaluator)
- 🚧 Comprehensive test suite
- 🚧 CLI tools

## 🎯 Design Principles

### 1. Security First

All credentials from environment variables. Comprehensive validation. Never expose secrets.

### 2. Type Safety

Full type hints using Python 3.9+ features. Validated with mypy.

### 3. Production Ready

Real metrics tracking. Error handling. Logging. Documentation.

### 4. Cost Conscious

Keyword filtering. Prompt caching. Model cascading. Cost tracking.

### 5. Developer Experience

Clear error messages. Comprehensive docs. Consistent API. Type hints for IDE support.

## 📖 Examples

See the [examples/](./examples/) directory for complete working examples:

- `examples/basic_classification.py` - Simple signal classification
- `examples/batch_processing.py` - Process multiple signals efficiently
- `examples/custom_model.py` - Use different models and providers
- `examples/metrics_tracking.py` - Track costs and performance

## 🐛 Troubleshooting

### "API key not configured"

```python
ValueError: API key not configured for anthropic.
Please set ANTHROPIC_API_KEY in your .env file.
```

**Solution**: Copy `.env.example` to `.env` and add your real API key:
```bash
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY=your-real-key-here
```

### "anthropic package is required"

```python
ImportError: anthropic package is required.
Install with: pip install anthropic
```

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
# Or if you installed the package:
pip install -e .
```

### "Unknown model: gpt-4"

```python
NotImplementedError: OpenAI provider for gpt-4 is not yet implemented.
Use Claude models for now.
```

**Solution**: Use Claude models (only ones implemented currently):
```python
classifier = SignalClassifier(model="claude-sonnet")  # ✅ Works
classifier = SignalClassifier(model="claude-haiku")   # ✅ Works
classifier = SignalClassifier(model="claude-opus")    # ✅ Works
classifier = SignalClassifier(model="gpt-4")          # ❌ Not yet implemented
```

## 🤝 Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on contributing to this project.

## 📝 License

MIT License - see [LICENSE](./LICENSE) for details.

## 🔗 Related Documentation

- [Main README](./README.md) - Repository overview and documentation
- [PROMPT_DESIGN_PRINCIPLES.md](./PROMPT_DESIGN_PRINCIPLES.md) - Core prompt engineering patterns
- [MODEL_OPTIMIZATION_GUIDE.md](./MODEL_OPTIMIZATION_GUIDE.md) - Provider-specific optimizations
- [examples/signal-classification](./examples/signal-classification/README.md) - Production system case study
- [TODO.md](./TODO.md) - Planned features and roadmap

## 📧 Support

- **Issues**: https://github.com/awoods187/PM-Prompt-Patterns/issues
- **Discussions**: https://github.com/awoods187/PM-Prompt-Patterns/discussions

---

**Built with ❤️ for AI-native product managers**
