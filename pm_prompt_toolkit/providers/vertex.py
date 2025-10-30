# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Google Vertex AI provider implementation for Claude models.

This module provides integration with Google Vertex AI for Claude models,
supporting Claude 4.5, Claude 4, and Claude 3.5 models via Google Cloud infrastructure.

Security:
    GCP credentials are loaded from:
    - GCP_CREDENTIALS_PATH: Path to service account JSON file
    - Or default credentials from gcloud CLI / GCE/GKE service account
    Never hardcode credentials.

Example:
    >>> from pm_prompt_toolkit.providers import VertexProvider
    >>> provider = VertexProvider(model="claude-sonnet-4-5")
    >>> result = provider.classify("We need SSO integration")
    >>> print(result.category, result.confidence)
    feature_request 0.96
    >>> print(result.provider_metadata)
    {'provider': 'vertex', 'project_id': 'my-project', ...}
"""

import json
import logging
import os
from typing import Any
from xml.sax.saxutils import escape

try:
    from anthropic import AnthropicVertex
except ImportError:
    AnthropicVertex = None  # type: ignore[assignment, misc]

from pm_prompt_toolkit.config import get_settings
from pm_prompt_toolkit.providers.base import ClassificationResult, LLMProvider, SignalCategory

logger = logging.getLogger(__name__)

# Model ID mapping for Vertex AI
# Maps our simplified names to Vertex AI's model identifiers
VERTEX_MODEL_IDS = {
    # Claude 4.5 models
    "claude-sonnet-4-5": "claude-3-5-sonnet-v2@20241022",
    # Claude 4 models
    "claude-sonnet-4": "claude-3-5-sonnet@20240620",
    "claude-opus-4-1": "claude-3-opus@20240229",
    "claude-opus-4": "claude-3-opus@20240229",
    # Claude 3.5 models (backward compatibility)
    "claude-sonnet": "claude-3-5-sonnet-v2@20241022",
    "claude-haiku": "claude-3-5-haiku@20241022",
    "claude-opus": "claude-3-opus@20240229",
}

# Vertex AI pricing (per 1M tokens) - Input/Output
# Last verified: 2025-01-28
VERTEX_PRICING = {
    "claude-3-5-sonnet-v2@20241022": (3.0, 15.0),
    "claude-3-5-sonnet@20240620": (3.0, 15.0),
    "claude-3-opus@20240229": (15.0, 75.0),
    "claude-3-5-haiku@20241022": (1.0, 5.0),
}


class VertexProvider(LLMProvider):
    """Google Vertex AI provider for Claude models.

    This provider uses Google Vertex AI to access Claude models, offering:
        - Google Cloud Platform integration
        - Regional data residency options
        - GCP-native security and compliance
        - Integrated GCP billing

    Supported Models:
        - claude-sonnet-4-5: Latest Claude Sonnet 4.5 ($3/$15 per 1M tokens)
        - claude-sonnet-4: Claude Sonnet 4 ($3/$15 per 1M tokens)
        - claude-opus-4-1: Claude Opus 4.1 ($15/$75 per 1M tokens)
        - claude-haiku: Claude Haiku 3.5 ($1/$5 per 1M tokens)

    Example:
        >>> provider = VertexProvider(
        ...     model="claude-sonnet-4-5",
        ...     project_id="my-gcp-project",
        ...     region="us-central1"
        ... )
        >>> result = provider.classify("Dashboard broken, getting 500 errors")
        >>> assert result.category == SignalCategory.BUG_REPORT
        >>> print(result.provider_metadata)
        {'provider': 'vertex', 'project_id': 'my-gcp-project', ...}

    Security:
        Requires GCP credentials via service account JSON or default credentials.
    """

    def __init__(
        self,
        model: str = "claude-sonnet-4-5",
        enable_caching: bool = False,
        project_id: str | None = None,
        region: str | None = None,
    ) -> None:
        """Initialize Vertex AI provider.

        Args:
            model: Claude model to use (e.g., 'claude-sonnet-4-5', 'claude-opus-4-1')
            enable_caching: Enable caching (Note: Vertex caching works differently)
            project_id: GCP project ID (defaults to settings.gcp_project_id)
            region: GCP region (defaults to settings.gcp_region)

        Raises:
            ValueError: If model is not supported
            ImportError: If anthropic package with Vertex support is not installed
            ValueError: If GCP configuration is missing
        """
        if AnthropicVertex is None:
            raise ImportError(
                "anthropic[vertex] package is required for Vertex AI provider. "
                "Install with: pip install 'anthropic[vertex]'"
            )

        if model not in VERTEX_MODEL_IDS:
            raise ValueError(
                f"Unsupported Vertex model: {model}. " f"Valid models: {list(VERTEX_MODEL_IDS.keys())}"
            )

        super().__init__(model=model, enable_caching=enable_caching)

        # Get settings and validate Vertex configuration
        settings = get_settings()
        settings.validate_vertex_config()

        # Use provided values or defaults from settings
        self.project_id = project_id or settings.gcp_project_id
        self.region = region or settings.gcp_region

        # Set credentials if path is provided
        if settings.gcp_credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.gcp_credentials_path

        # Initialize Vertex AI client
        self.client = AnthropicVertex(
            project_id=self.project_id,
            region=self.region,
        )

        # Get full model ID for API calls
        self.vertex_model_id = VERTEX_MODEL_IDS[model]

        logger.info(
            f"Vertex AI provider initialized: model={model}, "
            f"vertex_model_id={self.vertex_model_id}, "
            f"project_id={self.project_id}, region={self.region}"
        )

    def _classify_impl(self, text: str, prompt: str) -> ClassificationResult:
        """Classify using Vertex AI with XML-structured prompts.

        Args:
            text: Text to classify
            prompt: Prompt template (unused, we use XML format)

        Returns:
            Classification result with metrics and provider metadata

        Raises:
            Exception: On Vertex AI API failures
        """
        # Build XML prompt (Claude's native format)
        xml_prompt = self._build_xml_prompt(text)

        # Call Vertex AI API
        response = self.client.messages.create(
            model=self.vertex_model_id,
            max_tokens=200,
            messages=[{"role": "user", "content": xml_prompt}],
        )

        # Extract classification from response
        result_text = response.content[0].text
        category, confidence, evidence = self._parse_response(result_text)

        # Calculate cost
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        cost = self._calculate_cost(input_tokens, output_tokens)

        # Build provider metadata
        provider_metadata: dict[str, Any] = {
            "provider": "vertex",
            "model": self.model,
            "provider_model_id": self.vertex_model_id,
            "project_id": self.project_id,
            "region": self.region,
        }

        return ClassificationResult(
            category=category,
            confidence=confidence,
            evidence=evidence,
            method=f"vertex:{self.model}",
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

    def _calculate_cost(self, input_tokens: int, output_tokens: int, cached_tokens: int = 0) -> float:
        """Calculate cost based on Vertex AI pricing.

        Note: Vertex AI caching works differently than direct Anthropic API.
        This implementation uses standard pricing.

        Args:
            input_tokens: Input tokens
            output_tokens: Output tokens
            cached_tokens: Cached tokens (not currently used for Vertex)

        Returns:
            Cost in USD
        """
        pricing = VERTEX_PRICING.get(self.vertex_model_id)
        if not pricing:
            logger.warning(
                f"No pricing found for {self.vertex_model_id}, using default Sonnet pricing"
            )
            pricing = (3.0, 15.0)

        input_price, output_price = pricing

        input_cost = (input_tokens / 1_000_000) * input_price
        output_cost = (output_tokens / 1_000_000) * output_price

        return input_cost + output_cost
