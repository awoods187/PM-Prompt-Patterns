#!/usr/bin/env python3
# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Basic example of using the PM Prompt Toolkit.

This example demonstrates:
    - Simple signal classification
    - Cost tracking
    - Keyword filtering benefits

Usage:
    python examples/basic_example.py

Requirements:
    - ANTHROPIC_API_KEY set in .env file
    - pm_prompt_toolkit package installed (pip install -e .)
"""

from pm_prompt_toolkit import SignalClassifier  # type: ignore[attr-defined]


def main() -> None:
    """Run basic classification examples."""
    print("=" * 70)
    print("PM Prompt Toolkit - Basic Example")
    print("=" * 70)
    print()

    # Initialize classifier
    print("📦 Initializing SignalClassifier...")
    classifier = SignalClassifier()
    print(f"   Model: {classifier.model}")
    print(f"   Keyword filter: {classifier.enable_keyword_filter}")
    print()

    # Example signals
    test_signals = [
        "We need SSO integration before Q4 rollout",
        "Dashboard won't load, getting 500 errors",
        "Frustrated with performance, considering alternatives",
        "Can we get a quote for 100 more seats?",
        "Thanks for the great support!",
    ]

    # Classify each signal
    print("🔍 Classifying signals...")
    print()

    for i, signal in enumerate(test_signals, 1):
        print(f'{i}. Signal: "{signal}"')

        result = classifier.classify(signal)

        print(f"   → Category: {result.category.value}")
        print(f"   → Confidence: {result.confidence:.2f}")
        print(f"   → Method: {result.method}")
        print(f"   → Cost: ${result.cost:.4f}")
        print(f"   → Latency: {result.latency_ms:.0f}ms")

        # Highlight keyword matches (free!)
        if result.method == "keyword":
            print("   💰 FREE (keyword match!)")

        print()

    # Show metrics
    print("=" * 70)
    print("📊 Metrics Summary")
    print("=" * 70)

    metrics = classifier.get_metrics()
    print(f"Total requests: {metrics['total_requests']}")
    print(f"Total cost: ${metrics['total_cost']:.4f}")
    print(f"Average cost: ${metrics['average_cost']:.4f}")
    print(f"Average latency: {metrics['average_latency_ms']:.0f}ms")

    if metrics["cache_hit_rate"] > 0:
        print(f"Cache hit rate: {metrics['cache_hit_rate']:.1%}")

    # Cost savings breakdown
    keyword_savings = sum(
        1 for result in [classifier.classify(s) for s in test_signals] if result.method == "keyword"
    )
    if keyword_savings > 0:
        print()
        print("💡 Cost Savings:")
        print(f"   {keyword_savings}/{len(test_signals)} signals caught by keyword filter (FREE)")
        estimated_without_filter = len(test_signals) * 0.0008  # Avg Sonnet cost
        actual_cost = metrics["total_cost"]
        savings = estimated_without_filter - actual_cost
        print(f"   Estimated savings: ${savings:.4f} ({savings/estimated_without_filter:.1%})")

    print()
    print("=" * 70)
    print("✅ Example completed successfully!")
    print()
    print("Next steps:")
    print("  - Try your own signals")
    print("  - Experiment with different models (claude-haiku, claude-opus)")
    print("  - See PYTHON_PACKAGE_README.md for more examples")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Make sure you have a .env file with ANTHROPIC_API_KEY set")
        print("  2. Run: cp .env.example .env")
        print("  3. Edit .env and add your API key")
        print("  4. Make sure you installed the package: pip install -e .")
        raise
