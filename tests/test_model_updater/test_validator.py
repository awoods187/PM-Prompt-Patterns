# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Tests for model validator."""

from datetime import date

import pytest

from scripts.model_updater.fetchers.base_fetcher import ModelData
from scripts.model_updater.validator import ModelValidator


@pytest.fixture
def validator() -> ModelValidator:
    """Create validator instance."""
    return ModelValidator()


@pytest.fixture
def valid_model() -> ModelData:
    """Create a valid model for testing."""
    return ModelData(
        model_id="test-model",
        provider="test",
        name="Test Model",
        api_identifier="test-model-v1",
        context_window_input=128000,
        context_window_output=4096,
        knowledge_cutoff="January 2025",
        release_date=date(2025, 1, 1),
        docs_url="https://example.com/docs",
        capabilities=["text_input", "text_output", "streaming"],
        input_per_1m=1.0,
        output_per_1m=3.0,
        cost_tier="mid-tier",
        speed_tier="balanced",
    )


def test_validate_valid_model(validator: ModelValidator, valid_model: ModelData) -> None:
    """Test validation of a valid model."""
    result = validator.validate(valid_model)

    assert result.is_valid
    assert len(result.errors) == 0
    assert result.model_id == "test-model"


def test_validate_missing_required_fields(validator: ModelValidator) -> None:
    """Test validation fails for missing required fields."""
    model = ModelData(
        model_id="",  # Missing
        provider="test",
        name="",  # Missing
        api_identifier="test",
        context_window_input=128000,
        context_window_output=None,
        knowledge_cutoff="Jan 2025",
        release_date=date.today(),
        docs_url="https://example.com",
    )

    result = validator.validate(model)

    assert not result.is_valid
    assert "model_id is required" in result.errors
    assert "name is required" in result.errors


def test_validate_invalid_context_window(validator: ModelValidator, valid_model: ModelData) -> None:
    """Test validation fails for invalid context window."""
    valid_model.context_window_input = -100

    result = validator.validate(valid_model)

    assert not result.is_valid
    assert any("context_window_input must be positive" in e for e in result.errors)


def test_validate_invalid_pricing(validator: ModelValidator, valid_model: ModelData) -> None:
    """Test validation fails for negative pricing."""
    valid_model.input_per_1m = -1.0

    result = validator.validate(valid_model)

    assert not result.is_valid
    assert any("input_per_1m must be non-negative" in e for e in result.errors)


def test_validate_invalid_capabilities(validator: ModelValidator, valid_model: ModelData) -> None:
    """Test validation fails for invalid capabilities."""
    valid_model.capabilities = ["text_input", "invalid_capability"]

    result = validator.validate(valid_model)

    assert not result.is_valid
    assert any("Invalid capabilities" in e for e in result.errors)


def test_validate_empty_capabilities(validator: ModelValidator, valid_model: ModelData) -> None:
    """Test validation fails for empty capabilities."""
    valid_model.capabilities = []

    result = validator.validate(valid_model)

    assert not result.is_valid
    assert "At least one capability is required" in result.errors


def test_validate_invalid_tier(validator: ModelValidator, valid_model: ModelData) -> None:
    """Test validation fails for invalid tiers."""
    valid_model.cost_tier = "invalid"

    result = validator.validate(valid_model)

    assert not result.is_valid
    assert any("Invalid cost_tier" in e for e in result.errors)


def test_validate_suspiciously_high_price(validator: ModelValidator, valid_model: ModelData) -> None:
    """Test warning for suspiciously high price."""
    valid_model.input_per_1m = 999.0
    valid_model.output_per_1m = 1200.0  # Also increase output to avoid another warning

    result = validator.validate(valid_model)

    # Should still be valid but with warning
    assert result.is_valid
    assert any("unusually high" in w or "seems unusually high" in w for w in result.warnings)


def test_validate_batch(validator: ModelValidator, valid_model: ModelData) -> None:
    """Test batch validation."""
    # Create multiple models
    model1 = valid_model
    model2 = ModelData(
        model_id="test-model-2",
        provider="test",
        name="Test Model 2",
        api_identifier="test-model-2-v1",
        context_window_input=100000,
        context_window_output=None,
        knowledge_cutoff="Jan 2025",
        release_date=date.today(),
        docs_url="https://example.com",
        capabilities=["text_input", "text_output"],
        input_per_1m=0.5,
        output_per_1m=1.5,
        cost_tier="budget",
        speed_tier="fast",
    )
    model3_invalid = ModelData(
        model_id="",  # Invalid
        provider="test",
        name="Invalid",
        api_identifier="invalid",
        context_window_input=-1,  # Invalid
        context_window_output=None,
        knowledge_cutoff="",
        release_date=date.today(),
        docs_url="",
    )

    results = validator.validate_batch([model1, model2, model3_invalid])

    assert len(results) == 3
    assert results["test-model"].is_valid
    assert results["test-model-2"].is_valid
    assert not results[""].is_valid


def test_validation_summary(validator: ModelValidator, valid_model: ModelData) -> None:
    """Test validation summary generation."""
    model1 = valid_model
    model2_invalid = ModelData(
        model_id="invalid",
        provider="",  # Invalid
        name="",  # Invalid
        api_identifier="",
        context_window_input=-1,  # Invalid
        context_window_output=None,
        knowledge_cutoff="",
        release_date=date.today(),
        docs_url="",
    )

    results = validator.validate_batch([model1, model2_invalid])
    summary = validator.get_validation_summary(results)

    assert summary["total_models"] == 2
    assert summary["valid"] == 1
    assert summary["invalid"] == 1
    assert summary["total_errors"] > 0
    assert summary["success_rate"] == 50.0


def test_validate_cache_pricing(validator: ModelValidator, valid_model: ModelData) -> None:
    """Test validation of cache pricing."""
    valid_model.cache_write_per_1m = 1.5
    valid_model.cache_read_per_1m = 0.1

    result = validator.validate(valid_model)

    assert result.is_valid
    # Should have warning if cache_write < input_per_1m
    if valid_model.cache_write_per_1m < valid_model.input_per_1m:
        assert any("cache_write" in w for w in result.warnings)
