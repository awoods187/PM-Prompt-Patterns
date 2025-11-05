# Multi-Provider LLM Orchestration System

## 🎯 Purpose

**Production-grade prompt for building a Python library that provides unified access to multiple LLM providers (OpenAI, Anthropic, Google Gemini, AWS Bedrock, Google Vertex AI).**

**Business Value**:
- Reduce vendor lock-in with provider-agnostic interface
- Enable cost optimization through provider/model selection across 5 major providers
- Improve reliability with automatic within-provider fallback
- Gain visibility into LLM usage and costs
- Support multi-cloud deployments (AWS, GCP, direct APIs)

**Use Cases**:
- Building LLM-powered applications that need provider flexibility
- Creating cost-aware AI systems with usage tracking
- Migrating between LLM providers without code changes
- Enterprise applications requiring cost accountability
- Multi-cloud architectures with provider diversity

**Production metrics**:
- Development time: 3-4 days for full implementation (5 providers)
- Code quality: 90%+ test coverage achievable
- Reliability: <1% failure rate with proper fallback
- Provider coverage: 5 major providers

**Complexity**: 🔴 Advanced

## 📊 Provider Variants

| Provider | File | Key Features | Best For | Cost Range |
|----------|------|-------------|----------|------------|
| **Base** | [`prompt.md`](./prompt.md) | Universal compatibility | Any provider, fallback | Varies |
| **Claude** | [`prompt.claude.md`](./prompt.claude.md) | XML tags, chain-of-thought | Complex reasoning, accuracy | $1-15 per 1M tokens |
| **OpenAI** | [`prompt.openai.md`](./prompt.openai.md) | Function calling, JSON mode | Structured output, integration | $0.15-10 per 1M tokens |
| **Gemini** | [`prompt.gemini.md`](./prompt.gemini.md) | 2M context, caching | High volume, batch processing | $0.038-5 per 1M tokens |

## 🚀 Quick Start

### Automatic Provider Selection

```python
from ai_models import get_prompt, get_model

# Auto-select best variant based on model
model = get_model("gpt-4o")
prompt = get_prompt("developing-internal-tools/llm-orchestration-system", model=model.id)

# Use the prompt
result = model.generate(prompt.format(**your_variables))
```

### Manual Provider Selection

```python
# Explicit provider selection
claude_prompt = get_prompt("developing-internal-tools/llm-orchestration-system", provider="claude")
openai_prompt = get_prompt("developing-internal-tools/llm-orchestration-system", provider="openai")
gemini_prompt = get_prompt("developing-internal-tools/llm-orchestration-system", provider="gemini")
```

## 🎯 When to Use Each Provider

### Use Claude when:
- ✅ Accuracy is critical
- ✅ Complex reasoning required
- ✅ Need detailed explanations
- ✅ Can leverage prompt caching (90% savings)

### Use OpenAI when:
- ✅ Need strict JSON schema validation
- ✅ Function calling for integration
- ✅ Batch processing with parallel tools
- ✅ Reproducible results required

### Use Gemini when:
- ✅ Ultra-high volume (10K+ operations/day)
- ✅ Cost is primary concern
- ✅ Can batch operations together
- ✅ Need large context window (2M tokens)

## 📚 Examples

See the individual prompt files for detailed usage examples:
- [Base Prompt](./prompt.md) - Universal examples
- [Claude Examples](./prompt.claude.md) - XML format, caching
- [OpenAI Examples](./prompt.openai.md) - Function calling, batch processing
- [Gemini Examples](./prompt.gemini.md) - Context window, ultra-low cost

## 🔗 Related Prompts

Browse more prompts in the [prompts directory](../../).

## 📝 Notes

- All variants return compatible output formats
- Provider selection is based on your specific use case requirements
- Cost estimates are approximate and vary by usage patterns
- See [provider-specific-prompts.md](../../docs/provider-specific-prompts.md) for detailed optimization guide

---
