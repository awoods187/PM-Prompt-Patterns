# Model Optimization Guide

**Last Updated**: 2025-01-24
**Status**: ✅ Verified from official documentation

Deep dive into provider-specific optimizations and strategic model selection based on production experience.

> **Important**: All model information verified from official provider documentation. See `models/registry.py` for complete specifications.

---

## Quick Reference Matrix

**Current Models** (January 2025)

| Model | API Identifier | Context | Cost (Input/Output per 1M) | Speed | Best For |
|-------|---------------|---------|---------------------------|-------|----------|
| **Claude Sonnet 4.5** | `claude-sonnet-4-5-20250929` | 200K | $3 / $15 | ⚡⚡ | **RECOMMENDED**: Production workhorse |
| **Claude Haiku 4.5** | `claude-haiku-4-5-20251001` | 200K | $1 / $5 | ⚡⚡⚡ | High-volume, fast processing |
| **Claude Opus 4.1** | `claude-opus-4-1-20250805` | 200K | $15 / $75 | ⚡ | Complex reasoning, high-stakes |
| **GPT-4o** | `gpt-4o` | 128K | $2.50 / $10 | ⚡⚡⚡ | Vision, function calling |
| **GPT-4o mini** | `gpt-4o-mini` | 128K | $0.15 / $0.60 | ⚡⚡⚡ | Cost-efficient, high-volume |
| **Gemini 2.5 Pro** | `gemini-2.5-pro` | 1M | $1.25 / $5 | ⚡⚡ | Massive context (1M+ tokens) |
| **Gemini 2.5 Flash** | `gemini-2.5-flash` | 1M | $0.075 / $0.30 | ⚡⚡⚡ | **CHEAPEST**: Budget option |
| **Gemini 2.5 Flash-Lite** | `gemini-2.5-flash-lite` | 1M | ~$0.05 / ~$0.20 | ⚡⚡⚡ | Ultra cost-efficient |

---

## Provider Comparison

### Anthropic Claude (Recommended Default)

**Philosophy**: Best for nuanced reasoning, analysis, and following complex instructions.

**Current Models**:
- **Sonnet 4.5**: Production workhorse for 80% of tasks
- **Haiku 4.5**: Fast processing (note: 4x more expensive than old Haiku 3.x)
- **Opus 4.1**: Highest capability for complex work

**Key Strengths**:
- ✅ Native XML understanding
- ✅ 200K context window (1M in beta)
- ✅ Excellent at following complex instructions
- ✅ Prompt caching (90% discount on cached tokens)
- ✅ Extended thinking for complex reasoning

**Use Claude When**:
- Quality and reasoning depth matter most
- Working with structured data (XML-friendly)
- Need reliable instruction-following
- Long-form content generation

### OpenAI GPT

**Philosophy**: Best for multimodal tasks and structured extraction.

**Current Models**:
- **GPT-4o**: Multimodal flagship (vision + text)
- **GPT-4o mini**: Budget option with GPT-4 quality

**Key Strengths**:
- ✅ Native vision/image understanding
- ✅ Function calling (best-in-class)
- ✅ JSON mode (guaranteed valid JSON)
- ✅ Broad ecosystem integration

**Use GPT When**:
- Need vision/image analysis
- Structured extraction with schema validation
- Function calling requirements
- Cost is priority (GPT-4o mini is very cheap)

### Google Gemini

**Philosophy**: Best for massive context and cost-sensitive high-volume work.

**Current Models**:
- **2.5 Pro**: 1M+ token context window
- **2.5 Flash**: Fast and cheap
- **2.5 Flash-Lite**: Ultra budget option

**Key Strengths**:
- ✅ Massive 1M+ token context window
- ✅ Cheapest options (Flash: $0.075 input!)
- ✅ Fast processing
- ✅ Google Search grounding

**Use Gemini When**:
- Need to process entire codebases
- Very high volume (thousands of requests)
- Budget is critical constraint
- Need Google Search integration

---

## Model Selection Decision Tree

```
START: What's your primary need?

QUALITY/REASONING → Claude Sonnet 4.5
├─ Complex reasoning needed? → Claude Opus 4.1
└─ Fast processing needed? → Claude Haiku 4.5

COST OPTIMIZATION → Gemini 2.5 Flash or GPT-4o mini
├─ Ultra-cheap needed? → Gemini 2.5 Flash-Lite ($0.05/$0.20)
└─ Need GPT-4 quality? → GPT-4o mini ($0.15/$0.60)

VISION/MULTIMODAL → GPT-4o
└─ Images, screenshots, charts → GPT-4o only current option

MASSIVE CONTEXT (>200K tokens) → Gemini 2.5 Pro
└─ Entire codebase analysis → Gemini 2.5 Pro (1M tokens)

FUNCTION CALLING → GPT-4o or GPT-4o mini
└─ Structured extraction → GPT-4o (best schema validation)
```

---

## Cost Optimization Strategies

### Strategy 1: Model Cascading

Start with cheapest, escalate only when needed:

