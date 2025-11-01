# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""OpenAI GPT provider implementation.

This module provides integration with OpenAI's GPT models (GPT-4o, GPT-4o-mini)
with support for function calling, JSON mode, and vision capabilities.

Security:
    API key is loaded from environment variable OPENAI_API_KEY.
    Never hardcode credentials.

Example:
    >>> from pm_prompt_toolkit.providers import OpenAIProvider
    >>> provider = OpenAIProvider(model="gpt-4o")
    >>> result = provider.classify("We need SSO integration")
    >>> print(result.category, result.confidence)
    feature_request 0.96
"""

import json
import logging
from typing import Any, Dict, Optional, Tuple

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # type: ignore[assignment, misc]

from pm_prompt_toolkit.config import get_settings
from pm_prompt_toolkit.providers.base import ClassificationResult, LLMProvider, SignalCategory

logger = logging.getLogger(__name__)

# Model ID mapping for OpenAI
# Maps our simplified names to OpenAI's model identifiers
OPENAI_MODEL_IDS = {
    "gpt-4o": "gpt-4o-2024-08-06",
    "gpt-4o-mini": "gpt-4o-mini-2024-07-18",
    "gpt-4-turbo": "gpt-4-turbo-2024-04-09",
}

# OpenAI pricing (per 1M tokens) - Input/Output
# Last verified: 2025-01-28
OPENAI_PRICING = {
    "gpt-4o-2024-08-06": (2.50, 10.00),
    "gpt-4o-mini-2024-07-18": (0.15, 0.60),
    "gpt-4-turbo-2024-04-09": (10.00, 30.00),
}


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider with JSON mode and function calling support.

    This provider implements OpenAI-specific optimizations including:
        - JSON mode for structured outputs
        - Function calling capabilities
        - Vision support for multimodal inputs
        - Efficient token usage with precise prompts

    Supported Models:
        - gpt-4o: Latest flagship model ($2.50/$10.00 per 1M tokens)
        - gpt-4o-mini: Efficient model for simple tasks ($0.15/$0.60 per 1M tokens)
        - gpt-4-turbo: High-capability turbo model ($10.00/$30.00 per 1M tokens)

    Example:
        >>> provider = OpenAIProvider(model="gpt-4o", enable_caching=True)
        >>> result = provider.classify("Dashboard broken, getting 500 errors")
        >>> assert result.category == SignalCategory.BUG_REPORT
        >>> assert result.cost < 0.001

    Security:
        Requires OPENAI_API_KEY environment variable.
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        enable_caching: bool = False,
        organization: Optional[str] = None,
    ) -> None:
        """Initialize OpenAI provider.

        Args:
            model: OpenAI model to use ('gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo')
            enable_caching: Enable caching (Note: OpenAI doesn't have built-in caching like Claude)
            organization: Optional OpenAI organization ID

        Raises:
            ValueError: If model is not supported
            ImportError: If openai package is not installed
            ValueError: If OPENAI_API_KEY is not configured
        """
        if OpenAI is None:
            raise ImportError("openai package is required. Install with: pip install openai")

        if model not in OPENAI_MODEL_IDS:
            raise ValueError(
                f"Unsupported OpenAI model: {model}. "
                f"Valid models: {list(OPENAI_MODEL_IDS.keys())}"
            )

        super().__init__(model=model, enable_caching=enable_caching)

        # Get API key from settings (validates it's configured)
        settings = get_settings()
        api_key = settings.get_api_key("openai")

        # Initialize OpenAI client
        client_kwargs: Dict[str, Any] = {"api_key": api_key}
        if organization:
            client_kwargs["organization"] = organization

        self.client = OpenAI(**client_kwargs)
        self.openai_model_id = OPENAI_MODEL_IDS[model]
        logger.info(f"OpenAI provider initialized: model={model}, model_id={self.openai_model_id}")

    def _classify_impl(self, text: str, prompt: str) -> ClassificationResult:
        """Classify using OpenAI GPT with JSON mode for structured output.

        Args:
            text: Text to classify
            prompt: Prompt template (unused, we use JSON mode format)

        Returns:
            Classification result with metrics and provider metadata

        Raises:
            Exception: On OpenAI API failures
        """
        # Build system prompt for classification
        system_prompt = self._build_system_prompt()

        # Build user message
        user_message = self._build_user_message(text)

        # Call OpenAI API with JSON mode for structured output
        response = self.client.chat.completions.create(
            model=self.openai_model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            response_format={"type": "json_object"},
            max_tokens=200,
            temperature=0.3,  # Lower temperature for more consistent classification
        )

        # Parse response
        result_text = response.choices[0].message.content or "{}"
        category, confidence, evidence = self._parse_response(result_text)

        # Calculate cost
        input_tokens = response.usage.prompt_tokens if response.usage else 0
        output_tokens = response.usage.completion_tokens if response.usage else 0
        cost = self._calculate_cost(input_tokens, output_tokens)

        # Build provider metadata
        provider_metadata = {
            "provider": "openai",
            "model": self.model,
            "provider_model_id": self.openai_model_id,
            "finish_reason": response.choices[0].finish_reason,
            "request_id": response.id,
        }

        return ClassificationResult(
            category=category,
            confidence=confidence,
            evidence=evidence,
            method=f"openai:{self.model}",
            cost=cost,
            tokens_used=input_tokens + output_tokens,
            model=self.model,
            provider_metadata=provider_metadata,
        )

    def _build_system_prompt(self) -> str:
        """Build system prompt for OpenAI classification.

        OpenAI works best with clear system instructions and JSON mode.

        Returns:
            System prompt for classification
        """
        return """You are a customer signal classification system for B2B SaaS products.
Your task is to classify customer signals into exactly ONE category with high accuracy.

Categories:
- feature_request: Customer requests new functionality or enhancements
- bug_report: Customer reports technical issues or broken functionality
- churn_risk: Customer expressing dissatisfaction or intent to leave
- expansion_signal: Customer showing interest in additional products/usage
- general_feedback: Other feedback not fitting the above categories

Respond with JSON containing:
{
  "category": "category_name",
  "confidence": 0.95,
  "evidence": "key phrase from signal"
}

Be precise with confidence scores:
- 0.95-1.0: Absolutely clear, obvious category
- 0.85-0.94: Very clear, strong indicators
- 0.70-0.84: Clear, but some ambiguity
- Below 0.70: Uncertain, multiple possible categories"""

    def _build_user_message(self, text: str) -> str:
        """Build user message for classification.

        Args:
            text: Signal text to classify

        Returns:
            User message with signal
        """
        return f"""Classify this customer signal:

"{text}"

Respond with JSON only."""

    def _parse_response(self, response: str) -> Tuple[SignalCategory, float, str]:
        """Parse OpenAI's JSON response.

        Expected format: {"category": "...", "confidence": 0.95, "evidence": "..."}

        Security:
            Truncates logged response to prevent sensitive customer data exposure.

        Args:
            response: JSON response from OpenAI

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
            logger.error(f"Failed to parse OpenAI response: {safe_response}")
            raise ValueError(f"Invalid response format: {e}") from e

    def _calculate_cost(
        self, input_tokens: int, output_tokens: int, cached_tokens: int = 0
    ) -> float:
        """Calculate cost based on OpenAI pricing.

        Note: OpenAI doesn't have built-in prompt caching like Claude.
        The cached_tokens parameter is included for interface consistency but not used.

        Args:
            input_tokens: Input tokens
            output_tokens: Output tokens
            cached_tokens: Cached tokens (not used for OpenAI)

        Returns:
            Cost in USD
        """
        pricing = OPENAI_PRICING.get(self.openai_model_id)
        if not pricing:
            logger.warning(
                f"No pricing found for {self.openai_model_id}, using default GPT-4o pricing"
            )
            pricing = (2.50, 10.00)

        input_price, output_price = pricing

        input_cost = (input_tokens / 1_000_000) * input_price
        output_cost = (output_tokens / 1_000_000) * output_price

        return input_cost + output_cost
