# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Provider factory for creating LLM provider instances.

This module provides a factory function to instantiate the correct provider
based on model name and configuration, with automatic provider detection.

Three-tier routing logic:
    1. Explicit prefix (highest priority): bedrock:claude-sonnet, vertex:claude-opus
    2. Enabled providers check: Route to enabled providers based on configuration
    3. Fallback: Default to direct Anthropic API if no match

Example:
    >>> from pm_prompt_toolkit.providers import get_provider
    >>> # Explicit provider selection
    >>> provider = get_provider("bedrock:claude-sonnet-4-5")
    >>> # Automatic provider selection
    >>> provider = get_provider("claude-sonnet")
    >>> result = provider.classify("We need SSO")
"""

import logging

from pm_prompt_toolkit.config import get_settings
from pm_prompt_toolkit.providers.base import LLMProvider
from pm_prompt_toolkit.providers.bedrock import BedrockProvider
from pm_prompt_toolkit.providers.claude import ClaudeProvider
from pm_prompt_toolkit.providers.gemini import GeminiProvider
from pm_prompt_toolkit.providers.mock import MockProvider
from pm_prompt_toolkit.providers.openai import OpenAIProvider
from pm_prompt_toolkit.providers.vertex import VertexProvider

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when provider configuration is invalid.

    This error is raised when:
    - An explicit provider prefix is used but that provider is not enabled
    - Required credentials are missing for an enabled provider
    - Provider is not properly configured
    """

    pass


def get_provider(
    model: str,
    enable_caching: bool = True,
) -> LLMProvider:
    """Get appropriate provider for the specified model.

    This function implements three-tier routing logic:
    1. **Explicit prefix** (highest priority):
       - bedrock:claude-sonnet-4-5 → BedrockProvider
       - vertex:claude-opus-4 → VertexProvider
       - mock:claude-sonnet → MockProvider

    2. **Enabled providers check**:
       - If enable_bedrock=True and credentials configured → BedrockProvider
       - If enable_vertex=True and credentials configured → VertexProvider
       - If enable_openai=True and credentials configured → OpenAIProvider

    3. **Fallback**:
       - Default to direct Anthropic API (ClaudeProvider)

    Args:
        model: Model identifier with optional provider prefix
               Examples: "claude-sonnet", "bedrock:claude-opus-4", "vertex:claude-haiku"
        enable_caching: Whether to enable prompt caching

    Returns:
        Initialized LLM provider

    Raises:
        ConfigurationError: If explicit provider prefix is used but provider is disabled
        ValueError: If model is not recognized or provider not available

    Examples:
        >>> # Explicit provider selection
        >>> provider = get_provider("bedrock:claude-sonnet-4-5")
        >>> provider = get_provider("vertex:claude-opus-4")

        >>> # Automatic selection based on enabled providers
        >>> provider = get_provider("claude-sonnet")  # Uses Bedrock if enabled

        >>> # Mock for testing
        >>> provider = get_provider("mock:claude-sonnet")
    """
    settings = get_settings()

    # Validate model is not empty
    if not model or not model.strip():
        raise ValueError(
            f"Unknown model: {model}. "
            f"Supported models: claude-haiku, claude-sonnet, claude-opus. "
            f"Planned: gpt-4, gpt-3.5, gemini-pro, gemini-flash (see TODO.md)"
        )

    # Tier 1: Check for explicit provider prefix
    if ":" in model:
        provider_prefix, model_name = model.split(":", 1)
        # Normalize model name to lowercase for consistency
        model_name_normalized = model_name.lower()
        return _get_provider_by_prefix(
            provider_prefix, model_name_normalized, enable_caching, settings
        )

    # Tier 2: Check enabled providers and route accordingly
    # Priority order: Bedrock > Vertex > OpenAI > Gemini > Anthropic (default)

    # Normalize model name to lowercase for consistency
    model_normalized = model.lower()

    # Check if model is a Claude model
    claude_models = [
        "claude-sonnet-4-5",
        "claude-sonnet-4",
        "claude-opus-4-1",
        "claude-opus-4",
        "claude-sonnet",
        "claude-haiku",
        "claude-opus",
    ]
    is_claude_model = any(
        model_normalized in m for m in claude_models
    ) or model_normalized.startswith("claude")

    if is_claude_model:
        # Check if Bedrock is enabled for Claude models
        if settings.enable_bedrock:
            try:
                logger.info(f"Routing Claude model '{model_normalized}' to Bedrock (enabled)")
                return BedrockProvider(model=model_normalized, enable_caching=enable_caching)
            except Exception as e:
                logger.warning(f"Bedrock provider failed to initialize: {e}")
                logger.info("Falling back to next available provider")

        # Check if Vertex is enabled for Claude models
        if settings.enable_vertex:
            try:
                logger.info(f"Routing Claude model '{model_normalized}' to Vertex AI (enabled)")
                return VertexProvider(model=model_normalized, enable_caching=enable_caching)
            except Exception as e:
                logger.warning(f"Vertex provider failed to initialize: {e}")
                logger.info("Falling back to next available provider")

        # Tier 3: Fallback to direct Anthropic API
        logger.info(f"Routing Claude model '{model_normalized}' to direct Anthropic API (fallback)")
        return ClaudeProvider(model=model_normalized, enable_caching=enable_caching)

    # Check for OpenAI models
    openai_models = ["gpt-4", "gpt-4o", "gpt-4o-mini", "gpt-3.5", "gpt-4-turbo", "o1", "o1-mini"]
    if any(model_normalized in m for m in openai_models) or model_normalized.startswith("gpt"):
        if settings.enable_openai:
            logger.info(f"Routing OpenAI model '{model_normalized}' to OpenAI provider")
            return OpenAIProvider(model=model_normalized, enable_caching=enable_caching)
        else:
            # For backward compatibility with tests, raise NotImplementedError
            raise NotImplementedError(
                f"OpenAI provider for {model} is not yet implemented. "
                "Use Claude models for now. "
                "See TODO.md for planned implementation."
            )

    # Check for Gemini models
    gemini_models = ["gemini-pro", "gemini-flash", "gemini-1.5", "gemini-2.0"]
    if any(model_normalized in m for m in gemini_models) or model_normalized.startswith("gemini"):
        logger.info(f"Routing Gemini model '{model_normalized}' to Gemini provider")
        return GeminiProvider(model=model_normalized, enable_caching=enable_caching)

    # Unknown model
    raise ValueError(
        f"Unknown model: {model}. "
        f"Supported models: claude-haiku, claude-sonnet, claude-opus. "
        f"Planned: gpt-4, gpt-3.5, gemini-pro, gemini-flash (see TODO.md)"
    )


