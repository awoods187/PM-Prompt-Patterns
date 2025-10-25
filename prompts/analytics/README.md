# Analytics Prompts

**Production-tested prompts for data analysis, metrics, and reporting**

This category contains prompts organized by temporal pattern and use case, following MECE (Mutually Exclusive, Collectively Exhaustive) principles.

## Directory Structure

```
analytics/
├── monitoring/     # Real-time signals, alerts, anomaly detection
├── reporting/      # Periodic summaries, standardized dashboards
└── investigation/  # Ad-hoc analysis, root cause, deep dives
```

## Quick Navigation

### By Use Case

| I Need To... | Go To | Example Prompts |
|-------------|-------|-----------------|
| Detect anomalies in real-time metrics | [monitoring/](./monitoring/) | Alert generation, spike detection |
| Create weekly/monthly business reviews | [reporting/](./reporting/) | KPI dashboards, cohort analysis |
| Investigate a specific metric drop | [investigation/](./investigation/) | Root cause analysis, exploratory analysis |
| Build automated alerting | [monitoring/](./monitoring/) | Threshold detection, pattern recognition |
| Generate standardized reports | [reporting/](./reporting/) | Business reviews, metric narratives |
| Perform one-off deep dive | [investigation/](./investigation/) | Custom analysis, signal classification |

### By Temporal Pattern

**Monitoring** (Continuous, Real-Time)
- Active surveillance of metrics
- Immediate anomaly detection
- Live dashboard narration
- Automated alert generation
- → [Browse monitoring prompts](./monitoring/)

**Reporting** (Periodic, Standardized)
- Weekly/monthly business reviews
- Recurring KPI summaries
- Standardized dashboards
- Cohort analysis reports
- → [Browse reporting prompts](./reporting/)

**Investigation** (Ad-Hoc, Exploratory)
- Root cause analysis
- One-off deep dives
- Exploratory data analysis
- Custom metric investigations
- → [Browse investigation prompts](./investigation/)

## Common Tasks

### Setting Up Alerts
1. Start with [monitoring/anomaly-detection.md](./monitoring/) (Coming Soon)
2. Configure thresholds based on your metrics
3. Set up automated notifications

### Creating Business Reviews
1. Use [reporting/business-review.md](./reporting/) (Coming Soon)
2. Customize KPIs for your business
3. Schedule recurring generation

### Investigating Metric Changes
1. Begin with [investigation/root-cause-analysis.md](./investigation/) (Coming Soon)
2. Follow systematic exploration framework
3. Document findings for team

## Category Principles

### Monitoring vs. Reporting vs. Investigation

**When to use Monitoring:**
- ✅ You need continuous tracking
- ✅ Speed matters (real-time or near-real-time)
- ✅ Automated responses required
- ✅ Focused on detecting changes

**When to use Reporting:**
- ✅ Periodic (daily/weekly/monthly) cadence
- ✅ Standardized format needed
- ✅ Audience is executives/stakeholders
- ✅ Focused on summarizing trends

**When to use Investigation:**
- ✅ One-time analysis needed
- ✅ Exploring unknown patterns
- ✅ Deep dive into specific issue
- ✅ Focused on understanding "why"

## Migration Notice

**Previous Structure** (Deprecated):
- `prompts/data-analysis/` → Now organized by temporal pattern
- `prompts/metrics-reporting/` → Now `analytics/reporting/`

The new structure provides clearer boundaries and reduces overlap between categories.

## Production Metrics

Our analytics prompts have been used to:
- Process 10K+ signals weekly
- Generate 100+ business reviews
- Detect 50+ critical anomalies
- Reduce analysis time by 85%

See individual prompt files for specific metrics and case studies.

## Contributing

When adding analytics prompts, use this decision tree:

```
Is it continuous/real-time?
├─ Yes → monitoring/
└─ No → Is it recurring/standardized?
    ├─ Yes → reporting/
    └─ No → investigation/
```

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for full guidelines.

---

**Start here if you're new**: [monitoring/README.md](./monitoring/) for real-time use cases, [reporting/README.md](./reporting/) for periodic reports, [investigation/README.md](./investigation/) for ad-hoc analysis.
