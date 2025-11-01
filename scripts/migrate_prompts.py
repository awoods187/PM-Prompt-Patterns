#!/usr/bin/env python3
# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
Multi-Provider Prompt Migration Tool

Migrates single-file prompts to multi-provider directory structure with
provider-specific optimizations for Claude, OpenAI, and Gemini.

Usage:
    python scripts/migrate_prompts.py --dry-run          # Preview changes
    python scripts/migrate_prompts.py                    # Migrate all prompts
    python scripts/migrate_prompts.py --prompt <path>    # Migrate specific prompt
    python scripts/migrate_prompts.py --skip-existing    # Skip already migrated
"""

import argparse
import re
import shutil
from pathlib import Path
from typing import Dict, List


class PromptMigrator:
    """Migrates single-file prompts to multi-provider structure."""

    def __init__(self, prompts_dir: Path, dry_run: bool = False):
        self.prompts_dir = prompts_dir
        self.dry_run = dry_run
        self.changes: List[str] = []

    def find_single_file_prompts(self) -> List[Path]:
        """Find all single-file prompts that need migration."""
        prompts = []

        for md_file in self.prompts_dir.rglob("*.md"):
            # Skip README files
            if md_file.name == "README.md":
                continue

            # Skip if already in multi-provider structure
            parent_dir = md_file.parent
            if self._is_multi_provider_dir(parent_dir):
                continue

            # Skip if file is already a provider variant
            if md_file.stem.startswith("prompt."):
                continue

            prompts.append(md_file)

        return sorted(prompts)

    def _is_multi_provider_dir(self, directory: Path) -> bool:
        """Check if directory already has multi-provider structure."""
        files = [f.name for f in directory.glob("*.md")]
        return "prompt.md" in files or any(
            f.startswith("prompt.") and f.endswith(".md") for f in files
        )

    def migrate_prompt(self, prompt_file: Path) -> bool:
        """
        Migrate a single prompt to multi-provider structure.

        Returns:
            True if migration was performed, False if skipped
        """
        # Determine new directory structure
        prompt_dir = prompt_file.parent / prompt_file.stem
        base_file = prompt_dir / "prompt.md"
        claude_file = prompt_dir / "prompt.claude.md"
        openai_file = prompt_dir / "prompt.openai.md"
        gemini_file = prompt_dir / "prompt.gemini.md"
        readme_file = prompt_dir / "README.md"

        # Read original prompt content
        original_content = prompt_file.read_text(encoding="utf-8")

        # Extract metadata
        metadata = self._extract_metadata(original_content, prompt_file)

        self.log(f"\n{'='*80}")
        self.log(f"Migrating: {prompt_file.relative_to(self.prompts_dir)}")
        self.log(f"To: {prompt_dir.relative_to(self.prompts_dir)}/")

        if not self.dry_run:
            # Create directory
            prompt_dir.mkdir(parents=True, exist_ok=True)

            # Move/copy original to base variant
            shutil.copy2(prompt_file, base_file)
            self.log("  ✓ Created base variant: prompt.md")

            # Generate provider-specific variants
            self._generate_claude_variant(original_content, claude_file, metadata)
            self.log("  ✓ Created Claude variant: prompt.claude.md")

            self._generate_openai_variant(original_content, openai_file, metadata)
            self.log("  ✓ Created OpenAI variant: prompt.openai.md")

            self._generate_gemini_variant(original_content, gemini_file, metadata)
            self.log("  ✓ Created Gemini variant: prompt.gemini.md")

            # Generate README
            self._generate_readme(readme_file, metadata)
            self.log("  ✓ Created README.md")

            # Delete original file
            prompt_file.unlink()
            self.log("  ✓ Removed original file")
        else:
            self.log("  [DRY RUN] Would create:")
            self.log(f"    - {base_file.relative_to(self.prompts_dir)}")
            self.log(f"    - {claude_file.relative_to(self.prompts_dir)}")
            self.log(f"    - {openai_file.relative_to(self.prompts_dir)}")
            self.log(f"    - {gemini_file.relative_to(self.prompts_dir)}")
            self.log(f"    - {readme_file.relative_to(self.prompts_dir)}")
            self.log(f"  [DRY RUN] Would remove: {prompt_file.relative_to(self.prompts_dir)}")

        return True

    def _extract_metadata(self, content: str, file_path: Path) -> Dict[str, str]:
        """Extract metadata from prompt content."""
        # Extract title (first # heading)
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1) if title_match else file_path.stem.replace("-", " ").title()

        # Extract purpose/description (first paragraph after title)
        purpose = "No description available"
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("# "):
                # Find first non-empty line after title
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() and not lines[j].startswith("#"):
                        purpose = lines[j].strip()
                        break
                break

        return {
            "title": title,
            "purpose": purpose,
            "category": file_path.parent.name,
            "name": file_path.stem,
        }

    def _generate_claude_variant(
        self, base_content: str, output_file: Path, metadata: Dict[str, str]
    ) -> None:
        """Generate Claude-optimized variant with XML tags."""
        # Add Claude-specific header
        claude_content = f"""# {metadata['title']} (Claude Optimized)

