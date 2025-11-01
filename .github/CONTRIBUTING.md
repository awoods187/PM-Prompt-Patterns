# Contributing to AI PM Toolkit

Thank you for your interest in contributing! This repository showcases production-grade prompts and frameworks for AI-native product management.

## Philosophy

This is not a collection of toy examples. Every contribution should meet our **production quality bar**:

- ✅ **Real metrics** from actual usage (accuracy, cost, latency)
- ✅ **Quantified results** (no vague "this works well")
- ✅ **Technical depth** (token optimization, model selection rationale)
- ✅ **Production considerations** (error handling, edge cases, monitoring)
- ✅ **Cost analysis** ($ per task, optimization strategies)

## Types of Contributions Welcome

### ✅ Accepted Contributions

**1. New Production-Tested Prompts**
- Must include real metrics from ≥100 uses
- Show before/after optimization
- Include cost analysis
- Document failure modes
- Provide model recommendations

**2. Cost Optimization Strategies**
- Must show quantified savings (%)
- Include before/after costs
- Explain tradeoffs
- Real production examples

**3. Model Comparison Insights**
- Test same prompt across ≥3 models
- Quantify accuracy, cost, speed differences
- Explain when to use each
- Include code examples

**4. Quality Evaluation Methodologies**
- How you measure prompt quality
- Test set composition
- A/B testing approach
- Continuous monitoring strategy

**5. Production System Case Studies**
- Complete end-to-end architecture
- Real business impact metrics
- Evolution history (iterations)
- Lessons learned

### ❌ Not Accepted

- ❌ Toy examples without production use
- ❌ Vague claims ("this is better")
- ❌ No quantified metrics
- ❌ Untested suggestions
- ❌ Proprietary/confidential information
- ❌ Customer data or company-specific details

---

## Contribution Process

### Step 1: Review Existing Content

Before contributing, familiarize yourself with:
- [README.md](./README.md) - Repository philosophy
- [PROMPT_DESIGN_PRINCIPLES.md](./PROMPT_DESIGN_PRINCIPLES.md) - Core patterns
- [examples/signal-classification](./examples/signal-classification/) - Quality bar example

### Step 2: Open an Issue First

**Before writing**:
1. Open an issue describing what you want to contribute
2. Explain why it's valuable
3. Share initial metrics/results
4. Wait for maintainer feedback

**Why**: Avoids wasted effort on contributions that don't fit the repository's goals.

### Step 3: Prepare Your Contribution

Use this checklist based on contribution type:

#### For New Prompts

- [ ] Tested on ≥100 real examples (classification) or ≥20 examples (generative)
- [ ] Measured accuracy on labeled test set
- [ ] Calculated cost per execution
- [ ] Tested with ≥2 different models
- [ ] Documented failure modes (≥3 edge cases)
- [ ] Included before/after optimization metrics
- [ ] Provided code examples for ≥1 provider

#### For Cost Optimizations

- [ ] Quantified cost reduction (%)
- [ ] Measured impact on accuracy/quality
- [ ] Tested on ≥50 examples
- [ ] Documented tradeoffs
- [ ] Included implementation code
- [ ] Showed ROI calculation

#### For Model Comparisons

- [ ] Tested ≥3 models on same task
- [ ] Used same test set (≥100 examples)
- [ ] Measured accuracy, cost, latency for each
- [ ] Explained when to use each model
- [ ] Included code for each provider

### Step 4: Follow the Template

Use the appropriate template:

**Prompt Template**:
```markdown
# [Prompt Name]

**Complexity**: 🟢/🟡/🔴
**Category**: [Data Analysis | Product Strategy | etc.]
**Model Compatibility**: ✅/❌ for Claude, GPT-4, Gemini

## Overview
[What this prompt does, business value]

## Base Prompt (Model Agnostic)
[Basic version that works everywhere]

## Model-Specific Optimizations
[Claude / GPT-4 / Gemini versions]

## Production Metrics
- Accuracy: X%
- Cost: $X per task
- Latency: Xms p95

## Cost Comparison
[Table showing different approaches]

## Common Issues & Fixes
[≥3 known failure modes with solutions]

## Version History
[Show iteration/improvement over time]
```

