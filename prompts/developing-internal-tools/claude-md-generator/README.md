# CLAUDE.md Engineering Standards Generator

## ⚠️ Important Clarification

**These prompts are for GENERATING CLAUDE.md files, not for Claude to read.**

This prompt library helps you use **different LLMs** (GPT-6 Luna, Gemini, or Claude itself) to **create** CLAUDE.md files. The resulting CLAUDE.md files are then read by Claude's computer use feature, regardless of which LLM generated them.

```
┌─────────────┐    ┌──────────────────┐    ┌──────────────┐    ┌────────────────┐
│ Your Code   │ →  │ LLM + Provider   │ →  │ CLAUDE.md    │ →  │ Claude Code    │
│             │    │ Prompt           │    │ (generated)  │    │ (reads file)   │
└─────────────┘    └──────────────────┘    └──────────────┘    └────────────────┘
                        ↑
                  (GPT-6 Luna, Gemini,
                   or Claude)
```

**Why use different LLMs for generation?**
- **Scale**: Gemini's 1M context handles entire codebases
- **Quality**: Claude excels at nuanced, complex standards
- **Speed**: GPT-6 Luna provides fast, validated output

## 🎯 Purpose

**Generate CLAUDE.md engineering standards files using various LLMs optimized for different use cases.**

CLAUDE.md files establish development standards, testing requirements, git workflows, and behavioral guidelines for Claude Code sessions. This prompt helps you create comprehensive, project-specific CLAUDE.md files automatically.

**Complexity**: 🔴 Advanced

## 📊 Provider Variants

| Provider | File | Key Features | Best For | Cost/Generation |
|----------|------|-------------|----------|-----------------|
| **Base** | [`prompt.md`](./prompt.md) | Universal compatibility | Any provider, fallback | Varies |
| **Claude** | [`prompt.claude.md`](./prompt.claude.md) | XML tags, chain-of-thought | Generating complex CLAUDE.md with nuanced instructions | $0.01-0.20 |
| **OpenAI** | [`prompt.openai.md`](./prompt.openai.md) | Function calling, JSON mode | Batch generating validated CLAUDE.md files with consistent structure | $0.01 |
| **Gemini** | [`prompt.gemini.md`](./prompt.gemini.md) | 1M context, caching | High-volume CLAUDE.md generation for large codebases | $0.075-0.20 |

*Costs based on typical CLAUDE.md generation (10K-20K tokens output)*

## 🚀 Quick Start

### Automatic Provider Selection

```python
from ai_models import get_prompt, get_model

# Auto-select best variant based on model
model = get_model("gemini-3-8-flash")
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

# Use Gemini for large codebase (cheap + 1M context)
gemini_prompt = get_prompt("developing-internal-tools/claude-md-generator", provider="gemini")

# Use GPT-6 Luna for batch generation with validation
openai_prompt = get_prompt("developing-internal-tools/claude-md-generator", provider="openai")

# Use Claude for highest quality, most nuanced output
claude_prompt = get_prompt("developing-internal-tools/claude-md-generator", provider="claude")
```

## 🎯 When to Use Each Provider for Generation

### Use Claude when:
- ✅ Generating complex CLAUDE.md with nuanced behavioral guidelines
- ✅ Need meta-understanding of what makes good Claude instructions
- ✅ Creating standards for ambiguous or novel domains
- ✅ Budget allows $0.01-0.20 per generation

**Example**: Generating CLAUDE.md for a cutting-edge ML research project with novel patterns

### Use OpenAI when:
- ✅ Batch generating CLAUDE.md files for multiple similar projects
- ✅ Need strict schema validation for consistency
- ✅ Want reproducible results (seed parameter)
- ✅ Budget-conscious: GPT-6 Luna at $0.01 per generation

**Example**: Creating standardized CLAUDE.md files for 50 microservices

### Use Gemini when:
- ✅ Generating CLAUDE.md for very large codebases (1M context window)
- ✅ Ultra-high volume: 100+ CLAUDE.md files per day
- ✅ Cost is critical: ~$0.075 with gemini-3-8-flash
- ✅ Can batch multiple projects in single request

**Example**: Analyzing entire monorepo (500K+ LOC) to generate comprehensive CLAUDE.md

## 💡 Common Misconceptions

### ❌ Misconception 1
**"These prompts are for Claude to read different file formats"**

✅ **Reality**: These prompts help different LLMs **generate** CLAUDE.md files. Claude always reads the standard CLAUDE.md format, regardless of which LLM created it.

### ❌ Misconception 2
**"I need the OpenAI variant if I want Claude to work with OpenAI APIs"**

✅ **Reality**: You use the OpenAI variant when you want **GPT-6 Luna to generate** your CLAUDE.md file. The generated file works with Claude regardless.

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

