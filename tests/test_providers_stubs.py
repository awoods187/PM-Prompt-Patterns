# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
Tests for stub provider implementations (OpenAI, Gemini).

These providers are not yet implemented and should raise NotImplementedError.
"""

import pytest

from pm_prompt_toolkit.providers.gemini import GeminiProvider
from pm_prompt_toolkit.providers.openai import OpenAIProvider


class TestOpenAIProviderStub:
    """Test OpenAIProvider stub implementation."""

    def test_initialization_raises_not_implemented(self):
        """Test that OpenAI provider raises NotImplementedError on init."""
        with pytest.raises(NotImplementedError) as exc_info:
            OpenAIProvider(model="gpt-4o")

        error_msg = str(exc_info.value)
        assert "OpenAI provider not yet implemented" in error_msg
        assert "ClaudeProvider" in error_msg
        assert "CONTRIBUTING.md" in error_msg

    def test_initialization_with_caching_disabled(self):
        """Test that init raises NotImplementedError regardless of caching setting."""
        with pytest.raises(NotImplementedError):
            OpenAIProvider(model="gpt-4o-mini", enable_caching=False)

    def test_default_model_parameter(self):
        """Test that default model parameter still raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            OpenAIProvider()  # Uses default model="gpt-4"


class TestGeminiProviderStub:
    """Test GeminiProvider stub implementation."""

    def test_initialization_raises_not_implemented(self):
        """Test that Gemini provider raises NotImplementedError on init."""
        with pytest.raises(NotImplementedError) as exc_info:
            GeminiProvider(model="gemini-pro")

        error_msg = str(exc_info.value)
        assert "Gemini provider not yet implemented" in error_msg
        assert "ClaudeProvider" in error_msg
        assert "CONTRIBUTING.md" in error_msg

    def test_initialization_with_caching_disabled(self):
        """Test that init raises NotImplementedError regardless of caching setting."""
        with pytest.raises(NotImplementedError):
            GeminiProvider(model="gemini-pro-vision", enable_caching=False)

    def test_default_model_parameter(self):
        """Test that default model parameter still raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            GeminiProvider()  # Uses default model="gemini-pro"
