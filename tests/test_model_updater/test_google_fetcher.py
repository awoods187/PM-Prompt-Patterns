# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
Comprehensive tests for Google Gemini fetcher.

Coverage Target: 80%+
Current Coverage: 20.31%
Priority: HIGH - API integration, error handling
"""

from datetime import date
from unittest.mock import Mock, patch

import pytest

from scripts.model_updater.fetchers.base_fetcher import ModelData
from scripts.model_updater.fetchers.google_fetcher import GoogleFetcher

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def google_fetcher() -> GoogleFetcher:
    """Create Google fetcher instance."""
    return GoogleFetcher()


@pytest.fixture
def mock_genai_models() -> list[Mock]:
    """Create mock Google Generative AI model list."""
    models = []

    # Create mock model objects that match API response
    # Note: Using hyphens (2-5) to match target_model_ids in the actual code
    for model_name in [
        "models/gemini-2-5-flash-lite",
        "models/gemini-2-5-flash",
        "models/gemini-2-5-pro",
    ]:
        mock_model = Mock()
        mock_model.name = model_name
        models.append(mock_model)

    return models


# ============================================================================
# STATIC SPECS TESTS
# ============================================================================


class TestStaticModelSpecs:
    """Test suite for static model specifications."""

    def test_get_static_specs_gemini_flash_lite_returns_valid_specs(
        self, google_fetcher: GoogleFetcher
    ) -> None:
        """Test that Gemini 2.5 Flash Lite specs are complete and valid."""
        specs = google_fetcher._get_static_model_specs("gemini-2-5-flash-lite")

        assert specs is not None
        assert specs["name"] == "Gemini 2.5 Flash Lite"
        assert specs["api_identifier"] == "gemini-2.5-flash-lite-latest"
        assert specs["context_window_input"] == 1000000
        assert specs["context_window_output"] == 8192
        assert specs["knowledge_cutoff"] == "August 2024"
        assert specs["release_date"] == "2025-02-01"
        assert "pricing" in specs
        assert specs["pricing"]["input_per_1m"] == 0.075
        assert specs["pricing"]["output_per_1m"] == 0.30
        assert "capabilities" in specs
        assert "vision" in specs["capabilities"]
        assert "function_calling" in specs["capabilities"]
        assert specs["cost_tier"] == "budget"
        assert specs["speed_tier"] == "fast"

    def test_get_static_specs_gemini_flash_returns_valid_specs(
        self, google_fetcher: GoogleFetcher
    ) -> None:
        """Test that Gemini 2.5 Flash specs are complete and valid."""
        specs = google_fetcher._get_static_model_specs("gemini-2-5-flash")

        assert specs is not None
        assert specs["name"] == "Gemini 2.5 Flash"
        assert specs["context_window_input"] == 1000000
        assert specs["pricing"]["input_per_1m"] == 0.15
        assert specs["pricing"]["output_per_1m"] == 0.60
        assert specs["cost_tier"] == "budget"

    def test_get_static_specs_gemini_pro_returns_valid_specs(
        self, google_fetcher: GoogleFetcher
    ) -> None:
        """Test that Gemini 2.5 Pro specs are complete and valid."""
        specs = google_fetcher._get_static_model_specs("gemini-2-5-pro")

        assert specs is not None
        assert specs["name"] == "Gemini 2.5 Pro"
        assert specs["api_identifier"] == "gemini-2.5-pro-latest"
        assert specs["context_window_input"] == 2000000  # 2M context
        assert specs["context_window_output"] == 8192
        assert specs["pricing"]["input_per_1m"] == 1.25
        assert specs["pricing"]["output_per_1m"] == 5.00
        assert specs["cost_tier"] == "mid-tier"
        assert specs["speed_tier"] == "balanced"

    def test_get_static_specs_unknown_model_returns_none(
        self, google_fetcher: GoogleFetcher
    ) -> None:
        """Test that unknown model ID returns None."""
        specs = google_fetcher._get_static_model_specs("unknown-model")

        assert specs is None

    def test_static_specs_include_recommended_for(self, google_fetcher: GoogleFetcher) -> None:
        """Test that specs include recommended use cases."""
        specs = google_fetcher._get_static_model_specs("gemini-2-5-flash")

        assert "recommended_for" in specs
        assert len(specs["recommended_for"]) > 0
        assert isinstance(specs["recommended_for"], list)

    def test_static_specs_include_best_practices(self, google_fetcher: GoogleFetcher) -> None:
        """Test that specs include best practices."""
        specs = google_fetcher._get_static_model_specs("gemini-2-5-pro")

        assert "best_practices" in specs
        assert len(specs["best_practices"]) > 0
        assert isinstance(specs["best_practices"], list)


# ============================================================================
# API FETCHING TESTS
# ============================================================================


class TestAPIFetching:
    """Test suite for Google Generative AI API fetching."""

    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test-api-key"})
    @patch("google.generativeai.configure")
    @patch("google.generativeai.list_models")
    def test_fetch_from_api_with_valid_credentials_succeeds(
        self,
        mock_list_models: Mock,
        mock_configure: Mock,
        google_fetcher: GoogleFetcher,
        mock_genai_models: list[Mock],
    ) -> None:
        """Test successful API fetch with valid credentials."""
        # Setup mocks
        mock_list_models.return_value = mock_genai_models

        # Execute
        models = google_fetcher.fetch_from_api()

        # Verify
        assert len(models) == 3  # flash-lite, flash, pro
        assert all(isinstance(m, ModelData) for m in models)

        model_ids = [m.model_id for m in models]
        assert "gemini-2-5-flash-lite" in model_ids
        assert "gemini-2-5-flash" in model_ids
        assert "gemini-2-5-pro" in model_ids

        # Verify API was called
        mock_configure.assert_called_once_with(api_key="test-api-key")
        mock_list_models.assert_called_once()

    @patch.dict("os.environ", {}, clear=True)
    def test_fetch_from_api_without_api_key_raises_error(
        self, google_fetcher: GoogleFetcher
    ) -> None:
        """Test that missing API key raises ValueError."""
        with pytest.raises(ValueError, match="GOOGLE_API_KEY not set"):
            google_fetcher.fetch_from_api()

    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test-key"})
    def test_fetch_from_api_without_genai_package_raises_error(
        self, google_fetcher: GoogleFetcher
    ) -> None:
        """Test that missing google-generativeai package raises ImportError."""
        # Simulate import failure
        with patch(
            "builtins.__import__", side_effect=ImportError("No module named 'google.generativeai'")
        ):
            with pytest.raises(ImportError, match="google-generativeai package not installed"):
                google_fetcher.fetch_from_api()

    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test-api-key"})
    @patch("google.generativeai.configure")
    @patch("google.generativeai.list_models")
    def test_fetch_from_api_filters_gemini_25_models(
        self,
        mock_list_models: Mock,
        mock_configure: Mock,
        google_fetcher: GoogleFetcher,
    ) -> None:
        """Test that only Gemini 2.5 models are included."""
        # Create mixed model list
        all_models = []

        # Gemini 2.5 models (should be included) - use hyphens
        for name in ["models/gemini-2-5-flash", "models/gemini-2-5-pro"]:
            mock_model = Mock()
            mock_model.name = name
            all_models.append(mock_model)

        # Other models (should be filtered out)
        for name in ["models/gemini-1.5-pro", "models/text-bison-001"]:
            mock_model = Mock()
            mock_model.name = name
            all_models.append(mock_model)

        mock_list_models.return_value = all_models

        models = google_fetcher.fetch_from_api()

        # Should only get Gemini 2.5 models
        assert len(models) == 2
        assert all("gemini-2-5" in m.model_id for m in models)

    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test-api-key"})
    @patch("google.generativeai.configure")
    @patch("google.generativeai.list_models")
    def test_fetch_from_api_handles_no_matching_models(
        self,
        mock_list_models: Mock,
        mock_configure: Mock,
        google_fetcher: GoogleFetcher,
    ) -> None:
        """Test that ValueError is raised when no Gemini 2.5 models found."""
        # Return only non-Gemini 2.5 models
        other_models = []
        for name in ["models/gemini-1.0-pro", "models/palm-2"]:
            mock_model = Mock()
            mock_model.name = name
            other_models.append(mock_model)

        mock_list_models.return_value = other_models

        with pytest.raises(ValueError, match="No Gemini 2.5 models found via API"):
            google_fetcher.fetch_from_api()

    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test-api-key"})
    @patch("google.generativeai.configure")
    @patch("google.generativeai.list_models")
    def test_fetch_from_api_creates_model_data_with_correct_fields(
        self,
        mock_list_models: Mock,
        mock_configure: Mock,
        google_fetcher: GoogleFetcher,
        mock_genai_models: list[Mock],
    ) -> None:
        """Test that ModelData objects are created with all required fields."""
        mock_list_models.return_value = mock_genai_models

        models = google_fetcher.fetch_from_api()

        # Check one model in detail (Gemini 2.5 Pro)
        pro_model = next(m for m in models if m.model_id == "gemini-2-5-pro")
        assert pro_model.provider == "google"
        assert pro_model.name == "Gemini 2.5 Pro"
        assert pro_model.api_identifier == "gemini-2.5-pro-latest"
        assert pro_model.context_window_input == 2000000  # 2M
        assert pro_model.context_window_output == 8192
        assert pro_model.knowledge_cutoff == "August 2024"
        assert pro_model.release_date == date(2025, 2, 1)
        assert pro_model.docs_url == "https://ai.google.dev/gemini-api/docs/models/gemini"
        assert "vision" in pro_model.capabilities
        assert pro_model.input_per_1m == 1.25
        assert pro_model.output_per_1m == 5.00
        assert pro_model.cost_tier == "mid-tier"
        assert pro_model.speed_tier == "balanced"
        assert pro_model.source == "google_api"

    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test-api-key"})
    @patch("google.generativeai.configure")
    @patch("google.generativeai.list_models")
    def test_fetch_from_api_handles_model_name_with_path(
        self,
        mock_list_models: Mock,
        mock_configure: Mock,
        google_fetcher: GoogleFetcher,
    ) -> None:
        """Test that model names with 'models/' prefix are handled correctly."""
        models_with_prefix = []
        mock_model = Mock()
        mock_model.name = "models/gemini-2-5-flash"  # hyphen not period
        models_with_prefix.append(mock_model)

        mock_list_models.return_value = models_with_prefix

        models = google_fetcher.fetch_from_api()

        assert len(models) > 0
        # Name should be extracted correctly
        assert any("gemini-2-5-flash" in m.model_id for m in models)


# ============================================================================
# DOCS FALLBACK TESTS
# ============================================================================


class TestDocsFallback:
    """Test suite for docs-based fallback fetching."""

    def test_fetch_from_docs_returns_all_models(self, google_fetcher: GoogleFetcher) -> None:
        """Test that fetch_from_docs returns all supported models."""
        models = google_fetcher.fetch_from_docs()

        assert len(models) == 3
        model_ids = [m.model_id for m in models]
        assert "gemini-2-5-flash-lite" in model_ids
        assert "gemini-2-5-flash" in model_ids
        assert "gemini-2-5-pro" in model_ids

    def test_fetch_from_docs_creates_valid_model_data(self, google_fetcher: GoogleFetcher) -> None:
        """Test that docs-based models have all required fields."""
        models = google_fetcher.fetch_from_docs()

        for model in models:
            assert model.model_id is not None
            assert model.provider == "google"
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
            assert model.source == "google_docs"

    def test_fetch_from_docs_logs_usage_of_static_specs(
        self, google_fetcher: GoogleFetcher, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that fetch_from_docs logs that it's using static specs."""
        import logging

        caplog.set_level(logging.INFO)
        google_fetcher.fetch_from_docs()

        assert "Using static model specifications" in caplog.text

    def test_fetch_from_docs_preserves_model_order(self, google_fetcher: GoogleFetcher) -> None:
        """Test that models are returned in expected order."""
        models = google_fetcher.fetch_from_docs()

        model_ids = [m.model_id for m in models]
        expected_order = [
            "gemini-2-5-flash-lite",
            "gemini-2-5-flash",
            "gemini-2-5-pro",
        ]
        assert model_ids == expected_order


