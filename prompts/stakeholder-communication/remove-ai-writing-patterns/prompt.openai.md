# Remove AI Writing Patterns - OpenAI Optimized

> Extends `prompt.md` with OpenAI-specific optimizations

## System Prompt

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

7. Anaphoric triads and fragment cascades
   - Pattern: Three or more consecutive sentences (or sentence fragments) starting with the same word or phrase, used as rhythmic emphasis
   - Pattern: "It is a missed close. It is an audit finding. It is a compliance exposure."
   - Pattern: "Did the data hold up. Did the integration round-trip. Did the migration land. Did the period close."
   - Pattern: "The pitch decks will rhyme. The demos will sing."
   - Pattern: Comma-separated noun triplets like "One person, one post, one afternoon"
   - Fix: Break the parallel structure. Consolidate into a single sentence, or vary the sentence openers so the rhythm disappears
   - Example: Change "It is a missed close. It is an audit finding. It is a compliance exposure." to "A missed close becomes an audit finding and a compliance exposure."
   - This is one of the strongest AI "tells" because humans rarely sustain this cadence naturally

8. Clickbait insight openers (pattern interrupts)
   - Pattern: "Here's the thing:", "Here's what's interesting:", "Here's the kicker:"
   - Pattern: "The dirty secret of X", "What nobody is talking about", "What they don't tell you"
   - Pattern: "Something clicked for me recently:", "This changed everything for me:"
   - Pattern: "The real reason X happens", "The true cost of X", "Why X actually fails"
   - Pattern: "Picture this:", "Imagine this:", "Stop me if you've heard this one"
   - Pattern: "Plot twist:", "Spoiler:", "Turns out,"
   - Pattern: "Let's be honest.", "Let's be real.", "The hard truth is...", "The uncomfortable truth..."
   - Pattern: "Hear me out", "Bear with me", "Think about it.", "Consider this:", "Food for thought."
   - Fix: Delete the opener entirely and lead with the actual point. If the point cannot stand without the windup, the point is too weak.
   - Example: Change "Here's the thing about modern finance: it's lean." to "Modern finance is lean."

9. Fake-authority credentialing
   - Pattern: "After X years in this space...", "Having worked with hundreds of [founders/teams/customers]..."
   - Pattern: "I've talked to hundreds of founders and they all say the same thing:"
   - Pattern: "I've seen this movie before", "Trust me on this", "Take it from someone who's been there", "In the trenches"
   - Fix: Cut the credential preamble. Make the claim directly. If credibility matters, earn it with a specific anecdote or data point, not a vague appeal to experience.

10. False contrarianism
    - Pattern: "Contrary to popular belief", "Despite what you've been told", "Forget everything you know about X"
    - Pattern: "X isn't about Y. It's about Z." (the parent form of the "not X, but Y" trap in pattern #1)
    - Pattern: "And here's the part nobody wants to admit:", "What most people get wrong about X"
    - Fix: State the actual claim. Skip the framing that pretends conventional wisdom is wrong before saying anything substantive.

11. Empty intensifiers and false-modesty hedges
    - Pattern: "Genuinely", "Truly", "Literally", "Quite literally"
    - Pattern: "I might be wrong, but...", "Take this with a grain of salt", "Your mileage may vary"
    - Fix: Delete intensifiers (the sentence is stronger without them). Cut hedges unless you actually mean them.

12. Engagement-bait closers
    - Pattern: "What do you think?", "Let me know your thoughts.", "Drop a comment below."
    - Pattern: "Just my two cents.", "But that's just me."
    - Fix: End on the substantive point. The reader can comment without being prompted.

13. "X for X" tautology closers
    - Pattern: "A serious tool for serious work", "A real solution for real problems", "Built by builders for builders"
    - Fix: Replace with a specific, concrete claim. The tautology sounds profound but says nothing.

14. Anthropomorphized abstractions
    - Pattern: "A timeline that does not negotiate", "Deadlines that don't care", "Markets that punish", "Software that just works"
    - Fix: Describe the actual mechanism or constraint. "The board meets Tuesday" beats "a timeline that does not negotiate."

15. Punchy single-sentence-paragraph closers
    - Pattern: A short, declarative single-sentence paragraph used to "land" a point, deployed more than once in a piece.
    - Pattern: "That is the whole point." "Full stop." "End of story." "Period."
    - Fix: One per piece, maximum. If the writing needs more than one to feel emphatic, the prose around them is too soft.

16. Density meta-check (run this last)
    - Any single instance of the patterns above can read as human. Density is the tell.
    - Flag any piece where multiple categories (especially #1, #7, #8, #15) appear more than twice each in under 1,500 words.
    - Flag any section where three consecutive paragraphs each end on a punchy fragment or use the same rhetorical structure.
    - Fix: Vary cadence. Let some paragraphs end quietly. Let some claims arrive without setup or punctuation games.

Output format:
- List each instance found with line/paragraph reference
- Provide before/after diff for each
- Explain why the change improves readability
- Count total instances of each pattern
- For pattern #16, provide a density score and flag the worst-offending section
- Suggest 2-3 alternative phrasings when helpful

Goal: Make writing sound more human, confident, and direct while preserving meaning and tone.

---

[PASTE YOUR CONTENT HERE]

---
```

## OpenAI Optimizations Applied

- **Clear role definition**: Explicit system message with role and responsibilities
- **Structured output**: Consistent formatting instructions
- **Function calling ready**: Can be combined with function schemas for structured output
- **Concise directives**: Optimized for GPT-5's instruction-following capabilities

## Usage

```python
from pm_prompt_toolkit.providers import get_provider

# Initialize OpenAI provider
provider = get_provider("gpt-4o")

result = provider.generate(
    system_prompt="<prompt from above>",
    user_message="<your content here>"
)
```

## Model Recommendations

- **gpt-4o**: Best balance of speed, quality, and cost for most use cases
- **gpt-4o-mini**: Faster and more cost-effective for simpler tasks
- **gpt-4-turbo**: Use for extended context needs (>128k tokens)

## See Also

- Base prompt: `prompt.md` (examples, testing checklist, business value)
- Provider documentation: `../../docs/provider-specific-prompts.md`
