# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
Multi-provider prompt registry and management.

This module provides a unified interface for loading and managing prompts
optimized for different LLM providers (Claude, OpenAI, Gemini).

Example:
    >>> from ai_models.prompts import PromptRegistry, get_prompt
    >>> # Auto-select best variant for model
    >>> prompt = get_prompt("signal-classification", model="gpt-4o")
    >>> # Explicit provider selection
    >>> prompt = get_prompt("signal-classification", provider="openai")
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class PromptRegistry:
    """Registry for multi-provider prompt management."""

    # Base directory for prompts
    PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

    # Provider name mapping
    PROVIDER_MAP = {
        "claude": ["claude", "anthropic"],
        "openai": ["gpt", "openai"],
        "gemini": ["gemini", "google"],
    }

    @classmethod
    def get_prompt(
        cls, prompt_name: str, provider: Optional[str] = None, model: Optional[str] = None
    ) -> str:
        """
        Load the best prompt variant for the given provider or model.

        Args:
            prompt_name: Name/path of the prompt (e.g., "analytics/signal-classification")
            provider: Optional provider name (claude, openai, gemini)
            model: Optional model name for auto-detection (e.g., "gpt-4o", "claude-sonnet")

        Returns:
            Prompt content optimized for the provider

        Raises:
            FileNotFoundError: If no prompt found for the given name
            ValueError: If both provider and model specified

        Example:
            >>> # Auto-detect from model name
            >>> prompt = PromptRegistry.get_prompt("signal-classification", model="gpt-4o")
            >>> # Explicit provider
            >>> prompt = PromptRegistry.get_prompt("signal-classification", provider="openai")
        """
        if provider and model:
            raise ValueError("Specify either provider or model, not both")

        # Auto-detect provider from model name
        if model and not provider:
            provider = cls._detect_provider(model)

        # Find prompt directory
        prompt_path = cls._resolve_prompt_path(prompt_name)

        if not prompt_path or not prompt_path.exists():
            raise FileNotFoundError(
                f"Prompt '{prompt_name}' not found in {cls.PROMPTS_DIR}. "
                f"Available prompts: {cls.list_prompts()}"
            )

        # Try provider-specific variant first
        if provider:
            provider_file = prompt_path / f"prompt.{provider}.md"
            if provider_file.exists():
                logger.info(f"Loading {provider}-optimized prompt: {prompt_name}")
                return provider_file.read_text(encoding="utf-8")

        # Fall back to base prompt
        base_file = prompt_path / "prompt.md"
        if base_file.exists():
            logger.info(f"Loading base prompt: {prompt_name}")
            return base_file.read_text(encoding="utf-8")

        # If directory exists but no prompt files, raise helpful error
        raise FileNotFoundError(
            f"No prompt files found in {prompt_path}. "
            f"Expected 'prompt.md' or 'prompt.{provider}.md'"
        )

    @classmethod
    def list_variants(cls, prompt_name: str) -> Dict[str, Path]:
        """
        List all available variants for a prompt.

        Args:
            prompt_name: Name/path of the prompt

        Returns:
            Dict mapping variant names to file paths

        Example:
            >>> variants = PromptRegistry.list_variants("signal-classification")
            >>> print(variants.keys())
            dict_keys(['base', 'claude', 'openai', 'gemini'])
        """
        prompt_path = cls._resolve_prompt_path(prompt_name)

        if not prompt_path or not prompt_path.exists():
            return {}

        variants = {}

        # Check for base prompt
        base_file = prompt_path / "prompt.md"
        if base_file.exists():
            variants["base"] = base_file

        # Check for provider-specific variants
        for provider_file in prompt_path.glob("prompt.*.md"):
            if provider_file.stem != "prompt":
                # Extract provider name from prompt.{provider}.md
                provider = provider_file.stem.split(".")[-1]
                variants[provider] = provider_file

        return variants

    @classmethod
    def list_prompts(cls) -> List[str]:
        """
        List all available prompts in the registry.

        Returns:
            List of prompt names (relative paths from prompts directory)

        Example:
            >>> prompts = PromptRegistry.list_prompts()
            >>> print(prompts[:3])
            ['analytics/signal-classification', 'analytics/epic-categorization', ...]
        """
        if not cls.PROMPTS_DIR.exists():
            return []

        prompts = []
        for prompt_dir in cls.PROMPTS_DIR.rglob("*"):
            if not prompt_dir.is_dir():
                continue

            # Check if directory contains any prompt files
            has_prompts = any(
                f.name.startswith("prompt") and f.suffix == ".md" for f in prompt_dir.glob("*.md")
            )

            if has_prompts:
                # Get relative path from prompts directory
                rel_path = prompt_dir.relative_to(cls.PROMPTS_DIR)
                prompts.append(str(rel_path))

        return sorted(prompts)

    @classmethod
    def has_provider_variant(cls, prompt_name: str, provider: str) -> bool:
        """
        Check if a provider-specific variant exists for a prompt.

        Args:
            prompt_name: Name/path of the prompt
            provider: Provider name to check

        Returns:
            True if provider variant exists

        Example:
            >>> PromptRegistry.has_provider_variant("signal-classification", "openai")
            True
        """
        prompt_path = cls._resolve_prompt_path(prompt_name)
        if not prompt_path:
            return False

        provider_file = prompt_path / f"prompt.{provider}.md"
        return provider_file.exists()

    @classmethod
    def _detect_provider(cls, model_name: str) -> Optional[str]:
        """
        Detect provider from model name.

        Args:
            model_name: Model identifier (e.g., "gpt-4o", "claude-sonnet-4-5")

        Returns:
            Provider name or None if not detected
        """
        model_lower = model_name.lower()

        for provider, keywords in cls.PROVIDER_MAP.items():
            if any(keyword in model_lower for keyword in keywords):
                return provider

        return None

    @classmethod
    def _resolve_prompt_path(cls, prompt_name: str) -> Optional[Path]:
        """
        Resolve prompt name to directory path.

        Handles both direct paths and fuzzy matching.

        Args:
            prompt_name: Prompt name or path

        Returns:
            Path to prompt directory or None if not found
        """
        # Direct path
        direct_path = cls.PROMPTS_DIR / prompt_name
        if direct_path.exists() and direct_path.is_dir():
            return direct_path

        # Try without extension if provided
        if prompt_name.endswith(".md"):
            prompt_name = prompt_name[:-3]
            direct_path = cls.PROMPTS_DIR / prompt_name
            if direct_path.exists() and direct_path.is_dir():
                return direct_path

        return None


# Convenience function
def get_prompt(
    prompt_name: str, provider: Optional[str] = None, model: Optional[str] = None
) -> str:
    """
    Convenience function to get a prompt.

    Args:
        prompt_name: Name/path of the prompt
        provider: Optional provider name (claude, openai, gemini)
        model: Optional model name for auto-detection

    Returns:
        Prompt content optimized for the provider

    Example:
        >>> from ai_models import get_prompt
        >>> prompt = get_prompt("signal-classification", model="gpt-4o")
    """
    return PromptRegistry.get_prompt(prompt_name, provider=provider, model=model)


def list_prompts() -> List[str]:
    """
    List all available prompts.

    Returns:
        List of prompt names

    Example:
        >>> from ai_models import list_prompts
        >>> prompts = list_prompts()
    """
    return PromptRegistry.list_prompts()


def list_variants(prompt_name: str) -> Dict[str, Path]:
    """
    List all available variants for a prompt.

    Args:
        prompt_name: Name/path of the prompt

    Returns:
        Dict mapping variant names to file paths

    Example:
        >>> from ai_models import list_variants
        >>> variants = list_variants("signal-classification")
    """
    return PromptRegistry.list_variants(prompt_name)
