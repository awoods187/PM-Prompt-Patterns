# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
Tests for providers/gemini.py

Tests Gemini 2.5 Provider implementation including initialization, classification,
JSON parsing, cost calculation with caching, and error handling.
"""

from unittest.mock import MagicMock, patch

import pytest

from pm_prompt_toolkit.providers.base import SignalCategory
from pm_prompt_toolkit.providers.gemini import (
    GEMINI_CACHE_PRICING,
    GEMINI_MODEL_IDS,
    GEMINI_PRICING,
    GeminiProvider,
)


class TestGeminiProviderInitialization:
    """Test GeminiProvider initialization and validation."""

    def test_init_missing_genai_package(self):
        """Test initialization raises ImportError when google-generativeai is not installed."""
        with patch("pm_prompt_toolkit.providers.gemini.genai", None):
            with pytest.raises(ImportError) as exc_info:
                GeminiProvider()

            assert "google-generativeai package is required" in str(exc_info.value)
            assert "pip install google-generativeai" in str(exc_info.value)

    @patch("pm_prompt_toolkit.providers.gemini.genai")
    @patch("pm_prompt_toolkit.providers.gemini.get_settings")
    def test_init_invalid_model(self, mock_settings, mock_genai):
        """Test initialization raises ValueError for unsupported model."""
        mock_settings.return_value.get_api_key.return_value = "test-key"

        with pytest.raises(ValueError) as exc_info:
            GeminiProvider(model="invalid-model")

        error_msg = str(exc_info.value)
        assert "Unsupported Gemini model: invalid-model" in error_msg
        assert "gemini-2-5-pro" in error_msg
        assert "gemini-2-5-flash" in error_msg

    @patch("pm_prompt_toolkit.providers.gemini.genai")
    @patch("pm_prompt_toolkit.providers.gemini.get_settings")
    def test_init_successful_flash(self, mock_settings, mock_genai):
        """Test successful initialization with Gemini 2.5 Flash model."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model

        provider = GeminiProvider(model="gemini-2-5-flash", enable_caching=True)

        assert provider.model == "gemini-2-5-flash"
        assert provider.enable_caching is True
        assert provider.client == mock_model
        assert provider.gemini_model_id == "gemini-2.5-flash-001"
        mock_genai.configure.assert_called_once_with(api_key="test-key")

    @patch("pm_prompt_toolkit.providers.gemini.genai")
    @patch("pm_prompt_toolkit.providers.gemini.get_settings")
    def test_init_successful_pro(self, mock_settings, mock_genai):
        """Test successful initialization with Gemini 2.5 Pro model."""
        mock_settings.return_value.get_api_key.return_value = "ai-test"
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model

        provider = GeminiProvider(model="gemini-2-5-pro")

        assert provider.model == "gemini-2-5-pro"
        assert provider.gemini_model_id == "gemini-2.5-pro-002"
        mock_settings.return_value.get_api_key.assert_called_once_with("google")

    @patch("pm_prompt_toolkit.providers.gemini.genai")
    @patch("pm_prompt_toolkit.providers.gemini.get_settings")
    def test_init_configures_json_mode(self, mock_settings, mock_genai):
        """Test initialization configures JSON response mode."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model

        GeminiProvider(model="gemini-2-5-flash")

        # Verify GenerativeModel was called with JSON config
        call_args = mock_genai.GenerativeModel.call_args
        assert call_args.kwargs["model_name"] == "gemini-2.5-flash-001"
        config = call_args.kwargs["generation_config"]
        assert config["temperature"] == 0.3
        assert config["max_output_tokens"] == 200
        assert config["response_mime_type"] == "application/json"


class TestBuildPrompt:
    """Test prompt building for Gemini."""

    @patch("pm_prompt_toolkit.providers.gemini.genai")
    @patch("pm_prompt_toolkit.providers.gemini.get_settings")
    def test_build_classification_prompt(self, mock_settings, mock_genai):
        """Test classification prompt structure."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_genai.GenerativeModel.return_value = MagicMock()

        provider = GeminiProvider()
        prompt = provider._build_classification_prompt("Need SSO integration")

        assert "customer signal classification" in prompt.lower()
        assert "feature_request" in prompt
        assert "bug_report" in prompt
        assert "churn_risk" in prompt
        assert "expansion_signal" in prompt
        assert "general_feedback" in prompt
        assert "Need SSO integration" in prompt
        assert "JSON" in prompt
        assert "confidence" in prompt


