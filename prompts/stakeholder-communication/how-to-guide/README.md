# How-To Guide Writer (Claude Code Skill)

## 🎯 Purpose

**Turn docs pages, specs, transcripts, code, screenshots, or rough notes into a Diátaxis-compliant how-to guide, delivered as a `.md` file.**

Names the reader's goal rather than the tool's features, cuts explanation and reference material (and tells you where it should live instead), sequences steps for how the work actually happens, and self-checks before delivering.

**Business Value**:
- Feature-shaped docs become task-shaped guides people can follow
- Shorter guides, because teaching, catalogs, and rationale get linked instead of inlined
- Gaps and contradictions in the sources are flagged instead of guessed

**Use Cases**:
- "How do I use X" docs, runbooks, playbooks
- Rewriting a help-center page or feature spec into something actionable
- Turning a Slack thread or call transcript into documented steps

**Complexity**: 🟡 Intermediate

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt:

| File | Contents |
|------|----------|
| [`SKILL.md`](./SKILL.md) | The skill: ingest, name the goal, keep/link/cut, sequence, write, deliver, self-check |
| [`assets/template.md`](./assets/template.md) | Output skeleton |
| [`references/diataxis-notes.md`](./references/diataxis-notes.md) | The four Diátaxis modes, boundary cases, before/after rewrites, handling pushback |

## 🚀 Setup

Copy this folder to `~/.claude/skills/how-to/` (or your project's `.claude/skills/`). No other dependencies. Web fetch helps when sources are URLs.

## 💡 Design Notes

- **Goal, not machinery.** "Send a receipt email when a payment succeeds," not "Use the Webhooks API."
- **Cutting is the job.** Explanation and exhaustive options get linked, not inlined.
- **Nothing invented.** Unverified commands or labels get `<!-- TODO: confirm -->`.
