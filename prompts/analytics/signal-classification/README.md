# Customer Signal Classification - Multi-Provider Prompt

## 🎯 Purpose

Automatically classify customer feedback, support tickets, and product signals into standardized categories (feature requests, bug reports, churn risks, expansion signals, general feedback) for intelligent routing and prioritization.

## 📊 Provider Variants

| Provider | File | Key Features | Best For | Cost/1K Signals |
|----------|------|-------------|----------|-----------------|
| **Base** | [`prompt.md`](./prompt.md) | Universal compatibility | Any provider, fallback | Varies |
| **Claude** | [`prompt.claude.md`](./prompt.claude.md) | XML tags, chain-of-thought | Complex reasoning, accuracy | $0.10-2 |
| **OpenAI** | [`prompt.openai.md`](./prompt.openai.md) | Function calling, JSON mode | Structured output, integration | $0.10-2 |
| **Gemini** | [`prompt.gemini.md`](./prompt.gemini.md) | 1M context, caching | High volume, batch processing | $0.30-2 |

## 🚀 Quick Start

### Automatic Provider Selection

```python
from ai_models import get_prompt, get_model

# Auto-select best variant based on model
model = get_model("gpt-6-luna")
prompt = get_prompt("analytics/signal-classification", model=model.id)

# Classify a signal
signal = "App keeps crashing after latest update!"
result = model.classify(prompt.format(signal_text=signal))
```

### Manual Provider Selection

```python
# Explicit provider selection
claude_prompt = get_prompt("analytics/signal-classification", provider="claude")
openai_prompt = get_prompt("analytics/signal-classification", provider="openai")
gemini_prompt = get_prompt("analytics/signal-classification", provider="gemini")
```

### Using with Provider SDK

```python
# Claude with prompt caching
from pm_prompt_toolkit.providers import get_provider

provider = get_provider("claude-haiku", enable_caching=True)
prompt = get_prompt("analytics/signal-classification", provider="claude")
result = provider.classify(prompt, text=signal)
```

## 📈 Performance Metrics

### Accuracy by Provider

| Provider | Model | Accuracy | Notes |
|----------|-------|----------|-------|
| Claude | Haiku 4.5 | 92% | Fast, cost-effective |
| Claude | Sonnet 4.5 | 95% | Best accuracy |
| OpenAI | GPT-4o-mini | 90% | Excellent value |
| OpenAI | GPT-4o | 93% | Balanced |
| Gemini | Flash Lite | 88% | Ultra-low cost |
| Gemini | Flash | 91% | Best for high volume |
| Gemini | Pro | 94% | High accuracy |

_Measured on the previous model lineup; not yet re-run on current models._

### Latency (p95)

| Provider | Model | Latency | Throughput |
|----------|-------|---------|------------|
| Gemini | Flash Lite | 0.4s | 2500/s |
| OpenAI | GPT-4o-mini | 0.6s | 1600/s |
| Claude | Haiku 4.5 | 1.0s | 1000/s |
| Gemini | Flash | 0.7s | 1400/s |
| Claude | Sonnet 4.5 | 1.2s | 800/s |
| OpenAI | GPT-4o | 1.0s | 1000/s |
| Gemini | Pro | 1.3s | 750/s |

_Measured on the previous model lineup; not yet re-run on current models._

### Cost per 1,000 Signals

| Provider | Model | Cost/1K | With Caching | Notes |
|----------|-------|---------|--------------|-------|
| OpenAI | GPT-6 Luna | $0.10 | $0.01 | Lowest cost |
| Claude | Haiku 5.5 | $0.10 | $0.01 | 90% cache rate |
| Gemini | 3.5 Flash-Lite | $0.30 | $0.03 | Ultra-low cost |
| Gemini | 3.8 Flash | $0.75 | $0.075 | High volume |
| Gemini | 4 Argon | $2.00 | $0.10 | Accuracy focus |
| OpenAI | GPT-6.1 Sol | $2.00 | $0.10 | Balanced |
| Claude | Sonnet 5.5 | $2.00 | $0.10 | Best accuracy |

## 🔧 Provider-Specific Features

### Claude Optimizations

✅ **XML Structured Tags**
- Clear category boundaries with XML markup
- Better parsing accuracy for complex signals
- Chain-of-thought reasoning in `<thinking>` tags

✅ **Prompt Caching**
- 90% cost reduction on repeated classifications
- Category definitions cached automatically
- Best for sustained high-volume use

✅ **Advanced Reasoning**
- Explicit thinking steps improve edge case handling
- Better at ambiguous signal classification
- Superior explanation quality

**Use Claude when:**
- Accuracy is critical
- Signals have complex or ambiguous language
- You need detailed reasoning/explanations
- You have sustained high volume (enables caching)

### OpenAI Optimizations

✅ **Function Calling**
- Guaranteed JSON schema compliance
- Structured output validation
- No post-processing needed

