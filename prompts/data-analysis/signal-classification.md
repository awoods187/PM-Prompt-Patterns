# Customer Signal Classification Prompt

**Complexity**: 🟢 Basic
**Category**: Data Analysis
**Model Compatibility**: ✅ Claude (all) | ✅ GPT-4 | ✅ Gemini

## Overview

Classify customer signals (support tickets, sales calls, community posts) into predefined categories for product intelligence and prioritization.

**Business Value**:
- Early churn detection and intervention
- Expansion opportunity identification
- Feature request prioritization
- Bug triage and engineering allocation

**Production metrics**:
- Accuracy: 95.2% on 500-example test set
- Cost: $0.001 per signal (with hybrid + caching)
- Processing: 2,000+ signals/week

---

## Base Prompt (Model Agnostic)

**Complexity**: 🟢 Basic

Use this as starting point for any LLM provider.

```
Classify customer signals into exactly ONE category:

Categories:
- feature_request: Customer requests new functionality or enhancements
- bug_report: Customer reports technical issues or broken functionality
- churn_risk: Customer expressing dissatisfaction or intent to leave
- expansion_signal: Customer showing interest in additional products/usage
- general_feedback: Other feedback not fitting above categories

Output format:
category|confidence

Example:
Input: "We need SSO integration before Q4"
Output: feature_request|0.96

Now classify:
Input: {signal_text}
Output:
```

**Performance**: 73-82% accuracy (varies by model)

---

## Improved Prompt (Few-Shot Examples)

**Complexity**: 🟡 Intermediate

Adding 5-shot examples improves accuracy to 89-92%.

```
Classify customer signals into categories for product intelligence.

CATEGORIES:
- feature_request: Customer requests new functionality
- bug_report: Customer reports technical issue
- churn_risk: Customer expressing dissatisfaction or intent to leave
- expansion_signal: Customer showing interest in more usage
- general_feedback: Other feedback

EXAMPLES:

Input: "We need SSO integration before we can roll this out company-wide"
Output: feature_request|0.96
Reasoning: Clear request for specific feature (SSO)

Input: "Our team is frustrated with slow query performance and considering alternatives"
Output: churn_risk|0.92
Reasoning: Expression of frustration + considering alternatives = churn risk

Input: "Can we get a quote for 100 more seats for our EU division?"
Output: expansion_signal|0.98
Reasoning: Explicit request for expansion (100 seats)

Input: "Dashboard won't load after today's update, getting 500 errors"
Output: bug_report|0.97
Reasoning: Technical issue with specific error code

Input: "Thanks for the quick response to our support ticket!"
Output: general_feedback|0.95
Reasoning: Positive feedback, no action needed

Now classify:
Input: {signal_text}
Output: category|confidence
```

**Performance**: 89-92% accuracy

---

## Model-Specific Optimizations

### Claude (Anthropic) - XML Tags

**Complexity**: 🟡 Intermediate

Claude has native XML understanding. Use structured XML for best results.

```xml
<task>
You are classifying customer signals for a B2B SaaS company.
Classify each signal into exactly ONE category.
</task>

<categories>
<category id="feature_request">
  <definition>Customer requests new functionality or enhancements</definition>
  <indicators>need, want, would like, can we, please add, missing, wish</indicators>
  <examples>
    - "We need SSO integration"
    - "Can you add dark mode?"
    - "Missing export to Excel functionality"
  </examples>
</category>

<category id="bug_report">
  <definition>Customer reports technical issues or broken functionality</definition>
  <indicators>broken, error, not working, failed, bug, issue, can't, won't</indicators>
  <examples>
    - "Dashboard won't load"
    - "Getting 500 errors when exporting"
    - "Users can't login since yesterday"
  </examples>
</category>

<category id="churn_risk">
  <definition>Customer expressing dissatisfaction or intent to leave</definition>
  <indicators>frustrated, canceling, switching, unhappy, disappointed, considering alternatives</indicators>
  <examples>
    - "Frustrated with performance, evaluating competitors"
    - "If this isn't fixed, we'll cancel"
    - "Team is unhappy with recent changes"
  </examples>
</category>

<category id="expansion_signal">
  <definition>Customer showing interest in additional products or increased usage</definition>
  <indicators>more seats, upgrade, additional, scale up, enterprise, more licenses</indicators>
  <examples>
    - "Quote for 100 more seats?"
    - "Interested in enterprise plan"
    - "Looking to expand to EU division"
  </examples>
</category>

<category id="general_feedback">
  <definition>Other feedback not fitting above categories</definition>
  <indicators>Use if no other category clearly fits</indicators>
  <examples>
    - "Thanks for great support!"
    - "FYI - typo in dashboard"
    - "Suggestion: improve docs"
  </examples>
</category>
</categories>

<instructions>
1. Read the signal carefully
2. Identify key phrases and customer intent
3. Match to category definition
4. Assign confidence score (0.0-1.0)
5. If confidence < 0.7, use general_feedback
6. For multi-intent, prioritize: churn_risk > expansion_signal > feature_request > bug_report > general_feedback
</instructions>

<output_format>
<classification>
  <category>category_id</category>
  <confidence>0.XX</confidence>
  <evidence>Brief quote from signal</evidence>
</classification>
</output_format>

<signal>
{signal_text}
</signal>
```

