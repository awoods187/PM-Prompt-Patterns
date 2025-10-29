# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
Additional tests for ai_models/capabilities.py to achieve 90%+ coverage.

Focuses on edge cases, error handling, and untested code paths.
"""

from pathlib import Path
from unittest.mock import Mock, mock_open, patch

import pytest
import yaml

from ai_models.capabilities import (
    CapabilityValidator,
    ModelCapability,
    has_function_calling,
    has_prompt_caching,
    has_vision,
    supports_large_context,
)


class TestModelCapabilityEnum:
    """Test ModelCapability enum functionality."""

    def test_from_string_with_invalid_capability(self):
        """Test from_string raises ValueError with helpful message for invalid input."""
        with pytest.raises(ValueError) as exc_info:
            ModelCapability.from_string("invalid_capability")

        error_msg = str(exc_info.value)
        assert "Invalid capability 'invalid_capability'" in error_msg
        assert "Valid:" in error_msg
        # Should list all valid capabilities
        assert "vision" in error_msg
        assert "function_calling" in error_msg

    def test_from_string_with_valid_capabilities(self):
        """Test from_string correctly converts valid capability strings."""
        assert ModelCapability.from_string("vision") == ModelCapability.VISION
        assert (
            ModelCapability.from_string("function_calling") == ModelCapability.FUNCTION_CALLING
        )
        assert (
            ModelCapability.from_string("prompt_caching") == ModelCapability.PROMPT_CACHING
        )
        assert ModelCapability.from_string("streaming") == ModelCapability.STREAMING

    def test_str_representation(self):
        """Test __str__ returns the value."""
        assert str(ModelCapability.VISION) == "vision"
        assert str(ModelCapability.FUNCTION_CALLING) == "function_calling"
        assert str(ModelCapability.LARGE_CONTEXT) == "large_context"

    def test_all_capabilities_have_string_values(self):
        """Test that all capabilities can be converted to/from strings."""
        for cap in ModelCapability:
            # Should be able to convert to string and back
            cap_str = str(cap)
            assert isinstance(cap_str, str)
            assert ModelCapability.from_string(cap_str) == cap


class TestCapabilityValidatorErrorHandling:
    """Test error handling in CapabilityValidator."""

    @patch("pathlib.Path.exists")
    def test_missing_definitions_directory(self, mock_exists):
        """Test graceful handling when definitions directory doesn't exist."""
        mock_exists.return_value = False

        CapabilityValidator.clear_cache()
        CapabilityValidator._load_capabilities()

        # Should not crash, just return early with loaded=True but empty cache
        # Since the directory doesn't exist, it returns early after setting _loaded
        caps = CapabilityValidator.get_capabilities("nonexistent-model")
        assert caps == set()

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.rglob")
    @patch("builtins.open", new_callable=mock_open)
    def test_invalid_yaml_data_skipped(self, mock_file, mock_rglob, mock_exists):
        """Test that YAML files without model_id are skipped."""
        mock_exists.return_value = True

        mock_yaml_path = Mock(spec=Path)
        mock_yaml_path.__str__ = Mock(return_value="test.yaml")
        mock_rglob.return_value = [mock_yaml_path]

        # Mock YAML content without model_id
        with patch("yaml.safe_load", return_value={"name": "Test"}):
            CapabilityValidator.clear_cache()
            CapabilityValidator._load_capabilities()

            # Should have loaded but skipped this file
            assert CapabilityValidator._loaded is True

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.rglob")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_invalid_capability_in_yaml_generates_warning(
        self, mock_print, mock_file, mock_rglob, mock_exists
    ):
        """Test that invalid capabilities in YAML generate warnings."""
        mock_exists.return_value = True

        mock_yaml_path = Mock(spec=Path)
        mock_yaml_path.__str__ = Mock(return_value="test.yaml")
        mock_rglob.return_value = [mock_yaml_path]

        # YAML with invalid capability
        yaml_content = """
model_id: test-model
capabilities:
  - vision
  - invalid_capability
  - function_calling
"""

        with patch("yaml.safe_load", return_value=yaml.safe_load(yaml_content)):
            CapabilityValidator.clear_cache()
            CapabilityValidator._load_capabilities()

            # Should have printed warning about invalid capability
            mock_print.assert_called()
            call_args = str(mock_print.call_args_list)
            assert "Warning" in call_args

            # Should have loaded the valid capabilities
            caps = CapabilityValidator.get_capabilities("test-model")
            assert ModelCapability.VISION in caps
            assert ModelCapability.FUNCTION_CALLING in caps

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.rglob")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_yaml_load_exception_handling(
        self, mock_print, mock_file, mock_rglob, mock_exists
    ):
        """Test exception handling when YAML loading fails."""
        mock_exists.return_value = True

        mock_yaml_path = Mock(spec=Path)
        mock_yaml_path.__str__ = Mock(return_value="bad.yaml")
        mock_rglob.return_value = [mock_yaml_path]

        # Simulate YAML parsing error
        with patch("yaml.safe_load", side_effect=yaml.YAMLError("Parse error")):
            CapabilityValidator.clear_cache()
            CapabilityValidator._load_capabilities()

            # Verify error was caught and warning printed
            mock_print.assert_called()
            call_args = str(mock_print.call_args_list[-1])
            assert "Warning" in call_args or "Failed" in call_args