**Provider:** Claude (Anthropic)
**Optimizations:** XML tags, chain-of-thought reasoning, prompt caching

{metadata['purpose']}

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
prompt = get_prompt("{metadata['category']}/{metadata['name']}", provider="claude")

# Use with caching for cost savings
provider = get_provider("claude-sonnet-4-5", enable_caching=True)
result = provider.generate(prompt)
```

---

## Original Prompt (Enhanced with XML)

<task>
{base_content}
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
"""
        output_file.write_text(claude_content, encoding="utf-8")

    def _generate_openai_variant(
        self, base_content: str, output_file: Path, metadata: Dict[str, str]
    ) -> None:
        """Generate OpenAI-optimized variant with function calling."""
        openai_content = f"""# {metadata['title']} (OpenAI Optimized)

**Provider:** OpenAI
**Optimizations:** Function calling, JSON mode, structured outputs

{metadata['purpose']}

## OpenAI-Specific Features

This variant is optimized for OpenAI models with:
- **Function calling** for guaranteed structured output
- **JSON mode** for valid JSON responses
- **Parallel tool calls** for batch processing
- **Reproducible results** with seed parameter

## Usage with Function Calling

```python
from ai_models import get_prompt
import openai

prompt = get_prompt("{metadata['category']}/{metadata['name']}", provider="openai")

# Define function schema for structured output
function_schema = {{
    "name": "process_prompt",
    "description": "Process the prompt and return structured output",
    "parameters": {{
        "type": "object",
        "properties": {{
            "result": {{"type": "string", "description": "The processed result"}},
            "confidence": {{"type": "number", "minimum": 0.0, "maximum": 1.0}},
            "reasoning": {{"type": "string", "description": "Step-by-step reasoning"}}
        }},
        "required": ["result", "confidence", "reasoning"]
    }}
}}

# Use with GPT-4o or GPT-4o-mini
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {{"role": "system", "content": prompt}},
        {{"role": "user", "content": "Your input here"}}
    ],
    functions=[function_schema],
    function_call={{"name": "process_prompt"}},
    temperature=0.0  # Deterministic output
)

result = json.loads(response.choices[0].message.function_call.arguments)
```

## Usage with JSON Mode

```python
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {{"role": "system", "content": prompt}},
        {{"role": "user", "content": "Your input here"}}
    ],
    response_format={{"type": "json_object"}},
    temperature=0.0
)

result = json.loads(response.choices[0].message.content)
```

---

## Original Prompt

{base_content}

---

## Model Recommendations

- **GPT-4o-mini**: Best value, 94% of GPT-4o accuracy ($0.15/$0.60 per 1M tokens)
- **GPT-4o**: Balanced performance ($2.50/$10.00 per 1M tokens)
- **gpt-4o**: For complex reasoning ($10/$30 per 1M tokens)
"""
        output_file.write_text(openai_content, encoding="utf-8")

    def _generate_gemini_variant(
        self, base_content: str, output_file: Path, metadata: Dict[str, str]
    ) -> None:
        """Generate Gemini-optimized variant with caching and large context."""
        gemini_content = f"""# {metadata['title']} (Gemini Optimized)

**Provider:** Google Gemini
**Optimizations:** 2M token context, caching, ultra-low cost

{metadata['purpose']}

## Gemini-Specific Features

This variant is optimized for Gemini models with:
- **2M token context window** for massive batch processing
- **Context caching** for 74% cost reduction
- **Native JSON schema** for structured outputs
- **Ultra-low cost** Flash models (10x cheaper than competitors)

## Usage with Context Caching

```python
from ai_models import get_prompt
import google.generativeai as genai
import datetime