### Step 5: Write Quality Documentation

**Standards**:
- Use clear, technical language
- Quantify everything
- Include code examples
- Show evolution/iteration
- Document tradeoffs
- Explain "why" not just "what"

**Formatting**:
- Use tables for comparisons
- Use code blocks with language tags
- Use complexity badges (🟢🟡🔴)
- Use checkmarks (✅❌)
- Use callout boxes for important notes

### Step 6: Submit Pull Request

**PR checklist**:
- [ ] Descriptive title (e.g., "Add customer feedback sentiment analysis prompt")
- [ ] Reference related issue
- [ ] Include metrics in PR description
- [ ] All files follow style guide
- [ ] No proprietary information
- [ ] Tests pass (if applicable)
- [ ] Ready for review

**PR description template**:
```markdown
## What

[Brief description of contribution]

## Why

[Why this is valuable]

## Metrics

- Accuracy: X%
- Cost: $X per task
- Tested on: X examples
- Production use: X tasks

## Testing

[How you validated this]

## Related

Closes #[issue number]
```

---

## Quality Standards

### Metrics Requirements

**For Classification Prompts**:
- Test set: ≥100 labeled examples
- Accuracy: Report overall + per-category
- Cost: $ per classification
- Latency: p50, p95, p99
- Edge cases: ≥3 documented failure modes

**For Generative Prompts**:
- Test set: ≥20 examples with human evaluation
- Quality: Human rating (1-5 scale) or specific metrics
- Cost: $ per generation
- Token count: Average input + output
- Consistency: Standard deviation of quality scores

**For Cost Optimizations**:
- Baseline cost: $ before optimization
- Optimized cost: $ after optimization
- Savings: % reduction
- Quality impact: Accuracy delta
- Trade-offs: What was sacrificed (if anything)

### Code Standards

**Python examples** (preferred):
- Use type hints
- Include docstrings
- Handle errors
- Show provider SDK usage
- Runnable with minimal setup

**Example**:
```python
from typing import Tuple
from anthropic import Anthropic

def classify_signal(signal: str) -> Tuple[str, float]:
    """
    Classify customer signal using Claude Sonnet.

    Args:
        signal: Customer signal text

    Returns:
        Tuple of (category, confidence)

    Raises:
        ValueError: If signal is empty
        APIError: If Claude API fails
    """
    if not signal:
        raise ValueError("Signal cannot be empty")

    client = Anthropic(api_key="...")
    response = client.messages.create(...)

    return parse_response(response)
```

### Documentation Standards

**Tone**:
- Technical but accessible
- Assume AI-native audience
- Don't explain basics (e.g., "what is temperature")
- Include learning comments for advanced concepts
- Honest about limitations

**Structure**:
- Start with overview (what, why, value)
- Show basic version first
- Build to advanced versions
- Include production considerations
- End with related content

**Quantification**:
- Every claim backed by data
- Use specific numbers, not ranges
- Show before/after comparisons
- Include cost analysis
- Document iteration history

---

## Review Criteria

Your contribution will be evaluated on:

**1. Technical Quality** (40%)
- Prompt engineering best practices
- Token optimization
- Error handling
- Edge case coverage

**2. Evidence** (30%)
- Real metrics from production/testing
- Quantified results
- Test methodology
- Cost analysis

**3. Presentation** (20%)
- Clear documentation
- Code examples
- Formatting
- Completeness

**4. Value** (10%)
- Novel insight or approach
- Fills gap in repository
- Reusable by others
- Demonstrates expertise

**Minimum bar**:
- 70% overall score
- No section below 50%

---

## Style Guide

### Complexity Badges

- 🟢 **Basic**: Single-turn, straightforward prompts
- 🟡 **Intermediate**: Multi-step reasoning, few-shot, structured output
- 🔴 **Advanced**: Chain-of-thought, meta-prompting, multi-model

### Status Indicators

- ✅ Supported/Recommended
- ❌ Not supported/Not recommended
- ⚠️ Supported with caveats
- 🚧 Under development

### Model Compatibility

Always indicate compatibility:
```markdown
**Model Compatibility**: ✅ Claude (all) | ✅ GPT-4 | ❌ Gemini (not tested)
```

