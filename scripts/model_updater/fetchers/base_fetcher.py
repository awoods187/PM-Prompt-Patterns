# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Base fetcher abstract class for model data retrieval."""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


@dataclass
class ModelData:
    """Normalized model data structure matching YAML schema."""

    model_id: str
    provider: str
    name: str
    api_identifier: str

    # Metadata
    context_window_input: int
    context_window_output: Optional[int]
    knowledge_cutoff: str
    release_date: date
    docs_url: str

    # Capabilities
    capabilities: list[str] = field(default_factory=list)

    # Pricing (per 1M tokens)
    input_per_1m: float = 0.0
    output_per_1m: float = 0.0
    cache_write_per_1m: Optional[float] = None
    cache_read_per_1m: Optional[float] = None

    # Optimization
    recommended_for: list[str] = field(default_factory=list)
    best_practices: list[str] = field(default_factory=list)
    cost_tier: str = "mid-tier"
    speed_tier: str = "balanced"

    # Additional info
    notes: str = ""
    source: str = ""  # Where this data was fetched from
    fetch_timestamp: datetime = field(default_factory=datetime.now)

    def to_yaml_dict(self) -> dict[str, Any]:
        """Convert to YAML-compatible dictionary."""
        return {
            "schema_version": "1.0.0",
            "model_id": self.model_id,
            "provider": self.provider,
            "name": self.name,
            "api_identifier": self.api_identifier,
            "metadata": {
                "context_window_input": self.context_window_input,
                "context_window_output": self.context_window_output,
                "knowledge_cutoff": self.knowledge_cutoff,
                "release_date": self.release_date.isoformat(),
                "last_verified": date.today().isoformat(),
                "docs_url": self.docs_url,
            },
            "capabilities": self.capabilities,
            "pricing": {
                "input_per_1m": self.input_per_1m,
                "output_per_1m": self.output_per_1m,
                **(
                    {"cache_write_per_1m": self.cache_write_per_1m}
                    if self.cache_write_per_1m is not None
                    else {}
                ),
                **(
                    {"cache_read_per_1m": self.cache_read_per_1m}
                    if self.cache_read_per_1m is not None
                    else {}
                ),
            },
            "optimization": {
                "recommended_for": self.recommended_for,
                "best_practices": self.best_practices,
                "cost_tier": self.cost_tier,
                "speed_tier": self.speed_tier,
            },
            "notes": self.notes,
        }


