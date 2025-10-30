#!/usr/bin/env python3
"""Check if model definitions need verification.

This script checks all model YAML files and reports models that haven't been
verified within the staleness threshold (default 90 days).

Usage:
    python scripts/check_staleness.py                    # Check all models
    python scripts/check_staleness.py --days 60          # Custom threshold
    python scripts/check_staleness.py --provider anthropic  # Single provider

Exit codes:
    0 - All models current
    1 - Stale models found
    2 - Error occurred
"""

import argparse
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(2)


class ModelStalenessChecker:
    """Check model definitions for staleness."""

    def __init__(self, stale_days: int = 90):
        """Initialize checker.

        Args:
            stale_days: Number of days before model is considered stale
        """
        self.stale_days = stale_days
        self.stale_threshold = date.today() - timedelta(days=stale_days)
        self.definitions_dir = Path(__file__).parent.parent / "ai_models" / "definitions"

    def check_all_models(
        self, provider_filter: Optional[str] = None
    ) -> Dict[str, List[Dict[str, any]]]:
        """Check all model definitions.

        Args:
            provider_filter: Only check models from this provider

        Returns:
            Dictionary with 'stale' and 'current' lists
        """
        if not self.definitions_dir.exists():
            print(f"Error: Definitions directory not found: {self.definitions_dir}")
            sys.exit(2)

        stale_models = []
        current_models = []

        # Find all YAML files
        yaml_files = list(self.definitions_dir.rglob("*.yaml"))

        if not yaml_files:
            print(f"Warning: No model definitions found in {self.definitions_dir}")
            return {"stale": [], "current": []}

        for yaml_file in yaml_files:
            provider_name = yaml_file.parent.name

            # Apply provider filter if specified
            if provider_filter and provider_name.lower() != provider_filter.lower():
                continue

            try:
                with open(yaml_file) as f:
                    data = yaml.safe_load(f)

                if not data or "model_id" not in data:
                    print(f"Warning: Skipping invalid file: {yaml_file}")
                    continue

                model_id = data["model_id"]
                metadata = data.get("metadata", {})
                last_verified_str = metadata.get("last_verified")

                if not last_verified_str:
                    print(f"Warning: No last_verified date for {model_id}")
                    stale_models.append(
                        {
                            "model_id": model_id,
                            "provider": provider_name,
                            "last_verified": None,
                            "days_old": None,
                            "file": str(yaml_file.relative_to(self.definitions_dir.parent)),
                            "docs_url": metadata.get("docs_url", ""),
                        }
                    )
                    continue

                # Parse last_verified date
                try:
                    last_verified = datetime.strptime(last_verified_str, "%Y-%m-%d").date()
                except ValueError:
                    print(f"Warning: Invalid date format for {model_id}: {last_verified_str}")
                    continue

                days_old = (date.today() - last_verified).days

                model_info = {
                    "model_id": model_id,
                    "provider": provider_name,
                    "last_verified": last_verified,
                    "days_old": days_old,
                    "file": str(yaml_file.relative_to(self.definitions_dir.parent)),
                    "docs_url": metadata.get("docs_url", ""),
                    "api_identifier": data.get("api_identifier", ""),
                }

                if last_verified < self.stale_threshold:
                    stale_models.append(model_info)
                else:
                    current_models.append(model_info)

            except Exception as e:
                print(f"Error processing {yaml_file}: {e}")
                continue

        return {"stale": stale_models, "current": current_models}

    def print_report(self, results: Dict[str, List[Dict[str, any]]]) -> None:
        """Print formatted staleness report.

        Args:
            results: Results from check_all_models
        """
        stale = results["stale"]
        current = results["current"]

        print("\n" + "=" * 80)
        print(f"MODEL STALENESS REPORT - {date.today()}")
        print("=" * 80)
        print(f"\nStaleness Threshold: {self.stale_days} days")
        print(f"Stale if not verified since: {self.stale_threshold}")
        print(f"\nTotal Models: {len(stale) + len(current)}")
        print(f"  Current: {len(current)}")
        print(f"  Stale:   {len(stale)}")

        if stale:
            print("\n" + "-" * 80)
            print("⚠️  STALE MODELS (need verification)")
            print("-" * 80)

            # Group by provider
            by_provider = {}
            for model in stale:
                provider = model["provider"]
                if provider not in by_provider:
                    by_provider[provider] = []
                by_provider[provider].append(model)

            for provider, models in sorted(by_provider.items()):
                print(f"\n📦 {provider.upper()}")
                for model in sorted(models, key=lambda m: m["days_old"] or 999, reverse=True):
                    days_str = f"{model['days_old']} days" if model["days_old"] else "NEVER"
                    print(f"\n  • {model['model_id']}")
                    print(
                        f"    Last verified: {model['last_verified'] or 'NEVER'} ({days_str} ago)"
                    )
                    print(f"    File: {model['file']}")
                    if model["api_identifier"]:
                        print(f"    API ID: {model['api_identifier']}")
                    if model["docs_url"]:
                        print(f"    Check: {model['docs_url']}")

        if current:
            print("\n" + "-" * 80)
            print("✅ CURRENT MODELS")
            print("-" * 80)

            # Group by provider
            by_provider = {}
            for model in current:
                provider = model["provider"]
                if provider not in by_provider:
                    by_provider[provider] = []
                by_provider[provider].append(model)

            for provider, models in sorted(by_provider.items()):
                print(f"\n📦 {provider.upper()}")
                for model in sorted(models, key=lambda m: m["model_id"]):
                    days_str = f"{model['days_old']} days ago"
                    print(
                        f"  • {model['model_id']}: verified {model['last_verified']} ({days_str})"
                    )

        print("\n" + "=" * 80)

        if stale:
            print("\n⚠️  ACTION REQUIRED:")
            print(
                f"   {len(stale)} model(s) need verification. Follow docs/workflows/MODEL_UPDATE_WORKFLOW.md"
            )
            print("=" * 80 + "\n")
        else:
            print("\n✅ All models are current!")
            print("=" * 80 + "\n")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check model definitions for staleness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/check_staleness.py                    # Check all models
  python scripts/check_staleness.py --days 60          # Custom threshold
  python scripts/check_staleness.py --provider anthropic  # Single provider
  python scripts/check_staleness.py --quiet            # Only print if stale
        """,
    )

    parser.add_argument(
        "--days",
        type=int,
        default=90,
        help="Number of days before model is considered stale (default: 90)",
    )

    parser.add_argument(
        "--provider",
        type=str,
        help="Only check models from this provider (anthropic, openai, google)",
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print report if stale models found",
    )

    args = parser.parse_args()

    checker = ModelStalenessChecker(stale_days=args.days)
    results = checker.check_all_models(provider_filter=args.provider)

    stale_count = len(results["stale"])

    if not args.quiet or stale_count > 0:
        checker.print_report(results)

    # Exit with code 1 if stale models found
    return 1 if stale_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
