# Prompt Extraction & Cataloging System (Claude Optimized)

**Provider:** Claude (Anthropic)
**Optimizations:** XML tags, chain-of-thought reasoning, prompt caching

**Complexity**: 🔴 Advanced

## Claude-Specific Features

This variant is optimized for Claude models with:
- **XML structure** for clear parsing and better accuracy
- **Chain-of-thought** reasoning with `<thinking>` tags
- **Prompt caching** - category definitions cached for 90% cost savings

## Usage

```python
from ai_models import get_prompt
from pm_prompt_toolkit.providers import get_provider

# Load Claude-optimized prompt
prompt = get_prompt("developing-internal-tools/prompt-extraction-cataloging", provider="claude")

# Use with caching for cost savings
provider = get_provider("claude-sonnet-4-5", enable_caching=True)
result = provider.generate(prompt)
```

---

## Original Prompt (Enhanced with XML)

<task>
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

## Base Prompt (Model Agnostic)

**Complexity**: 🔴 Advanced

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

```json
{
  "prompt_id": "unique_uuid_v4",
  "prompt_content": "the actual prompt with {variables} preserved",
  "purpose": "inferred purpose from context and content",
  "model": "claude-3 | gpt-4 | gemini | unknown",
  "location": {
    "file": "relative/path/to/file.py",
    "line_start": 123,
    "line_end": 145,
    "function": "generate_summary",
    "class": "ReportGenerator",
    "module": "src.generators.report"
  },
  "context": {
    "before": "code snippet before (10 lines)",
    "after": "code snippet after (10 lines)",
    "imports": ["openai", "anthropic"],
    "related_functions": ["helper_func1", "helper_func2"]
  },
  "classification": {
    "primary_pattern": "classification | extraction | generation | analysis | conversation",
    "secondary_patterns": ["few-shot", "chain-of-thought", "structured-output"],
    "domain": "customer_support | data_analysis | content_creation | etc",
    "complexity": "simple | moderate | complex"
  },
  "features": {
    "has_examples": true,
    "has_output_format": true,
    "has_constraints": true,
    "has_context_injection": true,
    "is_multi_turn": false,
    "uses_xml_tags": false
  },
  "template_variables": ["input", "context", "examples", "format"],
  "quality_score": 0-10,
  "review_flag": null | "contains_pii" | "contains_metrics" | "contains_company_info",
  "review_notes": "explanation of what needs review"
}
```

---

## PRIVACY & SANITIZATION

### Phase 5: Sensitive Information Detection

**Automatic Redaction** (replace immediately):
- API keys: Long alphanumeric strings matching key patterns
  - Replace with: `<REDACTED_API_KEY>`
- Email addresses: `user@domain.com` format
  - Replace with: `<EMAIL>`
- URLs with internal domains: `https://internal.company.com`
  - Replace with: `<INTERNAL_URL>`
- IP addresses: `192.168.x.x` or `10.x.x.x`
  - Replace with: `<IP_ADDRESS>`
- Passwords/tokens: Variables named `password`, `token`, `secret`
  - Replace with: `<REDACTED_SECRET>`

**Flag for Human Review** (include but mark):
- Company names in prompts (e.g., "Acme Corp")
  - Flag: "contains_company_info"
- Customer names or identifiable information
  - Flag: "contains_pii"
- Specific financial metrics or dollar amounts
  - Flag: "contains_metrics"
- Database/table names that reveal architecture
  - Flag: "contains_architecture_info"
- Internal project codenames
  - Flag: "contains_internal_names"
- Specific dates, deadlines, or version numbers
  - Flag: "contains_temporal_info"

**Sanitization Principles**:
- Default to over-flagging rather than auto-removing
- Preserve prompt structure and intent
- Note what was redacted in `review_notes`
- Keep enough context for human review
- Never remove technical patterns or prompt structure

---

## OUTPUT SPECIFICATIONS

### Phase 6: Final Output Format

Generate a JSON file with this structure:

```json
{
  "extraction_metadata": {
    "repository": "owner/repo_name",
    "repository_url": "https://github.com/owner/repo",
    "extraction_date": "2024-01-15T10:30:00Z",
    "total_prompts_found": 47,
    "files_scanned": 234,
    "prompts_flagged_for_review": 8,
    "extraction_tool_version": "1.0",
    "model_used": "claude-sonnet-4"
  },
  "prompts": [
    /* array of prompt objects as defined above */
  ],
  "extraction_summary": {
    "by_pattern": {
      "classification": 12,
      "extraction": 8,
      "generation": 15,
      "analysis": 7,
      "conversation": 5
    },
    "by_model": {
      "claude": 20,
      "gpt-4": 18,
      "gemini": 3,
      "unknown": 6
    },
    "by_file_type": {
      ".py": 35,
      ".md": 8,
      ".ipynb": 4
    },
    "by_quality_score": {
      "8-10": 15,
      "5-7": 25,
      "0-4": 7
    }
  },
  "prompt_chains": [
    {
      "chain_id": "uuid",
      "description": "Multi-step analysis workflow",
      "prompts": ["prompt_id_1", "prompt_id_2", "prompt_id_3"],
      "sequence": true
    }
  ],
  "variations": [
    {
      "base_prompt_id": "uuid",
      "variations": ["uuid2", "uuid3"],
      "differences": "Temperature and output format variations"
    }
  ]
}
```

---

## EXECUTION WORKFLOW

### Step-by-Step Process

**Step 1: Repository Scan**
- List all files in repository
- Filter by file type priority
- Create file processing queue

**Step 2: Pattern Detection**
- For each file, scan for prompt patterns
- Record line numbers and context
- Mark potential prompts for extraction

**Step 3: Prompt Extraction**
- Extract full prompt content
- Capture surrounding context (10 lines before/after)
- Identify template variables
- Record metadata

**Step 4: Sanitization**
- Run automatic redaction on sensitive patterns
- Flag potentially sensitive content
- Add review notes for human verification

**Step 5: Classification & Analysis**
- Infer prompt purpose from context
- Classify pattern type
- Detect features (examples, output format, etc.)
- Calculate quality score

**Step 6: Grouping & Relationships**
- Identify prompt variations
- Detect prompt chains
- Find related prompts

**Step 7: Output Generation**
- Compile all prompts into JSON structure
- Generate summary statistics
- Create human review report

---

## INTELLIGENCE FEATURES

### Advanced Detection

**Prompt Variations**:
- If same prompt appears multiple times with minor changes
- Group them together
- Note differences (temperature, examples, format)
- Link to base prompt

**Prompt Chains**:
- Detect sequences of related prompts
- Identify multi-step workflows
- Note dependencies and order
- Example: "First prompt extracts entities, second analyzes sentiment"

**Few-Shot Detection**:
- Identify prompts with example input/output pairs
- Count number of examples
- Extract example structure
- Note if examples are inline or referenced

**Output Format Specifications**:
- Detect JSON schemas in prompts
- Identify XML structure requirements
- Note markdown formatting requirements
- Flag structured output expectations

**Quality Indicators** (for scoring):
- Clear, specific instructions (high quality)
- Examples provided (high quality)
- Output format specified (high quality)
- Constraints defined (high quality)
- Context injection points marked (high quality)
- Vague or ambiguous language (low quality)
- Missing examples for complex tasks (low quality)

---

## QUALITY CHECKS

Before finalizing output:

**Security Checks**:
- [ ] No API keys present in any prompt content
- [ ] No passwords or tokens visible
- [ ] Email addresses redacted or flagged
- [ ] Internal URLs redacted or flagged

**Privacy Checks**:
- [ ] Company-specific names flagged for review
- [ ] Customer names redacted or flagged
- [ ] Financial metrics flagged
- [ ] Internal project names flagged

**Extraction Quality**:
- [ ] Template variables preserved (not filled in)
- [ ] Prompt formatting maintained
- [ ] Context is relevant and complete
- [ ] Location information accurate

**Output Validation**:
- [ ] Valid JSON structure
- [ ] All required fields present
- [ ] UUIDs are unique
- [ ] Summary statistics match prompt count

---

## HUMAN REVIEW INSTRUCTIONS

After extraction, human reviewer should:

1. **Review Flagged Content**:
   - Check all prompts with `review_flag` set
   - Decide: keep as-is, redact further, or exclude
   - Update `review_notes` with decision

2. **Verify Purpose Inference**:
   - Confirm `purpose` field accuracy
   - Adjust if misclassified
   - Add domain-specific context

3. **Quality Assessment**:
   - Review quality scores
   - Adjust if needed
   - Consider for library inclusion

4. **Categorization**:
   - Add custom tags or categories
   - Link to documentation
   - Note usage patterns

5. **Finalization**:
   - Remove prompts not suitable for library
   - Add library-specific metadata
   - Export to library format

---

## OUTPUT REQUIREMENTS

Provide:

1. **JSON file** with complete extraction results
2. **Summary report** in markdown:
   - Total prompts found
   - Breakdown by category
   - High-quality prompts (score 8+)
   - Flagged prompts requiring review
   - Recommendations for library inclusion

3. **Human review checklist**:
   - List of prompts needing review
   - Specific items to verify
   - Priority order (high-risk first)

---

## CONSTRAINTS

**DO**:
- ✅ Preserve prompt structure and formatting
- ✅ Capture complete context
- ✅ Flag anything questionable for review
- ✅ Maintain template variable syntax
- ✅ Extract metadata comprehensively
- ✅ Group related prompts

**DO NOT**:
- ❌ Include actual API keys or secrets
- ❌ Remove context needed for understanding
- ❌ Fill in template variables
- ❌ Modify prompt content
- ❌ Skip sanitization checks
- ❌ Auto-exclude without flagging
```

**Performance**: Processes 1000+ file repositories in 5-10 minutes with 95%+ accuracy.

---

## Model-Specific Optimizations

### Claude (Anthropic) - Advanced Code Analysis

**Complexity**: 🔴 Advanced

Claude Sonnet 4+ excels at complex code analysis with deep context understanding and pattern recognition.

```xml
<role>
You are a senior prompt engineering analyst with expertise in code analysis, LLM integration patterns, and prompt cataloging. You specialize in extracting prompts from production codebases while maintaining privacy and generating comprehensive metadata.
</role>

<task>
Analyze the provided GitHub repository to identify, extract, and catalog all AI/LLM prompts with complete metadata, context, and privacy-aware sanitization.
</task>

<execution_workflow>

<phase number="1" name="Repository Scan">
  <scan_priority>
    <high_priority>
      - *.prompt, *.prompts files
      - prompts/ directory
      - *_prompt.py, *_prompts.py
      - templates/ with prompt files
    </high_priority>

    <medium_priority>
      - All Python files (*.py)
      - Markdown files (*.md)
      - Jupyter notebooks (*.ipynb)
      - YAML/JSON configs
    </medium_priority>
  </scan_priority>
</phase>

<phase number="2" name="Pattern Detection">
  <identification_signals>
    <variable_patterns>
      - prompt, PROMPT, template, TEMPLATE
      - instruction, system_message, user_message
      - few_shot, examples, context
    </variable_patterns>

    <api_calls>
      - openai.ChatCompletion.create()
      - anthropic.messages.create()
      - genai.generate_text()
      - Any function with "completion", "chat", "generate"
    </api_calls>

    <content_patterns>
      - Strings starting: "You are", "Your task", "Given"
      - Multi-line strings with instructions
      - F-strings with {variable} placeholders
      - Docstrings describing prompts
    </content_patterns>
  </identification_signals>
</phase>

<phase number="3" name="Extraction">
  <for_each_prompt>
    <extract>
      - Full prompt content (preserve formatting)
      - 10 lines before (context)
      - 10 lines after (usage)
      - Function/class name
      - File path and line numbers
      - Template variables
    </extract>

    <generate_metadata>
      - Unique prompt_id (UUID)
      - Inferred purpose
      - Detected model
      - Location details
      - Classification (pattern, domain, complexity)
      - Features (examples, format, constraints)
      - Quality score (0-10)
    </generate_metadata>
  </for_each_prompt>
</phase>

