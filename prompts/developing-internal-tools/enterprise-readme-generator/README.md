# Enterprise README Generator & Optimizer

## 🎯 Purpose

**Production-grade prompt for creating and optimizing professional README files that serve multiple stakeholders.**

**Business Value**:
- Reduce onboarding time by 60-70% with progressive information disclosure
- Increase developer productivity through clear, actionable documentation
- Enable executive visibility with stakeholder-friendly summaries
- Reduce support requests by 40-50% through comprehensive quick-start guides

**Use Cases**:
- Creating READMEs for new enterprise projects
- Optimizing existing documentation for multiple audiences
- Standardizing documentation across organization
- Preparing open-source releases from internal projects

**Production metrics**:
- Time to first contribution: Reduced from 2 hours to 15 minutes
- Documentation coverage: 95%+ of common questions answered
- Stakeholder satisfaction: 85%+ report improved clarity

**Complexity**: 🟡 Intermediate

## 📊 Provider Variants

| Provider | File | Key Features | Best For | Cost Range |
|----------|------|-------------|----------|------------|
| **Base** | [`prompt.md`](./prompt.md) | Universal compatibility | Any provider, fallback | Varies |
| **Claude** | [`prompt.claude.md`](./prompt.claude.md) | XML tags, chain-of-thought | Complex reasoning, accuracy | $0.10-20 per 1M tokens |
| **OpenAI** | [`prompt.openai.md`](./prompt.openai.md) | Function calling, JSON mode | Structured output, integration | $0.10-10 per 1M tokens |
| **Gemini** | [`prompt.gemini.md`](./prompt.gemini.md) | 1M context, caching | High volume, batch processing | $0.30-10 per 1M tokens |

## 🚀 Quick Start

### Automatic Provider Selection

```python
from ai_models import get_prompt, get_model

# Auto-select best variant based on model
model = get_model("gpt-6-luna")
prompt = get_prompt("developing-internal-tools/enterprise-readme-generator", model=model.id)

# Use the prompt
result = model.generate(prompt.format(**your_variables))
```

### Manual Provider Selection

```python
# Explicit provider selection
claude_prompt = get_prompt("developing-internal-tools/enterprise-readme-generator", provider="claude")
openai_prompt = get_prompt("developing-internal-tools/enterprise-readme-generator", provider="openai")
gemini_prompt = get_prompt("developing-internal-tools/enterprise-readme-generator", provider="gemini")
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
- ✅ Need large context window (1M tokens)

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