# Use Gemini 1M context to analyze entire codebase
model = genai.GenerativeModel("gemini-3.8-flash")
prompt = get_prompt("developing-internal-tools/claude-md-generator", provider="gemini")

# Include entire codebase context (up to 1M tokens)
codebase_summary = analyze_codebase()  # Your function

claude_md = model.generate_content(
    prompt.format(
        codebase_summary=codebase_summary,
        project_type="E-commerce monorepo",
        tech_stack="React, Node.js, PostgreSQL, Redis, Kubernetes"
    )
).text

# Cost: ~$0.075
save_file(".claude/CLAUDE.md", claude_md)
```

### Example 2: Batch Generation with GPT-6 Luna

```python
from ai_models import get_prompt
import openai

# Generate CLAUDE.md for 50 microservices
model = openai.ChatCompletion
prompt = get_prompt("developing-internal-tools/claude-md-generator", provider="openai")

for service in microservices:
    response = model.create(
        model="gpt-6-luna",  # $0.01 per generation
        messages=[{"role": "user", "content": prompt.format(
            project_type=f"Microservice: {service.name}",
            tech_stack=service.stack,
            team_size=2
        )}],
        temperature=0.0  # Consistent output
    )

    save_file(f"{service.path}/.claude/CLAUDE.md", response.choices[0].message.content)

# Total cost: 50 × $0.01 = $0.50 vs $10.00 with GPT-6.1 Sol
```

### Example 3: High-Quality Generation with Claude

```python
from ai_models import get_prompt
from pm_prompt_toolkit.providers import get_provider

# Use Claude for highest quality output
provider = get_provider("claude-sonnet-5-5")
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

# Cost: ~$0.20 but highest quality
save_file(".claude/CLAUDE.md", claude_md)
```

## 🔧 Latest Model Recommendations

### OpenAI Models (Updated Oct 2026)

| Model | Cost/1M | Best For | Generation Cost |
|-------|---------|----------|-----------------|
| **gpt-6-luna** | $0.10/$0.50 | High-volume, budget, balanced quality | $0.01 |

### Gemini Models (Updated Oct 2026)

| Model | Cost/1M | Best For | Generation Cost |
|-------|---------|----------|-----------------|
| **gemini-3-8-flash** | $0.75/$3.75 | Production, balanced, high-volume | $0.075 |
| **gemini-4-argon** | $2.00/$10.00 | Large context, quality | $0.20 |

### Claude Models

| Model | Cost/1M | Best For | Generation Cost |
|-------|---------|----------|-----------------|
| **claude-haiku-5-5** | $0.10/$0.50 | Fast, cost-effective | $0.01 |
| **claude-sonnet-5-5** | $2/$10 | Best quality | $0.20 |

*Generation costs assume 20K token output (typical CLAUDE.md file)*

## 🎯 Provider Selection Guide

```
┌─────────────────────────────────────────────────────────────┐
│                    Choose Your Provider                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Need to analyze huge codebase (>100K LOC)?                 │
│  → Gemini 4 Argon (1M context)                              │
│                                                              │
│  Generating 50+ files on a tight budget?                    │
│  → Gemini 3.8 Flash                                         │
│                                                              │
│  Need batch generation with validation?                     │
│  → GPT-6 Luna ($0.01 each)                                  │
│                                                              │
│  Complex project with unique requirements?                  │
│  → Claude Sonnet 5.5 (highest quality)                      │
│                                                              │
│  Prototyping or learning?                                   │
│  → Gemini 3.8 Flash                                         │
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

1. **Start Cheap**: Use `gemini-3-8-flash` for experimentation
2. **Batch Smart**: Generate 10-50 CLAUDE.md files with GPT-6 Luna in one go
3. **Cache Context**: With Gemini 4 Argon, cache your codebase analysis
4. **Iterate Cheap**: Refine prompts with cheap models before using premium
5. **Mix & Match**: Use Gemini to generate, Claude to refine, GPT to batch-produce

## ❓ FAQ

**Q: Which LLM should I use to generate CLAUDE.md files?**
A: For most cases, start with `gemini-3-8-flash`. Upgrade to Claude Sonnet if quality issues arise.

**Q: Will Claude work differently based on which LLM generated the file?**
A: No. Claude reads the same CLAUDE.md format regardless of generator. Choose based on generation needs, not execution.

**Q: Can I edit the generated CLAUDE.md file?**
A: Absolutely! Generated files are starting points. Edit to match your exact needs.

**Q: How often should I regenerate CLAUDE.md?**
A: Regenerate when project scope, tech stack, or team practices change significantly. Otherwise, manually update.

---

*Documentation updated November 2025 with latest model versions and pricing*
