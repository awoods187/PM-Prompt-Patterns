# Investigation Prompts

**Ad-hoc analysis, root cause investigation, and exploratory deep dives**

## Overview

Investigation prompts are designed for **one-time, exploratory** analysis when you need to understand "why" something happened. Use these for root cause analysis, custom investigations, and ad-hoc deep dives.

### Key Characteristics
- 🔍 **Temporal Pattern**: Ad-hoc, one-time, exploratory
- 🎯 **Primary Goal**: Understand root causes and discover insights
- 🧪 **Approach**: Exploratory, hypothesis-driven
- 📝 **Output**: Findings, hypotheses, recommendations

## Use Cases

### When to Use Investigation Prompts

✅ **Use investigation when you need to:**
- Understand why a metric changed unexpectedly
- Perform root cause analysis on incidents
- Explore new data sources or metrics
- Answer specific business questions
- Validate or disprove hypotheses
- Classify signals or feedback ad-hoc

❌ **Don't use investigation for:**
- Continuous monitoring (use [monitoring/](../monitoring/) instead)
- Recurring reports (use [reporting/](../reporting/) instead)
- Standardized analysis (use [reporting/](../reporting/) instead)

## Available Prompts

### 🚧 Coming Soon

This section will include production-tested prompts for:

**Root Cause Analysis**
- Metric change investigation
- Incident post-mortems
- Performance degradation analysis
- User behavior changes

**Exploratory Analysis**
- Signal classification
- Pattern discovery
- Correlation analysis
- Hypothesis generation

**Deep Dives**
- Feature impact analysis
- Cohort behavior exploration
- Customer segment analysis
- Competitive analysis

**Custom Investigations**
- Ad-hoc metric analysis
- Data quality assessment
- Funnel breakdown analysis
- User journey mapping

## Example Scenarios

### Scenario 1: Conversion Rate Drop Investigation
**Context**: Signup conversion dropped from 3.2% to 2.1% over 3 days

**Prompt Type**: Root Cause Analysis

**Expected Output**:
```markdown
# Root Cause Analysis: Conversion Rate Drop

## Problem Statement
Signup conversion rate dropped 34% (3.2% → 2.1%) from Oct 18-21, 2025

## Investigation Framework

### 1. When did it start?
- **Onset**: Oct 18, 2025, 14:30 UTC
- **Pattern**: Sudden drop, not gradual decline
- **Correlation**: Coincides with pricing page deploy (v2.4.1)

### 2. Who is affected?
**By Segment:**
- Self-serve: 3.2% → 1.8% (↓44%) 🚨
- Enterprise: 12% → 11.5% (↓4%) ✅
- SMB: 4.1% → 3.9% (↓5%) ✅

**By Source:**
- Organic: 3.5% → 2.0% (↓43%) 🚨
- Paid: 2.8% → 2.6% (↓7%) ✅
- Referral: 4.2% → 4.0% (↓5%) ✅

**Finding**: Primarily affecting self-serve + organic traffic

### 3. What changed?
**Code Deploys:**
- ✅ Oct 18, 14:32 UTC: Pricing page redesign (v2.4.1)
- Oct 17, 09:15 UTC: Backend optimization (v2.4.0)

**Marketing:**
- No campaign changes
- No pricing changes
- No major announcements

**External:**
- No competitor launches
- No industry news
- No seasonal factors

**Finding**: Strong correlation with pricing page deploy

### 4. Hypothesis Testing

**Hypothesis 1**: New pricing page is confusing
- **Evidence**: Time on page increased 45% (2min → 3min)
- **Evidence**: "Compare plans" clicks decreased 60%
- **Evidence**: 3 support tickets mentioning "can't find free tier"
- **Conclusion**: LIKELY ROOT CAUSE

**Hypothesis 2**: Technical issue with signup button
- **Evidence**: No error logs
- **Evidence**: Button click tracking working
- **Conclusion**: NOT THE CAUSE

**Hypothesis 3**: Broader market shift
- **Evidence**: Only self-serve affected
- **Evidence**: Enterprise conversion stable
- **Conclusion**: NOT THE CAUSE

## Root Cause

**Primary**: New pricing page (v2.4.1) removed prominent free tier callout
- Self-serve users can't find free plan quickly
- Increased cognitive load to compare plans
- Disproportionately affects organic traffic (price-sensitive)

**Secondary**: None identified

## Recommendations

### Immediate (< 24h)
1. 🚨 Roll back pricing page to v2.4.0
2. Monitor conversion recovery
3. Alert stakeholders

### Short-term (1 week)
1. Redesign pricing page with prominent free tier
2. A/B test new design before full deploy
3. Add analytics tracking for plan comparison flow

### Long-term (1 month)
1. Implement pre-deploy conversion monitoring
2. Create pricing page A/B testing framework
3. Document this incident for future deploys

## Impact Assessment

**Revenue Impact:**
- Lost conversions: ~150 signups
- Estimated revenue impact: $8,700 MRR
- Time to detect: 3 days (goal: < 1 day)

**Lessons Learned:**
- Need real-time conversion monitoring
- A/B test all pricing page changes
- Segment analysis crucial for root cause
```

