---
name: how-to
description: Turn documentation pages, product specs, transcripts, code, screenshots, or rough notes into a Diátaxis-compliant how-to guide delivered as a .md file. Use this skill whenever the user asks for a how-to guide, a walkthrough, a "how do I use X" doc, a runbook, a playbook, a set of instructions, or asks to convert or rewrite existing docs into task-focused guidance, even if they never say "Diátaxis" or "documentation." Also use it when the user drops a doc URL, a help-center page, or a feature spec and asks to make it usable, actionable, or clearer.
---

# How-to guide writer

Produce goal-oriented how-to guides that follow the Diátaxis framework (https://diataxis.fr), written from whatever raw material the user supplies, and delivered as `.md` files.

A how-to guide serves a competent user who already knows what they want to achieve and needs directions to get it done. It is not a lesson, not a feature tour, and not a reference dump. Recipes are the model: define the result, list what's needed, give the sequence, stay out of the way.

## Workflow

### 1. Ingest the source material

Read everything before writing anything.

- URLs: fetch them. Follow obvious child pages when the guide spans several (API auth page plus endpoint page, for example).
- Uploaded files: read them from wherever your environment puts uploads (for example `/mnt/user-data/uploads` on Claude.ai) if the content is not already in context.
- Screenshots and recordings: describe UI labels and paths exactly as they appear, since users will search for those strings.
- Pasted text, transcripts, Slack threads, code: mine them for the actual sequence someone follows, including the undocumented steps people mention in passing. Those are usually the most valuable part of the guide.

If a source contradicts itself or is clearly stale (deprecated endpoints, old UI labels), note the conflict in your response to the user rather than silently picking one.

### 2. Name the user's goal, not the tool's features

This is the step that decides whether the guide is any good. Source docs are usually organized around what the machinery does. A how-to guide is organized around what a person is trying to accomplish.

Ask yourself: what human project brings someone to this page? Write the goal as a sentence starting with a verb. "Send a receipt email when a payment succeeds," not "Use the Webhooks API."

Watch for scope errors in both directions:
- Too broad: "How to build a web app" is a field of skill, not a task. Split it.
- Too narrow or tool-shaped: "How to use the export button" is machinery. Ask what the export is for and title the guide after that.

One source page often contains several distinct goals. Say so and produce several files, or ask which goal matters, rather than mashing them into one guide.

If the goal, the audience's starting competence, or the environment (version, plan tier, self-hosted vs cloud) is genuinely ambiguous and you cannot infer it from the sources, ask once, briefly, then proceed. Do not interrogate.

### 3. Sort the material into keep, link, and cut

Run every paragraph of source material past this test:

| Source content | Belongs in a how-to? |
|---|---|
| An action the user takes | Keep |
| A judgment call the user must make ("if your traffic is bursty, choose...") | Keep. Thinking is action |
| Why the system works this way | Cut. Link to the explanation |
| Full parameter tables, every option, all error codes | Cut. Link to the reference |
| Teaching, learning objectives, "now you have learned" | Cut. That's a tutorial |
| "Click the button labeled Save to save" | Cut. Insulting to a competent user |

Cutting is the job. Bloated how-to guides are the most common failure mode, and the second most common is padding steps with things any competent practitioner already knows.

Preserve the cut material as links where the source provides URLs. When there is no URL to link to, tell the user what was removed and where it should live, so they can file it under reference or explanation later.

### 4. Sequence for flow

Order steps by how the work actually happens, not by how the source doc was laid out.

- Group everything that happens in one tool or one screen before switching context.
- Front-load anything that must be requested, provisioned, or approved and then waited on.
- Do not make the reader hold a value in their head across several steps if you can have them capture it at the moment of use.
- Real work forks. Use conditional branches ("If you're on self-hosted, do this instead") rather than pretending the path is linear.

The target quality is anticipation: the reader reaches for the next thing and it's already there.

### 5. Write it

Use `assets/template.md` as the starting structure. Adapt it. Not every guide needs every section, and a guide with empty ceremonial headings is worse than a short one.

Language rules, drawn from Diátaxis:
- Title is always "How to <verb phrase>". Not a gerund ("Configuring backups"), not a noun phrase ("Backup configuration"). Both leave the reader guessing whether the page covers how, whether, or what.
- Open with one or two sentences naming the problem and the end state.
- Second person, imperative mood: "Run the migration," not "The user should run the migration" or "We will now run."
- Conditional imperatives for choices: "To keep existing rows, pass `--merge`."
- Steps are actions with a visible result. If a step has no observable outcome, it's probably explanation in disguise.
- Concrete values in commands and code, with placeholders in an obvious convention (`YOUR_API_KEY`, `<project-id>`), never vague ones.
- Present tense, no marketing adjectives, no "simply," "just," or "easily." They make a stuck reader feel stupid.
- Include real failure modes people hit, not invented ones.

Match the house conventions of the target docs when the sources reveal them: YAML front matter for MkDocs or Docusaurus, admonition syntax, heading depth, product naming, US vs UK spelling.

### 6. Deliver

- Write to `how-to-<slug>.md` in your environment's outputs directory (for example `/mnt/user-data/outputs/` on Claude.ai), slug derived from the goal (`how-to-rotate-api-keys.md`).
- Multiple guides get multiple files. Add an `index.md` only if there are four or more.
- Share the file paths (on Claude.ai, call `present_files`), then keep the chat summary to a few lines: what you produced, what you deliberately cut, and any open questions or contradictions from the sources.
- Do not paste the full guide back into chat. It's in the file.

## Self-check before delivering

Run through this. Fix anything that fails.

1. Does the title name a real goal a person would have, in "How to..." form?
2. Could a competent user follow this without reading anything else first, and without knowing why the system is designed this way?
3. Is there any paragraph that teaches, explains, or catalogs? Cut or link it.
4. Does every step start with a verb the reader performs?
5. Are prerequisites stated up front rather than sprung mid-sequence?
6. Can the reader tell they succeeded?
7. Would this survive a plausible real-world variation, or does it only work for one exact narrow case?
8. Is anything invented? Every command, flag, path, and UI label must trace to a source. Flag gaps as `<!-- TODO: confirm -->` instead of guessing.

## Reference files

- `assets/template.md`: the output skeleton to start from.
- `references/diataxis-notes.md`: the four Diátaxis modes, the boundary cases people get wrong, and worked before/after examples of source prose rewritten as how-to steps. Read it when the material resists classification, or when the user pushes back on what you cut.
