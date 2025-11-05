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
from pm_prompt_toolkit.providers.factory import ConfigurationError, get_provider


class TestGetProviderClaude:
    """Test get_provider with Claude models."""

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_get_provider_claude_haiku(self, mock_claude_provider) -> None:  # type: ignore[no-untyped-def]
        """Test get_provider returns ClaudeProvider for haiku."""
        mock_instance = MagicMock(spec=ClaudeProvider)
        mock_claude_provider.return_value = mock_instance

        result = get_provider("claude-haiku")

        mock_claude_provider.assert_called_once_with(model="claude-haiku", enable_caching=True)
        assert result == mock_instance

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_get_provider_claude_sonnet(self, mock_claude_provider) -> None:  # type: ignore[no-untyped-def]
        """Test get_provider returns ClaudeProvider for sonnet."""
        mock_instance = MagicMock(spec=ClaudeProvider)
        mock_claude_provider.return_value = mock_instance

        result = get_provider("claude-sonnet")

        mock_claude_provider.assert_called_once_with(model="claude-sonnet", enable_caching=True)
        assert result == mock_instance

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_get_provider_claude_opus(self, mock_claude_provider) -> None:  # type: ignore[no-untyped-def]
        """Test get_provider returns ClaudeProvider for opus."""
        mock_instance = MagicMock(spec=ClaudeProvider)
        mock_claude_provider.return_value = mock_instance

        result = get_provider("claude-opus")

        mock_claude_provider.assert_called_once_with(model="claude-opus", enable_caching=True)
        assert result == mock_instance

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_get_provider_case_insensitive(self, mock_claude_provider) -> None:  # type: ignore[no-untyped-def]
        """Test get_provider handles mixed case model names."""
        mock_instance = MagicMock(spec=ClaudeProvider)
        mock_claude_provider.return_value = mock_instance

        # Try various cases
        get_provider("CLAUDE-HAIKU")
        get_provider("Claude-Sonnet")
        get_provider("cLaUdE-OpUs")

        # Should normalize to lowercase
        assert mock_claude_provider.call_count == 3
        assert all(call[1]["model"].islower() for call in mock_claude_provider.call_args_list)

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_get_provider_with_caching_enabled(self, mock_claude_provider) -> None:  # type: ignore[no-untyped-def]
        """Test get_provider passes enable_caching=True by default."""
        mock_instance = MagicMock(spec=ClaudeProvider)
        mock_claude_provider.return_value = mock_instance

        get_provider("claude-sonnet")

        mock_claude_provider.assert_called_once_with(model="claude-sonnet", enable_caching=True)

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_get_provider_with_caching_disabled(self, mock_claude_provider) -> None:  # type: ignore[no-untyped-def]
        """Test get_provider passes enable_caching=False when requested."""
        mock_instance = MagicMock(spec=ClaudeProvider)
        mock_claude_provider.return_value = mock_instance

        get_provider("claude-haiku", enable_caching=False)

        mock_claude_provider.assert_called_once_with(model="claude-haiku", enable_caching=False)


class TestGetProviderOpenAI:
    """Test get_provider with OpenAI models when not enabled."""

    def test_get_provider_gpt4_raises_configuration_error(self) -> None:
        """Test get_provider raises ConfigurationError for GPT-4 when not enabled."""
        with pytest.raises(ConfigurationError) as exc_info:
            get_provider("gpt-4")

        error_msg = str(exc_info.value)
        assert "OpenAI provider for gpt-4 is not enabled" in error_msg
        assert "ENABLE_OPENAI=true" in error_msg
        assert "OPENAI_API_KEY" in error_msg

    def test_get_provider_gpt35_raises_configuration_error(self) -> None:
        """Test get_provider raises ConfigurationError for GPT-3.5 when not enabled."""
        with pytest.raises(ConfigurationError) as exc_info:
            get_provider("gpt-3.5")

        error_msg = str(exc_info.value)
        assert "OpenAI provider for gpt-3.5 is not enabled" in error_msg

    def test_get_provider_gpt4_turbo_raises_configuration_error(self) -> None:
        """Test get_provider raises ConfigurationError for GPT-4o when not enabled."""
        with pytest.raises(ConfigurationError) as exc_info:
            get_provider("gpt-4o")

        error_msg = str(exc_info.value)
        assert "OpenAI provider for gpt-4o is not enabled" in error_msg

    def test_get_provider_openai_case_insensitive(self) -> None:
        """Test OpenAI model detection is case-insensitive."""
        with pytest.raises(ConfigurationError):
            get_provider("GPT-4")

        with pytest.raises(ConfigurationError):
            get_provider("Gpt-3.5")


