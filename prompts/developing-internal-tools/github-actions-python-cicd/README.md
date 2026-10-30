# GitHub Actions CI/CD Pipeline Generator for Python

## 🎯 Purpose

**Production-grade prompt for generating comprehensive GitHub Actions CI/CD pipelines for Python applications.**

**Business Value**:
- Reduce setup time from 4-8 hours to 10-20 minutes (85-95% savings)
- Catch 90%+ of issues before PR merge through automated quality gates
- Accelerate PR review cycles by 70% with automated checks
- Prevent production bugs with 100% coverage enforcement
- Enable safe, confident deploys with comprehensive test and security coverage

**Use Cases**:
- New Python project initialization with production-ready CI/CD
- Modernizing legacy projects without CI/CD
- Open source repository setup
- Enterprise projects requiring strict quality gates

**Production metrics**:
- Setup time: 10-20 minutes vs 4-8 hours manual
- Issue detection rate: 90%+ before merge
- PR review time reduction: 70% faster

**Complexity**: 🔴 Advanced

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
prompt = get_prompt("developing-internal-tools/github-actions-python-cicd", model=model.id)

# Use the prompt
result = model.generate(prompt.format(**your_variables))
```

### Manual Provider Selection

```python
# Explicit provider selection
claude_prompt = get_prompt("developing-internal-tools/github-actions-python-cicd", provider="claude")
openai_prompt = get_prompt("developing-internal-tools/github-actions-python-cicd", provider="openai")
gemini_prompt = get_prompt("developing-internal-tools/github-actions-python-cicd", provider="gemini")
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
