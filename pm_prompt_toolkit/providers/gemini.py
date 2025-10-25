# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Google Gemini provider implementation.

🚧 IMPLEMENTATION IN PROGRESS

Security:
    API key loaded from GOOGLE_API_KEY environment variable.
"""

import logging

from pm_prompt_toolkit.providers.base import ClassificationResult, LLMProvider

logger = logging.getLogger(__name__)


class GeminiProvider(LLMProvider):
    """Google Gemini provider (PLACEHOLDER - Full implementation coming soon)."""

    def __init__(self, model: str = "gemini-pro", enable_caching: bool = False) -> None:
        super().__init__(model=model, enable_caching=enable_caching)
        raise NotImplementedError(
            "Gemini provider not yet implemented. Use ClaudeProvider for now."
        )

    def _classify_impl(self, text: str, prompt: str) -> ClassificationResult:
        raise NotImplementedError()

    def _calculate_cost(
        self, input_tokens: int, output_tokens: int, cached_tokens: int = 0
    ) -> float:
        raise NotImplementedError()