### Code Blocks

Always specify language:
````markdown
```python
# Python code
```

```xml
<!-- XML prompt -->
```

```json
{"json": "example"}
```
````

### Tables

Use tables for comparisons:
```markdown
| Model | Cost | Accuracy | Latency |
|-------|------|----------|---------|
| Haiku | $0.0003 | 89% | 300ms |
| Sonnet | $0.002 | 95% | 450ms |
```

---

## Community Guidelines

### Be Respectful

- Assume good intent
- Constructive feedback only
- No gatekeeping
- Help newcomers

### Be Honest

- Don't exaggerate results
- Admit limitations
- Share failures, not just successes
- Question assumptions

### Be Rigorous

- Test thoroughly
- Show your work
- Provide evidence
- Document methodology

---

## Getting Help

**Questions about contributing?**
- Open an issue with "Question:" prefix
- Check existing issues first
- Be specific about what you need

**Unsure if your contribution fits?**
- Open an issue describing your idea
- Share preliminary metrics
- Ask for feedback before writing

**Need help testing?**
- Share your approach in an issue
- Ask for methodology advice
- We can help with test set design

---

## Recognition

**Contributors will be**:
- Listed in README acknowledgments
- Credited in their contribution files
- Thanked publicly for valuable additions

**Top contributors** (≥5 accepted PRs) get:
- Recognition in README
- Input on repository direction
- Early access to new content

---

## Legal

### Licensing

By contributing, you agree that your contributions will be licensed under the MIT License.

### Confidentiality

**DO NOT include**:
- Customer names or data
- Company-specific information
- Proprietary systems or code
- Exact revenue/ARR numbers
- Internal tool names

**Instead**:
- Genericize examples ("B2B SaaS company")
- Approximate metrics ("$100M+ ARR")
- Use placeholder names ("Acme Corp")
- Focus on patterns, not specifics

### Attribution

If using ideas/prompts from others:
- Credit original source
- Link to original work
- Explain what you changed
- Get permission if significant

---

## Maintenance

### Versioning

Prompts should include version history:
```markdown
## Version History

| Version | Date | Changes | Accuracy | Cost |
|---------|------|---------|----------|------|
| v1.0 | 2024-01 | Initial version | 82% | $0.015 |
| v2.0 | 2024-03 | Added examples | 89% | $0.004 |
```

### Deprecation

If a prompt becomes outdated:
1. Mark as deprecated in header
2. Explain why (model upgrade, better approach)
3. Link to replacement
4. Keep for historical reference

### Updates

Contributions may need updates for:
- New model versions
- Pricing changes
- Better techniques discovered
- User feedback

Original authors will be tagged for input on updates.

---

## Developer Certificate of Origin (DCO)

This project uses the Developer Certificate of Origin (DCO) to ensure that contributors have the right to submit their code. By contributing to this project, you certify that:

1. The contribution was created in whole or in part by you and you have the right to submit it under the MIT License; or
2. The contribution is based upon previous work that, to your knowledge, is covered under an appropriate open source license and you have the right to submit that work with modifications under the same open source license; or
3. The contribution was provided directly to you by some other person who certified (1) or (2) and you have not modified it.

### How to Sign Off Commits

All commits must include a `Signed-off-by` line. Add it with the `-s` flag:

```bash
git commit -s -m "Add new prompt for feature prioritization

This prompt helps PMs prioritize features using weighted scoring.
Tested with Claude Sonnet 4.5, achieving 92% stakeholder agreement.

Signed-off-by: Your Name <your.email@example.com>"
```

The `-s` flag automatically adds the `Signed-off-by` line to your commit message.

**Important**: Pull requests with unsigned commits will not be merged. The DCO check runs automatically on all PRs.

### Why DCO?

The DCO protects both you and the project:
- **For you**: Certifies you have the right to contribute
- **For the project**: Creates a clear legal trail for contributions
- **For users**: Ensures code can be used under the MIT License

This is a lightweight alternative to a Contributor License Agreement (CLA) and is used by many major open source projects including Linux, Docker, and GitLab.

---

## Questions?

Open an issue or email [your contact].

Thank you for helping build the best resource for AI-native product managers!
