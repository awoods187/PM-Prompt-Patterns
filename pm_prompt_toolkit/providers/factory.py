"""Provider factory for creating LLM provider instances.

This module provides a factory function to instantiate the correct provider
based on model name, with automatic provider detection.

Example:
    >>> from pm_prompt_toolkit.providers import get_provider
    >>> provider = get_provider("claude-sonnet")
    >>> result = provider.classify("We need SSO")
"""

import logging
from typing import Optional

from pm_prompt_toolkit.providers.base import LLMProvider
from pm_prompt_toolkit.providers.claude import ClaudeProvider

logger = logging.getLogger(__name__)


def get_provider(
    model: str,
    enable_caching: bool = True,
) -> LLMProvider:
    """Get appropriate provider for the specified model.

    Args:
        model: Model identifier (e.g., 'claude-sonnet', 'gpt-4', 'gemini-pro')
        enable_caching: Whether to enable prompt caching

    Returns:
        Initialized LLM provider

    Raises:
        ValueError: If model is not recognized or provider not available

    Example:
        >>> provider = get_provider("claude-haiku")
        >>> result = provider.classify("Dashboard is broken")
    """
    model_lower = model.lower()

    # Claude models
    if model_lower in ["claude-haiku", "claude-sonnet", "claude-opus"]:
        return ClaudeProvider(model=model_lower, enable_caching=enable_caching)

    # OpenAI models (not yet implemented)
    if model_lower in ["gpt-4", "gpt-3.5", "gpt-4-turbo"]:
        raise NotImplementedError(
            f"OpenAI provider for {model} is not yet implemented. "
            "Use Claude models for now. "
            "See TODO.md for planned implementation."
        )

    # Gemini models (not yet implemented)
    if model_lower in ["gemini-pro", "gemini-flash"]:
        raise NotImplementedError(
            f"Gemini provider for {model} is not yet implemented. "
            "Use Claude models for now. "
            "See TODO.md for planned implementation."
        )

    # Unknown model
    raise ValueError(
        f"Unknown model: {model}. "
        f"Supported models: claude-haiku, claude-sonnet, claude-opus. "
        f"Planned: gpt-4, gpt-3.5, gemini-pro, gemini-flash (see TODO.md)"
    )
