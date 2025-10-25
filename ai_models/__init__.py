# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""AI Models Package

Unified interface for AI model specifications, pricing, and capabilities.

Example:
    >>> from ai_models import ModelRegistry, get_model
    >>>
    >>> # Get a model
    >>> model = get_model("claude-sonnet-4-5")
    >>> print(f"{model.name}: ${model.pricing.input_per_1m}/1M tokens")
    >>>
    >>> # Check capabilities
    >>> if model.has_capability("vision"):
    ...     print("Supports vision!")
    >>>
    >>> # Calculate cost
    >>> cost = model.calculate_cost(input_tokens=1000, output_tokens=500)
    >>> print(f"Cost: ${cost:.4f}")
"""

from ai_models.registry import (
    ModelRegistry,
    Model,
    ModelMetadata,
    ModelOptimization,
    get_model,
    list_models,
    list_providers,
)

from ai_models.capabilities import (
    ModelCapability,
    CapabilityValidator,
    has_vision,
    has_function_calling,
    has_prompt_caching,
    supports_large_context,
)

from ai_models.pricing import (
    PricingService,
    Pricing,
    get_pricing_service,
)

__all__ = [
    # Registry
    "ModelRegistry",
    "Model",
    "ModelMetadata",
    "ModelOptimization",
    "get_model",
    "list_models",
    "list_providers",
    # Capabilities
    "ModelCapability",
    "CapabilityValidator",
    "has_vision",
    "has_function_calling",
    "has_prompt_caching",
    "supports_large_context",
    # Pricing
    "PricingService",
    "Pricing",
    "get_pricing_service",
]

__version__ = "1.0.0"
