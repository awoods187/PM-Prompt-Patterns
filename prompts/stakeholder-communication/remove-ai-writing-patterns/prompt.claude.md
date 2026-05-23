# Remove AI Writing Patterns - Claude Optimized

> Extends `prompt.md` with Claude-specific optimizations

## Prompt

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

<pattern id="bolded_list_leadins">
  <name>Bolded list lead-ins with category labels</name>
  <examples>
    - "* **Performance**: Improved through caching"
    - "* **Key benefit**: Reduces latency"
    - "* **Reliability**: Implements automatic retry logic"
  </examples>
  <fix_strategy>Remove bolding and integrate naturally into the bullet point. Rewrite to avoid the "[Category]:[Description]" structure. Change "* **Performance**: Improved through caching" to "* Caching improves performance"</fix_strategy>
</pattern>

<pattern id="anaphoric_triads">
  <name>Anaphoric triads and fragment cascades</name>
  <description>Three or more consecutive sentences or fragments starting with the same word or phrase, used as rhythmic emphasis. One of the strongest AI tells — humans rarely sustain this cadence naturally.</description>
  <examples>
    - "It is a missed close. It is an audit finding. It is a compliance exposure."
    - "Did the data hold up. Did the integration round-trip. Did the migration land. Did the period close."
    - "The pitch decks will rhyme. The demos will sing."
    - "One person, one post, one afternoon" (comma-separated noun triplet variant)
  </examples>
  <detection_hints>
    - Flag any run of 3+ sentences in a row that share the same opening word/phrase
    - Flag comma-separated triplets where each element follows a "[article] [noun]" or "[number] [noun]" template
    - Fragment sentences (no verb, or verb repeated verbatim) in a cascade are especially strong signals
  </detection_hints>
  <fix_strategy>Break the parallel structure. Consolidate the triad into a single sentence, or vary the sentence openers so the rhythm disappears. Example: "It is a missed close. It is an audit finding. It is a compliance exposure." → "A missed close becomes an audit finding and a compliance exposure."</fix_strategy>
</pattern>

<pattern id="clickbait_openers">
  <name>Clickbait insight openers (pattern interrupts)</name>
  <description>Windup phrases that promise a revelation before delivering one. The opener does the rhetorical work the sentence itself should do.</description>
  <examples>
    - "Here's the thing:", "Here's what's interesting:", "Here's the kicker:"
    - "The dirty secret of X", "What nobody is talking about", "What they don't tell you"
    - "Something clicked for me recently:", "This changed everything for me:"
    - "The real reason X happens", "The true cost of X", "Why X actually fails"
    - "Picture this:", "Imagine this:", "Stop me if you've heard this one"
    - "Plot twist:", "Spoiler:", "Turns out,"
    - "Let's be honest.", "Let's be real.", "The hard truth is...", "The uncomfortable truth..."
    - "Hear me out", "Bear with me", "Think about it.", "Consider this:", "Food for thought."
  </examples>
  <fix_strategy>Delete the opener entirely and lead with the actual point. If the point cannot stand without the windup, the point is too weak. Example: "Here's the thing about modern finance: it's lean." → "Modern finance is lean."</fix_strategy>
</pattern>

<pattern id="fake_authority">
  <name>Fake-authority credentialing</name>
  <description>Vague appeals to experience that substitute for specific evidence.</description>
  <examples>
    - "After X years in this space...", "Having worked with hundreds of [founders/teams/customers]..."
    - "I've talked to hundreds of founders and they all say the same thing:"
    - "I've seen this movie before", "Trust me on this", "Take it from someone who's been there", "In the trenches"
  </examples>
  <fix_strategy>Cut the credential preamble. Make the claim directly. If credibility matters, earn it with a specific anecdote or data point, not a vague appeal to experience.</fix_strategy>
</pattern>

<pattern id="false_contrarianism">
  <name>False contrarianism</name>
  <description>Framing that pretends conventional wisdom is wrong before saying anything substantive. The parent form of the "not X, but Y" trap in negation_framing.</description>
  <examples>
    - "Contrary to popular belief", "Despite what you've been told", "Forget everything you know about X"
    - "X isn't about Y. It's about Z."
    - "And here's the part nobody wants to admit:", "What most people get wrong about X"
  </examples>
  <fix_strategy>State the actual claim. Skip the framing that pretends conventional wisdom is wrong before saying anything substantive.</fix_strategy>
</pattern>

