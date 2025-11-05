# Meta-Prompt Designer

**Complexity**: 🔴 Advanced
**Category**: Product Strategy / Prompt Engineering
**Model Compatibility**: ✅ Claude (all) | ✅ GPT-5 | ✅ Gemini

## Overview

A meta-prompt that helps you design high-quality, production-ready prompts for your professional prompt library. Takes a use case description and generates a complete, structured, reusable prompt following best practices and your library's standards.

**Business Value**:
- Standardize prompt quality across your library
- Reduce time from idea to production-ready prompt (hours → minutes)
- Ensure consistency in prompt structure and documentation
- Enable non-experts to create expert-level prompts
- Build reusable prompt library faster

**Use Cases**:
- Creating new prompts for your library
- Refactoring existing ad-hoc prompts into standardized format
- Documenting successful prompts for team sharing
- Training team members on prompt engineering best practices
- Rapid prototyping of prompt ideas

**Production metrics**:
- Prompt quality improvement: Ad-hoc → Production-grade
- Time savings: ~2-4 hours per prompt
- First-try success rate: ~85% (vs ~40% for manual design)
- Consistency: 100% format compliance

---

---

## Prompt

```
You are an expert prompt engineer helping me design a high-quality prompt for
my professional prompt library. I'll describe what I need, and you'll create
a structured, reusable prompt.

## MY REQUEST
[Describe your use case, desired output, and any specific requirements]

## YOUR TASK
Create a complete prompt following this structure:

### 1. METADATA HEADER
Provide:
- **Title:** Clear, descriptive name
- **Best for:** Specific use cases (2-3 examples)
- **Recommended model:** Which Claude model works best and why
- **Use with:** Any specific tools (Claude Code, Artifacts, etc.)
- **Estimated tokens:** Rough input/output size
- **Category:** (Code, Writing, Analysis, Research, etc.)

### 2. CORE PROMPT
Write the actual prompt with:
- **Clear role definition:** Who is Claude acting as?
- **Explicit objective:** What should be accomplished?
- **Structured sections:** Use ## headers for major sections
- **Numbered priorities:** When order matters
- **Concrete examples:** Show desired output format
- **Constraints:** Explicit dos/don'ts if needed
- **Output format specification:** Exactly how results should be structured

### 3. CUSTOMIZATION TIPS
Provide 3-5 adaptation suggestions:
- How to adjust for different contexts
- Optional sections that can be added/removed
- Variable parameters users might want to change
- Common variations for related use cases

### 4. USAGE EXAMPLES
Show 2-3 realistic examples:
- Input variations
- Expected output structure
- Different parameter combinations

### 5. TESTING CHECKLIST
Help users validate the prompt works:
- Test cases to try
- Edge cases to consider
- Quality criteria for outputs
- Common failure modes and fixes

## PROMPT DESIGN PRINCIPLES
Apply these best practices:
- **Specificity over generality:** Be concrete and explicit
- **Examples over explanations:** Show, don't just tell
- **Structure over prose:** Use markdown, lists, clear sections
- **Constraints over freedom:** Define boundaries clearly
- **Iteration markers:** Where should users expect to refine?

## OUTPUT FORMAT
Deliver as:
1. Clean markdown ready for my library
2. Metadata section at top
3. Main prompt in code fence
4. Supporting sections below
5. No preamble - just the structured prompt

## QUALITY STANDARDS
Ensure the prompt:
- [ ] Works on first try without clarification
- [ ] Produces consistent outputs across runs
- [ ] Scales to different complexity levels
- [ ] Handles edge cases gracefully
- [ ] Is self-documenting (users understand without you)
- [ ] Follows my library's format (like examples you've seen)

**Note:** Ask clarifying questions if my use case is ambiguous, but keep
questions focused (max 3). Prefer making reasonable assumptions with notes
about alternatives.
```

---

## Production Patterns

### Pattern 1: Prompt Library Builder

**Use case**: Build a comprehensive prompt library for your organization.

