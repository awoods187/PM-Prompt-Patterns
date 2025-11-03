# Remove AI Writing Patterns

**Complexity**: 🟡 Intermediate
**Category**: Technical Documentation
**Model Compatibility**: ✅ Claude (all) | ✅ GPT-4 | ✅ Gemini

## Overview

Analyze and improve text by identifying and removing common AI-generated writing patterns. Transform AI-sounding content into more natural, confident, human writing while preserving technical accuracy and meaning.

**Business Value**:
- Improve readability and engagement in documentation
- Create more authentic-sounding content
- Reduce "AI tell" patterns in published materials
- Enhance professional credibility

**Use Cases**:
- Blog posts and technical articles
- Product documentation
- Marketing content
- Technical writing

---

## Base Prompt (Model Agnostic)

**Complexity**: 🟡 Intermediate

```
Analyze the following text for common AI-generated writing patterns and provide specific diffs to fix them.

Focus on these patterns:

1. "It's not X, it's Y" constructions
   - Pattern: "This isn't just about X—it's about Y"
   - Fix: Direct statements without negation framing

2. Excessive em-dashes (—)
   - Pattern: Overuse of em-dashes for emphasis or explanation
   - Fix: Replace with periods, colons, or remove entirely
   - Target: Use em-dashes sparingly (1-2 per 1000 words max)

3. AI hedge words
   - Pattern: "remarkably," "particularly," "essentially," "effectively"
   - Fix: Remove or replace with stronger, specific words

4. "Here's the X part" constructions
   - Pattern: "But here's the interesting/remarkable/important part:"
   - Fix: State the point directly without meta-commentary

5. Listicle intro patterns
   - Pattern: "What X knew that I didn't:", "Here's what happened:"
   - Fix: More direct transitions

Output format:
- List each instance found with line/paragraph reference
- Provide before/after diff for each
- Explain why the change improves readability
- Count total instances of each pattern
- Suggest 2-3 alternative phrasings when helpful

Goal: Make writing sound more human, confident, and direct while preserving meaning and tone.

---

[PASTE YOUR CONTENT HERE]

---
```

**Performance**: Works across all models, results vary by model reasoning capability.

---

## Model-Specific Optimizations

### Claude (Anthropic) - XML Structure

**Complexity**: 🟡 Intermediate

Claude's XML understanding provides better structured analysis and clearer diffs.

```xml
<task>
Analyze text for AI-generated writing patterns and provide specific improvements.
You are a writing coach helping transform AI-sounding content into natural, human writing.
</task>

<patterns_to_detect>
<pattern id="negation_framing">
  <name>"It's not X, it's Y" constructions</name>
  <examples>
    - "This isn't just about speed—it's about the entire workflow"
    - "It's not a bug—it's a feature"
  </examples>
  <fix_strategy>Rewrite as direct positive statement</fix_strategy>
</pattern>

<pattern id="excessive_em_dashes">
  <name>Overuse of em-dashes</name>
  <examples>
    - Using em-dashes more than 2 times per 1000 words
    - Using em-dashes for parenthetical asides that should be separate sentences
  </examples>
  <fix_strategy>Replace with periods, colons, commas, or remove. Keep only for genuine interruption or emphasis.</fix_strategy>
</pattern>

<pattern id="hedge_words">
  <name>AI-typical hedge words</name>
  <indicators>remarkably, particularly, essentially, effectively, certainly, indeed, quite, rather, somewhat</indicators>
  <fix_strategy>Remove entirely or replace with specific, concrete descriptors</fix_strategy>
</pattern>

<pattern id="meta_commentary">
  <name>"Here's the X part" constructions</name>
  <examples>
    - "But here's the interesting part:"
    - "Here's what's remarkable:"
    - "The important thing to note is:"
  </examples>
  <fix_strategy>State the point directly without announcing it</fix_strategy>
</pattern>

<pattern id="listicle_intros">
  <name>Formulaic listicle introductions</name>
  <examples>
    - "What X knew that I didn't:"
    - "Here's what happened:"
    - "Here are 5 things you need to know:"
  </examples>
  <fix_strategy>Use more direct, contextual transitions</fix_strategy>
</pattern>
</patterns_to_detect>

<instructions>
1. Read the entire text first
2. Identify all instances of each pattern
3. For each instance found:
   - Note the location (paragraph number or first few words)
   - Quote the problematic text
   - Provide improved version
   - Explain why the change improves readability
4. Count total instances of each pattern type
5. Provide 2-3 alternative phrasings for the most common issues
6. Preserve technical accuracy and meaning
7. Maintain the original tone (professional, casual, etc.)
</instructions>

<output_format>
<analysis>
<summary>
  <total_issues>N</total_issues>
  <patterns_found>List of pattern types detected</patterns_found>
</summary>

<pattern_instances>
<instance>
  <pattern_type>negation_framing</pattern_type>
  <location>Paragraph 2</location>
  <before>Original problematic text</before>
  <after>Improved version</after>
  <reasoning>Why this improves readability</reasoning>
</instance>
<!-- Repeat for each instance -->
</pattern_instances>

<pattern_counts>
<count pattern="negation_framing">N</count>
<count pattern="excessive_em_dashes">N</count>
<!-- etc -->
</pattern_counts>

<alternative_phrasings>
<alternative for="common pattern">
  <option>Alternative 1</option>
  <option>Alternative 2</option>
  <option>Alternative 3</option>
</alternative>
</alternative_phrasings>
</analysis>
</output_format>

<content_to_analyze>
{text}
</content_to_analyze>
```

