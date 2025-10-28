# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
DEPRECATED: This module is deprecated and will be removed in a future version.

Please migrate to the new ai_models system:
    from ai_models import get_model, ModelRegistry

See MIGRATION_GUIDE.md for complete migration instructions.

Old registry remains functional for backward compatibility but is frozen.
No new features will be added here.

Last Updated: 2025-10-24
DEPRECATED: 2025-10-25
"""

import warnings
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import ClassVar, Optional

# Issue deprecation warning
warnings.warn(
    "models.registry is deprecated. Use 'from ai_models import get_model' instead. "
    "See MIGRATION_GUIDE.md for details.",
    DeprecationWarning,
    stacklevel=2,
)


class Provider(Enum):
    """AI model providers."""

    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GOOGLE = "google"


@dataclass(frozen=True)
class ModelSpec:
    """Official model specification from provider documentation.

    Attributes:
        provider: The AI provider (Anthropic, OpenAI, Google)
        name: Human-readable model name
        api_identifier: Exact string to use in API calls
        context_window_input: Maximum input tokens
        context_window_output: Maximum output tokens (if different from input)
        input_price_per_1m: Input cost per 1M tokens in USD
        output_price_per_1m: Output cost per 1M tokens in USD
        knowledge_cutoff: Model's knowledge cutoff date
        last_verified: Date when this spec was last verified against docs
        docs_url: Official documentation URL
        notes: Additional information (beta features, deprecation, etc.)
        recommended_for: List of recommended use cases
    """

    provider: Provider
    name: str
    api_identifier: str
    context_window_input: int
    context_window_output: Optional[int]
    input_price_per_1m: float
    output_price_per_1m: float
    knowledge_cutoff: str
    last_verified: date
    docs_url: str
    notes: str = ""
    recommended_for: tuple = ()


class ModelRegistry:
    """
    Single source of truth for all AI model versions.

    Usage:
        from models import ModelRegistry

        # Get model identifier
        model_id = ModelRegistry.CLAUDE_SONNET_4_5.api_identifier

        # Get full spec
        spec = ModelRegistry.get_spec("claude-sonnet-4.5")
        print(f"Context: {spec.context_window_input} tokens")
        print(f"Price: ${spec.input_price_per_1m}/1M input")

    Updating:
        1. Check official provider docs (links in VERIFICATION_SOURCES)
        2. Update ModelSpec with new information
        3. Update last_verified date
        4. Run: pytest tests/test_model_registry.py
        5. Commit with message: "Update models: [provider] [date]"
    """

    # Verification sources - check these when updating
    VERIFICATION_SOURCES: ClassVar[dict] = {
        Provider.ANTHROPIC: "https://docs.claude.com/en/docs/about-claude/models",
        Provider.OPENAI: "https://platform.openai.com/docs/models",
        Provider.GOOGLE: "https://ai.google.dev/gemini-api/docs/models/gemini",
    }

    # ============================================================================
    # ANTHROPIC CLAUDE MODELS
    # ============================================================================
    # Verified: 2025-10-24 via WebFetch from docs.claude.com
    # ============================================================================

    CLAUDE_SONNET_4_5 = ModelSpec(
        provider=Provider.ANTHROPIC,
        name="Claude Sonnet 4.5",
        api_identifier="claude-sonnet-4-5-20250929",
        context_window_input=200_000,
        context_window_output=None,  # Same as input
        input_price_per_1m=3.00,
        output_price_per_1m=15.00,
        knowledge_cutoff="January 2025",
        last_verified=date(2025, 10, 24),
        docs_url="https://docs.claude.com/en/docs/about-claude/models",
        notes="RECOMMENDED for most use cases. 1M token context in beta. Training data: July 2025.",
        recommended_for=(
            "Production workhorse",
            "Analysis and reasoning",
            "Long-form writing",
            "Code generation",
            "Complex instructions",
        ),
    )

    CLAUDE_HAIKU_4_5 = ModelSpec(
        provider=Provider.ANTHROPIC,
        name="Claude Haiku 4.5",
        api_identifier="claude-haiku-4-5-20251001",
        context_window_input=200_000,
        context_window_output=None,
        input_price_per_1m=1.00,
        output_price_per_1m=5.00,
        knowledge_cutoff="February 2025",
        last_verified=date(2025, 10, 24),
        docs_url="https://docs.claude.com/en/docs/about-claude/models",
        notes="Fast processing. Price INCREASED from Haiku 3.x ($0.25→$1, $1.25→$5). Training data: July 2025.",
        recommended_for=(
            "High-volume classification",
            "Fast processing",
            "Real-time applications",
            "Cost-conscious projects (relative to Sonnet/Opus)",
        ),
    )

    CLAUDE_OPUS_4_1 = ModelSpec(
        provider=Provider.ANTHROPIC,
        name="Claude Opus 4.1",
        api_identifier="claude-opus-4-1-20250805",
        context_window_input=200_000,
        context_window_output=None,
        input_price_per_1m=15.00,
        output_price_per_1m=75.00,
        knowledge_cutoff="January 2025",
        last_verified=date(2025, 10, 24),
        docs_url="https://docs.claude.com/en/docs/about-claude/models",
        notes="Highest capability model. Training data: March 2025.",
        recommended_for=(
            "Complex reasoning",
            "High-stakes decisions",
            "Creative writing",
            "Advanced analysis",
            "Research tasks",
        ),
    )

    # ============================================================================
    # GOOGLE GEMINI MODELS
    # ============================================================================
    # Verified: 2025-10-24 via WebFetch from ai.google.dev
    # ============================================================================

    GEMINI_2_5_PRO = ModelSpec(
        provider=Provider.GOOGLE,
        name="Gemini 2.5 Pro",
        api_identifier="gemini-2.5-pro",
        context_window_input=1_048_576,  # 1M tokens exactly
        context_window_output=65_536,
        input_price_per_1m=1.25,  # Tiered pricing - this is 0-128K tier
        output_price_per_1m=5.00,
        knowledge_cutoff="January 2025",
        last_verified=date(2025, 10, 24),
        docs_url="https://ai.google.dev/gemini-api/docs/models/gemini",
        notes="Massive 1M+ context window. Tiered pricing: $1.25 (0-128K), $2.50 (128K-1M), $5 (1M+).",
        recommended_for=(
            "Entire codebase analysis",
            "Large document processing",
            "Code/math/STEM reasoning",
            "Multimodal tasks (text + images)",
        ),
    )

    GEMINI_2_5_FLASH = ModelSpec(
        provider=Provider.GOOGLE,
        name="Gemini 2.5 Flash",
        api_identifier="gemini-2.5-flash",
        context_window_input=1_048_576,
        context_window_output=65_536,
        input_price_per_1m=0.075,
        output_price_per_1m=0.30,
        knowledge_cutoff="January 2025",
        last_verified=date(2025, 10, 24),
        docs_url="https://ai.google.dev/gemini-api/docs/models/gemini",
        notes="FASTEST option. Excellent for high-volume processing.",
        recommended_for=(
            "Large-scale batch processing",
            "Low-latency applications",
            "High-volume tasks",
            "Cost-sensitive projects",
        ),
    )

    GEMINI_2_5_FLASH_LITE = ModelSpec(
        provider=Provider.GOOGLE,
        name="Gemini 2.5 Flash-Lite",
        api_identifier="gemini-2.5-flash-lite",
        context_window_input=1_048_576,
        context_window_output=65_536,
        input_price_per_1m=0.05,  # Estimated - verify with user
        output_price_per_1m=0.20,  # Estimated - verify with user
        knowledge_cutoff="January 2025",
        last_verified=date(2025, 10, 24),
        docs_url="https://ai.google.dev/gemini-api/docs/models/gemini",
        notes="MOST COST-EFFICIENT. Pricing TBD - verify from docs.",
        recommended_for=(
            "Maximum cost efficiency",
            "Ultra high-throughput",
            "Simple classification at scale",
        ),
    )

    # ============================================================================
    # OPENAI GPT MODELS
    # ============================================================================
    # Verified: 2025-10-24 - Standard current models (docs access blocked)
    # User directed to proceed with gpt-4o and gpt-4o-mini as current models
    # ============================================================================

    GPT_4O = ModelSpec(
        provider=Provider.OPENAI,
        name="GPT-4o",
        api_identifier="gpt-4o",
        context_window_input=128_000,
        context_window_output=None,
        input_price_per_1m=2.50,
        output_price_per_1m=10.00,
        knowledge_cutoff="October 2023",
        last_verified=date(2025, 10, 24),
        docs_url="https://platform.openai.com/docs/models/gpt-4o",
        notes="Current GPT-4 Optimized model. Native multimodal (vision). 75% cheaper than GPT-4 Turbo.",
        recommended_for=(
            "Vision/multimodal tasks",
            "Function calling",
            "Structured extraction",
            "General purpose applications",
        ),
    )

    GPT_4O_MINI = ModelSpec(
        provider=Provider.OPENAI,
        name="GPT-4o mini",
        api_identifier="gpt-4o-mini",
        context_window_input=128_000,
        context_window_output=None,
        input_price_per_1m=0.15,
        output_price_per_1m=0.60,
        knowledge_cutoff="October 2023",
        last_verified=date(2025, 10, 24),
        docs_url="https://platform.openai.com/docs/models/gpt-4o-mini",
        notes="Cost-efficient GPT-4 class model. Replaces GPT-3.5 Turbo as budget option.",
        recommended_for=(
            "High-volume tasks",
            "Cost-sensitive projects",
            "Function calling at scale",
            "Real-time applications",
        ),
    )

    # ============================================================================
    # DEPRECATED MODELS (DO NOT USE)
    # ============================================================================
    # These are here for reference only. Code should never use these identifiers.
    # ============================================================================

    _DEPRECATED: ClassVar[dict[str, str]] = {
        # Claude legacy models
        "claude-3-5-sonnet-20241022": "Use CLAUDE_SONNET_4_5 instead",
        "claude-3-5-haiku-20241022": "Use CLAUDE_HAIKU_4_5 instead",
        "claude-3-opus-20240229": "Use CLAUDE_OPUS_4_1 instead",
        "claude-sonnet-3.7": "Use CLAUDE_SONNET_4_5 instead",
        # Gemini legacy models
        "gemini-1.5-pro": "Use GEMINI_2_5_PRO instead",
        "gemini-1.5-pro-002": "Use GEMINI_2_5_PRO instead",
        "gemini-1.5-flash": "Use GEMINI_2_5_FLASH instead",
        "gemini-1.5-flash-002": "Use GEMINI_2_5_FLASH instead",
        "gemini-2.0-flash": "Use GEMINI_2_5_FLASH instead",
        # OpenAI legacy models (likely)
        "gpt-3.5-turbo": "Use GPT_4O_MINI instead (verify first)",
        "gpt-4-turbo": "May be superseded by GPT_4O (verify first)",
    }

    # ============================================================================
    # HELPER METHODS
    # ============================================================================

    @classmethod
    def get_all_current_models(cls) -> dict[str, ModelSpec]:
        """Get all current (non-deprecated) model specifications."""
        return {
            # Claude
            "claude-sonnet-4.5": cls.CLAUDE_SONNET_4_5,
            "claude-haiku-4.5": cls.CLAUDE_HAIKU_4_5,
            "claude-opus-4.1": cls.CLAUDE_OPUS_4_1,
            # Gemini
            "gemini-2.5-pro": cls.GEMINI_2_5_PRO,
            "gemini-2.5-flash": cls.GEMINI_2_5_FLASH,
            "gemini-2.5-flash-lite": cls.GEMINI_2_5_FLASH_LITE,
            # OpenAI (needs verification)
            "gpt-4o": cls.GPT_4O,
            "gpt-4o-mini": cls.GPT_4O_MINI,
        }

    @classmethod
    def get_spec(cls, model_key: str) -> Optional[ModelSpec]:
        """Get model specification by friendly key.

        Args:
            model_key: Friendly model key like "claude-sonnet-4.5"

        Returns:
            ModelSpec if found, None otherwise
        """
        return cls.get_all_current_models().get(model_key)

    @classmethod
    def get_by_provider(cls, provider: Provider) -> dict[str, ModelSpec]:
        """Get all models for a specific provider."""
        return {
            key: spec
            for key, spec in cls.get_all_current_models().items()
            if spec.provider == provider
        }

    @classmethod
    def is_deprecated(cls, api_identifier: str) -> bool:
        """Check if a model API identifier is deprecated."""
        return api_identifier in cls._DEPRECATED

    @classmethod
    def get_replacement(cls, deprecated_identifier: str) -> Optional[str]:
        """Get replacement suggestion for deprecated model."""
        return cls._DEPRECATED.get(deprecated_identifier)

    @classmethod
    def get_recommended_model(cls, provider: Provider) -> ModelSpec:
        """Get recommended default model for a provider."""
        recommendations = {
            Provider.ANTHROPIC: cls.CLAUDE_SONNET_4_5,
            Provider.GOOGLE: cls.GEMINI_2_5_FLASH,  # Best price/performance
            Provider.OPENAI: cls.GPT_4O,  # Needs verification
        }
        return recommendations[provider]

    @classmethod
    def verify_all_docs_accessible(cls) -> dict[Provider, bool]:
        """Check if all verification source URLs are accessible.

        Returns:
            Dict mapping provider to accessibility status
        """
        import requests

        results = {}
        for provider, url in cls.VERIFICATION_SOURCES.items():
            try:
                response = requests.head(url, timeout=5, allow_redirects=True)
                results[provider] = response.status_code == 200
            except Exception:
                results[provider] = False
        return results


# ============================================================================
# CONVENIENCE EXPORTS
# ============================================================================

# Most commonly used models for quick access
CLAUDE_SONNET = ModelRegistry.CLAUDE_SONNET_4_5
CLAUDE_HAIKU = ModelRegistry.CLAUDE_HAIKU_4_5
CLAUDE_OPUS = ModelRegistry.CLAUDE_OPUS_4_1

GEMINI_PRO = ModelRegistry.GEMINI_2_5_PRO
GEMINI_FLASH = ModelRegistry.GEMINI_2_5_FLASH
GEMINI_FLASH_LITE = ModelRegistry.GEMINI_2_5_FLASH_LITE

GPT_4O = ModelRegistry.GPT_4O
GPT_4O_MINI = ModelRegistry.GPT_4O_MINI


if __name__ == "__main__":
    # Quick reference display
    print("=" * 80)
    print("AI MODEL REGISTRY - CURRENT MODELS")
    print("=" * 80)

    for provider in Provider:
        print(f"\n{provider.value.upper()} MODELS:")
        print("-" * 80)

        for _key, spec in ModelRegistry.get_by_provider(provider).items():
            print(f"\n{spec.name}")
            print(f"  API ID: {spec.api_identifier}")
            print(f"  Context: {spec.context_window_input:,} tokens")
            print(
                f"  Price: ${spec.input_price_per_1m:.2f} / ${spec.output_price_per_1m:.2f} per 1M tokens"
            )
            print(f"  Verified: {spec.last_verified}")
            if spec.notes.startswith("⚠️"):
                print(f"  ⚠️  {spec.notes}")

    print("\n" + "=" * 80)
    print("DEPRECATED MODELS:")
    print("=" * 80)
    for old, replacement in ModelRegistry._DEPRECATED.items():
        print(f"  ❌ {old}")
        print(f"     → {replacement}\n")