class TestHasAllCapabilities:
    """Test has_all_capabilities method."""

    def test_has_all_capabilities_returns_true_when_all_present(self):
        """Test returns True when model has all required capabilities."""
        # Clear cache from mock tests
        CapabilityValidator.clear_cache()

        # Claude Sonnet has vision, function_calling, and more
        result = CapabilityValidator.has_all_capabilities(
            "claude-sonnet-4-5", [ModelCapability.VISION, ModelCapability.FUNCTION_CALLING]
        )
        assert result is True

    def test_has_all_capabilities_returns_false_when_some_missing(self):
        """Test returns False when model missing some capabilities."""
        # Gemini Flash-Lite has limited capabilities
        result = CapabilityValidator.has_all_capabilities(
            "gemini-2-5-flash-lite",
            [ModelCapability.VISION, ModelCapability.FUNCTION_CALLING, ModelCapability.PROMPT_CACHING],
        )
        assert result is False

    def test_has_all_capabilities_with_empty_list(self):
        """Test returns True when no capabilities required."""
        result = CapabilityValidator.has_all_capabilities("claude-haiku-4-5", [])
        assert result is True

    def test_has_all_capabilities_with_nonexistent_model(self):
        """Test returns False for nonexistent model."""
        result = CapabilityValidator.has_all_capabilities(
            "nonexistent-model", [ModelCapability.VISION]
        )
        assert result is False


class TestHasAnyCapability:
    """Test has_any_capability method."""

    def test_has_any_capability_returns_true_when_at_least_one_present(self):
        """Test returns True when model has at least one capability."""
        # Clear cache from mock tests
        CapabilityValidator.clear_cache()

        # Flash-Lite has VISION but not all advanced features
        result = CapabilityValidator.has_any_capability(
            "gemini-2-5-flash-lite",
            [ModelCapability.VISION, ModelCapability.FUNCTION_CALLING, ModelCapability.PROMPT_CACHING],
        )
        assert result is True  # Has VISION

    def test_has_any_capability_returns_false_when_none_present(self):
        """Test returns False when model has none of the capabilities."""
        # Flash-Lite doesn't have function_calling or prompt_caching
        result = CapabilityValidator.has_any_capability(
            "gemini-2-5-flash-lite",
            [ModelCapability.FUNCTION_CALLING, ModelCapability.PROMPT_CACHING],
        )
        assert result is False

    def test_has_any_capability_with_empty_list(self):
        """Test returns False when no capabilities to check."""
        result = CapabilityValidator.has_any_capability("claude-sonnet-4-5", [])
        assert result is False

    def test_has_any_capability_with_nonexistent_model(self):
        """Test returns False for nonexistent model."""
        result = CapabilityValidator.has_any_capability(
            "nonexistent-model", [ModelCapability.VISION]
        )
        assert result is False


class TestFilterModelsByCapability:
    """Test filter_models_by_capability method."""

    def test_filter_models_by_capability_returns_matching_models(self):
        """Test filtering returns all models with the capability."""
        # Clear cache from mock tests
        CapabilityValidator.clear_cache()

        vision_models = CapabilityValidator.filter_models_by_capability(ModelCapability.VISION)

        assert isinstance(vision_models, list)
        assert len(vision_models) > 0
        # Should include major vision-capable models
        assert "claude-sonnet-4-5" in vision_models
        assert "gpt-4o" in vision_models

    def test_filter_models_by_capability_with_rare_capability(self):
        """Test filtering with capability few models have."""
        # Clear cache from mock tests
        CapabilityValidator.clear_cache()

        code_exec_models = CapabilityValidator.filter_models_by_capability(
            ModelCapability.CODE_EXECUTION
        )

        assert isinstance(code_exec_models, list)
        # Gemini models have code execution
        gemini_models = [m for m in code_exec_models if "gemini" in m]
        assert len(gemini_models) > 0

    def test_filter_models_by_capability_returns_list(self):
        """Test method always returns a list, even if empty."""
        # Even if no models have a capability, should return empty list
        models = CapabilityValidator.filter_models_by_capability(ModelCapability.STREAMING)
        assert isinstance(models, list)


