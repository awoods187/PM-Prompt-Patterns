# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

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
        enable_bedrock: Enable AWS Bedrock provider
        enable_vertex: Enable Google Vertex AI provider
        enable_openai: Enable OpenAI provider
        aws_access_key_id: AWS Access Key ID for Bedrock
        aws_secret_access_key: AWS Secret Access Key for Bedrock
        aws_session_token: AWS Session Token (optional, for temporary credentials)
        aws_region: AWS region for Bedrock API
        gcp_project_id: GCP Project ID for Vertex AI
        gcp_region: GCP region for Vertex AI
        gcp_credentials_path: Path to GCP service account credentials JSON
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
    # Provider Enable Flags
    # ========================================================================
    enable_bedrock: bool = Field(
        default=False,
        description="Enable AWS Bedrock provider for Claude models",
    )

    enable_vertex: bool = Field(
        default=False,
        description="Enable Google Vertex AI provider for Claude models",
    )

    enable_openai: bool = Field(
        default=False,
        description="Enable OpenAI provider for GPT models",
    )

    # ========================================================================
    # AWS Bedrock Configuration
    # ========================================================================
    aws_access_key_id: Optional[str] = Field(
        default=None,
        description="AWS Access Key ID for Bedrock",
        alias="AWS_ACCESS_KEY_ID",
    )

    aws_secret_access_key: Optional[str] = Field(
        default=None,
        description="AWS Secret Access Key for Bedrock",
        alias="AWS_SECRET_ACCESS_KEY",
    )

    aws_session_token: Optional[str] = Field(
        default=None,
        description="AWS Session Token for temporary credentials",
        alias="AWS_SESSION_TOKEN",
    )

    aws_region: str = Field(
        default="us-east-1",
        description="AWS region for Bedrock API",
    )

    # ========================================================================
    # Google Vertex AI Configuration
    # ========================================================================
    gcp_project_id: Optional[str] = Field(
        default=None,
        description="GCP Project ID for Vertex AI",
        alias="GCP_PROJECT_ID",
    )

    gcp_region: str = Field(
        default="us-central1",
        description="GCP region for Vertex AI",
    )

    gcp_credentials_path: Optional[str] = Field(
        default=None,
        description="Path to GCP service account credentials JSON file",
        alias="GCP_CREDENTIALS_PATH",
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
                f"Unknown provider: {provider}. " f"Valid providers: {list(key_map.keys())}"
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

    def validate_bedrock_config(self) -> None:
        """Validate that AWS Bedrock is properly configured.

        Raises:
            ValueError: If Bedrock is enabled but credentials are missing

        Example:
            >>> settings = get_settings()
            >>> settings.validate_bedrock_config()
            # Raises ValueError if enable_bedrock=True but credentials missing
        """
        if not self.enable_bedrock:
            return

        if not self.aws_access_key_id or not self.aws_secret_access_key:
            raise ValueError(
                "AWS Bedrock is enabled but credentials are missing. "
                "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in your .env file. "
                "See .env.example for configuration template."
            )

        logger.debug(f"AWS Bedrock provider is properly configured (region={self.aws_region})")

    def validate_vertex_config(self) -> None:
        """Validate that Google Vertex AI is properly configured.

        Raises:
            ValueError: If Vertex is enabled but configuration is missing

        Example:
            >>> settings = get_settings()
            >>> settings.validate_vertex_config()
            # Raises ValueError if enable_vertex=True but config missing
        """
        if not self.enable_vertex:
            return

        if not self.gcp_project_id:
            raise ValueError(
                "Google Vertex AI is enabled but GCP_PROJECT_ID is missing. "
                "Please set GCP_PROJECT_ID in your .env file. "
                "See .env.example for configuration template."
            )

        # Credentials path is optional if using default credentials
        # (e.g., from gcloud CLI or service account in GCE/GKE)
        if self.gcp_credentials_path:
            import os

            if not os.path.exists(self.gcp_credentials_path):
                raise ValueError(
                    f"GCP credentials file not found: {self.gcp_credentials_path}. "
                    "Please verify the path in GCP_CREDENTIALS_PATH."
                )

        logger.debug(
            f"Google Vertex AI provider is properly configured "
            f"(project={self.gcp_project_id}, region={self.gcp_region})"
        )


@lru_cache
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
    if settings.enable_bedrock and settings.aws_access_key_id:
        configured_providers.append("bedrock")
    if settings.enable_vertex and settings.gcp_project_id:
        configured_providers.append("vertex")
    if settings.enable_openai and settings.openai_api_key:
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