# ============================================================================
# MAIN FETCH METHOD TESTS
# ============================================================================


class TestMainFetchMethod:
    """Test suite for main fetch_models() method."""

    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test-api-key"})
    @patch("google.generativeai.configure")
    @patch("google.generativeai.list_models")
    def test_fetch_models_prefers_api_when_available(
        self,
        mock_list_models: Mock,
        mock_configure: Mock,
        google_fetcher: GoogleFetcher,
        mock_genai_models: list[Mock],
    ) -> None:
        """Test that fetch_models tries API first."""
        mock_list_models.return_value = mock_genai_models

        models = google_fetcher.fetch_models()

        # Should get models from API
        assert len(models) > 0
        assert all(m.source == "google_api" for m in models)
        mock_configure.assert_called_once()

    @patch.dict("os.environ", {}, clear=True)
    def test_fetch_models_falls_back_to_docs_on_api_failure(
        self, google_fetcher: GoogleFetcher, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that fetch_models falls back to docs when API fails."""
        models = google_fetcher.fetch_models()

        # Should get models from docs
        assert len(models) > 0
        assert all(m.source == "google_docs" for m in models)
        assert "API fetch failed" in caplog.text
        assert "Falling back to docs parsing" in caplog.text

    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test-api-key"})
    def test_fetch_models_falls_back_on_import_error(self, google_fetcher: GoogleFetcher) -> None:
        """Test fallback when google-generativeai package not installed."""
        # Simulate import error
        with patch(
            "builtins.__import__", side_effect=ImportError("No module named 'google.generativeai'")
        ):
            models = google_fetcher.fetch_models()

            # Should fall back to docs
            assert len(models) > 0
            assert all(m.source == "google_docs" for m in models)

    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test-api-key"})
    @patch("google.generativeai.configure")
    @patch("google.generativeai.list_models")
    def test_fetch_models_falls_back_when_no_models_found(
        self,
        mock_list_models: Mock,
        mock_configure: Mock,
        google_fetcher: GoogleFetcher,
    ) -> None:
        """Test fallback when API returns no Gemini 2.5 models."""
        # Return empty list
        mock_list_models.return_value = []

        models = google_fetcher.fetch_models()

        # Should fall back to docs
        assert len(models) > 0
        assert all(m.source == "google_docs" for m in models)


# ============================================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================================


class TestEdgeCases:
    """Test suite for edge cases and error handling."""

    def test_provider_name_returns_google(self, google_fetcher: GoogleFetcher) -> None:
        """Test that provider_name property returns correct value."""
        assert google_fetcher.provider_name == "google"

    def test_static_specs_have_consistent_structure(self, google_fetcher: GoogleFetcher) -> None:
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

        for model_id in [
            "gemini-2-5-flash-lite",
            "gemini-2-5-flash",
            "gemini-2-5-pro",
        ]:
            specs = google_fetcher._get_static_model_specs(model_id)
            assert specs is not None
            assert required_keys.issubset(set(specs.keys()))
            assert "input_per_1m" in specs["pricing"]
            assert "output_per_1m" in specs["pricing"]

    def test_fetch_from_docs_handles_missing_specs_gracefully(
        self, google_fetcher: GoogleFetcher
    ) -> None:
        """Test that fetch_from_docs skips models with missing specs."""
        # Patch to simulate missing spec
        with patch.object(google_fetcher, "_get_static_model_specs") as mock_get_specs:
            mock_get_specs.return_value = None

            models = google_fetcher.fetch_from_docs()

            # Should return empty list when all specs are missing
            assert models == []

    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test-api-key"})
    @patch("google.generativeai.configure")
    @patch("google.generativeai.list_models")
    def test_fetch_from_api_handles_model_without_slash(
        self,
        mock_list_models: Mock,
        mock_configure: Mock,
        google_fetcher: GoogleFetcher,
    ) -> None:
        """Test handling of model names without 'models/' prefix."""
        # Create model without prefix (use hyphen not period)
        mock_model = Mock()
        mock_model.name = "gemini-2-5-flash"  # No "models/" prefix
        mock_list_models.return_value = [mock_model]

        models = google_fetcher.fetch_from_api()

        # Should still work
        assert len(models) > 0
        assert any("gemini-2-5-flash" in m.model_id for m in models)

    def test_all_models_have_large_context_capability(self, google_fetcher: GoogleFetcher) -> None:
        """Test that all Gemini 2.5 models advertise large_context capability."""
        models = google_fetcher.fetch_from_docs()

        for model in models:
            assert "large_context" in model.capabilities
            assert model.context_window_input >= 1000000  # At least 1M tokens

    def test_model_pricing_reflects_capability_tiers(self, google_fetcher: GoogleFetcher) -> None:
        """Test that pricing aligns with model capabilities."""
        models = google_fetcher.fetch_from_docs()

        # Get models by ID
        models_dict = {m.model_id: m for m in models}

        flash_lite = models_dict["gemini-2-5-flash-lite"]
        flash = models_dict["gemini-2-5-flash"]
        pro = models_dict["gemini-2-5-pro"]

        # Flash Lite should be cheapest
        assert flash_lite.input_per_1m < flash.input_per_1m < pro.input_per_1m
        assert flash_lite.output_per_1m < flash.output_per_1m < pro.output_per_1m

        # Pro should have largest context window
        assert pro.context_window_input > flash.context_window_input
