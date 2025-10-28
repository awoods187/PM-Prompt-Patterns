# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""LLM provider implementations for multiple vendors.

This module provides a unified interface for working with different LLM providers
(Anthropic Claude, OpenAI GPT, Google Gemini) with consistent APIs and error handling.

Supported Providers:
    - Anthropic Claude (Haiku, Sonnet, Opus)
    - OpenAI GPT (GPT-3.5, GPT-4, GPT-4 Turbo)
    - Google Gemini (Gemini Pro, Gemini Flash)

Example:
    >>> from pm_prompt_toolkit.providers import ClaudeProvider
    >>> provider = ClaudeProvider(model="claude-sonnet")
    >>> result = provider.classify("We need SSO integration")
    >>> print(result.category, result.confidence)
    feature_request 0.96

Security:
    All providers use API keys from environment variables.
    Never hardcode credentials.
"""

from pm_prompt_toolkit.providers.base import (
    ClassificationResult,
    LLMProvider,
    ProviderMetrics,
)
from pm_prompt_toolkit.providers.claude import ClaudeProvider
from pm_prompt_toolkit.providers.factory import get_provider
from pm_prompt_toolkit.providers.gemini import GeminiProvider
from pm_prompt_toolkit.providers.openai import OpenAIProvider

__all__ = [
    "ClassificationResult",
    "ClaudeProvider",
    "GeminiProvider",
    "LLMProvider",
    "OpenAIProvider",
    "ProviderMetrics",
    "get_provider",
]