✅ **JSON Mode**
- 100% valid JSON responses
- Simpler integration with downstream systems
- Alternative to function calling

✅ **Parallel Tool Execution**
- Process 50-100 signals per API call
- Massive throughput improvements
- Ideal for batch jobs

✅ **Reproducible Results**
- Seed parameter for testing
- Temperature 0.0 for deterministic output
- Consistent classifications

**Use OpenAI when:**
- You need strict JSON schema validation
- Batch processing many signals simultaneously
- Integration with existing OpenAI infrastructure
- Cost-effectiveness is priority (GPT-6 Luna)

### Gemini Optimizations

✅ **1M Token Context Window**
- Process 1000+ signals in single request
- Batch entire day's signals at once
- Massive cost savings through aggregation

✅ **Context Caching**
- 90% cost reduction
- Flash: $0.75 → $0.075 per 1M tokens
- Argon: $2.00 → $0.10 per 1M tokens

✅ **Ultra-Low Cost Models**
- Flash-Lite: $0.30 per 1M input tokens

✅ **Native JSON Schema**
- Built-in structured output validation
- Guaranteed valid JSON
- No function calling overhead

**Use Gemini when:**
- Processing very high volumes (10K+ signals/day)
- Cost is the primary concern
- You can batch signals for processing
- Real-time latency is acceptable

## 🎯 Decision Matrix

### Choose Claude Sonnet 5.5 if:
- Maximum accuracy required
- Budget allows ($2/1K signals)
- Need best reasoning explanations
- Complex/ambiguous signals

### Choose Claude Haiku 5.5 if:
- Good accuracy needed
- Cost-conscious but quality-focused
- Medium to high volume
- Want caching benefits

### Choose GPT-6 Luna if:
- Best cost/accuracy balance ($0.10/1K)
- Need JSON schema validation
- OpenAI infrastructure in place
- Want parallel batch processing

### Choose GPT-6.1 Sol if:
- High accuracy with OpenAI
- Need function calling features
- Budget allows ($2/1K)
- Complex signal types

### Choose Gemini 3.5 Flash-Lite if:
- Ultra-high volume (100K+ signals/day)
- Cost is critical ($0.30/1K)
- Can tolerate slightly lower accuracy
- Real-time processing not required

### Choose Gemini 3.8 Flash if:
- Very high volume (10K+ signals/day)
- Good accuracy needed
- Want to leverage caching ($0.075/1K cached)
- Can batch signals together

### Choose Gemini 4 Argon if:
- High accuracy with Gemini
- Need 1M context for batch processing
- Want caching benefits
- Budget allows ($2/1K)

## 💡 Best Practices

### For High-Volume Production

```python
# Use Gemini 3.8 Flash with caching for best economics
from ai_models import get_prompt
import google.generativeai as genai

# Create cached model (reuse for 1 hour)
cached_content = genai.caching.CachedContent.create(
    model="gemini-3.8-flash",
    system_instruction=get_prompt("analytics/signal-classification", provider="gemini"),
    ttl=datetime.timedelta(hours=1)
)

model = genai.GenerativeModel.from_cached_content(cached_content)

# First 1000 signals: $0.75
# Next 9000 signals: $0.68 (cached)
# Total: $1.43 for 10K signals vs $7.50 without caching
```

### For Accuracy-Critical Applications

```python
# Use Claude Sonnet with chain-of-thought
from pm_prompt_toolkit.providers import get_provider

provider = get_provider("claude-sonnet-5-5", enable_caching=True)
prompt = get_prompt("analytics/signal-classification", provider="claude")

# Get detailed reasoning with high accuracy
result = provider.classify(prompt, text=signal)
```

### For Batch Processing

```python
# Use Gemini's 1M context for massive batches
signals = load_signals()  # 1000 signals

batch_prompt = get_prompt("analytics/signal-classification", provider="gemini")
batch_prompt += f"\n\nClassify these {len(signals)} signals:\n"
for i, signal in enumerate(signals, 1):
    batch_prompt += f"{i}. {signal}\n"

# Single API call for all 1000 signals
response = model.generate_content(batch_prompt)
results = json.loads(response.text)  # Array of 1000 classifications
```

## 📚 Examples

See the individual prompt files for detailed usage examples:
- [Base Prompt](./prompt.md) - Universal examples
- [Claude Examples](./prompt.claude.md) - XML format, caching
- [OpenAI Examples](./prompt.openai.md) - Function calling, batch processing
- [Gemini Examples](./prompt.gemini.md) - Context window, ultra-low cost

## 🔗 Related Prompts

- **Epic Categorization**: For engineering ticket classification
- **Customer Health Scoring**: For expansion/churn prediction
- **Sentiment Analysis**: For deeper emotional analysis

## 📝 Notes

- All variants return the same information (category, confidence, evidence, reasoning)
- Performance metrics based on production data from 100K+ classifications
- Cost estimates include both input and output tokens
- Caching costs assume 90% cache hit rate after warmup
- Accuracy measured against human expert classifications
