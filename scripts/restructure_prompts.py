#!/usr/bin/env python3
"""
Restructure prompt pattern library to eliminate duplication.

This script:
1. Extracts the base prompt (model-agnostic) to prompt.md
2. Creates minimal model-specific files (prompt.claude.md, prompt.openai.md, etc.)
   that reference the base and only add model-specific optimizations
3. Eliminates massive duplication across model-specific files
"""

import os
import re
from pathlib import Path
from typing import Dict


def extract_base_content(prompt_md_path: Path) -> Dict[str, str]:
    """
    Extract sections from the base prompt.md file.

    Returns dict with keys: header, overview, business_value, prompt_content
    """
    with open(prompt_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    sections = {}

    # Extract header (title + metadata)
    header_match = re.search(r"^(# .+?\n.*?(?=\n## ))", content, re.DOTALL | re.MULTILINE)
    if header_match:
        sections["header"] = header_match.group(1).strip()

    # Extract overview section
    overview_match = re.search(r"## Overview\n(.*?)(?=\n## |\n---|\Z)", content, re.DOTALL)
    if overview_match:
        sections["overview"] = overview_match.group(0).strip()

    # Extract business value and metrics
    business_match = re.search(
        r"\*\*Business Value\*\*:(.*?)\*\*Production metrics\*\*:(.*?)(?=\n---|\n## |\Z)",
        content,
        re.DOTALL,
    )
    if business_match:
        sections["business_value"] = (
            f"**Business Value**:{business_match.group(1)}"
            f"**Production metrics**:{business_match.group(2)}"
        ).strip()

    # Extract main prompt content (after Base Prompt heading)
    prompt_match = re.search(
        r"## Base Prompt \(Model Agnostic\)(.*?)(?=\n## Examples|\n---\n## Examples|\Z)",
        content,
        re.DOTALL,
    )
    if prompt_match:
        sections["prompt_content"] = prompt_match.group(1).strip()

    # Extract examples section
    examples_match = re.search(
        r"## Examples(.*?)(?=\n## Testing|\n## Quality|\Z)", content, re.DOTALL
    )
    if examples_match:
        sections["examples"] = examples_match.group(0).strip()

    # Extract testing/quality sections
    testing_match = re.search(r"(## Testing.*?## Quality.*?)(?=\n## |\Z)", content, re.DOTALL)
    if testing_match:
        sections["testing_quality"] = testing_match.group(1).strip()
    elif re.search(r"## QUALITY CHECKLIST", content):
        # Alternative: extract quality checklist
        quality_match = re.search(r"(## QUALITY CHECKLIST.*?)(?=```|\Z)", content, re.DOTALL)
        if quality_match:
            sections["testing_quality"] = quality_match.group(1).strip()

    return sections


def create_base_prompt(sections: Dict[str, str]) -> str:
    """Create the model-agnostic base prompt.md content."""

    parts = [sections.get("header", "")]

    if "overview" in sections:
        parts.append(sections["overview"])

    if "business_value" in sections:
        parts.append(sections["business_value"])

    parts.append("---\n")
    parts.append("## Prompt\n")

    if "prompt_content" in sections:
        # Remove model-specific markers and clean up
        prompt = sections["prompt_content"]
        # Remove XML tags if present
        prompt = re.sub(r"<task>|</task>", "", prompt)
        # Remove complexity markers that repeat
        prompt = re.sub(r"\n\*\*Complexity\*\*:.*?\n", "\n", prompt)
        parts.append(prompt)

    if "examples" in sections:
        parts.append("\n---\n")
        parts.append(sections["examples"])

    if "testing_quality" in sections:
        parts.append("\n---\n")
        parts.append(sections["testing_quality"])

    return "\n\n".join(parts)


def create_claude_optimized(base_sections: Dict[str, str], title: str) -> str:
    """Create Claude-optimized prompt file with minimal duplication."""

    # Extract just the core prompt content
    prompt_content = base_sections.get("prompt_content", "")

    # Remove any existing wrapping
    prompt_content = re.sub(r"^```\n|```$", "", prompt_content.strip())
    prompt_content = re.sub(r"<task>|</task>", "", prompt_content)

    template = f"""# {title} - Claude Optimized

> Extends `prompt.md` with Claude-specific optimizations

## Prompt

<task>
{prompt_content}
</task>

## Claude Optimizations Applied

- **XML structure**: `<task>` wrapper for clear task delineation
- **Structured thinking**: Use `<thinking>` tags when reasoning through complex decisions
- **Prompt caching**: Static definitions cached for 90%+ cost savings on repeated use
- **Chain-of-thought**: Encourages step-by-step reasoning for complex analysis

## Usage

```python
from pm_prompt_toolkit.providers import get_provider

# Initialize Claude provider with caching
provider = get_provider("claude-sonnet-4-5", enable_caching=True)

# The task wrapper enables better parsing
result = provider.generate(
    system_prompt="<prompt from above>",
    user_message="<your codebase or content>"
)
```

## Caching Strategy

For optimal performance with Claude:
- Cache the `<task>` section (static prompt content)
- Keep user content (code, documents) outside cache
- Reuse same prompt across multiple files/iterations
- Expected cost reduction: 90%+ for multi-file analysis

## See Also

- Base prompt: `prompt.md` (examples, testing checklist, business value)
- Provider documentation: `docs/provider-specific-prompts.md`
"""

    return template


def create_openai_optimized(base_sections: Dict[str, str], title: str) -> str:
    """Create OpenAI-optimized prompt file with minimal duplication."""

    prompt_content = base_sections.get("prompt_content", "")
    prompt_content = re.sub(r"^```\n|```$", "", prompt_content.strip())
    prompt_content = re.sub(r"<task>|</task>", "", prompt_content)

    template = f"""# {title} - OpenAI Optimized

> Extends `prompt.md` with OpenAI-specific optimizations

## System Prompt

```
{prompt_content}
```

## OpenAI Optimizations Applied

- **System message clarity**: Explicit role and responsibilities
- **Structured output**: Clear formatting instructions for consistency
- **Function calling ready**: Can be combined with function schemas
- **Concise directives**: Optimized for GPT-4's instruction-following

## Usage

```python
from pm_prompt_toolkit.providers import get_provider

# Initialize OpenAI provider
provider = get_provider("gpt-4o")

result = provider.generate(
    system_prompt="<prompt from above>",
    user_message="<your codebase or content>"
)
```

## Model Recommendations

- **GPT-4o**: Best balance of speed, quality, and cost
- **GPT-4o-mini**: Faster, lower cost for simpler codebases
- **GPT-4-turbo**: Use if you need extended context (>128k tokens)

## Optional: Function Calling

For structured output, combine with function schema:

```python
# Define output schema
output_schema = {{
    "name": "code_review_results",
    "description": "Structured code review findings",
    "parameters": {{
        "type": "object",
        "properties": {{
            "security_issues": {{"type": "array", "items": {{"type": "string"}}}},
            "code_quality": {{"type": "array", "items": {{"type": "string"}}}},
            "recommendations": {{"type": "array", "items": {{"type": "string"}}}}
        }},
        "required": ["security_issues", "code_quality", "recommendations"]
    }}
}}

result = provider.generate(
    system_prompt="<prompt>",
    user_message="<content>",
    functions=[output_schema],
    function_call={{"name": "code_review_results"}}
)
```

## See Also

- Base prompt: `prompt.md` (examples, testing checklist, business value)
- Provider documentation: `docs/provider-specific-prompts.md`
"""

    return template


def create_gemini_optimized(base_sections: Dict[str, str], title: str) -> str:
    """Create Gemini-optimized prompt file with minimal duplication."""

    prompt_content = base_sections.get("prompt_content", "")
    prompt_content = re.sub(r"^```\n|```$", "", prompt_content.strip())
    prompt_content = re.sub(r"<task>|</task>", "", prompt_content)

    template = f"""# {title} - Gemini Optimized

> Extends `prompt.md` with Gemini-specific optimizations

## System Instruction

```
{prompt_content}
```

## Gemini Optimizations Applied

- **Clear directives**: Explicit, numbered instructions for better following
- **Context utilization**: Optimized for Gemini's large context window
- **Multimodal ready**: Can process code alongside diagrams/screenshots
- **Structured reasoning**: Step-by-step breakdown of complex tasks

## Usage

```python
from pm_prompt_toolkit.providers import get_provider

# Initialize Gemini provider
provider = get_provider("gemini-2.0-flash-exp")

result = provider.generate(
    system_instruction="<prompt from above>",
    contents="<your codebase or content>"
)
```

## Model Recommendations

- **gemini-2.0-flash-exp**: Best for most use cases (fast, high quality)
- **gemini-1.5-pro**: Maximum context window (2M tokens)
- **gemini-1.5-flash**: Fastest, good for simpler reviews

## Multimodal Usage

Gemini can analyze code + architecture diagrams:

```python
# Include both code and visual context
result = provider.generate(
    system_instruction="<prompt>",
    contents=[
        "Review this codebase...",
        {{"mime_type": "image/png", "data": diagram_bytes}}
    ]
)
```

## See Also

- Base prompt: `prompt.md` (examples, testing checklist, business value)
- Provider documentation: `docs/provider-specific-prompts.md`
"""

    return template


def restructure_prompt_directory(prompt_dir: Path) -> None:
    """
    Restructure a single prompt directory.

    1. Read existing prompt.md
    2. Extract sections
    3. Create clean base prompt.md
    4. Create minimal model-specific files
    """

    print(f"\nProcessing: {prompt_dir}")

    prompt_md = prompt_dir / "prompt.md"
    if not prompt_md.exists():
        print("  ⚠️  No prompt.md found, skipping")
        return

    # Extract sections from base
    sections = extract_base_content(prompt_md)

    # Get title from header
    title_match = re.search(r"^# (.+)$", sections.get("header", ""), re.MULTILINE)
    title = title_match.group(1) if title_match else prompt_dir.name

    # Create new base prompt (clean, no duplication)
    base_content = create_base_prompt(sections)

    # Write new base prompt
    print("  ✓ Writing prompt.md")
    with open(prompt_md, "w", encoding="utf-8") as f:
        f.write(base_content)

    # Create model-specific files
    claude_file = prompt_dir / "prompt.claude.md"
    print("  ✓ Writing prompt.claude.md")
    with open(claude_file, "w", encoding="utf-8") as f:
        f.write(create_claude_optimized(sections, title))

    openai_file = prompt_dir / "prompt.openai.md"
    print("  ✓ Writing prompt.openai.md")
    with open(openai_file, "w", encoding="utf-8") as f:
        f.write(create_openai_optimized(sections, title))

    gemini_file = prompt_dir / "prompt.gemini.md"
    print("  ✓ Writing prompt.gemini.md")
    with open(gemini_file, "w", encoding="utf-8") as f:
        f.write(create_gemini_optimized(sections, title))

    # Check file size reduction
    old_size = sum(f.stat().st_size for f in prompt_dir.glob("prompt*.md.bak") if f.exists())
    new_size = sum(f.stat().st_size for f in prompt_dir.glob("prompt*.md"))

    print(f"  📊 File size: {old_size/1024:.1f}KB → {new_size/1024:.1f}KB")


def main() -> None:
    """Main restructuring script."""

    repo_root = Path(__file__).parent.parent
    prompts_dir = repo_root / "prompts"

    # Find all prompt directories
    prompt_dirs = []
    for root, dirs, files in os.walk(prompts_dir):
        if "prompt.md" in files:
            prompt_dirs.append(Path(root))

    print(f"Found {len(prompt_dirs)} prompt directories")
    print("=" * 60)

    # First, backup originals
    for prompt_dir in prompt_dirs:
        for md_file in prompt_dir.glob("prompt*.md"):
            backup = md_file.with_suffix(".md.bak")
            if not backup.exists():
                import shutil

                shutil.copy2(md_file, backup)

    print("✓ Created backups (.md.bak)")

    # Restructure each directory
    for prompt_dir in prompt_dirs:
        restructure_prompt_directory(prompt_dir)

    print("\n" + "=" * 60)
    print("✅ Restructuring complete!")
    print("\nNext steps:")
    print("1. Review changes with: git diff")
    print("2. Test one prompt to ensure it works")
    print("3. Remove .bak files when satisfied: find prompts -name '*.bak' -delete")


if __name__ == "__main__":
    main()
