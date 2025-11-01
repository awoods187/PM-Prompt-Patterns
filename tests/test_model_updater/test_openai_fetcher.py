# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
Comprehensive tests for OpenAI fetcher.

Coverage Target: 80%+
Current Coverage: 22.41%
Priority: HIGH - API integration, error handling
"""

from datetime import date
from unittest.mock import Mock, patch

import pytest

from scripts.model_updater.fetchers.base_fetcher import ModelData
from scripts.model_updater.fetchers.openai_fetcher import OpenAIFetcher

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def mock_openai_client() -> Mock:
    """Create mock OpenAI client."""
    client = Mock()

    # Mock models.list() response
    client.models.list.return_value = Mock()

    # Mock models.retrieve() response for valid models
    mock_model = Mock()
    mock_model.id = "gpt-4o"
    client.models.retrieve.return_value = mock_model

    return client


@pytest.fixture
def openai_fetcher() -> OpenAIFetcher:
    """Create OpenAI fetcher instance."""
    return OpenAIFetcher()


# ============================================================================
# STATIC SPECS TESTS
# ============================================================================


class TestStaticModelSpecs:
    """Test suite for static model specifications."""

    def test_get_static_specs_gpt4o_returns_valid_specs(
        self, openai_fetcher: OpenAIFetcher
    ) -> None:
        """Test that GPT-4o specs are complete and valid."""
        specs = openai_fetcher._get_static_model_specs("gpt-4o")

        assert specs is not None
        assert specs["name"] == "GPT-4o"
        assert specs["api_identifier"] == "gpt-4o-2024-08-06"
        assert specs["context_window_input"] == 128000
        assert specs["context_window_output"] == 16384
        assert specs["knowledge_cutoff"] == "October 2023"
        assert specs["release_date"] == "2024-08-06"
        assert "pricing" in specs
        assert specs["pricing"]["input_per_1m"] == 2.50
        assert specs["pricing"]["output_per_1m"] == 10.00
        assert "capabilities" in specs
        assert "vision" in specs["capabilities"]
        assert "function_calling" in specs["capabilities"]

    def test_get_static_specs_gpt4o_mini_returns_valid_specs(
        self, openai_fetcher: OpenAIFetcher
    ) -> None:
        """Test that GPT-4o Mini specs are complete and valid."""
        specs = openai_fetcher._get_static_model_specs("gpt-4o-mini")

        assert specs is not None
        assert specs["name"] == "GPT-4o Mini"
        assert specs["api_identifier"] == "gpt-4o-mini-2024-07-18"
        assert specs["context_window_input"] == 128000
        assert specs["context_window_output"] == 16384
        assert specs["knowledge_cutoff"] == "October 2023"
        assert specs["release_date"] == "2024-07-18"
        assert specs["pricing"]["input_per_1m"] == 0.15
        assert specs["pricing"]["output_per_1m"] == 0.60
        assert specs["cost_tier"] == "budget"
        assert specs["speed_tier"] == "fast"

    def test_get_static_specs_unknown_model_returns_none(
        self, openai_fetcher: OpenAIFetcher
    ) -> None:
        """Test that unknown model ID returns None."""
        specs = openai_fetcher._get_static_model_specs("unknown-model")

        assert specs is None

    def test_static_specs_include_recommended_for(self, openai_fetcher: OpenAIFetcher) -> None:
        """Test that specs include recommended use cases."""
        specs = openai_fetcher._get_static_model_specs("gpt-4o")

        assert "recommended_for" in specs
        assert len(specs["recommended_for"]) > 0
        assert isinstance(specs["recommended_for"], list)

    def test_static_specs_include_best_practices(self, openai_fetcher: OpenAIFetcher) -> None:
        """Test that specs include best practices."""
        specs = openai_fetcher._get_static_model_specs("gpt-4o-mini")

        assert "best_practices" in specs
        assert len(specs["best_practices"]) > 0
        assert isinstance(specs["best_practices"], list)


# ============================================================================
# API FETCHING TESTS
# ============================================================================


class TestAPIFetching:
    """Test suite for OpenAI API fetching."""

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-api-key"})
    @patch("openai.OpenAI")
    def test_fetch_from_api_with_valid_credentials_succeeds(
        self, mock_openai_class: Mock, openai_fetcher: OpenAIFetcher
    ) -> None:
        """Test successful API fetch with valid credentials."""
        # Setup mock client
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        # Mock successful API calls
        mock_client.models.list.return_value = Mock()
        mock_model = Mock()
        mock_model.id = "gpt-4o"
        mock_client.models.retrieve.return_value = mock_model

        # Execute
        models = openai_fetcher.fetch_from_api()

        # Verify
        assert len(models) == 2  # gpt-4o and gpt-4o-mini
        assert all(isinstance(m, ModelData) for m in models)
        assert any(m.model_id == "gpt-4o" for m in models)
        assert any(m.model_id == "gpt-4o-mini" for m in models)

        # Verify API was called
        mock_openai_class.assert_called_once_with(api_key="test-api-key")
        mock_client.models.list.assert_called_once()

    @patch.dict("os.environ", {}, clear=True)
    def test_fetch_from_api_without_api_key_raises_error(
        self, openai_fetcher: OpenAIFetcher
    ) -> None:
        """Test that missing API key raises ValueError."""
        with pytest.raises(ValueError, match="OPENAI_API_KEY not set"):
            openai_fetcher.fetch_from_api()

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    def test_fetch_from_api_without_openai_package_raises_error(
        self, openai_fetcher: OpenAIFetcher
    ) -> None:
        """Test that missing openai package raises ImportError."""
        # Simulate import failure by making the import raise ImportError
        with patch("builtins.__import__", side_effect=ImportError("openai not installed")):
            with pytest.raises(ImportError, match="openai package not installed"):
                openai_fetcher.fetch_from_api()

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-api-key"})
    @patch("openai.OpenAI")
    def test_fetch_from_api_handles_model_retrieval_failure_gracefully(
        self, mock_openai_class: Mock, openai_fetcher: OpenAIFetcher
    ) -> None:
        """Test that model retrieval errors are logged but don't break fetch."""
        # Setup mock client
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        # Mock successful list but failed retrieve for one model
        mock_client.models.list.return_value = Mock()

        # First retrieve (gpt-4o) fails, second (gpt-4o-mini) succeeds
        mock_model = Mock()
        mock_model.id = "gpt-4o-mini"
        mock_client.models.retrieve.side_effect = [
            Exception("Model not found"),
            mock_model,
        ]

        # Execute
        models = openai_fetcher.fetch_from_api()

        # Should return only the successful model
        assert len(models) == 1
        assert models[0].model_id == "gpt-4o-mini"

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-api-key"})
    @patch("openai.OpenAI")
    def test_fetch_from_api_skips_models_without_specs(
        self, mock_openai_class: Mock, openai_fetcher: OpenAIFetcher
    ) -> None:
        """Test that models without static specs are skipped."""
        # Setup mock client
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        # Mock successful API calls
        mock_client.models.list.return_value = Mock()
        mock_model = Mock()
        mock_client.models.retrieve.return_value = mock_model

        # Get real specs for gpt-4o-mini once before patching
        real_specs = openai_fetcher._get_static_model_specs("gpt-4o-mini")

        # Patch _get_static_model_specs to return None for one model
        with patch.object(openai_fetcher, "_get_static_model_specs") as mock_get_specs:
            mock_get_specs.side_effect = [
                None,  # gpt-4o has no specs
                real_specs,  # gpt-4o-mini has specs
            ]

            models = openai_fetcher.fetch_from_api()

            # Should only return gpt-4o-mini
            assert len(models) == 1
            assert models[0].model_id == "gpt-4o-mini"

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-api-key"})
    @patch("openai.OpenAI")
    def test_fetch_from_api_creates_model_data_with_correct_fields(
        self, mock_openai_class: Mock, openai_fetcher: OpenAIFetcher
    ) -> None:
        """Test that ModelData objects are created with all required fields."""
        # Setup mock client
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        mock_client.models.list.return_value = Mock()
        mock_model = Mock()
        mock_client.models.retrieve.return_value = mock_model

        models = openai_fetcher.fetch_from_api()

        # Check first model (gpt-4o)
        gpt4o = next(m for m in models if m.model_id == "gpt-4o")
        assert gpt4o.provider == "openai"
        assert gpt4o.name == "GPT-4o"
        assert gpt4o.api_identifier == "gpt-4o-2024-08-06"
        assert gpt4o.context_window_input == 128000
        assert gpt4o.context_window_output == 16384
        assert gpt4o.knowledge_cutoff == "October 2023"
        assert gpt4o.release_date == date(2024, 8, 6)
        assert gpt4o.docs_url == "https://platform.openai.com/docs/models/gpt-4o"
        assert "vision" in gpt4o.capabilities
        assert gpt4o.input_per_1m == 2.50
        assert gpt4o.output_per_1m == 10.00
        assert gpt4o.cost_tier == "mid-tier"
        assert gpt4o.speed_tier == "balanced"
        assert gpt4o.source == "openai_api"