### Scenario 2: Feature Adoption Analysis
**Context**: New dashboard feature launched 60 days ago, need adoption analysis

**Prompt Type**: Exploratory Analysis

**Expected Output**:
```markdown
# Feature Adoption Analysis: Analytics Dashboard v2

## Summary
Dashboard v2 launched Sept 1, 2025 (60 days ago)

**Overall Adoption**: 34% of active users (3,456 / 10,200)
**Target**: 50% by Day 90
**Status**: 🟡 Behind target, but trending up

## Adoption Breakdown

### By User Segment
| Segment | Adoption Rate | vs. Average |
|---------|---------------|-------------|
| Power users | 78% | +44pp ✅ |
| Regular users | 42% | +8pp ✅ |
| Light users | 12% | -22pp 🚨 |

### By Plan Type
| Plan | Adoption Rate | vs. Average |
|------|---------------|-------------|
| Enterprise | 67% | +33pp ✅ |
| Pro | 45% | +11pp ✅ |
| Free | 18% | -16pp 🚨 |

### Time to First Use
- Median: 7 days post-launch
- Mean: 12 days post-launch
- 50% adopted within 14 days
- 20% never attempted feature

## Discovery Methods

**How users found feature:**
- In-app announcement: 45%
- Organic discovery: 28%
- Teammate share: 18%
- Support article: 9%

**Finding**: In-app prompts most effective

## Usage Patterns

**Frequency (among adopters):**
- Daily: 15%
- Weekly: 42%
- Monthly: 28%
- One-time: 15%

**Retention**: 72% still using after 30 days

## Barriers to Adoption

**Hypotheses tested:**
1. **Feature not discoverable** → Partially true
   - 20% of users never saw feature
   - Free users less likely to see announcements

2. **Feature too complex** → False
   - 85% successfully completed first use
   - Low abandonment rate

3. **Feature not valuable** → Partially true
   - Light users report "too advanced" (survey)
   - Free plan may not need dashboards

## Recommendations

### Increase Discoverability (Target: +10pp adoption)
1. Add persistent banner for free users
2. Include in onboarding checklist
3. Create "Quick Start" tutorial

### Improve Light User Experience (Target: +8pp adoption)
1. Create "Simplified Dashboard" for free tier
2. Reduce default widget complexity
3. Add templates for common use cases

### Accelerate Time to Value (Target: -5 days to first use)
1. Trigger in-app tutorial on first login post-launch
2. Send targeted email on Day 3 if not adopted
3. Add "Try Dashboard" CTAs in existing reports

## Success Metrics (30-day check-in)

- [ ] Overall adoption: 44% (+10pp)
- [ ] Light user adoption: 20% (+8pp)
- [ ] Time to first use: < 7 days
- [ ] 30-day retention: > 75%
```

## Template Structure

All investigation prompts follow this structure:

```markdown
# [Prompt Name]

**Use Case**: [Brief description]
**Investigation Type**: Root Cause / Exploratory / Hypothesis Testing
**Typical Duration**: [Time needed]

## Prompt

[XML or structured prompt with investigation framework]

## Input Data Required

- Primary data: [What you're investigating]
- Comparative data: [Baselines, segments, timeframes]
- Context data: [Deploys, campaigns, external events]

## Investigation Framework

1. Define the question
2. Gather relevant data
3. Form hypotheses
4. Test hypotheses systematically
5. Draw conclusions
6. Make recommendations

## Expected Output

[Format with findings, evidence, recommendations]

## Cost & Performance

- Average cost: $X per investigation
- Analysis time: X hours
- Recommended model: [Model name]

## Production Metrics

- Investigations completed: X
- Accuracy of root cause: X%
- Time saved vs manual: X hours
```

