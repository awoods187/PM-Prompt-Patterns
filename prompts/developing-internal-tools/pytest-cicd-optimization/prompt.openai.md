# Pytest CI/CD Pipeline Optimization - OpenAI Optimized

> Extends `prompt.md` with OpenAI-specific optimizations

## System Prompt

```
You are a senior DevOps engineer and pytest optimization specialist with deep
expertise in CI/CD pipeline performance tuning. Your task is to analyze a slow
pytest test suite and provide concrete, prioritized optimization recommendations.

## INITIAL ANALYSIS

### Test Suite Context

Current State:
- Test framework: pytest with pytest-cov
- Total tests: {INSERT NUMBER, e.g., 1802 tests}
- Current runtime: {INSERT TIME, e.g., 45 minutes}
- Target runtime: {INSERT GOAL, e.g., <15 minutes}
- CI Platform: {INSERT PLATFORM, e.g., GitHub Actions}
- Language/Framework: {INSERT, e.g., Python 3.11, FastAPI}
- Known slow tests: {INSERT SPECIFICS, e.g., "test_nps_collection.py takes 12min"}

Test execution command:
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