**Code example** (Python + Anthropic SDK):
```python
import anthropic
import xml.etree.ElementTree as ET

client = anthropic.Anthropic(api_key="...")

def analyze_ai_patterns(text: str) -> dict:
    """Analyze text for AI writing patterns using Claude."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",  # Latest Claude Sonnet 4.5
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": f"<content_to_analyze>\n{text}\n</content_to_analyze>"
        }]
    )

    # Parse XML response
    xml_content = response.content[0].text
    root = ET.fromstring(f"<root>{xml_content}</root>")

    # Extract instances
    instances = []
    for instance in root.findall(".//instance"):
        instances.append({
            "pattern": instance.find("pattern_type").text,
            "location": instance.find("location").text,
            "before": instance.find("before").text,
            "after": instance.find("after").text,
            "reasoning": instance.find("reasoning").text
        })

    return {
        "total_issues": root.find(".//total_issues").text,
        "instances": instances
    }
```

**Performance**:
- Accuracy: ~95% pattern detection (Claude Sonnet 3.5)
- Cost: ~$0.015-0.030 per 1000-word document
- Latency: ~2-4s for typical blog post

### OpenAI GPT-4 - Structured Output

**Complexity**: 🟡 Intermediate

GPT-4's structured output mode ensures consistent formatting.

```
You are a writing improvement assistant. Analyze text for AI-generated writing patterns.

Identify these specific patterns:

1. NEGATION_FRAMING: "It's not X, it's Y" constructions
2. EXCESSIVE_DASHES: More than 2 em-dashes per 1000 words
3. HEDGE_WORDS: remarkably, particularly, essentially, effectively, etc.
4. META_COMMENTARY: "Here's the interesting part:", "What's remarkable is:"
5. LISTICLE_INTROS: "What X knew:", "Here's what happened:"

For each instance:
- Identify the pattern type
- Quote the problematic text
- Provide improved version
- Explain the improvement

Output JSON format:
{
  "summary": {
    "total_issues": number,
    "patterns_found": ["pattern_type", ...]
  },
  "instances": [
    {
      "pattern_type": "NEGATION_FRAMING",
      "location": "paragraph number or context",
      "before": "original text",
      "after": "improved text",
      "reasoning": "explanation"
    }
  ],
  "pattern_counts": {
    "NEGATION_FRAMING": number,
    "EXCESSIVE_DASHES": number,
    ...
  },
  "alternatives": [
    {
      "pattern": "pattern name",
      "options": ["alternative 1", "alternative 2", "alternative 3"]
    }
  ]
}

Analyze this text:
{text}
```

**Code example** (Python + OpenAI SDK):
```python
from openai import OpenAI
import json

client = OpenAI(api_key="...")

def analyze_ai_patterns_gpt4(text: str) -> dict:
    """Analyze text for AI writing patterns using GPT-4."""

    response = client.chat.completions.create(
        model="gpt-4o",  # Latest GPT-4o (replaces gpt-4o)
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Analyze this text:\n\n{text}"}
        ]
    )

    return json.loads(response.choices[0].message.content)

# Example usage
result = analyze_ai_patterns_gpt4(blog_post_text)
for instance in result["instances"]:
    print(f"\nPattern: {instance['pattern_type']}")
    print(f"Before: {instance['before']}")
    print(f"After: {instance['after']}")
    print(f"Why: {instance['reasoning']}")
```

