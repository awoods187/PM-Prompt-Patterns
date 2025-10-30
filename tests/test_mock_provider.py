"""
Tests for module: pm_prompt_toolkit/providers/mock.py

Coverage Target: 85%
Current Coverage: 21.15%
Priority: UTILITY

The Mock provider is critical for testing infrastructure and CI/CD pipelines.
Tests focus on deterministic behavior, keyword matching, and zero-cost guarantees.
"""


import pytest

from pm_prompt_toolkit.providers.base import SignalCategory
from pm_prompt_toolkit.providers.mock import CLASSIFICATION_RULES, MockProvider

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def mock_provider():
    """Provide a standard MockProvider instance."""
    return MockProvider(model="mock-claude-sonnet", base_confidence=0.95)


@pytest.fixture
def low_confidence_provider():
    """Provide a MockProvider with low base confidence."""
    return MockProvider(model="mock-claude-haiku", base_confidence=0.70)


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================


class TestMockProviderInitialization:
    """Test suite for MockProvider initialization."""

    def test_init_with_default_parameters_succeeds(self):
        """Test successful initialization with default parameters."""
        # Arrange & Act
        provider = MockProvider()

        # Assert
        assert provider.model == "mock-claude-sonnet"
        assert provider.base_confidence == 0.95
        assert provider.enable_caching is False

    def test_init_with_custom_model_name_succeeds(self):
        """Test initialization with custom model name."""
        # Arrange & Act
        provider = MockProvider(model="custom-mock-model")

        # Assert
        assert provider.model == "custom-mock-model"

    def test_init_with_custom_confidence_succeeds(self):
        """Test initialization with custom base confidence."""
        # Arrange & Act
        provider = MockProvider(base_confidence=0.80)

        # Assert
        assert provider.base_confidence == 0.80

    def test_init_with_caching_enabled_sets_to_false(self):
        """Test that caching is always disabled for mock provider."""
        # Arrange & Act
        provider = MockProvider(enable_caching=True)

        # Assert
        assert provider.enable_caching is False  # Always false for mock

    @pytest.mark.parametrize(
        "invalid_confidence",
        [
            -0.1,  # Negative
            1.1,  # > 1.0
            2.0,  # Way too high
            -1.0,  # Negative
        ],
    )
    def test_init_with_invalid_confidence_raises_value_error(self, invalid_confidence):
        """Test that invalid confidence values raise ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="base_confidence must be between 0.0 and 1.0"):
            MockProvider(base_confidence=invalid_confidence)

    @pytest.mark.parametrize(
        "valid_confidence",
        [
            0.0,  # Minimum
            0.5,  # Middle
            1.0,  # Maximum
        ],
    )
    def test_init_with_boundary_confidence_succeeds(self, valid_confidence):
        """Test that boundary confidence values are accepted."""
        # Arrange & Act
        provider = MockProvider(base_confidence=valid_confidence)

        # Assert
        assert provider.base_confidence == valid_confidence


# ============================================================================
# CLASSIFICATION TESTS
# ============================================================================


class TestMockProviderClassification:
    """Test suite for MockProvider classification logic."""

    def test_classify_feature_request_with_keyword_match(self, mock_provider):
        """Test classification of clear feature request."""
        # Arrange
        text = "We need SSO integration for our enterprise customers"

        # Act
        result = mock_provider.classify(text)

        # Assert
        assert result.category == SignalCategory.FEATURE_REQUEST
        assert result.confidence >= 0.85  # High confidence with keyword matches
        assert "sso" in result.evidence or "need" in result.evidence
        assert result.cost == 0.0  # Mock is always free
        assert result.provider_metadata["provider"] == "mock"
        assert result.provider_metadata["is_mock"] is True

    def test_classify_bug_report_with_error_keywords(self, mock_provider):
        """Test classification of bug report with error keywords."""
        # Arrange
        text = "The dashboard is broken and showing 500 errors"

        # Act
        result = mock_provider.classify(text)

        # Assert
        assert result.category == SignalCategory.BUG_REPORT
        assert result.confidence >= 0.85
        assert "broken" in result.evidence or "error" in result.evidence or "500" in result.evidence

    def test_classify_churn_risk_with_negative_sentiment(self, mock_provider):
        """Test classification of churn risk signal."""
        # Arrange
        text = "We are very disappointed and considering switching to a competitor"

        # Act
        result = mock_provider.classify(text)

        # Assert
        assert result.category == SignalCategory.CHURN_RISK
        assert result.confidence >= 0.85
        assert any(kw in result.evidence for kw in ["disappointed", "switching", "competitor"])

    def test_classify_expansion_signal_with_growth_keywords(self, mock_provider):
        """Test classification of expansion signal."""
        # Arrange
        text = "We want to upgrade to enterprise and add more users to our team"

        # Act
        result = mock_provider.classify(text)

        # Assert
        assert result.category == SignalCategory.EXPANSION_SIGNAL
        assert result.confidence >= 0.85
        assert any(kw in result.evidence for kw in ["upgrade", "more", "team"])

    def test_classify_general_feedback_with_no_keyword_matches(self, mock_provider):
        """Test classification defaults to general feedback when no keywords match."""
        # Arrange
        text = "The sky is blue today"

        # Act
        result = mock_provider.classify(text)

        # Assert
        assert result.category == SignalCategory.GENERAL_FEEDBACK
        assert result.confidence >= 0.50
        assert len(result.evidence) > 0

    def test_classify_returns_deterministic_results(self, mock_provider):
        """Test that same input always produces same output."""
        # Arrange
        text = "We need SSO integration"

        # Act
        result1 = mock_provider.classify(text)
        result2 = mock_provider.classify(text)

        # Assert - Results should be identical (deterministic)
        assert result1.category == result2.category
        assert result1.confidence == result2.confidence
        assert result1.evidence == result2.evidence
        assert result1.cost == result2.cost


# ============================================================================
# KEYWORD MATCHING TESTS
# ============================================================================


class TestKeywordMatching:
    """Test suite for keyword matching logic."""

    @pytest.mark.parametrize(
        "text,expected_category",
        [
            ("I want a new feature", SignalCategory.FEATURE_REQUEST),
            ("We need SSO support", SignalCategory.FEATURE_REQUEST),
            ("Please add API integration", SignalCategory.FEATURE_REQUEST),
            ("Error 500 on dashboard", SignalCategory.BUG_REPORT),
            ("Application crashed", SignalCategory.BUG_REPORT),
            ("System is not working", SignalCategory.BUG_REPORT),
            ("We're canceling our subscription", SignalCategory.CHURN_RISK),
            ("Very unhappy with service", SignalCategory.CHURN_RISK),
            ("Looking at competitors", SignalCategory.CHURN_RISK),
            ("Want to upgrade to enterprise plan", SignalCategory.EXPANSION_SIGNAL),
            ("Add more users to our team", SignalCategory.EXPANSION_SIGNAL),
            ("Increase our growth capacity", SignalCategory.EXPANSION_SIGNAL),
        ],
    )
    def test_classify_matches_expected_category(self, mock_provider, text, expected_category):
        """Test that various inputs match expected categories."""
        # Act
        result = mock_provider.classify(text)

        # Assert
        assert result.category == expected_category

    def test_classify_case_insensitive_matching(self, mock_provider):
        """Test that keyword matching is case-insensitive."""
        # Arrange
        text_lower = "we need sso integration"
        text_upper = "WE NEED SSO INTEGRATION"
        text_mixed = "We NEED sso InTeGrAtIoN"

        # Act
        result_lower = mock_provider.classify(text_lower)
        result_upper = mock_provider.classify(text_upper)
        result_mixed = mock_provider.classify(text_mixed)

        # Assert - All should classify as feature request
        assert result_lower.category == SignalCategory.FEATURE_REQUEST
        assert result_upper.category == SignalCategory.FEATURE_REQUEST
        assert result_mixed.category == SignalCategory.FEATURE_REQUEST

    def test_classify_multiple_keyword_matches_increases_confidence(self, mock_provider):
        """Test that multiple keyword matches increase confidence."""
        # Arrange
        text_one_keyword = "We need this"
        text_multiple_keywords = "We need to add a feature and implement support for SSO"

        # Act
        result_one = mock_provider.classify(text_one_keyword)
        result_multiple = mock_provider.classify(text_multiple_keywords)

        # Assert - More keywords should give higher confidence
        assert result_multiple.confidence > result_one.confidence


# ============================================================================
# CONFIDENCE CALCULATION TESTS
# ============================================================================


class TestConfidenceCalculation:
    """Test suite for confidence score calculation."""

    def test_confidence_varies_by_text_hash(self, mock_provider):
        """Test that confidence has deterministic variation based on text hash."""
        # Arrange
        text1 = "We need SSO"
        text2 = "We need SSO integration"  # Different hash

        # Act
        result1 = mock_provider.classify(text1)
        result2 = mock_provider.classify(text2)

        # Assert - Confidence should be slightly different but deterministic
        assert result1.confidence != result2.confidence  # Different due to hash
        # But same text should always give same confidence
        result1_repeat = mock_provider.classify(text1)
        assert result1.confidence == result1_repeat.confidence

    def test_confidence_has_minimum_floor(self, mock_provider):
        """Test that confidence never goes below 0.5."""
        # Arrange
        text = "x"  # Minimal text, no keywords

        # Act
        result = mock_provider.classify(text)

        # Assert
        assert result.confidence >= 0.5

    def test_confidence_has_maximum_ceiling(self, mock_provider):
        """Test that confidence never exceeds 1.0."""
        # Arrange
        # Text with many matching keywords
        text = "need want request feature add support implement enhance"

        # Act
        result = mock_provider.classify(text)

        # Assert
        assert result.confidence <= 1.0

    def test_base_confidence_affects_final_score(self):
        """Test that base_confidence parameter affects final confidence."""
        # Arrange
        text = "We need SSO"
        high_confidence_provider = MockProvider(base_confidence=0.95)
        low_confidence_provider = MockProvider(base_confidence=0.70)

        # Act
        result_high = high_confidence_provider.classify(text)
        result_low = low_confidence_provider.classify(text)

        # Assert
        assert result_high.confidence > result_low.confidence


# ============================================================================
# PROVIDER METADATA TESTS
# ============================================================================


class TestProviderMetadata:
    """Test suite for provider metadata."""

    def test_provider_metadata_includes_required_fields(self, mock_provider):
        """Test that provider metadata includes all required fields."""
        # Arrange & Act
        result = mock_provider.classify("Test text")

        # Assert
        assert "provider" in result.provider_metadata
        assert "model" in result.provider_metadata
        assert "matched_keywords" in result.provider_metadata
        assert "match_count" in result.provider_metadata
        assert "is_mock" in result.provider_metadata

    def test_provider_metadata_has_correct_values(self, mock_provider):
        """Test that provider metadata has correct values."""
        # Arrange & Act
        result = mock_provider.classify("We need SSO")

        # Assert
        assert result.provider_metadata["provider"] == "mock"
        assert result.provider_metadata["model"] == "mock-claude-sonnet"
        assert result.provider_metadata["is_mock"] is True
        assert isinstance(result.provider_metadata["matched_keywords"], list)
        assert isinstance(result.provider_metadata["match_count"], int)

    def test_matched_keywords_contains_actual_matches(self, mock_provider):
        """Test that matched_keywords contains the keywords that were found."""
        # Arrange
        text = "We need SSO integration"

        # Act
        result = mock_provider.classify(text)

        # Assert
        matched = result.provider_metadata["matched_keywords"]
        assert "need" in matched or "sso" in matched or "integration" in matched
        assert result.provider_metadata["match_count"] > 0

    def test_match_count_equals_matched_keywords_length(self, mock_provider):
        """Test that match_count matches the number of matched keywords."""
        # Arrange & Act
        result = mock_provider.classify("We need SSO support")

        # Assert
        match_count = result.provider_metadata["match_count"]
        matched_keywords = result.provider_metadata["matched_keywords"]
        assert match_count == len(matched_keywords)


# ============================================================================
# COST AND PERFORMANCE TESTS
# ============================================================================


class TestCostAndPerformance:
    """Test suite for cost and performance characteristics."""

    def test_classify_always_returns_zero_cost(self, mock_provider):
        """Test that mock provider is always free."""
        # Arrange
        texts = [
            "Short",
            "Medium length text with some words",
            "Very long text " * 100,
        ]

        # Act & Assert
        for text in texts:
            result = mock_provider.classify(text)
            assert result.cost == 0.0

    def test_calculate_cost_always_returns_zero(self, mock_provider):
        """Test that _calculate_cost always returns 0."""
        # Arrange & Act
        cost = mock_provider._calculate_cost(
            input_tokens=1000, output_tokens=500, cached_tokens=200
        )

        # Assert
        assert cost == 0.0

    def test_tokens_used_approximates_word_count(self, mock_provider):
        """Test that tokens_used is based on word count."""
        # Arrange
        text = "one two three four five"  # 5 words

        # Act
        result = mock_provider.classify(text)

        # Assert
        assert result.tokens_used == 5

    def test_classify_completes_quickly(self, mock_provider):
        """Test that classification is fast (< 5ms)."""
        # Arrange
        import time

        text = "We need SSO integration"

        # Act
        start = time.time()
        result = mock_provider.classify(text)
        duration_ms = (time.time() - start) * 1000

        # Assert
        assert duration_ms < 5  # Should be nearly instant
        assert result.latency_ms > 0  # But latency is tracked


# ============================================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================================


class TestEdgeCases:
    """Test suite for edge cases and error handling."""

    def test_classify_with_empty_string_raises_value_error(self, mock_provider):
        """Test that empty string raises ValueError."""
        # Arrange
        text = ""

        # Act & Assert
        with pytest.raises(ValueError, match="Text cannot be empty"):
            mock_provider.classify(text)

    def test_classify_with_whitespace_only_raises_value_error(self, mock_provider):
        """Test that whitespace-only text raises ValueError."""
        # Arrange
        text = "   \n\t   "

        # Act & Assert
        with pytest.raises(ValueError, match="Text cannot be empty"):
            mock_provider.classify(text)

    def test_classify_with_special_characters(self, mock_provider):
        """Test that special characters don't break classification."""
        # Arrange
        text = "We need @#$% SSO!!! 🚀"

        # Act
        result = mock_provider.classify(text)

        # Assert
        assert result.category == SignalCategory.FEATURE_REQUEST
        assert isinstance(result.confidence, float)
        assert 0.0 <= result.confidence <= 1.0

    def test_classify_with_very_long_text(self, mock_provider):
        """Test that very long text is handled gracefully."""
        # Arrange
        text = "We need SSO integration. " * 1000

        # Act
        result = mock_provider.classify(text)

        # Assert
        assert result.category == SignalCategory.FEATURE_REQUEST
        assert result.cost == 0.0

    def test_classify_with_unicode_characters(self, mock_provider):
        """Test that unicode characters are handled correctly."""
        # Arrange
        text = "我们需要 SSO intégration für Unternehmenskunden"

        # Act
        result = mock_provider.classify(text)

        # Assert
        assert isinstance(result.category, SignalCategory)
        assert result.cost == 0.0


