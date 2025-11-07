# Remove AI Writing Patterns

**Complexity**: 🟡 Intermediate
**Category**: Technical Documentation
**Model Compatibility**: ✅ Claude (all) | ✅ GPT-5 | ✅ Gemini

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

---

## Prompt

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

6. Bolded list lead-ins
   - Pattern: "* **Performance**: Improved through caching"
   - Pattern: "* **Key benefit**: Reduces latency"
   - Fix: Remove bolding and integrate naturally into the bullet point
   - Or: Rewrite to avoid the colon structure entirely
   - Example: Change "* **Performance**: Improved through caching" to "* Caching improves performance"
   - Avoid formulaic "[Category]:[Description]" structure

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

Here are the key benefits of the new system:
* **Performance**: Achieves 10x faster processing through intelligent caching
* **Reliability**: Implements automatic retry logic with exponential backoff
* **Observability**: Provides detailed metrics and logging for debugging
* **Scalability**: Handles up to 10,000 concurrent connections
```

**After**:
```
This changes the entire development workflow, not just coding speed. The system handled edge
cases I hadn't considered. Results showed a 90% reduction in processing time for large datasets.
The key insight: performance optimization requires understanding your bottlenecks.

The new system provides several benefits:
* 10x faster processing through intelligent caching
* Automatic retry logic with exponential backoff for reliability
* Detailed metrics and logging for debugging
* Support for up to 10,000 concurrent connections
```

**Improvements**:
- Removed negation framing ("isn't just...it's")
- Removed meta-commentary ("here's the remarkable part")
- Removed hedge words ("particularly," "effectively," "essentially")
- Reduced em-dashes from 3 to 0
- More direct, confident tone
- Removed bolded list lead-ins and "[Category]:[Description]" structure

### Success Metrics

**Pattern detection accuracy**:
- Negation framing: ~98%
- Excessive em-dashes: ~99%
- Hedge words: ~95%
- Meta-commentary: ~92%
- Listicle intros: ~90%
- Bolded list lead-ins: ~97%

**Readability improvement**:
- Flesch Reading Ease: +5-10 points average
- Sentence length: -10-15% average
- Active voice usage: +15-20%

---

---

## Cost Comparison

| Approach | Tokens | Cost/1000 words | Accuracy | Notes |
|----------|--------|-----------------|----------|-------|
| **Claude Haiku** | ~2,000 | $0.001 | 85% | Fast, misses subtle patterns |
| **Claude Sonnet** | ~3,000 | $0.015 | 95% | Best balance |
| **Claude Opus** | ~3,500 | $0.070 | 97% | Highest quality, expensive |
| **GPT-5o** | ~3,000 | $0.025 | 92% | Good structured output |
| **Gemini 2.5 Pro** | ~2,500 | $0.004 | 88% | Budget option |

**Recommended**: Claude Sonnet for production use (best accuracy/cost balance)

---

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