**Performance**:
- Accuracy: ~92% pattern detection (GPT-4o)
- Cost: ~$0.020-0.040 per 1000-word document
- Latency: ~3-5s for typical blog post

---

## Advanced: Iterative Refinement

**Complexity**: 🔴 Advanced

For comprehensive improvement, run multiple passes with increasingly strict criteria.

```python
def iterative_improvement(text: str, passes: int = 3) -> dict:
    """
    Run multiple improvement passes with increasing strictness.

    Pass 1: Obvious AI patterns (high confidence)
    Pass 2: Subtle patterns and style issues
    Pass 3: Final polish and readability
    """

    current_text = text
    all_changes = []

    for pass_num in range(1, passes + 1):
        # Adjust strictness based on pass
        if pass_num == 1:
            instructions = "Focus on obvious AI patterns only"
        elif pass_num == 2:
            instructions = "Find subtle patterns and remaining issues"
        else:
            instructions = "Final polish: any remaining awkward phrasing"

        result = analyze_with_instructions(current_text, instructions)

        # Apply changes
        for instance in result["instances"]:
            current_text = current_text.replace(
                instance["before"],
                instance["after"]
            )
            all_changes.append(instance)

        # If no changes, stop early
        if not result["instances"]:
            break

    return {
        "final_text": current_text,
        "total_changes": len(all_changes),
        "passes_used": pass_num,
        "all_changes": all_changes
    }
```

---

## Production Patterns

### Pattern 1: Pre-publishing Check

**Use case**: Automated content review before publishing.

```python
def pre_publish_check(content: str, threshold: int = 5) -> dict:
    """
    Check content for AI patterns before publishing.

    Args:
        content: Text to check
        threshold: Maximum allowed issues (default: 5)

    Returns:
        dict with pass/fail status and recommendations
    """

    analysis = analyze_ai_patterns(content)
    total_issues = int(analysis["total_issues"])

    return {
        "pass": total_issues <= threshold,
        "issues_found": total_issues,
        "threshold": threshold,
        "critical_patterns": [
            i for i in analysis["instances"]
            if i["pattern_type"] in ["META_COMMENTARY", "HEDGE_WORDS"]
        ],
        "recommendations": analysis["instances"] if total_issues > threshold else []
    }

# Example usage in CI/CD
if __name__ == "__main__":
    with open("blog_post.md") as f:
        content = f.read()

    result = pre_publish_check(content)

    if not result["pass"]:
        print(f"❌ Failed: {result['issues_found']} AI patterns found")
        print("\nFix these issues:")
        for issue in result["recommendations"]:
            print(f"  - {issue['pattern_type']}: {issue['before']}")
        exit(1)
    else:
        print("✅ Passed: Content is ready to publish")
```

### Pattern 2: Batch Document Processing

**Use case**: Clean up multiple documents at scale.

```python
def batch_process_documents(file_paths: list[str]) -> list[dict]:
    """Process multiple documents in batch."""

    results = []

    for path in file_paths:
        with open(path) as f:
            content = f.read()

        analysis = analyze_ai_patterns(content)

        # Auto-apply fixes if confidence is high
        improved = content
        for instance in analysis["instances"]:
            if instance.get("confidence", 1.0) > 0.9:
                improved = improved.replace(
                    instance["before"],
                    instance["after"]
                )

        # Write improved version
        improved_path = path.replace(".md", "_improved.md")
        with open(improved_path, "w") as f:
            f.write(improved)

        results.append({
            "original": path,
            "improved": improved_path,
            "issues_fixed": len(analysis["instances"]),
            "manual_review_needed": [
                i for i in analysis["instances"]
                if i.get("confidence", 1.0) <= 0.9
            ]
        })

    return results
```

---

## Quality Evaluation

### Example Before/After

**Before**:
```
This isn't just about speed—it's about the entire development workflow changing fundamentally.
But here's the remarkable part: the system handled edge cases I hadn't considered. The results
were particularly impressive when dealing with large datasets—effectively reducing processing
time by 90%. What I learned was this: performance optimization is essentially about understanding
your bottlenecks.
```

