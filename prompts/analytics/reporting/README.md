# Reporting Prompts

**Periodic summaries, standardized dashboards, and recurring business reviews**

## Overview

Reporting prompts are designed for **periodic, standardized** analysis of metrics and trends. Use these when you need recurring reports, KPI dashboards, or scheduled business reviews.

### Key Characteristics
- 📅 **Temporal Pattern**: Periodic (daily, weekly, monthly, quarterly)
- 🎯 **Primary Goal**: Summarize trends and communicate status
- 📊 **Audience**: Executives, stakeholders, teams
- 🔄 **Cadence**: Recurring, predictable schedule

## Use Cases

### When to Use Reporting Prompts

✅ **Use reporting when you need to:**
- Generate weekly/monthly business reviews
- Create standardized KPI dashboards
- Summarize metrics for stakeholder updates
- Produce cohort analysis reports
- Build recurring performance summaries
- Track progress against goals

❌ **Don't use reporting for:**
- Real-time alerts (use [monitoring/](../monitoring/) instead)
- One-time investigations (use [investigation/](../investigation/) instead)
- Ad-hoc exploratory analysis (use [investigation/](../investigation/) instead)

## Available Prompts

### 🚧 Coming Soon

This section will include production-tested prompts for:

**Business Reviews**
- Weekly executive summaries
- Monthly board reports
- Quarterly business reviews
- Annual performance summaries

**KPI Dashboards**
- Product metrics dashboard
- Growth metrics summary
- Engagement analysis
- Retention cohort reports

**Performance Summaries**
- Team OKR progress
- Feature performance reports
- A/B test results summary
- Customer health scores

**Cohort Analysis**
- User retention cohorts
- Feature adoption trends
- Revenue cohort analysis
- Churn cohort breakdown

## Example Scenarios

### Scenario 1: Weekly Executive Summary
**Context**: Monday morning executive review

**Prompt Type**: Business Review

**Expected Output**:
```markdown
# Weekly Business Review - Week of Oct 21, 2025

## 🎯 Key Highlights

✅ DAU grew 12% WoW (23,450 → 26,264)
⚠️ Conversion rate declined 0.3pp (3.2% → 2.9%)
✅ Revenue beat forecast by 8% ($142K vs $132K target)

## 📊 Metrics Deep Dive

### Growth Metrics
- New signups: 2,145 (+15% WoW)
- Activation rate: 68% (↓2pp, within normal variance)
- Paid conversion: 2.9% (↓0.3pp, investigating)

### Engagement Metrics
- DAU/MAU: 42% (stable)
- Session duration: 8.2min (+5% WoW)
- Feature usage: Dashboard 78%, Reports 45%, Exports 23%

### Revenue Metrics
- MRR: $485K (+3% MoM)
- ARPU: $58 (+$2 MoM)
- Churn: 2.1% (target: <2.5%)

## 🔍 Notable Trends

1. **Mobile growth accelerating**: iOS DAU +18% WoW
2. **Enterprise segment outperforming**: +22% new enterprise signups
3. **Self-serve conversion softening**: Requires investigation

## 📋 Action Items

- [ ] Investigate self-serve conversion drop (Owner: PM)
- [ ] Analyze mobile growth drivers (Owner: Analytics)
- [ ] Prepare enterprise case study (Owner: Marketing)

## 🎯 Next Week Focus

- Launch new onboarding flow (targeting +5pp activation)
- Ship mobile dashboard v2
- Close Q4 enterprise pipeline
```

### Scenario 2: Cohort Retention Analysis
**Context**: Monthly retention review

**Prompt Type**: Cohort Analysis

**Expected Output**:
```markdown
# Monthly Cohort Retention - October 2025

## Cohort Performance

| Signup Month | D7 | D30 | D90 | D180 |
|-------------|-----|-----|-----|------|
| Oct 2025    | 45% | -   | -   | -    |
| Sep 2025    | 42% | 38% | -   | -    |
| Aug 2025    | 40% | 35% | 28% | -    |
| Jul 2025    | 38% | 32% | 25% | 22%  |

## Key Insights

✅ **Improving Early Retention**: Oct cohort shows +3pp D7 retention vs Sept
⚠️ **D30-D90 Drop**: 10pp average drop between D30-D90 (industry: 8pp)
✅ **Long-term Stable**: D90+ cohorts maintaining 22-25% retention

## Benchmarks

- Our D7: 42% vs Industry median: 38% ✅
- Our D30: 35% vs Industry median: 32% ✅
- Our D90: 28% vs Industry median: 30% ⚠️

## Recommendations

1. Focus on D30-D90 engagement (currently underperforming)
2. Study Oct cohort improvements (new onboarding impact?)
3. Implement re-engagement campaign for D60+ users
```

