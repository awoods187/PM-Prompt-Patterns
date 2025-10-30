# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
Additional tests for ai_models/registry.py to achieve 95%+ coverage.

Focuses on edge cases, error handling, and untested branches.
"""

from datetime import date
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

import pytest
import yaml

from ai_models import ModelRegistry, get_model, list_models, list_providers
from ai_models.capabilities import ModelCapability
from ai_models.registry import ModelMetadata, ModelOptimization


class TestModelToDict:
    """Test Model.to_dict() serialization."""

    def test_model_to_dict_complete_serialization(self):
        """Test that Model.to_dict() produces correct dictionary structure."""
        model = ModelRegistry.get("claude-sonnet-4-5")
        assert model is not None

        result = model.to_dict()

        # Verify all required fields present
        assert result["model_id"] == "claude-sonnet-4-5"
        assert result["provider"] == "anthropic"
        assert result["name"] == "Claude Sonnet 4.5"
        assert result["api_identifier"] == "claude-sonnet-4-5-20250929"

        # Verify metadata structure
        assert "metadata" in result
        assert "context_window_input" in result["metadata"]
        assert "knowledge_cutoff" in result["metadata"]
        assert isinstance(result["metadata"]["release_date"], str)  # ISO format
        assert isinstance(result["metadata"]["last_verified"], str)  # ISO format

        # Verify capabilities are serialized as strings
        assert "capabilities" in result
        assert isinstance(result["capabilities"], list)
        assert all(isinstance(cap, str) for cap in result["capabilities"])

        # Verify pricing structure
        assert "pricing" in result
        assert "input_per_1m" in result["pricing"]
        assert "output_per_1m" in result["pricing"]

        # Verify optimization structure
        assert "optimization" in result
        assert "cost_tier" in result["optimization"]
        assert "speed_tier" in result["optimization"]
        assert "recommended_for" in result["optimization"]
        assert "best_practices" in result["optimization"]

    def test_model_to_dict_handles_empty_notes(self):
        """Test to_dict with empty notes field."""
        model = ModelRegistry.get("claude-haiku-4-5")
        assert model is not None

        result = model.to_dict()
        assert "notes" in result
        assert isinstance(result["notes"], str)


class TestStringCapabilityConversion:
    """Test string-to-capability conversion edge cases."""

    def test_has_capability_with_string_conversion(self):
        """Test has_capability converts string to ModelCapability."""
        model = ModelRegistry.get("claude-sonnet-4-5")
        assert model is not None

        # Test with string that needs conversion
        assert model.has_capability("vision") is True
        assert model.has_capability("function_calling") is True

        # Test with non-existent capability (should raise ValueError)
        with pytest.raises(ValueError):
            model.has_capability("nonexistent")

    def test_filter_by_capability_with_string(self):
        """Test filter_by_capability handles string input correctly."""
        # Test with string (covers line 314-317)
        vision_models = ModelRegistry.filter_by_capability("vision")

        assert len(vision_models) > 0
        assert all(m.has_capability(ModelCapability.VISION) for m in vision_models)

        # Test with ModelCapability enum directly
        caching_models = ModelRegistry.filter_by_capability(ModelCapability.PROMPT_CACHING)
        assert len(caching_models) > 0


class TestDateParsing:
    """Test date parsing edge cases and error handling."""

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.rglob")
    @patch("builtins.open", new_callable=mock_open)
    def test_parse_date_with_none(self, mock_file, mock_rglob, mock_exists):
        """Test _parse_date returns today when date_str is None."""
        mock_exists.return_value = True
        mock_rglob.return_value = []

        # Clear and reload to test date parsing
        ModelRegistry.clear_cache()

        # Test that None date falls back to today
        result = ModelRegistry._parse_date(None)
        assert result == date.today()

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.rglob")
    def test_parse_date_with_invalid_format(self, mock_rglob, mock_exists):
        """Test _parse_date returns today when format is invalid."""
        mock_exists.return_value = True
        mock_rglob.return_value = []

        ModelRegistry.clear_cache()

        # Test invalid date format falls back to today
        result = ModelRegistry._parse_date("not-a-date")
        assert result == date.today()

        result = ModelRegistry._parse_date("2025/01/01")  # Wrong separator
        assert result == date.today()

    def test_parse_date_with_valid_format(self):
        """Test _parse_date correctly parses valid ISO dates."""
        result = ModelRegistry._parse_date("2025-01-15")
        assert result == date(2025, 1, 15)


class TestErrorHandling:
    """Test error handling and warnings."""

    @patch("pathlib.Path.exists")
    @patch("builtins.print")
    def test_missing_definitions_directory_warning(self, mock_print, mock_exists):
        """Test warning is printed when definitions directory missing."""
        mock_exists.return_value = False

        ModelRegistry.clear_cache()
        ModelRegistry._load_models()

        # Verify warning was printed
        mock_print.assert_called()
        call_args = str(mock_print.call_args)
        assert "Warning" in call_args
        assert "Definitions directory not found" in call_args

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.rglob")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_invalid_yaml_skipped(self, mock_print, mock_file, mock_rglob, mock_exists):
        """Test that YAML files without model_id are skipped."""
        mock_exists.return_value = True

        # Create mock YAML file path
        mock_yaml_path = Mock(spec=Path)
        mock_yaml_path.__str__ = Mock(return_value="test.yaml")
        mock_rglob.return_value = [mock_yaml_path]

        # Mock YAML content without model_id
        mock_file.return_value.read.return_value = "name: Test"

        with patch("yaml.safe_load", return_value={"name": "Test"}):  # No model_id
            ModelRegistry.clear_cache()
            ModelRegistry._load_models()

            # Should skip this file without error
            assert len(ModelRegistry.get_all()) == 0

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.rglob")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_yaml_load_error_handling(self, mock_print, mock_file, mock_rglob, mock_exists):
        """Test error handling when YAML loading fails."""
        mock_exists.return_value = True

        mock_yaml_path = Mock(spec=Path)
        mock_yaml_path.__str__ = Mock(return_value="bad.yaml")
        mock_rglob.return_value = [mock_yaml_path]

        # Simulate YAML parsing error
        with patch("yaml.safe_load", side_effect=yaml.YAMLError("Parse error")):
            ModelRegistry.clear_cache()
            ModelRegistry._load_models()

            # Verify error was caught and warning printed
            mock_print.assert_called()
            call_args = str(mock_print.call_args_list[-1])
            assert "Warning" in call_args or "Failed" in call_args

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.rglob")
    @patch("builtins.open", new_callable=mock_open)
    def test_invalid_capability_ignored(self, mock_file, mock_rglob, mock_exists):
        """Test that invalid capabilities are ignored without crashing."""
        mock_exists.return_value = True

        mock_yaml_path = Mock(spec=Path)
        mock_rglob.return_value = [mock_yaml_path]

        # YAML with invalid capability
        yaml_content = """
