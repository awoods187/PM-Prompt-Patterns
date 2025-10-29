# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
Tests for pm_prompt_toolkit/providers/base.py

Comprehensive coverage of base classes, dataclasses, enums, and abstract interfaces.
"""

from datetime import datetime
from unittest.mock import patch

import pytest

from pm_prompt_toolkit.providers.base import (
    ClassificationResult,
    LLMProvider,
    ProviderMetrics,
    SignalCategory,
)


class TestSignalCategoryEnum:
    """Test SignalCategory enum."""

    def test_all_categories_defined(self):
        """Test that all expected categories exist."""
        assert SignalCategory.FEATURE_REQUEST.value == "feature_request"
        assert SignalCategory.BUG_REPORT.value == "bug_report"
        assert SignalCategory.CHURN_RISK.value == "churn_risk"
        assert SignalCategory.EXPANSION_SIGNAL.value == "expansion_signal"
        assert SignalCategory.GENERAL_FEEDBACK.value == "general_feedback"

    def test_enum_is_string(self):
        """Test that SignalCategory inherits from str."""
        assert isinstance(SignalCategory.FEATURE_REQUEST, str)
        assert SignalCategory.FEATURE_REQUEST == "feature_request"

    def test_all_categories_unique(self):
        """Test that all category values are unique."""
        values = [cat.value for cat in SignalCategory]
        assert len(values) == len(set(values))


class TestClassificationResult:
    """Test ClassificationResult dataclass."""

    def test_valid_result_creation(self):
        """Test creating a valid classification result."""
        result = ClassificationResult(
            category=SignalCategory.FEATURE_REQUEST,
            confidence=0.95,
            evidence="need SSO integration",
            method="claude-sonnet",
            cost=0.0008,
            latency_ms=450.5,
            tokens_used=200,
            cached_tokens=50,
            model="claude-sonnet-4-5",
        )

        assert result.category == SignalCategory.FEATURE_REQUEST
        assert result.confidence == 0.95
        assert result.evidence == "need SSO integration"
        assert result.method == "claude-sonnet"
        assert result.cost == 0.0008
        assert result.latency_ms == 450.5
        assert result.tokens_used == 200
        assert result.cached_tokens == 50
        assert result.model == "claude-sonnet-4-5"

    def test_default_values(self):
        """Test default values for optional fields."""
        result = ClassificationResult(
            category=SignalCategory.BUG_REPORT,
            confidence=0.85,
            evidence="app crashes on login",
            method="test",
        )

        assert result.cost == 0.0
        assert result.latency_ms == 0.0
        assert result.tokens_used == 0
        assert result.cached_tokens == 0
        assert result.model == ""
        assert isinstance(result.timestamp, datetime)

    def test_validation_confidence_too_high(self):
        """Test validation rejects confidence > 1.0."""
        with pytest.raises(ValueError) as exc_info:
            ClassificationResult(
                category=SignalCategory.FEATURE_REQUEST,
                confidence=1.5,
                evidence="test",
                method="test",
            )
        assert "Confidence must be between 0.0 and 1.0" in str(exc_info.value)
        assert "1.5" in str(exc_info.value)

    def test_validation_confidence_too_low(self):
        """Test validation rejects confidence < 0.0."""
        with pytest.raises(ValueError) as exc_info:
            ClassificationResult(
                category=SignalCategory.BUG_REPORT,
                confidence=-0.1,
                evidence="test",
                method="test",
            )
        assert "Confidence must be between 0.0 and 1.0" in str(exc_info.value)

    def test_validation_negative_cost(self):
        """Test validation rejects negative cost."""
        with pytest.raises(ValueError) as exc_info:
            ClassificationResult(
                category=SignalCategory.CHURN_RISK,
                confidence=0.9,
                evidence="test",
                method="test",
                cost=-0.01,
            )
        assert "Cost cannot be negative" in str(exc_info.value)

    def test_validation_negative_latency(self):
        """Test validation rejects negative latency."""
        with pytest.raises(ValueError) as exc_info:
            ClassificationResult(
                category=SignalCategory.EXPANSION_SIGNAL,
                confidence=0.8,
                evidence="test",
                method="test",
                latency_ms=-10.0,
            )
        assert "Latency cannot be negative" in str(exc_info.value)

    def test_validation_boundary_confidence_values(self):
        """Test confidence boundary values (0.0 and 1.0 are valid)."""
        # 0.0 should be valid
        result_zero = ClassificationResult(
            category=SignalCategory.GENERAL_FEEDBACK,
            confidence=0.0,
            evidence="test",
            method="test",
        )
        assert result_zero.confidence == 0.0

        # 1.0 should be valid
        result_one = ClassificationResult(
            category=SignalCategory.FEATURE_REQUEST,
            confidence=1.0,
            evidence="test",
            method="test",
        )
        assert result_one.confidence == 1.0

    def test_to_dict_complete(self):
        """Test to_dict with all fields populated."""
        timestamp = datetime(2025, 1, 15, 12, 30, 45)
        result = ClassificationResult(
            category=SignalCategory.FEATURE_REQUEST,
            confidence=0.96,
            evidence="need SSO integration",
            method="claude-sonnet",
            cost=0.0008,
            latency_ms=450.5,
            tokens_used=200,
            cached_tokens=50,
            model="claude-sonnet-4-5",
            timestamp=timestamp,
        )

        result_dict = result.to_dict()

        assert result_dict["category"] == "feature_request"
        assert result_dict["confidence"] == 0.96
        assert result_dict["evidence"] == "need SSO integration"
        assert result_dict["method"] == "claude-sonnet"
        assert result_dict["cost"] == 0.0008
        assert result_dict["latency_ms"] == 450.5
        assert result_dict["tokens_used"] == 200
        assert result_dict["cached_tokens"] == 50
        assert result_dict["model"] == "claude-sonnet-4-5"
        assert result_dict["timestamp"] == "2025-01-15T12:30:45"

    def test_frozen_dataclass(self):
        """Test that ClassificationResult is immutable."""
        result = ClassificationResult(
            category=SignalCategory.BUG_REPORT,
            confidence=0.9,
            evidence="test",
            method="test",
        )

        # Should not be able to modify frozen dataclass
        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            result.confidence = 0.8


class TestProviderMetrics:
    """Test ProviderMetrics dataclass."""

    def test_initial_state(self):
        """Test metrics start at zero."""
        metrics = ProviderMetrics()

        assert metrics.total_requests == 0
        assert metrics.total_cost == 0.0
        assert metrics.total_tokens == 0
        assert metrics.total_cached_tokens == 0
        assert metrics.total_latency_ms == 0.0

    def test_average_cost_with_zero_requests(self):
        """Test average_cost returns 0 when no requests."""
        metrics = ProviderMetrics()
        assert metrics.average_cost == 0.0

    def test_average_cost_with_requests(self):
        """Test average_cost calculation."""
        metrics = ProviderMetrics()
        metrics.record_request(cost=0.001, tokens=100, latency_ms=200)
        metrics.record_request(cost=0.002, tokens=150, latency_ms=300)

        # Total cost: 0.003, Total requests: 2
        assert metrics.average_cost == pytest.approx(0.0015)

    def test_average_latency_with_zero_requests(self):
        """Test average_latency_ms returns 0 when no requests."""
        metrics = ProviderMetrics()
        assert metrics.average_latency_ms == 0.0

    def test_average_latency_with_requests(self):
        """Test average_latency_ms calculation."""
        metrics = ProviderMetrics()
        metrics.record_request(cost=0.001, tokens=100, latency_ms=200)
        metrics.record_request(cost=0.002, tokens=150, latency_ms=400)

        # Total latency: 600, Total requests: 2
        assert metrics.average_latency_ms == pytest.approx(300.0)

    def test_cache_hit_rate_with_zero_tokens(self):
        """Test cache_hit_rate returns 0 when no tokens."""
        metrics = ProviderMetrics()
        assert metrics.cache_hit_rate == 0.0

    def test_cache_hit_rate_with_tokens(self):
        """Test cache_hit_rate calculation."""
        metrics = ProviderMetrics()
        # First request: 100 tokens, 50 cached (50% hit rate)
        metrics.record_request(cost=0.001, tokens=100, latency_ms=200, cached_tokens=50)
        # Second request: 200 tokens, 100 cached (50% hit rate)
        metrics.record_request(cost=0.002, tokens=200, latency_ms=300, cached_tokens=100)

        # Total tokens: 300, Total cached: 150 = 50% overall
        assert metrics.cache_hit_rate == pytest.approx(0.5)

    def test_record_request_without_caching(self):
        """Test recording a request without cached tokens."""
        metrics = ProviderMetrics()
        metrics.record_request(cost=0.0008, tokens=200, latency_ms=450)

        assert metrics.total_requests == 1
        assert metrics.total_cost == 0.0008
        assert metrics.total_tokens == 200
        assert metrics.total_cached_tokens == 0
        assert metrics.total_latency_ms == 450

    def test_record_request_with_caching(self):
        """Test recording a request with cached tokens."""
        metrics = ProviderMetrics()
        metrics.record_request(cost=0.0005, tokens=150, latency_ms=300, cached_tokens=100)

        assert metrics.total_requests == 1
        assert metrics.total_cost == 0.0005
        assert metrics.total_tokens == 150
        assert metrics.total_cached_tokens == 100
        assert metrics.total_latency_ms == 300

    def test_record_multiple_requests(self):
        """Test accumulation across multiple requests."""
        metrics = ProviderMetrics()

        metrics.record_request(cost=0.001, tokens=100, latency_ms=200, cached_tokens=50)
        metrics.record_request(cost=0.002, tokens=150, latency_ms=300, cached_tokens=75)
        metrics.record_request(cost=0.001, tokens=120, latency_ms=250, cached_tokens=60)

        assert metrics.total_requests == 3
        assert metrics.total_cost == pytest.approx(0.004)
        assert metrics.total_tokens == 370
        assert metrics.total_cached_tokens == 185
        assert metrics.total_latency_ms == pytest.approx(750.0)

    def test_to_dict(self):
        """Test metrics serialization to dict."""
        metrics = ProviderMetrics()
        metrics.record_request(cost=0.001, tokens=100, latency_ms=200, cached_tokens=50)
        metrics.record_request(cost=0.002, tokens=200, latency_ms=400, cached_tokens=100)

        result = metrics.to_dict()

        assert result["total_requests"] == 2.0
        assert result["total_cost"] == pytest.approx(0.003)
        assert result["total_tokens"] == 300.0
        assert result["total_cached_tokens"] == 150.0
        assert result["average_cost"] == pytest.approx(0.0015)
        assert result["average_latency_ms"] == pytest.approx(300.0)
        assert result["cache_hit_rate"] == pytest.approx(0.5)


class MockProvider(LLMProvider):
    """Mock implementation of LLMProvider for testing."""

    def _classify_impl(self, text: str, prompt: str) -> ClassificationResult:
        """Mock implementation."""
        return ClassificationResult(
            category=SignalCategory.FEATURE_REQUEST,
            confidence=0.95,
            evidence="mock evidence",
            method="mock",
            cost=0.001,
            tokens_used=100,
        )

    def _calculate_cost(
        self, input_tokens: int, output_tokens: int, cached_tokens: int = 0
    ) -> float:
        """Mock implementation."""
        return (input_tokens + output_tokens) * 0.00001


class TestLLMProvider:
    """Test LLMProvider abstract base class."""

    def test_initialization(self):
        """Test provider initialization."""
        provider = MockProvider(model="test-model", enable_caching=True)

        assert provider.model == "test-model"
        assert provider.enable_caching is True
        assert isinstance(provider.metrics, ProviderMetrics)

    def test_initialization_without_caching(self):
        """Test provider initialization with caching disabled."""
        provider = MockProvider(model="test-model", enable_caching=False)

        assert provider.enable_caching is False

    def test_classify_with_valid_text(self):
        """Test successful classification."""
        provider = MockProvider(model="test-model")

        result = provider.classify("This is a test message")

        assert isinstance(result, ClassificationResult)
        assert result.category == SignalCategory.FEATURE_REQUEST
        assert result.confidence == 0.95
        assert result.model == "test-model"
        assert result.latency_ms > 0  # Should have been timed

    def test_classify_with_empty_text(self):
        """Test classification rejects empty text."""
        provider = MockProvider(model="test-model")

        with pytest.raises(ValueError) as exc_info:
            provider.classify("")
        assert "Text cannot be empty" in str(exc_info.value)

    def test_classify_with_whitespace_only(self):
        """Test classification rejects whitespace-only text."""
        provider = MockProvider(model="test-model")

        with pytest.raises(ValueError) as exc_info:
            provider.classify("   \n\t  ")
        assert "Text cannot be empty" in str(exc_info.value)

    def test_classify_with_custom_prompt(self):
        """Test classification with custom prompt."""
        provider = MockProvider(model="test-model")

        custom_prompt = "Custom prompt: {text}"
        result = provider.classify("Test text", prompt=custom_prompt)

        assert isinstance(result, ClassificationResult)

    def test_classify_uses_default_prompt_when_none(self):
        """Test that classify uses default prompt when none provided."""
        provider = MockProvider(model="test-model")

        with patch.object(provider, "_get_default_prompt", return_value="default prompt"):
            result = provider.classify("Test text")
            provider._get_default_prompt.assert_called_once()

    def test_classify_records_metrics(self):
        """Test that classification records metrics."""
        provider = MockProvider(model="test-model")

        assert provider.metrics.total_requests == 0

        provider.classify("Test message")

        assert provider.metrics.total_requests == 1
        assert provider.metrics.total_cost > 0
        assert provider.metrics.total_tokens > 0

    def test_classify_handles_implementation_exception(self):
        """Test that classify propagates implementation exceptions."""

        class FailingProvider(LLMProvider):
            def _classify_impl(self, text: str, prompt: str) -> ClassificationResult:
                raise RuntimeError("API Error")

            def _calculate_cost(
                self, input_tokens: int, output_tokens: int, cached_tokens: int = 0
            ) -> float:
                return 0.0

        provider = FailingProvider(model="test-model")

        with pytest.raises(RuntimeError) as exc_info:
            provider.classify("Test text")
        assert "API Error" in str(exc_info.value)

    def test_get_default_prompt(self):
        """Test default prompt template."""
        provider = MockProvider(model="test-model")

        prompt = provider._get_default_prompt()

        assert isinstance(prompt, str)
        assert "feature_request" in prompt
        assert "bug_report" in prompt
        assert "churn_risk" in prompt
        assert "expansion_signal" in prompt
        assert "general_feedback" in prompt
        assert "{text}" in prompt

    def test_get_metrics(self):
        """Test getting provider metrics."""
        provider = MockProvider(model="test-model")

        provider.classify("Test message 1")
        provider.classify("Test message 2")

        metrics = provider.get_metrics()

        assert isinstance(metrics, ProviderMetrics)
        assert metrics.total_requests == 2

    def test_reset_metrics(self):
        """Test resetting provider metrics."""
        provider = MockProvider(model="test-model")

        provider.classify("Test message")
        assert provider.metrics.total_requests == 1

        provider.reset_metrics()

        assert provider.metrics.total_requests == 0
        assert provider.metrics.total_cost == 0.0
        assert provider.metrics.total_tokens == 0

    def test_classify_updates_result_with_latency(self):
        """Test that classify adds latency to result."""
        provider = MockProvider(model="test-model")

        result = provider.classify("Test text")

        assert result.latency_ms > 0
        assert result.latency_ms < 10000  # Should be under 10 seconds

    def test_classify_preserves_method_from_impl(self):
        """Test that classify preserves method from implementation."""

        class CustomMethodProvider(LLMProvider):
            def _classify_impl(self, text: str, prompt: str) -> ClassificationResult:
                return ClassificationResult(
                    category=SignalCategory.BUG_REPORT,
                    confidence=0.9,
                    evidence="test",
                    method="custom-method",
                    cost=0.001,
                    tokens_used=100,
                )

            def _calculate_cost(
                self, input_tokens: int, output_tokens: int, cached_tokens: int = 0
            ) -> float:
                return 0.001

        provider = CustomMethodProvider(model="test-model")
        result = provider.classify("Test text")

        assert result.method == "custom-method"

    def test_classify_uses_model_name_when_method_empty(self):
        """Test that classify uses model name when method is not set."""

        class NoMethodProvider(LLMProvider):
            def _classify_impl(self, text: str, prompt: str) -> ClassificationResult:
                return ClassificationResult(
                    category=SignalCategory.CHURN_RISK,
                    confidence=0.85,
                    evidence="test",
                    method="",  # Empty method
                    cost=0.001,
                    tokens_used=100,
                )

            def _calculate_cost(
                self, input_tokens: int, output_tokens: int, cached_tokens: int = 0
            ) -> float:
                return 0.001

        provider = NoMethodProvider(model="my-model")
        result = provider.classify("Test text")

        assert result.method == "my-model"
