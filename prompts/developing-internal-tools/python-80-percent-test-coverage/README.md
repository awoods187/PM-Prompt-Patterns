# Python 80% Test Coverage Achievement

## 🎯 Purpose

**Systematic test generation prompt for achieving 80% code coverage across Python codebases.**

**Business Value**:
- Reduce production bugs by 60-80% with comprehensive test coverage
- Enable safe refactoring with confidence in test suite
- Meet deployment quality gates (80%+ coverage requirements)
- Reduce manual testing effort by ~40 hours per month
- Catch regressions before production deployment

**Use Cases**:
- Legacy codebases requiring test coverage before deployment
- Pre-open-source quality improvement
- Meeting compliance requirements (SOC2, ISO 27001)
- Technical debt reduction initiatives
- CI/CD pipeline quality gates

**Production metrics**:
- Coverage improvement: 0-30% → 80-95% systematically
- Test generation speed: ~50-100 tests per module (5-10 min)
- Edge case coverage: 90%+ (boundaries, None, empty, invalid types)
- Refactoring recommendations: ~3-5 per module for untestable code

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
prompt = get_prompt("developing-internal-tools/python-80-percent-test-coverage", model=model.id)

# Use the prompt
result = model.generate(prompt.format(**your_variables))
```

### Manual Provider Selection

```python
# Explicit provider selection
claude_prompt = get_prompt("developing-internal-tools/python-80-percent-test-coverage", provider="claude")
openai_prompt = get_prompt("developing-internal-tools/python-80-percent-test-coverage", provider="openai")
gemini_prompt = get_prompt("developing-internal-tools/python-80-percent-test-coverage", provider="gemini")
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