<pattern id="empty_intensifiers">
  <name>Empty intensifiers and false-modesty hedges</name>
  <description>Adverbs that add no information, and hedges that signal humility without earning it.</description>
  <examples>
    - "Genuinely", "Truly", "Literally", "Quite literally"
    - "I might be wrong, but...", "Take this with a grain of salt", "Your mileage may vary"
  </examples>
  <fix_strategy>Delete intensifiers (the sentence is stronger without them). Cut hedges unless you actually mean them.</fix_strategy>
</pattern>

<pattern id="engagement_bait_closers">
  <name>Engagement-bait closers</name>
  <description>Closing lines that solicit reader response or add false modesty.</description>
  <examples>
    - "What do you think?", "Let me know your thoughts.", "Drop a comment below."
    - "Just my two cents.", "But that's just me."
  </examples>
  <fix_strategy>End on the substantive point. The reader can comment without being prompted.</fix_strategy>
</pattern>

<pattern id="tautology_closers">
  <name>"X for X" tautology closers</name>
  <description>Closers that sound profound but say nothing concrete.</description>
  <examples>
    - "A serious tool for serious work"
    - "A real solution for real problems"
    - "Built by builders for builders"
  </examples>
  <fix_strategy>Replace with a specific, concrete claim. The tautology sounds profound but says nothing.</fix_strategy>
</pattern>

<pattern id="anthropomorphized_abstractions">
  <name>Anthropomorphized abstractions</name>
  <description>Abstract nouns given human agency in place of a described mechanism.</description>
  <examples>
    - "A timeline that does not negotiate"
    - "Deadlines that don't care"
    - "Markets that punish"
    - "Software that just works"
  </examples>
  <fix_strategy>Describe the actual mechanism or constraint. "The board meets Tuesday" beats "a timeline that does not negotiate."</fix_strategy>
</pattern>

<pattern id="punchy_paragraph_closers">
  <name>Punchy single-sentence-paragraph closers</name>
  <description>A short, declarative single-sentence paragraph used to "land" a point, deployed more than once in a piece.</description>
  <examples>
    - "That is the whole point."
    - "Full stop."
    - "End of story."
    - "Period."
  </examples>
  <fix_strategy>One per piece, maximum. If the writing needs more than one to feel emphatic, the prose around them is too soft.</fix_strategy>
</pattern>

<pattern id="density_meta_check">
  <name>Density meta-check (run this last)</name>
  <description>Any single instance of the patterns above can read as human. Density is the tell.</description>
  <detection_hints>
    - Flag any piece where multiple categories (especially negation_framing, anaphoric_triads, clickbait_openers, punchy_paragraph_closers) appear more than twice each in under 1,500 words.
    - Flag any section where three consecutive paragraphs each end on a punchy fragment or use the same rhetorical structure.
  </detection_hints>
  <fix_strategy>Vary cadence. Let some paragraphs end quietly. Let some claims arrive without setup or punctuation games.</fix_strategy>
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
<count pattern="hedge_words">N</count>
<count pattern="meta_commentary">N</count>
<count pattern="listicle_intros">N</count>
<count pattern="bolded_list_leadins">N</count>
<count pattern="anaphoric_triads">N</count>
<count pattern="clickbait_openers">N</count>
<count pattern="fake_authority">N</count>
<count pattern="false_contrarianism">N</count>
<count pattern="empty_intensifiers">N</count>
<count pattern="engagement_bait_closers">N</count>
<count pattern="tautology_closers">N</count>
<count pattern="anthropomorphized_abstractions">N</count>
<count pattern="punchy_paragraph_closers">N</count>
</pattern_counts>

<density_check>
  <score>0-10 scale, where 10 = pervasive AI tells, 0 = clean</score>
  <worst_section>Quote the section with the highest concentration of patterns</worst_section>
  <flagged_categories>List categories appearing more than twice in under 1,500 words</flagged_categories>
  <consecutive_punch_paragraphs>Note any run of 3+ paragraphs ending on punchy fragments or sharing rhetorical structure</consecutive_punch_paragraphs>
</density_check>

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

## Claude Optimizations Applied

- **XML structure**: Uses XML tags for clear task delineation and better parsing
- **Structured thinking**: Encourages use of `<thinking>` tags for complex reasoning
- **Prompt caching**: Static prompt content is cacheable for 90%+ cost savings
- **Extended context**: Leverages Claude's 200K token context window

## Usage

```python
from pm_prompt_toolkit.providers import get_provider

# Initialize Claude provider with caching
provider = get_provider("claude-sonnet-4-5", enable_caching=True)

result = provider.generate(
    system_prompt="<prompt from above>",
    user_message="<your content here>"
)
```

## See Also

- Base prompt: `prompt.md` (examples, testing checklist, business value)
- Provider documentation: `../../docs/provider-specific-prompts.md`
