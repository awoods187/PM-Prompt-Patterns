# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Google Gemini provider implementation.

⚠️ NOT YET IMPLEMENTED - Coming in future release

This provider is planned but not yet implemented. Currently only the Claude
provider is fully functional. Contributions welcome!

Planned features:
    - Gemini Pro and Gemini Pro Vision support
    - 1M+ token context window
    - Multimodal capabilities (text + images)
    - Competitive pricing with cost tracking

Security:
    API key will be loaded from GOOGLE_API_KEY environment variable.

See Also:
    - ClaudeProvider: Fully implemented provider (use this instead)
    - CONTRIBUTING.md: How to contribute provider implementations
"""

import logging

from pm_prompt_toolkit.providers.base import ClassificationResult, LLMProvider

logger = logging.getLogger(__name__)


class GeminiProvider(LLMProvider):
    """Google Gemini provider - Not yet implemented.

    This provider is planned for a future release. Currently raises NotImplementedError.
    Use ClaudeProvider for production workloads.

    Planned Support:
        - gemini-pro: Standard model with 1M+ token context
        - gemini-pro-vision: Multimodal (text + images)
        - Massive context windows for whole-codebase analysis
        - Cost-effective pricing

    Raises:
        NotImplementedError: Always raised on instantiation

    See Also:
        ClaudeProvider: Fully implemented and production-ready
    """

    def __init__(self, model: str = "gemini-pro", enable_caching: bool = False) -> None:
        """Initialize Gemini provider (not yet implemented).

        Args:
            model: Gemini model name (not used - raises error)
            enable_caching: Enable caching (not used - raises error)

        Raises:
            NotImplementedError: Always - provider not yet implemented
        """
        super().__init__(model=model, enable_caching=enable_caching)
        raise NotImplementedError(
            "Gemini provider not yet implemented. "
            "Use ClaudeProvider instead. "
            "Contributions welcome - see CONTRIBUTING.md"
        )

    def _classify_impl(self, text: str, prompt: str) -> ClassificationResult:
        raise NotImplementedError()

    def _calculate_cost(
        self, input_tokens: int, output_tokens: int, cached_tokens: int = 0
    ) -> float:
        raise NotImplementedError()
