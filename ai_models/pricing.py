# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Pricing Service for AI Models

This module provides versioned pricing information with historical tracking
and caching for optimal performance.

Example:
    >>> from ai_models.pricing import PricingService
    >>>
    >>> service = PricingService()
    >>> pricing = service.get_pricing("claude-sonnet-4-5")
    >>> cost = pricing.calculate_cost(input_tokens=1000, output_tokens=500)
    >>> print(f"Cost: ${cost:.4f}")
    Cost: $0.0105
"""

from dataclasses import dataclass
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path
from typing import Dict, Optional

import yaml


@dataclass(frozen=True)
class Pricing:
    """Pricing information for a specific model at a point in time.

    Attributes:
        model_id: Model identifier
        input_per_1m: Cost per 1M input tokens (USD)
        output_per_1m: Cost per 1M output tokens (USD)
        cache_write_per_1m: Cost per 1M cache write tokens (USD, optional)
        cache_read_per_1m: Cost per 1M cache read tokens (USD, optional)
        effective_date: Date this pricing became effective
        verified_date: Date when pricing was last verified
    """

    model_id: str
    input_per_1m: float
    output_per_1m: float
    cache_write_per_1m: Optional[float] = None
    cache_read_per_1m: Optional[float] = None
    effective_date: date = None
    verified_date: date = None

    def calculate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
        cached_input_tokens: int = 0,
    ) -> float:
        """Calculate total cost for token usage.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cached_input_tokens: Number of input tokens served from cache

        Returns:
            Total cost in USD

        Example:
            >>> pricing = Pricing("claude-sonnet-4-5", 3.00, 15.00, 3.75, 0.30)
            >>> # 1000 input (900 cached), 500 output
            >>> cost = pricing.calculate_cost(1000, 500, 900)
            >>> # (100 * 3.00/1M) + (900 * 0.30/1M) + (500 * 15.00/1M)
            >>> # = 0.0003 + 0.00027 + 0.0075 = $0.00807
            >>> print(f"${cost:.5f}")
            $0.00807
        """
        # Calculate uncached input cost
        uncached_input = input_tokens - cached_input_tokens
        input_cost = (uncached_input / 1_000_000) * self.input_per_1m

        # Calculate cached input cost (if applicable)
        cache_cost = 0.0
        if cached_input_tokens > 0 and self.cache_read_per_1m is not None:
            cache_cost = (cached_input_tokens / 1_000_000) * self.cache_read_per_1m

        # Calculate output cost
        output_cost = (output_tokens / 1_000_000) * self.output_per_1m

        return input_cost + cache_cost + output_cost

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary representation."""
        result = {
            "model_id": self.model_id,
            "input_per_1m": self.input_per_1m,
            "output_per_1m": self.output_per_1m,
        }

        if self.cache_write_per_1m is not None:
            result["cache_write_per_1m"] = self.cache_write_per_1m
        if self.cache_read_per_1m is not None:
            result["cache_read_per_1m"] = self.cache_read_per_1m
        if self.effective_date:
            result["effective_date"] = self.effective_date.isoformat()
        if self.verified_date:
            result["verified_date"] = self.verified_date.isoformat()

        return result


