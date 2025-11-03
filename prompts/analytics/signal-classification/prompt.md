# Customer Signal Classification

**Category**: Analytics / Classification
**Complexity**: 🟡 Moderate
**Model Compatibility**: Universal (all providers)

## Overview

Classify customer feedback, support tickets, and product signals into standardized categories for prioritization and routing. This prompt uses a structured classification approach suitable for any LLM provider.

## Prompt

```
You are a customer signal classification system. Your task is to analyze customer feedback and categorize it accurately.

## Classification Categories

1. **FEATURE_REQUEST**: Customer wants new functionality
   - Keywords: "would be great if", "wish", "need", "want", "can you add"
   - Examples: "Love the app! Would be great if you added dark mode"

2. **BUG_REPORT**: Something is broken or not working as expected
   - Keywords: "error", "broken", "crash", "doesn't work", "bug"
   - Examples: "App crashes when I try to export data"

3. **CHURN_RISK**: Customer expressing dissatisfaction or intent to leave
   - Keywords: "cancel", "disappointed", "frustrated", "switching to", "alternative"
   - Examples: "Very disappointed with recent changes, considering alternatives"

4. **EXPANSION_SIGNAL**: Customer showing growth or upsell potential
   - Keywords: "upgrade", "more users", "enterprise", "team plan", "additional"
   - Examples: "Want to upgrade to team plan and add 5 more users"

5. **GENERAL_FEEDBACK**: General comments, praise, or questions
   - Catch-all for signals that don't fit other categories
   - Examples: "Great product, using it daily!"

## Task

Analyze the following customer signal and classify it:

**Signal**: {signal_text}

Provide your classification in this format:

Category: [CATEGORY_NAME]
Confidence: [0.0-1.0]
Evidence: [Key phrases that support your classification]
Reasoning: [Brief explanation of why this category was chosen]

## Guidelines

- Choose the SINGLE most appropriate category
- Confidence should reflect how certain you are (0.0 = uncertain, 1.0 = very certain)
- Evidence should quote specific phrases from the signal
- If multiple categories apply, choose the one with highest business priority:
  1. CHURN_RISK (highest priority)
  2. EXPANSION_SIGNAL
  3. BUG_REPORT
  4. FEATURE_REQUEST
  5. GENERAL_FEEDBACK (lowest priority)
```

## Usage Example

```python
from ai_models import get_model, get_prompt

# Load prompt and model
model = get_model("claude-haiku")
prompt_template = get_prompt("analytics/signal-classification")

# Format with actual signal
signal = "App keeps crashing on iOS 17, very frustrating!"
prompt = prompt_template.format(signal_text=signal)

# Get classification
response = model.classify(prompt)
```

## Expected Output

```
Category: BUG_REPORT
Confidence: 0.95
Evidence: "App keeps crashing", "very frustrating"
Reasoning: Clear technical issue reported with strong negative sentiment. The word "crashing" indicates a bug, and "very frustrating" shows user impact.
```

## Performance Characteristics

- **Accuracy**: 85-92% depending on model
- **Latency**: 0.5-2s typical response time
- **Cost**: $0.0001-0.001 per classification (model dependent)
- **Batch Processing**: Can classify 100+ signals in parallel

## Notes

- This is a base prompt optimized for clarity and compatibility
- Provider-specific variants offer additional optimizations:
  - `prompt.claude.md`: XML tags, chain-of-thought
  - `prompt.openai.md`: Function calling, JSON mode
  - `prompt.gemini.md`: Context caching, batch processing
- Use confidence scores to route uncertain cases for human review
- Adjust category priority based on your business needs