prompt = get_prompt("{metadata['category']}/{metadata['name']}", provider="gemini")

# Create cached content (reusable for 1 hour)
cached_content = genai.caching.CachedContent.create(
    model="gemini-2.5-flash",
    display_name="{metadata['name']}-cache",
    system_instruction=prompt,
    ttl=datetime.timedelta(hours=1)
)

# Use cached model for massive cost savings
model = genai.GenerativeModel.from_cached_content(cached_content)

# First request: $0.075/1M tokens
# Subsequent requests: $0.019/1M tokens (74% savings!)
result = model.generate_content("Your input here")
```

## Usage with JSON Schema

```python
import google.generativeai as genai

generation_config = {{
    "temperature": 0.1,
    "response_mime_type": "application/json",
    "response_schema": {{
        "type": "object",
        "properties": {{
            "result": {{"type": "string"}},
            "confidence": {{"type": "number", "minimum": 0.0, "maximum": 1.0}},
            "reasoning": {{"type": "string"}}
        }},
        "required": ["result", "confidence", "reasoning"]
    }}
}}

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config,
    system_instruction=prompt
)

# Guaranteed valid JSON matching schema
response = model.generate_content("Your input here")
result = json.loads(response.text)
```

## Batch Processing (2M Context)

```python
# Process 1000+ items in single request
batch_input = "\\n".join([f"{{i}}. {{item}}" for i, item in enumerate(items, 1)])
response = model.generate_content(batch_input)

# Cost: ~$0.10 for 1000 items vs $100+ per-item approach
```

---

## Original Prompt

{base_content}

---

## Model Recommendations

- **Gemini 2.5 Flash Lite**: Ultra-low cost, real-time ($0.038/$0.15 per 1M tokens)
- **Gemini 2.5 Flash**: High volume, balanced ($0.075/$0.30 per 1M tokens)
- **Gemini 2.5 Pro**: Highest accuracy, large context ($1.25/$5.00 per 1M tokens)
"""
        output_file.write_text(gemini_content, encoding="utf-8")

    def _generate_readme(self, output_file: Path, metadata: Dict[str, str]) -> None:
        """Generate README with prompt metadata and usage guide."""
        readme_content = f"""# {metadata['title']}

## 🎯 Purpose

{metadata['purpose']}

## 📊 Provider Variants

| Provider | File | Key Features | Best For | Cost Range |
|----------|------|-------------|----------|------------|
| **Base** | [`prompt.md`](./prompt.md) | Universal compatibility | Any provider, fallback | Varies |
| **Claude** | [`prompt.claude.md`](./prompt.claude.md) | XML tags, chain-of-thought | Complex reasoning, accuracy | $1-15 per 1M tokens |
| **OpenAI** | [`prompt.openai.md`](./prompt.openai.md) | Function calling, JSON mode | Structured output, integration | $0.15-10 per 1M tokens |
| **Gemini** | [`prompt.gemini.md`](./prompt.gemini.md) | 2M context, caching | High volume, batch processing | $0.038-5 per 1M tokens |

## 🚀 Quick Start

### Automatic Provider Selection

```python
from ai_models import get_prompt, get_model

# Auto-select best variant based on model
model = get_model("gpt-4o")
prompt = get_prompt("{metadata['category']}/{metadata['name']}", model=model.id)

