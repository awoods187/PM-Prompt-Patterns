# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Model data validation."""

import logging
from dataclasses import dataclass, field
from datetime import date
from typing import Any

from scripts.model_updater.fetchers.base_fetcher import ModelData

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of model validation."""

    model_id: str
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class ModelValidator:
    """Validates fetched model data."""

    # Valid capability values
    VALID_CAPABILITIES = {
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

    # Valid tier values
    VALID_COST_TIERS = {"budget", "mid-tier", "premium"}
    VALID_SPEED_TIERS = {"fast", "balanced", "thorough"}

    # Reasonable ranges
    MIN_CONTEXT_WINDOW = 1000
    MAX_CONTEXT_WINDOW = 10_000_000  # 10M tokens
    MIN_PRICE_PER_1M = 0.0
    MAX_PRICE_PER_1M = 1000.0  # $1000 per 1M tokens
    MIN_RELEASE_YEAR = 2020
    MAX_FUTURE_YEARS = 2  # Allow up to 2 years in future

    def __init__(self) -> None:
        """Initialize validator."""
        self.logger = logging.getLogger(self.__class__.__name__)

    def validate(self, model: ModelData) -> ValidationResult:
        """Validate a model's data.

        Args:
            model: ModelData object to validate

        Returns:
            ValidationResult with errors and warnings
        """
        result = ValidationResult(model_id=model.model_id, is_valid=True)

        # Required fields
        self._check_required_fields(model, result)

        # Validate identifiers
        self._validate_identifiers(model, result)

        # Validate context windows
        self._validate_context_windows(model, result)

        # Validate pricing
        self._validate_pricing(model, result)

        # Validate capabilities
        self._validate_capabilities(model, result)

        # Validate tiers
        self._validate_tiers(model, result)

        # Validate dates
        self._validate_dates(model, result)

        # Validate URLs
        self._validate_urls(model, result)

        # Set overall validity
        result.is_valid = len(result.errors) == 0

        if result.errors:
            self.logger.error(f"Validation failed for {model.model_id}: {result.errors}")
        elif result.warnings:
            self.logger.warning(f"Validation warnings for {model.model_id}: {result.warnings}")
        else:
            self.logger.info(f"Validation passed for {model.model_id}")

        return result

    def _check_required_fields(self, model: ModelData, result: ValidationResult) -> None:
        """Check required fields are present."""
        if not model.model_id:
            result.errors.append("model_id is required")
        if not model.provider:
            result.errors.append("provider is required")
        if not model.name:
            result.errors.append("name is required")
        if not model.api_identifier:
            result.errors.append("api_identifier is required")
        if not model.docs_url:
            result.errors.append("docs_url is required")

    def _validate_identifiers(self, model: ModelData, result: ValidationResult) -> None:
        """Validate identifier formats."""
        # Model ID should be kebab-case
        if model.model_id and not all(c.isalnum() or c in ["-", "."] for c in model.model_id):
            result.warnings.append(
                f"model_id '{model.model_id}' should use kebab-case (lowercase, hyphens, dots)"
            )

        # Provider should be lowercase
        if model.provider and model.provider != model.provider.lower():
            result.errors.append(f"provider '{model.provider}' should be lowercase")

    def _validate_context_windows(self, model: ModelData, result: ValidationResult) -> None:
        """Validate context window sizes."""
        # Input context window
        if model.context_window_input <= 0:
            result.errors.append(
                f"context_window_input must be positive, got {model.context_window_input}"
            )
        elif model.context_window_input < self.MIN_CONTEXT_WINDOW:
            result.warnings.append(
                f"context_window_input ({model.context_window_input}) seems unusually small"
            )
        elif model.context_window_input > self.MAX_CONTEXT_WINDOW:
            result.errors.append(
                f"context_window_input ({model.context_window_input}) exceeds maximum "
                f"({self.MAX_CONTEXT_WINDOW})"
            )

        # Output context window (if specified)
        if model.context_window_output is not None:
            if model.context_window_output <= 0:
                result.errors.append(
                    f"context_window_output must be positive, got {model.context_window_output}"
                )
            elif model.context_window_output > model.context_window_input:
                result.warnings.append(
                    f"context_window_output ({model.context_window_output}) larger than input "
                    f"({model.context_window_input})"
                )

    def _validate_pricing(self, model: ModelData, result: ValidationResult) -> None:
        """Validate pricing values."""
        # Input pricing
        if model.input_per_1m < self.MIN_PRICE_PER_1M:
            result.errors.append(f"input_per_1m must be non-negative, got {model.input_per_1m}")
        elif model.input_per_1m > self.MAX_PRICE_PER_1M:
            result.warnings.append(f"input_per_1m (${model.input_per_1m}) seems unusually high")

        # Output pricing
        if model.output_per_1m < self.MIN_PRICE_PER_1M:
            result.errors.append(f"output_per_1m must be non-negative, got {model.output_per_1m}")
        elif model.output_per_1m > self.MAX_PRICE_PER_1M:
            result.warnings.append(f"output_per_1m (${model.output_per_1m}) seems unusually high")

        # Output should typically cost more than input
        if model.output_per_1m < model.input_per_1m:
            result.warnings.append(
                f"output_per_1m (${model.output_per_1m}) is less than input_per_1m "
                f"(${model.input_per_1m}), which is unusual"
            )

        # Cache pricing (if specified)
        if model.cache_write_per_1m is not None:
            if model.cache_write_per_1m < self.MIN_PRICE_PER_1M:
                result.errors.append(
                    f"cache_write_per_1m must be non-negative, got {model.cache_write_per_1m}"
                )
            elif model.cache_write_per_1m < model.input_per_1m:
                result.warnings.append("cache_write_per_1m should typically be >= input_per_1m")

        if model.cache_read_per_1m is not None:
            if model.cache_read_per_1m < self.MIN_PRICE_PER_1M:
                result.errors.append(
                    f"cache_read_per_1m must be non-negative, got {model.cache_read_per_1m}"
                )
            elif model.cache_read_per_1m > model.input_per_1m:
                result.warnings.append("cache_read_per_1m should typically be < input_per_1m")

    def _validate_capabilities(self, model: ModelData, result: ValidationResult) -> None:
        """Validate capabilities."""
        if not model.capabilities:
            result.errors.append("At least one capability is required")

        # Check for invalid capabilities
        invalid_caps = set(model.capabilities) - self.VALID_CAPABILITIES
        if invalid_caps:
            result.errors.append(f"Invalid capabilities: {invalid_caps}")

        # Sanity checks for common capability combinations
        caps_set = set(model.capabilities)

        # Should have both text_input and text_output (all LLMs do)
        if "text_output" not in caps_set:
            result.warnings.append("Model should have text_output capability")

    def _validate_tiers(self, model: ModelData, result: ValidationResult) -> None:
        """Validate tier classifications."""
        if model.cost_tier not in self.VALID_COST_TIERS:
            result.errors.append(
                f"Invalid cost_tier '{model.cost_tier}', must be one of {self.VALID_COST_TIERS}"
            )

        if model.speed_tier not in self.VALID_SPEED_TIERS:
            result.errors.append(
                f"Invalid speed_tier '{model.speed_tier}', must be one of {self.VALID_SPEED_TIERS}"
            )

        # Sanity check: budget models should have lower pricing
        if model.cost_tier == "budget" and model.input_per_1m > 1.0:
            result.warnings.append(f"Budget model has high input price (${model.input_per_1m})")

        # Premium models should have higher pricing
        if model.cost_tier == "premium" and model.input_per_1m < 5.0:
            result.warnings.append(f"Premium model has low input price (${model.input_per_1m})")

    def _validate_dates(self, model: ModelData, result: ValidationResult) -> None:
        """Validate date fields."""
        today = date.today()

        # Release date validation
        if model.release_date.year < self.MIN_RELEASE_YEAR:
            result.errors.append(f"release_date ({model.release_date}) is too far in the past")

        # Check if release date is too far in future
        max_future_date = date(today.year + self.MAX_FUTURE_YEARS, 12, 31)
        if model.release_date > max_future_date:
            result.warnings.append(
                f"release_date ({model.release_date}) is more than {self.MAX_FUTURE_YEARS} "
                "years in the future"
            )

    def _validate_urls(self, model: ModelData, result: ValidationResult) -> None:
        """Validate URL formats."""
        if model.docs_url:
            if not model.docs_url.startswith(("http://", "https://")):
                result.errors.append("docs_url must start with http:// or https://")

    def validate_batch(self, models: list[ModelData]) -> dict[str, ValidationResult]:
        """Validate multiple models.

        Args:
            models: List of ModelData objects

        Returns:
            Dictionary mapping model_id to ValidationResult
        """
        results = {}
        for model in models:
            results[model.model_id] = self.validate(model)

        # Summary logging
        total = len(results)
        valid = sum(1 for r in results.values() if r.is_valid)
        invalid = total - valid

        self.logger.info(f"Batch validation complete: {valid}/{total} valid, {invalid} invalid")

        return results

    def get_validation_summary(self, results: dict[str, ValidationResult]) -> dict[str, Any]:
        """Get summary statistics from validation results.

        Args:
            results: Dictionary of validation results

        Returns:
            Summary dictionary
        """
        total = len(results)
        valid = sum(1 for r in results.values() if r.is_valid)
        invalid = total - valid
        total_errors = sum(len(r.errors) for r in results.values())
        total_warnings = sum(len(r.warnings) for r in results.values())

        return {
            "total_models": total,
            "valid": valid,
            "invalid": invalid,
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "success_rate": (valid / total * 100) if total > 0 else 0,
        }
