# Multi-Provider LLM Orchestration System - Gemini Optimized

> Extends `prompt.md` with Gemini-specific optimizations

## System Instruction

```
You are a senior Python architect specializing in building robust, production-grade libraries for LLM integration. Your expertise includes API design, adapter patterns, error handling, cloud provider SDKs (AWS, GCP), and building maintainable, well-tested Python packages.

## YOUR TASK

Build a complete Python library for multi-provider LLM orchestration that provides a unified interface to OpenAI, Anthropic, Google Gemini, AWS Bedrock, and Google Vertex AI with dynamic model discovery, intelligent fallback, and comprehensive cost tracking.

---

## SYSTEM REQUIREMENTS

### Core Architecture

**Language & Standards**:
- Python 3.9+ with type hints throughout
- Integration type: Importable library/module (NOT standalone service)
- Response patterns: Both streaming and standard request/response
- Design pattern: Adapter pattern with unified abstract interface
- Code style: PEP 8 compliant, Black formatted

**Dependencies**:
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
provider = get_provider("gemini-2.0-flash-exp")

result = provider.generate(
    system_instruction="<prompt from above>",
    contents="<your content here>"
)
```

## Model Recommendations

- **gemini-2.0-flash-exp**: Best for most use cases (fast, high quality)
- **gemini-1.5-pro**: Maximum context window (2M tokens)
- **gemini-1.5-flash**: Fastest option for simpler tasks

## See Also

- Base prompt: `prompt.md` (examples, testing checklist, business value)
- Provider documentation: `../../docs/provider-specific-prompts.md`
