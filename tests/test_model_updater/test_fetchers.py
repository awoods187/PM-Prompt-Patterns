# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Tests for model fetchers."""

from datetime import date

from scripts.model_updater.fetchers.anthropic_fetcher import AnthropicFetcher
from scripts.model_updater.fetchers.base_fetcher import ModelData
from scripts.model_updater.fetchers.google_fetcher import GoogleFetcher
from scripts.model_updater.fetchers.openai_fetcher import OpenAIFetcher


def test_anthropic_fetcher_static_specs() -> None:
    """Test Anthropic fetcher can get static specs."""
    fetcher = AnthropicFetcher()

    # Should be able to get static specs
    specs = fetcher._get_static_model_specs("claude-sonnet-4-5")

    assert specs is not None
    assert specs["context_window_input"] == 200000
    assert "pricing" in specs
    assert specs["pricing"]["input_per_1m"] > 0
    assert specs["knowledge_cutoff"] == "January 2025"


def test_openai_fetcher_static_specs() -> None:
    """Test OpenAI fetcher can get static specs."""
    fetcher = OpenAIFetcher()

    specs = fetcher._get_static_model_specs("gpt-4o")

    assert specs is not None
    assert specs["name"] == "GPT-4o"
    assert specs["context_window_input"] == 128000
    assert "pricing" in specs


def test_google_fetcher_static_specs() -> None:
    """Test Google fetcher can get static specs."""
    fetcher = GoogleFetcher()

    specs = fetcher._get_static_model_specs("gemini-2-5-pro")

    assert specs is not None
    assert specs["name"] == "Gemini 2.5 Pro"
    assert specs["context_window_input"] == 2000000
    assert "pricing" in specs


def test_base_fetcher_validation() -> None:
    """Test base fetcher validation logic."""
    fetcher = AnthropicFetcher()

    # Valid model
    valid_model = ModelData(
        model_id="test-model",
        provider="test",
        name="Test Model",
        api_identifier="test-v1",
        context_window_input=100000,
        context_window_output=4096,
        knowledge_cutoff="Jan 2025",
        release_date=date(2025, 1, 1),
        docs_url="https://example.com",
        capabilities=["text_input", "text_output"],
        input_per_1m=1.0,
        output_per_1m=3.0,
        cost_tier="mid-tier",
        speed_tier="balanced",
    )

    is_valid, errors = fetcher.validate_model_data(valid_model)
    assert is_valid
    assert len(errors) == 0


def test_base_fetcher_validation_invalid_model() -> None:
    """Test base fetcher catches invalid models."""
    fetcher = AnthropicFetcher()

    # Invalid model (missing required fields, bad pricing)
    invalid_model = ModelData(
        model_id="",  # Missing
        provider="test",
        name="",  # Missing
        api_identifier="",
        context_window_input=-1,  # Invalid
        context_window_output=None,
        knowledge_cutoff="",
        release_date=date.today(),
        docs_url="",  # Missing
        capabilities=[],  # Empty
        input_per_1m=-1.0,  # Invalid
        output_per_1m=-1.0,  # Invalid
        cost_tier="invalid",  # Invalid
        speed_tier="invalid",  # Invalid
    )

    is_valid, errors = fetcher.validate_model_data(invalid_model)
    assert not is_valid
    assert len(errors) > 0


def test_base_fetcher_cache() -> None:
    """Test base fetcher caching."""
    fetcher = AnthropicFetcher()

    # First fetch (will use static specs)
    models1 = fetcher.fetch_from_docs()

    # Should get models
    assert len(models1) > 0

    # Cache the result manually
    from datetime import datetime

    fetcher._cache[fetcher.provider_name] = (datetime.now(), models1)

    # Second fetch should use cache
    models2 = fetcher.fetch_with_cache()

    # Should be same data
    assert len(models2) == len(models1)


def test_base_fetcher_cache_miss_fetches_fresh_data() -> None:
    """Test that cache miss triggers fresh data fetch."""
    fetcher = AnthropicFetcher()

    # Clear any existing cache
    fetcher._cache.clear()

    # Fetch should get fresh data (not from cache)
    models = fetcher.fetch_with_cache()

    # Should have fetched models
    assert len(models) > 0

    # Cache should now be populated
    assert fetcher.provider_name in fetcher._cache


def test_base_fetcher_validation_suspiciously_large_context() -> None:
    """Test validation catches suspiciously large context windows."""
    fetcher = AnthropicFetcher()

    # Model with extremely large context window
    model = ModelData(
        model_id="test-model",
        provider="test",
        name="Test Model",
        api_identifier="test-v1",
        context_window_input=20_000_000,  # Suspiciously large (> 10M)
        context_window_output=4096,
        knowledge_cutoff="Jan 2025",
        release_date=date(2025, 1, 1),
        docs_url="https://example.com",
        capabilities=["text_input", "text_output"],
        input_per_1m=1.0,
        output_per_1m=3.0,
        cost_tier="mid-tier",
        speed_tier="balanced",
    )

    is_valid, errors = fetcher.validate_model_data(model)
    assert not is_valid
    assert any("Suspiciously large context_window_input" in e for e in errors)