# Use the prompt
result = model.generate(prompt.format(**your_variables))
```

### Manual Provider Selection

```python
# Explicit provider selection
claude_prompt = get_prompt("{metadata['category']}/{metadata['name']}", provider="claude")
openai_prompt = get_prompt("{metadata['category']}/{metadata['name']}", provider="openai")
gemini_prompt = get_prompt("{metadata['category']}/{metadata['name']}", provider="gemini")
```

## 🎯 When to Use Each Provider

### Use Claude when:
- ✅ Accuracy is critical
- ✅ Complex reasoning required
- ✅ Need detailed explanations
- ✅ Can leverage prompt caching (90% savings)

### Use OpenAI when:
- ✅ Need strict JSON schema validation
- ✅ Function calling for integration
- ✅ Batch processing with parallel tools
- ✅ Reproducible results required

### Use Gemini when:
- ✅ Ultra-high volume (10K+ operations/day)
- ✅ Cost is primary concern
- ✅ Can batch operations together
- ✅ Need large context window (2M tokens)

## 📚 Examples

See the individual prompt files for detailed usage examples:
- [Base Prompt](./prompt.md) - Universal examples
- [Claude Examples](./prompt.claude.md) - XML format, caching
- [OpenAI Examples](./prompt.openai.md) - Function calling, batch processing
- [Gemini Examples](./prompt.gemini.md) - Context window, ultra-low cost

## 🔗 Related Prompts

Browse more prompts in the [prompts directory](../../).

## 📝 Notes

- All variants return compatible output formats
- Provider selection is based on your specific use case requirements
- Cost estimates are approximate and vary by usage patterns
- See [provider-specific-prompts.md](../../docs/provider-specific-prompts.md) for detailed optimization guide

---

*Auto-generated by migration tool. Edit individual variant files for customization.*
"""
        output_file.write_text(readme_content, encoding="utf-8")

    def log(self, message: str) -> None:
        """Log a message."""
        print(message)
        self.changes.append(message)

    def migrate_all(self, skip_existing: bool = False) -> Dict[str, int]:
        """
        Migrate all single-file prompts.

        Returns:
            Dictionary with migration statistics
        """
        prompts = self.find_single_file_prompts()

        stats = {"total": len(prompts), "migrated": 0, "skipped": 0, "errors": 0}

        self.log(f"\nFound {len(prompts)} prompts to migrate")
        self.log(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE MIGRATION'}")

        for prompt_file in prompts:
            try:
                if skip_existing and self._is_multi_provider_dir(prompt_file.parent):
                    self.log(
                        f"Skipping (already migrated): {prompt_file.relative_to(self.prompts_dir)}"
                    )
                    stats["skipped"] += 1
                    continue

                if self.migrate_prompt(prompt_file):
                    stats["migrated"] += 1
            except Exception as e:
                self.log(f"ERROR migrating {prompt_file}: {e}")
                stats["errors"] += 1

        return stats


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Migrate prompts to multi-provider structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="Migrate specific prompt (path relative to prompts/)",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip prompts that are already in multi-provider format",
    )
    parser.add_argument(
        "--prompts-dir",
        type=Path,
        default=Path(__file__).parent.parent / "prompts",
        help="Path to prompts directory (default: ../prompts)",
    )

    args = parser.parse_args()

    # Initialize migrator
    migrator = PromptMigrator(args.prompts_dir, dry_run=args.dry_run)

    # Migrate
    if args.prompt:
        # Migrate specific prompt
        prompt_file = args.prompts_dir / args.prompt
        if not prompt_file.exists():
            print(f"Error: Prompt not found: {prompt_file}")
            return 1

        migrator.migrate_prompt(prompt_file)
        stats = {"total": 1, "migrated": 1, "skipped": 0, "errors": 0}
    else:
        # Migrate all prompts
        stats = migrator.migrate_all(skip_existing=args.skip_existing)

    # Print summary
    print("\n" + "=" * 80)
    print("MIGRATION SUMMARY")
    print("=" * 80)
    print(f"Total prompts found: {stats['total']}")
    print(f"Migrated: {stats['migrated']}")
    print(f"Skipped: {stats['skipped']}")
    print(f"Errors: {stats['errors']}")

    if args.dry_run:
        print("\n⚠️  DRY RUN - No changes were made")
        print("Run without --dry-run to perform actual migration")
    else:
        print("\n✅ Migration complete!")

    return 0 if stats["errors"] == 0 else 1


if __name__ == "__main__":
    exit(main())
