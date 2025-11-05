#!/usr/bin/env python3
"""
Interactive script to create a new prompt pattern following library standards.

Usage:
    python scripts/create_new_prompt.py

This script will:
1. Ask for prompt metadata (name, category, complexity, etc.)
2. Ask for the core prompt content
3. Generate all 4 files (base + 3 model-specific variants)
4. Validate the structure matches library guidelines
"""

import re
from pathlib import Path
from typing import Dict, List, Union


def sanitize_filename(name: str) -> str:
    """Convert prompt name to valid filename (lowercase, hyphens)."""
    # Remove special characters, convert to lowercase, replace spaces with hyphens
    sanitized = re.sub(r"[^\w\s-]", "", name.lower())
    sanitized = re.sub(r"[-\s]+", "-", sanitized)
    return sanitized.strip("-")


def get_category_path() -> str:
    """Get or create category directory."""
    print("\n=== CATEGORY SELECTION ===")
    print("Available categories:")
    print("1. analytics")
    print("2. developing-internal-tools")
    print("3. product-strategy")
    print("4. stakeholder-communication")
    print("5. Create new category")

    choice = input("\nSelect category (1-5): ").strip()

    if choice == "1":
        return "analytics"
    elif choice == "2":
        return "developing-internal-tools"
    elif choice == "3":
        return "product-strategy"
    elif choice == "4":
        return "stakeholder-communication"
    elif choice == "5":
        new_category = input("Enter new category name (lowercase-with-hyphens): ").strip()
        return sanitize_filename(new_category)
    else:
        print("Invalid choice, defaulting to 'developing-internal-tools'")
        return "developing-internal-tools"


def get_prompt_metadata() -> Dict[str, str]:
    """Collect prompt metadata from user."""
    print("\n=== PROMPT METADATA ===")

    metadata = {}

    # Name
    metadata["name"] = input("Prompt name (e.g., 'API Documentation Generator'): ").strip()
    metadata["filename"] = sanitize_filename(metadata["name"])

    # Category
    metadata["category"] = get_category_path()

    # Complexity
    print("\nComplexity level:")
    print("1. 🟢 Beginner")
    print("2. 🟡 Intermediate")
    print("3. 🔴 Advanced")
    complexity_choice = input("Select (1-3): ").strip()
    complexity_map = {
        "1": "🟢 Beginner",
        "2": "🟡 Intermediate",
        "3": "🔴 Advanced",
    }
    metadata["complexity"] = complexity_map.get(complexity_choice, "🟡 Intermediate")

    # Subcategory
    metadata["subcategory"] = input(
        "Subcategory (e.g., 'Technical Documentation', optional): "
    ).strip()

    # Model compatibility
    print("\nModel compatibility:")
    print("1. ✅ All models (universal)")
    print("2. ✅ Claude (all) | ✅ GPT-4 | ⚠️ Gemini")
    print("3. Custom")
    compat_choice = input("Select (1-3): ").strip()
    if compat_choice == "1":
        metadata["compatibility"] = "✅ Claude (all) | ✅ GPT-4 | ✅ Gemini"
    elif compat_choice == "2":
        metadata["compatibility"] = "✅ Claude (all) | ✅ GPT-4 | ⚠️ Gemini (large context needed)"
    else:
        metadata["compatibility"] = input("Enter custom compatibility: ").strip()

    return metadata


def get_prompt_content() -> Dict[str, Union[str, List[str]]]:
    """Collect prompt content from user."""
    print("\n=== PROMPT CONTENT ===")

    content: Dict[str, Union[str, List[str]]] = {}

    # Overview
    print("\nOverview (1-2 sentences describing what this prompt does):")
    content["overview"] = input("> ").strip()

    # Business value
    print("\nBusiness value (comma-separated list, e.g., 'Reduce X, Improve Y'):")
    business_input = input("> ").strip()
    content["business_value"] = (
        [v.strip() for v in business_input.split(",")] if business_input else []
    )

    # Use cases
    print("\nUse cases (comma-separated list):")
    use_cases_input = input("> ").strip()
    content["use_cases"] = (
        [u.strip() for u in use_cases_input.split(",")] if use_cases_input else []
    )

    # Production metrics (optional)
    print("\nProduction metrics (optional, comma-separated, e.g., 'Accuracy: 95%, Time: <2s'):")
    metrics_input = input("> ").strip()
    if metrics_input:
        content["metrics"] = [m.strip() for m in metrics_input.split(",")]
    else:
        content["metrics"] = []

    # Core prompt
    print("\n=== CORE PROMPT CONTENT ===")
    print("Enter the main prompt instructions below.")
    print("Type 'END' on a new line when done:\n")

    prompt_lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        prompt_lines.append(line)

    content["prompt"] = "\n".join(prompt_lines).strip()

    return content


