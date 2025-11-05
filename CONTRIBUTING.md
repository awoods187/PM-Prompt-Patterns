# Contributing to PM Prompt Patterns

Thank you for your interest in contributing! This guide will help you add new prompts or improve existing ones while following our library standards.

---

## Quick Start

### Adding a New Prompt

**Option 1: Use the Interactive Script (Recommended)**

```bash
python scripts/create_new_prompt.py
```

This script will:
- Guide you through metadata collection
- Ask for prompt content
- Generate all 4 required files (base + 3 model-specific)
- Validate the structure automatically

**Option 2: Manual Creation**

1. Copy the template:
   ```bash
   cp templates/new-prompt-template.md prompts/category/your-prompt-name/prompt.md
   ```

2. Fill in the template following the structure guide

3. Generate model-specific files using the script:
   ```bash
   python scripts/restructure_prompts_v2.py
   ```

---

## File Structure Requirements

Each prompt pattern **MUST** have these 4 files:

### 1. `prompt.md` (Base Prompt)

**Purpose**: Model-agnostic base with all content

**Required sections**:
- Title and metadata (complexity, category, compatibility)
- Overview
- Business value
- Use cases
- Production metrics
- The prompt itself (in code block)
- Production patterns
- Quality evaluation
- Usage notes
- Common issues & fixes
- Related prompts

**Key rules**:
- ✅ NO model-specific syntax (no XML tags like `<task>`, no function schemas)
- ✅ Include ALL examples and patterns
- ✅ Self-contained and copy/paste ready
- ✅ Works with any LLM provider

### 2. `prompt.claude.md` (Claude Optimized)

**Purpose**: Claude-specific wrapper with optimizations

**Structure**:
```markdown
# [Name] - Claude Optimized

> Extends `prompt.md` with Claude-specific optimizations

## Prompt

<task>
[FULL PROMPT CONTENT HERE]
</task>

## Claude Optimizations Applied
[List of optimizations]

## Usage
[Code example]

## See Also
[Reference to base prompt]
```

**Key rules**:
- ✅ Wrap prompt in `<task>` tags
- ✅ Include FULL prompt (not just diff)
- ✅ NO duplicate examples (reference base)
- ❌ NO mentions of OpenAI or Gemini

### 3. `prompt.openai.md` (OpenAI Optimized)

**Purpose**: OpenAI-specific optimizations

**Structure**:
```markdown
# [Name] - OpenAI Optimized

> Extends `prompt.md` with OpenAI-specific optimizations

## System Prompt

```
[FULL PROMPT CONTENT HERE]
```

## OpenAI Optimizations Applied
[List of optimizations]

## Usage
[Code example]

## Model Recommendations
[Which GPT models to use]

## See Also
[Reference to base prompt]
```

**Key rules**:
- ✅ Format for OpenAI system message
- ✅ Include FULL prompt (not just diff)
- ✅ Optional function calling schema
- ❌ NO mentions of Claude or Gemini

### 4. `prompt.gemini.md` (Gemini Optimized)

**Purpose**: Gemini-specific optimizations

**Structure**: Similar to OpenAI but with:
- `## System Instruction` instead of `## System Prompt`
- Gemini-specific model recommendations
- Multimodal usage notes if applicable

---

## Quality Checklist

Before submitting your prompt, verify:

### Structure
- [ ] All 4 files exist (`prompt.md`, `prompt.claude.md`, `prompt.openai.md`, `prompt.gemini.md`)
- [ ] Base prompt is model-agnostic (no `<task>` tags, no XML)
- [ ] Model files contain FULL prompt (copy/paste ready)
- [ ] No duplicate examples across files
- [ ] Each model file only references its own model

### Content
- [ ] Clear, descriptive title
- [ ] Complexity level assigned (🟢/🟡/🔴)
- [ ] 1-2 sentence overview
- [ ] Business value clearly stated
- [ ] Use cases listed
- [ ] Production metrics included (if available)
- [ ] Prompt is clear and actionable
- [ ] At least one production pattern example
- [ ] Usage notes included

### Validation
- [ ] Run validation script:
  ```bash
  python scripts/create_new_prompt.py  # Will validate at the end
  ```
- [ ] Test with at least one model to verify it works
- [ ] Examples produce expected output
- [ ] No obvious errors or typos

---

## Style Guidelines

### Naming Conventions

**File/Directory Names**:
- Use lowercase
- Use hyphens for spaces
- Be descriptive
- Example: `api-documentation-generator`

**Prompt Titles**:
- Use Title Case
- Be descriptive and specific
- Example: "API Documentation Generator"

