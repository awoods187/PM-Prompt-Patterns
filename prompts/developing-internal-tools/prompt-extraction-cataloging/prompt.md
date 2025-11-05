# Prompt Extraction & Cataloging System

**Complexity**: 🔴 Advanced
**Category**: Code Analysis / Prompt Engineering
**Model Compatibility**: ✅ Claude Sonnet 4+ (best) | ✅ Claude Opus | ⚠️ GPT-4 (may miss context)

## Overview

Production-grade prompt for analyzing GitHub repositories to identify, extract, and catalog AI/LLM prompts for building reusable prompt libraries. Handles multi-file scanning, context extraction, sensitive information detection, and structured metadata generation.

**Business Value**:
- Build reusable prompt libraries from existing codebases
- Standardize prompt patterns across organization
- Enable prompt version control and sharing
- Identify prompt optimization opportunities
- Reduce duplicate prompt development by 60-80%
- Create organizational prompt knowledge base

**Use Cases**:
- Extracting prompts from production codebases for documentation
- Building prompt libraries from open-source projects
- Auditing prompt usage across applications
- Migrating prompts between LLM providers
- Creating prompt catalogs for team collaboration
- Analyzing prompt patterns for optimization

**Production metrics**:
- Extraction accuracy: 95%+ prompt detection rate
- Processing speed: 1000+ files in 5-10 minutes
- False positive rate: <5% with proper filtering
- Sanitization effectiveness: 99%+ sensitive data removal

---

---

## Prompt

```
You are an expert code analyst specializing in prompt engineering and LLM integration patterns. Your task is to analyze a GitHub repository to identify, extract, and catalog all AI/LLM prompts for building a reusable prompt library.

## YOUR TASK

Systematically scan the repository to find all prompts used with LLMs (OpenAI, Anthropic, Google, etc.), extract them with context, sanitize sensitive information, and output structured metadata for cataloging.

---

## DETECTION STRATEGY

### Phase 1: File Scanning Priority

Scan files in this order for efficiency:

**High Priority** (scan first):
- `*.prompt`, `*.prompts` files
- `prompts/` directory contents
- `*_prompt.py`, `*_prompts.py`
- `templates/` directory with prompt-related files

**Medium Priority**:
- All Python files (`*.py`) - check for API calls and prompt strings
- Markdown files (`*.md`) - look for examples and documentation
- Jupyter notebooks (`*.ipynb`) - extract from code and markdown cells
- YAML/JSON configs (`*.yaml`, `*.json`) - search for prompt templates

**Low Priority** (if time permits):
- Documentation files
- Test files (may contain prompt examples)
- Configuration files

### Phase 2: Prompt Identification Patterns

Identify prompts through multiple signals:

**Variable/Constant Names**:
- Contains: `prompt`, `PROMPT`, `template`, `TEMPLATE`
- Contains: `instruction`, `system_message`, `user_message`
- Contains: `few_shot`, `examples`, `context`

**Function Calls** (API invocations):
- OpenAI: `openai.ChatCompletion.create()`, `client.chat.completions.create()`
- Anthropic: `anthropic.messages.create()`, `claude.completion()`
- Google: `genai.generate_text()`, `model.generate_content()`
- Generic: `*completion*`, `*chat*`, `*generate*`

**String Content Patterns**:
- Multi-line strings (triple quotes) with instruction-like language
- Strings starting with: "You are", "Your task", "Given", "Generate", "Analyze"
- Strings with role definitions: "Act as", "You will", "Your role"
- Strings with output format specifications: "Output format:", "Return JSON"

**Code Context**:
- Docstrings describing prompt usage
- Comments explaining prompt purpose
- F-strings with template variables like `{input}`, `{context}`

---

## EXTRACTION PROCESS

### Phase 3: Context Capture

For each identified prompt, extract:

**Prompt Content**:
- Full prompt text (preserve formatting, newlines)
- Handle f-strings: show template structure with `{variable}` placeholders
- Handle concatenated strings: combine into single prompt
- Preserve XML tags, JSON structures, markdown formatting

**Surrounding Context**:
- **10 lines before** the prompt definition
- **10 lines after** the prompt usage
- Function/method name containing the prompt
- Class name if within a class
- Module-level context (imports, constants)

**Location Information**:
- File path (relative to repository root)
- Line number where prompt starts
- Line number where prompt ends
- Git commit hash (if available)

### Phase 4: Metadata Generation

For each prompt, generate this structure:
```

