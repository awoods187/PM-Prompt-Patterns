# AI PM Toolkit

**Production-grade prompts and frameworks for AI-native product management**

A comprehensive collection of battle-tested prompt patterns, model optimization strategies, and production frameworks for product managers building with LLMs. Built on real-world experience deploying AI systems processing 10K+ signals weekly and monitoring $100M+ ARR.

## Why This Exists

Most prompt libraries focus on toy examples. This toolkit provides **production-grade patterns** with:

- ✅ **Real metrics** from production systems (95% accuracy, $0.001/signal cost)
- ✅ **Cost optimization** strategies (99.7% cost reduction examples)
- ✅ **Multi-model expertise** across Claude, GPT, and Gemini families
- ✅ **Token-level optimization** (prompt caching, hybrid classification, model cascading)
- ✅ **Quality frameworks** (evaluation methodology, test sets, continuous monitoring)

## Quick Start

### By Experience Level

**🟢 Getting Started** → Read [PROMPT_DESIGN_PRINCIPLES.md](./PROMPT_DESIGN_PRINCIPLES.md) for core patterns

**🟡 Optimizing Prompts** → Explore [MODEL_OPTIMIZATION_GUIDE.md](./MODEL_OPTIMIZATION_GUIDE.md) for provider-specific techniques

**🔴 Production Systems** → Study [examples/signal-classification](./examples/signal-classification/README.md) for end-to-end architecture

### By Use Case

| Use Case | Prompt | Complexity | Models |
|----------|--------|------------|--------|
| Customer Signal Classification | [signal-classification.md](./prompts/data-analysis/signal-classification.md) | 🟢 Basic | Claude, GPT-4, Gemini |
| Epic Categorization | [epic-categorization](./examples/epic-categorization/) | 🟡 Intermediate | Claude Sonnet, GPT-4 |
| Executive Reporting | [executive-reporting](./examples/executive-reporting/) | 🔴 Advanced | Claude Opus, GPT-4 |

## Model Selection Guide

Understanding **when** to use each model is as important as **how** to prompt them.

### Quick Reference

| Model | Cost (Input/Output per 1M tokens) | Context | Best For | Production Use |
|-------|---------|---------|----------|----------------|
| **Claude Haiku** | $0.25 / $1.25 | 200K | High-volume classification (1000s/day) | 70% of our workload |
| **Claude Sonnet** | $3 / $15 | 200K | Production workhorse, complex analysis | 25% of our workload |
| **Claude Opus** | $15 / $75 | 200K | High-stakes decisions, creative work | 5% of our workload |
| **GPT-4 Turbo** | $10 / $30 | 128K | Function calling, structured extraction | Specific use cases |
| **GPT-3.5 Turbo** | $0.50 / $1.50 | 16K | Simple classification, cost-sensitive | Legacy systems |
| **Gemini Pro** | $1.25 / $5 | 2M | Massive context analysis | Codebase analysis |
| **Gemini Flash** | $0.075 / $0.30 | 1M | Speed-critical applications | Real-time features |

*Pricing as of October 2024. See [MODEL_OPTIMIZATION_GUIDE.md](./MODEL_OPTIMIZATION_GUIDE.md) for detailed comparison.*

### Model Cascading Pattern

Don't use one model for everything. **Route intelligently**:

```
┌─────────────────┐
│  Input Signal   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Keyword Filter  │──── 70% caught ──── FREE
└────────┬────────┘
         │ 30% through
         ▼
┌─────────────────┐
│ Claude Haiku    │──── 25% caught ──── $0.0003/signal
└────────┬────────┘
         │ 5% through
         ▼
┌─────────────────┐
│ Claude Sonnet   │──── 4.5% caught ─── $0.002/signal
└────────┬────────┘
         │ 0.5% through
         ▼
┌─────────────────┐
│ Claude Opus     │──── 0.5% caught ─── $0.015/signal
└─────────────────┘

Average cost per signal: $0.001
Naive Opus-only approach: $0.015 (15x more expensive)
```