### Writing Style

**For Prompts**:
- Be direct and imperative
- Use numbered lists for steps
- Provide clear examples
- Avoid ambiguity

**For Documentation**:
- Be concise
- Use active voice
- Include real-world examples
- Explain the "why" not just "what"

### Code Examples

```python
# ✅ Good: Clear, complete, works out of the box
from pm_prompt_toolkit.providers import get_provider

provider = get_provider("claude-sonnet-4-5")
result = provider.generate(
    system_prompt="Your prompt here",
    user_message="User input here"
)
print(result)
```

```python
# ❌ Bad: Incomplete, unclear, won't run
provider.generate(prompt, input)
```

---

## Testing Your Prompt

### Manual Testing

1. **Test with multiple models**:
   ```python
   from pm_prompt_toolkit.providers import get_provider

   models = ["claude-sonnet-4-5", "gpt-4o", "gemini-2.0-flash-exp"]

   for model_name in models:
       provider = get_provider(model_name)
       result = provider.generate(
           system_prompt=your_prompt,
           user_message=test_input
       )
       print(f"{model_name}: {result[:100]}")
   ```

2. **Verify output quality**:
   - Does it follow instructions?
   - Is the format correct?
   - Are all required fields present?

3. **Test edge cases**:
   - Empty input
   - Very long input
   - Ambiguous input
   - Invalid input

### Automated Testing

```bash
# Run library tests to ensure nothing broke
pytest tests/test_prompts.py -v

# Lint your files
black scripts/
ruff check .
```

---

## Submitting Your Contribution

### 1. Create a Branch

```bash
git checkout -b add-prompt-[your-prompt-name]
```

### 2. Add Your Files

```bash
git add prompts/category/your-prompt-name/
```

### 3. Commit

```bash
git commit -m "feat: Add [your prompt name] prompt pattern

- Brief description of what the prompt does
- Why it's useful
- Any special considerations"
```

### 4. Push and Create PR

```bash
git push origin add-prompt-[your-prompt-name]
gh pr create --title "Add [Your Prompt Name] prompt pattern" \
  --body "Description of the prompt and its use cases"
```

### 5. PR Checklist

Your PR description should include:

- [ ] Prompt name and category
- [ ] Brief description of what it does
- [ ] Why this prompt is useful (business value)
- [ ] Tested with at least one model
- [ ] All 4 files present and validated
- [ ] Follows library structure guidelines

---

## Updating Existing Prompts

### For Content Changes

1. **Edit ONLY `prompt.md`** for:
   - Prompt logic changes
   - New examples
   - Updated business metrics
   - Additional use cases

2. **Update model-specific files** if needed:
   - Run: `python scripts/restructure_prompts_v2.py`
   - Or manually update optimization notes

### For Model-Specific Optimizations

1. Edit the specific model file (`prompt.claude.md`, `prompt.openai.md`, or `prompt.gemini.md`)
2. Update optimization notes
3. Test with that model to verify

### Version Bumping

When making significant changes:

```markdown
## Version History

**v1.1** (2025-11-05)
- Improved clarity in step 3
- Added example for edge case handling
- Updated production metrics
```

---

## Common Patterns

### Multi-Step Prompts

For prompts with multiple sequential steps:

```
You are a [role]. Follow these steps:

## Step 1: [Action]
[Details]

## Step 2: [Action]
[Details]

## Step 3: [Action]
[Details]

Provide output in this format:
[Format specification]
```

### Classification Prompts

For categorization tasks:

```
You are a classifier. Categorize the input into ONE of these categories:

1. **CATEGORY_A**: Description
   - Indicators: [list]

2. **CATEGORY_B**: Description
   - Indicators: [list]

Output format:
Category: [CATEGORY_NAME]
Confidence: [0.0-1.0]
Reasoning: [Brief explanation]
```

### Generation Prompts

For content creation:

```
You are a [type] generator. Create [output type] that:

Requirements:
1. [Requirement 1]
2. [Requirement 2]

Style guidelines:
- [Guideline 1]
- [Guideline 2]

Output the result in [format].
```

---

## Getting Help

- **Documentation**: See `docs/prompt-structure-guide.md` for detailed structure guidelines
- **Examples**: Browse existing prompts in `prompts/` for inspiration
- **Questions**: Open an issue with the `question` label

---

## Code of Conduct

- Be respectful and constructive
- Focus on what's best for the community
- Help others learn and improve
- Give credit where credit is due

---

## Thank You!

Your contributions help make this library more valuable for everyone. We appreciate your time and effort! 🙏
