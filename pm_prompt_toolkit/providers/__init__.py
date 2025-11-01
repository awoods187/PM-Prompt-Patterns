# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""LLM provider implementations for multiple vendors.

This module provides a unified interface for working with different LLM providers
with consistent APIs, error handling, and flexible routing.

Supported Providers:
    - Anthropic Claude (direct API) - Haiku, Sonnet, Opus (fully implemented)
    - AWS Bedrock - Claude models via AWS infrastructure (fully implemented)
    - Google Vertex AI - Claude models via Google Cloud (fully implemented)
    - OpenAI GPT - GPT-4o, GPT-4o-mini, gpt-4o (fully implemented)
    - Google Gemini - Gemini 2.5 Pro, Flash, Flash Lite (fully implemented)
    - Mock - Testing provider with zero cost (fully implemented)

Provider Routing:
    Three-tier routing logic:
    1. Explicit prefix: bedrock:claude-sonnet, vertex:claude-opus
    2. Enabled providers: Automatically routes to enabled cloud providers
    3. Fallback: Direct Anthropic API

Example:
    >>> from pm_prompt_toolkit.providers import get_provider
    >>> # Explicit provider selection
    >>> provider = get_provider("bedrock:claude-sonnet-4-5")
    >>> # Automatic routing to enabled provider
    >>> provider = get_provider("claude-sonnet")
    >>> result = provider.classify("We need SSO integration")
    >>> print(result.category, result.confidence)
    feature_request 0.96
    >>> print(result.provider_metadata)
    {'provider': 'bedrock', 'region': 'us-east-1', ...}

Security:
    All providers use credentials from environment variables.
    Never hardcode credentials.
"""

from pm_prompt_toolkit.providers.base import (
    ClassificationResult,
    LLMProvider,
    ProviderMetrics,
    SignalCategory,
)
from pm_prompt_toolkit.providers.bedrock import BedrockProvider
from pm_prompt_toolkit.providers.claude import ClaudeProvider
from pm_prompt_toolkit.providers.factory import ConfigurationError, get_provider
from pm_prompt_toolkit.providers.gemini import GeminiProvider
from pm_prompt_toolkit.providers.mock import MockProvider
from pm_prompt_toolkit.providers.openai import OpenAIProvider
from pm_prompt_toolkit.providers.vertex import VertexProvider

__all__ = [
    "BedrockProvider",
    "ClassificationResult",
    "ClaudeProvider",
    "ConfigurationError",
    "GeminiProvider",
    "LLMProvider",
    "MockProvider",
    "OpenAIProvider",
    "ProviderMetrics",
    "SignalCategory",
    "VertexProvider",
    "get_provider",
]
