# Remove AI Writing Patterns - OpenAI Optimized

> Extends `prompt.md` with OpenAI-specific optimizations

## System Prompt

```
Analyze the following text for common AI-generated writing patterns and provide specific diffs to fix them.

Focus on these patterns:

1. "It's not X, it's Y" constructions
   - Pattern: "This isn't just about X—it's about Y"
   - Fix: Direct statements without negation framing

2. Excessive em-dashes (—)
   - Pattern: Overuse of em-dashes for emphasis or explanation
   - Fix: Replace with periods, colons, or remove entirely
   - Target: Use em-dashes sparingly (1-2 per 1000 words max)

3. AI hedge words
   - Pattern: "remarkably," "particularly," "essentially," "effectively"
   - Fix: Remove or replace with stronger, specific words

4. "Here's the X part" constructions
   - Pattern: "But here's the interesting/remarkable/important part:"
   - Fix: State the point directly without meta-commentary

5. Listicle intro patterns
   - Pattern: "What X knew that I didn't:", "Here's what happened:"
   - Fix: More direct transitions

Output format:
- List each instance found with line/paragraph reference
- Provide before/after diff for each
- Explain why the change improves readability
- Count total instances of each pattern
- Suggest 2-3 alternative phrasings when helpful

Goal: Make writing sound more human, confident, and direct while preserving meaning and tone.

---

[PASTE YOUR CONTENT HERE]

---
```

## OpenAI Optimizations Applied

- **Clear role definition**: Explicit system message with role and responsibilities
- **Structured output**: Consistent formatting instructions
- **Function calling ready**: Can be combined with function schemas for structured output
- **Concise directives**: Optimized for GPT-4's instruction-following capabilities

## Usage

```python
from pm_prompt_toolkit.providers import get_provider

# Initialize OpenAI provider
provider = get_provider("gpt-4o")

result = provider.generate(
    system_prompt="<prompt from above>",
    user_message="<your content here>"
)
```

## Model Recommendations

- **gpt-4o**: Best balance of speed, quality, and cost for most use cases
- **gpt-4o-mini**: Faster and more cost-effective for simpler tasks
- **gpt-4-turbo**: Use for extended context needs (>128k tokens)

## See Also

- Base prompt: `prompt.md` (examples, testing checklist, business value)
- Provider documentation: `../../docs/provider-specific-prompts.md`
