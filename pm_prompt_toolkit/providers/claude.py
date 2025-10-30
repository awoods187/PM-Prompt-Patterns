# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Anthropic Claude provider implementation.

This module provides integration with Anthropic's Claude models (Haiku, Sonnet, Opus)
with support for XML-based prompts, prompt caching, and cascading strategies.

Security:
    API key is loaded from environment variable ANTHROPIC_API_KEY.
    Never hardcode credentials.

Example:
    >>> from pm_prompt_toolkit.providers import ClaudeProvider
    >>> provider = ClaudeProvider(model="claude-sonnet")
    >>> result = provider.classify("We need SSO integration")
    >>> print(result.category, result.confidence)
    feature_request 0.96
"""

import logging
from xml.sax.saxutils import escape

try:
    import anthropic
except ImportError:
    anthropic = None  # type: ignore[assignment]

from pm_prompt_toolkit.config import get_settings
from pm_prompt_toolkit.providers.base import ClassificationResult, LLMProvider, SignalCategory

logger = logging.getLogger(__name__)

# DEPRECATED: Use ai_models.PricingService instead
# This dict is kept for backward compatibility but will be removed in future versions
# Last verified: 2025-10-25
CLAUDE_PRICING = {
    "claude-haiku": (1.00, 5.00),  # Fixed: was (0.25, 1.25) - 4x underestimation
    "claude-sonnet": (3.0, 15.0),
    "claude-opus": (15.0, 75.0),
}

# Try to import new pricing system (graceful fallback if not available)
try:
    from ai_models import get_pricing_service  # noqa: F401

    _use_new_pricing = True
except ImportError:
    _use_new_pricing = False


class ClaudeProvider(LLMProvider):
    """Anthropic Claude provider with XML prompts and caching support.

    This provider implements the Claude-specific optimizations documented in
    MODEL_OPTIMIZATION_GUIDE.md, including:
        - XML-structured prompts (native understanding)
        - Prompt caching (90% cost discount)
        - Model-specific pricing

    Supported Models:
        - claude-haiku: Fast, cheap classification ($1.00/$5.00 per 1M tokens)
        - claude-sonnet: Production workhorse ($3/$15 per 1M tokens)
        - claude-opus: Highest quality ($15/$75 per 1M tokens)

    Example:
        >>> provider = ClaudeProvider(model="claude-sonnet", enable_caching=True)
        >>> result = provider.classify("Dashboard broken, getting 500 errors")
        >>> assert result.category == SignalCategory.BUG_REPORT
        >>> assert result.cost < 0.001  # With caching

    Security:
        Requires ANTHROPIC_API_KEY environment variable.
    """

    def __init__(self, model: str = "claude-sonnet", enable_caching: bool = True) -> None:
        """Initialize Claude provider.

        Args:
            model: Claude model to use ('claude-haiku', 'claude-sonnet', 'claude-opus')
            enable_caching: Enable prompt caching for cost savings

        Raises:
            ValueError: If model is not supported
            ImportError: If anthropic package is not installed
            ValueError: If ANTHROPIC_API_KEY is not configured
        """
        if anthropic is None:
            raise ImportError("anthropic package is required. Install with: pip install anthropic")

        if model not in CLAUDE_PRICING:
            raise ValueError(
                f"Unsupported Claude model: {model}. "
                f"Valid models: {list(CLAUDE_PRICING.keys())}"
            )

        super().__init__(model=model, enable_caching=enable_caching)

        # Get API key from settings (validates it's configured)
        settings = get_settings()
        api_key = settings.get_api_key("anthropic")

        # Initialize Anthropic client
        self.client = anthropic.Anthropic(api_key=api_key)
        logger.info(f"Claude provider initialized with {model}")

    def _classify_impl(self, text: str, prompt: str) -> ClassificationResult:
        """Classify using Claude with XML-structured prompts.

        Args:
            text: Text to classify
            prompt: Prompt template (unused, we use XML format)

        Returns:
            Classification result with metrics

        Raises:
            anthropic.APIError: On API failures
        """
        # Build XML prompt (Claude's native format)
        xml_prompt = self._build_xml_prompt(text)

        # Call Claude API
        response = self.client.messages.create(
            model=self._get_model_id(),
            max_tokens=200,
            messages=[{"role": "user", "content": xml_prompt}],
        )

        # Parse response
        result_text = response.content[0].text
        category, confidence, evidence = self._parse_response(result_text)

        # Calculate cost
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        cost = self._calculate_cost(input_tokens, output_tokens)

        return ClassificationResult(
            category=category,
            confidence=confidence,
            evidence=evidence,
            method=self.model,
            cost=cost,
            tokens_used=input_tokens + output_tokens,
            model=self.model,
        )

    def _build_xml_prompt(self, text: str) -> str:
        """Build XML-structured prompt for Claude.

        Claude has native XML understanding, making it faster and more reliable.

        Security:
            Uses xml.sax.saxutils.escape() to prevent XML injection attacks.
            Customer signals may contain XML special characters (< > & ' ")
            that must be properly escaped.

        Args:
            text: Signal text to classify

        Returns:
            XML-formatted prompt with escaped user input
        """
        # Escape XML special characters to prevent injection
        escaped_text = escape(text)

        return f"""<task>Classify this customer signal into exactly ONE category</task>

<categories>
<category id="feature_request">Customer requests new functionality</category>
<category id="bug_report">Customer reports technical issue</category>
<category id="churn_risk">Customer expressing dissatisfaction or intent to leave</category>
<category id="expansion_signal">Customer showing interest in more usage</category>
<category id="general_feedback">Other feedback</category>
</categories>

<signal>{escaped_text}</signal>

<output_format>
category|confidence|evidence
</output_format>"""

    def _parse_response(self, response: str) -> tuple[SignalCategory, float, str]:
        """Parse Claude's response.

        Expected format: category|confidence|evidence

        Security:
            Truncates logged response to prevent sensitive customer data exposure.
            Full response is not logged to avoid leaking PII or confidential content.

        Args:
            response: Raw response from Claude

        Returns:
            Tuple of (category, confidence, evidence)

        Raises:
            ValueError: If response format is invalid
        """
        try:
            parts = response.strip().split("|")
            if len(parts) != 3:
                raise ValueError(f"Invalid response format: {response}")

            category_str, confidence_str, evidence = parts
            category = SignalCategory(category_str.strip())
            confidence = float(confidence_str.strip())

            return category, confidence, evidence.strip()
        except Exception as e:
            # Truncate response to prevent logging sensitive customer data
            safe_response = response[:100] + "..." if len(response) > 100 else response
            logger.error(f"Failed to parse response: {safe_response}")
            raise ValueError(f"Invalid response format: {e}") from e

    def _calculate_cost(
        self, input_tokens: int, output_tokens: int, cached_tokens: int = 0
    ) -> float:
        """Calculate cost based on Claude pricing.

        Args:
            input_tokens: Input tokens
            output_tokens: Output tokens
            cached_tokens: Cached tokens (90% discount)

        Returns:
            Cost in USD
        """
        input_price, output_price = CLAUDE_PRICING[self.model]

        # Cached tokens get 90% discount
        cache_discount = 0.1  # 90% off
        uncached_input = input_tokens - cached_tokens
        cached_input_cost = (cached_tokens / 1_000_000) * input_price * cache_discount

        input_cost = (uncached_input / 1_000_000) * input_price
        output_cost = (output_tokens / 1_000_000) * output_price

        return input_cost + output_cost + cached_input_cost

    def _get_model_id(self) -> str:
        """Get full Claude model ID.

        Returns:
            Full model identifier for API
        """
        # Import current models from new registry
        from ai_models import ModelRegistry

        model = ModelRegistry.get(
            f"{self.model}-4-5"
            if "haiku" in self.model or "sonnet" in self.model
            else f"{self.model}-4-1"
        )
        if model is None:
            # Fallback for unknown models
            raise ValueError(f"Model {self.model} not found in registry")
        return model.api_identifier