class TestGetCapabilityMatrix:
    """Test get_capability_matrix method."""

    def test_get_capability_matrix_returns_complete_mapping(self):
        """Test matrix returns all models with their capabilities."""
        # Clear cache from mock tests
        CapabilityValidator.clear_cache()

        matrix = CapabilityValidator.get_capability_matrix()

        assert isinstance(matrix, dict)
        assert len(matrix) > 0

        # Should include known models
        assert "claude-sonnet-4-5" in matrix
        assert "gpt-4o" in matrix

    def test_get_capability_matrix_capabilities_are_strings(self):
        """Test capability values in matrix are strings, not enums."""
        matrix = CapabilityValidator.get_capability_matrix()

        for model_id, capabilities in matrix.items():
            assert isinstance(capabilities, set)
            for cap in capabilities:
                assert isinstance(cap, str)
                # Should be valid capability strings
                assert cap in [
                    "text_input",
                    "text_output",
                    "vision",
                    "function_calling",
                    "streaming",
                    "json_mode",
                    "large_context",
                    "prompt_caching",
                    "code_execution",
                    "search",
                ]

    def test_get_capability_matrix_consistency(self):
        """Test matrix is consistent with individual lookups."""
        matrix = CapabilityValidator.get_capability_matrix()

        for model_id, cap_strings in matrix.items():
            # Get capabilities using normal method
            caps_enum = CapabilityValidator.get_capabilities(model_id)

            # Convert enums to strings
            caps_strings_from_enum = {cap.value for cap in caps_enum}

            # Should match the matrix
            assert cap_strings == caps_strings_from_enum


class TestConvenienceFunctions:
    """Test module-level convenience functions."""

    def test_has_vision_convenience_function(self):
        """Test has_vision convenience function."""
        # Clear cache to ensure fresh data
        CapabilityValidator.clear_cache()

        assert has_vision("claude-sonnet-4-5") is True
        assert has_vision("gpt-4o") is True
        assert has_vision("nonexistent-model") is False

    def test_has_function_calling_convenience_function(self):
        """Test has_function_calling convenience function."""
        CapabilityValidator.clear_cache()

        assert has_function_calling("claude-opus-4-1") is True
        assert has_function_calling("gpt-4o-mini") is True
        # Flash-Lite doesn't have function calling
        assert has_function_calling("gemini-2-5-flash-lite") is False

    def test_has_prompt_caching_convenience_function(self):
        """Test has_prompt_caching convenience function."""
        CapabilityValidator.clear_cache()

        assert has_prompt_caching("claude-sonnet-4-5") is True
        assert has_prompt_caching("gemini-2-5-flash") is True
        # Flash-Lite and GPT models don't have prompt caching
        assert has_prompt_caching("gemini-2-5-flash-lite") is False
        assert has_prompt_caching("gpt-4o") is False

    def test_supports_large_context_convenience_function(self):
        """Test supports_large_context convenience function."""
        CapabilityValidator.clear_cache()

        # All current models have large context (>32k)
        assert supports_large_context("claude-haiku-4-5") is True
        assert supports_large_context("gpt-4o") is True
        assert supports_large_context("gemini-2-5-pro") is True
        assert supports_large_context("nonexistent-model") is False


class TestGetCapabilities:
    """Test get_capabilities returns a copy."""

    def test_get_capabilities_returns_copy(self):
        """Test that get_capabilities returns a copy, not the original set."""
        caps1 = CapabilityValidator.get_capabilities("claude-sonnet-4-5")
        caps2 = CapabilityValidator.get_capabilities("claude-sonnet-4-5")

        # Should be equal but not the same object
        assert caps1 == caps2
        assert caps1 is not caps2

        # Modifying one shouldn't affect the other
        caps1.clear()
        caps2_after = CapabilityValidator.get_capabilities("claude-sonnet-4-5")
        assert len(caps2_after) > 0  # Original data unchanged

    def test_get_capabilities_for_nonexistent_model(self):
        """Test get_capabilities returns empty set for unknown model."""
        caps = CapabilityValidator.get_capabilities("nonexistent-model")
        assert isinstance(caps, set)
        assert len(caps) == 0


class TestCacheClear:
    """Test cache clearing functionality."""

    def test_clear_cache_resets_state(self):
        """Test that clear_cache resets validator state."""
        # Load some data
        _ = CapabilityValidator.get_capabilities("claude-sonnet-4-5")
        assert CapabilityValidator._loaded is True
        assert len(CapabilityValidator._capabilities_cache) > 0

        # Clear cache
        CapabilityValidator.clear_cache()

        # Should be reset
        assert CapabilityValidator._loaded is False
        assert len(CapabilityValidator._capabilities_cache) == 0

        # Should reload on next access
        caps = CapabilityValidator.get_capabilities("claude-haiku-4-5")
        assert len(caps) > 0
        assert CapabilityValidator._loaded is True