def test_base_fetcher_validation_high_pricing() -> None:
    """Test validation catches suspiciously high pricing."""
    fetcher = AnthropicFetcher()

    # Model with extremely high pricing
    model = ModelData(
        model_id="test-model",
        provider="test",
        name="Test Model",
        api_identifier="test-v1",
        context_window_input=100000,
        context_window_output=4096,
        knowledge_cutoff="Jan 2025",
        release_date=date(2025, 1, 1),
        docs_url="https://example.com",
        capabilities=["text_input", "text_output"],
        input_per_1m=2000.0,  # Suspiciously high (> 1000)
        output_per_1m=10000.0,  # Suspiciously high (> 5000)
        cost_tier="mid-tier",
        speed_tier="balanced",
    )

    is_valid, errors = fetcher.validate_model_data(model)
    assert not is_valid
    assert any("Suspiciously high input_per_1m" in e for e in errors)
    assert any("Suspiciously high output_per_1m" in e for e in errors)


def test_base_fetcher_validation_negative_cache_pricing() -> None:
    """Test validation catches negative cache pricing."""
    fetcher = AnthropicFetcher()

    # Model with negative cache pricing
    model = ModelData(
        model_id="test-model",
        provider="test",
        name="Test Model",
        api_identifier="test-v1",
        context_window_input=100000,
        context_window_output=4096,
        knowledge_cutoff="Jan 2025",
        release_date=date(2025, 1, 1),
        docs_url="https://example.com",
        capabilities=["text_input", "text_output"],
        input_per_1m=1.0,
        output_per_1m=3.0,
        cache_write_per_1m=-1.0,  # Invalid
        cache_read_per_1m=-0.5,  # Invalid
        cost_tier="mid-tier",
        speed_tier="balanced",
    )

    is_valid, errors = fetcher.validate_model_data(model)
    assert not is_valid
    assert any("Invalid cache_write_per_1m" in e for e in errors)
    assert any("Invalid cache_read_per_1m" in e for e in errors)


def test_base_fetcher_validation_invalid_capabilities() -> None:
    """Test validation catches invalid capability names."""
    fetcher = AnthropicFetcher()

    # Model with invalid capabilities
    model = ModelData(
        model_id="test-model",
        provider="test",
        name="Test Model",
        api_identifier="test-v1",
        context_window_input=100000,
        context_window_output=4096,
        knowledge_cutoff="Jan 2025",
        release_date=date(2025, 1, 1),
        docs_url="https://example.com",
        capabilities=["text_input", "invalid_capability", "another_invalid"],
        input_per_1m=1.0,
        output_per_1m=3.0,
        cost_tier="mid-tier",
        speed_tier="balanced",
    )

    is_valid, errors = fetcher.validate_model_data(model)
    assert not is_valid
    assert any("Invalid capabilities" in e for e in errors)


def test_base_fetcher_retry_with_backoff_success() -> None:
    """Test retry_with_backoff succeeds on retry."""
    fetcher = AnthropicFetcher()

    # Function that fails twice then succeeds
    attempts = [0]

    def flaky_function():
        attempts[0] += 1
        if attempts[0] < 3:
            raise Exception("Temporary failure")
        return "success"

    result = fetcher.retry_with_backoff(flaky_function, max_retries=3, initial_delay=0.01)

    assert result == "success"
    assert attempts[0] == 3  # Should have tried 3 times


def test_base_fetcher_retry_with_backoff_all_fail() -> None:
    """Test retry_with_backoff raises after all retries fail."""
    fetcher = AnthropicFetcher()

    def always_fail():
        raise ValueError("Persistent failure")

    import pytest

    with pytest.raises(ValueError, match="Persistent failure"):
        fetcher.retry_with_backoff(always_fail, max_retries=2, initial_delay=0.01)


def test_model_data_to_yaml_dict() -> None:
    """Test ModelData conversion to YAML dictionary."""
    model = ModelData(
        model_id="test-model",
        provider="test",
        name="Test Model",
        api_identifier="test-v1",
        context_window_input=100000,
        context_window_output=4096,
        knowledge_cutoff="Jan 2025",
        release_date=date(2025, 1, 1),
        docs_url="https://example.com",
        capabilities=["text_input", "text_output", "streaming"],
        input_per_1m=1.0,
        output_per_1m=3.0,
        cache_write_per_1m=1.25,
        cache_read_per_1m=0.10,
        recommended_for=["Test use case"],
        best_practices=["Use wisely"],
        cost_tier="mid-tier",
        speed_tier="balanced",
        notes="Test notes",
    )

    yaml_dict = model.to_yaml_dict()

    # Check structure
    assert yaml_dict["schema_version"] == "1.0.0"
    assert yaml_dict["model_id"] == "test-model"
    assert yaml_dict["provider"] == "test"
    assert yaml_dict["name"] == "Test Model"

    # Check metadata
    assert "metadata" in yaml_dict
    assert yaml_dict["metadata"]["context_window_input"] == 100000
    assert yaml_dict["metadata"]["release_date"] == "2025-01-01"

    # Check pricing
    assert "pricing" in yaml_dict
    assert yaml_dict["pricing"]["input_per_1m"] == 1.0
    assert yaml_dict["pricing"]["cache_write_per_1m"] == 1.25

    # Check capabilities
    assert "capabilities" in yaml_dict
    assert "text_input" in yaml_dict["capabilities"]

    # Check optimization
    assert "optimization" in yaml_dict
    assert yaml_dict["optimization"]["cost_tier"] == "mid-tier"
