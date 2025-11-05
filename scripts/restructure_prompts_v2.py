#!/usr/bin/env python3
"""
Restructure prompt pattern library to eliminate duplication - V2.

This version properly extracts sections and creates clean files.
"""

import os
import re
from pathlib import Path
from typing import Dict, List


def read_file_lines(file_path: Path) -> List[str]:
    """Read file and return lines."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.readlines()


def find_section_ranges(lines: List[str]) -> Dict[str, tuple]:
    """
    Find line ranges for each major section.

    Returns dict mapping section name to (start_line, end_line) tuple.
    Ignores ## headers that appear inside code blocks (``` ... ```).
    """
    sections = {}
    current_section = None
    start_line = 0
    in_code_block = False

    for i, line in enumerate(lines):
        # Track code block state
        if line.strip().startswith("```"):
            in_code_block = not in_code_block

        # Match ## headers (but only outside code blocks)
        if line.startswith("## ") and not in_code_block:
            if current_section:
                sections[current_section] = (start_line, i)
            current_section = line.strip("# \n")
            start_line = i

    # Add last section
    if current_section:
        sections[current_section] = (start_line, len(lines))

    return sections


def extract_header(lines: List[str]) -> str:
    """Extract title and metadata (before first ## header)."""
    header_lines = []
    for line in lines:
        if line.startswith("## "):
            break
        header_lines.append(line)
    return "".join(header_lines).strip()


def extract_section(lines: List[str], start: int, end: int) -> str:
    """Extract section content between line numbers."""
    return "".join(lines[start:end]).strip()


def get_base_prompt_content(lines: List[str], sections: Dict[str, tuple]) -> str:
    """
    Extract just the core prompt instructions from Base Prompt section.

    This is the part between ```  markers.
    """
    if "Base Prompt (Model Agnostic)" not in sections:
        return ""

    start, end = sections["Base Prompt (Model Agnostic)"]

    # Find the code block bounds
    code_block_start = None
    code_block_end = None

    for i in range(start, end):
        line = lines[i]
        if line.strip() == "```" or line.startswith("```"):
            if code_block_start is None:
                code_block_start = i + 1  # Start after the ```
            else:
                code_block_end = i  # End before the closing ```
                break

    if code_block_start and code_block_end:
        # Extract lines between markers
        prompt_lines = lines[code_block_start:code_block_end]
        return "".join(prompt_lines).strip()

    # Fallback: return everything after ## Base Prompt header
    return "".join(lines[start + 1 : end]).strip()


def create_base_prompt_md(lines: List[str], sections: Dict[str, tuple]) -> str:
    """
    Create the clean base prompt.md file.

    Includes:
    - Header
    - Overview
    - Business value/metrics
    - Base prompt content
    - Examples (if present)
    - Testing/Quality sections

    Excludes:
    - Model-specific optimizations
    - Model-specific usage examples
    """
    parts = []

    # Header (title + metadata)
    header = extract_header(lines)
    parts.append(header)
    parts.append("")

    # Overview
    if "Overview" in sections:
        start, end = sections["Overview"]
        parts.append(extract_section(lines, start, end))
        parts.append("")

    # Separator and Base Prompt
    parts.append("---")
    parts.append("")
    parts.append("## Prompt")
    parts.append("")
    base_prompt = get_base_prompt_content(lines, sections)
    parts.append("```")
    parts.append(base_prompt)
    parts.append("```")
    parts.append("")

    # Add relevant additional sections (avoid model-specific ones)
    additional_sections = [
        "Production Patterns",
        "Quality Evaluation",
        "Testing",
        "Cost Comparison",
        "Usage Notes",
        "Common Issues & Fixes",
        "Related Prompts",
    ]

    for section_name in additional_sections:
        if section_name in sections:
            start, end = sections[section_name]
            parts.append("---")
            parts.append("")
            parts.append(extract_section(lines, start, end))
            parts.append("")

    return "\n".join(parts)


def create_claude_md(lines: List[str], sections: Dict[str, tuple], title: str) -> str:
    """Create Claude-optimized file."""

    # Get base prompt
    base_prompt = get_base_prompt_content(lines, sections)

    # Look for Claude-specific XML example if it exists
    claude_section_start = None
    claude_section_end = None

    if "Model-Specific Optimizations" in sections:
        start, end = sections["Model-Specific Optimizations"]
        for i in range(start, min(end, len(lines))):
            if "Claude (Anthropic)" in lines[i]:
                claude_section_start = i
                # Find end of Claude section (next ### or ## header)
                for j in range(i + 1, end):
                    if lines[j].startswith("### ") or lines[j].startswith("## "):
                        claude_section_end = j
                        break
                if not claude_section_end:
                    claude_section_end = end
                break

    # Extract Claude-specific formatted version if it exists
    claude_formatted = None
    if claude_section_start and claude_section_end:
        section_text = "".join(lines[claude_section_start:claude_section_end])
        # Look for XML formatted version
        xml_match = re.search(r"```xml\n(.*?)```", section_text, re.DOTALL)
        if xml_match:
            claude_formatted = xml_match.group(1).strip()

    # Build output
    output = []
    output.append(f"# {title} - Claude Optimized")
    output.append("")
    output.append("> Extends `prompt.md` with Claude-specific optimizations")
    output.append("")
    output.append("## Prompt")
    output.append("")

    if claude_formatted:
        # Use the XML-formatted version
        output.append(claude_formatted)
    else:
        # Wrap base prompt in <task> tags
        output.append("<task>")
        output.append(base_prompt)
        output.append("</task>")

    output.append("")
    output.append("## Claude Optimizations Applied")
    output.append("")
    output.append(
        "- **XML structure**: Uses XML tags for clear task delineation and better parsing"
    )
    output.append(
        "- **Structured thinking**: Encourages use of `<thinking>` tags for complex reasoning"
    )
    output.append("- **Prompt caching**: Static prompt content is cacheable for 90%+ cost savings")
    output.append("- **Extended context**: Leverages Claude's 200K token context window")
    output.append("")
    output.append("## Usage")
    output.append("")
    output.append("```python")
    output.append("from pm_prompt_toolkit.providers import get_provider")
    output.append("")
    output.append("# Initialize Claude provider with caching")
    output.append('provider = get_provider("claude-sonnet-4-5", enable_caching=True)')
    output.append("")
    output.append("result = provider.generate(")
    output.append('    system_prompt="<prompt from above>",')
    output.append('    user_message="<your content here>"')
    output.append(")")
    output.append("```")
    output.append("")
    output.append("## See Also")
    output.append("")
    output.append("- Base prompt: `prompt.md` (examples, testing checklist, business value)")
    output.append("- Provider documentation: `../../docs/provider-specific-prompts.md`")
    output.append("")

    return "\n".join(output)


def create_openai_md(lines: List[str], sections: Dict[str, tuple], title: str) -> str:
    """Create OpenAI-optimized file."""

    base_prompt = get_base_prompt_content(lines, sections)

    output = []
    output.append(f"# {title} - OpenAI Optimized")
    output.append("")
    output.append("> Extends `prompt.md` with OpenAI-specific optimizations")
    output.append("")
    output.append("## System Prompt")
    output.append("")
    output.append("```")
    output.append(base_prompt)
    output.append("```")
    output.append("")
    output.append("## OpenAI Optimizations Applied")
    output.append("")
    output.append(
        "- **Clear role definition**: Explicit system message with role and responsibilities"
    )
    output.append("- **Structured output**: Consistent formatting instructions")
    output.append(
        "- **Function calling ready**: Can be combined with function schemas for structured output"
    )
    output.append(
        "- **Concise directives**: Optimized for GPT-4's instruction-following capabilities"
    )
    output.append("")
    output.append("## Usage")
    output.append("")
    output.append("```python")
    output.append("from pm_prompt_toolkit.providers import get_provider")
    output.append("")
    output.append("# Initialize OpenAI provider")
    output.append('provider = get_provider("gpt-4o")')
    output.append("")
    output.append("result = provider.generate(")
    output.append('    system_prompt="<prompt from above>",')
    output.append('    user_message="<your content here>"')
    output.append(")")
    output.append("```")
    output.append("")
    output.append("## Model Recommendations")
    output.append("")
    output.append("- **gpt-4o**: Best balance of speed, quality, and cost for most use cases")
    output.append("- **gpt-4o-mini**: Faster and more cost-effective for simpler tasks")
    output.append("- **gpt-4-turbo**: Use for extended context needs (>128k tokens)")
    output.append("")
    output.append("## See Also")
    output.append("")
    output.append("- Base prompt: `prompt.md` (examples, testing checklist, business value)")
    output.append("- Provider documentation: `../../docs/provider-specific-prompts.md`")
    output.append("")

    return "\n".join(output)


def create_gemini_md(lines: List[str], sections: Dict[str, tuple], title: str) -> str:
    """Create Gemini-optimized file."""

    base_prompt = get_base_prompt_content(lines, sections)

    output = []
    output.append(f"# {title} - Gemini Optimized")
    output.append("")
    output.append("> Extends `prompt.md` with Gemini-specific optimizations")
    output.append("")
    output.append("## System Instruction")
    output.append("")
    output.append("```")
    output.append(base_prompt)
    output.append("```")
    output.append("")
    output.append("## Gemini Optimizations Applied")
    output.append("")
    output.append(
        "- **Clear directives**: Explicit, numbered instructions for better instruction-following"
    )
    output.append("- **Context utilization**: Optimized for Gemini's large context window")
    output.append(
        "- **Multimodal ready**: Can process code alongside diagrams, screenshots, or other media"
    )
    output.append("- **Structured reasoning**: Step-by-step breakdown for complex analysis tasks")
    output.append("")
    output.append("## Usage")
    output.append("")
    output.append("```python")
    output.append("from pm_prompt_toolkit.providers import get_provider")
    output.append("")
    output.append("# Initialize Gemini provider")
    output.append('provider = get_provider("gemini-2.0-flash-exp")')
    output.append("")
    output.append("result = provider.generate(")
    output.append('    system_instruction="<prompt from above>",')
    output.append('    contents="<your content here>"')
    output.append(")")
    output.append("```")
    output.append("")
    output.append("## Model Recommendations")
    output.append("")
    output.append("- **gemini-2.0-flash-exp**: Best for most use cases (fast, high quality)")
    output.append("- **gemini-1.5-pro**: Maximum context window (2M tokens)")
    output.append("- **gemini-1.5-flash**: Fastest option for simpler tasks")
    output.append("")
    output.append("## See Also")
    output.append("")
    output.append("- Base prompt: `prompt.md` (examples, testing checklist, business value)")
    output.append("- Provider documentation: `../../docs/provider-specific-prompts.md`")
    output.append("")

    return "\n".join(output)


def restructure_directory(prompt_dir: Path) -> None:
    """Restructure a single prompt directory."""

    print(f"\nProcessing: {prompt_dir.relative_to(Path.cwd())}")

    prompt_md = prompt_dir / "prompt.md"
    if not prompt_md.exists():
        print("  ⚠️  No prompt.md found, skipping")
        return

    # Read original file
    lines = read_file_lines(prompt_md)

    # Find all sections
    sections = find_section_ranges(lines)

    # Get title
    header = extract_header(lines)
    title_match = re.search(r"^# (.+)$", header, re.MULTILINE)
    title = title_match.group(1) if title_match else prompt_dir.name

    # Create new base prompt
    base_content = create_base_prompt_md(lines, sections)
    print(f"  ✓ Writing prompt.md ({len(base_content)} chars)")
    with open(prompt_md, "w", encoding="utf-8") as f:
        f.write(base_content)

    # Create model-specific files
    claude_content = create_claude_md(lines, sections, title)
    claude_file = prompt_dir / "prompt.claude.md"
    print(f"  ✓ Writing prompt.claude.md ({len(claude_content)} chars)")
    with open(claude_file, "w", encoding="utf-8") as f:
        f.write(claude_content)

    openai_content = create_openai_md(lines, sections, title)
    openai_file = prompt_dir / "prompt.openai.md"
    print(f"  ✓ Writing prompt.openai.md ({len(openai_content)} chars)")
    with open(openai_file, "w", encoding="utf-8") as f:
        f.write(openai_content)

    gemini_content = create_gemini_md(lines, sections, title)
    gemini_file = prompt_dir / "prompt.gemini.md"
    print(f"  ✓ Writing prompt.gemini.md ({len(gemini_content)} chars)")
    with open(gemini_file, "w", encoding="utf-8") as f:
        f.write(gemini_content)


def main():
    """Main script."""

    repo_root = Path(__file__).parent.parent
    prompts_dir = repo_root / "prompts"

    # Find all prompt directories
    prompt_dirs = []
    for root, dirs, files in os.walk(prompts_dir):
        if "prompt.md" in files:
            prompt_dirs.append(Path(root))

    print(f"Found {len(prompt_dirs)} prompt directories")
    print("=" * 70)

    for prompt_dir in prompt_dirs:
        restructure_directory(prompt_dir)

    print("\n" + "=" * 70)
    print("✅ Restructuring complete!")
    print("\nNext steps:")
    print("1. Review changes: git diff prompts/")
    print("2. Test a prompt to verify it works")
    print("3. Commit changes when satisfied")


if __name__ == "__main__":
    main()
