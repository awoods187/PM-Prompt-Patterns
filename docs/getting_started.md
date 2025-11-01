# Getting Started with PM Prompt Toolkit

**Last Updated:** 2025-11-01
**Status:** Complete
**Prerequisites:** Python 3.9+, pip

---

## Overview

This guide walks you through installing the PM Prompt Toolkit, configuring your environment, and running your first prompt in under 10 minutes.

---

## Table of Contents

1. [Installation](#installation)
2. [Environment Setup](#environment-setup)
3. [Quick Start Example](#quick-start-example)
4. [Understanding the Output](#understanding-the-output)
5. [Next Steps](#next-steps)
6. [Troubleshooting](#troubleshooting)

---

## Installation

### Option 1: Install from Source (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/awoods187/PM-Prompt-Patterns.git
cd PM-Prompt-Patterns

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .

# Verify installation
python -c "from ai_models import get_model; print('✅ Installation successful!')"
```

### Option 2: Install Specific Cloud Providers

```bash
# For AWS Bedrock support
pip install -e ".[bedrock]"

# For Google Vertex AI support
pip install -e ".[vertex]"

# For all cloud providers
pip install -e ".[all]"

# For development (includes testing/linting tools)
pip install -e ".[dev]"
```

---

## Environment Setup

### 1. Create Environment File

Copy the example environment file:

```bash
cp .env.example .env
```

### 2. Configure API Keys

Edit `.env` and add your API keys:

```bash
# Required: At least one provider
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here

# Optional: Cloud providers
ENABLE_BEDROCK=false
ENABLE_VERTEX=false
```

**Where to get API keys:**
- **Anthropic Claude:** https://console.anthropic.com/
- **OpenAI GPT:** https://platform.openai.com/api-keys
- **Google Gemini:** https://makersuite.google.com/app/apikey

### 3. Verify Configuration

```bash
# Test that environment is loaded
python -c "from pm_prompt_toolkit.config import get_settings; print(get_settings())"
```

---

## Quick Start Example

### Method 1: Using the AI Models Registry

The simplest way to get started is using the model registry:

```python
from ai_models import get_model, list_models

# List all available models
models = list_models()
print(f"Available models: {len(models)}")

# Get a specific model
model = get_model("claude-sonnet-4-5")
print(f"Model: {model.name}")
print(f"Context window: {model.metadata.context_window_input:,} tokens")
print(f"Cost: ${model.pricing.input_per_1m}/1M input tokens")
```

### Method 2: Using the Provider Factory

For classification and more advanced use cases:

```python
from pm_prompt_toolkit.providers import get_provider

# Get a provider (auto-selects based on .env configuration)
provider = get_provider("claude-sonnet")

# Classify a signal
text = "We need SSO integration before Q4 rollout"
result = provider.classify(text)

print(f"Category: {result.category}")
print(f"Confidence: {result.confidence:.2f}")
print(f"Cost: ${result.cost:.4f}")
```

### Method 3: Run the Basic Example

We've included a complete example that demonstrates signal classification:

```bash
# Run the basic example
python examples/basic_example.py
```

**Expected output:**
```
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

2. Signal: "Dashboard won't load, getting 500 errors"
   → Category: bug
   → Confidence: 0.98
   → Method: keyword
   → Cost: $0.0000
   → Latency: 0ms
   💰 FREE (keyword match!)

...
```

---

## Understanding the Output

### Classification Results

Each classification returns:

- **category**: The detected category (e.g., `feature_request`, `bug`, `churn_risk`)
- **confidence**: Confidence score from 0.0 to 1.0
- **method**: How it was classified:
  - `keyword`: Fast, free pattern matching
  - `llm`: AI model classification (costs API credits)
  - `cached`: Retrieved from cache (costs 10% of normal)
- **cost**: Actual cost in USD for this request
- **latency_ms**: Time taken in milliseconds

### Cost Optimization

The toolkit automatically optimizes costs:

1. **Keyword filtering first** - Free pattern matching catches obvious cases
2. **Prompt caching** - Reuses cached prompts for 90% savings
3. **Model cascading** - Use cheaper models when appropriate

**Example savings:**
```
Without optimization: 5,000 signals × $0.0008 = $4.00/week
With optimization:    5,000 signals × $0.0001 = $0.50/week
Savings:              87.5%
```

---

## Next Steps

### 1. Explore Models

```python
from ai_models import list_models, filter_by_capability

# List all models
all_models = list_models()

# Filter by capability
vision_models = filter_by_capability("vision")
cheap_models = [m for m in all_models if m.pricing.cost_tier == "budget"]
```

**See:** [Model Registry](../ai_models/README.md)

### 2. Try Different Providers

```python
from pm_prompt_toolkit.providers import get_provider

# Force specific provider
claude_provider = get_provider("claude:claude-sonnet-4-5")
gpt_provider = get_provider("openai:gpt-4o")
gemini_provider = get_provider("google:gemini-2.0-flash-exp")

# Use AWS Bedrock (requires configuration)
bedrock_provider = get_provider("bedrock:claude-sonnet-4-5")
```

**See:** [Provider Documentation](./python_package_readme.md#providers)

### 3. Production Examples

Study our complete production systems:

- **[Epic Categorization](../examples/epic-categorization/)** - Real-world classification system with 95% accuracy
- **[Basic Example](../examples/basic_example.py)** - Simple signal classification with metrics

**See:** [All Examples](../examples/)

### 4. Learn Advanced Techniques

- [Prompt Design Principles](./prompt_design_principles.md)
- [Cost Optimization](./cost_optimization.md)
- [Quality Evaluation](./quality_evaluation.md)

### 5. Integrate into Your Project

```python
# In your application
from pm_prompt_toolkit.providers import get_provider

def categorize_user_feedback(feedback_text: str) -> dict:
    """Categorize user feedback using AI."""
    provider = get_provider("claude-sonnet")  # Or configure via env
    result = provider.classify(feedback_text)

    return {
        "category": result.category,
        "confidence": result.confidence,
        "cost": result.cost,
        "method": result.method,
    }

# Use it
feedback = "The dashboard is too slow"
category = categorize_user_feedback(feedback)
print(f"This is a {category['category']} (confidence: {category['confidence']:.0%})")
```

---

## Troubleshooting

### Common Issues

#### 1. Import Error: No module named 'pm_prompt_toolkit'

**Solution:**
```bash
# Make sure you installed the package
pip install -e .

# Verify installation
pip show pm-prompt-toolkit
```

#### 2. Import Error: No module named 'anthropic'

**Solution:**
```bash
# Install missing dependencies
pip install anthropic openai google-generativeai
```

#### 3. Missing API Key Error

**Error:** `ValueError: ANTHROPIC_API_KEY not found`

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Copy from example if missing
cp .env.example .env

# Edit and add your API key
nano .env  # or your preferred editor
```

#### 4. Model Not Found Error

**Error:** `ValueError: Model 'xyz' not found`

**Solution:**
```python
# List available models
from ai_models import list_models

models = list_models()
for model in models:
    print(f"  - {model.model_id}")
```

**Available models:**
- `claude-haiku-4-0`
- `claude-sonnet-4-5`
- `claude-opus-4-0`
- `gpt-4o`
- `gpt-4o-mini`
- `gemini-2.0-flash-exp`
- `gemini-2.5-pro`

#### 5. Tests Failing

**Solution:**
```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run specific test file
pytest tests/test_ai_models.py -v
```

#### 6. API Rate Limits

**Error:** `RateLimitError: You exceeded your current quota`

**Solution:**
- Check your API usage dashboard
- Consider using a cheaper model (claude-haiku vs claude-opus)
- Enable caching to reduce API calls
- Implement exponential backoff retry logic

---

## Development Setup

For contributors and advanced users:

```bash
# Install with all development tools
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run linters
black .
ruff check .
mypy pm_prompt_toolkit/

# Run tests with coverage
pytest --cov=pm_prompt_toolkit --cov-report=html

# View coverage report
open htmlcov/index.html
```

**See:** [CONTRIBUTING.md](../.github/CONTRIBUTING.md)

---

## Additional Resources

### Documentation
- [README.md](../README.md) - Project overview
- [prompt_design_principles.md](./prompt_design_principles.md) - Core patterns
- [project_structure.md](./project_structure.md) - Codebase organization
- [CHANGELOG.md](../CHANGELOG.md) - Version history

### Support
- **Issues:** [GitHub Issues](https://github.com/awoods187/PM-Prompt-Patterns/issues)
- **Security:** [SECURITY.md](../.github/SECURITY.md)
- **Contributing:** [CONTRIBUTING.md](../.github/CONTRIBUTING.md)

### Community
- **Roadmap:** [ROADMAP.md](../.github/ROADMAP.md)
- **Code of Conduct:** [CODE_OF_CONDUCT.md](../.github/CODE_OF_CONDUCT.md)

---

## Success Criteria

You're ready to move on when you can:

- ✅ Install the package without errors
- ✅ Import and use the model registry
- ✅ Run `examples/basic_example.py` successfully
- ✅ Classify text using a provider
- ✅ Understand the cost breakdown

**Ready?** Continue to [Advanced Techniques](./advanced_techniques.md) →

---

**Questions?** Open an issue or check the [troubleshooting](#troubleshooting) section above.
