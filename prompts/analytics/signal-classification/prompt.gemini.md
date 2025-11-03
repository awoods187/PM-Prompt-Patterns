# Customer Signal Classification - Gemini Optimized

**Category**: Analytics / Classification
**Complexity**: 🟡 Moderate
**Model Compatibility**: Gemini 2.5 Pro, Gemini 2.5 Flash, Gemini 2.5 Flash Lite

## Gemini-Specific Optimizations

- **Context Caching**: 90% cost reduction on repeated prompts
- **2M Token Context**: Process 1000+ signals in single request
- **JSON Schema**: Native structured output validation
- **Best Models**: Gemini 2.5 Flash Lite (ultra-low cost), Flash (balanced), Pro (accuracy)

## System Instruction (Cacheable)

```
You are an expert customer signal classification system with deep expertise in SaaS customer success patterns, product feedback analysis, and churn prediction.

Your specialized knowledge includes:
- Pattern recognition in customer communication
- Early warning signs of churn risk
- Identifying expansion opportunities
- Technical issue vs. feature request disambiguation
- Sentiment analysis and severity assessment

## Classification Framework

### Category Definitions

**FEATURE_REQUEST** - Customer wants new functionality
Indicators:
- Constructive suggestions for product improvements
- Missing functionality that would add value
- Enhancement requests for existing features
- Keywords: "would be great if", "wish", "need", "can you add", "enhancement", "improvement"

**BUG_REPORT** - Something is broken or not working as expected
Indicators:
- Technical failures or errors
- Unexpected behavior or malfunctions
- Recent regressions after updates
- Keywords: "error", "broken", "crash", "doesn't work", "bug", "glitch", "not working", "failed"

**CHURN_RISK** - Customer expressing dissatisfaction or intent to leave
Indicators:
- Explicit or implicit cancellation intent
- Extreme frustration or disappointment
- Mention of competitors or alternatives
- Keywords: "cancel", "disappointed", "frustrated", "switching to", "alternative", "unsubscribe", "competitor"

**EXPANSION_SIGNAL** - Customer showing growth or upsell potential
Indicators:
- Business growth requiring more capacity
- Request for higher-tier features
- Team expansion or new use cases
- Keywords: "upgrade", "more users", "enterprise", "team plan", "additional seats", "scale up", "expand"

**GENERAL_FEEDBACK** - General comments, praise, questions, or neutral feedback
Indicators:
- Positive feedback without specific requests
- General questions about usage
- Neutral observations
- Doesn't fit other high-priority categories

### Priority Rules

When multiple categories apply, use this priority ordering (highest to lowest):
1. **CHURN_RISK** - Immediate retention risk, requires urgent action
2. **EXPANSION_SIGNAL** - Revenue growth opportunity
3. **BUG_REPORT** - Product quality issue affecting user experience
4. **FEATURE_REQUEST** - Product enhancement opportunity
5. **GENERAL_FEEDBACK** - General communication, lowest priority

### Classification Process

For each signal, analyze in this order:
1. Extract key phrases and sentiment indicators
2. Identify category based on strongest indicators
3. Calculate confidence based on signal clarity and keyword strength
4. Determine severity for actionable categories
5. Provide evidence and reasoning

## Response Schema

Always respond with valid JSON matching this exact schema:

{
  "category": "string (one of the five categories)",
  "confidence": "number (0.0 to 1.0)",
  "evidence": ["array", "of", "key", "phrases"],
  "reasoning": "string (clear explanation)",
  "severity": "string (low|medium|high|critical) - for BUG_REPORT and CHURN_RISK",
  "suggested_action": "string (optional recommended next step)",
  "processing_time_ms": "number (optional)"
}
```

## Generation Config

```python
import google.generativeai as genai

generation_config = {
    "temperature": 0.1,  # Low temperature for consistent classification
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 500,
    "response_mime_type": "application/json",
    "response_schema": {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "enum": [
                    "FEATURE_REQUEST",
                    "BUG_REPORT",
                    "CHURN_RISK",
                    "EXPANSION_SIGNAL",
                    "GENERAL_FEEDBACK"
                ]
            },
            "confidence": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0
            },
            "evidence": {
                "type": "array",
                "items": {"type": "string"}
            },
            "reasoning": {"type": "string"},
            "severity": {
                "type": "string",
                "enum": ["low", "medium", "high", "critical"]
            },
            "suggested_action": {"type": "string"}
        },
        "required": ["category", "confidence", "evidence", "reasoning"]
    }
}
```

## Usage Example (Single Signal)

```python
import google.generativeai as genai
from ai_models import get_prompt

# Configure API
genai.configure(api_key="your-api-key")

# Load Gemini-optimized prompt
system_instruction = get_prompt(
    "analytics/signal-classification",
    provider="gemini"
)

# Create model with configuration
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config,
    system_instruction=system_instruction
)

# Classify signal
signal = "Dashboard completely broken after update! Can't access any reports!"
response = model.generate_content(f"Classify this signal: {signal}")

# Parse JSON result
import json
classification = json.loads(response.text)
```

