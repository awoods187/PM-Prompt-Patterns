# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Google Gemini 2.5 Provider implementation.

This module provides integration with Google's Gemini models (Gemini 2.5 Pro, Flash)
with support for massive context windows, multimodal capabilities, and context caching.

Security:
    API key is loaded from environment variable GOOGLE_API_KEY.
    Never hardcode credentials.

Example:
    >>> from pm_prompt_toolkit.providers import GeminiProvider
    >>> provider = GeminiProvider(model="gemini-2-5-flash")
    >>> result = provider.classify("We need SSO integration")
    >>> print(result.category, result.confidence)
    feature_request 0.96
"""

import json
import logging
from typing import Tuple

try:
    import google.generativeai as genai
except ImportError:
    genai = None  # type: ignore[assignment]

from pm_prompt_toolkit.config import get_settings
from pm_prompt_toolkit.providers.base import ClassificationResult, LLMProvider, SignalCategory

logger = logging.getLogger(__name__)

# Model ID mapping for Gemini
# Maps our simplified names to Gemini's model identifiers
GEMINI_MODEL_IDS = {
    "gemini-2-5-pro": "gemini-2.5-pro-002",
    "gemini-2-5-flash": "gemini-2.5-flash-001",
    "gemini-2-5-flash-lite": "gemini-2.5-flash-lite-001",
}

# Gemini pricing (per 1M tokens) - Input/Output
# Last verified: 2025-01-28
# Note: Gemini has different pricing for cached tokens
GEMINI_PRICING = {
    "gemini-2.5-pro-002": (1.25, 5.00),
    "gemini-2.5-flash-001": (0.075, 0.30),
    "gemini-2.5-flash-lite-001": (0.038, 0.15),
}

# Context caching pricing (per 1M tokens) - Write/Read
GEMINI_CACHE_PRICING = {
    "gemini-2.5-pro-002": (3.13, 0.31),
    "gemini-2.5-flash-001": (0.19, 0.019),
    "gemini-2.5-flash-lite-001": (0.095, 0.0095),
}


class GeminiProvider(LLMProvider):
    """Google Gemini 2.5 Provider with massive context and multimodal support.

    This provider implements Gemini-specific features including:
        - 2M token context window (Pro) or 1M (Flash)
        - Context caching for large repeated contexts
        - Multimodal capabilities (text + images)
        - JSON mode for structured outputs
        - Efficient pricing for high-volume tasks

    Supported Models:
        - gemini-2-5-pro: 2M context, highest quality ($1.25/$5.00 per 1M tokens)
        - gemini-2-5-flash: 1M context, fast and efficient ($0.075/$0.30 per 1M tokens)
        - gemini-2-5-flash-lite: 1M context, ultra-low cost ($0.038/$0.15 per 1M tokens)

    Example:
        >>> provider = GeminiProvider(model="gemini-2-5-flash", enable_caching=True)
        >>> result = provider.classify("Dashboard broken, getting 500 errors")
        >>> assert result.category == SignalCategory.BUG_REPORT
        >>> assert result.cost < 0.0005

    Security:
        Requires GOOGLE_API_KEY environment variable.
    """

    def __init__(
        self,
        model: str = "gemini-2-5-flash",
        enable_caching: bool = True,
    ) -> None:
        """Initialize Gemini 2.5 Provider.

        Args:
            model: Gemini model to use ('gemini-2-5-pro', 'gemini-2-5-flash', 'gemini-2-5-flash-lite')
            enable_caching: Enable context caching for cost savings

        Raises:
            ValueError: If model is not supported
            ImportError: If google-generativeai package is not installed
            ValueError: If GOOGLE_API_KEY is not configured
        """
        if genai is None:
            raise ImportError(
                "google-generativeai package is required. "
                "Install with: pip install google-generativeai"
            )

        if model not in GEMINI_MODEL_IDS:
            raise ValueError(
                f"Unsupported Gemini model: {model}. "
                f"Valid models: {list(GEMINI_MODEL_IDS.keys())}"
            )

        super().__init__(model=model, enable_caching=enable_caching)

        # Get API key from settings (validates it's configured)
        settings = get_settings()
        api_key = settings.get_api_key("google")

        # Configure Gemini
        genai.configure(api_key=api_key)

        # Get full model ID
        self.gemini_model_id = GEMINI_MODEL_IDS[model]

        # Initialize Gemini model
        generation_config = {
            "temperature": 0.3,  # Lower temperature for consistent classification
            "max_output_tokens": 200,
            "response_mime_type": "application/json",  # JSON mode
        }

        self.client = genai.GenerativeModel(
            model_name=self.gemini_model_id,
            generation_config=generation_config,  # type: ignore[arg-type]
        )

        logger.info(
            f"Gemini 2.5 Provider initialized: model={model}, model_id={self.gemini_model_id}"
        )

    def _classify_impl(self, text: str, prompt: str) -> ClassificationResult:
        """Classify using Gemini with JSON mode for structured output.

        Args:
            text: Text to classify
            prompt: Prompt template (unused, we use JSON mode format)

        Returns:
            Classification result with metrics and provider metadata

        Raises:
            Exception: On Gemini API failures
        """
        # Build classification prompt
        classification_prompt = self._build_classification_prompt(text)

        # Call Gemini API
        response = self.client.generate_content(classification_prompt)

        # Parse response
        result_text = response.text if hasattr(response, "text") else "{}"
        category, confidence, evidence = self._parse_response(result_text)

        # Calculate cost
        # Gemini returns usage metadata differently than OpenAI
        usage_metadata = getattr(response, "usage_metadata", None)
        input_tokens = getattr(usage_metadata, "prompt_token_count", 0) if usage_metadata else 0
        output_tokens = (
            getattr(usage_metadata, "candidates_token_count", 0) if usage_metadata else 0
        )
        cached_tokens = (
            getattr(usage_metadata, "cached_content_token_count", 0) if usage_metadata else 0
        )

        cost = self._calculate_cost(input_tokens, output_tokens, cached_tokens)

        # Build provider metadata
        finish_reason_obj = (
            getattr(response.candidates[0], "finish_reason", None) if response.candidates else None
        )
        provider_metadata = {
            "provider": "gemini",
            "model": self.model,
            "provider_model_id": self.gemini_model_id,
            "finish_reason": finish_reason_obj.name if finish_reason_obj else "UNKNOWN",
        }

        return ClassificationResult(
            category=category,
            confidence=confidence,
            evidence=evidence,
            method=f"gemini:{self.model}",
            cost=cost,
            tokens_used=input_tokens + output_tokens,
            cached_tokens=cached_tokens,
            model=self.model,
            provider_metadata=provider_metadata,
        )

    def _build_classification_prompt(self, text: str) -> str:
        """Build classification prompt for Gemini.

        Gemini works well with clear instructions and JSON mode.

        Args:
            text: Signal text to classify

        Returns:
            Prompt for classification
        """
        return f"""You are a customer signal classification system for B2B SaaS products.