# ============================================================================
# CLASSIFICATION RULES VALIDATION
# ============================================================================


class TestClassificationRules:
    """Test suite for the CLASSIFICATION_RULES constant."""

    def test_classification_rules_is_dict(self):
        """Test that CLASSIFICATION_RULES is a dictionary."""
        assert isinstance(CLASSIFICATION_RULES, dict)

    def test_classification_rules_has_all_categories(self):
        """Test that CLASSIFICATION_RULES covers all main categories."""
        # Arrange
        expected_categories = {"feature_request", "bug_report", "churn_risk", "expansion_signal"}

        # Act & Assert
        assert expected_categories.issubset(set(CLASSIFICATION_RULES.keys()))

    def test_classification_rules_keywords_are_lowercase(self):
        """Test that all keywords in rules are lowercase."""
        # Act & Assert
        for category, keywords in CLASSIFICATION_RULES.items():
            for keyword in keywords:
                assert (
                    keyword == keyword.lower()
                ), f"Keyword '{keyword}' in {category} is not lowercase"

    def test_classification_rules_keywords_are_strings(self):
        """Test that all keywords are strings."""
        # Act & Assert
        for category, keywords in CLASSIFICATION_RULES.items():
            assert isinstance(keywords, list)
            for keyword in keywords:
                assert isinstance(keyword, str)


# ============================================================================
# METHOD TESTS
# ============================================================================


class TestGetDefaultPrompt:
    """Test suite for _get_default_prompt method."""

    def test_get_default_prompt_returns_string(self, mock_provider):
        """Test that default prompt is a string."""
        # Act
        prompt = mock_provider._get_default_prompt()

        # Assert
        assert isinstance(prompt, str)
        assert len(prompt) > 0

    def test_get_default_prompt_indicates_mock_usage(self, mock_provider):
        """Test that default prompt mentions mock provider."""
        # Act
        prompt = mock_provider._get_default_prompt()

        # Assert
        assert "mock" in prompt.lower() or "not use" in prompt.lower()