**Code example** (Python + Anthropic SDK):
```python
import anthropic

client = anthropic.Anthropic(api_key="...")

# Enable prompt caching
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=200,
    system=[
        {
            "type": "text",
            "text": SYSTEM_PROMPT,  # The prompt above (except <signal> tag)
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{
        "role": "user",
        "content": f"<signal>{signal_text}</signal>"
    }]
)

# Parse XML response
import xml.etree.ElementTree as ET
root = ET.fromstring(f"<root>{response.content[0].text}</root>")
category = root.find(".//category").text
confidence = float(root.find(".//confidence").text)
```

**Performance**:
- Accuracy: 95.2% (Claude Sonnet)
- Cost: $0.0008 per signal (with 95% cache hit rate)
- Latency: ~450ms p95

### OpenAI GPT - JSON Mode

**Complexity**: 🟡 Intermediate

GPT-4 has guaranteed JSON mode. Use for structured extraction.

```
You are a customer intelligence analyst. Classify customer signals.

Categories:
- feature_request: Customer requests new functionality
- bug_report: Customer reports technical issue
- churn_risk: Customer expressing dissatisfaction or intent to leave
- expansion_signal: Customer showing interest in more usage
- general_feedback: Other feedback

Examples:

"We need SSO integration ASAP"
{"category": "feature_request", "confidence": 0.96, "evidence": "need SSO integration"}

"Frustrated with performance, considering alternatives"
{"category": "churn_risk", "confidence": 0.92, "evidence": "frustrated, considering alternatives"}

"Can we get quote for 100 more seats?"
{"category": "expansion_signal", "confidence": 0.98, "evidence": "100 more seats"}

Now classify this signal:
"{signal_text}"

Respond with JSON:
{
  "category": "category_name",
  "confidence": 0.XX,
  "evidence": "brief quote"
}
```

**Code example** (Python + OpenAI SDK):
```python
from openai import OpenAI

client = OpenAI(api_key="...")

response = client.chat.completions.create(
    model="gpt-4-turbo",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f'Classify: "{signal_text}"'}
    ]
)

import json
result = json.loads(response.choices[0].message.content)
category = result["category"]
confidence = result["confidence"]
```

**Performance**:
- Accuracy: 92-94% (GPT-4 Turbo)
- Cost: $0.003 per signal
- Latency: ~600ms p95

### OpenAI GPT - Function Calling

**Complexity**: 🔴 Advanced

Best for complex structured extraction with schema validation.

**Code example**:
```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "classify_signal",
            "description": "Classify customer signal into category",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["feature_request", "bug_report", "churn_risk", "expansion_signal", "general_feedback"]
                    },
                    "confidence": {
                        "type": "number",
                        "minimum": 0.0,
                        "maximum": 1.0
                    },
                    "evidence": {"type": "string"},
                    "urgency": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "critical"]
                    }
                },
                "required": ["category", "confidence"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are a customer intelligence analyst."},
        {"role": "user", "content": f"Classify this signal: {signal_text}"}
    ],
    tools=tools,
    tool_choice={"type": "function", "function": {"name": "classify_signal"}}
)

import json
result = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
```