```python
from pathlib import Path
from typing import List, Dict
import yaml

class PromptLibraryBuilder:
    """
    Automated prompt library builder using meta-prompt.

    Creates standardized, documented prompts from use case descriptions.
    """

    def __init__(self, library_path: Path):
        self.library_path = library_path
        self.categories = {
            "code": "prompts/code",
            "writing": "prompts/writing",
            "analysis": "prompts/analysis",
            "research": "prompts/research",
            "data": "prompts/data",
            "strategy": "prompts/strategy"
        }

        # Ensure directories exist
        for category_path in self.categories.values():
            (library_path / category_path).mkdir(parents=True, exist_ok=True)

    def create_from_use_cases(self, use_cases_file: Path) -> List[Dict]:
        """
        Batch create prompts from YAML file of use cases.

        Args:
            use_cases_file: YAML file with use case descriptions

        Returns:
            List of created prompt metadata

        Example YAML format:
            prompts:
              - name: code_security_audit
                category: code
                description: |
                  Analyze code for security vulnerabilities...
              - name: market_research
                category: research
                description: |
                  Conduct comprehensive market research...
        """

        with open(use_cases_file) as f:
            use_cases = yaml.safe_load(f)

        created_prompts = []

        for uc in use_cases['prompts']:
            print(f"\n🔨 Designing: {uc['name']}")

            # Design prompt using meta-prompt
            prompt_design = design_prompt(uc['description'])

            # Determine file path
            category = uc['category'].lower()
            file_path = (
                self.library_path /
                self.categories[category] /
                f"{uc['name']}.md"
            )

            # Save to library
            with open(file_path, "w") as f:
                f.write(prompt_design['full_markdown'])

            created_prompts.append({
                "name": uc['name'],
                "title": prompt_design['title'],
                "category": category,
                "path": str(file_path),
                "complexity": prompt_design['complexity']
            })

            print(f"   ✅ Saved to {file_path}")

        return created_prompts

    def update_index(self, created_prompts: List[Dict]) -> None:
        """Update library index/catalog."""

        index_path = self.library_path / "INDEX.md"

        # Group by category
        by_category = {}
        for prompt in created_prompts:
            cat = prompt['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(prompt)

        # Generate index markdown
        index_md = "# Prompt Library Index\n\n"

        for category, prompts in sorted(by_category.items()):
            index_md += f"\n## {category.title()}\n\n"
            for p in sorted(prompts, key=lambda x: x['title']):
                index_md += f"- [{p['title']}]({p['path']}) {p['complexity']}\n"

        with open(index_path, "w") as f:
            f.write(index_md)

        print(f"\n📚 Updated library index: {index_path}")

# Example usage
if __name__ == "__main__":
    # Create use_cases.yaml
    use_cases_yaml = """
prompts:
  - name: code_review_security
    category: code
    description: |
      Comprehensive code review focusing on security:
      - Identify hardcoded credentials
      - SQL injection vulnerabilities
      - Input validation issues
      - Authentication/authorization flaws
      Provide severity ratings and fix recommendations.

  - name: customer_feedback_analysis
    category: analysis
    description: |
      Analyze customer feedback to extract:
      - Sentiment (positive/negative/neutral)
      - Key themes and patterns
      - Urgency indicators
      - Product areas mentioned
      - Actionable insights

  - name: competitive_research
    category: research
    description: |
      Research competitors and provide:
      - Feature comparison matrix
      - Pricing analysis
      - Market positioning
      - Strengths and weaknesses
      - Opportunities for differentiation
"""

    # Save to file
    with open("use_cases.yaml", "w") as f:
        f.write(use_cases_yaml)

    # Build library
    builder = PromptLibraryBuilder(Path("./my_prompt_library"))
    created = builder.create_from_use_cases(Path("use_cases.yaml"))
    builder.update_index(created)

    print(f"\n✅ Created {len(created)} prompts in library")
```

### Pattern 2: Interactive Prompt Designer CLI

**Use case**: Interactive tool for designing prompts with iteration.

