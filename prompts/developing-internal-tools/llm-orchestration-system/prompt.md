# Multi-Provider LLM Orchestration System

**Complexity**: 🔴 Advanced
**Category**: Code Generation / System Architecture
**Model Compatibility**: ✅ Claude Opus (best) | ✅ Claude Sonnet 4 | ⚠️ GPT-4 (may need more guidance)

## Overview

Production-grade prompt for building a Python library that provides unified access to multiple LLM providers (OpenAI, Anthropic, Google Gemini, AWS Bedrock, Google Vertex AI) with dynamic model discovery, intelligent fallback, and comprehensive cost tracking.

**Business Value**:
- Reduce vendor lock-in with provider-agnostic interface
- Enable cost optimization through provider/model selection across 5 major providers
- Improve reliability with automatic within-provider fallback
- Gain visibility into LLM usage and costs across applications
- Simplify integration with single unified API
- Support multi-cloud deployments (AWS, GCP, direct APIs)

**Use Cases**:
- Building LLM-powered applications that need provider flexibility
- Creating cost-aware AI systems with usage tracking
- Migrating between LLM providers without code changes
- Prototyping with multiple models from single codebase
- Enterprise applications requiring cost accountability
- AWS-native applications leveraging Bedrock
- GCP-native applications leveraging Vertex AI
- Multi-cloud architectures with provider diversity

**Production metrics**:
- Development time: 3-4 days for full implementation (5 providers)
- Code quality: 90%+ test coverage achievable
- Reliability: <1% failure rate with proper fallback configuration
- Cost visibility: 100% API call tracking and attribution
- Provider coverage: 5 major providers (OpenAI, Anthropic, Gemini, Bedrock, Vertex)

---

---

## Prompt

```
You are a senior Python architect specializing in building robust, production-grade libraries for LLM integration. Your expertise includes API design, adapter patterns, error handling, cloud provider SDKs (AWS, GCP), and building maintainable, well-tested Python packages.

## YOUR TASK

Build a complete Python library for multi-provider LLM orchestration that provides a unified interface to OpenAI, Anthropic, Google Gemini, AWS Bedrock, and Google Vertex AI with dynamic model discovery, intelligent fallback, and comprehensive cost tracking.

---

## SYSTEM REQUIREMENTS

### Core Architecture

**Language & Standards**:
- Python 3.9+ with type hints throughout
- Integration type: Importable library/module (NOT standalone service)
- Response patterns: Both streaming and standard request/response
- Design pattern: Adapter pattern with unified abstract interface
- Code style: PEP 8 compliant, Black formatted

**Dependencies**:
```

---

## Production Patterns

### Pattern 1: Gradual Provider Migration

**Use case**: Migrate from one provider to another without downtime.

```python
# Week 1: Add new provider to config
# config.yaml
active_provider: "openai"  # Still using OpenAI
active_model: "gpt-4"

providers:
  openai:
    api_key: "${OPENAI_API_KEY}"
    fallback_models: ["gpt-4", "gpt-4o-mini"]

  anthropic:  # Add Anthropic
    api_key: "${ANTHROPIC_API_KEY}"
    fallback_models: ["claude-opus-4-20250514"]

# Week 2: Test Anthropic integration
from llm_orchestrator import LLMOrchestrator

orchestrator = LLMOrchestrator("config.yaml")

# Verify Anthropic models available
anthropic_models = orchestrator.get_available_models("anthropic")
print(f"Anthropic ready: {len(anthropic_models)} models")

# Week 3: Switch active provider
# config.yaml
active_provider: "anthropic"  # Switch!
active_model: "claude-opus-4-20250514"

# No code changes needed - just config update
```

### Pattern 2: Cost-Aware Model Selection

**Use case**: Track costs across different models to optimize spending.

```python
from llm_orchestrator import LLMOrchestrator
import pandas as pd

# Run experiment with different models
configs = [
    ("openai", "gpt-4"),
    ("openai", "gpt-4o-mini"),
    ("anthropic", "claude-sonnet-4-5"),
]

results = []

for provider, model in configs:
    # Update config
    orchestrator = LLMOrchestrator("config.yaml")

    # Run same prompt 100 times
    for i in range(100):
        response = orchestrator.send_request(
            messages=[{"role": "user", "content": "Summarize quantum physics in 50 words"}],
            temperature=0.7
        )

    # Get cost
    cost = orchestrator.get_session_cost()
    results.append({
        "provider": provider,
        "model": model,
        "cost": cost,
        "cost_per_request": cost / 100
    })

# Analyze results
df = pd.DataFrame(results)
print(df.sort_values("cost"))

# Output:
#     provider                          model      cost  cost_per_request
# 1    openai              gpt-4o-mini   0.42          0.0042
# 2  anthropic  claude-sonnet-4-5   1.85          0.0185
# 0    openai                      gpt-4   6.30          0.0630
```

### Pattern 3: Multi-Environment Configuration

**Use case**: Different configs for dev/staging/production.

