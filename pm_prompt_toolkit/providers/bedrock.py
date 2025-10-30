# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""AWS Bedrock provider implementation for Claude models.

This module provides integration with AWS Bedrock for Claude models,
supporting Claude 4.5, Claude 4, and Claude 3.5 models via AWS infrastructure.

Security:
    AWS credentials are loaded from environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_SESSION_TOKEN (optional, for temporary credentials)
    Never hardcode credentials.

Example:
    >>> from pm_prompt_toolkit.providers import BedrockProvider
    >>> provider = BedrockProvider(model="claude-sonnet-4-5")
    >>> result = provider.classify("We need SSO integration")
    >>> print(result.category, result.confidence)
    feature_request 0.96
    >>> print(result.provider_metadata)
    {'provider': 'bedrock', 'region': 'us-east-1', ...}
"""

import json
import logging
from typing import Any
from xml.sax.saxutils import escape

try:
    import boto3
except ImportError:
    boto3 = None  # type: ignore[assignment]

from pm_prompt_toolkit.config import get_settings
from pm_prompt_toolkit.providers.base import ClassificationResult, LLMProvider, SignalCategory

logger = logging.getLogger(__name__)

# Model ID mapping for Bedrock
# Maps our simplified names to Bedrock's full model identifiers
BEDROCK_MODEL_IDS = {
    # Claude 4.5 models
    "claude-sonnet-4-5": "anthropic.claude-3-5-sonnet-20241022-v2:0",
    # Claude 4 models
    "claude-sonnet-4": "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "claude-opus-4-1": "anthropic.claude-3-opus-20240229-v1:0",
    "claude-opus-4": "anthropic.claude-3-opus-20240229-v1:0",
    # Claude 3.5 models (backward compatibility)
    "claude-sonnet": "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "claude-haiku": "anthropic.claude-3-5-haiku-20241022-v1:0",
    "claude-opus": "anthropic.claude-3-opus-20240229-v1:0",
}

# Bedrock pricing (per 1M tokens) - Input/Output
# Last verified: 2025-01-28
BEDROCK_PRICING = {
    "anthropic.claude-3-5-sonnet-20241022-v2:0": (3.0, 15.0),
    "anthropic.claude-3-5-sonnet-20240620-v1:0": (3.0, 15.0),
    "anthropic.claude-3-opus-20240229-v1:0": (15.0, 75.0),
    "anthropic.claude-3-5-haiku-20241022-v1:0": (1.0, 5.0),
}


class BedrockProvider(LLMProvider):
    """AWS Bedrock provider for Claude models.

    This provider uses AWS Bedrock to access Claude models, offering:
        - Enterprise-grade AWS infrastructure
        - Regional data residency options
        - AWS-native security and compliance
        - Integrated AWS billing

    Supported Models:
        - claude-sonnet-4-5: Latest Claude Sonnet 4.5 ($3/$15 per 1M tokens)
        - claude-sonnet-4: Claude Sonnet 4 ($3/$15 per 1M tokens)
        - claude-opus-4-1: Claude Opus 4.1 ($15/$75 per 1M tokens)
        - claude-haiku: Claude Haiku 3.5 ($1/$5 per 1M tokens)

    Example:
        >>> provider = BedrockProvider(model="claude-sonnet-4-5", region="us-east-1")
        >>> result = provider.classify("Dashboard broken, getting 500 errors")
        >>> assert result.category == SignalCategory.BUG_REPORT
        >>> print(result.provider_metadata)
        {'provider': 'bedrock', 'region': 'us-east-1', ...}

    Security:
        Requires AWS credentials via environment variables or IAM role.
    """

    def __init__(
        self,
        model: str = "claude-sonnet-4-5",
        enable_caching: bool = False,
        region: str | None = None,
    ) -> None:
        """Initialize Bedrock provider.

        Args:
            model: Claude model to use (e.g., 'claude-sonnet-4-5', 'claude-opus-4-1')
            enable_caching: Enable caching (Note: Bedrock caching works differently)
            region: AWS region (defaults to settings.aws_region)

        Raises:
            ValueError: If model is not supported
            ImportError: If boto3 package is not installed
            ValueError: If AWS credentials are not configured
        """
        if boto3 is None:
            raise ImportError(
                "boto3 package is required for Bedrock provider. " "Install with: pip install boto3"
            )

        if model not in BEDROCK_MODEL_IDS:
            raise ValueError(
                f"Unsupported Bedrock model: {model}. "
                f"Valid models: {list(BEDROCK_MODEL_IDS.keys())}"
            )

        super().__init__(model=model, enable_caching=enable_caching)

        # Get settings and validate Bedrock configuration
        settings = get_settings()
        settings.validate_bedrock_config()

        # Use provided region or default from settings
        self.region = region or settings.aws_region

        # Initialize Bedrock client
        session_kwargs: dict[str, Any] = {
            "aws_access_key_id": settings.aws_access_key_id,
            "aws_secret_access_key": settings.aws_secret_access_key,
            "region_name": self.region,
        }

        # Add session token if provided (for temporary credentials)
        if settings.aws_session_token:
            session_kwargs["aws_session_token"] = settings.aws_session_token

        session = boto3.Session(**session_kwargs)
        self.client = session.client("bedrock-runtime")

        # Get full model ID for API calls
        self.bedrock_model_id = BEDROCK_MODEL_IDS[model]

        logger.info(
            f"Bedrock provider initialized: model={model}, "
            f"bedrock_model_id={self.bedrock_model_id}, region={self.region}"
        )

    def _classify_impl(self, text: str, prompt: str) -> ClassificationResult:
        """Classify using Bedrock with XML-structured prompts.

        Args:
            text: Text to classify
            prompt: Prompt template (unused, we use XML format)

        Returns:
            Classification result with metrics and provider metadata

        Raises:
            Exception: On Bedrock API failures
        """
        # Build XML prompt (Claude's native format)
        xml_prompt = self._build_xml_prompt(text)

        # Prepare request body for Bedrock
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 200,
            "messages": [{"role": "user", "content": xml_prompt}],
        }

        # Call Bedrock API
        response = self.client.invoke_model(
            modelId=self.bedrock_model_id,
            body=json.dumps(request_body),
        )

        # Parse response
        response_body = json.loads(response["body"].read())

        # Extract classification from response
        result_text = response_body["content"][0]["text"]
        category, confidence, evidence = self._parse_response(result_text)

        # Calculate cost
        input_tokens = response_body["usage"]["input_tokens"]
        output_tokens = response_body["usage"]["output_tokens"]
        cost = self._calculate_cost(input_tokens, output_tokens)

        # Build provider metadata
        provider_metadata = {
            "provider": "bedrock",
            "model": self.model,
            "provider_model_id": self.bedrock_model_id,
            "region": self.region,
            "request_id": response["ResponseMetadata"].get("RequestId", ""),
        }

        return ClassificationResult(
            category=category,
            confidence=confidence,
            evidence=evidence,
            method=f"bedrock:{self.model}",
            cost=cost,
            tokens_used=input_tokens + output_tokens,
            model=self.model,
            provider_metadata=provider_metadata,
        )

    def _build_xml_prompt(self, text: str) -> str:
        """Build XML-structured prompt for Claude.

        Claude has native XML understanding, making it faster and more reliable.

        Security:
            Uses xml.sax.saxutils.escape() to prevent XML injection attacks.

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
        """Calculate cost based on Bedrock pricing.

        Note: Bedrock caching works differently than direct Anthropic API.
        This implementation uses standard pricing.

        Args:
            input_tokens: Input tokens
            output_tokens: Output tokens
            cached_tokens: Cached tokens (not currently used for Bedrock)

        Returns:
            Cost in USD
        """
        pricing = BEDROCK_PRICING.get(self.bedrock_model_id)
        if not pricing:
            logger.warning(
                f"No pricing found for {self.bedrock_model_id}, using default Sonnet pricing"
            )
            pricing = (3.0, 15.0)

        input_price, output_price = pricing

        input_cost = (input_tokens / 1_000_000) * input_price
        output_cost = (output_tokens / 1_000_000) * output_price

        return input_cost + output_cost
