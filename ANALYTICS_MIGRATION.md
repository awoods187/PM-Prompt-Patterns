# Analytics Category Reorganization - Migration Guide

**Date**: October 25, 2025
**Impact**: Low (directory structure change only)
**Status**: ✅ Complete

## Summary

We've reorganized the analytics-related prompt categories to follow MECE (Mutually Exclusive, Collectively Exhaustive) principles, making it clearer which prompts to use for different temporal patterns.

## What Changed

### Old Structure (Had Overlap Issues)
```
prompts/
├── data-analysis/         # Unclear: real-time or periodic?
│   └── README.md          # Placeholder only
└── metrics-reporting/     # Overlap with data-analysis
    └── README.md          # Placeholder only
```

**Problems**:
- Categories overlapped (both covered "analysis")
- Unclear which to use for different scenarios
- No clear distinction between real-time vs. periodic vs. ad-hoc

### New Structure (MECE Organized)
```
prompts/
└── analytics/             # Unified parent category
    ├── README.md          # Comprehensive navigation guide
    ├── monitoring/        # Real-time, continuous surveillance
    │   └── README.md      # Anomaly detection, alerts
    ├── reporting/         # Periodic, standardized reports
    │   └── README.md      # Business reviews, dashboards
    └── investigation/     # Ad-hoc, exploratory analysis
        └── README.md      # Root cause, deep dives
```

**Benefits**:
- Clear temporal boundaries (continuous vs. periodic vs. one-time)
- No overlap between categories
- Easy decision tree for choosing the right prompt
- Comprehensive navigation at every level

## Migration Mapping

| Old Location | New Location | Reasoning |
|-------------|--------------|-----------|
| `prompts/data-analysis/` | `prompts/analytics/` | Organized by temporal pattern |
| `prompts/metrics-reporting/` | `prompts/analytics/reporting/` | Periodic, standardized reports |
| N/A | `prompts/analytics/monitoring/` | New: Real-time monitoring |
| N/A | `prompts/analytics/investigation/` | New: Ad-hoc analysis |

## Decision Tree: Which Category to Use?

```
Need to analyze metrics?
│
├─ Is it continuous/real-time?
│  ├─ YES → analytics/monitoring/
│  │         (alerts, anomaly detection, live dashboards)
│  │
│  └─ NO → Is it recurring/scheduled?
│     ├─ YES → analytics/reporting/
│     │         (weekly reviews, KPI dashboards, cohort reports)
│     │
│     └─ NO → analytics/investigation/
│               (root cause analysis, one-off deep dives)
```

## Examples by Category

### analytics/monitoring/ - Use for:
- ✅ Real-time anomaly detection
- ✅ Automated alert generation
- ✅ Live dashboard narration
- ✅ Continuous metric surveillance
- ✅ SLA monitoring

**Example**: "Alert me when DAU drops > 15% in 4 hours"

### analytics/reporting/ - Use for:
- ✅ Weekly business reviews
- ✅ Monthly KPI dashboards
- ✅ Quarterly board reports
- ✅ Cohort retention analysis
- ✅ Standardized metric summaries

**Example**: "Generate Monday morning executive summary"

### analytics/investigation/ - Use for:
- ✅ Root cause analysis of metric changes
- ✅ Ad-hoc signal classification
- ✅ Exploratory data analysis
- ✅ One-time deep dives
- ✅ Hypothesis testing

**Example**: "Why did conversion rate drop 30% last week?"

## Impact Assessment

### Content Changes
- ❌ No existing prompts were deleted
- ❌ No prompt content was modified
- ✅ Only organizational structure changed
- ✅ Comprehensive READMEs added for navigation

### Link Changes
- Main README updated to reflect new structure
- All internal links verified and working
- Navigation aids added at every level

### Breaking Changes
**None**. Both old directories only contained placeholder READMEs that said "Coming Soon". No production prompts were affected.

## Navigation Guide

### Finding Prompts by Use Case

