# AI PM Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Production-grade prompts and frameworks for AI-native product management**

A comprehensive collection of battle-tested prompt patterns, model optimization strategies, and production frameworks for product managers building with LLMs. Built on real-world experience deploying AI systems processing 5K+ heterogeneous data points weekly with 95% accuracy and monitoring $100M+ ARR.

## Why This Exists

Most prompt libraries focus on toy examples. This toolkit provides **production-grade patterns** with:

- ✅ **Real metrics** from production systems (95% accuracy, $0.001/signal cost)
- ✅ **Cost optimization** strategies (99.7% cost reduction examples)
- ✅ **Multi-model expertise** across Claude, GPT, and Gemini families
- ✅ **Token-level optimization** (prompt caching, hybrid classification, model cascading)
- ✅ **Quality frameworks** (evaluation methodology, test sets, continuous monitoring)
- ✅ **Production model management** (YAML-based registry, pricing service, capability validation)

## Quick Start

### Installation

For Python integration:

```bash
# Clone the repository
git clone https://github.com/awoods187/PM-Prompt-Patterns.git
cd PM-Prompt-Patterns

# Install as package (optional)
pip install -e .

# Verify installation
python -c "from ai_models import get_model; print(get_model('claude-sonnet-4-5').name)"
```

### By Experience Level

**🟢 Getting Started** → Read [PROMPT_DESIGN_PRINCIPLES.md](./PROMPT_DESIGN_PRINCIPLES.md) for core patterns

**🟡 Optimizing Prompts** → Explore [MODEL_OPTIMIZATION_GUIDE.md](./MODEL_OPTIMIZATION_GUIDE.md) for provider-specific techniques

**🔴 Production Systems** → Study [examples/epic-categorization](./examples/epic-categorization/) for end-to-end architecture

### By Use Case

| Use Case            | Prompt       | Complexity | Models |
|---------------------|--------------|------------|--------|
| Analytics & Metrics | [analytics/](./prompts/analytics/) | 🟢-🔴 All levels | All models |
| Epic Categorization | [epic-categorization](./examples/epic-categorization/) | 🟡 Intermediate | Claude Sonnet, GPT-4 |
| Product Strategy    | [product-strategy/](./prompts/product-strategy/) | 🟡-🔴 Intermediate-Advanced | Claude Opus, Sonnet |

## Model Selection Guide

Understanding **when** to use each model is as important as **how** to prompt them.

### Quick Reference

| Model                    | Cost (Input/Output per 1M tokens) | Context | Best For | Production Use |
|--------------------------|---------|---------|----------|----------------|
| **Claude Haiku 4.5** | $1.00 / $5.00 | 200K | High-volume classification (1000s/day) | 70% of our workload |
| **Claude Sonnet 4.5** | $3.00 / $15.00 | 200K | Production workhorse, complex analysis | 25% of our workload |
| **Claude Opus 4.1** | $15.00 / $75.00 | 200K | High-stakes decisions, creative work | 5% of our workload |
| **GPT-4o** | $2.50 / $10.00 | 128K | Multimodal, function calling, structured extraction | Specific use cases |
| **GPT-4o mini** | $0.15 / $0.60 | 128K | Cost-efficient alternative to 3.5 Turbo | Budget tasks |
| **Gemini 2.5 Pro** | $1.25 / $5.00 | 2M | Massive context analysis (entire codebases) | Large document analysis |
| **Gemini 2.5 Flash** | $0.075 / $0.30 | 1M | Speed-critical, high-volume applications | Real-time features |
| **Gemini 2.5 Flash-Lite** | Coming Soon | 1M | Ultra cost-efficient processing | Maximum throughput |

*Pricing verified October 2025. Managed via `ai_models` system - see [MODEL_OPTIMIZATION_GUIDE.md](./MODEL_OPTIMIZATION_GUIDE.md).*

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

## AI Model Management System

This repository includes a production-grade model management system (`ai_models/`) with:

### Key Features

**✅ YAML-based Model Definitions**: Version-controlled model specifications
```python
from ai_models import get_model

model = get_model("claude-sonnet-4-5")
print(f"Context: {model.metadata.context_window_input:,} tokens")
print(f"Cost: ${model.pricing.input_per_1m}/M input")
# Context: 200,000 tokens
# Cost: $3.0/M input
```

**✅ Runtime Capability Validation**: Check model features before API calls
```python
from ai_models import has_vision, has_function_calling, has_prompt_caching

if has_vision("gpt-4o"):
    process_image()  # Safe - GPT-4o supports vision

if has_prompt_caching("claude-sonnet-4-5"):
    enable_caching()  # 90% cost savings on cached tokens
```

**✅ Optimized Pricing Service**: LRU-cached cost calculations
```python
model = get_model("claude-haiku-4-5")
cost = model.calculate_cost(
    input_tokens=10_000,
    output_tokens=2_000,
    cached_input_tokens=5_000  # Automatic cache discount
)
# Cost: ~$0.013 (vs $0.025 without caching)
```

**✅ Cost Tier Filtering**: Find budget-friendly models
```python
from ai_models import ModelRegistry

budget_models = ModelRegistry.filter_by_cost_tier("budget")
# Returns: Haiku, 4o-mini, Flash, Flash-Lite
```

**✅ Comprehensive Testing**: 97 tests ensure pricing accuracy
- Fixed critical bug: Claude Haiku was 4x underpriced
- Prevents future pricing regressions
- Validates all model specs against official docs

