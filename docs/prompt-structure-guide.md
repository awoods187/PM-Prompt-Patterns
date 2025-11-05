# Prompt Structure Guide

**Last Updated:** 2025-11-05
**Purpose:** Define the standard structure for prompt pattern files in this library

---

## Overview

This library uses a three-file structure for each prompt pattern to eliminate duplication while providing model-specific optimizations:

1. **`prompt.md`** - Base prompt (model-agnostic)
2. **`prompt.claude.md`** - Claude-optimized version
3. **`prompt.openai.md`** - OpenAI-optimized version
4. **`prompt.gemini.md`** - Gemini-optimized version

This structure reduces duplication by ~80% while maintaining copy/paste-ready model-specific files.

---

## File Structure

### 1. `prompt.md` (Base Prompt)

**Purpose:** Model-agnostic base prompt with all examples, patterns, and business context.

**Structure:**
```markdown
# [Prompt Title]

**Complexity**: [🟢 Beginner | 🟡 Intermediate | 🔴 Advanced]
**Category**: [Category Name]
**Model Compatibility**: [Compatibility notes]

## Overview

[Brief description of what this prompt does]

**Business Value**:
- [Value point 1]
- [Value point 2]

**Use Cases**:
- [Use case 1]
- [Use case 2]

**Production metrics**:
- [Metric 1]
- [Metric 2]

---

## Prompt

```
[The actual prompt content - model-agnostic, no XML/special syntax]
```

---

## Production Patterns

[Examples of using this prompt in production scenarios]

---

## Quality Evaluation

[How to evaluate if the prompt is working well]

---

## Cost Comparison

[Cost analysis across providers if applicable]

---

## Usage Notes

[Tips for using this prompt effectively]

---

## Common Issues & Fixes

[Known issues and their solutions]

---

## Related Prompts

[Links to related prompt patterns]
```

**Key Requirements:**
- ✅ NO model-specific syntax (no XML tags, no function schemas)
- ✅ Include ALL examples and patterns
- ✅ Include business value, metrics, use cases
- ✅ Include testing/quality checklist
- ✅ Self-contained and copy/paste ready
- ✅ Works with any LLM provider

---

### 2. `prompt.claude.md` (Claude-Optimized)

**Purpose:** Claude-specific optimizations with the full prompt ready to copy/paste.

**Structure:**
```markdown
# [Prompt Title] - Claude Optimized

> Extends `prompt.md` with Claude-specific optimizations

## Prompt

<task>
[FULL PROMPT CONTENT - wrapped in Claude's XML structure]
</task>

## Claude Optimizations Applied

- **XML structure**: Uses XML tags for clear task delineation
- **Structured thinking**: Encourages `<thinking>` tags for complex reasoning
- **Prompt caching**: Static content is cacheable for cost savings
- **Extended context**: Leverages Claude's 200K token context window

## Usage

```python
from pm_prompt_toolkit.providers import get_provider

# Initialize Claude provider with caching
provider = get_provider("claude-sonnet-4-5", enable_caching=True)

result = provider.generate(
    system_prompt="<prompt from above>",
    user_message="<your content here>"
)
```

## See Also

- Base prompt: `prompt.md` (examples, testing checklist, business value)
- Provider documentation: `../../docs/provider-specific-prompts.md`
```

**Key Requirements:**
- ✅ Brief header explaining relationship to base
- ✅ FULL prompt content (not just diff/modifications)
- ✅ Claude-specific XML wrapping where appropriate
- ✅ NO duplicate examples (reference main file)
- ✅ NO model cross-contamination (no OpenAI/Gemini mentions)
- ✅ Copy/paste ready

---

### 3. `prompt.openai.md` (OpenAI-Optimized)

**Purpose:** OpenAI-specific optimizations with the full prompt ready to copy/paste.