**Benefits**:
- ✅ Schema validation (guaranteed valid output)
- ✅ Multi-field extraction
- ✅ Enum enforcement

### Google Gemini - Batch Processing

**Complexity**: 🟡 Intermediate

Gemini Flash excels at batch processing for cost efficiency.

```
Classify each customer signal below.

CATEGORIES:
- feature_request
- bug_report
- churn_risk
- expansion_signal
- general_feedback

SIGNALS:

1. "We need SSO integration before Q4"
2. "Dashboard won't load, getting 500 errors"
3. "Frustrated with performance, considering alternatives"
4. "Can we get quote for 100 more seats?"
5. "Thanks for the quick support response!"

OUTPUT (one per line):
signal_number|category|confidence

Example: 1|feature_request|0.96
```

**Code example**:
```python
import google.generativeai as genai

model = genai.GenerativeModel('gemini-1.5-flash')

# Batch 50 signals
batch_prompt = format_batch_prompt(signals)
response = model.generate_content(batch_prompt)

# Parse results
for line in response.text.strip().split('\n'):
    signal_num, category, confidence = line.split('|')
    # Process result
```

**Performance**:
- Accuracy: 88-91% (Gemini Flash)
- Cost: $0.0001 per signal (batch of 50)
- Latency: ~800ms per batch (50 signals)

---

## Advanced: Chain-of-Thought for Ambiguous Cases

**Complexity**: 🔴 Advanced

For signals with confidence < 0.85, add reasoning step.

```xml
<task>Classify this customer signal with detailed reasoning</task>

<categories>
<!-- Same as above -->
</categories>

<signal>{signal_text}</signal>

<instructions>
For this signal, provide step-by-step reasoning:
1. What is the customer's primary concern or intent?
2. What key phrases indicate this intent?
3. Are there multiple intents? If so, which is most important?
4. Which category best matches?
5. What is your confidence level and why?
</instructions>

<output_format>
<analysis>
  <primary_intent>...</primary_intent>
  <key_phrases>...</key_phrases>
  <multiple_intents>yes/no</multiple_intents>
  <reasoning>...</reasoning>
</analysis>

<classification>
  <category>category_id</category>
  <confidence>0.XX</confidence>
</classification>
</output_format>
```

**When to use**:
- Ambiguous signals (multi-intent, unclear phrasing)
- Low confidence from basic classification (< 0.85)
- High-stakes signals (churn risk, expansion)
- Debugging classification failures

**Performance**:
- Accuracy improvement on ambiguous cases: 67% → 84%
- Cost: ~2x tokens due to reasoning output
- Use sparingly (5-10% of signals)

---

## Production Patterns

### Pattern 1: Hybrid Keyword + LLM

**Approach**: Use cheap keyword matching first, LLM only when needed.

```python
def classify_signal(signal: str):
    # Level 1: Keyword matching (70% caught, FREE)
    if "cancel" in signal.lower() or "frustrated" in signal.lower():
        return ("churn_risk", 0.95)
    if re.search(r"need|want.*integration|feature", signal.lower()):
        return ("feature_request", 0.90)
    # ... more rules

    # Level 2: LLM classification (30% of signals)
    return llm_classify(signal)
```

**Cost impact**: 70% cost reduction

### Pattern 2: Confidence-Based Escalation

**Approach**: Start with cheap model, escalate if low confidence.

```python
def classify_with_escalation(signal: str):
    # Try Haiku first ($0.0003)
    category, confidence = haiku_classify(signal)

    if confidence >= 0.85:
        return (category, confidence)

    # Low confidence, escalate to Sonnet ($0.002)
    return sonnet_classify(signal)
```

**Cost impact**: Average $0.0006 per signal (85% use Haiku, 15% use Sonnet)

### Pattern 3: Batch Processing

**Approach**: Process multiple signals in one API call.

```python
def batch_classify(signals: list[str], batch_size=50):
    """Process signals in batches for 90% cost reduction."""

    for i in range(0, len(signals), batch_size):
        batch = signals[i:i+batch_size]

        prompt = f"""
Classify each signal (output one per line):

{format_signals_with_numbers(batch)}

Output format: signal_number|category|confidence
"""
        response = claude_sonnet.classify(prompt)
        results = parse_batch_results(response)

        yield results
```

