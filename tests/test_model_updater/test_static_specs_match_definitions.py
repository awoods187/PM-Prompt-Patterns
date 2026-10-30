# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Drift guard: fetcher static specs must match ai_models/definitions/*.yaml.

Without API keys (as in CI) the updater falls back to the static specs, and the
change detector compares them against the YAMLs. If the two drift apart the
weekly run proposes reverting verified YAML values, so any edit to one side must
be mirrored on the other.
"""

from pathlib import Path
from typing import Any

import pytest
import yaml

from scripts.model_updater.change_detector import ChangeDetector
from scripts.model_updater.fetchers.anthropic_fetcher import AnthropicFetcher
from scripts.model_updater.fetchers.base_fetcher import BaseFetcher
from scripts.model_updater.fetchers.google_fetcher import GoogleFetcher
from scripts.model_updater.fetchers.openai_fetcher import OpenAIFetcher
from scripts.model_updater.validator import ModelValidator

DEFINITIONS_DIR = Path(__file__).resolve().parents[2] / "ai_models" / "definitions"
FETCHERS = [AnthropicFetcher, OpenAIFetcher, GoogleFetcher]


def _load_definitions(provider: str) -> dict[str, dict[str, Any]]:
    definitions = {}
    for path in sorted((DEFINITIONS_DIR / provider).glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        definitions[data["model_id"]] = data
    return definitions


@pytest.mark.parametrize("fetcher_cls", FETCHERS)
def test_model_list_matches_definitions(fetcher_cls: type[BaseFetcher]) -> None:
    """The fetcher tracks exactly the models defined for its provider."""
    fetcher = fetcher_cls()
    definitions = _load_definitions(fetcher.provider_name)

    assert definitions, f"No YAML definitions found for {fetcher.provider_name}"
    assert sorted(fetcher.MODEL_IDS) == sorted(definitions)  # type: ignore[attr-defined]


@pytest.mark.parametrize("fetcher_cls", FETCHERS)
def test_static_specs_match_definitions(fetcher_cls: type[BaseFetcher]) -> None:
    """Each static spec agrees with its YAML on IDs, context, dates and pricing."""
    fetcher = fetcher_cls()

    for model_id, definition in _load_definitions(fetcher.provider_name).items():
        specs = fetcher._get_static_model_specs(model_id)  # type: ignore[attr-defined]
        assert specs is not None, f"{model_id}: missing from static specs"
        metadata = definition["metadata"]

        assert specs["api_identifier"] == definition["api_identifier"], model_id
        assert specs["context_window_input"] == metadata["context_window_input"], model_id
        assert specs["context_window_output"] == metadata["context_window_output"], model_id
        assert specs["release_date"] == str(metadata["release_date"]), model_id
        assert specs["pricing"] == definition["pricing"], model_id


@pytest.mark.parametrize("fetcher_cls", FETCHERS)
def test_static_fallback_detects_no_changes(fetcher_cls: type[BaseFetcher]) -> None:
    """The keyless fallback validates cleanly and proposes no changes to the YAMLs."""
    fetcher = fetcher_cls()
    models = fetcher.fetch_from_docs()

    for model in models:
        result = ModelValidator().validate(model)
        assert result.is_valid, f"{model.model_id}: {result.errors}"

    report = ChangeDetector().detect_changes(_load_definitions(fetcher.provider_name), models)
    assert not report.has_changes, report.to_markdown()
