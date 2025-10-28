# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Model Capability System

Defines and validates AI model capabilities for runtime feature checking.

Example:
    >>> from ai_models.capabilities import ModelCapability, CapabilityValidator
    >>>
    >>> # Check if model supports vision
    >>> if CapabilityValidator.has_capability("claude-sonnet-4-5", ModelCapability.VISION):
    ...     process_image()
"""

from enum import Enum
from pathlib import Path
from typing import ClassVar

import yaml


class ModelCapability(str, Enum):
    """Enumeration of AI model capabilities.

    These capabilities can be checked at runtime to determine
    what features a model supports.
    """

    # Core I/O
    TEXT_INPUT = "text_input"
    TEXT_OUTPUT = "text_output"

    # Advanced Features
    FUNCTION_CALLING = "function_calling"
    VISION = "vision"
    STREAMING = "streaming"
    JSON_MODE = "json_mode"

    # Context & Caching
    LARGE_CONTEXT = "large_context"  # >32k tokens
    PROMPT_CACHING = "prompt_caching"

    # Specialized
    CODE_EXECUTION = "code_execution"
    SEARCH = "search"

    def __str__(self) -> str:
        """String representation."""
        return self.value

    @classmethod
    def from_string(cls, value: str) -> "ModelCapability":
        """Create capability from string.

        Args:
            value: Capability string (e.g., "vision")

        Returns:
            ModelCapability enum

        Raises:
            ValueError: If invalid capability string
        """
        try:
            return cls(value)
        except ValueError:
            valid = ", ".join(c.value for c in cls)
            raise ValueError(f"Invalid capability '{value}'. Valid: {valid}") from None


class CapabilityValidator:
    """Validates and checks model capabilities.

    This class loads capabilities from YAML definitions and provides
    fast lookup for runtime capability checking.
    """

    _capabilities_cache: ClassVar[dict[str, set[ModelCapability]]] = {}
    _loaded: ClassVar[bool] = False

    @classmethod
    def _load_capabilities(cls) -> None:
        """Load capabilities from YAML model definitions."""
        if cls._loaded:
            return

        definitions_dir = Path(__file__).parent / "definitions"
        if not definitions_dir.exists():
            return

        for yaml_file in definitions_dir.rglob("*.yaml"):
            try:
                with open(yaml_file) as f:
                    data = yaml.safe_load(f)

                if not data or "model_id" not in data:
                    continue

                model_id = data["model_id"]
                capabilities_list = data.get("capabilities", [])

                # Convert to ModelCapability enums
                capabilities = set()
                for cap_str in capabilities_list:
                    try:
                        cap = ModelCapability.from_string(cap_str)
                        capabilities.add(cap)
                    except ValueError as e:
                        print(f"Warning: {yaml_file}: {e}")

                cls._capabilities_cache[model_id] = capabilities

            except Exception as e:
                print(f"Warning: Failed to load capabilities from {yaml_file}: {e}")

        cls._loaded = True

    @classmethod
    def get_capabilities(cls, model_id: str) -> set[ModelCapability]:
        """Get all capabilities for a model.

        Args:
            model_id: Model identifier

        Returns:
            Set of ModelCapability enums

        Example:
            >>> caps = CapabilityValidator.get_capabilities("claude-sonnet-4-5")
            >>> ModelCapability.VISION in caps
            True
        """
        cls._load_capabilities()
        return cls._capabilities_cache.get(model_id, set()).copy()

    @classmethod
    def has_capability(cls, model_id: str, capability: ModelCapability) -> bool:
        """Check if model has a specific capability.

        Args:
            model_id: Model identifier
            capability: Capability to check

        Returns:
            True if model has the capability

        Example:
            >>> CapabilityValidator.has_capability(
            ...     "claude-haiku-4-5",
            ...     ModelCapability.FUNCTION_CALLING
            ... )
            True
        """
        caps = cls.get_capabilities(model_id)
        return capability in caps

    @classmethod
    def has_all_capabilities(cls, model_id: str, capabilities: list[ModelCapability]) -> bool:
        """Check if model has all specified capabilities.

        Args:
            model_id: Model identifier
            capabilities: List of required capabilities

        Returns:
            True if model has all capabilities

        Example:
            >>> CapabilityValidator.has_all_capabilities(
            ...     "gpt-4o",
            ...     [ModelCapability.VISION, ModelCapability.FUNCTION_CALLING]
            ... )
            True
        """
        model_caps = cls.get_capabilities(model_id)
        return all(cap in model_caps for cap in capabilities)

    @classmethod
    def has_any_capability(cls, model_id: str, capabilities: list[ModelCapability]) -> bool:
        """Check if model has any of the specified capabilities.

        Args:
            model_id: Model identifier
            capabilities: List of capabilities to check

        Returns:
            True if model has at least one capability

        Example:
            >>> CapabilityValidator.has_any_capability(
            ...     "gemini-2-5-flash-lite",
            ...     [ModelCapability.FUNCTION_CALLING, ModelCapability.VISION]
            ... )
            True  # Has vision but not function calling
        """
        model_caps = cls.get_capabilities(model_id)
        return any(cap in model_caps for cap in capabilities)

    @classmethod
    def filter_models_by_capability(cls, capability: ModelCapability) -> list[str]:
        """Get all models that have a specific capability.

        Args:
            capability: Capability to filter by

        Returns:
            List of model IDs

        Example:
            >>> models = CapabilityValidator.filter_models_by_capability(
            ...     ModelCapability.PROMPT_CACHING
            ... )
            >>> "claude-sonnet-4-5" in models
            True
        """
        cls._load_capabilities()
        return [
            model_id for model_id, caps in cls._capabilities_cache.items() if capability in caps
        ]

    @classmethod
    def get_capability_matrix(cls) -> dict[str, set[str]]:
        """Get complete capability matrix for all models.

        Returns:
            Dictionary mapping model_id to set of capability strings

        Example:
            >>> matrix = CapabilityValidator.get_capability_matrix()
            >>> matrix["claude-sonnet-4-5"]
            {'text_input', 'text_output', 'vision', ...}
        """
        cls._load_capabilities()
        return {
            model_id: {cap.value for cap in caps}
            for model_id, caps in cls._capabilities_cache.items()
        }

    @classmethod
    def clear_cache(cls) -> None:
        """Clear cached capabilities and force reload."""
        cls._capabilities_cache.clear()
        cls._loaded = False


# Convenience functions
def has_vision(model_id: str) -> bool:
    """Check if model supports vision.

    Args:
        model_id: Model identifier

    Returns:
        True if model has vision capability
    """
    return CapabilityValidator.has_capability(model_id, ModelCapability.VISION)


def has_function_calling(model_id: str) -> bool:
    """Check if model supports function calling.

    Args:
        model_id: Model identifier

    Returns:
        True if model has function calling capability
    """
    return CapabilityValidator.has_capability(model_id, ModelCapability.FUNCTION_CALLING)


def has_prompt_caching(model_id: str) -> bool:
    """Check if model supports prompt caching.

    Args:
        model_id: Model identifier

    Returns:
        True if model has prompt caching capability
    """
    return CapabilityValidator.has_capability(model_id, ModelCapability.PROMPT_CACHING)


def supports_large_context(model_id: str) -> bool:
    """Check if model has large context window (>32k).

    Args:
        model_id: Model identifier

    Returns:
        True if model supports large context
    """
    return CapabilityValidator.has_capability(model_id, ModelCapability.LARGE_CONTEXT)
