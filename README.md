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

### Multi-Provider Support (New in v0.2.0)

The toolkit supports **6 AI providers** with intelligent routing and cost optimization:

**Supported Providers:**
- **Anthropic Claude** (direct API) - Haiku, Sonnet, Opus
- **AWS Bedrock** - Claude models via AWS infrastructure
- **Google Vertex AI** - Claude models via Google Cloud
- **OpenAI** - GPT-5 (all variants), GPT-4.1, o3, o4-mini, GPT-4o
- **Google Gemini** - Gemini 2.5 Pro, Flash, Flash Lite
- **Mock Provider** - Zero-cost testing provider

**Installation:**
```bash
# Base installation (Anthropic Claude + Mock)
pip install -e .

# With AWS Bedrock support
pip install -e ".[bedrock]"

# With Google Vertex AI support
pip install -e ".[vertex]"

# With OpenAI support
pip install -e ".[openai]"

# With Google Gemini support
pip install -e ".[gemini]"

# With all providers
pip install -e ".[all]"
```

**Provider Configuration (.env file):**
```bash
# Anthropic Claude (direct API)
ANTHROPIC_API_KEY=your_key_here

# AWS Bedrock
ENABLE_BEDROCK=true
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here
AWS_REGION=us-east-1

# Google Vertex AI
ENABLE_VERTEX=true
GCP_PROJECT_ID=your-project-id
GCP_REGION=us-central1
GCP_CREDENTIALS_PATH=/path/to/credentials.json  # Optional

# OpenAI
ENABLE_OPENAI=true
OPENAI_API_KEY=sk-your_key_here
OPENAI_ORG_ID=org-your_org_here  # Optional

# Google Gemini
GOOGLE_API_KEY=your_key_here
```

**Usage Examples:**
```python
from pm_prompt_toolkit.providers import get_provider

# Explicit provider selection with prefix
claude = get_provider("anthropic:claude-sonnet-4-5")
bedrock = get_provider("bedrock:claude-sonnet-4-5")
vertex = get_provider("vertex:claude-sonnet-4-5")
openai = get_provider("openai:gpt-5")  # GPT-5 flagship with auto-routing
gemini = get_provider("gemini:gemini-2-5-pro")

# Automatic routing (Claude models prefer Bedrock if enabled)
provider = get_provider("claude-sonnet-4-5")  # Uses Bedrock if enabled
result = provider.classify("We need SSO integration")

# Direct model routing
openai_provider = get_provider("gpt-5")  # Routes to OpenAI if enabled (auto-routing Instant/Thinking)
gemini_provider = get_provider("gemini-2-5-flash")  # Routes to Gemini

# Mock provider for testing (zero cost)
mock = get_provider("mock:claude-sonnet")
```

**Provider Benefits:**
- **Bedrock:** Enterprise AWS infrastructure, AWS-native billing, regional data residency
- **Vertex AI:** Google Cloud integration, GCP-native billing, unified GCP experience
- **OpenAI:** Advanced function calling, structured outputs, multimodal
- **Gemini:** 2M token context (Pro), ultra-low cost (Flash Lite), context caching
- **Fallback:** Automatically falls back to direct Anthropic API if cloud providers unavailable

---

## 📖 Usage

### Basic Model Management

```python
from ai_models import get_model, has_vision, has_prompt_caching

# Get model specifications
model = get_model("gpt-5")  # GPT-5 flagship
print(f"Context: {model.metadata.context_window_input:,} tokens")
print(f"Cost: ${model.pricing.input_per_1m}/M input tokens")

# Calculate costs with caching
cost = model.calculate_cost(
    input_tokens=10_000,
    output_tokens=2_000,
    cached_input_tokens=5_000  # 90% discount on cached tokens
)

# Validate capabilities before API calls
if has_vision("gpt-5"):  # GPT-5 has vision capabilities
    process_image()
```

### Finding Budget-Friendly Models

```python
from ai_models import ModelRegistry

budget_models = ModelRegistry.filter_by_cost_tier("budget")
# Returns: Haiku 4.5, GPT-5 mini, GPT-4.1 mini, Gemini 2.5 Flash
```

**Advanced Examples:** [API Documentation](./docs/api-examples.md) | [Production Architecture](./examples/epic-categorization/)

