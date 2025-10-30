#!/usr/bin/env python3
"""Verify that current models are accessible via their APIs.

This script tests each model by making a minimal API call to confirm
the model identifier is valid and the API is accessible.

Usage:
    python scripts/verify_current_models.py                    # Test all models
    python scripts/verify_current_models.py --provider anthropic  # Single provider
    python scripts/verify_current_models.py --model claude-sonnet-4-5  # Single model

Requires:
    - API keys set in .env file or environment variables:
      - ANTHROPIC_API_KEY
      - OPENAI_API_KEY
      - GOOGLE_API_KEY
    - Provider packages installed (anthropic, openai, google-generativeai)

Exit codes:
    0 - All tested models succeeded
    1 - Some models failed
    2 - Setup error (missing deps/keys)
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, Optional

# Add parent directory to path to import ai_models
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(2)

# Optional: Load environment variables
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # dotenv is optional


class ModelVerifier:
    """Verify model API endpoints."""

    def __init__(self):
        """Initialize verifier."""
        self.results: Dict[str, Dict[str, any]] = {}
        self.definitions_dir = Path(__file__).parent.parent / "ai_models" / "definitions"

    def verify_anthropic_model(self, model_id: str, api_identifier: str) -> Dict[str, any]:
        """Verify Anthropic model.

        Args:
            model_id: Internal model ID
            api_identifier: Anthropic API model identifier

        Returns:
            Result dictionary with success/failure info
        """
        try:
            import anthropic
        except ImportError:
            return {
                "success": False,
                "error": "anthropic package not installed",
                "skip_reason": "missing_dependency",
            }

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return {
                "success": False,
                "error": "ANTHROPIC_API_KEY not set",
                "skip_reason": "missing_api_key",
            }

        try:
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model=api_identifier, max_tokens=10, messages=[{"role": "user", "content": "Hi"}]
            )

            return {
                "success": True,
                "api_identifier": api_identifier,
                "response_model": response.model,
                "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
            }

        except anthropic.NotFoundError:
            return {"success": False, "error": f"Model not found: {api_identifier}"}
        except anthropic.AuthenticationError:
            return {"success": False, "error": "Authentication failed", "skip_reason": "auth_error"}
        except Exception as e:
            return {"success": False, "error": f"{type(e).__name__}: {str(e)}"}

    def verify_openai_model(self, model_id: str, api_identifier: str) -> Dict[str, any]:
        """Verify OpenAI model.

        Args:
            model_id: Internal model ID
            api_identifier: OpenAI API model identifier

        Returns:
            Result dictionary with success/failure info
        """
        try:
            import openai
        except ImportError:
            return {
                "success": False,
                "error": "openai package not installed",
                "skip_reason": "missing_dependency",
            }

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {
                "success": False,
                "error": "OPENAI_API_KEY not set",
                "skip_reason": "missing_api_key",
            }

        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=api_identifier,
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}],
            )

            return {
                "success": True,
                "api_identifier": api_identifier,
                "response_model": response.model,
                "tokens_used": response.usage.total_tokens,
            }

        except openai.NotFoundError:
            return {"success": False, "error": f"Model not found: {api_identifier}"}
        except openai.AuthenticationError:
            return {"success": False, "error": "Authentication failed", "skip_reason": "auth_error"}
        except Exception as e:
            return {"success": False, "error": f"{type(e).__name__}: {str(e)}"}

    def verify_google_model(self, model_id: str, api_identifier: str) -> Dict[str, any]:
        """Verify Google Gemini model.

        Args:
            model_id: Internal model ID
            api_identifier: Google API model identifier

        Returns:
            Result dictionary with success/failure info
        """
        try:
            import google.generativeai as genai
        except ImportError:
            return {
                "success": False,
                "error": "google-generativeai package not installed",
                "skip_reason": "missing_dependency",
            }

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return {
                "success": False,
                "error": "GOOGLE_API_KEY not set",
                "skip_reason": "missing_api_key",
            }

        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(api_identifier)
            response = model.generate_content("Hi", generation_config={"max_output_tokens": 10})

            return {
                "success": True,
                "api_identifier": api_identifier,
                "response_text_preview": response.text[:50] if response.text else "",
            }

        except Exception as e:
            error_msg = str(e)
            if "API_KEY_INVALID" in error_msg or "authentication" in error_msg.lower():
                return {
                    "success": False,
                    "error": "Authentication failed",
                    "skip_reason": "auth_error",
                }
            elif "not found" in error_msg.lower():
                return {"success": False, "error": f"Model not found: {api_identifier}"}
            else:
                return {"success": False, "error": f"{type(e).__name__}: {error_msg}"}

    def verify_model(self, provider: str, model_id: str, api_identifier: str) -> Dict[str, any]:
        """Verify a model based on its provider.

        Args:
            provider: Provider name
            model_id: Internal model ID
            api_identifier: Provider's API model identifier

        Returns:
            Result dictionary
        """
        if provider.lower() == "anthropic":
            return self.verify_anthropic_model(model_id, api_identifier)
        elif provider.lower() == "openai":
            return self.verify_openai_model(model_id, api_identifier)
        elif provider.lower() == "google":
            return self.verify_google_model(model_id, api_identifier)
        else:
            return {"success": False, "error": f"Unknown provider: {provider}"}

    def verify_all_models(
        self, provider_filter: Optional[str] = None, model_filter: Optional[str] = None
    ) -> Dict[str, Dict[str, any]]:
        """Verify all model definitions.

        Args:
            provider_filter: Only check models from this provider
            model_filter: Only check this specific model

        Returns:
            Dictionary mapping model_id to result
        """
        if not self.definitions_dir.exists():
            print(f"Error: Definitions directory not found: {self.definitions_dir}")
            sys.exit(2)

        yaml_files = list(self.definitions_dir.rglob("*.yaml"))

        if not yaml_files:
            print(f"Warning: No model definitions found in {self.definitions_dir}")
            return {}

        for yaml_file in yaml_files:
            provider_name = yaml_file.parent.name

            # Apply filters
            if provider_filter and provider_name.lower() != provider_filter.lower():
                continue

            try:
                with open(yaml_file) as f:
                    data = yaml.safe_load(f)

                if not data or "model_id" not in data:
                    continue

                model_id = data["model_id"]

                if model_filter and model_id != model_filter:
                    continue

                api_identifier = data.get("api_identifier", model_id)

                print(f"\nTesting {model_id} ({api_identifier})...", end=" ")

                result = self.verify_model(provider_name, model_id, api_identifier)
                result["provider"] = provider_name
                result["model_id"] = model_id
                self.results[model_id] = result

                # Print immediate feedback
                if result["success"]:
                    print("✅ PASS")
                elif "skip_reason" in result:
                    print(f"⏭️  SKIP ({result.get('skip_reason')})")
                else:
                    print(f"❌ FAIL: {result.get('error', 'Unknown error')}")

            except Exception as e:
                print(f"Error processing {yaml_file}: {e}")
                continue

        return self.results

    def print_summary(self) -> None:
        """Print verification summary."""
        if not self.results:
            print("\nNo models tested.")
            return

        passed = [m for m in self.results.values() if m["success"]]
        failed = [m for m in self.results.values() if not m["success"] and "skip_reason" not in m]
        skipped = [m for m in self.results.values() if "skip_reason" in m]

        print("\n" + "=" * 80)
        print("MODEL VERIFICATION SUMMARY")
        print("=" * 80)
        print(f"\nTotal Models: {len(self.results)}")
        print(f"  ✅ Passed:  {len(passed)}")
        print(f"  ❌ Failed:  {len(failed)}")
        print(f"  ⏭️  Skipped: {len(skipped)}")

        if failed:
            print("\n" + "-" * 80)
            print("FAILED MODELS")
            print("-" * 80)
            for result in failed:
                print(f"\n  • {result['model_id']} ({result['provider']})")
                print(f"    Error: {result.get('error', 'Unknown error')}")

        if skipped:
            print("\n" + "-" * 80)
            print("SKIPPED MODELS")
            print("-" * 80)

            # Group by skip reason
            by_reason = {}
            for result in skipped:
                reason = result.get("skip_reason", "unknown")
                if reason not in by_reason:
                    by_reason[reason] = []
                by_reason[reason].append(result)

            for reason, models in by_reason.items():
                print(f"\n  {reason}:")
                for result in models:
                    print(f"    • {result['model_id']} ({result['provider']})")

        print("\n" + "=" * 80 + "\n")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Verify model API endpoints",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/verify_current_models.py                    # Test all models
  python scripts/verify_current_models.py --provider anthropic  # Single provider
  python scripts/verify_current_models.py --model claude-sonnet-4-5  # Single model

API Keys Required:
  Set in .env file or environment:
    ANTHROPIC_API_KEY
    OPENAI_API_KEY
    GOOGLE_API_KEY
        """,
    )

    parser.add_argument(
        "--provider",
        type=str,
        help="Only test models from this provider (anthropic, openai, google)",
    )

    parser.add_argument("--model", type=str, help="Only test this specific model")

    args = parser.parse_args()

    verifier = ModelVerifier()
    verifier.verify_all_models(provider_filter=args.provider, model_filter=args.model)
    verifier.print_summary()

    # Exit with code 1 if any models failed (not counting skipped)
    failed_count = sum(
        1 for r in verifier.results.values() if not r["success"] and "skip_reason" not in r
    )

    return 1 if failed_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