| I Need To... | Old Path | New Path |
|-------------|----------|----------|
| Detect anomalies | `data-analysis/` (unclear) | `analytics/monitoring/` |
| Create business review | `metrics-reporting/` | `analytics/reporting/` |
| Investigate metric drop | `data-analysis/` (unclear) | `analytics/investigation/` |
| Generate alerts | Not available | `analytics/monitoring/` |
| Build dashboard | `metrics-reporting/` | `analytics/reporting/` |
| Classify signals | `data-analysis/` | `analytics/investigation/` |

### Quick Links

- **Browse all analytics prompts**: [prompts/analytics/](./prompts/analytics/)
- **Real-time monitoring**: [prompts/analytics/monitoring/](./prompts/analytics/monitoring/)
- **Periodic reporting**: [prompts/analytics/reporting/](./prompts/analytics/reporting/)
- **Ad-hoc investigation**: [prompts/analytics/investigation/](./prompts/analytics/investigation/)

## For Contributors

### When Adding New Analytics Prompts

Use this decision tree:

```
Is your prompt for continuous/real-time use?
├─ YES → Add to analytics/monitoring/
└─ NO → Is it for recurring/standardized reports?
    ├─ YES → Add to analytics/reporting/
    └─ NO → Add to analytics/investigation/
```

### Prompt Categorization Rules

**Monitoring** prompts have:
- ⏱️ Real-time or near-real-time execution
- 🎯 Focus on detecting changes/anomalies
- 🤖 Designed for automation
- 📊 Output: alerts, flags, anomaly reports

**Reporting** prompts have:
- 📅 Periodic cadence (daily/weekly/monthly)
- 🎯 Focus on summarizing trends
- 👥 Audience: executives, stakeholders
- 📊 Output: dashboards, summaries, reviews

**Investigation** prompts have:
- 🔍 One-time, ad-hoc execution
- 🎯 Focus on understanding "why"
- 🧪 Exploratory, hypothesis-driven
- 📊 Output: findings, root causes, insights

### Documentation Requirements

All analytics prompts must include:
1. Clear temporal pattern (monitoring/reporting/investigation)
2. Use case description
3. Example scenarios
4. Model selection guidance
5. Cost and performance metrics

See [CONTRIBUTING.md](./CONTRIBUTING.md) for full guidelines.

## FAQ

### Q: Where did my favorite prompt go?
**A**: Both `data-analysis/` and `metrics-reporting/` only contained placeholder READMEs. No actual prompts existed in those directories. The new `analytics/` structure has comprehensive READMEs with examples and guidance for creating prompts.

### Q: Why reorganize if there were no existing prompts?
**A**: This reorganization establishes the correct structure *before* adding production prompts, ensuring future prompts go in the right category from the start. It also provides clear navigation for contributors.

### Q: Can I still use the old directory names?
**A**: The old directories have been removed. All analytics prompts should now go in the appropriate `analytics/` subdirectory based on temporal pattern.

### Q: How do I know which category to use?
**A**: See the [decision tree](#decision-tree-which-category-to-use) above, or read the comprehensive guide at [prompts/analytics/README.md](./prompts/analytics/).

### Q: What if my prompt fits multiple categories?
**A**: If a prompt genuinely fits multiple patterns, it's likely too broad. Break it into focused prompts for each temporal pattern. For example:
- "Monitor dashboard" → Split into monitoring (real-time alerts) + reporting (weekly summary)

## Version History

- **v1.0** (Oct 25, 2025): Initial reorganization
  - Created analytics/ parent directory
  - Added monitoring/, reporting/, investigation/ subdirectories
  - Removed empty data-analysis/ and metrics-reporting/ placeholders
  - Created comprehensive navigation READMEs

## Support

Questions about the reorganization?
1. Check the [analytics README](./prompts/analytics/) for navigation
2. Review the [decision tree](#decision-tree-which-category-to-use)
3. Open an issue if you need clarification

---

**Status**: ✅ Migration complete, all links verified, no breaking changes.
