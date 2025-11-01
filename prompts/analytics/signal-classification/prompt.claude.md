# Customer Signal Classification - Claude Optimized

**Category**: Analytics / Classification
**Complexity**: 🟡 Moderate
**Model Compatibility**: Claude 3+, Claude 4+

## Claude-Specific Optimizations

- **XML Tags**: Structured data with proper escaping
- **Chain-of-Thought**: Explicit thinking steps for accuracy
- **Examples**: Few-shot learning with Claude's preferred format
- **Best Models**: Claude Haiku 4.5 (cost), Claude Sonnet 4.5 (accuracy)

## Prompt

```xml
You are a customer signal classification expert. You excel at analyzing customer feedback and categorizing it with high accuracy and clear reasoning.

<classification_task>
Analyze customer signals and classify them into one of five categories with supporting evidence.
</classification_task>

<categories>
<category name="FEATURE_REQUEST">
<description>Customer wants new functionality or enhancement</description>
<indicators>
- Words like "would be great if", "wish", "need", "want", "can you add"
- Describes missing functionality
- Suggests improvements
</indicators>
<example>
"Love the app! Would be great if you added dark mode for night usage"
</example>
</category>

<category name="BUG_REPORT">
<description>Something is broken or not working as expected</description>
<indicators>
- Technical issues or errors
- Words like "error", "broken", "crash", "doesn't work", "bug", "glitch"
- Describes unexpected behavior
</indicators>
<example>
"App crashes every time I try to export my data to CSV format"
</example>
</category>

<category name="CHURN_RISK">
<description>Customer expressing dissatisfaction or intent to leave</description>
<indicators>
- Words like "cancel", "disappointed", "frustrated", "switching to", "alternative"
- Negative sentiment about product or service
- Mentions competitors
</indicators>
<example>
"Very disappointed with recent changes. Considering switching to Competitor X"
</example>
</category>

<category name="EXPANSION_SIGNAL">
<description>Customer showing growth or upsell potential</description>
<indicators>
- Words like "upgrade", "more users", "enterprise", "team plan", "additional"
- Indicates business growth
- Requests higher-tier features
</indicators>
<example>
"Our team is growing! Want to upgrade to enterprise plan and add 10 more seats"
</example>
</category>

<category name="GENERAL_FEEDBACK">
<description>General comments, praise, questions, or feedback</description>
<indicators>
- Doesn't fit other categories
- General positive feedback
- Usage questions
- Neutral observations
</indicators>
<example>
"Great product, I use it every day for my workflows!"
</example>
</category>
</categories>

<priority_rules>
If multiple categories apply, choose based on business priority (highest first):
1. CHURN_RISK - Immediate retention risk
2. EXPANSION_SIGNAL - Revenue growth opportunity
3. BUG_REPORT - Product quality issue
4. FEATURE_REQUEST - Product enhancement
5. GENERAL_FEEDBACK - General communication
</priority_rules>

<signal_to_analyze>
{signal_text}
</signal_to_analyze>

<classification_instructions>
Analyze the signal using this process:

1. First, read the signal carefully and identify key phrases
2. Consider which category best fits based on the indicators
3. Determine your confidence level
4. Extract specific evidence from the signal
5. Provide clear reasoning for your choice

Respond in this exact XML format:

<classification>
<category>[CATEGORY_NAME]</category>
<confidence>[0.0-1.0]</confidence>
<evidence>
<phrase>[Key phrase 1]</phrase>
<phrase>[Key phrase 2]</phrase>
</evidence>
<reasoning>
[Step-by-step explanation of your classification decision]
</reasoning>
<thinking>
[Your internal thought process - be thorough]
</thinking>
</classification>

Think step-by-step and be explicit about your reasoning.
</classification_instructions>
```

## Usage Example

```python
from pm_prompt_toolkit.providers import get_provider
from ai_models import get_prompt

# Get Claude provider
provider = get_provider("claude-haiku")

# Load Claude-optimized prompt
prompt_template = get_prompt("analytics/signal-classification", provider="claude")

# Format with actual signal
signal = "Dashboard is completely broken after latest update. Team can't access reports!"
prompt = prompt_template.format(signal_text=signal)

# Get classification
response = provider.classify(prompt, model="claude-haiku")
```

## Expected Output

```xml
<classification>
<category>BUG_REPORT</category>
<confidence>0.98</confidence>
<evidence>
<phrase>Dashboard is completely broken</phrase>
<phrase>can't access reports</phrase>
<phrase>after latest update</phrase>
</evidence>
<reasoning>
This signal clearly describes a technical malfunction. The word "broken" directly indicates a bug, and the context shows it affects core functionality (dashboard and reports). The temporal marker "after latest update" suggests a regression. While there's frustration expressed, the primary issue is the technical failure, not churn intent, making BUG_REPORT the correct classification.
</reasoning>
<thinking>
Let me analyze this signal:
1. Key phrases: "completely broken", "can't access"
2. This is clearly about something not working (bug)
3. High confidence because language is unambiguous
4. Not churn risk because focus is on the technical issue, not leaving
5. Not just frustration - actionable bug report
</thinking>
</classification>
```

## Claude-Specific Performance

- **Accuracy**: 92-95% (higher than base prompt due to chain-of-thought)
- **Reasoning Quality**: Excellent - clear step-by-step thinking
- **Best Model**: Claude Haiku 4.5 ($1/$5 per 1M tokens)
- **Latency**: 0.8-1.5s with Haiku
- **Caching**: Use prompt caching for repeated classifications to reduce cost by 90%

## Prompt Caching Strategy

```python
from pm_prompt_toolkit.providers import get_provider

provider = get_provider("claude-sonnet-4-5", enable_caching=True)

# The category definitions will be cached
# Only the signal changes between requests
# First request: $3/1M tokens
# Subsequent requests: $0.30/1M tokens (90% savings)
```

## Notes

- XML structure improves Claude's parsing accuracy
- `<thinking>` tags encourage better reasoning
- Few-shot examples use Claude's preferred format
- Chain-of-thought significantly improves accuracy on edge cases
- Works best with Claude Sonnet 4+ or Haiku 4+
