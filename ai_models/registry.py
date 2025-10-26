# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Unified Model Registry

Auto-loads model definitions from YAML files and provides a single
source of truth for all AI model information.

Example:
    >>> from ai_models import ModelRegistry
    >>>
    >>> # Get model by ID
    >>> model = ModelRegistry.get("claude-sonnet-4-5")
    >>> print(model.name)
    Claude Sonnet 4.5
    >>>
    >>> # Check capability
    >>> if model.has_capability("vision"):
    ...     process_image()
"""

from dataclasses import dataclass, field
from datetime import date
from functools import lru_cache
from pathlib import Path
from typing import Optional, Union

import yaml

from ai_models.capabilities import CapabilityValidator, ModelCapability  # noqa: F401
from ai_models.pricing import Pricing, PricingService  # noqa: F401


@dataclass
class ModelOptimization:
    """Optimization guidance for a model."""

    recommended_for: list[str] = field(default_factory=list)
    best_practices: list[str] = field(default_factory=list)
    cost_tier: str = "mid-tier"  # budget, mid-tier, premium
    speed_tier: str = "balanced"  # fast, balanced, thorough


@dataclass
class ModelMetadata:
    """Metadata about a model."""

    context_window_input: int
    context_window_output: Optional[int]
    knowledge_cutoff: str
    release_date: date
    last_verified: date
    docs_url: str


@dataclass
class Model:
    """Complete model specification.

    This class represents a full model definition loaded from YAML,
    including metadata, capabilities, pricing, and optimization guidance.
    """

    model_id: str
    provider: str
    name: str
    api_identifier: str
    metadata: ModelMetadata
    capabilities: set[ModelCapability]
    pricing: Pricing
    optimization: ModelOptimization
    notes: str = ""

    def has_capability(self, capability: Union[ModelCapability, str]) -> bool:
        """Check if model has a specific capability.

        Args:
            capability: ModelCapability enum or string

        Returns:
            True if model has the capability

        Example:
            >>> model = ModelRegistry.get("claude-sonnet-4-5")
            >>> model.has_capability("vision")
            True
        """
        if isinstance(capability, str):
            capability = ModelCapability.from_string(capability)
        return capability in self.capabilities

    def has_all_capabilities(self, capabilities: list[Union[ModelCapability, str]]) -> bool:
        """Check if model has all specified capabilities."""
        caps = [ModelCapability.from_string(c) if isinstance(c, str) else c for c in capabilities]
        return all(cap in self.capabilities for cap in caps)

    def calculate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
        cached_input_tokens: int = 0,
    ) -> float:
        """Calculate cost for token usage.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cached_input_tokens: Number of cached input tokens

        Returns:
            Cost in USD
        """
        return self.pricing.calculate_cost(input_tokens, output_tokens, cached_input_tokens)

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "model_id": self.model_id,
            "provider": self.provider,
            "name": self.name,
            "api_identifier": self.api_identifier,
            "metadata": {
                "context_window_input": self.metadata.context_window_input,
                "context_window_output": self.metadata.context_window_output,
                "knowledge_cutoff": self.metadata.knowledge_cutoff,
                "release_date": self.metadata.release_date.isoformat(),
                "last_verified": self.metadata.last_verified.isoformat(),
                "docs_url": self.metadata.docs_url,
            },
            "capabilities": [cap.value for cap in self.capabilities],
            "pricing": self.pricing.to_dict(),
            "optimization": {
                "recommended_for": self.optimization.recommended_for,
                "best_practices": self.optimization.best_practices,
                "cost_tier": self.optimization.cost_tier,
                "speed_tier": self.optimization.speed_tier,
            },
            "notes": self.notes,
        }


class ModelRegistry:
    """Central registry for all AI models.

    Automatically loads model definitions from YAML files and provides
    a unified interface for accessing model information.
    """

    _models: dict[str, Model] = {}
    _loaded = False

    @classmethod
    def _load_models(cls) -> None:
        """Load all model definitions from YAML files."""
        if cls._loaded:
            return

        definitions_dir = Path(__file__).parent / "definitions"
        if not definitions_dir.exists():
            print(f"Warning: Definitions directory not found: {definitions_dir}")
            return

        for yaml_file in definitions_dir.rglob("*.yaml"):
            try:
                with open(yaml_file) as f:
                    data = yaml.safe_load(f)

                if not data or "model_id" not in data:
                    continue

                # Parse metadata
                meta_data = data.get("metadata", {})
                metadata = ModelMetadata(
                    context_window_input=meta_data.get("context_window_input", 0),
                    context_window_output=meta_data.get("context_window_output"),
                    knowledge_cutoff=meta_data.get("knowledge_cutoff", "Unknown"),
                    release_date=cls._parse_date(meta_data.get("release_date")),
                    last_verified=cls._parse_date(meta_data.get("last_verified")),
                    docs_url=meta_data.get("docs_url", ""),
                )

                # Parse capabilities
                caps_list = data.get("capabilities", [])
                capabilities = set()
                for cap_str in caps_list:
                    try:
                        capabilities.add(ModelCapability.from_string(cap_str))
                    except ValueError:
                        pass

                # Parse pricing
                pricing_data = data.get("pricing", {})
                pricing = Pricing(
                    model_id=data["model_id"],
                    input_per_1m=pricing_data.get("input_per_1m", 0.0),
                    output_per_1m=pricing_data.get("output_per_1m", 0.0),
                    cache_write_per_1m=pricing_data.get("cache_write_per_1m"),
                    cache_read_per_1m=pricing_data.get("cache_read_per_1m"),
                    effective_date=metadata.release_date,
                    verified_date=metadata.last_verified,
                )

                # Parse optimization
                opt_data = data.get("optimization", {})
                optimization = ModelOptimization(
                    recommended_for=opt_data.get("recommended_for", []),
                    best_practices=opt_data.get("best_practices", []),
                    cost_tier=opt_data.get("cost_tier", "mid-tier"),
                    speed_tier=opt_data.get("speed_tier", "balanced"),
                )

                # Create model
                model = Model(
                    model_id=data["model_id"],
                    provider=data.get("provider", "unknown"),
                    name=data.get("name", data["model_id"]),
                    api_identifier=data.get("api_identifier", data["model_id"]),
                    metadata=metadata,
                    capabilities=capabilities,
                    pricing=pricing,
                    optimization=optimization,
                    notes=data.get("notes", ""),
                )

                cls._models[model.model_id] = model

            except Exception as e:
                print(f"Warning: Failed to load model from {yaml_file}: {e}")

        cls._loaded = True

    @classmethod
    def _parse_date(cls, date_str: Optional[str]) -> date:
        """Parse ISO date string."""
        if not date_str:
            return date.today()
        try:
            from datetime import datetime

            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return date.today()

    @classmethod
    @lru_cache(maxsize=128)
    def get(cls, model_id: str) -> Optional[Model]:
        """Get model by ID.

        Args:
            model_id: Model identifier (e.g., "claude-sonnet-4-5")

        Returns:
            Model object or None if not found

        Example:
            >>> model = ModelRegistry.get("claude-haiku-4-5")
            >>> model.name
            'Claude Haiku 4.5'
        """
        cls._load_models()
        return cls._models.get(model_id)

    @classmethod
    def get_all(cls) -> dict[str, Model]:
        """Get all models.

        Returns:
            Dictionary mapping model_id to Model

        Example:
            >>> models = ModelRegistry.get_all()
            >>> len(models)
            8
        """
        cls._load_models()
        return cls._models.copy()

    @classmethod
    def get_by_provider(cls, provider: str) -> list[Model]:
        """Get all models from a specific provider.

        Args:
            provider: Provider name ("anthropic", "openai", "google")

        Returns:
            List of Model objects

        Example:
            >>> models = ModelRegistry.get_by_provider("anthropic")
            >>> len(models)
            3
        """
        cls._load_models()
        return [
            model for model in cls._models.values() if model.provider.lower() == provider.lower()
        ]

    @classmethod
    def filter_by_capability(cls, capability: Union[ModelCapability, str]) -> list[Model]:
        """Get all models with a specific capability.

        Args:
            capability: Capability to filter by

        Returns:
            List of Model objects

        Example:
            >>> models = ModelRegistry.filter_by_capability("prompt_caching")
            >>> all(m.has_capability("prompt_caching") for m in models)
            True
        """
        cls._load_models()
        if isinstance(capability, str):
            capability = ModelCapability.from_string(capability)

        return [model for model in cls._models.values() if capability in model.capabilities]

    @classmethod
    def filter_by_cost_tier(cls, tier: str) -> list[Model]:
        """Get all models in a specific cost tier.

        Args:
            tier: Cost tier ("budget", "mid-tier", "premium")

        Returns:
            List of Model objects

        Example:
            >>> budget_models = ModelRegistry.filter_by_cost_tier("budget")
            >>> len(budget_models) >= 3  # Haiku, 4o-mini, Flash, Flash-Lite
            True
        """
        cls._load_models()
        return [model for model in cls._models.values() if model.optimization.cost_tier == tier]

    @classmethod
    def clear_cache(cls) -> None:
        """Clear all caches and force reload."""
        cls.get.cache_clear()
        cls._models.clear()
        cls._loaded = False


# Convenience functions
def get_model(model_id: str) -> Optional[Model]:
    """Get model by ID (convenience function).

    Args:
        model_id: Model identifier

    Returns:
        Model object or None
    """
    return ModelRegistry.get(model_id)


def list_models() -> list[str]:
    """List all available model IDs.

    Returns:
        List of model identifiers
    """
    return list(ModelRegistry.get_all().keys())


def list_providers() -> list[str]:
    """List all available providers.

    Returns:
        List of unique provider names
    """
    models = ModelRegistry.get_all()
    return list({model.provider for model in models.values()})