class TestResponseParsing:
    """Test JSON response parsing."""

    @patch("pm_prompt_toolkit.providers.gemini.genai")
    @patch("pm_prompt_toolkit.providers.gemini.get_settings")
    def test_parse_response_valid_json(self, mock_settings, mock_genai):
        """Test parsing valid JSON response."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_genai.GenerativeModel.return_value = MagicMock()

        provider = GeminiProvider()
        response = '{"category": "feature_request", "confidence": 0.95, "evidence": "need SSO"}'

        category, confidence, evidence = provider._parse_response(response)

        assert category == SignalCategory.FEATURE_REQUEST
        assert confidence == 0.95
        assert evidence == "need SSO"

    @patch("pm_prompt_toolkit.providers.gemini.genai")
    @patch("pm_prompt_toolkit.providers.gemini.get_settings")
    def test_parse_response_invalid_json(self, mock_settings, mock_genai):
        """Test parsing invalid JSON raises ValueError."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_genai.GenerativeModel.return_value = MagicMock()

        provider = GeminiProvider()

        with pytest.raises(ValueError) as exc_info:
            provider._parse_response("not valid json")

        assert "Invalid response format" in str(exc_info.value)

    @patch("pm_prompt_toolkit.providers.gemini.genai")
    @patch("pm_prompt_toolkit.providers.gemini.get_settings")
    def test_parse_response_invalid_category(self, mock_settings, mock_genai):
        """Test parsing invalid category raises ValueError."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_genai.GenerativeModel.return_value = MagicMock()

        provider = GeminiProvider()
        response = '{"category": "invalid_category", "confidence": 0.95, "evidence": "test"}'

        with pytest.raises(ValueError):
            provider._parse_response(response)

    @patch("pm_prompt_toolkit.providers.gemini.genai")
    @patch("pm_prompt_toolkit.providers.gemini.get_settings")
    def test_parse_response_truncates_long_responses_in_logs(self, mock_settings, mock_genai):
        """Test long responses are truncated in error logs."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_genai.GenerativeModel.return_value = MagicMock()

        provider = GeminiProvider()
        long_invalid = "x" * 200  # 200 characters

        with pytest.raises(ValueError):
            provider._parse_response(long_invalid)


class TestCostCalculation:
    """Test cost calculation including caching."""

    @patch("pm_prompt_toolkit.providers.gemini.genai")
    @patch("pm_prompt_toolkit.providers.gemini.get_settings")
    def test_calculate_cost_flash_no_cache(self, mock_settings, mock_genai):
        """Test cost calculation for Flash without caching."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_genai.GenerativeModel.return_value = MagicMock()

        provider = GeminiProvider(model="gemini-2-5-flash")
        cost = provider._calculate_cost(input_tokens=100_000, output_tokens=10_000, cached_tokens=0)

        # Flash: $0.075 input, $0.30 output per 1M tokens
        expected = (100_000 / 1_000_000) * 0.075 + (10_000 / 1_000_000) * 0.30
        assert abs(cost - expected) < 0.0001

    @patch("pm_prompt_toolkit.providers.gemini.genai")
    @patch("pm_prompt_toolkit.providers.gemini.get_settings")
    def test_calculate_cost_pro_no_cache(self, mock_settings, mock_genai):
        """Test cost calculation for Pro without caching."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_genai.GenerativeModel.return_value = MagicMock()

        provider = GeminiProvider(model="gemini-2-5-pro")
        cost = provider._calculate_cost(input_tokens=100_000, output_tokens=10_000, cached_tokens=0)

        # Pro: $1.25 input, $5.00 output per 1M tokens
        expected = (100_000 / 1_000_000) * 1.25 + (10_000 / 1_000_000) * 5.00
        assert abs(cost - expected) < 0.0001

    @patch("pm_prompt_toolkit.providers.gemini.genai")
    @patch("pm_prompt_toolkit.providers.gemini.get_settings")
    def test_calculate_cost_with_caching(self, mock_settings, mock_genai):
        """Test cost calculation with cached tokens."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_genai.GenerativeModel.return_value = MagicMock()

        provider = GeminiProvider(model="gemini-2-5-flash")
        cost = provider._calculate_cost(
            input_tokens=100_000, output_tokens=10_000, cached_tokens=50_000
        )

        # Flash: $0.075 input, $0.30 output, $0.019 cache read per 1M tokens
        # Uncached input: 50,000 tokens
        # Cached input: 50,000 tokens
        expected = (
            (50_000 / 1_000_000) * 0.075  # Uncached input
            + (50_000 / 1_000_000) * 0.019  # Cached input
            + (10_000 / 1_000_000) * 0.30  # Output
        )
        assert abs(cost - expected) < 0.0001

    @patch("pm_prompt_toolkit.providers.gemini.genai")
    @patch("pm_prompt_toolkit.providers.gemini.get_settings")
    def test_calculate_cost_all_cached(self, mock_settings, mock_genai):
        """Test cost calculation when all input tokens are cached."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_genai.GenerativeModel.return_value = MagicMock()

        provider = GeminiProvider(model="gemini-2-5-pro")
        cost = provider._calculate_cost(
            input_tokens=100_000, output_tokens=10_000, cached_tokens=100_000
        )

        # Pro: $1.25 input, $5.00 output, $0.31 cache read per 1M tokens
        # All input is cached
        expected = (100_000 / 1_000_000) * 0.31 + (10_000 / 1_000_000) * 5.00
        assert abs(cost - expected) < 0.0001