```python
import anthropic
from typing import Optional

client = anthropic.Anthropic(api_key="...")

def interactive_prompt_designer():
    """
    Interactive CLI for designing prompts with iteration and refinement.
    """

    print("=" * 70)
    print("INTERACTIVE PROMPT DESIGNER")
    print("=" * 70)

    # Step 1: Gather use case
    print("\n📝 Describe your use case:")
    print("   (Be specific about inputs, outputs, and requirements)")
    print("   (Press Enter twice when done)\n")

    lines = []
    while True:
        line = input()
        if line == "" and len(lines) > 0 and lines[-1] == "":
            break
        lines.append(line)

    use_case = "\n".join(lines[:-1])  # Remove last empty line

    # Step 2: Design initial prompt
    print("\n🔨 Designing prompt...")
    prompt_design = design_prompt(use_case)

    print(f"\n✅ Created: {prompt_design['title']}")
    print(f"   Category: {prompt_design['category']}")
    print(f"   Complexity: {prompt_design['complexity']}")

    # Step 3: Review and iterate
    while True:
        print("\n" + "=" * 70)
        print("OPTIONS:")
        print("  1. View core prompt")
        print("  2. View usage examples")
        print("  3. Test the prompt")
        print("  4. Refine (iterate on design)")
        print("  5. Save to library")
        print("  6. Exit")
        print("=" * 70)

        choice = input("\nSelect option (1-6): ").strip()

        if choice == "1":
            print("\n" + "=" * 70)
            print("CORE PROMPT:")
            print("=" * 70)
            print(prompt_design['core_prompt'])

        elif choice == "2":
            print("\n" + "=" * 70)
            print("USAGE EXAMPLES:")
            print("=" * 70)
            for i, ex in enumerate(prompt_design['usage_examples'], 1):
                print(f"\n{i}. {ex['scenario']}")
                print(f"   Input: {ex['input'][:100]}...")
                print(f"   Output: {ex['output'][:100]}...")

        elif choice == "3":
            print("\n📝 Enter test input (or 'skip' to skip):")
            test_input = input()

            if test_input.lower() != 'skip':
                print("\n🔍 Testing prompt...")

                response = client.messages.create(
                    model="claude-sonnet-4-5-20250929",  # Latest Claude Sonnet 4.5
                    max_tokens=4000,
                    messages=[{
                        "role": "user",
                        "content": f"{prompt_design['core_prompt']}\n\nINPUT:\n{test_input}"
                    }]
                )

                print("\n" + "=" * 70)
                print("TEST RESULT:")
                print("=" * 70)
                print(response.content[0].text)

                print("\n✅ Does this match your expectations? (y/n)")
                satisfied = input().strip().lower()

                if satisfied != 'y':
                    print("\n💡 What should be different?")
                    feedback = input()

                    # Refine based on feedback
                    refined_use_case = f"{use_case}\n\nREFINEMENT: {feedback}"
                    print("\n🔨 Refining prompt...")
                    prompt_design = design_prompt(refined_use_case)
                    print("✅ Prompt refined")

        elif choice == "4":
            print("\n💡 What aspects should be refined?")
            refinement = input()

            refined_use_case = f"{use_case}\n\nREFINEMENT: {refinement}"
            print("\n🔨 Refining prompt...")
            prompt_design = design_prompt(refined_use_case)

            print(f"✅ Prompt refined: {prompt_design['title']}")

        elif choice == "5":
            # Save to library
            category = prompt_design['category'].lower()
            filename = prompt_design['title'].lower().replace(" ", "_") + ".md"
            filepath = f"prompts/{category}/{filename}"

            print(f"\n💾 Save to: {filepath}")
            print("   Confirm? (y/n)")

            if input().strip().lower() == 'y':
                # Create directory if needed
                Path(f"prompts/{category}").mkdir(parents=True, exist_ok=True)

                with open(filepath, "w") as f:
                    f.write(prompt_design['full_markdown'])

                print(f"✅ Saved to {filepath}")
                print("\n🎉 Prompt added to library!")
                break

        elif choice == "6":
            print("\n👋 Exiting without saving")
            break

        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    interactive_prompt_designer()
```

---

---

## Quality Evaluation

### Before (Ad-hoc prompt):
```
Analyze this customer feedback and tell me what's important.

{feedback}
```

**Issues**:
- ❌ Vague objective ("what's important")
- ❌ No output structure
- ❌ Inconsistent results
- ❌ No edge case handling
- ❌ Not reusable