## Context Caching (90% Cost Savings)

```python
# Create cached content with system instruction and examples
cached_content = genai.caching.CachedContent.create(
    model="gemini-2.5-flash",
    display_name="signal-classification-cache",
    system_instruction=system_instruction,
    ttl=datetime.timedelta(hours=1)  # Cache for 1 hour
)

# Use cached model for subsequent requests
model = genai.GenerativeModel.from_cached_content(
    cached_content=cached_content,
    generation_config=generation_config
)

# First classification: $0.075/1M input tokens
# Subsequent classifications: $0.019/1M input tokens (74% savings!)
for signal in signals:
    classification = model.generate_content(signal)
```

## Batch Processing (2M Token Context)

```python
# Process up to 1000 signals in a single request
signals_batch = [
    "Signal 1: App keeps crashing...",
    "Signal 2: Love the new features!",
    "Signal 3: Need SSO integration...",
    # ... up to 1000 signals
]

# Format as single prompt
batch_prompt = "Classify each of the following signals:\n\n"
for i, signal in enumerate(signals_batch, 1):
    batch_prompt += f"{i}. {signal}\n"

batch_prompt += "\nProvide an array of classifications in JSON format."

# Single API call for entire batch
response = model.generate_content(batch_prompt)
classifications = json.loads(response.text)

# Cost: ~$0.10 for 1000 signals with Flash
# vs. $100+ with traditional per-signal approach
```

## Model Selection by Volume

```python
def select_gemini_model(volume: int, latency_sensitive: bool):
    """Select optimal Gemini model based on requirements."""

    if latency_sensitive and volume < 10_000:
        # Ultra-fast, lowest cost
        return "gemini-2.5-flash-lite"  # $0.038/$0.15 per 1M

    elif volume > 100_000:
        # High volume, batch processing
        return "gemini-2.5-flash"  # $0.075/$0.30 per 1M

    else:
        # Highest accuracy for moderate volume
        return "gemini-2.5-pro"  # $1.25/$5.00 per 1M
```

## Expected Output

```json
{
  "category": "BUG_REPORT",
  "confidence": 0.97,
  "evidence": [
    "Dashboard completely broken",
    "after update",
    "Can't access any reports"
  ],
  "reasoning": "This is clearly a technical malfunction. The words 'completely broken' and 'can't access' indicate a bug rather than a feature request. The temporal marker 'after update' suggests a regression. High confidence due to unambiguous language.",
  "severity": "critical",
  "suggested_action": "Immediate escalation to engineering. Check deployment logs from recent update. Contact customer with ETA for fix."
}
```

## Gemini-Specific Performance

| Model | Accuracy | Latency | Cost/1K | Best For |
|-------|----------|---------|---------|----------|
| **Flash Lite** | 85-88% | 0.3-0.5s | $0.0001 | Ultra-high volume, real-time |
| **Flash** | 88-91% | 0.5-0.8s | $0.0002 | Balanced performance/cost |
| **Pro** | 91-94% | 0.8-1.5s | $0.003 | Highest accuracy, complex cases |

## Cost Comparison

```python
# Example: 10,000 signals/day

# Without caching:
# - Flash: 10K * $0.0002 = $2.00/day
# - Pro: 10K * $0.003 = $30.00/day

# With caching (90% cached):
# - Flash: (10K * 0.1 * $0.0002) + (10K * 0.9 * $0.000038) = $0.54/day (73% savings!)
# - Pro: (10K * 0.1 * $0.003) + (10K * 0.9 * $0.00031) = $5.79/day (81% savings!)
```

## Streaming for Real-Time Processing

```python
# Stream results for immediate processing
for chunk in model.generate_content(signal, stream=True):
    partial_result = chunk.text
    # Process incrementally as JSON builds
```

## Error Handling

```python
try:
    response = model.generate_content(signal)
    classification = json.loads(response.text)

    # Validate schema
    assert "category" in classification
    assert classification["confidence"] >= 0.0 and classification["confidence"] <= 1.0

except (json.JSONDecodeError, AssertionError, Exception) as e:
    # Fallback classification
    classification = {
        "category": "GENERAL_FEEDBACK",
        "confidence": 0.2,
        "evidence": ["Error parsing response"],
        "reasoning": f"Classification failed: {str(e)}",
        "severity": "low"
    }
```

## Notes

- **Context caching** is killer feature - 90% cost reduction for repeated use
- **2M token context** enables massive batch processing (1000+ signals per request)
- **Flash Lite** is incredibly cost-effective for high-volume classification
- **JSON schema** guarantees valid structured output
- **Streaming** enables real-time processing for immediate routing
- Gemini excels at pattern recognition across large batches
- Cost per classification as low as $0.0001 with Flash Lite
