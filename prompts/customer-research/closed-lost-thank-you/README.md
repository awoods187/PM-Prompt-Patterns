# Closed-Lost Thank-You Email (Claude Code Skill)

## 🎯 Purpose

**Turn rough notes from a lost deal into a short, warm thank-you email from the head of product to the buyer who gave feedback.**

Extracts only the product feedback, asks once for the real status of each item, and drafts a 120 to 180 word email that names what the buyer said in their own words, says honestly where each item stands, links your public product updates page, and leaves the door open without pitching.

**Business Value**:
- Lost buyers who gave feedback come away feeling heard, which keeps win-back possible
- No overpromising: every roadmap claim is confirmed by the person who owns the roadmap
- Minutes instead of a blank-page email after a disappointing call

**Use Cases**:
- Competitive losses, no-decisions, and churn calls where the buyer explained what fell short
- Closing the loop after a prospect's detailed product feedback

**Complexity**: 🟢 Beginner

## 📦 Format

This is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills), not a provider-variant prompt. Everything is in [`SKILL.md`](./SKILL.md), including a worked example.

## 🔧 Requirements

- `/anti-ai` for the final pass. This is the [Remove AI Writing Patterns](../../stakeholder-communication/remove-ai-writing-patterns/) prompt installed as a skill.

## 🚀 Setup

1. Copy this folder to `~/.claude/skills/closed-lost-thank-you/` (or your project's `.claude/skills/`).
2. Replace `[PRODUCT_UPDATES_URL]` in `SKILL.md` with your changelog or product updates page.

## 💡 Design Notes

- **Ask about status, never guess it.** A roadmap claim from the head of product reads as a commitment.
- **Never pitch, never relitigate.** No re-demo offers, no referral asks, no mention of the competitor.
- Pairs with [Call Notes](../call-notes/), which handles the internal write-up of the same call.
