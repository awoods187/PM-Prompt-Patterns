# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
Tests for providers/openai.py

Tests OpenAI provider implementation including initialization, classification,
JSON parsing, cost calculation, and error handling.
"""

from unittest.mock import MagicMock, patch

import pytest

from pm_prompt_toolkit.providers.base import SignalCategory
from pm_prompt_toolkit.providers.openai import OPENAI_MODEL_IDS, OPENAI_PRICING, OpenAIProvider


class TestOpenAIProviderInitialization:
    """Test OpenAIProvider initialization and validation."""

    def test_init_missing_openai_package(self):
        """Test initialization raises ImportError when openai is not installed."""
        with patch("pm_prompt_toolkit.providers.openai.OpenAI", None):
            with pytest.raises(ImportError) as exc_info:
                OpenAIProvider()

            assert "openai package is required" in str(exc_info.value)
            assert "pip install openai" in str(exc_info.value)

    @patch("pm_prompt_toolkit.providers.openai.OpenAI")
    @patch("pm_prompt_toolkit.providers.openai.get_settings")
    def test_init_invalid_model(self, mock_settings, mock_openai_class):
        """Test initialization raises ValueError for unsupported model."""
        mock_settings.return_value.get_api_key.return_value = "test-key"

        with pytest.raises(ValueError) as exc_info:
            OpenAIProvider(model="invalid-model")

        error_msg = str(exc_info.value)
        assert "Unsupported OpenAI model: invalid-model" in error_msg
        assert "gpt-4o" in error_msg
        assert "gpt-4o-mini" in error_msg

    @patch("pm_prompt_toolkit.providers.openai.OpenAI")
    @patch("pm_prompt_toolkit.providers.openai.get_settings")
    def test_init_successful_gpt4o(self, mock_settings, mock_openai_class):
        """Test successful initialization with GPT-4o model."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        provider = OpenAIProvider(model="gpt-4o", enable_caching=False)

        assert provider.model == "gpt-4o"
        assert provider.enable_caching is False
        assert provider.client == mock_client
        assert provider.openai_model_id == "gpt-4o-2024-08-06"
        mock_openai_class.assert_called_once_with(api_key="test-key")

    @patch("pm_prompt_toolkit.providers.openai.OpenAI")
    @patch("pm_prompt_toolkit.providers.openai.get_settings")
    def test_init_successful_gpt4o_mini(self, mock_settings, mock_openai_class):
        """Test successful initialization with GPT-4o-mini model."""
        mock_settings.return_value.get_api_key.return_value = "sk-test"
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        provider = OpenAIProvider(model="gpt-4o-mini")

        assert provider.model == "gpt-4o-mini"
        assert provider.openai_model_id == "gpt-4o-mini-2024-07-18"
        mock_settings.return_value.get_api_key.assert_called_once_with("openai")

    @patch("pm_prompt_toolkit.providers.openai.OpenAI")
    @patch("pm_prompt_toolkit.providers.openai.get_settings")
    def test_init_with_organization(self, mock_settings, mock_openai_class):
        """Test initialization with optional organization parameter."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        OpenAIProvider(model="gpt-4o", organization="org-test-123")

        mock_openai_class.assert_called_once_with(api_key="test-key", organization="org-test-123")


class TestBuildPrompts:
    """Test prompt building for OpenAI."""

    @patch("pm_prompt_toolkit.providers.openai.OpenAI")
    @patch("pm_prompt_toolkit.providers.openai.get_settings")
    def test_build_system_prompt(self, mock_settings, mock_openai_class):
        """Test system prompt structure."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_openai_class.return_value = MagicMock()

        provider = OpenAIProvider()
        system_prompt = provider._build_system_prompt()

        assert "customer signal classification" in system_prompt.lower()
        assert "feature_request" in system_prompt
        assert "bug_report" in system_prompt
        assert "churn_risk" in system_prompt
        assert "expansion_signal" in system_prompt
        assert "general_feedback" in system_prompt
        assert "JSON" in system_prompt
        assert "confidence" in system_prompt

    @patch("pm_prompt_toolkit.providers.openai.OpenAI")
    @patch("pm_prompt_toolkit.providers.openai.get_settings")
    def test_build_user_message(self, mock_settings, mock_openai_class):
        """Test user message formatting."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_openai_class.return_value = MagicMock()

        provider = OpenAIProvider()
        user_message = provider._build_user_message("Need SSO integration")

        assert "Classify this customer signal" in user_message
        assert "Need SSO integration" in user_message
        assert "JSON" in user_message


class TestResponseParsing:
    """Test JSON response parsing."""

    @patch("pm_prompt_toolkit.providers.openai.OpenAI")
    @patch("pm_prompt_toolkit.providers.openai.get_settings")
    def test_parse_response_valid_json(self, mock_settings, mock_openai_class):
        """Test parsing valid JSON response."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_openai_class.return_value = MagicMock()

        provider = OpenAIProvider()
        response = '{"category": "feature_request", "confidence": 0.95, "evidence": "need SSO"}'

        category, confidence, evidence = provider._parse_response(response)

        assert category == SignalCategory.FEATURE_REQUEST
        assert confidence == 0.95
        assert evidence == "need SSO"

    @patch("pm_prompt_toolkit.providers.openai.OpenAI")
    @patch("pm_prompt_toolkit.providers.openai.get_settings")
    def test_parse_response_invalid_json(self, mock_settings, mock_openai_class):
        """Test parsing invalid JSON raises ValueError."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_openai_class.return_value = MagicMock()

        provider = OpenAIProvider()

        with pytest.raises(ValueError) as exc_info:
            provider._parse_response("not valid json")

        assert "Invalid response format" in str(exc_info.value)

    @patch("pm_prompt_toolkit.providers.openai.OpenAI")
    @patch("pm_prompt_toolkit.providers.openai.get_settings")
    def test_parse_response_invalid_category(self, mock_settings, mock_openai_class):
        """Test parsing invalid category raises ValueError."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_openai_class.return_value = MagicMock()

        provider = OpenAIProvider()
        response = '{"category": "invalid_category", "confidence": 0.95, "evidence": "test"}'

        with pytest.raises(ValueError):
            provider._parse_response(response)

    @patch("pm_prompt_toolkit.providers.openai.OpenAI")
    @patch("pm_prompt_toolkit.providers.openai.get_settings")
    def test_parse_response_truncates_long_responses_in_logs(
        self, mock_settings, mock_openai_class
    ):
        """Test long responses are truncated in error logs."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_openai_class.return_value = MagicMock()

        provider = OpenAIProvider()
        long_invalid = "x" * 200  # 200 characters

        with pytest.raises(ValueError):
            provider._parse_response(long_invalid)


class TestCostCalculation:
    """Test cost calculation for OpenAI pricing."""

    @patch("pm_prompt_toolkit.providers.openai.OpenAI")
    @patch("pm_prompt_toolkit.providers.openai.get_settings")
    def test_calculate_cost_gpt4o(self, mock_settings, mock_openai_class):
        """Test cost calculation for GPT-4o."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_openai_class.return_value = MagicMock()

        provider = OpenAIProvider(model="gpt-4o")
        cost = provider._calculate_cost(input_tokens=100_000, output_tokens=10_000)

        # GPT-4o: $2.50 input, $10.00 output per 1M tokens
        expected = (100_000 / 1_000_000) * 2.50 + (10_000 / 1_000_000) * 10.00
        assert abs(cost - expected) < 0.0001

    @patch("pm_prompt_toolkit.providers.openai.OpenAI")
    @patch("pm_prompt_toolkit.providers.openai.get_settings")
    def test_calculate_cost_gpt4o_mini(self, mock_settings, mock_openai_class):
        """Test cost calculation for GPT-4o-mini."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_openai_class.return_value = MagicMock()

        provider = OpenAIProvider(model="gpt-4o-mini")
        cost = provider._calculate_cost(input_tokens=100_000, output_tokens=10_000)

        # GPT-4o-mini: $0.15 input, $0.60 output per 1M tokens
        expected = (100_000 / 1_000_000) * 0.15 + (10_000 / 1_000_000) * 0.60
        assert abs(cost - expected) < 0.0001

    @patch("pm_prompt_toolkit.providers.openai.OpenAI")
    @patch("pm_prompt_toolkit.providers.openai.get_settings")
    def test_calculate_cost_cached_tokens_ignored(self, mock_settings, mock_openai_class):
        """Test cached tokens parameter is ignored (OpenAI doesn't have caching)."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_openai_class.return_value = MagicMock()

        provider = OpenAIProvider(model="gpt-4o")
        cost_no_cache = provider._calculate_cost(input_tokens=100_000, output_tokens=10_000)
        cost_with_cache = provider._calculate_cost(
            input_tokens=100_000, output_tokens=10_000, cached_tokens=50_000
        )

        # OpenAI doesn't have caching, so cost should be the same
        assert cost_no_cache == cost_with_cache


class TestClassifyImplementation:
    """Test full classification workflow."""

    @patch("pm_prompt_toolkit.providers.openai.OpenAI")
    @patch("pm_prompt_toolkit.providers.openai.get_settings")
    def test_classify_impl_success(self, mock_settings, mock_openai_class):
        """Test successful classification."""
        mock_settings.return_value.get_api_key.return_value = "test-key"

        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(
                message=MagicMock(
                    content='{"category": "bug_report", "confidence": 0.98, "evidence": "500 errors"}'
                ),
                finish_reason="stop",
            )
        ]
        mock_response.usage = MagicMock(prompt_tokens=150, completion_tokens=50)
        mock_response.id = "chatcmpl-test-123"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        provider = OpenAIProvider(model="gpt-4o")
        result = provider._classify_impl("Dashboard broken, getting 500 errors", "")

        assert result.category == SignalCategory.BUG_REPORT
        assert result.confidence == 0.98
        assert result.evidence == "500 errors"
        assert result.method == "openai:gpt-4o"
        assert result.tokens_used == 200
        assert result.provider_metadata["provider"] == "openai"
        assert result.provider_metadata["finish_reason"] == "stop"
        assert result.provider_metadata["request_id"] == "chatcmpl-test-123"

    @patch("pm_prompt_toolkit.providers.openai.OpenAI")
    @patch("pm_prompt_toolkit.providers.openai.get_settings")
    def test_classify_impl_uses_json_mode(self, mock_settings, mock_openai_class):
        """Test classification uses JSON mode."""
        mock_settings.return_value.get_api_key.return_value = "test-key"

        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(
                message=MagicMock(
                    content='{"category": "feature_request", "confidence": 0.9, "evidence": "SSO"}'
                ),
                finish_reason="stop",
            )
        ]
        mock_response.usage = MagicMock(prompt_tokens=100, completion_tokens=30)
        mock_response.id = "test-id"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        provider = OpenAIProvider(model="gpt-4o")
        provider._classify_impl("Need SSO", "")

        # Verify JSON mode was enabled
        call_args = mock_client.chat.completions.create.call_args
        assert call_args.kwargs["response_format"] == {"type": "json_object"}
        assert call_args.kwargs["temperature"] == 0.3
        assert call_args.kwargs["max_tokens"] == 200


class TestModelMapping:
    """Test model ID mapping."""

    def test_model_ids_match_pricing(self):
        """Test all model IDs have corresponding pricing."""
        for model_name, model_id in OPENAI_MODEL_IDS.items():
            assert model_id in OPENAI_PRICING, f"Missing pricing for {model_id}"

    def test_pricing_covers_all_models(self):
        """Test pricing table covers all supported models."""
        model_ids = set(OPENAI_MODEL_IDS.values())
        pricing_ids = set(OPENAI_PRICING.keys())
        assert model_ids == pricing_ids