See [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md) for migrating from old `models/registry.py` system.

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

[→ Read the full case study](./examples/epic-categorization/)

[→ Explore analytics prompts](./prompts/analytics/)

## Repository Structure

```
PM-Prompt-Patterns/
├── prompts/                    # Production-ready prompts by category
│   ├── analytics/              # ✨ NEW: Data analysis, metrics, reporting (MECE organized)
│   │   ├── monitoring/         # Real-time alerts, anomaly detection
│   │   ├── reporting/          # Periodic dashboards, business reviews
│   │   └── investigation/      # Ad-hoc analysis, root cause deep dives
│   ├── product-strategy/       # Roadmapping, prioritization
│   ├── customer-research/      # User feedback analysis
│   ├── roadmap-planning/       # Feature prioritization
│   ├── stakeholder-communication/
│   └── technical-documentation/
├── templates/                  # Reusable prompt patterns
│   ├── meta-prompting.md       # Use LLMs to improve prompts
│   ├── chain-of-thought.md     # Reasoning patterns
│   ├── structured-output.md    # JSON/XML output design
│   └── few-shot-examples.md    # Example-based learning
├── ai_models/                  # ✨ NEW: Unified model management
│   ├── registry.py             # YAML-based model registry
│   ├── pricing.py              # Pricing service with caching
│   ├── capabilities.py         # Runtime capability validation
│   └── definitions/            # Model specifications (YAML)
│       ├── anthropic/          # Claude Haiku, Sonnet, Opus 4.x
│       ├── openai/             # GPT-4o, GPT-4o mini
│       └── google/             # Gemini 2.5 Pro, Flash, Flash-Lite
├── pm_prompt_toolkit/          # Python package for production use
│   ├── providers/              # LLM provider integrations
│   ├── optimizers/             # Prompt optimization utilities
│   └── config/                 # Configuration management
├── examples/                   # Complete production systems
│   └── epic-categorization/    # Real-world classification
├── tests/                      # Comprehensive test suite (97 tests)
│   ├── test_model_registry.py  # Registry validation
│   ├── test_ai_models.py       # New system tests
│   └── test_pricing_consistency.py
├── scripts/                    # Automation and testing
│   └── run_tests.sh            # Test runner with multiple modes
└── docs/                       # Deep-dive guides
    ├── PROMPT_DESIGN_PRINCIPLES.md
    ├── MODEL_OPTIMIZATION_GUIDE.md
    ├── MIGRATION_GUIDE.md      # ✨ NEW: Old → new system migration
    └── REFACTOR_COMPLETE.md    # ✨ NEW: Refactor summary
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

## License & Contributing

### License

This project is licensed under the **MIT License** - see [LICENSE](./LICENSE) for full details.

**TL;DR**: You can use this freely in commercial products, modify as needed, and don't need attribution (though it's appreciated).

**Key Points**:
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ❌ No warranty provided
- ❌ No liability accepted

**Questions about licensing?**
- [LICENSE_FAQ.md](./LICENSE_FAQ.md) - Common questions answered
- [CONTENT_LICENSE.md](./CONTENT_LICENSE.md) - Prompt-specific clarifications
- [ATTRIBUTION.md](./ATTRIBUTION.md) - How to credit (optional)

### Contributing

We welcome contributions! This project thrives on:
- 📊 **Production-tested prompts** with real metrics
- 🔧 **Code improvements** to ai_models system
- 📚 **Documentation** enhancements
- 🧪 **Test additions** and quality improvements

**How to contribute**:
1. Read [CONTRIBUTING.md](./CONTRIBUTING.md) - Quality standards and process
2. Check [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) - Community guidelines
3. Sign your commits with DCO (`git commit -s`)
4. Submit a PR using our [template](.github/pull_request_template.md)

**All contributors** are recognized in [ATTRIBUTION.md](./ATTRIBUTION.md).

## 📦 Recent Changes: Analytics Category Reorganization

**What Changed** (October 2025):
- Consolidated `prompts/data-analysis/` and `prompts/metrics-reporting/` into new `prompts/analytics/` structure
- Organized by temporal pattern (monitoring, reporting, investigation) for MECE principles
- Added comprehensive navigation and category guidelines

**Migration**:
- Old `data-analysis/` → Now `analytics/` (organized by use case)
- Old `metrics-reporting/` → Now `analytics/reporting/`
- See [prompts/analytics/README.md](./prompts/analytics/) for navigation guide

**Why**: The new structure eliminates category overlap and makes it clearer which prompts to use for real-time monitoring vs. periodic reporting vs. ad-hoc investigation.

## Important Note

All examples are genericized for public sharing. No proprietary information, customer data, or company-specific details included. Metrics are approximate and rounded for privacy.

---

## Quick Links

**📚 Learning Path**: [PROMPT_DESIGN_PRINCIPLES.md](./PROMPT_DESIGN_PRINCIPLES.md) → [MODEL_OPTIMIZATION_GUIDE.md](./MODEL_OPTIMIZATION_GUIDE.md) → [examples/epic-categorization](./examples/epic-categorization/)

**🔧 Developer Guide**: [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md) for using the `ai_models` system

**✅ Test Suite**: `./scripts/run_tests.sh` to run 97 tests validating all models

**📊 Model Registry**: See `ai_models/definitions/` for current model specifications

Questions? Open an issue or contribute your own patterns.