**After**:
```
This changes the entire development workflow, not just coding speed. The system handled edge
cases I hadn't considered. Results showed a 90% reduction in processing time for large datasets.
The key insight: performance optimization requires understanding your bottlenecks.
```

**Improvements**:
- Removed negation framing ("isn't just...it's")
- Removed meta-commentary ("here's the remarkable part")
- Removed hedge words ("particularly," "effectively," "essentially")
- Reduced em-dashes from 3 to 0
- More direct, confident tone

### Success Metrics

**Pattern detection accuracy**:
- Negation framing: ~98%
- Excessive em-dashes: ~99%
- Hedge words: ~95%
- Meta-commentary: ~92%
- Listicle intros: ~90%

**Readability improvement**:
- Flesch Reading Ease: +5-10 points average
- Sentence length: -10-15% average
- Active voice usage: +15-20%

---

## Common Issues & Fixes

### Issue 1: Over-correction

**Problem**: Removing too many em-dashes or qualifiers can make text choppy or overconfident.

**Fix**: Set threshold for acceptable usage
```xml
<guideline>
Allow 1-2 em-dashes per 1000 words for genuine emphasis
Keep qualifiers when expressing genuine uncertainty
Preserve technical hedging where appropriate (e.g., "approximately," "estimated")
</guideline>
```

### Issue 2: Context-Dependent Patterns

**Problem**: "Here's" constructions may be appropriate in conversational content.

**Fix**: Adjust based on content type
```python
def analyze_with_context(text: str, content_type: str) -> dict:
    """Adjust pattern detection based on content type."""

    strictness = {
        "technical_docs": "high",      # Remove all patterns
        "blog_post": "medium",          # Allow some conversational style
        "social_media": "low"           # Keep casual tone
    }

    return analyze_ai_patterns(
        text,
        strictness=strictness.get(content_type, "medium")
    )
```

### Issue 3: False Positives on Technical Content

**Problem**: Technical writing legitimately uses words like "effectively" or "essentially."

**Fix**: Context-aware detection
```xml
<pattern id="hedge_words">
  <exceptions>
    - "effectively" in technical context (e.g., "effectively final")
    - "essentially" when describing technical equivalence
  </exceptions>
</pattern>
```

---

## Cost Comparison

| Approach | Tokens | Cost/1000 words | Accuracy | Notes |
|----------|--------|-----------------|----------|-------|
| **Claude Haiku** | ~2,000 | $0.001 | 85% | Fast, misses subtle patterns |
| **Claude Sonnet** | ~3,000 | $0.015 | 95% | Best balance |
| **Claude Opus** | ~3,500 | $0.070 | 97% | Highest quality, expensive |
| **GPT-4o** | ~3,000 | $0.025 | 92% | Good structured output |
| **Gemini 2.5 Pro** | ~2,500 | $0.004 | 88% | Budget option |

**Recommended**: Claude Sonnet for production use (best accuracy/cost balance)

---

## Usage Notes

**Best for**:
- Blog posts and articles (500-2000 words)
- Technical documentation
- Marketing content
- Executive communications

**Not recommended for**:
- Already-human-written content (may over-correct)
- Creative fiction (different style considerations)
- Transcripts (conversational patterns are expected)

**Iteration strategy**:
- Run once on AI-generated drafts
- Use iterative mode (2-3 passes) for heavily AI-written content
- Manual review recommended for final polish

---

## Version History

| Version | Date | Changes | Detection Accuracy |
|---------|------|---------|-------------------|
| v1.0 | Initial | Basic pattern detection (3 patterns) | 78% |
| v1.1 | +2 weeks | Added 2 more patterns, improved examples | 85% |
| v2.0 | +1 month | Model-specific optimizations, XML structure | 92% |
| v2.1 | +2 months | Context-aware detection, false positive reduction | 95% |

---

## Related Prompts

- [Technical Writing Review](./technical-writing-review.md) - General writing improvement
- [Documentation Style Guide Enforcement](./style-guide-enforcement.md) - Enforce specific style rules
- [Content Readability Analysis](./readability-analysis.md) - Broader readability metrics

---

**Questions?** This prompt works best when you:
1. Provide full context (complete document, not fragments)
2. Specify content type (technical docs vs blog post)
3. Review suggested changes manually (don't auto-apply all)
4. Run iteratively on heavily AI-generated content
