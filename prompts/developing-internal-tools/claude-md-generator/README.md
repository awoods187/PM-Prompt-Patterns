# CLAUDE.md Engineering Standards Generator

## ⚠️ Important Clarification

**These prompts are for GENERATING CLAUDE.md files, not for Claude to read.**

This prompt library helps you use **different LLMs** (GPT-4o, Gemini, or Claude itself) to **create** CLAUDE.md files. The resulting CLAUDE.md files are then read by Claude's computer use feature, regardless of which LLM generated them.

```
┌─────────────┐    ┌──────────────────┐    ┌──────────────┐    ┌────────────────┐
│ Your Code   │ →  │ LLM + Provider   │ →  │ CLAUDE.md    │ →  │ Claude Code    │
│             │    │ Prompt           │    │ (generated)  │    │ (reads file)   │
└─────────────┘    └──────────────────┘    └──────────────┘    └────────────────┘
                        ↑
                  (GPT-4o, Gemini,
                   or Claude)
```

**Why use different LLMs for generation?**
- **Cost**: Gemini is 10-50x cheaper for bulk generation
- **Scale**: Gemini's 2M context handles entire codebases
- **Quality**: Claude excels at nuanced, complex standards
- **Speed**: GPT-4o-mini provides fast, validated output

## 🎯 Purpose

**Generate CLAUDE.md engineering standards files using various LLMs optimized for different use cases.**

CLAUDE.md files establish development standards, testing requirements, git workflows, and behavioral guidelines for Claude Code sessions. This prompt helps you create comprehensive, project-specific CLAUDE.md files automatically.

**Complexity**: 🔴 Advanced

## 📊 Provider Variants

| Provider | File | Key Features | Best For | Cost/Generation |
|----------|------|-------------|----------|-----------------|
| **Base** | [`prompt.md`](./prompt.md) | Universal compatibility | Any provider, fallback | Varies |
| **Claude** | [`prompt.claude.md`](./prompt.claude.md) | XML tags, chain-of-thought | Generating complex CLAUDE.md with nuanced instructions | $0.03-0.15 |
| **OpenAI** | [`prompt.openai.md`](./prompt.openai.md) | Function calling, JSON mode | Batch generating validated CLAUDE.md files with consistent structure | $0.002-0.02 |
| **Gemini** | [`prompt.gemini.md`](./prompt.gemini.md) | 2M context, caching | High-volume CLAUDE.md generation for large codebases | $0.0004-0.005 |

*Costs based on typical CLAUDE.md generation (10K-20K tokens output)*

## 🚀 Quick Start

### Automatic Provider Selection

```python
from ai_models import get_prompt, get_model

# Auto-select best variant based on model
model = get_model("gemini-2.0-flash-exp")  # Free experimental
prompt = get_prompt("developing-internal-tools/claude-md-generator", model=model.id)

# Generate CLAUDE.md content
claude_md_content = model.generate(prompt.format(
    project_type="Python web API",
    tech_stack="FastAPI, PostgreSQL, Redis",
    team_size=5
))

# Save to file for Claude to read
with open(".claude/CLAUDE.md", "w") as f:
    f.write(claude_md_content)
```

### Manual Provider Selection

```python
from ai_models import get_prompt

# Use Gemini for large codebase (cheap + 2M context)
gemini_prompt = get_prompt("developing-internal-tools/claude-md-generator", provider="gemini")

# Use GPT-4o for batch generation with validation
openai_prompt = get_prompt("developing-internal-tools/claude-md-generator", provider="openai")

# Use Claude for highest quality, most nuanced output
claude_prompt = get_prompt("developing-internal-tools/claude-md-generator", provider="claude")
```

## 🎯 When to Use Each Provider for Generation

### Use Claude when:
- ✅ Generating complex CLAUDE.md with nuanced behavioral guidelines
- ✅ Need meta-understanding of what makes good Claude instructions
- ✅ Creating standards for ambiguous or novel domains
- ✅ Budget allows $0.03-0.15 per generation

**Example**: Generating CLAUDE.md for a cutting-edge ML research project with novel patterns

### Use OpenAI when:
- ✅ Batch generating CLAUDE.md files for multiple similar projects
- ✅ Need strict schema validation for consistency
- ✅ Want reproducible results (seed parameter)
- ✅ Budget-conscious: GPT-4o-mini at $0.002 per generation