class BaseFetcher(ABC):
    """Abstract base class for model data fetchers.

    Each provider should implement a fetcher that inherits from this class
    and implements the fetch_models method.
    """

    def __init__(self, cache_ttl: int = 3600) -> None:
        """Initialize fetcher.

        Args:
            cache_ttl: Cache time-to-live in seconds (default 1 hour)
        """
        self.cache_ttl = cache_ttl
        self.logger = logging.getLogger(self.__class__.__name__)
        self._cache: dict[str, tuple[datetime, list[ModelData]]] = {}

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name (e.g., 'anthropic', 'openai')."""
        pass

    @abstractmethod
    def fetch_models(self) -> list[ModelData]:
        """Fetch all models from the provider.

        This method should:
        1. Try API first (if available)
        2. Fallback to documentation parsing
        3. Handle errors gracefully
        4. Return normalized ModelData objects

        Returns:
            List of ModelData objects

        Raises:
            Exception: If fetching fails from all sources
        """
        pass

    def fetch_with_cache(self) -> list[ModelData]:
        """Fetch models with caching support.

        Returns:
            List of ModelData objects
        """
        cache_key = self.provider_name
        if cache_key in self._cache:
            cached_time, cached_data = self._cache[cache_key]
            age = (datetime.now() - cached_time).total_seconds()
            if age < self.cache_ttl:
                self.logger.info(f"Using cached data for {self.provider_name} (age: {age:.0f}s)")
                return cached_data

        self.logger.info(f"Fetching fresh data for {self.provider_name}")
        models = self.fetch_models()
        self._cache[cache_key] = (datetime.now(), models)
        return models

    def fetch_from_api(self) -> list[ModelData]:
        """Fetch models from API (if available).

        Override this method if the provider has an API.

        Returns:
            List of ModelData objects

        Raises:
            NotImplementedError: If provider doesn't support API fetching
        """
        raise NotImplementedError(f"{self.provider_name} does not support API fetching")

    def fetch_from_docs(self) -> list[ModelData]:
        """Fetch models from documentation (fallback).

        Override this method to parse provider documentation.

        Returns:
            List of ModelData objects

        Raises:
            NotImplementedError: If provider doesn't support docs parsing
        """
        raise NotImplementedError(f"{self.provider_name} does not support documentation parsing")

    def validate_model_data(self, model: ModelData) -> tuple[bool, list[str]]:
        """Validate model data for sanity checks.

        Args:
            model: ModelData object to validate

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        # Required fields
        if not model.model_id:
            errors.append("model_id is required")
        if not model.name:
            errors.append("name is required")
        if not model.api_identifier:
            errors.append("api_identifier is required")
        if not model.docs_url:
            errors.append("docs_url is required")

        # Context window validation
        if model.context_window_input <= 0:
            errors.append(f"Invalid context_window_input: {model.context_window_input}")
        if model.context_window_input > 10_000_000:
            errors.append(f"Suspiciously large context_window_input: {model.context_window_input}")

        # Pricing validation
        if model.input_per_1m < 0:
            errors.append(f"Invalid input_per_1m: {model.input_per_1m}")
        if model.output_per_1m < 0:
            errors.append(f"Invalid output_per_1m: {model.output_per_1m}")
        if model.input_per_1m > 1000:
            errors.append(f"Suspiciously high input_per_1m: {model.input_per_1m}")
        if model.output_per_1m > 5000:
            errors.append(f"Suspiciously high output_per_1m: {model.output_per_1m}")

        # Cache pricing validation (if applicable)
        if model.cache_write_per_1m is not None and model.cache_write_per_1m < 0:
            errors.append(f"Invalid cache_write_per_1m: {model.cache_write_per_1m}")
        if model.cache_read_per_1m is not None and model.cache_read_per_1m < 0:
            errors.append(f"Invalid cache_read_per_1m: {model.cache_read_per_1m}")

        # Capabilities validation
        if not model.capabilities:
            errors.append("At least one capability required")

        valid_capabilities = {
            "text_input",
            "text_output",
            "function_calling",
            "vision",
            "audio_input",
            "audio_output",
            "large_context",
            "prompt_caching",
            "streaming",
            "json_mode",
            "tool_use",
        }
        invalid_caps = set(model.capabilities) - valid_capabilities
        if invalid_caps:
            errors.append(f"Invalid capabilities: {invalid_caps}")

        # Tier validation
        valid_cost_tiers = {"budget", "mid-tier", "premium"}
        if model.cost_tier not in valid_cost_tiers:
            errors.append(f"Invalid cost_tier: {model.cost_tier}")

        valid_speed_tiers = {"fast", "balanced", "thorough"}
        if model.speed_tier not in valid_speed_tiers:
            errors.append(f"Invalid speed_tier: {model.speed_tier}")

        return len(errors) == 0, errors

    def retry_with_backoff(
        self, func: Callable[[], Any], max_retries: int = 3, initial_delay: float = 1.0
    ) -> Any:
        """Retry a function with exponential backoff.

        Args:
            func: Function to retry
            max_retries: Maximum number of retries
            initial_delay: Initial delay in seconds

        Returns:
            Function result

        Raises:
            Exception: If all retries fail
        """
        import time

        delay = initial_delay
        last_exception = None

        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                last_exception = e
                if attempt < max_retries - 1:
                    self.logger.warning(
                        f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s..."
                    )
                    time.sleep(delay)
                    delay *= 2
                else:
                    self.logger.error(f"All {max_retries} attempts failed")

        raise last_exception  # type: ignore