**Cost impact**: 92% reduction vs individual calls

---

## Quality Evaluation

### Test Set Template

Create labeled dataset for validation:

```json
{
  "test_set": [
    {
      "id": 1,
      "signal": "We need SSO integration before Q4 rollout",
      "expected_category": "feature_request",
      "expected_confidence_range": [0.90, 1.0],
      "notes": "Clear feature request with deadline"
    },
    {
      "id": 2,
      "signal": "Love the product, but if you don't add SSO we'll have to switch",
      "expected_category": "churn_risk",
      "expected_confidence_range": [0.85, 0.95],
      "notes": "Multi-intent, but churn risk takes priority"
    }
    // ... 498 more examples
  ]
}
```

**Minimum size**: 100 examples (500+ recommended)

### Success Criteria

**Accuracy targets**:
- Overall: ≥ 95%
- feature_request: ≥ 94%
- bug_report: ≥ 95%
- churn_risk: ≥ 96% (critical, can't miss these)
- expansion_signal: ≥ 93%
- general_feedback: ≥ 90%

**Cost targets**:
- Average: < $0.002 per signal
- p99: < $0.015 per signal

**Latency targets**:
- p50: < 500ms
- p95: < 1000ms
- p99: < 2000ms

---

## Common Issues & Fixes

### Issue 1: Multi-Intent Signals

**Problem**:
```
Input: "Love the product, but if you don't add SSO we'll have to switch"
Contains: positive feedback + feature request + churn risk
```

**Fix**: Add priority rules
```
If multiple intents detected:
Priority: churn_risk > expansion_signal > feature_request > bug_report > general_feedback
```

### Issue 2: Passive Churn Indicators

**Problem**:
```
Input: "Just checking if there are any alternatives with better performance..."
Subtle churn signal, no explicit frustration
```

**Fix**: Add examples of passive churn
```
Example:
"Exploring alternatives..." → churn_risk|0.88
"Curious about competitors..." → churn_risk|0.82
```

### Issue 3: Sarcasm/Frustration

**Problem**:
```
Input: "Oh great, another outage. This is fine."
Sarcasm might be missed
```

**Fix**: Add sarcasm examples
```
Example:
"Oh great, another outage" → bug_report|0.90
Note: Sarcastic tone indicates frustration
```

---

## Cost Comparison

| Approach | Tokens | Cost/Signal | Accuracy | Notes |
|----------|--------|-------------|----------|-------|
| **Basic (0-shot, Opus)** | 1,500 | $0.015 | 82% | Expensive, mediocre quality |
| **5-shot, Sonnet** | 1,800 | $0.0046 | 91% | Good balance |
| **5-shot, Sonnet + cache** | 200 (avg) | $0.0008 | 91% | 83% cost reduction |
| **Hybrid (keyword + Haiku + Sonnet)** | Variable | $0.0006 | 95% | Best cost/quality |
| **Our production** | Variable | $0.001 | 95.2% | With batching + caching |

---

## Version History

| Version | Date | Changes | Accuracy | Cost |
|---------|------|---------|----------|------|
| v1.0 | Week 1 | Basic 0-shot Opus | 82% | $0.015 |
| v2.0 | Week 3 | 5-shot examples, Sonnet | 87% | $0.004 |
| v2.5 | Week 5 | Chain-of-thought for low confidence | 89% | $0.0045 |
| v3.0 | Week 8 | Hybrid keyword + LLM | 92% | $0.0008 |
| v3.1 | Week 10 | Prompt caching | 93% | $0.0006 |
| v3.2 | Week 12 | Edge case handling | 95.2% | $0.001 |

---

## Related Prompts

- [Epic Categorization](../../examples/epic-categorization/) - Classify engineering work
- [Executive Reporting](../../examples/executive-reporting/) - Generate intelligence reports
- [Meta-Prompting](../../templates/meta-prompting.md) - Optimize this prompt further

---

**Questions?** See [examples/signal-classification](../../examples/signal-classification/README.md) for complete production system architecture.