class TestGetProviderGemini:
    """Test get_provider with Gemini models (now implemented)."""

    @patch("pm_prompt_toolkit.providers.factory.GeminiProvider")
    def test_get_provider_gemini_pro(self, mock_gemini_provider) -> None:  # type: ignore[no-untyped-def]
        """Test get_provider returns GeminiProvider for Gemini 2.5 Pro."""
        from pm_prompt_toolkit.providers.gemini import GeminiProvider

        mock_instance = MagicMock(spec=GeminiProvider)
        mock_gemini_provider.return_value = mock_instance

        result = get_provider("gemini-2-5-pro")

        mock_gemini_provider.assert_called_once_with(model="gemini-2-5-pro", enable_caching=True)
        assert result == mock_instance

    @patch("pm_prompt_toolkit.providers.factory.GeminiProvider")
    def test_get_provider_gemini_flash(self, mock_gemini_provider) -> None:  # type: ignore[no-untyped-def]
        """Test get_provider returns GeminiProvider for Gemini 2.5 Flash."""
        from pm_prompt_toolkit.providers.gemini import GeminiProvider

        mock_instance = MagicMock(spec=GeminiProvider)
        mock_gemini_provider.return_value = mock_instance

        result = get_provider("gemini-2-5-flash")

        mock_gemini_provider.assert_called_once_with(model="gemini-2-5-flash", enable_caching=True)
        assert result == mock_instance

    @patch("pm_prompt_toolkit.providers.factory.GeminiProvider")
    def test_get_provider_gemini_case_insensitive(self, mock_gemini_provider) -> None:  # type: ignore[no-untyped-def]
        """Test Gemini model detection is case-insensitive."""
        from pm_prompt_toolkit.providers.gemini import GeminiProvider

        mock_instance = MagicMock(spec=GeminiProvider)
        mock_gemini_provider.return_value = mock_instance

        # Uppercase should work
        get_provider("GEMINI-2-5-FLASH")
        # Will be normalized to lowercase by factory
        assert mock_gemini_provider.called


class TestGetProviderUnknownModel:
    """Test get_provider with unknown models."""

    def test_get_provider_unknown_model_raises_value_error(self) -> None:
        """Test get_provider raises ValueError for unknown model."""
        with pytest.raises(ValueError) as exc_info:
            get_provider("unknown-model")

        error_msg = str(exc_info.value)
        assert "Unknown model: unknown-model" in error_msg
        assert "claude-haiku" in error_msg
        assert "claude-sonnet" in error_msg
        assert "claude-opus" in error_msg

    def test_get_provider_empty_string_raises_value_error(self) -> None:
        """Test get_provider raises ValueError for empty string."""
        with pytest.raises(ValueError) as exc_info:
            get_provider("")

        error_msg = str(exc_info.value)
        assert "Unknown model:" in error_msg

    def test_get_provider_invalid_model_shows_planned_models(self) -> None:
        """Test error message includes supported models."""
        with pytest.raises(ValueError) as exc_info:
            get_provider("invalid-model")

        error_msg = str(exc_info.value)
        assert "gpt-4" in error_msg
        assert "gpt-4o" in error_msg
        assert "gemini-2-5" in error_msg
        assert "claude-haiku" in error_msg
        assert "README.md" in error_msg

    def test_get_provider_similar_but_invalid_model(self) -> None:
        """Test models that are close to valid but not exact."""
        # Close to valid but not exact - these raise ValueError
        invalid_models = [
            "claude",
            "claude-haiku-3",
            "sonnet",
            "claude-sonnet-3-5",
        ]

        for model in invalid_models:
            with pytest.raises(ValueError):
                get_provider(model)

        # "gpt" triggers ConfigurationError (OpenAI not enabled)
        with pytest.raises(ConfigurationError):
            get_provider("gpt")

        # "gemini" gets routed to GeminiProvider which raises ValueError for unsupported model
        with pytest.raises(ValueError, match="Unsupported Gemini model"):
            get_provider("gemini")


