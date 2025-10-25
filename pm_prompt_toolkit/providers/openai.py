# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""OpenAI GPT provider implementation.

⚠️ NOT YET IMPLEMENTED - Coming in future release

This provider is planned but not yet implemented. Currently only the Claude
provider is fully functional. Contributions welcome!

Planned features:
    - GPT-3.5-Turbo and GPT-4 support
    - JSON mode for structured outputs
    - Function calling for complex classifications
    - Proper cost tracking with latest pricing

Security:
    API key will be loaded from OPENAI_API_KEY environment variable.

See Also:
    - ClaudeProvider: Fully implemented provider (use this instead)
    - CONTRIBUTING.md: How to contribute provider implementations
"""

import logging

from pm_prompt_toolkit.providers.base import ClassificationResult, LLMProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider - Not yet implemented.

    This provider is planned for a future release. Currently raises NotImplementedError.
    Use ClaudeProvider for production workloads.

    Planned Support:
        - gpt-3.5-turbo: Fast, cost-effective
        - gpt-4: High quality
        - gpt-4-turbo: Balanced performance
        - JSON mode for reliable structured outputs
        - Function calling for complex tasks

    Raises:
        NotImplementedError: Always raised on instantiation

    See Also:
        ClaudeProvider: Fully implemented and production-ready
    """

    def __init__(self, model: str = "gpt-4", enable_caching: bool = False) -> None:
        """Initialize OpenAI provider (not yet implemented).

        Args:
            model: GPT model name (not used - raises error)
            enable_caching: Enable caching (not used - raises error)

        Raises:
            NotImplementedError: Always - provider not yet implemented
        """
        super().__init__(model=model, enable_caching=enable_caching)
        raise NotImplementedError(
            "OpenAI provider not yet implemented. "
            "Use ClaudeProvider instead. "
            "Contributions welcome - see CONTRIBUTING.md"
        )

    def _classify_impl(self, text: str, prompt: str) -> ClassificationResult:
        raise NotImplementedError()

    def _calculate_cost(
        self, input_tokens: int, output_tokens: int, cached_tokens: int = 0
    ) -> float:
        raise NotImplementedError()
