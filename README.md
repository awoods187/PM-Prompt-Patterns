# PM Prompt Toolkit

Production-grade prompt patterns and multi-cloud AI orchestration for product teams building with Claude, GPT, and Gemini. Now with AWS Bedrock and Google Vertex AI support. Proven at scale: 5K+ signals/week, 95% accuracy, $0.001/signal cost.

## 📊 Project Status

![CI](https://github.com/awoods187/PM-Prompt-Patterns/workflows/CI/badge.svg)
![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

**Status:** Production-ready | **Last Updated:** 2025-10-27 | **Maintenance:** Active development

---

## 🎯 Why This Exists

**Problem:** Most prompt libraries showcase toy examples. Production systems need battle-tested patterns with real metrics.

**Solution:** Enterprise-grade toolkit combining 200+ production prompts, multi-model orchestration, and cost optimization strategies.

**Key Benefits:**
- **Proven ROI:** 99.7% cost reduction through intelligent model cascading (Haiku → Sonnet → Opus)
- **Production Metrics:** 95% accuracy on 5K+ weekly signals, validated on $100M+ ARR systems
- **Multi-Model Expertise:** Optimized patterns for Claude 4.x, GPT-4o, Gemini 2.5 families
- **Zero to Production:** Complete examples with evaluation methodology, not just prompts
- **Developer Tools:** Python package with YAML-based model registry, pricing service, capability validation

---

## 🚀 Quick Start

Get operational in under 5 minutes:

```bash
# Clone and install
git clone https://github.com/awoods187/PM-Prompt-Patterns.git
cd PM-Prompt-Patterns
pip install -e .

# Verify installation
python -c "from ai_models import get_model; print(get_model('claude-sonnet-4-5').name)"
```

**Next Steps by Role:**
- **New to prompts?** → [Design Principles](./docs/prompt_design_principles.md)
- **Optimizing costs?** → [Model Selection Guide](#-model-selection-guide)
- **Building production systems?** → [Epic Categorization Example](./examples/epic-categorization/)
- **Understanding the codebase?** → [Project Structure](./docs/project_structure.md)

---

## 📋 Prerequisites

| Tool | Version | Verification | Purpose |
|------|---------|--------------|---------|
| Python | 3.9+ | `python --version` | Core runtime |
| pip | Latest | `pip --version` | Package management |
| API Keys | - | Set in `.env` | Claude/GPT/Gemini access |

<details>
<summary>API Key Setup (Optional)</summary>

Create `.env` file:
```bash
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

Keys only required for live API testing. Browse prompts without keys.
</details>

### Multi-Cloud Provider Support (New in v0.2.0)

The toolkit now supports running Claude models through **AWS Bedrock** and **Google Vertex AI** in addition to direct Anthropic APIs.

**Installation with cloud providers:**
```bash
# For AWS Bedrock support
pip install -e ".[bedrock]"

# For Google Vertex AI support
pip install -e ".[vertex]"

# For all cloud providers
pip install -e ".[all]"
```

**Provider Configuration:**
```bash
# AWS Bedrock (add to .env)
ENABLE_BEDROCK=true
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here
AWS_REGION=us-east-1

# Google Vertex AI (add to .env)
ENABLE_VERTEX=true
GCP_PROJECT_ID=your-project-id
GCP_REGION=us-central1
GCP_CREDENTIALS_PATH=/path/to/credentials.json  # Optional
```

**Usage:**
```python
from pm_prompt_toolkit.providers import get_provider

# Explicit provider selection
bedrock = get_provider("bedrock:claude-sonnet-4-5")
vertex = get_provider("vertex:claude-sonnet-4-5")

# Automatic routing (uses Bedrock if enabled)
provider = get_provider("claude-sonnet-4-5")
result = provider.classify("We need SSO integration")
```

**Benefits:**
- **Bedrock:** Enterprise AWS infrastructure, AWS-native billing, regional data residency
- **Vertex AI:** Google Cloud integration, GCP-native billing, unified GCP experience
- **Fallback:** Automatically falls back to direct Anthropic API if cloud providers unavailable

---

## 📖 Usage

### Basic Model Management

```python
from ai_models import get_model, has_vision, has_prompt_caching

# Get model specifications
model = get_model("claude-sonnet-4-5")
print(f"Context: {model.metadata.context_window_input:,} tokens")
print(f"Cost: ${model.pricing.input_per_1m}/M input tokens")

# Calculate costs with caching
cost = model.calculate_cost(
    input_tokens=10_000,
    output_tokens=2_000,
    cached_input_tokens=5_000  # 90% discount on cached tokens
)

# Validate capabilities before API calls
if has_vision("gpt-4o"):
    process_image()
```

### Finding Budget-Friendly Models

```python
from ai_models import ModelRegistry

budget_models = ModelRegistry.filter_by_cost_tier("budget")
# Returns: Haiku 4.5, GPT-4o mini, Gemini Flash
```

**Advanced Examples:** [API Documentation](./docs/api-examples.md) | [Production Architecture](./examples/epic-categorization/)

---

## 🤖 Model Selection Guide

Choose the right model for your workload:

| Model | Input/Output (per 1M) | Context | Best For | Our Usage |
|-------|----------------------|---------|----------|-----------|
| **Claude Haiku 4.5** | $1/$5 | 200K | High-volume classification | 70% |
| **Claude Sonnet 4.5** | $3/$15 | 200K | Production workhorse | 25% |
| **Claude Opus 4.1** | $15/$75 | 200K | High-stakes decisions | 5% |
| **GPT-4o** | $2.5/$10 | 128K | Multimodal, function calling | Specific |
| **GPT-4o mini** | $0.15/$0.60 | 128K | Budget alternative | Budget |
| **Gemini 2.5 Pro** | $1.25/$5 | 2M | Massive context analysis | Large docs |
| **Gemini 2.5 Flash** | $0.075/$0.30 | 1M | Speed-critical apps | Real-time |

*Pricing verified October 2025. See [MODEL_OPTIMIZATION_GUIDE.md](./MODEL_OPTIMIZATION_GUIDE.md) for detailed comparison.*

### Cost Optimization Pattern

**Don't use one model for everything.** Intelligent routing saves 99.7%:

```
Keyword Filter (free) → 70% resolved
    ↓
Haiku ($0.0003/signal) → 25% resolved
    ↓
Sonnet ($0.002/signal) → 4.5% resolved
    ↓
Opus ($0.015/signal) → 0.5% resolved

Average: $0.001/signal (vs $0.015 naive approach)
```

[→ Implementation Guide](./docs/cost-optimization.md)

---

## 📁 Repository Structure

```
PM-Prompt-Patterns/
├── prompts/              # Production-ready prompts by category
│   ├── analytics/        # Monitoring, reporting, investigation (MECE)
│   ├── product-strategy/ # Roadmapping, prioritization
│   └── technical-docs/   # API docs, CLAUDE.md generation
├── ai_models/            # Python model management system
│   ├── registry.py       # YAML-based model registry
│   ├── pricing.py        # Cost calculation with caching
│   └── definitions/      # Model specs (Anthropic, OpenAI, Google)
├── examples/             # Complete production systems
│   └── epic-categorization/  # 95% accuracy, $0.001/signal
├── tests/                # 97 tests for model validation
└── docs/                 # Deep-dive guides
```

**Navigate by Experience:**
- 🟢 **Beginner:** [prompts/](./prompts/) basic patterns
- 🟡 **Intermediate:** [MODEL_OPTIMIZATION_GUIDE.md](./MODEL_OPTIMIZATION_GUIDE.md)
- 🔴 **Advanced:** [examples/epic-categorization/](./examples/epic-categorization/)

---

## 🔐 Security & Compliance

**Security Scanning:** Multi-layer (Bandit, Safety, pip-audit, Semgrep, TruffleHog)
**Dependency Updates:** Automated weekly via Dependabot
**API Key Management:** Environment variables only, never committed
**Vulnerability Reporting:** Open GitHub issue with `security` label

**CI/CD Status:** All security scans pass. See [workflows](./.github/workflows/) for details.

---

## 📈 Performance & Scalability

**Proven Metrics:**
- **Throughput:** 5,000+ signals/week in production
- **Accuracy:** 95% (vs 85% manual baseline)
- **Cost Efficiency:** $0.001/signal average (99.7% reduction)
- **Latency:** <2s p95 with model cascading
- **Cache Hit Rate:** 95% on repeat patterns

**Scalability:**
- Batch processing: 50-100 signals/batch for 92% cost reduction
- Prompt caching: 90% discount on cached tokens
- Model registry: LRU-cached for <1ms lookups

[→ Benchmarks & Architecture](./docs/performance.md)

---

## 🤝 Support & Ownership

**Team:** Product Infrastructure
**Issues:** [GitHub Issues](https://github.com/awoods187/PM-Prompt-Patterns/issues)
**Contributions:** [CONTRIBUTING.md](./.github/CONTRIBUTING.md) | [CODE_OF_CONDUCT.md](./.github/CODE_OF_CONDUCT.md)
**Response Time:** Best effort (open source project)

**Getting Help:**
1. Check [docs/](./docs/) for guides
2. Search existing issues
3. Open new issue with reproduction steps

---

## 📅 Maintenance Status

| Section | Update Frequency | Next Update |
|---------|-----------------|-------------|
| Model Definitions | Weekly (automated staleness check) | Continuous |
| Model Pricing | Monthly | Nov 2025 |
| Model Specs | As released | Ongoing |
| Security Scans | Weekly (automated) | Continuous |
| Dependencies | Weekly (Dependabot) | Continuous |
| Prompts | Ad-hoc | As contributed |

**Model Update Process:** Automated weekly staleness checks via GitHub Actions. See [Model Update System](./docs/model_update_system.md) for manual update procedures.

**Deprecation Policy:** 90-day notice for breaking changes. See [CHANGELOG.md](./CHANGELOG.md).

---

## 🎓 Learning Resources

**Fundamentals** (Start here):
1. [Prompt Design Principles](./docs/prompt_design_principles.md) - Core patterns
2. [Model Optimization Guide](./MODEL_OPTIMIZATION_GUIDE.md) - Provider techniques
3. [Cost Optimization](./docs/cost_optimization.md) - ROI strategies

**Production Systems:**
- [Epic Categorization Example](./examples/epic-categorization/) - End-to-end architecture
- [Quality Evaluation](./docs/quality_evaluation.md) - Testing methodology
- [Meta-Prompting](./templates/meta-prompting.md) - Iterative improvement

**Migration:**
- [Old → New System](./MIGRATION_GUIDE.md) - Upgrade from legacy registry

[→ Full Learning Path](./docs/learning-path.md)

---

## 🤝 Contributing

We welcome production-tested contributions with real metrics:

**Quality Bar:**
- ✅ Quantified results from actual usage (no toy examples)
- ✅ Before/after metrics (accuracy, cost, latency)
- ✅ Failure modes documented
- ✅ Tests included (97 existing tests for reference)

**Process:**
1. Review [CONTRIBUTING.md](./.github/CONTRIBUTING.md)
2. Sign commits with DCO: `git commit -s`
3. Submit PR using [template](./.github/pull_request_template.md)

**Recognition:** All contributors listed in [ATTRIBUTION.md](./docs/attribution.md).

---

## 📄 License

**MIT License** - Commercial use, modification, distribution allowed. No warranty.

**TL;DR:** Use freely in commercial products, no attribution required (appreciated).

**Details:** [LICENSE](./LICENSE) | [LICENSE_FAQ.md](./docs/license_faq.md) | [CONTENT_LICENSE.md](./docs/content_license.md)

---

## 🔗 Quick Links

**Getting Started:** [Design Principles](./docs/prompt_design_principles.md) → [Model Guide](./MODEL_OPTIMIZATION_GUIDE.md) → [Examples](./examples/)

**Repository Structure:** [Project Structure Guide](./docs/project_structure.md) | [Changelog](./CHANGELOG.md)
**Developer API:** [ai_models Package](./docs/api-examples.md) | [Migration Guide](./MIGRATION_GUIDE.md)
**CI/CD:** [Workflows](./.github/workflows/) | [Run Tests](./scripts/run_tests.sh)
**Model Registry:** [Definitions](./ai_models/definitions/) | [Pricing](./ai_models/pricing.py)

---

**Note:** All examples genericized for public sharing. No proprietary data included. Metrics approximate and rounded for privacy.
