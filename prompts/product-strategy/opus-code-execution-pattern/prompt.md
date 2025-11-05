# Opus Design → Claude Code Execution Pattern

**Production-grade workflow for leveraging Opus's architectural capabilities with Claude Code's autonomous execution**

---

## Overview

This pattern uses **Claude Opus for system design** and **Claude Code for implementation**, creating a powerful architect-builder workflow that combines strategic thinking with tactical execution.

### When to Use This Pattern

✅ **Ideal for:**
- Complex systems requiring both high-level design and detailed implementation
- Projects where architecture mistakes are expensive (>$10K impact)
- Multi-file codebases or system refactoring
- When you need both "why" (architecture) and "how" (implementation)
- Greenfield projects with unclear technical approach
- Legacy system modernization

❌ **Not ideal for:**
- Simple CRUD operations or single-file scripts
- Well-understood problems with established patterns
- Rapid prototyping where architecture can evolve
- Time-critical hotfixes (use Claude Code directly)

### Cost Profile

| Phase | Model | Typical Cost | Duration |
|-------|-------|--------------|----------|
| Design | Opus 4.1 | $0.05-0.15 | 2-5 min |
| Execution | Claude Code/Sonnet 4.5 | $0.01-0.03 per file | 10-30 min |
| Validation | Opus 4.1 (optional) | $0.02-0.05 | 1-2 min |
| **Total** | | **$0.06-0.21** | **15-40 min** |

**ROI Comparison** (vs alternatives):
- Pure Opus implementation: 10-20x cost reduction, equal quality
- Direct Claude Code: 3-5x quality improvement, 1.2x cost
- Human developer: 99.98% cost reduction, comparable quality for well-scoped tasks

---

---

## Prompt

```

```