class PricingService:
    """Service for retrieving and managing model pricing.

    Features:
        - LRU cache for fast lookups
        - Historical pricing support
        - Automatic YAML loading
        - Fallback to current pricing

    Example:
        >>> service = PricingService()
        >>> pricing = service.get_pricing("claude-haiku-4-5")
        >>> print(f"${pricing.input_per_1m}/1M input")
        $1.00/1M input
    """

    def __init__(self, definitions_dir: Optional[Path] = None):
        """Initialize pricing service.

        Args:
            definitions_dir: Path to model definitions directory.
                           Defaults to ai_models/definitions/
        """
        if definitions_dir is None:
            definitions_dir = Path(__file__).parent / "definitions"

        self.definitions_dir = definitions_dir
        self._pricing_cache: Dict[str, Pricing] = {}
        self._load_all_pricing()

    def _load_all_pricing(self) -> None:
        """Load pricing from all YAML model definitions."""
        if not self.definitions_dir.exists():
            return

        # Find all YAML files
        for yaml_file in self.definitions_dir.rglob("*.yaml"):
            if yaml_file.name == "schema.md":
                continue

            try:
                with open(yaml_file) as f:
                    data = yaml.safe_load(f)

                if not data or "model_id" not in data:
                    continue

                # Extract pricing info
                model_id = data["model_id"]
                pricing_data = data.get("pricing", {})
                metadata = data.get("metadata", {})

                pricing = Pricing(
                    model_id=model_id,
                    input_per_1m=pricing_data.get("input_per_1m", 0.0),
                    output_per_1m=pricing_data.get("output_per_1m", 0.0),
                    cache_write_per_1m=pricing_data.get("cache_write_per_1m"),
                    cache_read_per_1m=pricing_data.get("cache_read_per_1m"),
                    effective_date=self._parse_date(metadata.get("release_date")),
                    verified_date=self._parse_date(metadata.get("last_verified")),
                )

                self._pricing_cache[model_id] = pricing

            except Exception as e:
                print(f"Warning: Failed to load pricing from {yaml_file}: {e}")

    def _parse_date(self, date_str: Optional[str]) -> Optional[date]:
        """Parse ISO date string to date object."""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None

    @lru_cache(maxsize=128)
    def get_pricing(self, model_id: str, as_of_date: Optional[date] = None) -> Optional[Pricing]:
        """Get pricing for a model.

        Args:
            model_id: Model identifier (e.g., "claude-sonnet-4-5")
            as_of_date: Get pricing as of this date (future: historical support)

        Returns:
            Pricing object or None if not found

        Example:
            >>> service = PricingService()
            >>> pricing = service.get_pricing("claude-haiku-4-5")
            >>> pricing.input_per_1m
            1.0
        """
        # For now, ignore as_of_date and return current pricing
        # Future: Support historical pricing queries
        return self._pricing_cache.get(model_id)

    def calculate_cost(
        self,
        model_id: str,
        input_tokens: int,
        output_tokens: int,
        cached_input_tokens: int = 0,
    ) -> float:
        """Calculate cost for a model.

        Args:
            model_id: Model identifier
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cached_input_tokens: Number of cached input tokens

        Returns:
            Cost in USD

        Raises:
            ValueError: If model not found

        Example:
            >>> service = PricingService()
            >>> cost = service.calculate_cost(
            ...     "claude-sonnet-4-5",
            ...     input_tokens=1000,
            ...     output_tokens=500
            ... )
            >>> print(f"${cost:.4f}")
            $0.0105
        """
        pricing = self.get_pricing(model_id)
        if pricing is None:
            raise ValueError(f"Pricing not found for model: {model_id}")

        return pricing.calculate_cost(input_tokens, output_tokens, cached_input_tokens)

    def get_all_pricing(self) -> Dict[str, Pricing]:
        """Get pricing for all models.

        Returns:
            Dictionary mapping model_id to Pricing
        """
        return self._pricing_cache.copy()

    def clear_cache(self) -> None:
        """Clear the LRU cache and reload pricing."""
        self.get_pricing.cache_clear()
        self._pricing_cache.clear()
        self._load_all_pricing()


# Global singleton instance
_pricing_service: Optional[PricingService] = None


def get_pricing_service() -> PricingService:
    """Get global pricing service instance.

    Returns:
        Singleton PricingService instance

    Example:
        >>> from ai_models.pricing import get_pricing_service
        >>> service = get_pricing_service()
        >>> pricing = service.get_pricing("gpt-4o")
    """
    global _pricing_service
    if _pricing_service is None:
        _pricing_service = PricingService()
    return _pricing_service