## Investigation Frameworks

### Framework 1: The 5 Whys
```
Problem: Conversion rate dropped

Why? Pricing page confusing
  Why? Free tier not prominent
    Why? Design removed callout
      Why? Designer didn't see original metrics
        Why? No documentation of high-performing elements

Root Cause: Missing design documentation
Fix: Document critical UI elements before redesigns
```

### Framework 2: Segment Analysis
```
1. When did it start?
2. Who is affected? (segment by everything)
3. What changed? (code, marketing, external)
4. Test hypotheses
5. Identify root cause
6. Recommend fixes
```

### Framework 3: Hypothesis-Driven
```
1. State the problem quantitatively
2. Generate 3-5 hypotheses
3. For each hypothesis:
   - What evidence would prove it?
   - What evidence would disprove it?
4. Gather evidence systematically
5. Rank hypotheses by likelihood
6. Investigate top hypothesis deeply
```

## Best Practices

### 1. Be Systematic
```markdown
# Good: Structured, testable
Hypothesis 1: New pricing page is confusing
Evidence for: Time on page +45%, clicks down 60%
Evidence against: No error logs
Conclusion: LIKELY CAUSE

# Bad: Jumping to conclusions
I think it's the new pricing page.
```

### 2. Use Data to Eliminate Hypotheses
- Start with 5-10 hypotheses
- Systematically eliminate unlikely causes
- Focus investigation on top 1-2 remaining
- Document why you ruled out others

### 3. Consider Multiple Segments
Always analyze by:
- User type (new vs. returning)
- Plan tier (free vs. paid)
- Traffic source (organic vs. paid)
- Platform (web vs. mobile)
- Geography (if relevant)

### 4. Quantify Impact
```markdown
# Good: Quantified business impact
Revenue impact: $8,700 MRR lost
Affected users: 2,450 self-serve signups
Time to detect: 3 days

# Bad: Vague
This is bad and we should fix it.
```

## Model Selection for Investigation

| Model | Cost | Speed | When to Use |
|-------|------|-------|-------------|
| **Claude Sonnet 4.5** | $3/M | ⚡⚡ | **RECOMMENDED**: Best for complex analysis |
| Claude Opus 4.1 | $15/M | ⚡ | High-stakes incidents, critical decisions |
| Gemini 2.5 Pro | $1.25/M | ⚡⚡ | Large context (analyzing 100+ data points) |
| GPT-4o | $2.50/M | ⚡⚡ | Structured hypothesis testing |

**Cost Optimization**: For incident investigation:
- Manual analysis: 8-16 hours @ $100/hr = $800-1,600
- Sonnet investigation: $0.15 + 2 hours review = $215
- **Savings**: $585-1,385 per investigation

## Investigation Checklist

Before starting investigation:
- [ ] Define the specific question to answer
- [ ] Set investigation scope (time, depth)
- [ ] Gather baseline comparison data
- [ ] List what changed (deploys, campaigns, external)
- [ ] Generate initial hypotheses

During investigation:
- [ ] Test each hypothesis systematically
- [ ] Document evidence for and against
- [ ] Segment analysis by user type, source, platform
- [ ] Consider multiple timeframes (hourly, daily, weekly)
- [ ] Validate findings with stakeholders

After investigation:
- [ ] Quantify business impact
- [ ] Provide specific, actionable recommendations
- [ ] Document lessons learned
- [ ] Create prevention measures
- [ ] Share findings with team

## Related Prompts

- **For continuous monitoring**: See [monitoring/](../monitoring/)
- **For recurring analysis**: See [reporting/](../reporting/)
- **For strategic decisions**: See ../../product-strategy/

## Contributing

When adding investigation prompts, ensure they:
1. ✅ Include systematic investigation framework
2. ✅ Show hypothesis generation and testing
3. ✅ Provide segment analysis examples
4. ✅ Quantify impact and recommendations
5. ✅ Document time/cost savings vs manual

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for full guidelines.

---

**Need help choosing?** Use the [decision tree](../README.md#category-principles) to select the right category.