**Structure:**
```markdown
# [Prompt Title] - OpenAI Optimized

> Extends `prompt.md` with OpenAI-specific optimizations

## System Prompt

```
[FULL PROMPT CONTENT - formatted for OpenAI's system message]
```

## OpenAI Optimizations Applied

- **Clear role definition**: Explicit system message with responsibilities
- **Structured output**: Consistent formatting instructions
- **Function calling ready**: Can combine with function schemas
- **Concise directives**: Optimized for GPT-4's instruction-following

## Usage

```python
from pm_prompt_toolkit.providers import get_provider

# Initialize OpenAI provider
provider = get_provider("gpt-4o")

result = provider.generate(
    system_prompt="<prompt from above>",
    user_message="<your content here>"
)
```

## Model Recommendations

- **gpt-4o**: Best balance of speed, quality, and cost
- **gpt-4o-mini**: Faster and more cost-effective for simpler tasks
- **gpt-4-turbo**: Use for extended context needs (>128k tokens)

## See Also

- Base prompt: `prompt.md` (examples, testing checklist, business value)
- Provider documentation: `../../docs/provider-specific-prompts.md`
```

**Key Requirements:**
- ✅ Brief header explaining relationship to base
- ✅ FULL prompt content (not just diff/modifications)
- ✅ OpenAI-specific formatting
- ✅ Optional function calling schema
- ✅ NO duplicate examples (reference main file)
- ✅ NO model cross-contamination (no Claude/Gemini mentions)
- ✅ Copy/paste ready

---

### 4. `prompt.gemini.md` (Gemini-Optimized)

**Purpose:** Gemini-specific optimizations with the full prompt ready to copy/paste.

**Structure:**
```markdown
# [Prompt Title] - Gemini Optimized

> Extends `prompt.md` with Gemini-specific optimizations

## System Instruction

```
[FULL PROMPT CONTENT - formatted for Gemini]
```

## Gemini Optimizations Applied

- **Clear directives**: Explicit, numbered instructions
- **Context utilization**: Optimized for Gemini's large context window
- **Multimodal ready**: Can process code + diagrams/screenshots
- **Structured reasoning**: Step-by-step breakdown for complex tasks

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
```

**Key Requirements:**
- ✅ Brief header explaining relationship to base
- ✅ FULL prompt content (not just diff/modifications)
- ✅ Gemini-specific formatting
- ✅ NO duplicate examples (reference main file)
- ✅ NO model cross-contamination (no Claude/OpenAI mentions)
- ✅ Copy/paste ready

---

## Benefits of This Structure

### 1. Eliminates Duplication
- **Before:** 4 files × 1,400 lines = 5,600 lines total
- **After:** 1 base (450 lines) + 3 small (110 lines each) = 780 lines total
- **Reduction:** ~86% fewer lines to maintain

### 2. Clear Hierarchy
- Base prompt (`prompt.md`) is the source of truth
- Model-specific files are clearly labeled as extensions
- No confusion about which file to edit for content changes

### 3. Easier Maintenance
- Examples only need updating in one place (`prompt.md`)
- Business metrics only need updating in one place
- Model-specific optimizations isolated and easy to find

### 4. Copy/Paste Ready
- Each file is self-contained and immediately usable
- No need to cobble together multiple sources
- Clear usage examples in each model-specific file

### 5. No Cross-Contamination
- Claude file has no references to OpenAI or Gemini
- OpenAI file has no references to Claude or Gemini
- Each file is optimized specifically for its target model

---

## Creating New Prompts

When creating a new prompt pattern:

1. **Start with `prompt.md`**
   - Write the complete base prompt
   - Add all examples and patterns
   - Include business value and metrics
   - Make it model-agnostic

2. **Create `prompt.claude.md`**
   - Copy the core prompt content
   - Wrap in appropriate XML tags (`<task>`, etc.)
   - Add Claude usage example
   - Reference base file for examples

3. **Create `prompt.openai.md`**
   - Copy the core prompt content
   - Format for OpenAI's system message structure
   - Add function calling schema if applicable
   - Add OpenAI usage example
   - Reference base file for examples

4. **Create `prompt.gemini.md`**
   - Copy the core prompt content
   - Format for Gemini's system instruction
   - Add Gemini usage example
   - Reference base file for examples

---

## Quality Checklist

Before committing a new or updated prompt:

- [ ] Base prompt (`prompt.md`) is model-agnostic (no XML, no provider mentions)
- [ ] Each model file contains the FULL prompt (copy/paste ready)
- [ ] No duplicate examples across files
- [ ] No model cross-contamination (each file only mentions its own model)
- [ ] Each model file clearly states it extends the base
- [ ] Usage examples are present and correct for each model
- [ ] File sizes are reasonable (base is largest, model files are small)

---

## Automated Restructuring

If you have old-style prompts with massive duplication, use the restructuring script:

```bash
python scripts/restructure_prompts_v2.py
```

This will:
1. Extract the base prompt content
2. Create clean base `prompt.md` files
3. Generate minimal model-specific files
4. Create backups (`.bak`) of originals
5. Reduce total code by ~80%

---

## See Also

- [Provider-Specific Prompts Guide](./provider-specific-prompts.md)
- [Prompt Design Principles](./prompt_design_principles.md)
- [Contributing Guide](../CONTRIBUTING.md)