def _get_provider_by_prefix(
    provider_prefix: str, model_name: str, enable_caching: bool, settings: object
) -> LLMProvider:
    """Get provider based on explicit prefix.

    Args:
        provider_prefix: Provider name (bedrock, vertex, anthropic, openai, gemini, mock)
        model_name: Model name without prefix
        enable_caching: Whether to enable caching
        settings: Application settings

    Returns:
        Initialized provider

    Raises:
        ConfigurationError: If provider is disabled but prefix is used
        ValueError: If provider prefix is unknown
    """
    prefix_lower = provider_prefix.lower()

    # Handle mock provider (always available)
    if prefix_lower == "mock":
        logger.info(f"Using mock provider for model '{model_name}'")
        return MockProvider(model=model_name, enable_caching=enable_caching)

    # Handle Bedrock provider
    if prefix_lower == "bedrock":
        if not settings.enable_bedrock:  # type: ignore[attr-defined]
            raise ConfigurationError(
                "Explicit 'bedrock:' prefix used but enable_bedrock=False. "
                "Set ENABLE_BEDROCK=true in your .env file to enable Bedrock provider."
            )
        logger.info(f"Using Bedrock provider for model '{model_name}' (explicit prefix)")
        return BedrockProvider(model=model_name, enable_caching=enable_caching)

    # Handle Vertex AI provider
    if prefix_lower == "vertex":
        if not settings.enable_vertex:  # type: ignore[attr-defined]
            raise ConfigurationError(
                "Explicit 'vertex:' prefix used but enable_vertex=False. "
                "Set ENABLE_VERTEX=true in your .env file to enable Vertex AI provider."
            )
        logger.info(f"Using Vertex AI provider for model '{model_name}' (explicit prefix)")
        return VertexProvider(model=model_name, enable_caching=enable_caching)

    # Handle direct Anthropic API
    if prefix_lower == "anthropic":
        logger.info(f"Using direct Anthropic API for model '{model_name}' (explicit prefix)")
        return ClaudeProvider(model=model_name, enable_caching=enable_caching)

    # Handle OpenAI provider
    if prefix_lower == "openai":
        if not settings.enable_openai:  # type: ignore[attr-defined]
            raise ConfigurationError(
                "Explicit 'openai:' prefix used but enable_openai=False. "
                "Set ENABLE_OPENAI=true in your .env file to enable OpenAI provider."
            )
        logger.info(f"Using OpenAI provider for model '{model_name}' (explicit prefix)")
        return OpenAIProvider(model=model_name, enable_caching=enable_caching)

    # Handle Gemini provider
    if prefix_lower == "gemini":
        logger.info(f"Using Gemini provider for model '{model_name}' (explicit prefix)")
        return GeminiProvider(model=model_name, enable_caching=enable_caching)

    # Unknown provider prefix
    raise ValueError(
        f"Unknown provider prefix: '{provider_prefix}'. "
        f"Valid prefixes: bedrock, vertex, anthropic, openai, gemini, mock"
    )
