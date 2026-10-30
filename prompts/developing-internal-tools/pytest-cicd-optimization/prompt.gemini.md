# Pytest CI/CD Pipeline Optimization - Gemini Optimized

> Extends `prompt.md` with Gemini-specific optimizations

## System Instruction

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

## Gemini Optimizations Applied

- **Clear directives**: Explicit, numbered instructions for better instruction-following
- **Context utilization**: Optimized for Gemini's large context window
- **Multimodal ready**: Can process code alongside diagrams, screenshots, or other media
- **Structured reasoning**: Step-by-step breakdown for complex analysis tasks

## Usage

```python
from pm_prompt_toolkit.providers import get_provider

# Initialize Gemini provider
provider = get_provider("gemini-3-8-flash")

result = provider.generate(
    system_instruction="<prompt from above>",
    contents="<your content here>"
)
```

## Model Recommendations

- **gemini-3-8-flash**: Best for most use cases (fast, high quality)
- **gemini-4-argon**: Hardest reasoning and agentic tasks

## See Also

- Base prompt: `prompt.md` (examples, testing checklist, business value)
- Provider documentation: `../../docs/provider-specific-prompts.md`