# ============================================================================
# DOCS FALLBACK TESTS
# ============================================================================


class TestDocsFallback:
    """Test suite for docs-based fallback fetching."""

    def test_fetch_from_docs_returns_all_models(self, openai_fetcher: OpenAIFetcher) -> None:
        """Test that fetch_from_docs returns all supported models."""
        models = openai_fetcher.fetch_from_docs()

        assert len(models) == 2
        model_ids = [m.model_id for m in models]
        assert "gpt-4o" in model_ids
        assert "gpt-4o-mini" in model_ids

    def test_fetch_from_docs_creates_valid_model_data(self, openai_fetcher: OpenAIFetcher) -> None:
        """Test that docs-based models have all required fields."""
        models = openai_fetcher.fetch_from_docs()

        for model in models:
            assert model.model_id is not None
            assert model.provider == "openai"
            assert model.name is not None
            assert model.api_identifier is not None
            assert model.context_window_input > 0
            assert model.context_window_output > 0
            assert model.knowledge_cutoff is not None
            assert isinstance(model.release_date, date)
            assert model.docs_url.startswith("https://")
            assert len(model.capabilities) > 0
            assert model.input_per_1m > 0
            assert model.output_per_1m > 0
            assert model.source == "openai_docs"

    def test_fetch_from_docs_logs_usage_of_static_specs(
        self, openai_fetcher: OpenAIFetcher, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that fetch_from_docs logs that it's using static specs."""
        import logging

        caplog.set_level(logging.INFO)
        openai_fetcher.fetch_from_docs()

        assert "Using static model specifications" in caplog.text


# ============================================================================
# MAIN FETCH METHOD TESTS
# ============================================================================


class TestMainFetchMethod:
    """Test suite for main fetch_models() method."""

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-api-key"})
    @patch("openai.OpenAI")
    def test_fetch_models_prefers_api_when_available(
        self, mock_openai_class: Mock, openai_fetcher: OpenAIFetcher
    ) -> None:
        """Test that fetch_models tries API first."""
        # Setup successful API fetch
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.models.list.return_value = Mock()
        mock_model = Mock()
        mock_client.models.retrieve.return_value = mock_model

        models = openai_fetcher.fetch_models()

        # Should get models from API
        assert len(models) > 0
        assert all(m.source == "openai_api" for m in models)
        mock_openai_class.assert_called_once()

    @patch.dict("os.environ", {}, clear=True)
    def test_fetch_models_falls_back_to_docs_on_api_failure(
        self, openai_fetcher: OpenAIFetcher, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that fetch_models falls back to docs when API fails."""
        models = openai_fetcher.fetch_models()

        # Should get models from docs
        assert len(models) > 0
        assert all(m.source == "openai_docs" for m in models)
        assert "API fetch failed" in caplog.text
        assert "Falling back to docs parsing" in caplog.text

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-api-key"})
    def test_fetch_models_falls_back_on_import_error(self, openai_fetcher: OpenAIFetcher) -> None:
        """Test fallback when OpenAI package not installed."""
        # Simulate import error by patching the import
        with patch("builtins.__import__", side_effect=ImportError("No module named 'openai'")):
            models = openai_fetcher.fetch_models()

            # Should fall back to docs
            assert len(models) > 0
            assert all(m.source == "openai_docs" for m in models)


# ============================================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================================


class TestEdgeCases:
    """Test suite for edge cases and error handling."""

    def test_provider_name_returns_openai(self, openai_fetcher: OpenAIFetcher) -> None:
        """Test that provider_name property returns correct value."""
        assert openai_fetcher.provider_name == "openai"

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-api-key"})
    @patch("openai.OpenAI")
    def test_fetch_from_api_handles_empty_model_list(
        self, mock_openai_class: Mock, openai_fetcher: OpenAIFetcher
    ) -> None:
        """Test behavior when no models pass validation."""
        # Setup mock to fail all model retrievals
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.models.list.return_value = Mock()
        mock_client.models.retrieve.side_effect = Exception("All models failed")

        models = openai_fetcher.fetch_from_api()

        # Should return empty list
        assert models == []

    def test_static_specs_have_consistent_structure(self, openai_fetcher: OpenAIFetcher) -> None:
        """Test that all static specs follow the same structure."""
        required_keys = {
            "name",
            "api_identifier",
            "context_window_input",
            "context_window_output",
            "knowledge_cutoff",
            "release_date",
            "capabilities",
            "pricing",
            "cost_tier",
            "speed_tier",
            "recommended_for",
            "best_practices",
            "notes",
        }

        for model_id in ["gpt-4o", "gpt-4o-mini"]:
            specs = openai_fetcher._get_static_model_specs(model_id)
            assert specs is not None
            assert required_keys.issubset(set(specs.keys()))
            assert "input_per_1m" in specs["pricing"]
            assert "output_per_1m" in specs["pricing"]

    def test_fetch_from_docs_handles_missing_specs_gracefully(
        self, openai_fetcher: OpenAIFetcher
    ) -> None:
        """Test that fetch_from_docs skips models with missing specs."""
        # Patch to simulate missing spec
        with patch.object(openai_fetcher, "_get_static_model_specs") as mock_get_specs:
            mock_get_specs.return_value = None

            models = openai_fetcher.fetch_from_docs()

            # Should return empty list when all specs are missing
            assert models == []