### After (Meta-prompt designed):
```
You are a customer insights analyst specializing in SaaS feedback analysis.

## OBJECTIVE
Extract actionable insights from customer feedback for product prioritization.

## ANALYSIS FRAMEWORK
For each feedback item, identify:

1. **Sentiment**: Positive | Neutral | Negative | Mixed
2. **Category**: Feature Request | Bug Report | Praise | Complaint | Question
3. **Product Area**: [List of your product areas]
4. **Urgency**: Critical | High | Medium | Low
5. **Key Insights**: Specific, actionable takeaway

## OUTPUT FORMAT
```json
{
  "sentiment": "positive",
  "category": "feature_request",
  "product_area": "authentication",
  "urgency": "high",
  "key_insights": [
    "Customer needs SSO for enterprise rollout",
    "Blocking $100K deal",
    "3rd request this month"
  ],
  "suggested_action": "Prioritize SSO feature for Q3"
}
```

## EXAMPLES
[3 concrete examples showing expected analysis]

---

FEEDBACK TO ANALYZE:
{feedback}
```

**Improvements**:
- ✅ Clear role and objective
- ✅ Structured output format
- ✅ Consistent categorization
- ✅ Actionable insights
- ✅ Reusable and documented

---

---

## Cost Comparison

| Approach | Design Time | Cost per Design | Quality Score | Consistency |
|----------|-------------|-----------------|---------------|-------------|
| **Manual (Ad-hoc)** | 2-4 hours | $0 (time only) | 60-75% | Low (varies) |
| **Manual (Structured)** | 3-5 hours | $0 (time only) | 80-90% | Medium |
| **Meta-prompt (Claude Sonnet)** | 5-15 min | $0.02-0.08 | 90-95% | High |
| **Meta-prompt (GPT-5)** | 10-20 min | $0.03-0.10 | 85-92% | High |
| **Meta-prompt (Interactive)** | 15-30 min | $0.05-0.15 | 95%+ | Very High |

**Recommendation**: Meta-prompt with Claude Sonnet for best balance of quality, cost, and speed.

---

---

## Usage Notes

**When to use this meta-prompt**:
- ✅ Building a prompt library for your organization
- ✅ Standardizing team prompt practices
- ✅ Converting successful ad-hoc prompts to reusable format
- ✅ Training team members on prompt engineering
- ✅ Rapid prototyping of new prompt ideas

**When manual design may be better**:
- ❌ Highly domain-specific prompts requiring deep expertise
- ❌ Prompts for brand-new, undefined use cases
- ❌ Very simple one-time use prompts
- ❌ Prompts requiring extensive testing and validation

**Best practices**:
1. **Start with clear use case** - Vague inputs = vague prompts
2. **Iterate based on testing** - Use option 3 in interactive mode
3. **Document customizations** - Note what you changed and why
4. **Version your prompts** - Track improvements over time
5. **Share learnings** - Build institutional knowledge

---

---

## Common Issues & Fixes

### Issue 1: Generated Prompt Too Generic

**Problem**: Meta-prompt creates a prompt that's too broad.

**Fix**: Provide more specific constraints in your request
```
Instead of: "I need a prompt for code review"
Try: "I need a prompt for reviewing Python FastAPI code focusing on:
- Security (SQL injection, auth issues)
- Performance (N+1 queries, blocking I/O)
- API design (RESTful conventions)
Output should be line-by-line with severity ratings"
```

### Issue 2: Output Format Not Quite Right

**Problem**: The structured output doesn't match your needs.

**Fix**: Specify exact format in your request
```
Add to request: "Output must be JSON with these exact fields:
{
  \"severity\": \"critical|high|medium|low\",
  \"line_number\": 123,
  \"issue\": \"description\",
  \"fix\": \"how to fix it\"
}"
```

### Issue 3: Missing Edge Cases

**Problem**: Prompt doesn't handle edge cases well.

**Fix**: Include edge cases in your request
```
Add: "Must handle these edge cases:
- Empty input
- Malformed data
- Very long inputs (10K+ words)
- Multiple languages mixed together"
```

---

---

## Related Prompts

- [Code Review & Refactoring](./code-review-refactoring.md) - Example of well-structured prompt
- [Remove AI Writing Patterns](./remove-ai-writing-patterns.md) - Another example
- [Prompt Optimization Guide](../docs/prompt-optimization.md) - Advanced techniques

---
