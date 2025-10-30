# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Mock provider for testing without real API calls.

This module provides a deterministic mock provider that returns
predictable classifications without making actual API calls,
useful for testing, development, and CI/CD pipelines.

Example:
    >>> from pm_prompt_toolkit.providers import MockProvider
    >>> provider = MockProvider(model="claude-sonnet")
    >>> result = provider.classify("We need SSO")
    >>> print(result.category, result.confidence)
    feature_request 0.95
    >>> print(result.cost)  # Always zero
    0.0
"""

import hashlib
import logging
from typing import Any, Dict, List

from pm_prompt_toolkit.providers.base import ClassificationResult, LLMProvider, SignalCategory

logger = logging.getLogger(__name__)

# Deterministic keyword-based classification rules
CLASSIFICATION_RULES = {
    "feature_request": [
        "feature",
        "request",
        "need",
        "want",
        "sso",
        "integration",
        "api",
        "enhance",
        "add",
        "support",
        "implement",
    ],
    "bug_report": [
        "bug",
        "broken",
        "error",
        "crash",
        "fail",
        "issue",
        "problem",
        "not working",
        "500",
        "404",
        "exception",
    ],
    "churn_risk": [
        "cancel",
        "churn",
        "leave",
        "competitor",
        "unhappy",
        "disappointed",
        "frustrated",
        "switching",
        "terrible",
        "awful",
    ],
    "expansion_signal": [
        "upgrade",
        "expand",
        "more",
        "additional",
        "enterprise",
        "scale",
        "growth",
        "increase",
        "team",
        "users",
    ],
}


class MockProvider(LLMProvider):
    """Mock provider for testing without real API calls.

    This provider returns deterministic classifications based on keyword
    matching, making it perfect for:
        - Unit testing
        - Integration testing
        - CI/CD pipelines
        - Development without API keys
        - Cost-free experimentation

    Features:
        - Zero cost (no API calls)
        - Instant responses (<1ms latency)
        - Deterministic results (same input = same output)
        - Keyword-based classification
        - Configurable confidence scores

    Example:
        >>> provider = MockProvider(model="claude-sonnet", base_confidence=0.90)
        >>> result = provider.classify("We need SSO integration")
        >>> assert result.category == SignalCategory.FEATURE_REQUEST
        >>> assert result.cost == 0.0
        >>> assert result.latency_ms < 5

    Note:
        This provider does NOT make real API calls and should only be
        used for testing/development, never for production classification.
    """

    def __init__(
        self,
        model: str = "mock-claude-sonnet",
        enable_caching: bool = False,
        base_confidence: float = 0.95,
    ) -> None:
        """Initialize mock provider.

        Args:
            model: Mock model name (can be any string)
            enable_caching: Ignored (no caching in mock)
            base_confidence: Base confidence score for classifications (0.0-1.0)

        Raises:
            ValueError: If base_confidence is not between 0.0 and 1.0
        """
        if not 0.0 <= base_confidence <= 1.0:
            raise ValueError(f"base_confidence must be between 0.0 and 1.0, got {base_confidence}")

        super().__init__(model=model, enable_caching=False)
        self.base_confidence = base_confidence
        logger.info(f"Mock provider initialized: model={model}, base_confidence={base_confidence}")

    def _classify_impl(self, text: str, prompt: str) -> ClassificationResult:
        """Classify using deterministic keyword matching.

        This implementation:
        1. Converts text to lowercase
        2. Counts keyword matches for each category
        3. Returns category with most matches
        4. Adds slight variation to confidence based on text hash (deterministic)
        5. Extracts evidence from matched keywords

        Args:
            text: Text to classify
            prompt: Ignored (not used in mock)

        Returns:
            Classification result with deterministic output
        """
        text_lower = text.lower()

        # Count keyword matches for each category
        scores: Dict[str, int] = {}
        evidence_keywords: Dict[str, List[str]] = {}

        for category, keywords in CLASSIFICATION_RULES.items():
            matches = []
            for keyword in keywords:
                if keyword in text_lower:
                    matches.append(keyword)

            scores[category] = len(matches)
            evidence_keywords[category] = matches

        # Find category with highest score
        if not scores or max(scores.values()) == 0:
            # Default to general_feedback if no matches
            category = SignalCategory.GENERAL_FEEDBACK
            evidence = text[:50] + "..." if len(text) > 50 else text
            match_count = 0
        else:
            best_category = max(scores, key=scores.get)  # type: ignore[arg-type]
            category = SignalCategory(best_category)
            evidence = ", ".join(evidence_keywords[best_category][:3])  # Top 3 keywords
            match_count = scores[best_category]

        # Calculate confidence with slight deterministic variation
        # Use hash of text to add variation while keeping it deterministic
        text_hash = int(hashlib.md5(text.encode()).hexdigest()[:8], 16)
        hash_variation = (text_hash % 100) / 1000  # 0.000 to 0.099

        # Higher match count = higher confidence
        confidence = min(self.base_confidence + (match_count * 0.01) - hash_variation, 1.0)
        confidence = max(confidence, 0.5)  # Minimum 0.5 confidence

        # Build provider metadata
        provider_metadata: Dict[str, Any] = {
            "provider": "mock",
            "model": self.model,
            "matched_keywords": evidence_keywords.get(category.value, []),
            "match_count": match_count,
            "is_mock": True,
        }

        return ClassificationResult(
            category=category,
            confidence=round(confidence, 2),
            evidence=evidence,
            method=f"mock:{self.model}",
            cost=0.0,  # Mock is always free
            tokens_used=len(text.split()),  # Approximate token count
            model=self.model,
            provider_metadata=provider_metadata,
        )

    def _calculate_cost(
        self, input_tokens: int, output_tokens: int, cached_tokens: int = 0
    ) -> float:
        """Calculate cost (always zero for mock).

        Args:
            input_tokens: Ignored
            output_tokens: Ignored
            cached_tokens: Ignored

        Returns:
            Always 0.0 (mock is free)
        """
        return 0.0

    def _get_default_prompt(self) -> str:
        """Get default prompt (not used in mock).

        Returns:
            Placeholder prompt
        """
        return "Mock provider does not use prompts"
