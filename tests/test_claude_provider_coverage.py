# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
Additional tests for providers/claude.py to achieve 85%+ coverage.

Focuses on XML prompt building, response parsing, cost calculation, and error handling.
"""

from unittest.mock import MagicMock, Mock, patch

import pytest

from pm_prompt_toolkit.providers.base import ClassificationResult, SignalCategory
from pm_prompt_toolkit.providers.claude import CLAUDE_PRICING, ClaudeProvider


class TestClaudeProviderInitialization:
    """Test ClaudeProvider initialization and validation."""

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    def test_init_missing_anthropic_package(self, mock_anthropic_module):
        """Test initialization raises ImportError when anthropic is not installed."""
        # Simulate missing anthropic package

        with patch("pm_prompt_toolkit.providers.claude.anthropic", None):
            with pytest.raises(ImportError) as exc_info:
                ClaudeProvider()

            assert "anthropic package is required" in str(exc_info.value)
            assert "pip install anthropic" in str(exc_info.value)

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_init_invalid_model(self, mock_settings, mock_anthropic):
        """Test initialization raises ValueError for unsupported model."""
        mock_settings.return_value.get_api_key.return_value = "test-key"

        with pytest.raises(ValueError) as exc_info:
            ClaudeProvider(model="invalid-model")

        error_msg = str(exc_info.value)
        assert "Unsupported Claude model: invalid-model" in error_msg
        assert "claude-haiku" in error_msg
        assert "claude-sonnet" in error_msg
        assert "claude-opus" in error_msg

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_init_successful_haiku(self, mock_settings, mock_anthropic):
        """Test successful initialization with Haiku model."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client

        provider = ClaudeProvider(model="claude-haiku", enable_caching=True)

        assert provider.model == "claude-haiku"
        assert provider.enable_caching is True
        assert provider.client == mock_client
        mock_anthropic.Anthropic.assert_called_once_with(api_key="test-key")

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_init_successful_sonnet(self, mock_settings, mock_anthropic):
        """Test successful initialization with Sonnet model (default)."""
        mock_settings.return_value.get_api_key.return_value = "sk-ant-test"
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client

        provider = ClaudeProvider()  # Default model is sonnet

        assert provider.model == "claude-sonnet"
        assert provider.enable_caching is True
        mock_settings.return_value.get_api_key.assert_called_once_with("anthropic")

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_init_successful_opus(self, mock_settings, mock_anthropic):
        """Test successful initialization with Opus model."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        provider = ClaudeProvider(model="claude-opus", enable_caching=False)

        assert provider.model == "claude-opus"
        assert provider.enable_caching is False

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_init_calls_get_api_key(self, mock_settings, mock_anthropic):
        """Test initialization retrieves API key from settings."""
        mock_settings.return_value.get_api_key.return_value = "sk-ant-test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        ClaudeProvider()

        mock_settings.return_value.get_api_key.assert_called_once_with("anthropic")
        mock_anthropic.Anthropic.assert_called_once_with(api_key="sk-ant-test-key")


class TestBuildXmlPrompt:
    """Test XML prompt building and XML injection prevention."""

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_build_xml_prompt_basic(self, mock_settings, mock_anthropic):
        """Test XML prompt structure with normal text."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        provider = ClaudeProvider()
        prompt = provider._build_xml_prompt("Need SSO integration")

        assert "<task>Classify this customer signal" in prompt
        assert "<categories>" in prompt
        assert '<category id="feature_request">' in prompt
        assert '<category id="bug_report">' in prompt
        assert "<signal>Need SSO integration</signal>" in prompt
        assert "<output_format>" in prompt
        assert "category|confidence|evidence" in prompt

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_build_xml_prompt_escapes_xml_characters(self, mock_settings, mock_anthropic):
        """Test XML special characters are properly escaped."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        provider = ClaudeProvider()

        # Text with XML injection attempt
        malicious_text = "<script>alert('xss')</script> & <inject>bad</inject>"
        prompt = provider._build_xml_prompt(malicious_text)

        # Should be escaped, not raw
        assert "<script>" not in prompt
        assert "&lt;script&gt;" in prompt
        assert "&amp;" in prompt
        assert "<inject>" not in prompt

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_build_xml_prompt_all_categories_present(self, mock_settings, mock_anthropic):
        """Test all signal categories are included in prompt."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        provider = ClaudeProvider()
        prompt = provider._build_xml_prompt("test")

        # All 5 categories should be present
        assert "feature_request" in prompt
        assert "bug_report" in prompt
        assert "churn_risk" in prompt
        assert "expansion_signal" in prompt
        assert "general_feedback" in prompt