**Example**: Creating standardized CLAUDE.md files for 50 microservices

### Use Gemini when:
- ✅ Generating CLAUDE.md for very large codebases (2M context window)
- ✅ Ultra-high volume: 100+ CLAUDE.md files per day
- ✅ Cost is critical: $0.0004 with gemini-2.0-flash-exp (free experimental)
- ✅ Can batch multiple projects in single request

**Example**: Analyzing entire monorepo (500K+ LOC) to generate comprehensive CLAUDE.md

## 💡 Common Misconceptions

### ❌ Misconception 1
**"These prompts are for Claude to read different file formats"**

✅ **Reality**: These prompts help different LLMs **generate** CLAUDE.md files. Claude always reads the standard CLAUDE.md format, regardless of which LLM created it.

### ❌ Misconception 2
**"I need the OpenAI variant if I want Claude to work with OpenAI APIs"**

✅ **Reality**: You use the OpenAI variant when you want **GPT-4o to generate** your CLAUDE.md file. The generated file works with Claude regardless.

### ❌ Misconception 3
**"Provider-specific prompts produce different CLAUDE.md formats"**

✅ **Reality**: All providers generate standard CLAUDE.md markdown files. The prompts optimize **how each LLM generates**, not the output format.

### ❌ Misconception 4
**"I should use the same provider for generation and execution"**

✅ **Reality**: It's perfectly fine (and often optimal) to use Gemini to generate a CLAUDE.md file that Claude will read. Choose based on generation requirements, not execution.

## 📚 Real-World Examples

### Example 1: Large Monorepo with Gemini

```python
from ai_models import get_prompt
import google.generativeai as genai

# Use Gemini 2M context to analyze entire codebase
model = genai.GenerativeModel("gemini-2.0-flash-exp")  # Free!
prompt = get_prompt("developing-internal-tools/claude-md-generator", provider="gemini")

# Include entire codebase context (up to 2M tokens)
codebase_summary = analyze_codebase()  # Your function

claude_md = model.generate_content(
    prompt.format(
        codebase_summary=codebase_summary,
        project_type="E-commerce monorepo",
        tech_stack="React, Node.js, PostgreSQL, Redis, Kubernetes"
    )
).text

# Cost: ~$0 (free experimental) vs $2-10 with other providers
save_file(".claude/CLAUDE.md", claude_md)
```

### Example 2: Batch Generation with GPT-4o-mini

```python
from ai_models import get_prompt
import openai

# Generate CLAUDE.md for 50 microservices
model = openai.ChatCompletion
prompt = get_prompt("developing-internal-tools/claude-md-generator", provider="openai")

for service in microservices:
    response = model.create(
        model="gpt-4o-mini",  # $0.002 per generation
        messages=[{"role": "user", "content": prompt.format(
            project_type=f"Microservice: {service.name}",
            tech_stack=service.stack,
            team_size=2
        )}],
        temperature=0.0  # Consistent output
    )

    save_file(f"{service.path}/.claude/CLAUDE.md", response.choices[0].message.content)

# Total cost: 50 × $0.002 = $0.10 vs $1.50 with GPT-4o
```

### Example 3: High-Quality Generation with Claude

```python
from ai_models import get_prompt
from pm_prompt_toolkit.providers import get_provider

# Use Claude for highest quality output
provider = get_provider("claude-sonnet-4-5")
prompt = get_prompt("developing-internal-tools/claude-md-generator", provider="claude")

# Generate nuanced CLAUDE.md for complex project
claude_md = provider.generate(
    prompt.format(
        project_type="ML research platform",
        tech_stack="PyTorch, Ray, PostgreSQL, FastAPI",
        team_size=15,
        compliance_requirements="HIPAA, SOC2"
    )
)

# Cost: ~$0.06 but highest quality
save_file(".claude/CLAUDE.md", claude_md)
```

## 🔧 Latest Model Recommendations

### OpenAI Models (Updated Nov 2025)

| Model | Cost/1M | Best For | Generation Cost |
|-------|---------|----------|-----------------|
| **gpt-4o-mini** | $0.15/$0.60 | High-volume, budget | $0.002 |
| **gpt-4o** | $2.50/$10.00 | Balanced quality | $0.02 |

