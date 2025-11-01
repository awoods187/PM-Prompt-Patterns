# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
Comprehensive tests for Anthropic Claude fetcher.

Coverage Target: 80%+
Current Coverage: 42.86%
Priority: HIGH - Close coverage gap
"""

from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from scripts.model_updater.fetchers.anthropic_fetcher import AnthropicFetcher
from scripts.model_updater.fetchers.base_fetcher import ModelData


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def anthropic_fetcher() -> AnthropicFetcher:
    """Create Anthropic fetcher instance."""
    return AnthropicFetcher()


# ============================================================================
# STATIC SPECS TESTS
# ============================================================================


class TestStaticModelSpecs:
    """Test suite for static model specifications."""

    def test_get_static_specs_claude_sonnet_45_returns_valid_specs(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that Claude Sonnet 4.5 specs are complete and valid."""
        specs = anthropic_fetcher._get_static_model_specs("claude-sonnet-4-5")

        assert specs is not None
        assert specs["context_window_input"] == 200000
        assert specs["context_window_output"] is None
        assert specs["knowledge_cutoff"] == "January 2025"
        assert specs["release_date"] == "2025-09-29"
        assert "pricing" in specs
        assert specs["pricing"]["input_per_1m"] == 3.00
        assert specs["pricing"]["output_per_1m"] == 15.00
        assert "cache_write_per_1m" in specs["pricing"]
        assert "cache_read_per_1m" in specs["pricing"]
        assert "capabilities" in specs
        assert "vision" in specs["capabilities"]
        assert "function_calling" in specs["capabilities"]

    def test_get_static_specs_claude_haiku_45_returns_valid_specs(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that Claude Haiku 4.5 specs are complete and valid."""
        specs = anthropic_fetcher._get_static_model_specs("claude-haiku-4-5")

        assert specs is not None
        assert specs["context_window_input"] == 200000
        assert specs["context_window_output"] == 16000
        assert specs["pricing"]["input_per_1m"] == 0.80
        assert specs["pricing"]["output_per_1m"] == 4.00
        assert specs["cost_tier"] == "budget"
        assert specs["speed_tier"] == "fast"

    def test_get_static_specs_unknown_model_returns_none(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that unknown model ID returns None."""
        specs = anthropic_fetcher._get_static_model_specs("unknown-model")

        assert specs is None

    def test_static_specs_include_prompt_caching_pricing(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that specs include prompt caching pricing."""
        specs = anthropic_fetcher._get_static_model_specs("claude-sonnet-4-5")

        assert "pricing" in specs
        assert "cache_write_per_1m" in specs["pricing"]
        assert "cache_read_per_1m" in specs["pricing"]
        # Cache write should be slightly more expensive than input (1.25x)
        assert specs["pricing"]["cache_write_per_1m"] > specs["pricing"]["input_per_1m"]
        # Cache read should be significantly cheaper than input
        assert specs["pricing"]["cache_read_per_1m"] < specs["pricing"]["input_per_1m"]

    def test_static_specs_include_recommended_for(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that specs include recommended use cases."""
        specs = anthropic_fetcher._get_static_model_specs("claude-sonnet-4-5")

        assert "recommended_for" in specs
        assert len(specs["recommended_for"]) > 0
        assert isinstance(specs["recommended_for"], list)

    def test_static_specs_include_best_practices(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that specs include best practices."""
        specs = anthropic_fetcher._get_static_model_specs("claude-haiku-4-5")

        assert "best_practices" in specs
        assert len(specs["best_practices"]) > 0
        assert isinstance(specs["best_practices"], list)


# ============================================================================
# DOCS FALLBACK TESTS
# ============================================================================


class TestDocsFallback:
    """Test suite for docs-based fallback fetching."""

    def test_fetch_from_docs_returns_all_models(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that fetch_from_docs returns all supported models."""
        models = anthropic_fetcher.fetch_from_docs()

        assert len(models) == 3  # Sonnet 4.5, Haiku 4.5, and Opus 4.1
        model_ids = [m.model_id for m in models]
        assert "claude-sonnet-4-5" in model_ids
        assert "claude-haiku-4-5" in model_ids
        assert "claude-opus-4-1" in model_ids

    def test_fetch_from_docs_creates_valid_model_data(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that docs-based models have all required fields."""
        models = anthropic_fetcher.fetch_from_docs()

        for model in models:
            assert model.model_id is not None
            assert model.provider == "anthropic"
            assert model.name is not None
            assert model.api_identifier is not None
            assert model.context_window_input > 0
            # context_window_output can be None for some models
            assert model.context_window_output is None or model.context_window_output > 0
            assert model.knowledge_cutoff is not None
            assert isinstance(model.release_date, date)
            assert model.docs_url.startswith("https://")
            assert len(model.capabilities) > 0
            assert model.input_per_1m > 0
            assert model.output_per_1m > 0
            assert model.cache_write_per_1m > 0
            assert model.cache_read_per_1m > 0
            assert model.source == "anthropic_docs"

    def test_fetch_from_docs_logs_usage_of_static_specs(
        self, anthropic_fetcher: AnthropicFetcher, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that fetch_from_docs logs that it's using static specs."""
        import logging

        caplog.set_level(logging.INFO)
        anthropic_fetcher.fetch_from_docs()

        assert "Using static model specifications" in caplog.text

    def test_fetch_from_docs_preserves_model_order(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that models are returned in expected order."""
        models = anthropic_fetcher.fetch_from_docs()

        model_ids = [m.model_id for m in models]
        expected_order = ["claude-sonnet-4-5", "claude-haiku-4-5", "claude-opus-4-1"]
        assert model_ids == expected_order


# ============================================================================
# MAIN FETCH METHOD TESTS
# ============================================================================


class TestMainFetchMethod:
    """Test suite for main fetch_models() method."""

    def test_fetch_models_uses_docs_by_default(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that fetch_models uses docs (API not yet available)."""
        models = anthropic_fetcher.fetch_models()

        # Should get models from docs
        assert len(models) > 0
        assert all(m.source == "anthropic_docs" for m in models)

    def test_fetch_models_returns_all_claude_models(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that all Claude models are returned."""
        models = anthropic_fetcher.fetch_models()

        model_ids = [m.model_id for m in models]
        assert "claude-sonnet-4-5" in model_ids
        assert "claude-haiku-4-5" in model_ids
        assert "claude-opus-4-1" in model_ids


# ============================================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================================


class TestEdgeCases:
    """Test suite for edge cases and error handling."""

    def test_provider_name_returns_anthropic(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that provider_name property returns correct value."""
        assert anthropic_fetcher.provider_name == "anthropic"

    def test_static_specs_have_consistent_structure(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that all static specs follow the same structure."""
        # Note: 'name' and 'api_identifier' are NOT in static specs
        # They are added when creating ModelData objects
        required_keys = {
            "context_window_input",
            "context_window_output",
            "knowledge_cutoff",
            "release_date",
            "capabilities",
            "pricing",
            "cost_tier",
            "speed_tier",
            "recommended_for",
            "best_practices",
            "notes",
        }

        for model_id in ["claude-sonnet-4-5", "claude-haiku-4-5", "claude-opus-4-1"]:
            specs = anthropic_fetcher._get_static_model_specs(model_id)
            assert specs is not None
            assert required_keys.issubset(set(specs.keys()))
            assert "input_per_1m" in specs["pricing"]
            assert "output_per_1m" in specs["pricing"]
            assert "cache_write_per_1m" in specs["pricing"]
            assert "cache_read_per_1m" in specs["pricing"]

    def test_fetch_from_docs_handles_missing_specs_gracefully(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that fetch_from_docs skips models with missing specs."""
        # Patch to simulate missing spec
        with patch.object(
            anthropic_fetcher, "_get_static_model_specs"
        ) as mock_get_specs:
            mock_get_specs.return_value = None

            models = anthropic_fetcher.fetch_from_docs()

            # Should return empty list when all specs are missing
            assert models == []

    def test_all_models_have_function_calling_capability(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that all Claude models advertise function_calling capability."""
        models = anthropic_fetcher.fetch_from_docs()

        for model in models:
            assert "function_calling" in model.capabilities
            assert "vision" in model.capabilities

    def test_all_models_have_prompt_caching(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that all models have prompt caching pricing."""
        models = anthropic_fetcher.fetch_from_docs()

        for model in models:
            assert model.cache_write_per_1m > 0
            assert model.cache_read_per_1m > 0
            # Cache read should be cheaper than cache write
            assert model.cache_read_per_1m < model.cache_write_per_1m

    def test_model_pricing_reflects_capability_tiers(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that pricing aligns with model capabilities."""
        models = anthropic_fetcher.fetch_from_docs()

        # Get models by ID
        models_dict = {m.model_id: m for m in models}

        haiku = models_dict["claude-haiku-4-5"]
        sonnet = models_dict["claude-sonnet-4-5"]
        opus = models_dict["claude-opus-4-1"]

        # Haiku should be cheapest (budget tier)
        assert haiku.input_per_1m < sonnet.input_per_1m < opus.input_per_1m
        assert haiku.output_per_1m < sonnet.output_per_1m < opus.output_per_1m
        assert haiku.cost_tier == "budget"
        assert sonnet.cost_tier == "mid-tier"
        assert opus.cost_tier == "premium"

    def test_all_models_have_200k_context(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that all Claude models have 200k input context window."""
        models = anthropic_fetcher.fetch_from_docs()

        for model in models:
            assert model.context_window_input == 200000
            # Output context may vary (some models have None, some 16000)

    def test_sonnet_is_recommended_for_production(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that Sonnet 4.5 is recommended for production workloads."""
        models = anthropic_fetcher.fetch_from_docs()

        sonnet = next(m for m in models if m.model_id == "claude-sonnet-4-5")
        assert sonnet.cost_tier == "mid-tier"
        assert sonnet.speed_tier == "balanced"
        assert any("Production" in rec for rec in sonnet.recommended_for)

    def test_haiku_is_fastest_model(
        self, anthropic_fetcher: AnthropicFetcher
    ) -> None:
        """Test that Haiku is marked as fastest model."""
        models = anthropic_fetcher.fetch_from_docs()

        haiku = next(m for m in models if m.model_id == "claude-haiku-4-5")
        assert haiku.speed_tier == "fast"
        assert haiku.cost_tier == "budget"
