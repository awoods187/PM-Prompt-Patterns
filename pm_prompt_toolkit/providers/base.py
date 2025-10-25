# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Base classes and interfaces for LLM providers.

This module defines the abstract base class that all LLM providers must implement,
ensuring a consistent interface across different vendors (Claude, GPT, Gemini).

The base classes enforce:
    - Consistent classification interface
    - Cost tracking and metrics
    - Error handling patterns
    - Type safety with comprehensive type hints

Example:
    >>> class MyProvider(LLMProvider):
    ...     def _classify_impl(self, text: str, prompt: str) -> ClassificationResult:
    ...         # Implementation here
    ...         pass
"""

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class SignalCategory(str, Enum):
    """Valid categories for customer signal classification.

    These categories are mutually exclusive and collectively exhaustive (MECE)
    for B2B SaaS customer signals.

    Attributes:
        FEATURE_REQUEST: Customer requests new functionality or enhancements
        BUG_REPORT: Customer reports technical issues or broken functionality
        CHURN_RISK: Customer expressing dissatisfaction or intent to leave
        EXPANSION_SIGNAL: Customer showing interest in additional products/usage
        GENERAL_FEEDBACK: Other feedback not fitting the above categories
    """

    FEATURE_REQUEST = "feature_request"
    BUG_REPORT = "bug_report"
    CHURN_RISK = "churn_risk"
    EXPANSION_SIGNAL = "expansion_signal"
    GENERAL_FEEDBACK = "general_feedback"


@dataclass(frozen=True)
class ClassificationResult:
    """Result of a classification operation.

    This dataclass encapsulates all information about a classification,
    including the category, confidence, cost, and timing metrics.

    Attributes:
        category: The classified category
        confidence: Confidence score between 0.0 and 1.0
        evidence: Key evidence from the input text supporting the classification
        method: Classification method used (e.g., 'keyword', 'haiku', 'sonnet')
        cost: Cost of the classification in USD
        latency_ms: Time taken for classification in milliseconds
        tokens_used: Number of tokens used (input + output)
        cached_tokens: Number of tokens that were cached (if applicable)
        model: Model name used for classification
        timestamp: When the classification was performed

    Example:
        >>> result = ClassificationResult(
        ...     category=SignalCategory.FEATURE_REQUEST,
        ...     confidence=0.96,
        ...     evidence="need SSO integration",
        ...     method="claude-sonnet",
        ...     cost=0.0008,
        ...     latency_ms=450,
        ... )
    """

    category: SignalCategory
    confidence: float
    evidence: str
    method: str
    cost: float = 0.0
    latency_ms: float = 0.0
    tokens_used: int = 0
    cached_tokens: int = 0
    model: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate classification result after initialization.

        Raises:
            ValueError: If confidence is not between 0.0 and 1.0
            ValueError: If cost or latency is negative
        """
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {self.confidence}")
        if self.cost < 0:
            raise ValueError(f"Cost cannot be negative, got {self.cost}")
        if self.latency_ms < 0:
            raise ValueError(f"Latency cannot be negative, got {self.latency_ms}")

    def to_dict(self) -> Dict[str, object]:
        """Convert result to dictionary for serialization.

        Returns:
            Dictionary representation of the classification result

        Example:
            >>> result.to_dict()
            {
                'category': 'feature_request',
                'confidence': 0.96,
                'evidence': 'need SSO integration',
                ...
            }
        """
        return {
            "category": self.category.value,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "method": self.method,
            "cost": self.cost,
            "latency_ms": self.latency_ms,
            "tokens_used": self.tokens_used,
            "cached_tokens": self.cached_tokens,
            "model": self.model,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class ProviderMetrics:
    """Metrics for tracking provider performance and costs.

    This class tracks cumulative metrics across all operations for a provider,
    useful for monitoring and cost optimization.

    Attributes:
        total_requests: Total number of classification requests
        total_cost: Total cost in USD
        total_tokens: Total tokens used (input + output)
        total_cached_tokens: Total tokens served from cache
        average_latency_ms: Average latency per request
        cache_hit_rate: Percentage of requests that used cached tokens (0.0-1.0)

    Example:
        >>> metrics = ProviderMetrics()
        >>> metrics.record_request(cost=0.001, tokens=150, latency_ms=300)
        >>> print(f"Average cost: ${metrics.average_cost:.4f}")
        Average cost: $0.0010
    """

    total_requests: int = 0
    total_cost: float = 0.0
    total_tokens: int = 0
    total_cached_tokens: int = 0
    total_latency_ms: float = 0.0

    @property
    def average_cost(self) -> float:
        """Calculate average cost per request."""
        return self.total_cost / self.total_requests if self.total_requests > 0 else 0.0

    @property
    def average_latency_ms(self) -> float:
        """Calculate average latency per request."""
        return self.total_latency_ms / self.total_requests if self.total_requests > 0 else 0.0

    @property
    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate as percentage of tokens cached."""
        return self.total_cached_tokens / self.total_tokens if self.total_tokens > 0 else 0.0

    def record_request(
        self,
        cost: float,
        tokens: int,
        latency_ms: float,
        cached_tokens: int = 0,
    ) -> None:
        """Record metrics for a single request.

        Args:
            cost: Cost of the request in USD
            tokens: Total tokens used (input + output)
            latency_ms: Request latency in milliseconds
            cached_tokens: Number of tokens served from cache

        Example:
            >>> metrics.record_request(cost=0.0008, tokens=200, latency_ms=450)
        """
        self.total_requests += 1
        self.total_cost += cost
        self.total_tokens += tokens
        self.total_cached_tokens += cached_tokens
        self.total_latency_ms += latency_ms

    def to_dict(self) -> Dict[str, float]:
        """Convert metrics to dictionary.

        Returns:
            Dictionary with all metrics including calculated averages
        """
        return {
            "total_requests": float(self.total_requests),
            "total_cost": self.total_cost,
            "total_tokens": float(self.total_tokens),
            "total_cached_tokens": float(self.total_cached_tokens),
            "average_cost": self.average_cost,
            "average_latency_ms": self.average_latency_ms,
            "cache_hit_rate": self.cache_hit_rate,
        }


class LLMProvider(ABC):
    """Abstract base class for all LLM providers.

    This class defines the interface that all provider implementations must follow,
    ensuring consistency across different vendors (Claude, GPT, Gemini).

    All providers must implement:
        - _classify_impl: Core classification logic
        - _calculate_cost: Cost calculation based on token usage

    Subclasses:
        - ClaudeProvider: Anthropic Claude (Haiku, Sonnet, Opus)
        - OpenAIProvider: OpenAI GPT (GPT-3.5, GPT-4)
        - GeminiProvider: Google Gemini (Pro, Flash)

    Example:
        >>> class MyProvider(LLMProvider):
        ...     def _classify_impl(self, text, prompt):
        ...         # Call your LLM API here
        ...         return ClassificationResult(...)
        ...
        ...     def _calculate_cost(self, input_tokens, output_tokens):
        ...         return (input_tokens + output_tokens) * 0.000001
    """

    def __init__(self, model: str, enable_caching: bool = True) -> None:
        """Initialize the LLM provider.

        Args:
            model: Model name/identifier (e.g., 'claude-sonnet', 'gpt-4')
            enable_caching: Whether to enable prompt caching for cost savings

        Raises:
            ValueError: If model is not supported by this provider
        """
        self.model = model
        self.enable_caching = enable_caching
        self.metrics = ProviderMetrics()
        logger.info(f"Initialized {self.__class__.__name__} with model={model}")

    @abstractmethod
    def _classify_impl(self, text: str, prompt: str) -> ClassificationResult:
        """Implement classification logic for this provider.

        This method must be implemented by all subclasses to provide
        vendor-specific classification logic.

        Args:
            text: Text to classify
            prompt: Prompt template to use for classification

        Returns:
            ClassificationResult with category, confidence, and metrics

        Raises:
            Exception: Provider-specific exceptions (rate limits, API errors, etc.)

        Example:
            >>> def _classify_impl(self, text, prompt):
            ...     response = self.client.classify(prompt.format(text=text))
            ...     return ClassificationResult(
            ...         category=parse_category(response),
            ...         confidence=parse_confidence(response),
            ...         ...
            ...     )
        """
        pass

    @abstractmethod
    def _calculate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
        cached_tokens: int = 0,
    ) -> float:
        """Calculate cost for this provider's pricing model.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cached_tokens: Number of tokens served from cache (discounted)

        Returns:
            Cost in USD

        Example:
            >>> cost = provider._calculate_cost(
            ...     input_tokens=1000,
            ...     output_tokens=50,
            ...     cached_tokens=900  # 90% cache hit
            ... )
        """
        pass

    def classify(self, text: str, prompt: Optional[str] = None) -> ClassificationResult:
        """Classify text using this provider.

        This is the public interface for classification. It handles:
            - Timing and latency tracking
            - Metrics recording
            - Error handling and logging
            - Consistent return type

        Args:
            text: Text to classify
            prompt: Optional custom prompt (uses default if not provided)

        Returns:
            ClassificationResult with all metrics

        Raises:
            ValueError: If text is empty
            Exception: Provider-specific errors

        Example:
            >>> provider = ClaudeProvider(model="claude-sonnet")
            >>> result = provider.classify("We need SSO integration ASAP")
            >>> print(f"{result.category}: {result.confidence:.2f}")
            feature_request: 0.96
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        # Use default prompt if none provided
        if prompt is None:
            prompt = self._get_default_prompt()

        # Track timing
        start_time = time.time()

        try:
            # Call implementation
            result = self._classify_impl(text, prompt)

            # Calculate latency
            latency_ms = (time.time() - start_time) * 1000

            # Update result with latency
            result = ClassificationResult(
                category=result.category,
                confidence=result.confidence,
                evidence=result.evidence,
                method=result.method or self.model,
                cost=result.cost,
                latency_ms=latency_ms,
                tokens_used=result.tokens_used,
                cached_tokens=result.cached_tokens,
                model=self.model,
            )

            # Record metrics
            self.metrics.record_request(
                cost=result.cost,
                tokens=result.tokens_used,
                latency_ms=result.latency_ms,
                cached_tokens=result.cached_tokens,
            )

            logger.debug(
                f"Classification completed: {result.category.value} "
                f"(confidence={result.confidence:.2f}, "
                f"cost=${result.cost:.4f}, "
                f"latency={result.latency_ms:.0f}ms)"
            )

            return result

        except Exception as e:
            logger.error(f"Classification failed: {e}", exc_info=True)
            raise

    def _get_default_prompt(self) -> str:
        """Get default classification prompt.

        Returns:
            Default prompt template for signal classification

        Note:
            This can be overridden by subclasses for provider-specific optimizations.
        """
        return """Classify this customer signal into exactly ONE category:

Categories:
- feature_request: Customer requests new functionality
- bug_report: Customer reports technical issue
- churn_risk: Customer expressing dissatisfaction or intent to leave
- expansion_signal: Customer showing interest in more usage
- general_feedback: Other feedback

Signal: {text}

Output format: category|confidence|evidence
Example: feature_request|0.96|need SSO integration
"""

    def get_metrics(self) -> ProviderMetrics:
        """Get current provider metrics.

        Returns:
            Current metrics for this provider

        Example:
            >>> metrics = provider.get_metrics()
            >>> print(f"Average cost: ${metrics.average_cost:.4f}")
            >>> print(f"Cache hit rate: {metrics.cache_hit_rate:.1%}")
        """
        return self.metrics

    def reset_metrics(self) -> None:
        """Reset provider metrics to zero.

        Useful for starting fresh measurements in a new time period.

        Example:
            >>> provider.reset_metrics()
            >>> # Metrics are now at zero for new tracking period
        """
        self.metrics = ProviderMetrics()
        logger.info(f"Reset metrics for {self.__class__.__name__}")
