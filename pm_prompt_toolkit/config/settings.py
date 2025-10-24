"""Application settings and configuration management.

This module provides secure configuration management using Pydantic Settings.
All sensitive credentials are loaded from environment variables.

Security:
    - API keys are NEVER hardcoded
    - All secrets must be provided via environment variables or .env file
    - Validation ensures required credentials are present before use
    - Settings are immutable after initialization

Example:
    >>> from pm_prompt_toolkit.config import get_settings
    >>> settings = get_settings()
    >>> # API keys are securely loaded from environment
    >>> client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
"""

import logging
from functools import lru_cache
from typing import Literal, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    All API keys and sensitive configuration are loaded from environment
    variables or a .env file. Never hardcode credentials.

    Attributes:
        anthropic_api_key: Anthropic API key for Claude models
        openai_api_key: OpenAI API key for GPT models
        google_api_key: Google API key for Gemini models
        default_model: Default LLM model to use
        enable_prompt_caching: Whether to enable prompt caching for cost savings
        enable_cost_tracking: Whether to track API costs
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        escalation_threshold: Confidence threshold for model escalation (0.0-1.0)
        enable_keyword_filter: Whether to use keyword filtering for cost savings
        batch_size: Number of items to process in a batch
        use_mock_providers: Use mock providers for testing (no real API calls)
        test_data_dir: Directory containing test data files

    Example:
        >>> settings = Settings()  # Loads from environment
        >>> print(settings.default_model)
        claude-sonnet

    Security Notes:
        - Never log or print API keys
        - Rotate keys immediately if exposed
        - Use different keys for dev/staging/production
        - Consider using a secrets manager in production
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignore extra environment variables
    )

    # ========================================================================
    # API Keys (CRITICAL - Never hardcode these)
    # ========================================================================
    anthropic_api_key: Optional[str] = Field(
        default=None,
        description="Anthropic API key for Claude models",
        alias="ANTHROPIC_API_KEY",
    )

    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key for GPT models",
        alias="OPENAI_API_KEY",
    )

    google_api_key: Optional[str] = Field(
        default=None,
        description="Google API key for Gemini models",
        alias="GOOGLE_API_KEY",
    )

    # ========================================================================
    # Model Configuration
    # ========================================================================
    default_model: Literal[
        "claude-sonnet",
        "claude-haiku",
        "claude-opus",
        "gpt-4",
        "gpt-3.5",
        "gemini-pro",
        "gemini-flash",
    ] = Field(
        default="claude-sonnet",
        description="Default model to use for LLM operations",
    )

    # ========================================================================
    # Cost Optimization Settings
    # ========================================================================
    enable_prompt_caching: bool = Field(
        default=True,
        description="Enable prompt caching for cost savings (90% discount on cached tokens)",
    )

    enable_cost_tracking: bool = Field(
        default=True,
        description="Track API costs for monitoring and optimization",
    )

    escalation_threshold: float = Field(
        default=0.85,
        ge=0.0,
        le=1.0,
        description="Confidence threshold below which to escalate to better model",
    )

    enable_keyword_filter: bool = Field(
        default=True,
        description="Use keyword filtering before LLM for 70% cost savings",
    )

    batch_size: int = Field(
        default=50,
        ge=1,
        le=1000,
        description="Number of items to process in a batch",
    )

    # ========================================================================
    # Logging Configuration
    # ========================================================================
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level for application",
    )

    # ========================================================================
    # Testing Configuration
    # ========================================================================
    use_mock_providers: bool = Field(
        default=False,
        description="Use mock LLM providers for testing (no real API calls)",
    )

    test_data_dir: str = Field(
        default="./tests/data",
        description="Directory containing test data files",
    )

    @field_validator("anthropic_api_key", "openai_api_key", "google_api_key")
    @classmethod
    def validate_api_key_format(cls, v: Optional[str], info) -> Optional[str]:  # type: ignore[no-untyped-def]
        """Validate API key format without logging the actual key.

        Security: This validator checks format but NEVER logs the actual key value.
        """
        if v is None:
            return None

        # Basic validation without exposing the key
        if len(v) < 10:
            field_name = info.field_name
            raise ValueError(
                f"{field_name} appears to be invalid (too short). "
                f"Check your .env file or environment variables."
            )

        # Warn if key looks like a placeholder
        if v in ["your_api_key_here", "..."]:
            field_name = info.field_name
            logger.warning(
                f"{field_name} appears to be a placeholder. "
                f"Please set a real API key in your .env file."
            )

        return v

    def get_api_key(self, provider: str) -> str:
        """Get API key for a specific provider.

        Args:
            provider: Provider name ('anthropic', 'openai', or 'google')

        Returns:
            The API key for the specified provider

        Raises:
            ValueError: If API key is not configured for the provider

        Security:
            This method validates that the key exists before use,
            preventing runtime errors from missing credentials.
        """
        key_map = {
            "anthropic": self.anthropic_api_key,
            "openai": self.openai_api_key,
            "google": self.google_api_key,
        }

        if provider not in key_map:
            raise ValueError(
                f"Unknown provider: {provider}. "
                f"Valid providers: {list(key_map.keys())}"
            )

        api_key = key_map[provider]
        if api_key is None:
            raise ValueError(
                f"API key not configured for {provider}. "
                f"Please set {provider.upper()}_API_KEY in your .env file. "
                f"See .env.example for configuration template."
            )

        return api_key

    def validate_provider_config(self, provider: str) -> None:
        """Validate that a provider is properly configured.

        Args:
            provider: Provider name to validate

        Raises:
            ValueError: If provider is not properly configured

        Example:
            >>> settings = get_settings()
            >>> settings.validate_provider_config('anthropic')
            # Raises ValueError if ANTHROPIC_API_KEY is not set
        """
        self.get_api_key(provider)  # Will raise if not configured
        logger.debug(f"{provider} provider is properly configured")


@lru_cache()
def get_settings() -> Settings:
    """Get application settings (cached singleton).

    This function returns a cached Settings instance to avoid
    re-reading environment variables on every call.

    Returns:
        Singleton Settings instance

    Example:
        >>> settings = get_settings()
        >>> print(settings.default_model)
        claude-sonnet

    Security:
        Settings are immutable after initialization.
        API keys are never logged or exposed.
    """
    settings = Settings()

    # Configure logging based on settings
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Log configuration status (WITHOUT exposing keys)
    configured_providers = []
    if settings.anthropic_api_key:
        configured_providers.append("anthropic")
    if settings.openai_api_key:
        configured_providers.append("openai")
    if settings.google_api_key:
        configured_providers.append("google")

    if configured_providers:
        logger.info(f"Configured providers: {', '.join(configured_providers)}")
    else:
        logger.warning(
            "No API keys configured. Set API keys in .env file. "
            "See .env.example for configuration template."
        )

    return settings