### Provider-Optimized Prompts ✨ ALL PROMPTS MIGRATED

**All 13 production prompts** now have **provider-specific optimizations** for Claude, OpenAI, and Gemini:

```python
from ai_models import get_prompt, get_model, list_prompts

# See all available prompts
prompts = list_prompts()
# Returns: ['analytics/signal-classification', 'developing-internal-tools/claude-md-generator', ...]

# Automatically select best prompt variant for your model
model = get_model("gpt-5")  # GPT-5 default model
prompt = get_prompt("analytics/signal-classification", model=model.id)

# Or explicitly choose a provider optimization
claude_prompt = get_prompt("developing-internal-tools/code-review-refactoring", provider="claude")
openai_prompt = get_prompt("product-strategy/meta-prompt-designer", provider="openai")
gemini_prompt = get_prompt("stakeholder-communication/executive-deck-review", provider="gemini")
```

**Provider-Specific Features:**

| Provider | Key Optimizations | Best For | Cost/1K Operations |
|----------|-------------------|----------|-------------------|
| **Claude** | XML tags, chain-of-thought, caching | Complex reasoning, accuracy | $1-15 |
| **OpenAI** | Auto-routing modes, reasoning (o3/o4), function calling, JSON mode | Coding (4.1), reasoning (o3), general tasks (GPT-5) | $0.15-40 |
| **Gemini** | 2M context, caching, batch processing | High volume, cost optimization | $0.038-5 |

**All 13 Prompts Available:**
- **Analytics:** [signal-classification](./prompts/analytics/signal-classification/)
- **Development:** [claude-md-generator](./prompts/developing-internal-tools/claude-md-generator/), [code-review-refactoring](./prompts/developing-internal-tools/code-review-refactoring/), [enterprise-readme-generator](./prompts/developing-internal-tools/enterprise-readme-generator/), [github-actions-python-cicd](./prompts/developing-internal-tools/github-actions-python-cicd/), [llm-orchestration-system](./prompts/developing-internal-tools/llm-orchestration-system/), [prompt-extraction-cataloging](./prompts/developing-internal-tools/prompt-extraction-cataloging/), [pytest-cicd-optimization](./prompts/developing-internal-tools/pytest-cicd-optimization/), [python-80-percent-test-coverage](./prompts/developing-internal-tools/python-80-percent-test-coverage/)
- **Strategy:** [meta-prompt-designer](./prompts/product-strategy/meta-prompt-designer/), [opus-code-execution-pattern](./prompts/product-strategy/opus-code-execution-pattern/)
- **Communication:** [executive-deck-review](./prompts/stakeholder-communication/executive-deck-review/), [remove-ai-writing-patterns](./prompts/stakeholder-communication/remove-ai-writing-patterns/)

**Total:** 13 prompts × 4 variants (base + Claude + OpenAI + Gemini) = **52 optimized prompt variants**

[→ Learn more about provider-optimized prompts](./docs/provider-specific-prompts.md) | [→ Migration tool](./scripts/migrate_prompts.py)

---

## 🤖 Model Selection Guide

Choose the right model for your workload:

| Model | Input/Output (per 1M) | Context | Best For | Our Usage |
|-------|----------------------|---------|----------|-----------|
| **Claude Haiku 4.5** | $1/$5 | 200K | High-volume classification | 70% |
| **Claude Sonnet 4.5** | $3/$15 | 200K | Production workhorse | 25% |
| **Claude Opus 4.1** | $15/$75 | 200K | High-stakes decisions | 5% |
| **GPT-5** | $3/$12 | 256K | Flagship auto-routing (Instant/Thinking modes) | Default |
| **GPT-5 mini** | $0.20/$0.80 | 128K | Fast, efficient GPT-5 variant | Budget |
| **GPT-4.1** | $2.5/$10 | 200K | Specialized for coding, precise instructions | Coding |
| **GPT-4.1 mini** | $0.15/$0.60 | 128K | Fast coding model, replaced 4o-mini | Budget coding |
| **o3** | $10/$40 | 128K | Advanced reasoning, full tool access | Complex reasoning |
| **o4-mini** | $1/$4 | 128K | Fast, cost-efficient reasoning | Math/coding |
| **GPT-4o** | $2.5/$10 | 128K | Multimodal specialist (voice, vision) | Multimodal |
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