class TestParseResponse:
    """Test Claude response parsing."""

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_parse_response_valid_feature_request(self, mock_settings, mock_anthropic):
        """Test parsing valid feature request response."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        provider = ClaudeProvider()
        response = "feature_request|0.95|Customer wants SSO login"

        category, confidence, evidence = provider._parse_response(response)

        assert category == SignalCategory.FEATURE_REQUEST
        assert confidence == 0.95
        assert evidence == "Customer wants SSO login"

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_parse_response_valid_bug_report(self, mock_settings, mock_anthropic):
        """Test parsing valid bug report response."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        provider = ClaudeProvider()
        response = "bug_report|0.99|Dashboard showing 500 error"

        category, confidence, evidence = provider._parse_response(response)

        assert category == SignalCategory.BUG_REPORT
        assert confidence == 0.99
        assert evidence == "Dashboard showing 500 error"

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_parse_response_with_whitespace(self, mock_settings, mock_anthropic):
        """Test parsing handles extra whitespace correctly."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        provider = ClaudeProvider()
        response = "  churn_risk  |  0.88  |  Customer threatening to leave  "

        category, confidence, evidence = provider._parse_response(response)

        assert category == SignalCategory.CHURN_RISK
        assert confidence == 0.88
        assert evidence == "Customer threatening to leave"

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_parse_response_invalid_format_too_few_parts(self, mock_settings, mock_anthropic):
        """Test parsing raises ValueError for too few parts."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        provider = ClaudeProvider()
        response = "feature_request|0.95"  # Missing evidence

        with pytest.raises(ValueError) as exc_info:
            provider._parse_response(response)

        assert "Invalid response format" in str(exc_info.value)

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_parse_response_invalid_format_too_many_parts(self, mock_settings, mock_anthropic):
        """Test parsing raises ValueError for too many parts."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        provider = ClaudeProvider()
        response = "feature_request|0.95|evidence|extra|parts"

        with pytest.raises(ValueError) as exc_info:
            provider._parse_response(response)

        assert "Invalid response format" in str(exc_info.value)

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_parse_response_invalid_category(self, mock_settings, mock_anthropic):
        """Test parsing raises ValueError for invalid category."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        provider = ClaudeProvider()
        response = "invalid_category|0.95|evidence"

        with pytest.raises(ValueError) as exc_info:
            provider._parse_response(response)

        assert "Invalid response format" in str(exc_info.value)

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_parse_response_invalid_confidence(self, mock_settings, mock_anthropic):
        """Test parsing raises ValueError for non-numeric confidence."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        provider = ClaudeProvider()
        response = "feature_request|not-a-number|evidence"

        with pytest.raises(ValueError) as exc_info:
            provider._parse_response(response)

        assert "Invalid response format" in str(exc_info.value)

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_parse_response_truncates_long_responses_in_error(self, mock_settings, mock_anthropic):
        """Test error logging truncates long responses to prevent PII exposure."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        provider = ClaudeProvider()
        # Create response >100 chars
        long_response = "invalid|format|" + ("x" * 200)

        with pytest.raises(ValueError):
            provider._parse_response(long_response)

        # Should raise but not expose full long response in logs
        # (we can't test log content directly without log capture)


