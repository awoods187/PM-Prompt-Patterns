# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""PM Prompt Toolkit - Production-grade prompt engineering for AI-native product managers.

This package provides tools and frameworks for building production LLM systems with:
- Multi-provider support (Claude, GPT, Gemini)
- Cost optimization strategies (caching, cascading, batching)
- Quality evaluation and metrics
- Production-ready classifiers and templates

Example:
    >>> from pm_prompt_toolkit import SignalClassifier
    >>> classifier = SignalClassifier()
    >>> result = classifier.classify("We need SSO integration ASAP")
    >>> print(result.category, result.confidence)
    feature_request 0.96

For more information, see: https://github.com/awoods187/PM-Prompt-Patterns
"""

from pm_prompt_toolkit.classifiers.signal_classifier import SignalClassifier
from pm_prompt_toolkit.config.settings import Settings, get_settings
from pm_prompt_toolkit.providers.base import ClassificationResult, LLMProvider

__version__ = "0.1.0"
__author__ = "Andy Woods"

__all__ = [
    "SignalClassifier",
    "Settings",
    "get_settings",
    "ClassificationResult",
    "LLMProvider",
    "__version__",
]
