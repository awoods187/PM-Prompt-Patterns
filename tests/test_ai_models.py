# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Comprehensive tests for the new ai_models system.

Tests YAML loading, pricing service, capabilities, and model registry.
"""

from datetime import date

import pytest

from ai_models import (
    CapabilityValidator,
    ModelCapability,
    ModelRegistry,
    PricingService,
    get_model,
    has_function_calling,
    has_prompt_caching,
    has_vision,
    list_models,
    list_providers,
)


class TestModelRegistry:
    """Test the new YAML-based model registry."""

    def test_registry_loads_models(self) -> None:
        """Registry should load all YAML model definitions."""
        models = ModelRegistry.get_all()
        assert len(models) >= 8, "Should load all 8 model definitions"

    def test_get_model_by_id(self) -> None:
        """Should retrieve model by ID."""
        model = ModelRegistry.get("claude-sonnet-4-5")
        assert model is not None
        assert model.name == "Claude Sonnet 4.5"
        assert model.api_identifier == "claude-sonnet-4-5-20250929"

    def test_get_model_not_found(self) -> None:
        """Should return None for unknown model."""
        model = ModelRegistry.get("nonexistent-model")
        assert model is None

    def test_get_by_provider(self) -> None:
        """Should filter models by provider."""
        anthropic_models = ModelRegistry.get_by_provider("anthropic")
        assert len(anthropic_models) == 3
        assert all(m.provider == "anthropic" for m in anthropic_models)

        openai_models = ModelRegistry.get_by_provider("openai")
        assert len(openai_models) == 8  # Updated for new OpenAI model lineup (Nov 2025)

        google_models = ModelRegistry.get_by_provider("google")
        assert len(google_models) == 3

    def test_model_metadata(self) -> None:
        """Model metadata should be correctly loaded."""
        model = ModelRegistry.get("claude-haiku-4-5")
        assert model.metadata.context_window_input == 200_000  # type: ignore[union-attr]
        assert model.metadata.knowledge_cutoff == "February 2025"  # type: ignore[union-attr]
        assert isinstance(model.metadata.last_verified, date)  # type: ignore[union-attr]
        assert "claude.com" in model.metadata.docs_url  # type: ignore[union-attr]

    def test_convenience_functions(self) -> None:
        """Convenience functions should work."""
        model = get_model("gpt-4o")
        assert model is not None
        assert model.provider == "openai"

        all_models = list_models()
        assert len(all_models) >= 8
        assert "claude-sonnet-4-5" in all_models

        providers = list_providers()
        assert "anthropic" in providers
        assert "openai" in providers
        assert "google" in providers


class TestPricingService:
    """Test pricing service functionality."""

    def test_pricing_service_loads(self) -> None:
        """Pricing service should load from YAML."""
        service = PricingService()
        pricing = service.get_pricing("claude-sonnet-4-5")
        assert pricing is not None
        assert pricing.input_per_1m == 3.00
        assert pricing.output_per_1m == 15.00

    def test_pricing_matches_registry(self) -> None:
        """Pricing in service should match model registry."""
        model = ModelRegistry.get("claude-haiku-4-5")
        service = PricingService()
        pricing = service.get_pricing("claude-haiku-4-5")

        assert pricing.input_per_1m == model.pricing.input_per_1m  # type: ignore[union-attr]
        assert pricing.output_per_1m == model.pricing.output_per_1m  # type: ignore[union-attr]

    def test_calculate_cost_basic(self) -> None:
        """Should calculate basic cost correctly."""
        service = PricingService()
        cost = service.calculate_cost(
            "claude-haiku-4-5", input_tokens=1_000_000, output_tokens=100_000
        )
        # (1M * $1.00/1M) + (100k * $5.00/1M) = $1.00 + $0.50 = $1.50
        assert cost == 1.50

    def test_calculate_cost_with_caching(self) -> None:
        """Should calculate cost with caching correctly."""
        service = PricingService()
        cost = service.calculate_cost(
            "claude-sonnet-4-5",
            input_tokens=1_000_000,
            output_tokens=500_000,
            cached_input_tokens=900_000,
        )
        # Uncached input: 100k * $3.00/1M = $0.30
        # Cached input: 900k * $0.30/1M = $0.27
        # Output: 500k * $15.00/1M = $7.50
        # Total: $0.30 + $0.27 + $7.50 = $8.07
        assert abs(cost - 8.07) < 0.01

    def test_pricing_not_found_raises(self) -> None:
        """Should raise ValueError for unknown model."""
        service = PricingService()
        with pytest.raises(ValueError, match="Pricing not found"):
            service.calculate_cost("nonexistent-model", 1000, 500)

    def test_all_models_have_pricing(self) -> None:
        """All models should have pricing information."""
        service = PricingService()
        models = ModelRegistry.get_all()

        for model_id in models:
            pricing = service.get_pricing(model_id)
            assert pricing is not None, f"{model_id} missing pricing"
            assert pricing.input_per_1m >= 0
            assert pricing.output_per_1m >= 0


class TestCapabilities:
    """Test capability system."""

    def test_capability_validator_loads(self) -> None:
        """CapabilityValidator should load capabilities from YAML."""
        caps = CapabilityValidator.get_capabilities("claude-sonnet-4-5")
        assert len(caps) > 0
        assert ModelCapability.TEXT_INPUT in caps
        assert ModelCapability.VISION in caps

    def test_has_capability(self) -> None:
        """Should check capabilities correctly."""
        assert CapabilityValidator.has_capability("claude-sonnet-4-5", ModelCapability.VISION)
        assert CapabilityValidator.has_capability(
            "claude-haiku-4-5", ModelCapability.FUNCTION_CALLING
        )

    def test_model_has_capability_method(self) -> None:
        """Model.has_capability() should work."""
        model = ModelRegistry.get("gpt-4o")
        assert model.has_capability(ModelCapability.VISION)  # type: ignore[union-attr]
        assert model.has_capability("vision")  # type: ignore[union-attr]  # String also works
        assert model.has_capability(ModelCapability.FUNCTION_CALLING)  # type: ignore[union-attr]

    def test_model_has_all_capabilities(self) -> None:
        """Model.has_all_capabilities() should work."""
        model = ModelRegistry.get("claude-sonnet-4-5")
        assert model.has_all_capabilities(  # type: ignore[union-attr]
            [
                ModelCapability.VISION,
                ModelCapability.FUNCTION_CALLING,
                ModelCapability.PROMPT_CACHING,
            ]
        )

    def test_filter_by_capability(self) -> None:
        """Should filter models by capability."""
        vision_models = ModelRegistry.filter_by_capability(ModelCapability.VISION)
        assert len(vision_models) > 0
        assert all(m.has_capability(ModelCapability.VISION) for m in vision_models)

        caching_models = ModelRegistry.filter_by_capability("prompt_caching")
        assert len(caching_models) >= 4  # Claude models + Gemini models

    def test_convenience_functions(self) -> None:
        """Capability convenience functions should work."""
        assert has_vision("claude-sonnet-4-5")
        assert has_function_calling("gpt-4o")
        assert has_prompt_caching("claude-haiku-4-5")

    def test_gemini_flash_lite_limited_capabilities(self) -> None:
        """Gemini 2.5 Flash-Lite should have limited capabilities (free tier)."""
        model = ModelRegistry.get("gemini-2-5-flash-lite")
        assert model.has_capability(ModelCapability.VISION)  # type: ignore[union-attr]
        assert not model.has_capability(ModelCapability.FUNCTION_CALLING)  # type: ignore[union-attr]
        assert not model.has_capability(ModelCapability.PROMPT_CACHING)  # type: ignore[union-attr]


class TestModelOptimization:
    """Test optimization guidance."""

    def test_cost_tier_filtering(self) -> None:
        """Should filter by cost tier."""
        budget = ModelRegistry.filter_by_cost_tier("budget")
        assert len(budget) >= 3  # Haiku, 4o-mini, Flash, Flash-Lite

        premium = ModelRegistry.filter_by_cost_tier("premium")
        assert len(premium) >= 1  # Opus

    def test_optimization_loaded(self) -> None:
        """Optimization data should be loaded."""
        model = ModelRegistry.get("claude-sonnet-4-5")
        assert len(model.optimization.recommended_for) > 0  # type: ignore[union-attr]
        assert len(model.optimization.best_practices) > 0  # type: ignore[union-attr]
        assert model.optimization.cost_tier == "mid-tier"  # type: ignore[union-attr]
        assert model.optimization.speed_tier == "balanced"  # type: ignore[union-attr]

    def test_budget_model_recommendations(self) -> None:
        """Budget models should have appropriate recommendations."""
        haiku = ModelRegistry.get("claude-haiku-4-5")
        assert haiku.optimization.cost_tier == "budget"  # type: ignore[union-attr]
        assert haiku.optimization.speed_tier == "fast"  # type: ignore[union-attr]
        assert any("classification" in rec.lower() for rec in haiku.optimization.recommended_for)  # type: ignore[union-attr]


class TestModelIntegration:
    """Integration tests combining multiple features."""

    def test_full_workflow_claude_sonnet(self) -> None:
        """Test complete workflow with Claude Sonnet."""
        # Get model
        model = ModelRegistry.get("claude-sonnet-4-5")
        assert model is not None

        # Check capabilities
        assert model.has_capability(ModelCapability.VISION)
        assert model.has_capability(ModelCapability.PROMPT_CACHING)
        assert model.has_capability(ModelCapability.FUNCTION_CALLING)

        # Calculate cost
        cost = model.calculate_cost(
            input_tokens=10_000, output_tokens=2_000, cached_input_tokens=5_000
        )
        # Uncached: 5k * $3/1M = $0.015
        # Cached: 5k * $0.30/1M = $0.0015
        # Output: 2k * $15/1M = $0.03
        # Total: ~$0.0465
        assert 0.046 < cost < 0.047

        # Check optimization
        assert "Production" in str(model.optimization.recommended_for)
        assert len(model.optimization.best_practices) > 3

    def test_model_selection_by_requirements(self) -> None:
        """Test selecting model based on requirements."""
        # Need: budget + vision + function calling
        budget_models = ModelRegistry.filter_by_cost_tier("budget")
        vision_models = [m for m in budget_models if m.has_capability(ModelCapability.VISION)]
        func_models = [
            m for m in vision_models if m.has_capability(ModelCapability.FUNCTION_CALLING)
        ]

        # Should find: Haiku, 4o-mini, Flash
        assert len(func_models) >= 2
        model_ids = [m.model_id for m in func_models]
        assert "claude-haiku-4-5" in model_ids or "gpt-4o-mini" in model_ids

    def test_cost_comparison(self) -> None:
        """Compare costs across models for same task."""
        models = [
            ModelRegistry.get("claude-haiku-4-5"),
            ModelRegistry.get("claude-sonnet-4-5"),
            ModelRegistry.get("gpt-4o-mini"),
        ]

        costs = []
        for model in models:
            cost = model.calculate_cost(input_tokens=100_000, output_tokens=10_000)  # type: ignore[union-attr]
            costs.append((model.model_id, cost))  # type: ignore[union-attr]

        # Verify costs are positive and differ
        assert all(cost > 0 for _, cost in costs)
        # Haiku and 4o-mini should be cheaper than Sonnet
        haiku_cost = next(c for m, c in costs if "haiku" in m)
        sonnet_cost = next(c for m, c in costs if "sonnet" in m)
        assert haiku_cost < sonnet_cost


class TestPricingConsistency:
    """Ensure new system maintains pricing accuracy from Phase 1."""

    def test_claude_haiku_correct_pricing(self) -> None:
        """Claude Haiku should have correct pricing (was 4x wrong before)."""
        model = ModelRegistry.get("claude-haiku-4-5")
        # Phase 1 identified this error - ensure it's fixed in new system
        assert model.pricing.input_per_1m == 1.00, "Haiku input should be $1.00 (not $0.25)"  # type: ignore[union-attr]
        assert model.pricing.output_per_1m == 5.00, "Haiku output should be $5.00 (not $1.25)"  # type: ignore[union-attr]

    def test_all_pricing_positive(self) -> None:
        """All pricing should be non-negative."""
        models = ModelRegistry.get_all()
        for model in models.values():
            assert model.pricing.input_per_1m >= 0
            assert model.pricing.output_per_1m >= 0

    def test_output_more_expensive_than_input(self) -> None:
        """Output should generally cost more than input (except free models)."""
        models = ModelRegistry.get_all()
        for model in models.values():
            # Skip free models
            if model.pricing.input_per_1m == 0 and model.pricing.output_per_1m == 0:
                continue

            assert (
                model.pricing.output_per_1m >= model.pricing.input_per_1m
            ), f"{model.model_id}: output should cost >= input"


class TestYAMLSchemaCompliance:
    """Verify YAML files comply with schema."""

    def test_all_models_have_required_fields(self) -> None:
        """All models should have required schema fields."""
        models = ModelRegistry.get_all()

        for model in models.values():
            # Required string fields
            assert model.model_id
            assert model.provider
            assert model.name
            assert model.api_identifier

            # Metadata
            assert model.metadata.context_window_input > 0
            assert model.metadata.knowledge_cutoff
            assert model.metadata.docs_url.startswith("http")

            # Pricing
            assert model.pricing.input_per_1m >= 0
            assert model.pricing.output_per_1m >= 0

            # Capabilities
            assert len(model.capabilities) > 0

    def test_model_ids_lowercase_hyphens(self) -> None:
        """Model IDs should be lowercase with hyphens."""
        models = ModelRegistry.get_all()
        for model_id in models:
            assert model_id == model_id.lower(), f"{model_id} should be lowercase"
            assert "_" not in model_id, f"{model_id} should use hyphens not underscores"

    def test_providers_valid(self) -> None:
        """Providers should be one of the expected values."""
        valid_providers = {"anthropic", "openai", "google"}
        models = ModelRegistry.get_all()

        for model in models.values():
            assert (
                model.provider in valid_providers
            ), f"{model.model_id} has invalid provider: {model.provider}"

    def test_cost_tiers_valid(self) -> None:
        """Cost tiers should be valid values."""
        valid_tiers = {"budget", "mid-tier", "premium"}
        models = ModelRegistry.get_all()

        for model in models.values():
            assert (
                model.optimization.cost_tier in valid_tiers
            ), f"{model.model_id} has invalid cost tier: {model.optimization.cost_tier}"

    def test_speed_tiers_valid(self) -> None:
        """Speed tiers should be valid values."""
        valid_tiers = {"fast", "balanced", "thorough"}
        models = ModelRegistry.get_all()

        for model in models.values():
            assert (
                model.optimization.speed_tier in valid_tiers
            ), f"{model.model_id} has invalid speed tier: {model.optimization.speed_tier}"


class TestCacheClear:
    """Test cache clearing functionality."""

    def test_registry_cache_clear(self) -> None:
        """Registry cache should clear and reload."""
        # Load once
        model1 = ModelRegistry.get("claude-sonnet-4-5")
        assert model1 is not None

        # Clear cache
        ModelRegistry.clear_cache()

        # Should reload
        model2 = ModelRegistry.get("claude-sonnet-4-5")
        assert model2 is not None
        assert model2.model_id == model1.model_id

    def test_capability_cache_clear(self) -> None:
        """Capability cache should clear and reload."""
        caps1 = CapabilityValidator.get_capabilities("gpt-4o")
        assert len(caps1) > 0

        CapabilityValidator.clear_cache()

        caps2 = CapabilityValidator.get_capabilities("gpt-4o")
        assert caps1 == caps2


class TestAvailabilityFiltering:
    """Test model availability filtering by date."""

    def test_get_available_models_defaults_to_today(self) -> None:
        """Should return models available as of today."""
        available = ModelRegistry.get_available_models()
        assert len(available) > 0
        # All models should have release_date <= today
        today = date.today()
        for model in available:
            assert model.metadata.release_date <= today

    def test_get_available_models_with_past_date(self) -> None:
        """Should return only models released by a specific date."""
        # August 1, 2024 - should only have gpt-4o-mini and gpt-4o
        past_date = date(2024, 8, 1)
        available = ModelRegistry.get_available_models(past_date)

        model_ids = {m.model_id for m in available}
        # Should include gpt-4o-mini (July 18, 2024)
        assert "gpt-4o-mini" in model_ids
        # Should NOT include GPT-5 (August 2025)
        assert "gpt-5" not in model_ids

    def test_get_available_models_with_future_date(self) -> None:
        """Should return all models if date is in future."""
        future_date = date(2026, 1, 1)
        available = ModelRegistry.get_available_models(future_date)
        all_models = ModelRegistry.get_all()
        # Should get all models
        assert len(available) == len(all_models)

    def test_get_available_by_provider(self) -> None:
        """Should filter available models by provider."""
        # Get OpenAI models available today
        openai_models = ModelRegistry.get_available_by_provider("openai")
        assert len(openai_models) > 0
        # All should be from OpenAI
        for model in openai_models:
            assert model.provider.lower() == "openai"
        # All should be released
        today = date.today()
        for model in openai_models:
            assert model.metadata.release_date <= today

    def test_get_available_by_provider_with_past_date(self) -> None:
        """Should get provider models available as of a date."""
        # August 1, 2024
        past_date = date(2024, 8, 1)
        openai_models = ModelRegistry.get_available_by_provider("openai", past_date)

        model_ids = {m.model_id for m in openai_models}
        # Should include older models
        assert "gpt-4o-mini" in model_ids
        # Should NOT include newer models
        assert "gpt-5" not in model_ids

    def test_get_latest_model_openai(self) -> None:
        """Should get the most recent OpenAI model."""
        latest = ModelRegistry.get_latest_model("openai")
        assert latest is not None
        # As of Nov 2025, should be GPT-5 or GPT-5 mini (both released August 7, 2025)
        assert latest.model_id in ["gpt-5", "gpt-5-mini"]
        assert latest.metadata.release_date == date(2025, 8, 7)

    def test_get_latest_model_anthropic(self) -> None:
        """Should get the most recent Anthropic model."""
        latest = ModelRegistry.get_latest_model("anthropic")
        assert latest is not None
        # Should be Claude Opus 4.1 (Oct 2025) or Sonnet/Haiku 4.5 (Sept 2025)
        assert latest.model_id in ["claude-opus-4-1", "claude-sonnet-4-5", "claude-haiku-4-5"]

    def test_get_latest_model_with_past_date(self) -> None:
        """Should get latest model as of a specific date."""
        # August 10, 2024
        past_date = date(2024, 8, 10)
        latest = ModelRegistry.get_latest_model("openai", past_date)
        assert latest is not None
        # Should be gpt-4o (August 6, 2024), not GPT-5
        assert latest.model_id == "gpt-4o"

    def test_get_latest_model_unknown_provider(self) -> None:
        """Should return None for unknown provider."""
        latest = ModelRegistry.get_latest_model("unknown-provider")
        assert latest is None

    def test_convenience_functions_available(self) -> None:
        """Convenience functions should be available at module level."""
        from ai_models import get_available_models, get_latest_model

        # Test they work
        available = get_available_models()
        assert len(available) > 0

        latest = get_latest_model("openai")
        assert latest is not None
