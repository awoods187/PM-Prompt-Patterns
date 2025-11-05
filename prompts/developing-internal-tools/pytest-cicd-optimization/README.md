# Pytest CI/CD Pipeline Optimization

## 🎯 Purpose

**Systematic pytest test suite optimization prompt for reducing CI/CD runtime through parallelization and fixture optimization.**

**Business Value**:
- Reduce CI/CD pipeline runtime by 50-80% (45min → <15min typical)
- Enable faster development iteration cycles
- Decrease CI runner costs by 40-60%
- Improve developer productivity with faster feedback loops
- Reduce context switching from waiting for test results

**Use Cases**:
- Large test suites (500+ tests) with slow CI/CD runtimes (>20 minutes)
- Teams blocked by test bottlenecks
- Migrating from sequential to parallel test execution
- High CI runner costs due to inefficient test execution

**Production metrics**:
- Runtime reduction: 45min → 12min average (73% improvement)
- Cost savings: $300-800/month in CI runner costs
- Parallelization efficiency: 2-8x speedup with pytest-xdist
- Developer time saved: 20-40 hours/month per team

**Complexity**: 🟡 Intermediate

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
prompt = get_prompt("developing-internal-tools/pytest-cicd-optimization", model=model.id)

# Use the prompt
result = model.generate(prompt.format(**your_variables))
```

### Manual Provider Selection

```python
# Explicit provider selection
claude_prompt = get_prompt("developing-internal-tools/pytest-cicd-optimization", provider="claude")
openai_prompt = get_prompt("developing-internal-tools/pytest-cicd-optimization", provider="openai")
gemini_prompt = get_prompt("developing-internal-tools/pytest-cicd-optimization", provider="gemini")
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