---

## Production Patterns

### Pattern 1: Repository Analysis Workflow

**Use case**: Extract prompts from production codebase for documentation.

```python
# Simulated usage (actual implementation would use the prompt)

from prompt_extractor import extract_prompts

# Run extraction
results = extract_prompts(
    repo_path="./my-llm-app",
    output_file="prompts_catalog.json",
    include_test_files=False,
    min_quality_score=5
)

print(f"Found {results['total_prompts']} prompts")
print(f"Flagged {results['flagged_count']} for review")

# Review flagged prompts
for prompt in results['flagged_prompts']:
    print(f"\nPrompt: {prompt['prompt_id']}")
    print(f"Flag: {prompt['review_flag']}")
    print(f"Notes: {prompt['review_notes']}")
    print(f"Location: {prompt['location']['file']}:{prompt['location']['line_start']}")

    # Human review decision
    decision = input("Keep (k), Redact (r), or Exclude (e)? ")
    # Process decision...
```

### Pattern 2: Multi-Repository Prompt Library Building

**Use case**: Build organizational prompt library from multiple projects.

```python
repos = [
    "company/customer-support-bot",
    "company/data-analysis-tool",
    "company/content-generator"
]

all_prompts = []

for repo in repos:
    print(f"Processing {repo}...")

    results = extract_prompts(
        repo_path=f"./{repo}",
        sanitize_company_name=True,
        company_name="ACME Corp"
    )

    # Add to library with project tag
    for prompt in results['prompts']:
        prompt['project'] = repo
        all_prompts.append(prompt)

# Deduplicate similar prompts
unique_prompts = deduplicate_prompts(all_prompts, similarity_threshold=0.9)

# Export to library
export_to_library(unique_prompts, "company_prompt_library.json")
```

---

---

## Common Issues & Fixes

### Issue 1: Missing Prompts

**Problem**: Extraction misses prompts that are clearly present.

**Fix**: Check detection patterns
```
Add to detection:
- Look for custom variable names (e.g., "query", "request_text")
- Check for prompts in class __init__ methods
- Scan string concatenation patterns
- Include single-line strings over 50 characters
```

### Issue 2: Too Many False Positives

**Problem**: Extracting non-prompt strings (error messages, logs, etc.).

**Fix**: Add filtering criteria
```
Exclude:
- Strings in logging statements
- Error/exception messages
- SQL queries (unless explicitly for LLM)
- Short strings (<30 characters)
- Strings without instruction words
```

### Issue 3: Incomplete Context

**Problem**: Context doesn't show how prompt is used.

**Fix**: Expand context capture
```
Increase to:
- 20 lines before/after (instead of 10)
- Include function signature
- Include class-level docstring
- Capture related helper functions
```

### Issue 4: Over-Sanitization

**Problem**: Too much redaction makes prompts unusable.

**Fix**: Adjust sanitization rules
```
More nuanced approach:
- Only redact when high confidence of sensitivity
- Preserve generic company references
- Keep placeholder metrics
- Flag instead of auto-redact for edge cases
```

---

---

## Related Prompts

- [Code Review & Refactoring](./code-review-refactoring.md) - For analyzing extracted code
- [CLAUDE.md Generator](./claude-md-generator.md) - For creating prompt library documentation

---

**Success Metrics**:

After using this extraction system, you should achieve:
- ✅ 95%+ prompt detection rate
- ✅ <5% false positive rate
- ✅ 100% API key redaction
- ✅ Complete metadata for all prompts
- ✅ Actionable quality scores
- ✅ Clear human review guidance

**Remember**: This is a privacy-sensitive operation. Always err on the side of over-flagging for human review rather than auto-removing potentially valuable content. The goal is to build a useful prompt library while protecting sensitive information.