def create_base_prompt(metadata: Dict[str, str], content: Dict[str, Union[str, List[str]]]) -> str:
    """Generate the base prompt.md file content."""

    parts = [f"# {metadata['name']}\n"]

    # Metadata
    parts.append(f"**Complexity**: {metadata['complexity']}")
    if metadata["subcategory"]:
        parts.append(f"**Category**: {metadata['subcategory']}")
    parts.append(f"**Model Compatibility**: {metadata['compatibility']}\n")

    # Overview
    parts.append("## Overview\n")
    parts.append(f"{content['overview']}\n")

    # Business value
    parts.append("**Business Value**:")
    for value in content["business_value"]:
        parts.append(f"- {value}")
    parts.append("")

    # Use cases
    parts.append("**Use Cases**:")
    for use_case in content["use_cases"]:
        parts.append(f"- {use_case}")
    parts.append("")

    # Production metrics (if provided)
    if content["metrics"]:
        parts.append("**Production metrics**:")
        for metric in content["metrics"]:
            parts.append(f"- {metric}")
        parts.append("")

    # Separator and prompt
    parts.append("---\n")
    parts.append("## Prompt\n")
    parts.append("```")
    parts.append(str(content["prompt"]))
    parts.append("```\n")

    # Placeholder sections
    parts.append("---\n")
    parts.append("## Production Patterns\n")
    parts.append("TODO: Add production usage patterns and examples\n")

    parts.append("---\n")
    parts.append("## Quality Evaluation\n")
    parts.append("TODO: Add quality evaluation criteria\n")

    parts.append("---\n")
    parts.append("## Usage Notes\n")
    parts.append("TODO: Add usage tips and best practices\n")

    parts.append("---\n")
    parts.append("## Common Issues & Fixes\n")
    parts.append("TODO: Add common issues and their solutions\n")

    parts.append("---\n")
    parts.append("## Related Prompts\n")
    parts.append("TODO: Link to related prompt patterns\n")

    return "\n".join(parts)


def create_claude_prompt(
    metadata: Dict[str, str], content: Dict[str, Union[str, List[str]]]
) -> str:
    """Generate the Claude-optimized prompt.claude.md file."""

    parts = [f"# {metadata['name']} - Claude Optimized\n"]
    parts.append("> Extends `prompt.md` with Claude-specific optimizations\n")

    parts.append("## Prompt\n")
    parts.append("<task>")
    parts.append(str(content["prompt"]))
    parts.append("</task>\n")

    parts.append("## Claude Optimizations Applied\n")
    parts.append("- **XML structure**: Uses XML tags for clear task delineation and better parsing")
    parts.append(
        "- **Structured thinking**: Encourages use of `<thinking>` tags for complex reasoning"
    )
    parts.append("- **Prompt caching**: Static prompt content is cacheable for 90%+ cost savings")
    parts.append("- **Extended context**: Leverages Claude's 200K token context window\n")

    parts.append("## Usage\n")
    parts.append("```python")
    parts.append("from pm_prompt_toolkit.providers import get_provider\n")
    parts.append("# Initialize Claude provider with caching")
    parts.append('provider = get_provider("claude-sonnet-4-5", enable_caching=True)\n')
    parts.append("result = provider.generate(")
    parts.append('    system_prompt="<prompt from above>",')
    parts.append('    user_message="<your content here>"')
    parts.append(")")
    parts.append("```\n")

    parts.append("## See Also\n")
    parts.append("- Base prompt: `prompt.md` (examples, testing checklist, business value)")
    parts.append("- Provider documentation: `../../docs/provider-specific-prompts.md`\n")

    return "\n".join(parts)


