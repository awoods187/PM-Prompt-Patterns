# Diátaxis notes for how-to writing

Condensed from https://diataxis.fr. Read the source pages when a case is genuinely contested.

## Contents

1. The four modes
2. Boundary cases people get wrong
3. Before and after examples
4. What to do with the material you cut
5. Handling pushback

## 1. The four modes

Diátaxis splits documentation by user need along two axes: whether the reader is acquiring or applying knowledge, and whether they need action or cognition.

| Mode | Reader's situation | Serves |
|---|---|---|
| Tutorial | Learning, needs a guided experience | Acquisition through action |
| How-to guide | Working, has a goal, needs directions | Application through action |
| Reference | Working, needs a fact | Application through cognition |
| Explanation | Studying, wants to understand | Acquisition through cognition |

Mixing modes on one page is the standard failure. A how-to guide that pauses to teach fundamentals fails the working reader; a tutorial that assumes competence fails the learner.

## 2. Boundary cases people get wrong

**How-to vs tutorial.** Both are step-by-step, which is why they get conflated. The difference is who is in charge. In a tutorial the writer chooses a safe, contrived project and guarantees the outcome, because the point is the learning. In a how-to guide the reader brings their own real situation and the writer supplies directions they must adapt. If the source says "in this lesson you will learn," it is tutorial material.

**How-to vs reference.** A how-to guide names the options that bear on the goal in front of the reader. A reference lists all options exhaustively. When you catch yourself writing a table of every flag, stop and link.

**Procedure vs guide.** Not every task reduces to a linear procedure. Real problems fork, overlap, and have several valid entry points. A how-to guide can and should ask the reader to exercise judgment. Presenting a branching problem as a single straight line produces a guide that works for exactly one reader.

**Tool-shaped vs goal-shaped.** "How to use the Reports module" is shaped by the software's menu structure. "How to reconcile a month with unmatched transactions" is shaped by someone's actual job. Tools should appear as the means, not the subject.

**Titles.** "How to configure rate limiting" is unambiguous. "Configuring rate limiting" might be about whether to. "Rate limiting" might be an explainer. Use the "How to" form.

**Scope.** A guide addressing an entire open-ended domain ("how to build a web application") is not a how-to guide, it is a course. Split it into the discrete goals underneath.

## 3. Before and after examples

**Example 1: tool-shaped source turned goal-shaped**

Source: "The Webhooks page lets you register endpoint URLs. Click New Endpoint, enter a URL, and select events from the dropdown."

Rewrite as: `How to notify your billing system when a payment succeeds`, with the endpoint registration as one step among several, alongside signature verification and retry handling, because that is the actual project.

**Example 2: explanation removed**

Source: "Idempotency keys exist because network failures can cause clients to retry requests, which in a distributed system risks duplicate side effects. The system stores the first response for 24 hours..."

Rewrite as: "Send an `Idempotency-Key` header with a unique value per logical operation. Retries with the same key return the original response for 24 hours." Then link to the explanation page for the reasoning.

**Example 3: insulting step removed**

Source: "Click Save to save your changes."

Cut it entirely, unless something non-obvious happens on save, in which case that is the actual content: "Saving triggers a reindex, which takes several minutes on large workspaces. Wait for the status to return to Ready before importing."

**Example 4: judgment preserved**

Source: "Batch size can be set between 1 and 10000."

Rewrite as a conditional imperative that helps the reader decide: "For interactive imports, set a batch size around 500 so progress stays visible. For overnight jobs, raise it to 5000 to reduce total runtime." Point to the reference for the full range.

## 4. What to do with the material you cut

Do not discard it silently. The user may be responsible for the whole docs set, and knowing what got displaced is part of the value.

Tell them, briefly, in the chat response:
- explanation material that should become or link to an explanation page,
- exhaustive option lists that belong in reference,
- learning-oriented sequences that suggest a tutorial is missing,
- contradictions or stale details found across sources.

Offer to write the companion pages. Do not write them unasked.

## 5. Handling pushback

If a user objects that the guide is too thin, the usual cause is that they expected completeness. Explain the tradeoff: in a how-to guide, usability beats completeness, and a guide that starts and ends at a reasonable point while linking outward is more useful than one that reproduces the manual. Then offer the companion reference or explanation page, which is what they usually actually wanted.

If a user wants the explanation inline anyway, do it. Their docs, their call. Keep it to a short note under the relevant step rather than a preamble the reader must scroll past while working.
