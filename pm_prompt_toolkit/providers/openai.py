# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""OpenAI GPT provider implementation.

🚧 IMPLEMENTATION IN PROGRESS

This module will provide integration with OpenAI's GPT models with support for
JSON mode and function calling.

Security:
    API key loaded from OPENAI_API_KEY environment variable.
"""

import logging
from typing import Optional

from pm_prompt_toolkit.providers.base import ClassificationResult, LLMProvider, SignalCategory

logger = logging.getLogger(__name__)


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider (PLACEHOLDER - Full implementation coming soon).

    TODO: Implement full OpenAI provider with:
        - JSON mode support
        - Function calling
        - GPT-3.5 and GPT-4 models
        - Proper pricing calculation
    """

    def __init__(self, model: str = "gpt-4", enable_caching: bool = False) -> None:
        super().__init__(model=model, enable_caching=enable_caching)
        raise NotImplementedError(
            "OpenAI provider not yet implemented. Use ClaudeProvider for now."
        )

    def _classify_impl(self, text: str, prompt: str) -> ClassificationResult:
        raise NotImplementedError()

    def _calculate_cost(
        self, input_tokens: int, output_tokens: int, cached_tokens: int = 0
    ) -> float:
        raise NotImplementedError()
