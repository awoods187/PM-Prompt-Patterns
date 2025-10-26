# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
Test Model Registry Validation

Validates the ModelRegistry structure, data integrity, and helper methods.
These tests do NOT require API keys - they test the registry data structure itself.

Usage:
    pytest tests/test_model_registry.py
"""

from dataclasses import FrozenInstanceError
from datetime import date, timedelta

import pytest

from models.registry import ModelRegistry, ModelSpec, Provider


class TestRegistryStructure:
    """Test basic registry structure and constants."""

    def test_all_providers_have_verification_sources(self):
        """Verify each provider has a verification source URL."""
        for provider in Provider:
            assert (
                provider in ModelRegistry.VERIFICATION_SOURCES
            ), f"Missing verification source for {provider.value}"

            url = ModelRegistry.VERIFICATION_SOURCES[provider]
            assert url.startswith(
                "https://"
            ), f"Verification URL for {provider.value} must use HTTPS"

    def test_registry_has_models(self):
        """Verify registry contains at least one model per provider."""
        all_models = ModelRegistry.get_all_current_models()

        assert len(all_models) > 0, "Registry has no models"

        # Check we have at least one model per provider
        providers_with_models = {spec.provider for spec in all_models.values()}

        for provider in Provider:
            assert provider in providers_with_models, f"No models found for {provider.value}"

    def test_registry_class_attributes_exist(self):
        """Verify expected class attributes are present."""
        # Claude models
        assert hasattr(ModelRegistry, "CLAUDE_SONNET_4_5")
        assert hasattr(ModelRegistry, "CLAUDE_HAIKU_4_5")
        assert hasattr(ModelRegistry, "CLAUDE_OPUS_4_1")

        # Gemini models
        assert hasattr(ModelRegistry, "GEMINI_2_5_PRO")
        assert hasattr(ModelRegistry, "GEMINI_2_5_FLASH")
        assert hasattr(ModelRegistry, "GEMINI_2_5_FLASH_LITE")

        # OpenAI models
        assert hasattr(ModelRegistry, "GPT_4O")
        assert hasattr(ModelRegistry, "GPT_4O_MINI")

    def test_deprecated_models_dict_exists(self):
        """Verify deprecated models dict is present and structured correctly."""
        assert hasattr(ModelRegistry, "_DEPRECATED")
        assert isinstance(ModelRegistry._DEPRECATED, dict)

        # Each deprecated model should have a replacement suggestion
        for old_id, suggestion in ModelRegistry._DEPRECATED.items():
            assert isinstance(old_id, str), "Deprecated model ID must be string"
            assert isinstance(suggestion, str), "Replacement suggestion must be string"
            assert len(suggestion) > 0, f"Empty replacement for {old_id}"


class TestModelSpecValidation:
    """Test that all ModelSpec instances are valid."""

    def test_all_specs_are_frozen_dataclasses(self):
        """Verify all ModelSpec instances are immutable."""
        for key, spec in ModelRegistry.get_all_current_models().items():
            assert isinstance(spec, ModelSpec), f"{key} is not a ModelSpec instance"

            # Frozen dataclasses should raise FrozenInstanceError on assignment
            with pytest.raises(FrozenInstanceError):
                spec.api_identifier = "should_fail"

    def test_all_required_fields_present(self):
        """Verify all ModelSpec instances have required fields populated."""
        required_fields = [
            "provider",
            "name",
            "api_identifier",
            "context_window_input",
            "input_price_per_1m",
            "output_price_per_1m",
            "knowledge_cutoff",
            "last_verified",
            "docs_url",
        ]

        for key, spec in ModelRegistry.get_all_current_models().items():
            for field in required_fields:
                value = getattr(spec, field, None)
                assert value is not None, f"{key} missing required field: {field}"

                # String fields should not be empty
                if isinstance(value, str):
                    assert len(value) > 0, f"{key} has empty {field}"

    def test_api_identifiers_are_unique(self):
        """Verify no two models share the same API identifier."""
        identifiers: set[str] = set()
        duplicates = []

        for key, spec in ModelRegistry.get_all_current_models().items():
            if spec.api_identifier in identifiers:
                duplicates.append((key, spec.api_identifier))
            identifiers.add(spec.api_identifier)

        assert len(duplicates) == 0, f"Duplicate API identifiers found: {duplicates}"

    def test_pricing_is_positive(self):
        """Verify all pricing is positive (no free models)."""
        for key, spec in ModelRegistry.get_all_current_models().items():
            assert (
                spec.input_price_per_1m > 0
            ), f"{key} has non-positive input price: {spec.input_price_per_1m}"
            assert (
                spec.output_price_per_1m > 0
            ), f"{key} has non-positive output price: {spec.output_price_per_1m}"

    def test_context_windows_positive(self):
        """Verify context windows are positive integers."""
        for key, spec in ModelRegistry.get_all_current_models().items():
            assert (
                spec.context_window_input > 0
            ), f"{key} has non-positive input context: {spec.context_window_input}"

            if spec.context_window_output is not None:
                assert (
                    spec.context_window_output > 0
                ), f"{key} has non-positive output context: {spec.context_window_output}"

    def test_last_verified_is_date(self):
        """Verify last_verified is a date object (not datetime or string)."""
        for key, spec in ModelRegistry.get_all_current_models().items():
            assert isinstance(
                spec.last_verified, date
            ), f"{key} last_verified is not a date object: {type(spec.last_verified)}"

    def test_docs_urls_are_valid(self):
        """Verify all documentation URLs are properly formatted."""
        for key, spec in ModelRegistry.get_all_current_models().items():
            assert spec.docs_url.startswith(
                "http"
            ), f"{key} docs_url doesn't start with http: {spec.docs_url}"

            # Should use HTTPS
            assert spec.docs_url.startswith(
                "https://"
            ), f"{key} docs_url should use HTTPS: {spec.docs_url}"


class TestRegistryHelperMethods:
    """Test registry helper methods work correctly."""

    def test_get_all_current_models(self):
        """Verify get_all_current_models returns dict of ModelSpec."""
        all_models = ModelRegistry.get_all_current_models()

        assert isinstance(all_models, dict)
        assert len(all_models) > 0

        for key, spec in all_models.items():
            assert isinstance(key, str)
            assert isinstance(spec, ModelSpec)

    def test_get_spec(self):
        """Verify get_spec retrieves models by key."""
        # Test valid keys
        claude = ModelRegistry.get_spec("claude-sonnet-4.5")
        assert claude is not None
        assert claude.provider == Provider.ANTHROPIC

        gemini = ModelRegistry.get_spec("gemini-2.5-flash")
        assert gemini is not None
        assert gemini.provider == Provider.GOOGLE

        gpt = ModelRegistry.get_spec("gpt-4o")
        assert gpt is not None
        assert gpt.provider == Provider.OPENAI

        # Test invalid key
        invalid = ModelRegistry.get_spec("nonexistent-model")
        assert invalid is None

    def test_get_by_provider(self):
        """Verify get_by_provider filters correctly."""
        # Test Anthropic
        claude_models = ModelRegistry.get_by_provider(Provider.ANTHROPIC)
        assert len(claude_models) >= 3  # Sonnet, Haiku, Opus
        for spec in claude_models.values():
            assert spec.provider == Provider.ANTHROPIC

        # Test Google
        gemini_models = ModelRegistry.get_by_provider(Provider.GOOGLE)
        assert len(gemini_models) >= 3  # Pro, Flash, Flash-Lite
        for spec in gemini_models.values():
            assert spec.provider == Provider.GOOGLE

        # Test OpenAI
        openai_models = ModelRegistry.get_by_provider(Provider.OPENAI)
        assert len(openai_models) >= 2  # GPT-4o, GPT-4o mini
        for spec in openai_models.values():
            assert spec.provider == Provider.OPENAI

    def test_is_deprecated(self):
        """Verify is_deprecated correctly identifies deprecated models."""
        # Test known deprecated models
        assert ModelRegistry.is_deprecated("claude-3-5-sonnet-20241022") is True
        assert ModelRegistry.is_deprecated("gemini-1.5-pro-002") is True
        assert ModelRegistry.is_deprecated("gpt-4-turbo") is True

        # Test current models are NOT deprecated
        assert ModelRegistry.is_deprecated("claude-sonnet-4-5-20250929") is False
        assert ModelRegistry.is_deprecated("gemini-2.5-pro") is False
        assert ModelRegistry.is_deprecated("gpt-4o") is False

    def test_get_replacement(self):
        """Verify get_replacement suggests correct replacements."""
        # Test getting replacement for deprecated model
        replacement = ModelRegistry.get_replacement("claude-3-5-sonnet-20241022")
        assert replacement is not None
        assert "CLAUDE_SONNET" in replacement or "claude-sonnet-4" in replacement.lower()

        # Test getting replacement for non-deprecated model
        no_replacement = ModelRegistry.get_replacement("claude-sonnet-4-5-20250929")
        assert no_replacement is None

    def test_get_recommended_model(self):
        """Verify get_recommended_model returns sensible defaults."""
        # Each provider should have a recommendation
        claude = ModelRegistry.get_recommended_model(Provider.ANTHROPIC)
        assert claude.provider == Provider.ANTHROPIC
        assert isinstance(claude, ModelSpec)

        gemini = ModelRegistry.get_recommended_model(Provider.GOOGLE)
        assert gemini.provider == Provider.GOOGLE
        assert isinstance(gemini, ModelSpec)

        gpt = ModelRegistry.get_recommended_model(Provider.OPENAI)
        assert gpt.provider == Provider.OPENAI
        assert isinstance(gpt, ModelSpec)


class TestStalenessDetection:
    """Test staleness detection for model verifications."""

    def test_no_stale_models_by_default(self):
        """Verify no models are stale (>90 days since verification)."""
        stale_threshold = date.today() - timedelta(days=90)
        stale_models = []

        for key, spec in ModelRegistry.get_all_current_models().items():
            if spec.last_verified < stale_threshold:
                days_old = (date.today() - spec.last_verified).days
                stale_models.append((key, days_old, spec.last_verified))

        if stale_models:
            warnings = "\n".join(
                f"  - {key}: {days} days old (verified: {verified})"
                for key, days, verified in stale_models
            )
            pytest.fail(
                f"\n⚠️  STALE MODELS DETECTED (>90 days since verification):\n\n"
                f"{warnings}\n\n"
                f"Action Required:\n"
                f"  1. Check official docs: See VERIFICATION_SOURCES in registry.py\n"
                f"  2. Update ModelSpec if changed\n"
                f"  3. Update last_verified date\n"
                f"  4. See UPDATING_MODELS.md for full procedure\n"
            )

    def test_warn_approaching_stale(self):
        """Warn if models approaching staleness (60-90 days)."""
        warn_threshold = date.today() - timedelta(days=60)
        stale_threshold = date.today() - timedelta(days=90)
        warning_models = []

        for key, spec in ModelRegistry.get_all_current_models().items():
            if warn_threshold <= spec.last_verified < stale_threshold:
                days_old = (date.today() - spec.last_verified).days
                warning_models.append((key, days_old, spec.last_verified))

        if warning_models:
            warnings = "\n".join(
                f"  - {key}: {days} days old (verified: {verified})"
                for key, days, verified in warning_models
            )
            # Don't fail, just print warning
            print(
                f"\n⚠️  Models approaching staleness (60-90 days):\n\n"
                f"{warnings}\n\n"
                f"Consider updating soon - see UPDATING_MODELS.md\n"
            )


class TestDeprecatedModelsComplete:
    """Test deprecated models list is comprehensive."""

    def test_no_old_claude_3_models_in_current(self):
        """Verify no Claude 3.x models in current registry."""
        for key, spec in ModelRegistry.get_all_current_models().items():
            if spec.provider == Provider.ANTHROPIC:
                # Should NOT contain "claude-3" in identifier
                assert (
                    "claude-3" not in spec.api_identifier.lower()
                ), f"{key} appears to be Claude 3.x (should be 4.x or later)"

    def test_no_old_gemini_1_models_in_current(self):
        """Verify no Gemini 1.x models in current registry."""
        for key, spec in ModelRegistry.get_all_current_models().items():
            if spec.provider == Provider.GOOGLE:
                # Should NOT contain "gemini-1" in identifier
                assert (
                    "gemini-1" not in spec.api_identifier.lower()
                ), f"{key} appears to be Gemini 1.x (should be 2.x or later)"

    def test_deprecated_list_has_common_old_models(self):
        """Verify deprecated list includes commonly-used old models."""
        deprecated = ModelRegistry._DEPRECATED

        # Should have old Claude models
        assert any(
            "claude-3-5" in k.lower() for k in deprecated.keys()
        ), "Missing Claude 3.5 models in deprecated list"

        # Should have old Gemini models
        assert any(
            "gemini-1.5" in k.lower() for k in deprecated.keys()
        ), "Missing Gemini 1.5 models in deprecated list"

        # Should have old GPT models
        assert any(
            "gpt-3.5" in k.lower() or "gpt-4-turbo" in k.lower() for k in deprecated.keys()
        ), "Missing old GPT models in deprecated list"


class TestConvenienceExports:
    """Test convenience export constants."""

    def test_convenience_exports_exist(self):
        """Verify convenience exports are available."""
        from models.registry import (
            CLAUDE_HAIKU,
            CLAUDE_OPUS,
            CLAUDE_SONNET,
            GEMINI_FLASH,
            GEMINI_FLASH_LITE,
            GEMINI_PRO,
            GPT_4O,
            GPT_4O_MINI,
        )

        # All should be ModelSpec instances
        for export in [
            CLAUDE_SONNET,
            CLAUDE_HAIKU,
            CLAUDE_OPUS,
            GEMINI_PRO,
            GEMINI_FLASH,
            GEMINI_FLASH_LITE,
            GPT_4O,
            GPT_4O_MINI,
        ]:
            assert isinstance(export, ModelSpec)

    def test_convenience_exports_match_registry(self):
        """Verify convenience exports point to correct registry entries."""
        from models.registry import (
            CLAUDE_HAIKU,
            CLAUDE_OPUS,
            CLAUDE_SONNET,
            GEMINI_FLASH,
            GEMINI_PRO,
            GPT_4O,
            GPT_4O_MINI,
        )

        assert CLAUDE_SONNET == ModelRegistry.CLAUDE_SONNET_4_5
        assert CLAUDE_HAIKU == ModelRegistry.CLAUDE_HAIKU_4_5
        assert CLAUDE_OPUS == ModelRegistry.CLAUDE_OPUS_4_1

        assert GEMINI_PRO == ModelRegistry.GEMINI_2_5_PRO
        assert GEMINI_FLASH == ModelRegistry.GEMINI_2_5_FLASH

        assert GPT_4O == ModelRegistry.GPT_4O
        assert GPT_4O_MINI == ModelRegistry.GPT_4O_MINI


class TestProviderConsistency:
    """Test provider-specific consistency rules."""

    def test_anthropic_models_use_claude_prefix(self):
        """Verify all Anthropic models start with 'claude-'."""
        for key, spec in ModelRegistry.get_by_provider(Provider.ANTHROPIC).items():
            assert spec.api_identifier.startswith(
                "claude-"
            ), f"Anthropic model {key} doesn't start with 'claude-': {spec.api_identifier}"

    def test_google_models_use_gemini_prefix(self):
        """Verify all Google models start with 'gemini-'."""
        for key, spec in ModelRegistry.get_by_provider(Provider.GOOGLE).items():
            assert spec.api_identifier.startswith(
                "gemini-"
            ), f"Google model {key} doesn't start with 'gemini-': {spec.api_identifier}"

    def test_openai_models_use_gpt_prefix(self):
        """Verify all OpenAI models start with 'gpt-'."""
        for key, spec in ModelRegistry.get_by_provider(Provider.OPENAI).items():
            assert spec.api_identifier.startswith(
                "gpt-"
            ), f"OpenAI model {key} doesn't start with 'gpt-': {spec.api_identifier}"


if __name__ == "__main__":
    """Run tests with verbose output."""
    pytest.main([__file__, "-v"])