class TestGetProviderReturnType:
    """Test get_provider return type and interface."""

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_get_provider_returns_llm_provider_interface(self, mock_claude_provider) -> None:  # type: ignore[no-untyped-def]
        """Test get_provider returns LLMProvider interface."""
        mock_instance = MagicMock(spec=LLMProvider)
        mock_claude_provider.return_value = mock_instance

        result = get_provider("claude-haiku")

        assert isinstance(result, LLMProvider)

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_get_provider_returns_claude_provider_instance(self, mock_claude_provider) -> None:  # type: ignore[no-untyped-def]
        """Test get_provider specifically returns ClaudeProvider for Claude models."""
        mock_instance = MagicMock(spec=ClaudeProvider)
        mock_claude_provider.return_value = mock_instance

        result = get_provider("claude-sonnet")

        # Should be a ClaudeProvider instance
        assert result == mock_instance


class TestGetProviderEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_get_provider_with_whitespace(self) -> None:
        """Test get_provider raises ValueError for models with whitespace."""
        # Whitespace is not stripped, so this is treated as unknown model
        with pytest.raises(ValueError) as exc_info:
            get_provider("  claude-haiku  ")

        error_msg = str(exc_info.value)
        assert "Unknown model:" in error_msg

    def test_get_provider_special_characters(self) -> None:
        """Test get_provider with special characters in model name."""
        with pytest.raises(ValueError):
            get_provider("claude@haiku")

        with pytest.raises(ValueError):
            get_provider("claude/haiku")

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_get_provider_preserves_original_model_casing_in_error(self, mock_claude_provider) -> None:  # type: ignore[no-untyped-def]
        """Test that error messages preserve original model casing."""
        # When ClaudeProvider raises an error, the original casing should be visible
        mock_claude_provider.side_effect = ValueError("Invalid model")

        with pytest.raises(ValueError):
            get_provider("CLAUDE-HAIKU")

        # The provider should receive lowercase
        mock_claude_provider.assert_called_once_with(model="claude-haiku", enable_caching=True)


class TestGetProviderParameterCombinations:
    """Test various parameter combinations."""

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_all_claude_models_with_caching_disabled(self, mock_claude_provider) -> None:  # type: ignore[no-untyped-def]
        """Test all Claude models can be instantiated with caching disabled."""
        mock_instance = MagicMock(spec=ClaudeProvider)
        mock_claude_provider.return_value = mock_instance

        models = ["claude-haiku", "claude-sonnet", "claude-opus"]

        for model in models:
            get_provider(model, enable_caching=False)

        # All should be called with caching disabled
        assert mock_claude_provider.call_count == 3
        assert all(not call[1]["enable_caching"] for call in mock_claude_provider.call_args_list)

    @patch("pm_prompt_toolkit.providers.factory.ClaudeProvider")
    def test_all_claude_models_with_caching_enabled(self, mock_claude_provider) -> None:  # type: ignore[no-untyped-def]
        """Test all Claude models can be instantiated with caching enabled."""
        mock_instance = MagicMock(spec=ClaudeProvider)
        mock_claude_provider.return_value = mock_instance

        models = ["claude-haiku", "claude-sonnet", "claude-opus"]

        for model in models:
            get_provider(model, enable_caching=True)

        assert mock_claude_provider.call_count == 3
        assert all(call[1]["enable_caching"] for call in mock_claude_provider.call_args_list)