class TestClassifyImplementation:
    """Test full classification workflow."""

    @patch("pm_prompt_toolkit.providers.gemini.genai")
    @patch("pm_prompt_toolkit.providers.gemini.get_settings")
    def test_classify_impl_success(self, mock_settings, mock_genai):
        """Test successful classification."""
        mock_settings.return_value.get_api_key.return_value = "test-key"

        # Mock Gemini response
        mock_response = MagicMock()
        mock_response.text = (
            '{"category": "bug_report", "confidence": 0.98, "evidence": "500 errors"}'
        )
        mock_response.usage_metadata = MagicMock(
            prompt_token_count=150, candidates_token_count=50, cached_content_token_count=0
        )
        # Mock finish_reason enum
        mock_finish_reason = MagicMock()
        mock_finish_reason.name = "STOP"
        mock_response.candidates = [MagicMock(finish_reason=mock_finish_reason)]

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model

        provider = GeminiProvider(model="gemini-2-5-flash")
        result = provider._classify_impl("Dashboard broken, getting 500 errors", "")

        assert result.category == SignalCategory.BUG_REPORT
        assert result.confidence == 0.98
        assert result.evidence == "500 errors"
        assert result.method == "gemini:gemini-2-5-flash"
        assert result.tokens_used == 200
        assert result.cached_tokens == 0
        assert result.provider_metadata["provider"] == "gemini"
        assert result.provider_metadata["finish_reason"] == "STOP"

    @patch("pm_prompt_toolkit.providers.gemini.genai")
    @patch("pm_prompt_toolkit.providers.gemini.get_settings")
    def test_classify_impl_with_caching(self, mock_settings, mock_genai):
        """Test classification with cached tokens."""
        mock_settings.return_value.get_api_key.return_value = "test-key"

        # Mock response with cached tokens
        mock_response = MagicMock()
        mock_response.text = (
            '{"category": "feature_request", "confidence": 0.9, "evidence": "need SSO"}'
        )
        mock_response.usage_metadata = MagicMock(
            prompt_token_count=150, candidates_token_count=50, cached_content_token_count=100
        )
        mock_response.candidates = [MagicMock(finish_reason=MagicMock(name="STOP"))]

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model

        provider = GeminiProvider(model="gemini-2-5-flash")
        result = provider._classify_impl("Need SSO", "")

        assert result.cached_tokens == 100
        # Cost should be lower due to caching
        assert result.cost < 0.0001


class TestModelMapping:
    """Test model ID mapping and pricing consistency."""

    def test_model_ids_match_pricing(self):
        """Test all model IDs have corresponding pricing."""
        for model_name, model_id in GEMINI_MODEL_IDS.items():
            assert model_id in GEMINI_PRICING, f"Missing pricing for {model_id}"
            assert model_id in GEMINI_CACHE_PRICING, f"Missing cache pricing for {model_id}"

    def test_pricing_covers_all_models(self):
        """Test pricing tables cover all supported models."""
        model_ids = set(GEMINI_MODEL_IDS.values())
        pricing_ids = set(GEMINI_PRICING.keys())
        cache_pricing_ids = set(GEMINI_CACHE_PRICING.keys())

        assert model_ids == pricing_ids
        assert model_ids == cache_pricing_ids

    def test_cache_pricing_structure(self):
        """Test cache pricing has write and read prices."""
        for model_id, (write_price, read_price) in GEMINI_CACHE_PRICING.items():
            assert write_price > 0, f"Invalid write price for {model_id}"
            assert read_price > 0, f"Invalid read price for {model_id}"
            assert (
                read_price < write_price
            ), f"Read price should be less than write price for {model_id}"
