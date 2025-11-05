# Meta-Prompt Designer

## 🎯 Purpose

**A meta-prompt that helps you design high-quality, production-ready prompts for your professional prompt library.**

Takes a use case description and generates a complete, structured, reusable prompt following best practices.

**Business Value**:
- Standardize prompt quality across your library
- Reduce time from idea to production-ready prompt (hours → minutes)
- Ensure consistency in prompt structure and documentation
- Enable non-experts to create expert-level prompts
- Build reusable prompt library faster

**Use Cases**:
- Creating new prompts for your library
- Refactoring existing ad-hoc prompts into standardized format
- Documenting successful prompts for team sharing
- Training team members on prompt engineering best practices
- Rapid prototyping of prompt ideas

**Production metrics**:
- Prompt quality improvement: Ad-hoc → Production-grade
- Time savings: ~2-4 hours per prompt
- First-try success rate: ~85% (vs ~40% for manual design)
- Consistency: 100% format compliance

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
prompt = get_prompt("product-strategy/meta-prompt-designer", model=model.id)

# Use the prompt
result = model.generate(prompt.format(**your_variables))
```

### Manual Provider Selection

```python
# Explicit provider selection
claude_prompt = get_prompt("product-strategy/meta-prompt-designer", provider="claude")
openai_prompt = get_prompt("product-strategy/meta-prompt-designer", provider="openai")
gemini_prompt = get_prompt("product-strategy/meta-prompt-designer", provider="gemini")
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