See [Cost Optimization Guide](./docs/cost-optimization.md) for implementation details.

## Featured Example: Signal Classification System

**Problem**: Manual classification of customer signals taking 8+ hours/week, inconsistent quality

**Solution**: Hybrid classification system combining keyword matching + LLM analysis

**Results**:
- ⚡ **15 minutes** end-to-end processing (vs 8 hours manual)
- 💰 **$0.001 per signal** (99.7% cost reduction from naive approach)
- 🎯 **95% accuracy** (vs 85% manual baseline)
- 📊 **2,000+ signals/week** processed automatically
- 🏗️ **Production-tested** on systems monitoring $100M+ ARR

**Key Techniques**:
1. **Progressive enhancement**: Keyword → Haiku → Sonnet → Opus (only when needed)
2. **Prompt caching**: 95% cache hit rate = 96% cost reduction on repeat patterns
3. **Batch processing**: Process signals in groups of 50-100 for 92% cost reduction
4. **Confidence-based escalation**: Automatic escalation when confidence < 0.85

[→ Read the full case study](./examples/signal-classification/README.md)

[→ See the production prompt](./prompts/data-analysis/signal-classification.md)

## Repository Structure

```
ai-pm-toolkit/
├── prompts/              # Production-ready prompts by category
│   ├── data-analysis/    # Classification, extraction, analysis
│   ├── product-strategy/ # Roadmapping, prioritization
│   └── ...
├── templates/            # Reusable prompt patterns
│   ├── meta-prompting.md        # Use LLMs to improve prompts
│   ├── chain-of-thought.md      # Reasoning patterns
│   ├── structured-output.md     # JSON/XML output design
│   └── few-shot-examples.md     # Example-based learning
├── model-configs/        # Provider-specific optimizations
│   ├── anthropic/        # Claude Haiku, Sonnet, Opus
│   ├── openai/           # GPT-4, GPT-3.5
│   └── google/           # Gemini Pro, Flash
├── examples/             # Complete production systems
│   ├── signal-classification/
│   ├── epic-categorization/
│   └── executive-reporting/
└── docs/                 # Deep-dive guides
    ├── getting-started.md
    ├── advanced-techniques.md
    ├── cost-optimization.md
    └── quality-evaluation.md
```

## Complexity Levels

Prompts are tagged by complexity to help you level up progressively:

- 🟢 **Basic**: Single-turn, straightforward prompts. Start here if you're new to prompt engineering.
- 🟡 **Intermediate**: Multi-step reasoning, few-shot learning, structured outputs. Use when basic prompts plateau.
- 🔴 **Advanced**: Chain-of-thought, meta-prompting, multi-model orchestration. Use for production systems at scale.

**When to level up complexity**:
- Basic → Intermediate: When accuracy < 80% or inconsistent outputs
- Intermediate → Advanced: When processing >100 signals/day or cost becomes significant
- Consider simpler approaches first: A well-crafted basic prompt often beats a poorly-designed advanced one

## Advanced Technique: Meta-Prompting

One of the most powerful patterns for prompt engineering is **using an LLM to improve your prompts without executing them**.

Example:
```
I need to refine this classification prompt, but DON'T execute it.

CURRENT PROMPT:
"""
Classify this customer signal as: feature_request, bug_report, or churn_risk
Signal: {input}
"""

REQUIREMENTS:
- Optimize for: accuracy and consistency
- Target model: Claude Sonnet
- Constraints: <1000 tokens

Please provide:
1. Analysis of weaknesses
2. Three refined versions
3. Expected accuracy improvement

DO NOT execute the prompt or provide example outputs.
```

This pattern helped us evolve from 82% → 95% accuracy across 5 prompt iterations.

[→ See complete meta-prompting guide](./templates/meta-prompting.md)

