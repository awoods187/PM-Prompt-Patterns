# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Tests for change detection."""

from datetime import date

import pytest

from scripts.model_updater.change_detector import ChangeDetector
from scripts.model_updater.fetchers.base_fetcher import ModelData


@pytest.fixture
def detector() -> ChangeDetector:
    """Create change detector instance."""
    return ChangeDetector()


@pytest.fixture
def current_models() -> dict:
    """Create current model definitions."""
    return {
        "existing-model": {
            "model_id": "existing-model",
            "provider": "test",
            "name": "Existing Model",
            "api_identifier": "existing-model-v1",
            "metadata": {
                "context_window_input": 100000,
                "context_window_output": 4096,
                "knowledge_cutoff": "Jan 2024",
                "release_date": "2024-01-01",
                "last_verified": "2024-01-01",
                "docs_url": "https://example.com",
            },
            "capabilities": ["text_input", "text_output"],
            "pricing": {
                "input_per_1m": 1.0,
                "output_per_1m": 3.0,
            },
            "optimization": {
                "cost_tier": "mid-tier",
                "speed_tier": "balanced",
            },
        }
    }


@pytest.fixture
def fetched_models() -> list[ModelData]:
    """Create fetched model data."""
    return [
        ModelData(
            model_id="existing-model",
            provider="test",
            name="Existing Model",
            api_identifier="existing-model-v1",
            context_window_input=100000,
            context_window_output=4096,
            knowledge_cutoff="Jan 2024",
            release_date=date(2024, 1, 1),
            docs_url="https://example.com",
            capabilities=["text_input", "text_output"],
            input_per_1m=1.0,
            output_per_1m=3.0,
            cost_tier="mid-tier",
            speed_tier="balanced",
        )
    ]


def test_detect_no_changes(
    detector: ChangeDetector,
    current_models: dict,
    fetched_models: list[ModelData],
) -> None:
    """Test detection when there are no changes."""
    report = detector.detect_changes(current_models, fetched_models)

    assert not report.has_changes
    assert report.total_changes == 0
    assert len(report.new_models) == 0
    assert len(report.removed_models) == 0
    assert len(report.pricing_changes) == 0


def test_detect_new_model(
    detector: ChangeDetector,
    current_models: dict,
    fetched_models: list[ModelData],
) -> None:
    """Test detection of new models."""
    # Add a new model
    new_model = ModelData(
        model_id="new-model",
        provider="test",
        name="New Model",
        api_identifier="new-model-v1",
        context_window_input=128000,
        context_window_output=None,
        knowledge_cutoff="Jan 2025",
        release_date=date(2025, 1, 1),
        docs_url="https://example.com",
        capabilities=["text_input", "text_output", "vision"],
        input_per_1m=2.0,
        output_per_1m=6.0,
        cost_tier="mid-tier",
        speed_tier="fast",
    )
    fetched_models.append(new_model)

    report = detector.detect_changes(current_models, fetched_models)

    assert report.has_changes
    assert len(report.new_models) == 1
    assert report.new_models[0].model_id == "new-model"


def test_detect_removed_model(
    detector: ChangeDetector,
    current_models: dict,
) -> None:
    """Test detection of removed models."""
    # No fetched models (all removed)
    report = detector.detect_changes(current_models, [])

    assert report.has_changes
    assert len(report.removed_models) == 1
    assert "existing-model" in report.removed_models


def test_detect_pricing_change(
    detector: ChangeDetector,
    current_models: dict,
    fetched_models: list[ModelData],
) -> None:
    """Test detection of pricing changes."""
    # Change pricing
    fetched_models[0].input_per_1m = 1.5
    fetched_models[0].output_per_1m = 4.0

    report = detector.detect_changes(current_models, fetched_models)

    assert report.has_changes
    assert len(report.pricing_changes) == 2  # Both input and output changed
    assert any(c.field == "input_per_1m" for c in report.pricing_changes)
    assert any(c.field == "output_per_1m" for c in report.pricing_changes)


