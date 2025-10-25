# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Test pricing consistency between registry and providers.

This test suite ensures that hardcoded pricing in provider implementations
matches the verified pricing in models/registry.py (single source of truth).

Why this matters:
    - Prevents cost estimation errors (e.g., 4x underestimation)
    - Ensures accurate budget tracking
    - Catches stale pricing when models update
    - Validates single source of truth principle

Run: pytest tests/test_pricing_consistency.py -v
"""

import pytest
from models.registry import ModelRegistry

# Import provider pricing dicts directly (avoid package-level imports)
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Now we can import the pricing dictionaries
# We'll parse them from the source files since importing triggers missing deps
def get_claude_pricing():
    """Extract CLAUDE_PRICING from providers/claude.py without importing."""
    claude_file = Path(__file__).parent.parent / "pm_prompt_toolkit/providers/claude.py"
    with open(claude_file) as f:
        content = f.read()

    # Extract the pricing dict
    import ast
    tree = ast.parse(content)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "CLAUDE_PRICING":
                    # Evaluate the dict literal
                    return ast.literal_eval(node.value)
    raise ValueError("CLAUDE_PRICING not found")

# Get pricing dicts (only Claude is implemented as of 2025-10-25)
CLAUDE_PRICING = get_claude_pricing()

# TODO: Add OpenAI and Gemini when those providers are implemented
# OPENAI_PRICING = None  # Provider not implemented yet
# GEMINI_PRICING = None  # Provider not implemented yet


class TestClaudePricingConsistency:
    """Verify Claude provider pricing matches registry."""

    def test_claude_haiku_pricing_matches_registry(self):
        """Claude Haiku pricing must match registry (was 4x wrong before)."""
        registry_pricing = (
            ModelRegistry.CLAUDE_HAIKU_4_5.input_price_per_1m,
            ModelRegistry.CLAUDE_HAIKU_4_5.output_price_per_1m,
        )
        provider_pricing = CLAUDE_PRICING["claude-haiku"]

        assert provider_pricing == registry_pricing, (
            f"Claude Haiku pricing mismatch!\n"
            f"  Registry (source of truth): ${registry_pricing[0]}/${registry_pricing[1]} per 1M tokens\n"
            f"  Provider (hardcoded): ${provider_pricing[0]}/${provider_pricing[1]} per 1M tokens\n"
            f"  Fix: Update CLAUDE_PRICING in providers/claude.py"
        )

    def test_claude_sonnet_pricing_matches_registry(self):
        """Claude Sonnet pricing must match registry."""
        registry_pricing = (
            ModelRegistry.CLAUDE_SONNET_4_5.input_price_per_1m,
            ModelRegistry.CLAUDE_SONNET_4_5.output_price_per_1m,
        )
        provider_pricing = CLAUDE_PRICING["claude-sonnet"]

        assert provider_pricing == registry_pricing, (
            f"Claude Sonnet pricing mismatch!\n"
            f"  Registry: ${registry_pricing[0]}/${registry_pricing[1]}\n"
            f"  Provider: ${provider_pricing[0]}/${provider_pricing[1]}"
        )

    def test_claude_opus_pricing_matches_registry(self):
        """Claude Opus pricing must match registry."""
        registry_pricing = (
            ModelRegistry.CLAUDE_OPUS_4_1.input_price_per_1m,
            ModelRegistry.CLAUDE_OPUS_4_1.output_price_per_1m,
        )
        provider_pricing = CLAUDE_PRICING["claude-opus"]

        assert provider_pricing == registry_pricing, (
            f"Claude Opus pricing mismatch!\n"
            f"  Registry: ${registry_pricing[0]}/${registry_pricing[1]}\n"
            f"  Provider: ${provider_pricing[0]}/${provider_pricing[1]}"
        )


# TODO: Enable these tests when OpenAI and Gemini providers are implemented
# class TestOpenAIPricingConsistency:
#     """Verify OpenAI provider pricing matches registry."""
#
#     def test_gpt_4o_pricing_matches_registry(self):
#         """GPT-4o pricing must match registry."""
#         registry_pricing = (
#             ModelRegistry.GPT_4O.input_price_per_1m,
#             ModelRegistry.GPT_4O.output_price_per_1m,
#         )
#         provider_pricing = OPENAI_PRICING["gpt-4o"]
#
#         assert provider_pricing == registry_pricing
#
# class TestGeminiPricingConsistency:
#     """Verify Gemini provider pricing matches registry."""
#     # Tests commented out - provider not implemented yet


class TestPricingReasonableness:
    """Sanity checks for pricing values."""

    @pytest.mark.parametrize(
        "model_name,spec",
        [
            ("Claude Haiku 4.5", ModelRegistry.CLAUDE_HAIKU_4_5),
            ("Claude Sonnet 4.5", ModelRegistry.CLAUDE_SONNET_4_5),
            ("Claude Opus 4.1", ModelRegistry.CLAUDE_OPUS_4_1),
            ("GPT-4o", ModelRegistry.GPT_4O),
            ("GPT-4o Mini", ModelRegistry.GPT_4O_MINI),
            ("Gemini 2.5 Pro", ModelRegistry.GEMINI_2_5_PRO),
            ("Gemini 2.5 Flash", ModelRegistry.GEMINI_2_5_FLASH),
            ("Gemini 2.5 Flash-Lite", ModelRegistry.GEMINI_2_5_FLASH_LITE),
        ],
    )
    def test_output_more_expensive_than_input(self, model_name, spec):
        """Output tokens should cost more than input tokens (industry standard)."""
        # Exception: Free models
        if spec.input_price_per_1m == 0.0 and spec.output_price_per_1m == 0.0:
            pytest.skip(f"{model_name} is free tier")

        assert (
            spec.output_price_per_1m >= spec.input_price_per_1m
        ), f"{model_name}: Output (${spec.output_price_per_1m}) should cost >= input (${spec.input_price_per_1m})"

    @pytest.mark.parametrize(
        "model_name,spec,expected_range",
        [
            ("Claude Haiku", ModelRegistry.CLAUDE_HAIKU_4_5, (0.1, 10.0)),  # Budget model
            ("Claude Sonnet", ModelRegistry.CLAUDE_SONNET_4_5, (1.0, 30.0)),  # Mid-tier
            ("Claude Opus", ModelRegistry.CLAUDE_OPUS_4_1, (10.0, 100.0)),  # Premium
            ("GPT-4o", ModelRegistry.GPT_4O, (1.0, 20.0)),  # Mid-tier
            ("GPT-4o Mini", ModelRegistry.GPT_4O_MINI, (0.1, 5.0)),  # Budget
            ("Gemini Pro", ModelRegistry.GEMINI_2_5_PRO, (0.5, 20.0)),  # Mid-tier
            ("Gemini Flash", ModelRegistry.GEMINI_2_5_FLASH, (0.01, 5.0)),  # Fast/cheap
        ],
    )
    def test_pricing_in_reasonable_range(self, model_name, spec, expected_range):
        """Pricing should be in reasonable range for model tier."""
        min_price, max_price = expected_range

        assert (
            min_price <= spec.input_price_per_1m <= max_price
        ), f"{model_name} input pricing ${spec.input_price_per_1m} outside expected range ${min_price}-${max_price}"

        assert (
            min_price <= spec.output_price_per_1m <= max_price
        ), f"{model_name} output pricing ${spec.output_price_per_1m} outside expected range ${min_price}-${max_price}"


class TestCostCalculationAccuracy:
    """Test cost calculation examples to catch estimation errors."""

    def test_claude_haiku_cost_calculation_example(self):
        """Verify Claude Haiku cost calculation (caught 4x error)."""
        # Example: 1M input tokens, 100k output tokens
        input_tokens = 1_000_000
        output_tokens = 100_000

        expected_cost = (
            (input_tokens / 1_000_000) * ModelRegistry.CLAUDE_HAIKU_4_5.input_price_per_1m
            + (output_tokens / 1_000_000) * ModelRegistry.CLAUDE_HAIKU_4_5.output_price_per_1m
        )

        # With correct pricing ($1.00/$5.00):
        # = (1M / 1M * 1.00) + (100k / 1M * 5.00)
        # = 1.00 + 0.50 = $1.50
        assert expected_cost == 1.50, f"Expected $1.50, got ${expected_cost}"

        # If using OLD WRONG pricing ($0.25/$1.25), would get:
        # = (1M / 1M * 0.25) + (100k / 1M * 1.25)
        # = 0.25 + 0.125 = $0.375
        # This is a 4x underestimation!

    def test_claude_pricing_dict_exists(self):
        """Claude pricing dict should exist and be non-empty."""
        assert isinstance(CLAUDE_PRICING, dict), "CLAUDE_PRICING should be a dict"
        assert len(CLAUDE_PRICING) > 0, "CLAUDE_PRICING should not be empty"

        # TODO: Add OpenAI and Gemini when providers are implemented


class TestProviderPricingFormat:
    """Verify provider pricing dictionaries follow expected format."""

    def test_claude_pricing_dict_format(self):
        """Claude pricing dict should map model names to (input, output) tuples."""
        for model_name, pricing in CLAUDE_PRICING.items():
            assert isinstance(
                pricing, tuple
            ), f"{model_name}: pricing should be tuple, got {type(pricing)}"
            assert (
                len(pricing) == 2
            ), f"{model_name}: pricing should be (input, output), got {pricing}"
            assert all(
                isinstance(p, (int, float)) for p in pricing
            ), f"{model_name}: pricing values should be numbers"

    # TODO: Add OpenAI and Gemini pricing format tests when providers are implemented


class TestPricingDocumentation:
    """Verify pricing documentation is up to date."""

    def test_claude_pricing_has_verification_comment(self):
        """Claude pricing should have verification date comment."""
        # This tests that we're following best practices for maintaining pricing
        claude_file = Path(__file__).parent.parent / "pm_prompt_toolkit/providers/claude.py"
        with open(claude_file) as f:
            source = f.read()

        assert "verified" in source.lower() or "updated" in source.lower(), (
            "Claude provider should document when pricing was last verified.\n"
            "Add comment: # Last verified: YYYY-MM-DD"
        )

    def test_all_models_have_recent_verification_dates(self):
        """All models in registry should have recent verification dates."""
        from datetime import date, timedelta

        # Allow models up to 90 days old (same as staleness test)
        max_age_days = 90
        today = date.today()
        min_allowed_date = today - timedelta(days=max_age_days)

        all_models_dict = ModelRegistry.get_all_current_models()

        for model_id, spec in all_models_dict.items():
            days_old = (today - spec.last_verified).days
            assert spec.last_verified >= min_allowed_date, (
                f"{spec.name}: Verification date {spec.last_verified} is {days_old} days old (max {max_age_days})\n"
                f"Pricing may be stale. Verify at: {spec.docs_url}"
            )