def create_openai_prompt(
    metadata: Dict[str, str], content: Dict[str, Union[str, List[str]]]
) -> str:
    """Generate the OpenAI-optimized prompt.openai.md file."""

    parts = [f"# {metadata['name']} - OpenAI Optimized\n"]
    parts.append("> Extends `prompt.md` with OpenAI-specific optimizations\n")

    parts.append("## System Prompt\n")
    parts.append("```")
    parts.append(str(content["prompt"]))
    parts.append("```\n")

    parts.append("## OpenAI Optimizations Applied\n")
    parts.append(
        "- **Clear role definition**: Explicit system message with role and responsibilities"
    )
    parts.append("- **Structured output**: Consistent formatting instructions")
    parts.append(
        "- **Function calling ready**: Can be combined with function schemas for structured output"
    )
    parts.append(
        "- **Concise directives**: Optimized for GPT-4's instruction-following capabilities\n"
    )

    parts.append("## Usage\n")
    parts.append("```python")
    parts.append("from pm_prompt_toolkit.providers import get_provider\n")
    parts.append("# Initialize OpenAI provider")
    parts.append('provider = get_provider("gpt-4o")\n')
    parts.append("result = provider.generate(")
    parts.append('    system_prompt="<prompt from above>",')
    parts.append('    user_message="<your content here>"')
    parts.append(")")
    parts.append("```\n")

    parts.append("## Model Recommendations\n")
    parts.append("- **gpt-4o**: Best balance of speed, quality, and cost for most use cases")
    parts.append("- **gpt-4o-mini**: Faster and more cost-effective for simpler tasks")
    parts.append("- **gpt-4-turbo**: Use for extended context needs (>128k tokens)\n")

    parts.append("## See Also\n")
    parts.append("- Base prompt: `prompt.md` (examples, testing checklist, business value)")
    parts.append("- Provider documentation: `../../docs/provider-specific-prompts.md`\n")

    return "\n".join(parts)


def create_gemini_prompt(
    metadata: Dict[str, str], content: Dict[str, Union[str, List[str]]]
) -> str:
    """Generate the Gemini-optimized prompt.gemini.md file."""

    parts = [f"# {metadata['name']} - Gemini Optimized\n"]
    parts.append("> Extends `prompt.md` with Gemini-specific optimizations\n")

    parts.append("## System Instruction\n")
    parts.append("```")
    parts.append(str(content["prompt"]))
    parts.append("```\n")

    parts.append("## Gemini Optimizations Applied\n")
    parts.append(
        "- **Clear directives**: Explicit, numbered instructions for better instruction-following"
    )
    parts.append("- **Context utilization**: Optimized for Gemini's large context window")
    parts.append(
        "- **Multimodal ready**: Can process code alongside diagrams, screenshots, or other media"
    )
    parts.append("- **Structured reasoning**: Step-by-step breakdown for complex analysis tasks\n")

    parts.append("## Usage\n")
    parts.append("```python")
    parts.append("from pm_prompt_toolkit.providers import get_provider\n")
    parts.append("# Initialize Gemini provider")
    parts.append('provider = get_provider("gemini-2.0-flash-exp")\n')
    parts.append("result = provider.generate(")
    parts.append('    system_instruction="<prompt from above>",')
    parts.append('    contents="<your content here>"')
    parts.append(")")
    parts.append("```\n")

    parts.append("## Model Recommendations\n")
    parts.append("- **gemini-2.0-flash-exp**: Best for most use cases (fast, high quality)")
    parts.append("- **gemini-1.5-pro**: Maximum context window (2M tokens)")
    parts.append("- **gemini-1.5-flash**: Fastest option for simpler tasks\n")

    parts.append("## See Also\n")
    parts.append("- Base prompt: `prompt.md` (examples, testing checklist, business value)")
    parts.append("- Provider documentation: `../../docs/provider-specific-prompts.md`\n")

    return "\n".join(parts)


