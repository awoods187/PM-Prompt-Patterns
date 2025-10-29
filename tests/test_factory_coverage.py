# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
Additional tests for providers/factory.py to achieve 90%+ coverage.

Focuses on model detection, provider instantiation, and error handling.
"""

from unittest.mock import MagicMock, patch

import pytest

from pm_prompt_toolkit.providers.base import LLMProvider
from pm_prompt_toolkit.providers.claude import ClaudeProvider
from pm_prompt_toolkit.providers.factory import get_provider


class TestGetProviderClaude:
    """Test get_provider with Claude models."""

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_get_provider_claude_haiku(self, mock_claude_provider):
        """Test get_provider returns ClaudeProvider for haiku."""
        mock_instance = MagicMock(spec=ClaudeProvider)
        mock_claude_provider.return_value = mock_instance

        result = get_provider("claude-haiku")

        mock_claude_provider.assert_called_once_with(
            model="claude-haiku", enable_caching=True
        )
        assert result == mock_instance

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_get_provider_claude_sonnet(self, mock_claude_provider):
        """Test get_provider returns ClaudeProvider for sonnet."""
        mock_instance = MagicMock(spec=ClaudeProvider)
        mock_claude_provider.return_value = mock_instance

        result = get_provider("claude-sonnet")

        mock_claude_provider.assert_called_once_with(
            model="claude-sonnet", enable_caching=True
        )
        assert result == mock_instance

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_get_provider_claude_opus(self, mock_claude_provider):
        """Test get_provider returns ClaudeProvider for opus."""
        mock_instance = MagicMock(spec=ClaudeProvider)
        mock_claude_provider.return_value = mock_instance

        result = get_provider("claude-opus")

        mock_claude_provider.assert_called_once_with(
            model="claude-opus", enable_caching=True
        )
        assert result == mock_instance

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_get_provider_case_insensitive(self, mock_claude_provider):
        """Test get_provider handles mixed case model names."""
        mock_instance = MagicMock(spec=ClaudeProvider)
        mock_claude_provider.return_value = mock_instance

        # Try various cases
        get_provider("CLAUDE-HAIKU")
        get_provider("Claude-Sonnet")
        get_provider("cLaUdE-OpUs")

        # Should normalize to lowercase
        assert mock_claude_provider.call_count == 3
        assert all(
            call[1]["model"].islower() for call in mock_claude_provider.call_args_list
        )

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_get_provider_with_caching_enabled(self, mock_claude_provider):
        """Test get_provider passes enable_caching=True by default."""
        mock_instance = MagicMock(spec=ClaudeProvider)
        mock_claude_provider.return_value = mock_instance

        get_provider("claude-sonnet")

        mock_claude_provider.assert_called_once_with(
            model="claude-sonnet", enable_caching=True
        )

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_get_provider_with_caching_disabled(self, mock_claude_provider):
        """Test get_provider passes enable_caching=False when requested."""
        mock_instance = MagicMock(spec=ClaudeProvider)
        mock_claude_provider.return_value = mock_instance

        get_provider("claude-haiku", enable_caching=False)

        mock_claude_provider.assert_called_once_with(
            model="claude-haiku", enable_caching=False
        )


class TestGetProviderOpenAI:
    """Test get_provider with OpenAI models (not yet implemented)."""

    def test_get_provider_gpt4_raises_not_implemented(self):
        """Test get_provider raises NotImplementedError for GPT-4."""
        with pytest.raises(NotImplementedError) as exc_info:
            get_provider("gpt-4")

        error_msg = str(exc_info.value)
        assert "OpenAI provider for gpt-4 is not yet implemented" in error_msg
        assert "Use Claude models for now" in error_msg
        assert "TODO.md" in error_msg

    def test_get_provider_gpt35_raises_not_implemented(self):
        """Test get_provider raises NotImplementedError for GPT-3.5."""
        with pytest.raises(NotImplementedError) as exc_info:
            get_provider("gpt-3.5")

        error_msg = str(exc_info.value)
        assert "OpenAI provider for gpt-3.5 is not yet implemented" in error_msg

    def test_get_provider_gpt4_turbo_raises_not_implemented(self):
        """Test get_provider raises NotImplementedError for GPT-4 Turbo."""
        with pytest.raises(NotImplementedError) as exc_info:
            get_provider("gpt-4-turbo")

        error_msg = str(exc_info.value)
        assert "OpenAI provider for gpt-4-turbo is not yet implemented" in error_msg

    def test_get_provider_openai_case_insensitive(self):
        """Test OpenAI model detection is case-insensitive."""
        with pytest.raises(NotImplementedError):
            get_provider("GPT-4")

        with pytest.raises(NotImplementedError):
            get_provider("Gpt-3.5")


class TestGetProviderGemini:
    """Test get_provider with Gemini models (not yet implemented)."""

    def test_get_provider_gemini_pro_raises_not_implemented(self):
        """Test get_provider raises NotImplementedError for Gemini Pro."""
        with pytest.raises(NotImplementedError) as exc_info:
            get_provider("gemini-pro")

        error_msg = str(exc_info.value)
        assert "Gemini provider for gemini-pro is not yet implemented" in error_msg
        assert "Use Claude models for now" in error_msg
        assert "TODO.md" in error_msg

    def test_get_provider_gemini_flash_raises_not_implemented(self):
        """Test get_provider raises NotImplementedError for Gemini Flash."""
        with pytest.raises(NotImplementedError) as exc_info:
            get_provider("gemini-flash")

        error_msg = str(exc_info.value)
        assert "Gemini provider for gemini-flash is not yet implemented" in error_msg

    def test_get_provider_gemini_case_insensitive(self):
        """Test Gemini model detection is case-insensitive."""
        with pytest.raises(NotImplementedError):
            get_provider("GEMINI-PRO")

        with pytest.raises(NotImplementedError):
            get_provider("Gemini-Flash")


class TestGetProviderUnknownModel:
    """Test get_provider with unknown models."""

    def test_get_provider_unknown_model_raises_value_error(self):
        """Test get_provider raises ValueError for unknown model."""
        with pytest.raises(ValueError) as exc_info:
            get_provider("unknown-model")

        error_msg = str(exc_info.value)
        assert "Unknown model: unknown-model" in error_msg
        assert "claude-haiku" in error_msg
        assert "claude-sonnet" in error_msg
        assert "claude-opus" in error_msg

    def test_get_provider_empty_string_raises_value_error(self):
        """Test get_provider raises ValueError for empty string."""
        with pytest.raises(ValueError) as exc_info:
            get_provider("")

        error_msg = str(exc_info.value)
        assert "Unknown model:" in error_msg

    def test_get_provider_invalid_model_shows_planned_models(self):
        """Test error message includes planned models."""
        with pytest.raises(ValueError) as exc_info:
            get_provider("invalid-model")

        error_msg = str(exc_info.value)
        assert "gpt-4" in error_msg
        assert "gpt-3.5" in error_msg
        assert "gemini-pro" in error_msg
        assert "gemini-flash" in error_msg
        assert "TODO.md" in error_msg

    def test_get_provider_similar_but_invalid_model(self):
        """Test models that are close to valid but not exact."""
        # Close to valid but not exact
        invalid_models = [
            "claude",
            "claude-haiku-3",
            "sonnet",
            "claude-sonnet-3-5",
            "gpt",
            "gemini",
        ]

        for model in invalid_models:
            with pytest.raises((ValueError, NotImplementedError)):
                get_provider(model)


class TestGetProviderReturnType:
    """Test get_provider return type and interface."""

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_get_provider_returns_llm_provider_interface(self, mock_claude_provider):
        """Test get_provider returns LLMProvider interface."""
        mock_instance = MagicMock(spec=LLMProvider)
        mock_claude_provider.return_value = mock_instance

        result = get_provider("claude-haiku")

        assert isinstance(result, LLMProvider)

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_get_provider_returns_claude_provider_instance(self, mock_claude_provider):
        """Test get_provider specifically returns ClaudeProvider for Claude models."""
        mock_instance = MagicMock(spec=ClaudeProvider)
        mock_claude_provider.return_value = mock_instance

        result = get_provider("claude-sonnet")

        # Should be a ClaudeProvider instance
        assert result == mock_instance


class TestGetProviderEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_get_provider_with_whitespace(self):
        """Test get_provider raises ValueError for models with whitespace."""
        # Whitespace is not stripped, so this is treated as unknown model
        with pytest.raises(ValueError) as exc_info:
            get_provider("  claude-haiku  ")

        error_msg = str(exc_info.value)
        assert "Unknown model:" in error_msg

    def test_get_provider_special_characters(self):
        """Test get_provider with special characters in model name."""
        with pytest.raises(ValueError):
            get_provider("claude@haiku")

        with pytest.raises(ValueError):
            get_provider("claude/haiku")

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_get_provider_preserves_original_model_casing_in_error(
        self, mock_claude_provider
    ):
        """Test that error messages preserve original model casing."""
        # When ClaudeProvider raises an error, the original casing should be visible
        mock_claude_provider.side_effect = ValueError("Invalid model")

        with pytest.raises(ValueError):
            get_provider("CLAUDE-HAIKU")

        # The provider should receive lowercase
        mock_claude_provider.assert_called_once_with(
            model="claude-haiku", enable_caching=True
        )


class TestGetProviderParameterCombinations:
    """Test various parameter combinations."""

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_all_claude_models_with_caching_disabled(self, mock_claude_provider):
        """Test all Claude models can be instantiated with caching disabled."""
        mock_instance = MagicMock(spec=ClaudeProvider)
        mock_claude_provider.return_value = mock_instance

        models = ["claude-haiku", "claude-sonnet", "claude-opus"]

        for model in models:
            get_provider(model, enable_caching=False)

        # All should be called with caching disabled
        assert mock_claude_provider.call_count == 3
        assert all(
            not call[1]["enable_caching"]
            for call in mock_claude_provider.call_args_list
        )

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_all_claude_models_with_caching_enabled(self, mock_claude_provider):
        """Test all Claude models can be instantiated with caching enabled."""
        mock_instance = MagicMock(spec=ClaudeProvider)
        mock_claude_provider.return_value = mock_instance

        models = ["claude-haiku", "claude-sonnet", "claude-opus"]

        for model in models:
            get_provider(model, enable_caching=True)

        assert mock_claude_provider.call_count == 3
        assert all(
            call[1]["enable_caching"] for call in mock_claude_provider.call_args_list
        )