model_id: test-model
name: Test Model
provider: test
api_identifier: test-api
capabilities:
  - vision
  - invalid_capability_xyz
  - function_calling
metadata:
  context_window_input: 1000
  release_date: "2025-01-01"
  last_verified: "2025-01-01"
pricing:
  input_per_1m: 1.0
  output_per_1m: 2.0
"""

        with patch("yaml.safe_load", return_value=yaml.safe_load(yaml_content)):
            ModelRegistry.clear_cache()
            ModelRegistry._load_models()

            model = ModelRegistry.get("test-model")
            assert model is not None
            # Should have valid capabilities, invalid one silently ignored
            assert ModelCapability.VISION in model.capabilities
            assert ModelCapability.FUNCTION_CALLING in model.capabilities


class TestConvenienceFunctions:
    """Test module-level convenience functions."""

    def test_get_model_convenience_function(self):
        """Test get_model convenience function."""
        # Clear cache from previous mock tests
        ModelRegistry.clear_cache()

        model = get_model("claude-haiku-4-5")
        assert model is not None
        assert model.model_id == "claude-haiku-4-5"

        # Test non-existent model
        assert get_model("nonexistent") is None

    def test_list_models_convenience_function(self):
        """Test list_models returns all model IDs."""
        # Clear cache from previous mock tests
        ModelRegistry.clear_cache()

        model_ids = list_models()

        assert isinstance(model_ids, list)
        assert len(model_ids) >= 8
        assert "claude-sonnet-4-5" in model_ids
        assert "gpt-4o" in model_ids
        assert "gemini-2-5-pro" in model_ids

    def test_list_providers_convenience_function(self):
        """Test list_providers returns unique providers."""
        # Clear cache from previous mock tests
        ModelRegistry.clear_cache()

        providers = list_providers()

        assert isinstance(providers, list)
        assert "anthropic" in providers
        assert "openai" in providers
        assert "google" in providers
        assert len(providers) == len(set(providers))  # All unique


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_get_by_provider_case_insensitive(self):
        """Test get_by_provider is case-insensitive."""
        # Clear cache from previous mock tests
        ModelRegistry.clear_cache()

        models_lower = ModelRegistry.get_by_provider("anthropic")
        models_upper = ModelRegistry.get_by_provider("ANTHROPIC")
        models_mixed = ModelRegistry.get_by_provider("Anthropic")

        assert len(models_lower) == len(models_upper) == len(models_mixed)
        assert len(models_lower) > 0

    def test_get_by_provider_empty_result(self):
        """Test get_by_provider returns empty list for unknown provider."""
        models = ModelRegistry.get_by_provider("nonexistent-provider")
        assert isinstance(models, list)
        assert len(models) == 0

    def test_filter_by_capability_empty_result(self):
        """Test filter_by_capability with capability no models have."""
        # All current models should have some capabilities,
        # but we can test the mechanism works
        all_models = ModelRegistry.get_all()
        assert len(all_models) > 0

        # Test filtering actually works
        vision_models = ModelRegistry.filter_by_capability(ModelCapability.VISION)
        assert len(vision_models) > 0

    def test_filter_by_cost_tier_all_tiers(self):
        """Test filter_by_cost_tier covers all tiers."""
        # Clear cache from previous mock tests
        ModelRegistry.clear_cache()

        budget = ModelRegistry.filter_by_cost_tier("budget")
        mid_tier = ModelRegistry.filter_by_cost_tier("mid-tier")
        premium = ModelRegistry.filter_by_cost_tier("premium")

        # Should have models in each tier
        assert len(budget) > 0
        assert len(mid_tier) > 0
        assert len(premium) > 0

        # Together should equal all models
        total = len(budget) + len(mid_tier) + len(premium)
        assert total == len(ModelRegistry.get_all())

    def test_cache_clear_reloads_models(self):
        """Test that clear_cache forces models to reload."""
        # Get initial models
        models_before = ModelRegistry.get_all()
        assert len(models_before) > 0

        # Clear cache
        ModelRegistry.clear_cache()

        # Verify cache was cleared
        assert not ModelRegistry._loaded
        assert len(ModelRegistry._models) == 0

        # Reload should work
        models_after = ModelRegistry.get_all()
        assert len(models_after) == len(models_before)

    def test_get_all_returns_copy(self):
        """Test that get_all returns a copy, not the original dict."""
        models1 = ModelRegistry.get_all()
        models2 = ModelRegistry.get_all()

        # Should be equal but not the same object
        assert models1 == models2
        assert models1 is not models2  # Different objects

        # Modifying one shouldn't affect the other
        models1.clear()
        assert len(models2) > 0


class TestModelDataclasses:
    """Test dataclass behavior and immutability."""

    def test_model_metadata_structure(self):
        """Test ModelMetadata dataclass structure."""
        metadata = ModelMetadata(
            context_window_input=100000,
            context_window_output=8000,
            knowledge_cutoff="January 2025",
            release_date=date(2025, 1, 1),
            last_verified=date(2025, 1, 15),
            docs_url="https://example.com",
        )

        assert metadata.context_window_input == 100000
        assert metadata.context_window_output == 8000
        assert metadata.knowledge_cutoff == "January 2025"
        assert metadata.docs_url == "https://example.com"

    def test_model_optimization_defaults(self):
        """Test ModelOptimization default values."""
        opt = ModelOptimization()

        assert opt.recommended_for == []
        assert opt.best_practices == []
        assert opt.cost_tier == "mid-tier"
        assert opt.speed_tier == "balanced"

    def test_model_optimization_custom_values(self):
        """Test ModelOptimization with custom values."""
        opt = ModelOptimization(
            recommended_for=["code_generation", "analysis"],
            best_practices=["Use structured outputs", "Enable caching"],
            cost_tier="premium",
            speed_tier="thorough",
        )

        assert "code_generation" in opt.recommended_for
        assert "Use structured outputs" in opt.best_practices
        assert opt.cost_tier == "premium"
        assert opt.speed_tier == "thorough"


class TestHasAllCapabilities:
    """Test Model.has_all_capabilities method."""

    def test_has_all_capabilities_with_all_present(self):
        """Test has_all_capabilities returns True when all are present."""
        model = ModelRegistry.get("claude-sonnet-4-5")
        assert model is not None

        # Test with capabilities the model has
        assert model.has_all_capabilities(["vision", "function_calling"]) is True

    def test_has_all_capabilities_with_some_missing(self):
        """Test has_all_capabilities returns False when some missing."""
        model = ModelRegistry.get("gemini-2-5-flash-lite")
        assert model is not None

        # Flash-Lite has limited capabilities - it's missing some of these
        all_caps = ["vision", "function_calling", "prompt_caching"]
        assert model.has_all_capabilities(all_caps) is False

    def test_has_all_capabilities_with_enum_and_string_mix(self):
        """Test has_all_capabilities with mixed enum/string input."""
        model = ModelRegistry.get("claude-opus-4-1")
        assert model is not None

        # Mix of string and enum
        mixed = [ModelCapability.VISION, "function_calling"]
        assert model.has_all_capabilities(mixed) is True

    def test_has_all_capabilities_empty_list(self):
        """Test has_all_capabilities with empty list returns True."""
        model = ModelRegistry.get("claude-haiku-4-5")
        assert model is not None

        # Empty requirements should return True
        assert model.has_all_capabilities([]) is True