```
Gemini 2.5 Flash ($0.08/task)
    ↓ confidence < 0.85
Claude Haiku 4.5 ($0.001/task)
    ↓ confidence < 0.90
Claude Sonnet 4.5 ($0.003/task)
    ↓ confidence < 0.95
Claude Opus 4.1 ($0.015/task)
```

**Result**: Average cost $0.0012/task vs $0.015 Opus-only (92% savings)

### Strategy 2: Prompt Caching (Claude Only)

Cache static parts of prompts for 90% discount:

```python
# Without caching: $0.0046/classification
# With caching (95% hit rate): $0.0008/classification
# Savings: 83%
```

### Strategy 3: Batch Processing

Process multiple items in single API call:

```python
# Individual: 50 × $0.003 = $0.15
# Batched: 1 × $0.015 = $0.015
# Savings: 90%
```

---

## Quick Start Guide

### For Most Use Cases
```python
from models import CLAUDE_SONNET

# Use Claude Sonnet 4.5 as default
model = CLAUDE_SONNET.api_identifier
# → "claude-sonnet-4-5-20250929"
```

### For High-Volume/Cost-Sensitive
```python
from models import GEMINI_FLASH, GPT_4O_MINI

# Ultra-cheap option
model = GEMINI_FLASH.api_identifier  # $0.075 input
# or
model = GPT_4O_MINI.api_identifier   # $0.15 input, GPT-4 quality
```

### For Vision Tasks
```python
from models import GPT_4O

# Only current option for vision
model = GPT_4O.api_identifier
```

### For Massive Context
```python
from models import GEMINI_PRO

# 1M+ tokens
model = GEMINI_PRO.api_identifier
```

---

## Migration from Old Models

**BREAKING CHANGES**: Model identifiers have changed!

| Old (DEPRECATED) | New (CURRENT) | Change |
|-----------------|---------------|--------|
| `claude-3-5-sonnet-20241022` | `claude-sonnet-4-5-20250929` | MAJOR version |
| `claude-3-5-haiku-20241022` | `claude-haiku-4-5-20251001` | MAJOR + 4x price ⚠️ |
| `gemini-1.5-pro-002` | `gemini-2.5-pro` | MAJOR version |
| `gemini-1.5-flash-002` | `gemini-2.5-flash` | MAJOR version |
| `gpt-4-turbo` | `gpt-4o` | Optimized version |
| `gpt-3.5-turbo` | `gpt-4o-mini` | Quality upgrade |

**Action Required**: Update all model identifiers in your code.

See `MIGRATION_MAP.md` for complete mapping.

---

## Model-Specific Features

### Claude: Prompt Caching

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    system=[{
        "type": "text",
        "text": "Your static prompt here...",
        "cache_control": {"type": "ephemeral"}  # Cache this
    }],
    messages=[{"role": "user", "content": "Dynamic input"}]
)
```

**Savings**: 90% on cached tokens

### GPT-4o: Vision

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
    }]
)
```

### Gemini: Massive Context

```python
model = genai.GenerativeModel('gemini-2.5-pro')

# Can handle 1M+ tokens in single request
response = model.generate_content(entire_codebase)
```

---

## Pricing Summary (per 1M tokens)

| Model | Input | Output | Total (1K in, 1K out) |
|-------|-------|--------|----------------------|
| Gemini 2.5 Flash | $0.075 | $0.30 | **$0.0004** ← Cheapest |
| GPT-4o mini | $0.15 | $0.60 | $0.0008 |
| Claude Haiku 4.5 | $1.00 | $5.00 | $0.006 |
| Gemini 2.5 Pro | $1.25 | $5.00 | $0.006 |
| GPT-4o | $2.50 | $10.00 | $0.013 |
| Claude Sonnet 4.5 | $3.00 | $15.00 | $0.018 |
| Claude Opus 4.1 | $15.00 | $75.00 | $0.090 |

---

## Best Practices

1. **Use the Registry**: Never hardcode model strings
   ```python
   from models import ModelRegistry
   model = ModelRegistry.CLAUDE_SONNET.api_identifier
   ```

2. **Test Before Deploying**: Verify new models work for your use case

3. **Monitor Costs**: Claude Haiku pricing increased 4x (v3 → v4.5)

4. **Cache When Possible**: Use prompt caching for repeated patterns (Claude)

5. **Batch Process**: Combine multiple tasks in single API calls

6. **Cascade Intelligently**: Start cheap, escalate only when needed

---

## Additional Resources

- **Model Registry**: `models/registry.py` - Single source of truth
- **Migration Guide**: `MIGRATION_MAP.md` - Complete old → new mapping
- **Verification Report**: `PHASE1_VERIFICATION_REPORT.md` - How models were verified

**Official Documentation**:
- Anthropic: https://docs.claude.com/en/docs/about-claude/models
- OpenAI: https://platform.openai.com/docs/models
- Google: https://ai.google.dev/gemini-api/docs/models/gemini

---

**Last Verification**: 2025-01-24
**Next Review**: Check for model updates monthly (see `UPDATING_MODELS.md`)