def validate_prompt_structure(prompt_dir: Path) -> bool:
    """Validate that all required files exist and follow guidelines."""
    print("\n=== VALIDATING PROMPT STRUCTURE ===")

    required_files = [
        "prompt.md",
        "prompt.claude.md",
        "prompt.openai.md",
        "prompt.gemini.md",
    ]

    all_valid = True

    for filename in required_files:
        filepath = prompt_dir / filename
        if not filepath.exists():
            print(f"❌ Missing file: {filename}")
            all_valid = False
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Validate base prompt
        if filename == "prompt.md":
            if "## Overview" not in content:
                print(f"⚠️  {filename}: Missing '## Overview' section")
                all_valid = False
            if "## Prompt" not in content:
                print(f"⚠️  {filename}: Missing '## Prompt' section")
                all_valid = False
            if "<task>" in content or "</task>" in content:
                print(f"⚠️  {filename}: Contains model-specific XML tags (should be model-agnostic)")
                all_valid = False
            else:
                print(f"✅ {filename}: Valid base prompt")

        # Validate Claude file
        elif filename == "prompt.claude.md":
            if "<task>" not in content:
                print(f"⚠️  {filename}: Missing <task> wrapper (Claude optimization)")
                all_valid = False
            if "OpenAI" in content or "Gemini" in content:
                print(f"⚠️  {filename}: Contains references to other models")
                all_valid = False
            if "prompt.md" not in content:
                print(f"⚠️  {filename}: Should reference base prompt.md file")
                all_valid = False
            else:
                print(f"✅ {filename}: Valid Claude prompt")

        # Validate OpenAI file
        elif filename == "prompt.openai.md":
            if "Claude" in content or "Gemini" in content:
                print(f"⚠️  {filename}: Contains references to other models")
                all_valid = False
            if "prompt.md" not in content:
                print(f"⚠️  {filename}: Should reference base prompt.md file")
                all_valid = False
            else:
                print(f"✅ {filename}: Valid OpenAI prompt")

        # Validate Gemini file
        elif filename == "prompt.gemini.md":
            if "Claude" in content or "OpenAI" in content:
                print(f"⚠️  {filename}: Contains references to other models")
                all_valid = False
            if "prompt.md" not in content:
                print(f"⚠️  {filename}: Should reference base prompt.md file")
                all_valid = False
            else:
                print(f"✅ {filename}: Valid Gemini prompt")

    return all_valid


def main() -> None:
    """Main script execution."""
    print("=" * 70)
    print("CREATE NEW PROMPT PATTERN")
    print("=" * 70)

    # Get metadata
    metadata = get_prompt_metadata()

    # Get content
    content = get_prompt_content()

    # Confirm before creating
    print("\n=== SUMMARY ===")
    print(f"Name: {metadata['name']}")
    print(f"Filename: {metadata['filename']}")
    print(f"Category: {metadata['category']}")
    print(f"Complexity: {metadata['complexity']}")
    print(f"Overview: {content['overview'][:80]}...")

    confirm = input("\nCreate prompt files? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return

    # Create directory
    repo_root = Path(__file__).parent.parent
    prompt_dir = repo_root / "prompts" / metadata["category"] / metadata["filename"]
    prompt_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== CREATING FILES IN {prompt_dir.relative_to(repo_root)} ===")

    # Create base prompt
    base_content = create_base_prompt(metadata, content)
    base_file = prompt_dir / "prompt.md"
    with open(base_file, "w", encoding="utf-8") as f:
        f.write(base_content)
    print(f"✓ Created {base_file.name}")

    # Create Claude prompt
    claude_content = create_claude_prompt(metadata, content)
    claude_file = prompt_dir / "prompt.claude.md"
    with open(claude_file, "w", encoding="utf-8") as f:
        f.write(claude_content)
    print(f"✓ Created {claude_file.name}")

    # Create OpenAI prompt
    openai_content = create_openai_prompt(metadata, content)
    openai_file = prompt_dir / "prompt.openai.md"
    with open(openai_file, "w", encoding="utf-8") as f:
        f.write(openai_content)
    print(f"✓ Created {openai_file.name}")

    # Create Gemini prompt
    gemini_content = create_gemini_prompt(metadata, content)
    gemini_file = prompt_dir / "prompt.gemini.md"
    with open(gemini_file, "w", encoding="utf-8") as f:
        f.write(gemini_content)
    print(f"✓ Created {gemini_file.name}")

    # Validate structure
    is_valid = validate_prompt_structure(prompt_dir)

    print("\n" + "=" * 70)
    if is_valid:
        print("✅ SUCCESS! Prompt pattern created and validated.")
        print("\nNext steps:")
        print(f"1. Edit {prompt_dir.relative_to(repo_root)}/prompt.md to add examples")
        print("2. Review model-specific optimizations in variant files")
        print("3. Add production patterns and usage notes")
        print(f"4. Commit the changes: git add {prompt_dir.relative_to(repo_root)}")
    else:
        print("⚠️  WARNING: Some validation checks failed.")
        print("Please review the files and fix any issues.")

    print("=" * 70)


if __name__ == "__main__":
    main()