## Core Principles

### 1. Model-Agnostic by Default

Base prompts work across all providers. Optimizations are **additive**:

**Base Prompt** (works everywhere):
```
Classify the customer signal into one of these categories:
- feature_request
- bug_report
- churn_risk
- expansion_signal
- general_feedback

Signal: {input}

Output only the category name.
```

**Claude Optimization** (add XML structure):
```xml
<classification_task>
  <categories>
    <category>feature_request</category>
    <category>bug_report</category>
    ...
  </categories>

  <signal>{input}</signal>

  <output_format>category_name_only</output_format>
</classification_task>
```

**GPT-4 Optimization** (add JSON mode):
```json
{
  "task": "classification",
  "categories": ["feature_request", "bug_report", ...],
  "signal": "{input}",
  "output": {
    "format": "json",
    "schema": {"category": "string"}
  }
}
```

### 2. Cost-Conscious

Every prompt includes cost analysis:
- Token count estimates
- Cost per execution
- Optimization opportunities
- Cheaper alternatives

### 3. Production-Tested

All prompts include:
- ✅ Real metrics from production use
- ✅ Failure modes and edge cases
- ✅ Quality evaluation methodology
- ✅ Version history showing iteration

### 4. Quantified Everything

Avoid vague claims. Every optimization shows:
- Before/after metrics
- Cost impact ($ and %)
- Accuracy delta
- Latency impact

## Learning Path

### Week 1: Fundamentals
1. Read [PROMPT_DESIGN_PRINCIPLES.md](./PROMPT_DESIGN_PRINCIPLES.md)
2. Try 3 basic prompts from [prompts/](./prompts/)
3. Learn [model selection framework](./MODEL_OPTIMIZATION_GUIDE.md#decision-framework)

### Week 2: Optimization
1. Study [cost optimization strategies](./docs/cost-optimization.md)
2. Implement [hybrid classification pattern](./examples/signal-classification/)
3. Practice [meta-prompting](./templates/meta-prompting.md)

### Week 3: Production
1. Build evaluation framework ([quality-evaluation.md](./docs/quality-evaluation.md))
2. Implement [model cascading](./MODEL_OPTIMIZATION_GUIDE.md#model-cascading)
3. Set up monitoring and regression testing

### Week 4: Advanced
1. Multi-model orchestration
2. Prompt caching strategies
3. Continuous improvement loops

## Contributing

This is a living repository. Contributions welcome for:

- ✅ New production-tested prompts with metrics
- ✅ Cost optimization strategies with before/after data
- ✅ Model comparison insights
- ✅ Quality evaluation methodologies

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

**Quality bar**: All contributions must include quantified results from real usage (no toy examples).

## About

Built by [Andy Woods](https://github.com/awoods187), Product Manager with 8+ years building B2B infrastructure products and production AI systems.

**Production AI Experience**:
- Customer intelligence systems processing 10K+ signals weekly
- Classification accuracy: 95%+ on production datasets
- Cost optimization: $0.001/signal (99.7% reduction from naive approaches)
- Multi-model orchestration across Claude, GPT-4, and Gemini
- Systems monitoring $100M+ ARR in B2B SaaS

Connect: [LinkedIn](https://linkedin.com/in/andrew-woods-pm) | [GitHub](https://github.com/awoods187)

## License

MIT License - see [LICENSE](./LICENSE)

## Important Note

All examples are genericized for public sharing. No proprietary information, customer data, or company-specific details included. Metrics are approximate and rounded for privacy.

---

**Start here**: [PROMPT_DESIGN_PRINCIPLES.md](./PROMPT_DESIGN_PRINCIPLES.md) → [MODEL_OPTIMIZATION_GUIDE.md](./MODEL_OPTIMIZATION_GUIDE.md) → [examples/signal-classification](./examples/signal-classification/)

Questions? Open an issue or contribute your own patterns.