```python
# config.dev.yaml (cheap models for testing)
active_provider: "openai"
active_model: "gpt-4o-mini"

providers:
  openai:
    api_key: "${OPENAI_API_KEY}"
    fallback_models: ["gpt-4o-mini"]

cost_tracking:
  enabled: true
  log_path: "./dev_costs.log"

# config.prod.yaml (production models)
active_provider: "anthropic"
active_model: "claude-opus-4-20250514"

providers:
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
    fallback_models:
      - "claude-opus-4-20250514"
      - "claude-sonnet-4-5"  # Fallback to cheaper

cost_tracking:
  enabled: true
  log_path: "/var/log/llm_costs.log"

# Application code
import os
from llm_orchestrator import LLMOrchestrator

env = os.getenv("ENVIRONMENT", "dev")
config_file = f"config.{env}.yaml"

orchestrator = LLMOrchestrator(config_file)
```

---

---

## Quality Evaluation

### Before (Direct Provider Integration)

**Problems**:
- ❌ Different API for each provider (openai vs anthropic vs genai)
- ❌ No unified error handling
- ❌ Manual cost tracking with spreadsheets
- ❌ Hard to switch providers (code changes required)
- ❌ No fallback logic (single point of failure)
- ❌ No model discovery (hardcoded model names)

**Code Example**:
```python
# Different code for each provider
import openai
import anthropic

# OpenAI
openai_response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)

# Anthropic (completely different API)
anthropic_client = anthropic.Anthropic(api_key="...")
anthropic_response = anthropic_client.messages.create(
    model="claude-opus-4-20250514",
    messages=[{"role": "user", "content": "Hello"}]
)

# No unified interface - can't swap easily
```

### After (Orchestrator Implementation)

**Improvements**:
- ✅ Single unified interface for all providers
- ✅ Automatic fallback within provider
- ✅ Comprehensive cost tracking and reporting
- ✅ Easy provider switching via config
- ✅ Dynamic model discovery
- ✅ Production-ready error handling

**Code Example**:
```python
from llm_orchestrator import LLMOrchestrator

# Same code works for any provider
orchestrator = LLMOrchestrator("config.yaml")

# Works regardless of active provider
response = orchestrator.send_request(
    messages=[{"role": "user", "content": "Hello"}]
)

# Automatic fallback, cost tracking, error handling
print(response.content)
print(f"Cost: ${orchestrator.get_session_cost():.4f}")

# Switch providers: just edit config.yaml, no code changes
```

---

---

## Cost Comparison

| Approach | Development Time | Maintenance | Flexibility | Cost Visibility |
|----------|------------------|-------------|-------------|-----------------|
| **Direct integration** | 2-3 days per provider | High (3 codebases) | Low | Manual tracking |
| **Wrapper functions** | 3-4 days | Medium | Medium | Basic logging |
| **This orchestrator** | 2-3 days (one time) | Low (unified) | High | Complete tracking |

**ROI Calculation**:
- Initial development: 2-3 days
- Savings per provider addition: 1-2 days
- Maintenance reduction: 60-70%
- Cost visibility: Priceless (enables optimization)
- **Payback**: After 2nd provider integration

---

---

## Common Issues & Fixes

### Issue 1: Import Errors

**Problem**: `ModuleNotFoundError: No module named 'llm_orchestrator'`

**Fix**: Install in development mode
```bash
# From project root
pip install -e .

# Or install dependencies
pip install -r requirements.txt
```

### Issue 2: API Keys Not Resolved

**Problem**: Config shows `${OPENAI_API_KEY}` literally instead of actual key.

**Fix**: Ensure environment variables are set
```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="..."

# Verify
echo $OPENAI_API_KEY
```

### Issue 3: Model Not Found

**Problem**: `ModelNotFoundError: gpt-4o not found`

**Fix**: Refresh model registry
```python
orchestrator = LLMOrchestrator("config.yaml")
orchestrator.refresh_models()  # Fetch latest models

# Check available models
models = orchestrator.get_available_models("openai")
print(models)
```

### Issue 4: Streaming Not Working

**Problem**: Streaming request returns all content at once.

**Fix**: Ensure you're iterating properly
```python
# Wrong - consumes iterator immediately
response = orchestrator.send_streaming_request(messages)
print(response)  # Iterator object, not content

# Correct - iterate over chunks
for chunk in orchestrator.send_streaming_request(messages):
    print(chunk, end='', flush=True)
```

---

---

## Related Prompts

- [Code Review & Refactoring](./code-review-refactoring.md) - For reviewing generated code
- [Enterprise README Generator](./enterprise-readme-generator.md) - For creating library documentation

---

**Success Metrics**:

After implementing this system, you should achieve:
- ✅ Single unified interface for 5 major providers
- ✅ 90%+ test coverage
- ✅ <1% request failure rate with fallback
- ✅ 100% cost visibility and tracking across all providers
- ✅ <5 minute provider switching time
- ✅ Zero vendor lock-in
- ✅ Multi-cloud deployment ready (AWS + GCP)
- ✅ 30-70% cost reduction through provider optimization
- ✅ Support for 20+ different models
- ✅ Enterprise-grade security (IAM, Workload Identity)

**Real-World Impact**:
- **Development Time Saved**: 2-3 days per additional provider integration
- **Maintenance Reduction**: 60-70% less code to maintain vs separate integrations
- **Cost Optimization**: $500-5000/month savings through optimal model selection
- **Flexibility**: Switch providers in <5 minutes vs days of refactoring
- **Reliability**: <0.5% failure rate with 3-model fallback chains

**Remember**: This is production infrastructure - prioritize reliability, testability, maintainability, and security over features. Build incrementally and test thoroughly at each phase. Use appropriate authentication methods for each environment (dev vs production). Consider cloud provider egress charges and regional availability when selecting providers. Always follow security best practices for credential management.