### Gemini Models (Updated Nov 2025)

| Model | Cost/1M | Best For | Generation Cost |
|-------|---------|----------|-----------------|
| **gemini-2.0-flash-exp** | $0/$0 (free!) | Experimentation, high-volume | $0 |
| **gemini-2-5-flash** | $0.075/$0.30 | Production, balanced | $0.0015 |
| **gemini-2-5-pro** | $1.25/$5.00 | Large context, quality | $0.005 |

### Claude Models

| Model | Cost/1M | Best For | Generation Cost |
|-------|---------|----------|-----------------|
| **claude-haiku-4.5** | $1/$5 | Fast, cost-effective | $0.03 |
| **claude-sonnet-4.5** | $3/$15 | Best quality | $0.06 |

*Generation costs assume 20K token output (typical CLAUDE.md file)*

## 🎯 Provider Selection Guide

```
┌─────────────────────────────────────────────────────────────┐
│                    Choose Your Provider                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Need to analyze huge codebase (>100K LOC)?                 │
│  → Gemini 2.5 Pro (2M context)                              │
│                                                              │
│  Generating 50+ files? Want them all free?                  │
│  → Gemini 2.0 Flash Exp (experimental, free)                │
│                                                              │
│  Need batch generation with validation?                     │
│  → GPT-4o-mini ($0.002 each)                                │
│                                                              │
│  Complex project with unique requirements?                  │
│  → Claude Sonnet 4.5 (highest quality)                      │
│                                                              │
│  Prototyping or learning?                                   │
│  → Gemini 2.0 Flash Exp (free!)                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 📝 What Gets Generated

All providers generate standard CLAUDE.md files containing:

- 🎯 Core development principles (TDD, DRY, SOLID)
- 🧪 Testing standards and coverage requirements
- 🔐 Security guidelines (OWASP Top 10 prevention)
- 🐛 Bug fix protocols and root cause analysis
- 💬 Communication standards and escalation paths
- 🔒 Execution safety rules (dangerous operations)
- 📚 Documentation requirements
- ⚡ Performance considerations
- 🎨 Project-specific adaptations

**The only difference is HOW they generate, not WHAT they generate.**

## 🔗 Related Prompts

- [Code Review & Refactoring](../code-review-refactoring/) - Review existing code
- [Enterprise README Generator](../enterprise-readme-generator/) - Create project READMEs
- [GitHub Actions CI/CD](../github-actions-python-cicd/) - Generate workflow files

## 📚 Additional Resources

See the individual prompt files for provider-specific usage:
- [Base Prompt](./prompt.md) - Universal examples
- [Claude Variant](./prompt.claude.md) - XML format, best quality
- [OpenAI Variant](./prompt.openai.md) - Function calling, batch processing
- [Gemini Variant](./prompt.gemini.md) - Large context, ultra-low cost

For detailed optimization strategies:
- [Provider-Specific Prompts Guide](../../docs/provider-specific-prompts.md)

---

## 💡 Pro Tips

1. **Start Free**: Use `gemini-2.0-flash-exp` for experimentation (it's free!)
2. **Batch Smart**: Generate 10-50 CLAUDE.md files with GPT-4o-mini in one go
3. **Cache Context**: With Gemini 2.5 Pro, cache your codebase analysis for 74% savings
4. **Iterate Cheap**: Refine prompts with free/cheap models before using premium
5. **Mix & Match**: Use Gemini to generate, Claude to refine, GPT to batch-produce

## ❓ FAQ

**Q: Which LLM should I use to generate CLAUDE.md files?**
A: For most cases, start with `gemini-2.0-flash-exp` (free). Upgrade to Claude Sonnet if quality issues arise.

**Q: Will Claude work differently based on which LLM generated the file?**
A: No. Claude reads the same CLAUDE.md format regardless of generator. Choose based on generation needs, not execution.

**Q: Can I edit the generated CLAUDE.md file?**
A: Absolutely! Generated files are starting points. Edit to match your exact needs.

**Q: How often should I regenerate CLAUDE.md?**
A: Regenerate when project scope, tech stack, or team practices change significantly. Otherwise, manually update.

---

*Documentation updated November 2025 with latest model versions and pricing*