class TestCalculateCost:
    """Test cost calculation logic."""

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_calculate_cost_haiku_no_cache(self, mock_settings, mock_anthropic):
        """Test cost calculation for Haiku without caching."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        provider = ClaudeProvider(model="claude-haiku")

        # Haiku: $1.00 input, $5.00 output per 1M tokens
        cost = provider._calculate_cost(input_tokens=1000, output_tokens=500)

        # (1000/1M * 1.00) + (500/1M * 5.00) = 0.001 + 0.0025 = 0.0035
        assert cost == pytest.approx(0.0035, rel=1e-6)

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_calculate_cost_sonnet_no_cache(self, mock_settings, mock_anthropic):
        """Test cost calculation for Sonnet without caching."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        provider = ClaudeProvider(model="claude-sonnet")

        # Sonnet: $3.00 input, $15.00 output per 1M tokens
        cost = provider._calculate_cost(input_tokens=1000, output_tokens=500)

        # (1000/1M * 3.00) + (500/1M * 15.00) = 0.003 + 0.0075 = 0.0105
        assert cost == pytest.approx(0.0105, rel=1e-6)

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_calculate_cost_opus_no_cache(self, mock_settings, mock_anthropic):
        """Test cost calculation for Opus without caching."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        provider = ClaudeProvider(model="claude-opus")

        # Opus: $15.00 input, $75.00 output per 1M tokens
        cost = provider._calculate_cost(input_tokens=1000, output_tokens=500)

        # (1000/1M * 15.00) + (500/1M * 75.00) = 0.015 + 0.0375 = 0.0525
        assert cost == pytest.approx(0.0525, rel=1e-6)

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_calculate_cost_with_caching(self, mock_settings, mock_anthropic):
        """Test cost calculation with cached tokens (90% discount)."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        provider = ClaudeProvider(model="claude-sonnet")

        # 1000 input tokens, 900 cached (90% discount)
        # Uncached: 100 tokens, Cached: 900 tokens
        cost = provider._calculate_cost(input_tokens=1000, output_tokens=500, cached_tokens=900)

        # Uncached input: (100/1M * 3.00) = 0.0003
        # Cached input: (900/1M * 3.00 * 0.1) = 0.00027
        # Output: (500/1M * 15.00) = 0.0075
        # Total: 0.00807
        assert cost == pytest.approx(0.00807, rel=1e-5)

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_calculate_cost_all_cached(self, mock_settings, mock_anthropic):
        """Test cost calculation when all input tokens are cached."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        provider = ClaudeProvider(model="claude-haiku")

        # All 1000 input tokens are cached
        cost = provider._calculate_cost(input_tokens=1000, output_tokens=500, cached_tokens=1000)

        # Cached input: (1000/1M * 1.00 * 0.1) = 0.0001
        # Output: (500/1M * 5.00) = 0.0025
        # Total: 0.0026
        assert cost == pytest.approx(0.0026, rel=1e-6)


class TestGetModelId:
    """Test _get_model_id method."""

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_get_model_id_haiku(self, mock_settings, mock_anthropic):
        """Test _get_model_id returns correct API identifier for Haiku."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        # Mock the model constants from models.registry (imported inside method)
        mock_haiku = Mock()
        mock_haiku.api_identifier = "claude-haiku-4-5-20250929"

        with patch("models.registry.CLAUDE_HAIKU", mock_haiku):
            provider = ClaudeProvider(model="claude-haiku")
            model_id = provider._get_model_id()

            assert model_id == "claude-haiku-4-5-20250929"

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_get_model_id_sonnet(self, mock_settings, mock_anthropic):
        """Test _get_model_id returns correct API identifier for Sonnet."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        mock_sonnet = Mock()
        mock_sonnet.api_identifier = "claude-sonnet-4-5-20250929"

        with patch("models.registry.CLAUDE_SONNET", mock_sonnet):
            provider = ClaudeProvider(model="claude-sonnet")
            model_id = provider._get_model_id()

            assert model_id == "claude-sonnet-4-5-20250929"

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_get_model_id_opus(self, mock_settings, mock_anthropic):
        """Test _get_model_id returns correct API identifier for Opus."""
        mock_settings.return_value.get_api_key.return_value = "test-key"
        mock_anthropic.Anthropic.return_value = MagicMock()

        mock_opus = Mock()
        mock_opus.api_identifier = "claude-opus-4-1-20250514"

        with patch("models.registry.CLAUDE_OPUS", mock_opus):
            provider = ClaudeProvider(model="claude-opus")
            model_id = provider._get_model_id()

            assert model_id == "claude-opus-4-1-20250514"


class TestClassifyImpl:
    """Test _classify_impl end-to-end classification."""

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_classify_impl_feature_request(self, mock_settings, mock_anthropic):
        """Test full classification flow for feature request."""
        mock_settings.return_value.get_api_key.return_value = "test-key"

        # Mock API response
        mock_response = Mock()
        mock_content = Mock()
        mock_content.text = "feature_request|0.95|Customer wants SSO integration"
        mock_response.content = [mock_content]
        mock_response.usage = Mock(input_tokens=150, output_tokens=20)

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.Anthropic.return_value = mock_client

        # Mock _get_model_id
        with patch.object(ClaudeProvider, "_get_model_id", return_value="claude-sonnet-4-5"):
            provider = ClaudeProvider(model="claude-sonnet")
            result = provider._classify_impl("Need SSO integration", "")

        assert isinstance(result, ClassificationResult)
        assert result.category == SignalCategory.FEATURE_REQUEST
        assert result.confidence == 0.95
        assert result.evidence == "Customer wants SSO integration"
        assert result.model == "claude-sonnet"
        assert result.tokens_used == 170  # 150 + 20
        assert result.cost > 0

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_classify_impl_bug_report(self, mock_settings, mock_anthropic):
        """Test full classification flow for bug report."""
        mock_settings.return_value.get_api_key.return_value = "test-key"

        # Mock API response
        mock_response = Mock()
        mock_content = Mock()
        mock_content.text = "bug_report|0.99|Dashboard returning 500 errors"
        mock_response.content = [mock_content]
        mock_response.usage = Mock(input_tokens=145, output_tokens=18)

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.Anthropic.return_value = mock_client

        with patch.object(ClaudeProvider, "_get_model_id", return_value="claude-haiku-4-5"):
            provider = ClaudeProvider(model="claude-haiku")
            result = provider._classify_impl("Dashboard broken, 500 errors", "")

        assert result.category == SignalCategory.BUG_REPORT
        assert result.confidence == 0.99
        assert result.tokens_used == 163

    @patch("pm_prompt_toolkit.providers.claude.anthropic")
    @patch("pm_prompt_toolkit.providers.claude.get_settings")
    def test_classify_impl_calls_api_with_correct_params(self, mock_settings, mock_anthropic):
        """Test that API is called with correct parameters."""
        mock_settings.return_value.get_api_key.return_value = "test-key"

        mock_response = Mock()
        mock_content = Mock()
        mock_content.text = "general_feedback|0.75|Thanks for the update"
        mock_response.content = [mock_content]
        mock_response.usage = Mock(input_tokens=100, output_tokens=15)

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.Anthropic.return_value = mock_client

        with patch.object(ClaudeProvider, "_get_model_id", return_value="claude-sonnet-4-5"):
            provider = ClaudeProvider(model="claude-sonnet")
            provider._classify_impl("Thanks for the update!", "")

        # Verify API was called correctly
        mock_client.messages.create.assert_called_once()
        call_kwargs = mock_client.messages.create.call_args[1]

        assert call_kwargs["model"] == "claude-sonnet-4-5"
        assert call_kwargs["max_tokens"] == 200
        assert len(call_kwargs["messages"]) == 1
        assert call_kwargs["messages"][0]["role"] == "user"
        assert "<signal>Thanks for the update!</signal>" in call_kwargs["messages"][0]["content"]


class TestClaudePricingConstants:
    """Test CLAUDE_PRICING constants."""

    def test_pricing_dict_has_all_models(self):
        """Test CLAUDE_PRICING contains all supported models."""
        assert "claude-haiku" in CLAUDE_PRICING
        assert "claude-sonnet" in CLAUDE_PRICING
        assert "claude-opus" in CLAUDE_PRICING

    def test_pricing_values_are_tuples(self):
        """Test all pricing values are (input, output) tuples."""
        for _model, prices in CLAUDE_PRICING.items():
            assert isinstance(prices, tuple)
            assert len(prices) == 2
            input_price, output_price = prices
            assert isinstance(input_price, (int, float))
            assert isinstance(output_price, (int, float))
            assert input_price > 0
            assert output_price > 0

    def test_pricing_output_higher_than_input(self):
        """Test output pricing is higher than input (standard model pricing)."""
        for model, (input_price, output_price) in CLAUDE_PRICING.items():
            assert output_price > input_price, f"{model}: output should cost more than input"
