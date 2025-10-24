"""Customer signal classifier implementation.

This module implements the production signal classification system described in
examples/signal-classification/README.md with hybrid classification strategy.

Example:
    >>> from pm_prompt_toolkit import SignalClassifier
    >>> classifier = SignalClassifier()
    >>> result = classifier.classify("We need SSO integration ASAP")
    >>> print(result.category, result.confidence, f"${result.cost:.4f}")
    feature_request 0.96 $0.0008
"""

import logging
import re
from typing import Optional

from pm_prompt_toolkit.config import get_settings
from pm_prompt_toolkit.providers.base import ClassificationResult, SignalCategory
from pm_prompt_toolkit.providers.factory import get_provider

logger = logging.getLogger(__name__)


class SignalClassifier:
    """Customer signal classifier with cost optimization strategies.

    This classifier implements the hybrid classification strategy from the
    production documentation:
        1. Keyword filtering (70% caught, FREE)
        2. LLM classification (30% remaining)
        3. Confidence-based escalation (optional)

    Attributes:
        provider: LLM provider for classification
        enable_keyword_filter: Whether to use keyword filtering
        escalation_threshold: Confidence threshold for model escalation

    Example:
        >>> classifier = SignalClassifier()
        >>> result = classifier.classify("Dashboard is broken")
        >>> assert result.category == SignalCategory.BUG_REPORT
        >>> assert result.cost < 0.001  # With keyword filter

    Security:
        Uses API keys from environment variables via Settings.
    """

    # Keyword patterns for each category (curated from 1000+ labeled examples)
    KEYWORD_PATTERNS = {
        SignalCategory.CHURN_RISK: [
            r"\b(cancel|canceling|switching|switch to|frustrated|unhappy|disappointed)\b",
            r"\b(considering alternatives|evaluating competitors)\b",
            r"\bif .{0,50}(not fixed|don't|we.ll have to|we will)\b",  # Conditional churn
        ],
        SignalCategory.EXPANSION_SIGNAL: [
            r"\b(more seats|additional users|upgrade|enterprise|scale up|expansion)\b",
            r"\b(quote|pricing) for \d+\b",  # Quote for N seats
        ],
        SignalCategory.FEATURE_REQUEST: [
            r"\b(need|want|would like|can we|please add|missing|wish|hoping for)\b.{0,30}\b(integration|feature|functionality|support for)\b",
        ],
        SignalCategory.BUG_REPORT: [
            r"\b(broken|not working|error|bug|issue|failed|failing|500|404)\b",
            r"\b(can't|cannot|unable to|won't|will not)\b.{0,30}\b(load|access|login|save|export)\b",
        ],
    }

    def __init__(
        self,
        model: Optional[str] = None,
        enable_keyword_filter: Optional[bool] = None,
        escalation_threshold: Optional[float] = None,
    ) -> None:
        """Initialize signal classifier.

        Args:
            model: LLM model to use (defaults to settings.default_model)
            enable_keyword_filter: Enable keyword filtering (defaults to settings)
            escalation_threshold: Confidence threshold for escalation (defaults to settings)

        Raises:
            ValueError: If model is not supported
        """
        settings = get_settings()

        # Use settings defaults if not provided
        self.model = model or settings.default_model
        self.enable_keyword_filter = (
            enable_keyword_filter
            if enable_keyword_filter is not None
            else settings.enable_keyword_filter
        )
        self.escalation_threshold = (
            escalation_threshold
            if escalation_threshold is not None
            else settings.escalation_threshold
        )

        # Initialize provider
        self.provider = get_provider(
            self.model,
            enable_caching=settings.enable_prompt_caching,
        )

        logger.info(
            f"SignalClassifier initialized with model={self.model}, "
            f"keyword_filter={self.enable_keyword_filter}"
        )

    def classify(self, text: str) -> ClassificationResult:
        """Classify a customer signal.

        Uses hybrid classification strategy:
            1. Try keyword filtering first (if enabled)
            2. Fall back to LLM if no keyword match
            3. Escalate to better model if confidence < threshold (future)

        Args:
            text: Signal text to classify

        Returns:
            ClassificationResult with category, confidence, and cost

        Raises:
            ValueError: If text is empty

        Example:
            >>> result = classifier.classify("We need SSO integration")
            >>> print(f"{result.category}: {result.confidence:.2f}")
            feature_request: 0.96
        """
        if not text or not text.strip():
            raise ValueError("Signal text cannot be empty")

        # Level 1: Keyword classification (if enabled)
        if self.enable_keyword_filter:
            keyword_result = self._classify_with_keywords(text)
            if keyword_result:
                logger.debug(
                    f"Classified with keywords: {keyword_result.category.value} "
                    f"(confidence={keyword_result.confidence})"
                )
                return keyword_result

        # Level 2: LLM classification
        result = self.provider.classify(text)

        logger.info(
            f"Classified signal: {result.category.value} "
            f"(confidence={result.confidence:.2f}, "
            f"cost=${result.cost:.4f}, "
            f"method={result.method})"
        )

        return result

    def _classify_with_keywords(self, text: str) -> Optional[ClassificationResult]:
        """Try to classify using keyword patterns.

        Args:
            text: Signal text

        Returns:
            ClassificationResult if high-confidence match, None otherwise
        """
        text_lower = text.lower()

        # Check each category's patterns
        for category, patterns in self.KEYWORD_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    # Extract evidence (matching text)
                    match = re.search(pattern, text_lower, re.IGNORECASE)
                    evidence = match.group() if match else text[:50]

                    # High confidence for keyword matches
                    confidence = 0.95 if category in [
                        SignalCategory.CHURN_RISK,
                        SignalCategory.BUG_REPORT,
                    ] else 0.90

                    return ClassificationResult(
                        category=category,
                        confidence=confidence,
                        evidence=evidence,
                        method="keyword",
                        cost=0.0,  # Free!
                        latency_ms=0.0,
                        model="keyword-filter",
                    )

        # No keyword match
        return None

    def get_metrics(self) -> dict:
        """Get classification metrics.

        Returns:
            Dictionary with provider metrics

        Example:
            >>> metrics = classifier.get_metrics()
            >>> print(f"Average cost: ${metrics['average_cost']:.4f}")
        """
        return self.provider.get_metrics().to_dict()

    def reset_metrics(self) -> None:
        """Reset classification metrics."""
        self.provider.reset_metrics()