def test_detect_capability_change(
    detector: ChangeDetector,
    current_models: dict,
    fetched_models: list[ModelData],
) -> None:
    """Test detection of capability changes."""
    # Add new capability
    fetched_models[0].capabilities = ["text_input", "text_output", "vision"]

    report = detector.detect_changes(current_models, fetched_models)

    assert report.has_changes
    assert len(report.capability_changes) == 1
    assert "vision" in report.capability_changes[0].description


def test_detect_context_window_change(
    detector: ChangeDetector,
    current_models: dict,
    fetched_models: list[ModelData],
) -> None:
    """Test detection of context window changes."""
    # Increase context window
    fetched_models[0].context_window_input = 200000

    report = detector.detect_changes(current_models, fetched_models)

    assert report.has_changes
    assert len(report.context_changes) == 1
    assert report.context_changes[0].field == "context_window_input"
    assert report.context_changes[0].new_value == 200000


def test_changelog_markdown_generation(
    detector: ChangeDetector,
    current_models: dict,
    fetched_models: list[ModelData],
) -> None:
    """Test markdown changelog generation."""
    # Make some changes
    fetched_models[0].input_per_1m = 1.5
    new_model = ModelData(
        model_id="new-model",
        provider="test",
        name="New Model",
        api_identifier="new-model-v1",
        context_window_input=128000,
        context_window_output=None,
        knowledge_cutoff="Jan 2025",
        release_date=date(2025, 1, 1),
        docs_url="https://example.com",
        capabilities=["text_input", "text_output"],
        input_per_1m=2.0,
        output_per_1m=6.0,
        cost_tier="mid-tier",
        speed_tier="fast",
    )
    fetched_models.append(new_model)

    report = detector.detect_changes(current_models, fetched_models)
    markdown = report.to_markdown()

    # Check markdown contains expected sections
    assert "# Model Update Changelog" in markdown
    assert "## 🆕 New Models" in markdown
    assert "## 💰 Pricing Changes" in markdown
    assert "new-model" in markdown.lower()


def test_changelog_no_changes(detector: ChangeDetector) -> None:
    """Test changelog when no changes detected."""
    report = detector.detect_changes({}, [])
    markdown = report.to_markdown()

    assert "No changes detected" in markdown


def test_detect_api_identifier_change(
    detector: ChangeDetector,
    current_models: dict,
    fetched_models: list[ModelData],
) -> None:
    """Test detection of API identifier changes."""
    # Change API identifier (new version)
    fetched_models[0].api_identifier = "existing-model-v2"

    report = detector.detect_changes(current_models, fetched_models)

    assert report.has_changes
    assert len(report.metadata_changes) == 1
    assert report.metadata_changes[0].field == "api_identifier"


def test_detect_cache_pricing_change(
    detector: ChangeDetector,
    current_models: dict,
    fetched_models: list[ModelData],
) -> None:
    """Test detection of cache pricing changes."""
    # Add cache pricing to current
    current_models["existing-model"]["pricing"]["cache_write_per_1m"] = 1.25
    current_models["existing-model"]["pricing"]["cache_read_per_1m"] = 0.10

    # Change cache pricing in fetched
    fetched_models[0].cache_write_per_1m = 1.50
    fetched_models[0].cache_read_per_1m = 0.12

    report = detector.detect_changes(current_models, fetched_models)

    assert report.has_changes
    cache_changes = [c for c in report.pricing_changes if "cache" in c.field]  # type: ignore[operator]
    assert len(cache_changes) == 2


def test_total_changes_count(
    detector: ChangeDetector,
    current_models: dict,
    fetched_models: list[ModelData],
) -> None:
    """Test total changes count."""
    # Add new model
    new_model = ModelData(
        model_id="new-model",
        provider="test",
        name="New Model",
        api_identifier="new-model-v1",
        context_window_input=128000,
        context_window_output=None,
        knowledge_cutoff="Jan 2025",
        release_date=date(2025, 1, 1),
        docs_url="https://example.com",
        capabilities=["text_input", "text_output"],
        input_per_1m=2.0,
        output_per_1m=6.0,
        cost_tier="mid-tier",
        speed_tier="fast",
    )
    fetched_models.append(new_model)

    # Change pricing
    fetched_models[0].input_per_1m = 1.5

    report = detector.detect_changes(current_models, fetched_models)

    # Should count new model + pricing change
    assert report.total_changes >= 2
    assert report.has_changes
