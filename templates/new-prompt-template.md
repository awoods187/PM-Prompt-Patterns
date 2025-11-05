# [Prompt Name]

**Complexity**: [🟢 Beginner | 🟡 Intermediate | 🔴 Advanced]
**Category**: [Category Name]
**Model Compatibility**: [✅ Claude (all) | ✅ GPT-5 | ✅ Gemini]

## Overview

[1-2 sentence description of what this prompt does and its primary use case]

**Business Value**:
- [Business value point 1]
- [Business value point 2]
- [Business value point 3]

**Use Cases**:
- [Use case 1]
- [Use case 2]
- [Use case 3]

**Production metrics**:
- [Metric 1: e.g., Accuracy: 95%]
- [Metric 2: e.g., Processing time: <2s]
- [Metric 3: e.g., Cost: $0.001 per request]

---

## Prompt

```
[Your actual prompt content goes here - model-agnostic, no XML tags or model-specific syntax]

[Example structure:]

You are a [role description]. Your task is to [primary objective].

## Requirements

1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

## Input Format

[Description of expected input]

## Output Format

[Description of expected output structure]

## Guidelines

- [Guideline 1]
- [Guideline 2]
- [Guideline 3]

## Examples

[Optional: Include 1-2 examples if helpful for the LLM to understand the task]
```

---

## Production Patterns

### Pattern 1: [Pattern Name]

**Use case**: [When to use this pattern]

**Implementation**:
```python
# Code example showing how to use this prompt in production
from pm_prompt_toolkit.providers import get_provider

provider = get_provider("claude-sonnet-4-5")
result = provider.generate(
    system_prompt="<your prompt>",
    user_message="<user input>"
)
```

**Best practices**:
- [Best practice 1]
- [Best practice 2]

### Pattern 2: [Another Pattern]

[Repeat structure above]

---

## Quality Evaluation

### Success Criteria

- [ ] [Criterion 1: e.g., Output follows specified format]
- [ ] [Criterion 2: e.g., All required fields are present]
- [ ] [Criterion 3: e.g., Accuracy meets threshold]

### Evaluation Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| [Metric 1] | [Target value] | [How to measure] |
| [Metric 2] | [Target value] | [How to measure] |

### Common Issues

**Issue**: [Problem description]
- **Symptom**: [How it manifests]
- **Cause**: [Why it happens]
- **Fix**: [How to resolve]

---

## Usage Notes

### When to Use This Prompt

✅ **Good for**:
- [Scenario 1]
- [Scenario 2]
- [Scenario 3]

❌ **Not recommended for**:
- [Scenario 1]
- [Scenario 2]

### Model-Specific Considerations

**Claude**:
- [Claude-specific tip]
- [Performance note]

**OpenAI (GPT-5)**:
- [OpenAI-specific tip]
- [Performance note]

**Gemini**:
- [Gemini-specific tip]
- [Performance note]

### Cost Optimization

- [Tip 1: e.g., Use prompt caching for repeated calls]
- [Tip 2: e.g., Batch processing reduces overhead]
- [Tip 3: e.g., Consider cheaper models for simpler cases]

---

## Common Issues & Fixes

### Issue 1: [Issue Name]

**Symptoms**:
- [Symptom 1]
- [Symptom 2]

**Root Cause**:
[Explanation of why this happens]

**Solution**:
```
[Code or prompt modification to fix the issue]
```

### Issue 2: [Another Issue]

[Repeat structure above]

---

## Related Prompts

- [`category/related-prompt-1`](../category/related-prompt-1/prompt.md) - [Brief description]
- [`category/related-prompt-2`](../category/related-prompt-2/prompt.md) - [Brief description]

---

## Version History

**v1.0** (YYYY-MM-DD)
- Initial version
- [Key features]

**v1.1** (YYYY-MM-DD)
- [Changes made]
- [Improvements]

---

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines on improving this prompt.
