# Remove AI Writing Patterns - Gemini Optimized

> Extends `prompt.md` with Gemini-specific optimizations

## System Instruction

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

6. Bolded list lead-ins
   - Pattern: "* **Performance**: Improved through caching"
   - Pattern: "* **Key benefit**: Reduces latency"
   - Fix: Remove bolding and integrate naturally into the bullet point
   - Or: Rewrite to avoid the colon structure entirely
   - Example: Change "* **Performance**: Improved through caching" to "* Caching improves performance"
   - Avoid formulaic "[Category]:[Description]" structure

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

## Gemini Optimizations Applied

- **Clear directives**: Explicit, numbered instructions for better instruction-following
- **Context utilization**: Optimized for Gemini's large context window
- **Multimodal ready**: Can process code alongside diagrams, screenshots, or other media
- **Structured reasoning**: Step-by-step breakdown for complex analysis tasks

## Usage

```python
from pm_prompt_toolkit.providers import get_provider

# Initialize Gemini provider
provider = get_provider("gemini-2.0-flash-exp")

result = provider.generate(
    system_instruction="<prompt from above>",
    contents="<your content here>"
)
```

## Model Recommendations

- **gemini-2.0-flash-exp**: Best for most use cases (fast, high quality)
- **gemini-1.5-pro**: Maximum context window (2M tokens)
- **gemini-1.5-flash**: Fastest option for simpler tasks

## See Also

- Base prompt: `prompt.md` (examples, testing checklist, business value)
- Provider documentation: `../../docs/provider-specific-prompts.md`
