# Opus Design → Claude Code Execution Pattern - Claude Optimized

> Extends `prompt.md` with Claude-specific optimizations

## Prompt

<task>

</task>

## Claude Optimizations Applied

- **XML structure**: Uses XML tags for clear task delineation and better parsing
- **Structured thinking**: Encourages use of `<thinking>` tags for complex reasoning
- **Prompt caching**: Static prompt content is cacheable for 90%+ cost savings
- **Extended context**: Leverages Claude's 200K token context window

## Usage

```python
from pm_prompt_toolkit.providers import get_provider

# Initialize Claude provider with caching
provider = get_provider("claude-sonnet-4-5", enable_caching=True)

result = provider.generate(
    system_prompt="<prompt from above>",
    user_message="<your content here>"
)
```

## See Also

- Base prompt: `prompt.md` (examples, testing checklist, business value)
- Provider documentation: `../../docs/provider-specific-prompts.md`