Classify this customer signal into exactly ONE category with high accuracy.

Categories:
- feature_request: Customer requests new functionality or enhancements
- bug_report: Customer reports technical issues or broken functionality
- churn_risk: Customer expressing dissatisfaction or intent to leave
- expansion_signal: Customer showing interest in additional products/usage
- general_feedback: Other feedback not fitting the above categories

Customer signal:
"{text}"

Respond with JSON containing:
{{
  "category": "category_name",
  "confidence": 0.95,
  "evidence": "key phrase from signal"
}}

Be precise with confidence scores:
- 0.95-1.0: Absolutely clear, obvious category
- 0.85-0.94: Very clear, strong indicators
- 0.70-0.84: Clear, but some ambiguity
- Below 0.70: Uncertain, multiple possible categories

Respond with JSON only, no other text."""

    def _parse_response(self, response: str) -> Tuple[SignalCategory, float, str]:
        """Parse Gemini's JSON response.

        Expected format: {"category": "...", "confidence": 0.95, "evidence": "..."}

        Security:
            Truncates logged response to prevent sensitive customer data exposure.

        Args:
            response: JSON response from Gemini

        Returns:
            Tuple of (category, confidence, evidence)

        Raises:
            ValueError: If response format is invalid
        """
        try:
            data = json.loads(response)

            category_str = data.get("category", "").strip()
            confidence = float(data.get("confidence", 0.0))
            evidence = data.get("evidence", "").strip()

            # Validate category
            category = SignalCategory(category_str)

            return category, confidence, evidence

        except Exception as e:
            # Truncate response to prevent logging sensitive customer data
            safe_response = response[:100] + "..." if len(response) > 100 else response
            logger.error(f"Failed to parse Gemini response: {safe_response}")
            raise ValueError(f"Invalid response format: {e}") from e

    def _calculate_cost(
        self, input_tokens: int, output_tokens: int, cached_tokens: int = 0
    ) -> float:
        """Calculate cost based on Gemini pricing.

        Gemini supports context caching with different pricing for cached content.

        Args:
            input_tokens: Input tokens
            output_tokens: Output tokens
            cached_tokens: Tokens served from cache (discounted)

        Returns:
            Cost in USD
        """
        # Get base pricing
        pricing = GEMINI_PRICING.get(self.gemini_model_id)
        if not pricing:
            logger.warning(
                f"No pricing found for {self.gemini_model_id}, using default Flash pricing"
            )
            pricing = (0.075, 0.30)

        input_price, output_price = pricing

        # Get cache pricing if applicable
        cache_pricing = GEMINI_CACHE_PRICING.get(self.gemini_model_id, (0.0, 0.0))
        _, cache_read_price = cache_pricing

        # Calculate costs
        # Uncached input tokens at full price
        uncached_input = input_tokens - cached_tokens
        input_cost = (uncached_input / 1_000_000) * input_price

        # Cached tokens at reduced price
        cached_cost = (cached_tokens / 1_000_000) * cache_read_price

        # Output tokens
        output_cost = (output_tokens / 1_000_000) * output_price

        return input_cost + cached_cost + output_cost
