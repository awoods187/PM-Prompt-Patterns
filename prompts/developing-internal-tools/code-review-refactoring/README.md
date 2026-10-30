# Code Review & Refactoring for Open Source

## 🎯 Purpose

**Comprehensive code review and refactoring prompt for preparing internal codebases for team sharing or open-sourcing.**

Focuses on security audit, code quality, documentation, and best practices compliance.

**Business Value**:
- Prevent security incidents from exposed credentials
- Reduce onboarding time with better documentation
- Improve code maintainability and collaboration
- Ensure compliance with industry best practices
- Enable safe open-sourcing of internal projects

**Use Cases**:
- Pre-open-source security audit
- Internal code sharing preparation
- Legacy codebase modernization
- Team handoff preparation
- Technical debt reduction

**Production metrics**:
- Security issue detection: ~98% (credentials, keys)
- Documentation coverage improvement: 0% → 90%+
- PEP 8 compliance improvement: Variable → 95%+
- Processing time: ~2-5min per 1000 lines of code

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
prompt = get_prompt("developing-internal-tools/code-review-refactoring", model=model.id)

# Use the prompt
result = model.generate(prompt.format(**your_variables))
```

### Manual Provider Selection

```python
# Explicit provider selection
claude_prompt = get_prompt("developing-internal-tools/code-review-refactoring", provider="claude")
openai_prompt = get_prompt("developing-internal-tools/code-review-refactoring", provider="openai")
gemini_prompt = get_prompt("developing-internal-tools/code-review-refactoring", provider="gemini")
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