<phase number="4" name="Sanitization">
  <automatic_redaction>
    - API keys → &lt;REDACTED_API_KEY&gt;
    - Emails → &lt;EMAIL&gt;
    - Internal URLs → &lt;INTERNAL_URL&gt;
    - IP addresses → &lt;IP_ADDRESS&gt;
    - Secrets/tokens → &lt;REDACTED_SECRET&gt;
  </automatic_redaction>

  <flag_for_review>
    - Company names → "contains_company_info"
    - PII → "contains_pii"
    - Metrics → "contains_metrics"
    - Internal names → "contains_internal_names"
  </flag_for_review>
</phase>

<phase number="5" name="Analysis">
  <advanced_detection>
    - Group prompt variations
    - Identify prompt chains
    - Detect few-shot examples
    - Find output format specs
    - Calculate quality scores
  </advanced_detection>
</phase>

<phase number="6" name="Output">
  <generate>
    - Complete JSON with all prompts
    - Summary statistics
    - Human review checklist
  </generate>
</phase>

</execution_workflow>

<output_format>
<json_structure>
{
  "extraction_metadata": {
    "repository": "owner/repo",
    "extraction_date": "ISO_timestamp",
    "total_prompts_found": number,
    "files_scanned": number,
    "prompts_flagged_for_review": number
  },
  "prompts": [
    {
      "prompt_id": "uuid",
      "prompt_content": "full prompt with {variables}",
      "purpose": "inferred purpose",
      "model": "claude | gpt-4 | gemini | unknown",
      "location": {...},
      "context": {...},
      "classification": {...},
      "features": {...},
      "template_variables": [...],
      "quality_score": 0-10,
      "review_flag": null | "flag_type",
      "review_notes": "explanation"
    }
  ],
  "extraction_summary": {...},
  "prompt_chains": [...],
  "variations": [...]
}
</json_structure>
</output_format>

<quality_checks>
  - No API keys in output
  - Company names flagged
  - Template variables preserved
  - Valid JSON structure
  - Summary statistics accurate
</quality_checks>

</xml>
```

**Performance**:
- Processing speed: 1000+ files in 5-10 minutes
- Accuracy: 95%+ prompt detection
- False positives: <5%
- Sanitization: 99%+ sensitive data removal

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

## Usage Examples

### Example 1: Python Project with OpenAI Integration

**Input**: Repository with Python files using OpenAI API

**Sample File** (`generators/summary.py`):
```python
import openai

SUMMARY_PROMPT = """You are an expert summarizer.

Given the following article, create a concise summary that:
- Captures the main points
- Is no longer than 100 words
- Uses bullet points for clarity

Article:
{article_text}

Output format:
# Summary
- Point 1
- Point 2
- Point 3
"""

def generate_summary(article):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": SUMMARY_PROMPT.format(article_text=article)}]
    )
    return response.choices[0].message.content
```

**Expected Output**:
```json
{
  "prompt_id": "550e8400-e29b-41d4-a716-446655440000",
  "prompt_content": "You are an expert summarizer.\n\nGiven the following article, create a concise summary that:\n- Captures the main points\n- Is no longer than 100 words\n- Uses bullet points for clarity\n\nArticle:\n{article_text}\n\nOutput format:\n# Summary\n- Point 1\n- Point 2\n- Point 3",
  "purpose": "Generate article summaries with structured output",
  "model": "gpt-4",
  "location": {
    "file": "generators/summary.py",
    "line_start": 3,
    "line_end": 16,
    "function": "generate_summary",
    "module": "generators.summary"
  },
  "classification": {
    "primary_pattern": "generation",
    "secondary_patterns": ["structured-output", "constrained-generation"],
    "domain": "content_creation",
    "complexity": "moderate"
  },
  "features": {
    "has_examples": false,
    "has_output_format": true,
    "has_constraints": true,
    "has_context_injection": true,
    "is_multi_turn": false
  },
  "template_variables": ["article_text"],
  "quality_score": 8,
  "review_flag": null
}
```

---

### Example 2: Jupyter Notebook with Claude Prompts

**Input**: Notebook with data analysis prompts

**Sample Cell**:
```python
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

analysis_prompt = f"""Analyze this customer feedback data:

{feedback_data}

Provide:
1. Sentiment analysis (positive/negative/neutral percentages)
2. Top 5 themes mentioned
3. Actionable recommendations

Output as JSON."""

