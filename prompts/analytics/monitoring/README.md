# Monitoring Prompts

**Real-time metric surveillance, anomaly detection, and automated alerting**

## Overview

Monitoring prompts are designed for **continuous, real-time** analysis of metrics and signals. Use these when you need to actively watch for changes, detect anomalies, or generate automated alerts.

### Key Characteristics
- ⏱️ **Temporal Pattern**: Continuous, real-time, or near-real-time
- 🎯 **Primary Goal**: Detect changes and anomalies quickly
- 🤖 **Automation**: Designed for automated execution
- 📊 **Output**: Alerts, flags, anomaly reports

## Use Cases

### When to Use Monitoring Prompts

✅ **Use monitoring when you need to:**
- Detect sudden spikes or drops in metrics
- Generate automated alerts for threshold violations
- Identify unusual patterns in real-time data
- Narrate live dashboard changes
- Flag potential issues before they become critical
- Monitor SLA compliance continuously

❌ **Don't use monitoring for:**
- One-time analysis (use [investigation/](../investigation/) instead)
- Weekly/monthly reports (use [reporting/](../reporting/) instead)
- Exploratory data analysis (use [investigation/](../investigation/) instead)

## Available Prompts

### 🚧 Coming Soon

This section will include production-tested prompts for:

**Anomaly Detection**
- Real-time spike detection
- Threshold violation alerts
- Pattern deviation identification
- Seasonal anomaly detection

**Alert Generation**
- Automated alert narration
- Severity classification
- Alert prioritization
- False positive reduction

**Dashboard Narration**
- Live metric explanation
- Change summarization
- Trend identification
- Quick insights generation

**Metric Surveillance**
- Continuous health checks
- SLA monitoring
- Performance tracking
- Quality score monitoring

## Example Scenarios

### Scenario 1: Real-Time Churn Alert
**Context**: Monitoring daily active users for sudden drops

**Prompt Type**: Anomaly Detection + Alert Generation

**Expected Output**:
```
🚨 ALERT: Critical DAU Drop Detected

Metric: Daily Active Users
Change: -23% (15,234 → 11,730)
Timeframe: Last 4 hours
Severity: HIGH

Anomaly Detection:
- 3.2σ deviation from 30-day mean
- Outside normal variance range
- Coincides with deploy at 14:32 UTC

Recommended Action:
1. Investigate recent deploy (v2.4.1)
2. Check error logs for spikes
3. Review user feedback channels
```

### Scenario 2: Conversion Rate Monitoring
**Context**: Continuous tracking of signup conversion

**Prompt Type**: Metric Surveillance

**Expected Output**:
```
✅ Conversion Rate: Normal

Current: 3.2% (↑0.1% from yesterday)
24h Trend: Stable
7d Average: 3.1%
Status: Within expected range (2.8% - 3.5%)

No anomalies detected.
```

## Template Structure

All monitoring prompts follow this structure:

```markdown
# [Prompt Name]

**Use Case**: [Brief description]
**Temporal Pattern**: Real-time / Continuous
**Automation**: [Manual / Semi-automated / Fully automated]

## Prompt

[XML or structured prompt]

## Expected Output

[Format and example]

## Cost & Performance

- Average cost: $X per execution
- Average latency: Xms
- Recommended model: [Model name]

## Production Metrics

- Accuracy: X%
- False positive rate: X%
- Detection time: Xms
```

## Best Practices

### 1. Set Clear Thresholds
```python
# Good: Specific, measurable
if metric_change > 2.5 * std_dev:
    trigger_alert()

# Bad: Vague
if metric_seems_unusual:
    trigger_alert()
```

### 2. Include Context in Alerts
- Compare to historical baselines
- Show statistical significance
- Reference recent changes (deploys, campaigns)
- Suggest next steps

### 3. Reduce Alert Fatigue
- Use severity levels (LOW, MEDIUM, HIGH, CRITICAL)
- Implement cooldown periods
- Aggregate related alerts
- Learn from false positives

### 4. Optimize for Speed
- Use faster models (Haiku, Flash) for monitoring
- Cache baseline calculations
- Pre-compute statistical thresholds
- Batch similar checks

## Model Selection for Monitoring

| Model | Cost | Speed | When to Use |
|-------|------|-------|-------------|
| **Claude Haiku 4.5** | $1/M | ⚡⚡⚡ | **RECOMMENDED**: Fast anomaly detection |
| **Gemini Flash** | $0.075/M | ⚡⚡⚡ | Ultra-high volume monitoring |
| **GPT-4o mini** | $0.15/M | ⚡⚡⚡ | Budget monitoring with good accuracy |
| Claude Sonnet | $3/M | ⚡⚡ | Complex pattern recognition |

**Cost Optimization**: For 10K daily checks:
- Haiku: ~$30/month
- Flash: ~$2.25/month
- Savings from early detection: $10K-100K+ (prevented incidents)

## Integration Patterns

### Pattern 1: Continuous Polling
```python
# Check every N minutes
while True:
    metrics = fetch_current_metrics()
    result = monitor_prompt.run(metrics)
    if result.is_anomaly:
        send_alert(result)
    time.sleep(300)  # 5 minutes
```

### Pattern 2: Event-Driven
```python
# Trigger on metric update
@on_metric_update
def check_anomaly(metric_event):
    result = monitor_prompt.run(metric_event.data)
    if result.is_anomaly:
        send_alert(result)
```

### Pattern 3: Batch Monitoring
```python
# Check multiple metrics efficiently
metrics_batch = fetch_all_metrics()
results = monitor_prompt.run_batch(metrics_batch)
anomalies = [r for r in results if r.is_anomaly]
send_daily_summary(anomalies)
```

## Related Prompts

- **For periodic reports**: See [reporting/](../reporting/)
- **For deep dives**: See [investigation/](../investigation/)
- **For metric definitions**: See ../../product-strategy/

## Contributing

When adding monitoring prompts, ensure they:
1. ✅ Execute in < 1 second for real-time use
2. ✅ Include clear threshold/anomaly criteria
3. ✅ Provide actionable outputs
4. ✅ Document false positive rate
5. ✅ Show production metrics (detection accuracy, etc.)

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for full guidelines.

---

**Need help choosing?** Use the [decision tree](../README.md#category-principles) to select the right category.
