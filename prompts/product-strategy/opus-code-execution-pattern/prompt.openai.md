# Opus Design → Claude Code Execution Pattern - OpenAI Optimized

> Extends `prompt.md` with OpenAI-specific optimizations

## System Prompt

```

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