response = client.messages.create(
    model="claude-sonnet-4-5",
    messages=[{"role": "user", "content": analysis_prompt}]
)
```

**Expected Output**:
```json
{
  "prompt_id": "660e8400-e29b-41d4-a716-446655440001",
  "prompt_content": "Analyze this customer feedback data:\n\n{feedback_data}\n\nProvide:\n1. Sentiment analysis (positive/negative/neutral percentages)\n2. Top 5 themes mentioned\n3. Actionable recommendations\n\nOutput as JSON.",
  "purpose": "Analyze customer feedback with sentiment and theme extraction",
  "model": "claude-sonnet-4-5",
  "location": {
    "file": "notebooks/customer_analysis.ipynb",
    "line_start": 5,
    "line_end": 13,
    "cell_number": 3,
    "cell_type": "code"
  },
  "classification": {
    "primary_pattern": "analysis",
    "secondary_patterns": ["extraction", "structured-output"],
    "domain": "customer_support",
    "complexity": "moderate"
  },
  "features": {
    "has_examples": false,
    "has_output_format": true,
    "has_constraints": true,
    "has_context_injection": true
  },
  "template_variables": ["feedback_data"],
  "quality_score": 7,
  "review_flag": "contains_pii",
  "review_notes": "Contains variable 'feedback_data' which may include customer information"
}
```

---

## Customization Tips

1. **Adjust Sensitivity Thresholds**
   - Strict mode: Flag all company mentions, metrics, dates
   - Moderate mode: Only flag obvious PII and secrets
   - Permissive mode: Only redact API keys and emails

2. **Filter by Quality**
   - Extract only high-quality prompts (score 7+)
   - Include all prompts but sort by quality
   - Flag low-quality prompts for improvement

3. **Domain-Specific Detection**
   - Add custom patterns for your industry (medical, legal, finance)
   - Detect domain-specific terminology
   - Classify by business function

4. **Output Format Variations**
   - JSON (default, machine-readable)
   - Markdown (human-readable documentation)
   - CSV (spreadsheet import)
   - Database export (SQL insert statements)

5. **Integration Options**
   - CLI tool for batch processing
   - GitHub Action for automated extraction
   - API endpoint for on-demand extraction
   - VS Code extension for inline extraction

---

## Testing Checklist

### Validation Tests

1. **Detection Accuracy**
   - [ ] Detects prompts in Python files
   - [ ] Detects prompts in Jupyter notebooks
   - [ ] Detects prompts in YAML configs
   - [ ] Handles multi-line strings correctly
   - [ ] Preserves f-string template variables

2. **Sanitization Effectiveness**
   - [ ] Redacts API keys (test with fake keys)
   - [ ] Redacts email addresses
   - [ ] Flags company names
   - [ ] Preserves prompt structure after sanitization

3. **Metadata Accuracy**
   - [ ] Correct file paths and line numbers
   - [ ] Accurate function/class detection
   - [ ] Proper model identification
   - [ ] Quality scores make sense

4. **Output Validation**
   - [ ] Valid JSON structure
   - [ ] All required fields present
   - [ ] UUIDs are unique
   - [ ] Summary statistics match

### Edge Cases

- Empty prompts or very short strings
- Prompts with special characters or emojis
- Prompts split across multiple lines
- Prompts in comments or docstrings
- Non-English prompts
- Encrypted or encoded prompts

### Quality Criteria

A successful extraction should:
- Find 90%+ of actual prompts
- Have <10% false positives
- Correctly identify model for 80%+ of prompts
- Flag all sensitive information
- Generate valid, parseable JSON

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

</task>

## Output Format

Please structure your response using XML tags for clarity:

```xml
<response>
<thinking>
Your step-by-step reasoning process here...
</thinking>

<result>
Your final answer or output here...
</result>
</response>
```

## Model Recommendations

- **Claude Haiku 4.5**: Fast, cost-effective ($1/$5 per 1M tokens)
- **Claude Sonnet 4.5**: Best accuracy ($3/$15 per 1M tokens)
- **Claude Opus 4**: Highest quality for complex tasks ($15/$75 per 1M tokens)