## Template Structure

All reporting prompts follow this structure:

```markdown
# [Prompt Name]

**Use Case**: [Brief description]
**Cadence**: Daily / Weekly / Monthly / Quarterly
**Audience**: [Executives / Team / Stakeholders]

## Prompt

[XML or structured prompt]

## Input Data Required

- Metric 1: [Source and timeframe]
- Metric 2: [Source and timeframe]
- Comparative data: [Benchmarks, targets, prior periods]

## Expected Output

[Format and example]

## Cost & Performance

- Average cost: $X per report
- Generation time: Xs
- Recommended model: [Model name]

## Production Metrics

- Generated: X reports
- Time saved: X hours vs manual
- Stakeholder satisfaction: X%
```

## Best Practices

### 1. Structure for Scanability
```markdown
# Good: Clear hierarchy, visual indicators
## 🎯 Key Highlights (2-3 bullets)
## 📊 Metrics Deep Dive (organized by category)
## 🔍 Notable Trends (insights, not just numbers)
## 📋 Action Items (clear owners)

# Bad: Wall of numbers
Metric1: 123, Metric2: 456, Metric3: 789...
```

### 2. Compare to Baselines
- Week-over-week (WoW)
- Month-over-month (MoM)
- Year-over-year (YoY)
- vs. Target/Goal
- vs. Industry benchmarks

### 3. Highlight What Matters
- Use ✅ ⚠️ 🚨 to indicate status
- Bold important changes
- Call out anomalies explicitly
- Separate signal from noise

### 4. Include Context
```markdown
# Good: Context + metric
Conversion rate: 2.9% (↓0.3pp WoW)
- Within normal variance range
- New pricing page deployed Oct 18
- Recommend monitoring for another week

# Bad: Just the number
Conversion rate: 2.9%
```

## Model Selection for Reporting

| Model | Cost | Speed | When to Use |
|-------|------|-------|-------------|
| **Claude Sonnet 4.5** | $3/M | ⚡⚡ | **RECOMMENDED**: Best insight quality |
| Claude Opus 4.1 | $15/M | ⚡ | Critical exec reports (quarterly reviews) |
| GPT-4o | $2.50/M | ⚡⚡ | Structured extraction, dashboard narration |
| Gemini Pro | $1.25/M | ⚡⚡ | Large context reports (100+ metrics) |

**Cost Optimization**: For weekly business reviews:
- Manual analysis: 4 hours @ $100/hr = $400/week
- Sonnet automation: $0.02/report + 30min review = $50/week
- **Savings**: $350/week, $18K/year

## Integration Patterns

### Pattern 1: Scheduled Generation
```python
# Weekly report every Monday 8am
@schedule.weekly(day='monday', hour=8)
def generate_weekly_report():
    metrics = fetch_metrics(period='last_week')
    report = reporting_prompt.run(metrics)
    send_to_stakeholders(report)
```

### Pattern 2: On-Demand with Caching
```python
# Generate once, serve to multiple stakeholders
@cache(ttl=86400)  # 24 hours
def get_daily_dashboard():
    metrics = fetch_metrics(period='today')
    return reporting_prompt.run(metrics)
```

### Pattern 3: Multi-Audience Variants
```python
# Same data, different audiences
metrics = fetch_metrics(period='last_month')

exec_report = reporting_prompt.run(
    metrics, audience='executives', detail_level='high_level'
)

team_report = reporting_prompt.run(
    metrics, audience='team', detail_level='detailed'
)
```

## Report Cadence Guidelines

| Cadence | Metrics Depth | Audience | Length |
|---------|--------------|----------|--------|
| **Daily** | 3-5 key metrics | Team, Ops | 1 page |
| **Weekly** | 10-15 metrics | Team, Leadership | 2-3 pages |
| **Monthly** | 20-30 metrics | Leadership, Board | 4-6 pages |
| **Quarterly** | 30-50 metrics | Board, Investors | 8-12 pages |

## Related Prompts

- **For real-time alerts**: See [monitoring/](../monitoring/)
- **For deep dives**: See [investigation/](../investigation/)
- **For stakeholder communication**: See ../../stakeholder-communication/

## Contributing

When adding reporting prompts, ensure they:
1. ✅ Specify clear cadence (daily/weekly/monthly)
2. ✅ Define target audience explicitly
3. ✅ Include comparison baselines
4. ✅ Show example output format
5. ✅ Document time/cost savings vs manual

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for full guidelines.

---

**Need help choosing?** Use the [decision tree](../README.md#category-principles) to select the right category.
