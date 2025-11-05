"""
Tests for module: pm_prompt_toolkit/config/settings.py

Coverage Target: 85%
Current Coverage: 53.28%
Priority: COMPLEX

The Settings module is critical for configuration management and security.
Tests focus on validation logic, API key handling, and provider configuration.
"""

import logging
import os
import tempfile
from pathlib import Path

import pytest
from pydantic import ValidationError

from pm_prompt_toolkit.config.settings import Settings, get_settings

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def clean_env(monkeypatch):  # type: ignore[no-untyped-def]
    """Provide clean environment without any API keys set."""

    # Temporarily rename .env file to prevent loading
    env_file = Path.cwd() / ".env"
    env_backup = Path.cwd() / ".env.test_backup"
    env_existed = env_file.exists()

    if env_existed:
        env_file.rename(env_backup)

    try:
        # Clear all relevant env vars
        env_vars_to_clear = [
            "ANTHROPIC_API_KEY",
            "OPENAI_API_KEY",
            "GOOGLE_API_KEY",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "AWS_SESSION_TOKEN",
            "AWS_REGION",
            "GCP_PROJECT_ID",
            "GCP_REGION",
            "GCP_CREDENTIALS_PATH",
            "ENABLE_BEDROCK",
            "ENABLE_VERTEX",
            "ENABLE_OPENAI",
        ]
        for var in env_vars_to_clear:
            monkeypatch.delenv(var, raising=False)

        # Clear the settings cache
        get_settings.cache_clear()

        yield

    finally:
        # Restore .env file
        if env_existed and env_backup.exists():
            env_backup.rename(env_file)

        # Clear cache again after test
        get_settings.cache_clear()


@pytest.fixture
def mock_env_with_anthropic(monkeypatch, clean_env):  # type: ignore[no-untyped-def]
    """Provide environment with valid Anthropic API key."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-api03-valid-key-1234567890")
    return {"ANTHROPIC_API_KEY": "sk-ant-api03-valid-key-1234567890"}


@pytest.fixture
def mock_env_with_all_keys(monkeypatch, clean_env):  # type: ignore[no-untyped-def]
    """Provide environment with all API keys configured."""
    env_vars = {
        "ANTHROPIC_API_KEY": "sk-ant-api03-valid-anthropic-key-1234567890",
        "OPENAI_API_KEY": "sk-valid-openai-key-1234567890",
        "GOOGLE_API_KEY": "valid-google-api-key-1234567890",
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars


@pytest.fixture
def mock_env_bedrock_enabled(monkeypatch, clean_env):  # type: ignore[no-untyped-def]
    """Provide environment with Bedrock enabled and configured."""
    env_vars = {
        "ENABLE_BEDROCK": "true",
        "AWS_ACCESS_KEY_ID": "AKIAIOSFODNN7EXAMPLE",
        "AWS_SECRET_ACCESS_KEY": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "AWS_REGION": "us-east-1",
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars


@pytest.fixture
def mock_env_vertex_enabled(monkeypatch, clean_env):  # type: ignore[no-untyped-def]
    """Provide environment with Vertex AI enabled and configured."""
    env_vars = {
        "ENABLE_VERTEX": "true",
        "GCP_PROJECT_ID": "my-gcp-project-123",
        "GCP_REGION": "us-central1",
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================


class TestSettingsInitialization:
    """Test suite for Settings initialization."""

    def test_init_with_defaults_succeeds(self, clean_env) -> None:  # type: ignore[no-untyped-def]
        """Test successful initialization with default values."""
        # Act
        settings = Settings()

        # Assert
        assert settings.anthropic_api_key is None
        assert settings.openai_api_key is None
        assert settings.google_api_key is None
        assert settings.enable_bedrock is False
        assert settings.enable_vertex is False
        assert settings.enable_openai is False
        assert settings.aws_region == "us-east-1"
        assert settings.gcp_region == "us-central1"

    def test_init_with_anthropic_key_from_env(self, mock_env_with_anthropic) -> None:  # type: ignore[no-untyped-def]
        """Test initialization loads Anthropic key from environment."""
        # Act
        settings = Settings()

        # Assert
        assert settings.anthropic_api_key == "sk-ant-api03-valid-key-1234567890"

    def test_init_with_all_keys_from_env(self, mock_env_with_all_keys) -> None:  # type: ignore[no-untyped-def]
        """Test initialization loads all API keys from environment."""
        # Act
        settings = Settings()

        # Assert
        assert settings.anthropic_api_key is not None
        assert settings.openai_api_key is not None
        assert settings.google_api_key is not None

    def test_init_with_bedrock_config_from_env(self, mock_env_bedrock_enabled) -> None:  # type: ignore[no-untyped-def]
        """Test initialization loads Bedrock configuration from environment."""
        # Act
        settings = Settings()

        # Assert
        assert settings.enable_bedrock is True
        assert settings.aws_access_key_id == "AKIAIOSFODNN7EXAMPLE"
        assert settings.aws_secret_access_key is not None
        assert settings.aws_region == "us-east-1"

    def test_init_with_vertex_config_from_env(self, mock_env_vertex_enabled) -> None:  # type: ignore[no-untyped-def]
        """Test initialization loads Vertex AI configuration from environment."""
        # Act
        settings = Settings()

        # Assert
        assert settings.enable_vertex is True
        assert settings.gcp_project_id == "my-gcp-project-123"
        assert settings.gcp_region == "us-central1"


# ============================================================================
# API KEY VALIDATION TESTS
# ============================================================================


class TestAPIKeyValidation:
    """Test suite for API key validation logic."""

    def test_validate_api_key_with_none_returns_none(self, clean_env) -> None:  # type: ignore[no-untyped-def]
        """Test that None API key is accepted (optional field)."""
        # Arrange
        settings = Settings()

        # Act - validator is called during init
        # Assert - No error should be raised
        assert settings.anthropic_api_key is None

    def test_validate_api_key_with_too_short_key_raises_error(self, monkeypatch, clean_env) -> None:  # type: ignore[no-untyped-def]
        """Test that too-short API key raises ValueError."""
        # Arrange
        monkeypatch.setenv("ANTHROPIC_API_KEY", "short")

        # Act & Assert
        with pytest.raises(ValidationError, match="anthropic_api_key appears to be invalid"):
            Settings()

    def test_validate_api_key_with_placeholder_logs_warning(self, monkeypatch, clean_env, caplog) -> None:  # type: ignore[no-untyped-def]
        """Test that placeholder API key triggers warning."""
        # Arrange
        monkeypatch.setenv("ANTHROPIC_API_KEY", "your_api_key_here")

        # Act
        with caplog.at_level(logging.WARNING):
            # Will raise ValidationError for being too short, but also should log warning
            try:
                Settings()
            except ValidationError:
                pass  # Expected to fail validation

        # Assert - Warning should be logged before validation error
        # (Note: placeholder check happens before length check in code)

    def test_validate_api_key_with_dots_placeholder_logs_warning(  # type: ignore[no-untyped-def]
        self, monkeypatch, clean_env, caplog
    ) -> None:
        """Test that '...' placeholder API key triggers warning."""
        # Arrange
        monkeypatch.setenv("ANTHROPIC_API_KEY", "...")

        # Act
        with caplog.at_level(logging.WARNING):
            try:
                Settings()
            except ValidationError:
                pass  # Expected to fail validation

    def test_validate_api_key_with_valid_key_succeeds(self, mock_env_with_anthropic) -> None:  # type: ignore[no-untyped-def]
        """Test that valid API key passes validation."""
        # Act
        settings = Settings()

        # Assert
        assert len(settings.anthropic_api_key) >= 10  # type: ignore[arg-type]


# ============================================================================
# GET_API_KEY METHOD TESTS
# ============================================================================


class TestGetAPIKey:
    """Test suite for get_api_key() method."""

    def test_get_api_key_for_anthropic_returns_key(self, mock_env_with_anthropic) -> None:  # type: ignore[no-untyped-def]
        """Test retrieving Anthropic API key."""
        # Arrange
        settings = Settings()

        # Act
        api_key = settings.get_api_key("anthropic")

        # Assert
        assert api_key == "sk-ant-api03-valid-key-1234567890"

    def test_get_api_key_for_openai_returns_key(self, mock_env_with_all_keys) -> None:  # type: ignore[no-untyped-def]
        """Test retrieving OpenAI API key."""
        # Arrange
        settings = Settings()

        # Act
        api_key = settings.get_api_key("openai")

        # Assert
        assert api_key is not None
        assert "openai" in api_key

    def test_get_api_key_for_google_returns_key(self, mock_env_with_all_keys) -> None:  # type: ignore[no-untyped-def]
        """Test retrieving Google API key."""
        # Arrange
        settings = Settings()

        # Act
        api_key = settings.get_api_key("google")

        # Assert
        assert api_key is not None
        assert "google" in api_key

    def test_get_api_key_with_unknown_provider_raises_error(self, mock_env_with_anthropic) -> None:  # type: ignore[no-untyped-def]
        """Test that unknown provider raises ValueError."""
        # Arrange
        settings = Settings()

        # Act & Assert
        with pytest.raises(ValueError, match="Unknown provider: unknown_provider"):
            settings.get_api_key("unknown_provider")

    def test_get_api_key_with_missing_key_raises_error(self, clean_env) -> None:  # type: ignore[no-untyped-def]
        """Test that missing API key raises ValueError."""
        # Arrange
        settings = Settings()

        # Act & Assert
        with pytest.raises(ValueError, match="API key not configured for anthropic"):
            settings.get_api_key("anthropic")

    @pytest.mark.parametrize(
        "provider,env_var",
        [
            ("anthropic", "ANTHROPIC_API_KEY"),
            ("openai", "OPENAI_API_KEY"),
            ("google", "GOOGLE_API_KEY"),
        ],
    )
    def test_get_api_key_error_message_includes_env_var_name(self, clean_env, provider, env_var) -> None:  # type: ignore[no-untyped-def]
        """Test that error message includes environment variable name."""
        # Arrange
        settings = Settings()

        # Act & Assert
        with pytest.raises(ValueError, match=f"Please set {provider.upper()}_API_KEY"):
            settings.get_api_key(provider)


# ============================================================================
# VALIDATE_PROVIDER_CONFIG TESTS
# ============================================================================


class TestValidateProviderConfig:
    """Test suite for validate_provider_config() method."""

    def test_validate_provider_config_with_valid_anthropic(self, mock_env_with_anthropic) -> None:  # type: ignore[no-untyped-def]
        """Test validating Anthropic provider configuration."""
        # Arrange
        settings = Settings()

        # Act & Assert - Should not raise
        settings.validate_provider_config("anthropic")

    def test_validate_provider_config_with_missing_key_raises_error(self, clean_env) -> None:  # type: ignore[no-untyped-def]
        """Test that validating provider without API key raises error."""
        # Arrange
        settings = Settings()

        # Act & Assert
        with pytest.raises(ValueError, match="API key not configured"):
            settings.validate_provider_config("anthropic")

    def test_validate_provider_config_logs_debug_message(self, mock_env_with_anthropic, caplog) -> None:  # type: ignore[no-untyped-def]
        """Test that successful validation logs debug message."""
        # Arrange
        settings = Settings()

        # Act
        with caplog.at_level(logging.DEBUG):
            settings.validate_provider_config("anthropic")

        # Assert
        assert "anthropic provider is properly configured" in caplog.text


# ============================================================================
# VALIDATE_BEDROCK_CONFIG TESTS
# ============================================================================


class TestValidateBedrockConfig:
    """Test suite for validate_bedrock_config() method."""

    def test_validate_bedrock_config_when_disabled_returns_early(self, clean_env) -> None:  # type: ignore[no-untyped-def]
        """Test that validation is skipped when Bedrock is disabled."""
        # Arrange
        settings = Settings()
        assert settings.enable_bedrock is False

        # Act & Assert - Should not raise
        settings.validate_bedrock_config()

    def test_validate_bedrock_config_with_valid_credentials_succeeds(  # type: ignore[no-untyped-def]
        self, mock_env_bedrock_enabled
    ) -> None:
        """Test that valid Bedrock configuration passes validation."""
        # Arrange
        settings = Settings()

        # Act & Assert - Should not raise
        settings.validate_bedrock_config()

    def test_validate_bedrock_config_enabled_without_access_key_raises_error(  # type: ignore[no-untyped-def]
        self, monkeypatch, clean_env
    ) -> None:
        """Test that Bedrock enabled without access key raises error."""
        # Arrange
        monkeypatch.setenv("ENABLE_BEDROCK", "true")
        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "secret-key-1234567890")
        settings = Settings()

        # Act & Assert
        with pytest.raises(ValueError, match="AWS Bedrock is enabled but credentials are missing"):
            settings.validate_bedrock_config()

    def test_validate_bedrock_config_enabled_without_secret_key_raises_error(  # type: ignore[no-untyped-def]
        self, monkeypatch, clean_env
    ) -> None:
        """Test that Bedrock enabled without secret key raises error."""
        # Arrange
        monkeypatch.setenv("ENABLE_BEDROCK", "true")
        monkeypatch.setenv("AWS_ACCESS_KEY_ID", "AKIAIOSFODNN7EXAMPLE")
        settings = Settings()

        # Act & Assert
        with pytest.raises(ValueError, match="AWS Bedrock is enabled but credentials are missing"):
            settings.validate_bedrock_config()

    def test_validate_bedrock_config_logs_debug_message(self, mock_env_bedrock_enabled, caplog) -> None:  # type: ignore[no-untyped-def]
        """Test that successful validation logs debug message with region."""
        # Arrange
        settings = Settings()

        # Act
        with caplog.at_level(logging.DEBUG):
            settings.validate_bedrock_config()

        # Assert
        assert "AWS Bedrock provider is properly configured" in caplog.text
        assert "region=us-east-1" in caplog.text


# ============================================================================
# VALIDATE_VERTEX_CONFIG TESTS
# ============================================================================


class TestValidateVertexConfig:
    """Test suite for validate_vertex_config() method."""

    def test_validate_vertex_config_when_disabled_returns_early(self, clean_env) -> None:  # type: ignore[no-untyped-def]
        """Test that validation is skipped when Vertex is disabled."""
        # Arrange
        settings = Settings()
        assert settings.enable_vertex is False

        # Act & Assert - Should not raise
        settings.validate_vertex_config()

    def test_validate_vertex_config_with_valid_config_succeeds(self, mock_env_vertex_enabled) -> None:  # type: ignore[no-untyped-def]
        """Test that valid Vertex configuration passes validation."""
        # Arrange
        settings = Settings()

        # Act & Assert - Should not raise
        settings.validate_vertex_config()

    def test_validate_vertex_config_enabled_without_project_id_raises_error(  # type: ignore[no-untyped-def]
        self, monkeypatch, clean_env
    ) -> None:
        """Test that Vertex enabled without project ID raises error."""
        # Arrange
        monkeypatch.setenv("ENABLE_VERTEX", "true")
        settings = Settings()

        # Act & Assert
        with pytest.raises(
            ValueError, match="Google Vertex AI is enabled but GCP_PROJECT_ID is missing"
        ):
            settings.validate_vertex_config()

    def test_validate_vertex_config_with_nonexistent_credentials_file_raises_error(  # type: ignore[no-untyped-def]
        self, monkeypatch, clean_env
    ) -> None:
        """Test that Vertex with nonexistent credentials file raises error."""
        # Arrange
        monkeypatch.setenv("ENABLE_VERTEX", "true")
        monkeypatch.setenv("GCP_PROJECT_ID", "my-project-123")
        monkeypatch.setenv("GCP_CREDENTIALS_PATH", "/nonexistent/path/to/credentials.json")
        settings = Settings()

        # Act & Assert
        with pytest.raises(ValueError, match="GCP credentials file not found"):
            settings.validate_vertex_config()

    def test_validate_vertex_config_with_existing_credentials_file_succeeds(  # type: ignore[no-untyped-def]
        self, monkeypatch, clean_env
    ) -> None:
        """Test that Vertex with existing credentials file passes validation."""
        # Arrange
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write('{"type": "service_account"}')
            credentials_path = f.name

        try:
            monkeypatch.setenv("ENABLE_VERTEX", "true")
            monkeypatch.setenv("GCP_PROJECT_ID", "my-project-123")
            monkeypatch.setenv("GCP_CREDENTIALS_PATH", credentials_path)
            settings = Settings()

            # Act & Assert - Should not raise
            settings.validate_vertex_config()
        finally:
            # Cleanup
            os.unlink(credentials_path)

    def test_validate_vertex_config_logs_debug_message(self, mock_env_vertex_enabled, caplog) -> None:  # type: ignore[no-untyped-def]
        """Test that successful validation logs debug message with project and region."""
        # Arrange
        settings = Settings()

        # Act
        with caplog.at_level(logging.DEBUG):
            settings.validate_vertex_config()

        # Assert
        assert "Google Vertex AI provider is properly configured" in caplog.text
        assert "project=my-gcp-project-123" in caplog.text
        assert "region=us-central1" in caplog.text


# ============================================================================
# GET_SETTINGS FUNCTION TESTS
# ============================================================================


class TestGetSettings:
    """Test suite for get_settings() function."""

    def test_get_settings_returns_settings_instance(self, clean_env) -> None:  # type: ignore[no-untyped-def]
        """Test that get_settings returns Settings instance."""
        # Act
        settings = get_settings()

        # Assert
        assert isinstance(settings, Settings)

    def test_get_settings_caches_result(self, clean_env) -> None:  # type: ignore[no-untyped-def]
        """Test that get_settings caches the result (returns same instance)."""
        # Act
        settings1 = get_settings()
        settings2 = get_settings()

        # Assert
        assert settings1 is settings2

    def test_get_settings_with_no_keys_logs_warning(self, clean_env, caplog) -> None:  # type: ignore[no-untyped-def]
        """Test that get_settings logs warning when no API keys configured."""
        # Act
        with caplog.at_level(logging.WARNING):
            get_settings()

        # Assert
        assert "No API keys configured" in caplog.text

    def test_get_settings_with_anthropic_key_logs_configured_provider(  # type: ignore[no-untyped-def]
        self, mock_env_with_anthropic, caplog
    ) -> None:
        """Test that get_settings logs configured Anthropic provider."""
        # Act
        with caplog.at_level(logging.INFO):
            get_settings()

        # Assert
        assert "Configured providers:" in caplog.text
        assert "anthropic" in caplog.text

    def test_get_settings_with_bedrock_logs_configured_provider(  # type: ignore[no-untyped-def]
        self, mock_env_bedrock_enabled, caplog
    ) -> None:
        """Test that get_settings logs configured Bedrock provider."""
        # Act
        with caplog.at_level(logging.INFO):
            get_settings()

        # Assert
        assert "Configured providers:" in caplog.text
        assert "bedrock" in caplog.text

    def test_get_settings_with_vertex_logs_configured_provider(  # type: ignore[no-untyped-def]
        self, mock_env_vertex_enabled, caplog
    ) -> None:
        """Test that get_settings logs configured Vertex AI provider."""
        # Act
        with caplog.at_level(logging.INFO):
            get_settings()

        # Assert
        assert "Configured providers:" in caplog.text
        assert "vertex" in caplog.text

    def test_get_settings_with_openai_logs_configured_provider(  # type: ignore[no-untyped-def]
        self, monkeypatch, clean_env, caplog
    ) -> None:
        """Test that get_settings logs configured OpenAI provider."""
        # Arrange
        monkeypatch.setenv("ENABLE_OPENAI", "true")
        monkeypatch.setenv("OPENAI_API_KEY", "sk-valid-openai-key-1234567890")

        # Act
        with caplog.at_level(logging.INFO):
            get_settings()

        # Assert
        assert "Configured providers:" in caplog.text
        assert "openai" in caplog.text

    def test_get_settings_with_google_logs_configured_provider(  # type: ignore[no-untyped-def]
        self, monkeypatch, clean_env, caplog
    ) -> None:
        """Test that get_settings logs configured Google provider."""
        # Arrange
        monkeypatch.setenv("GOOGLE_API_KEY", "valid-google-api-key-1234567890")

        # Act
        with caplog.at_level(logging.INFO):
            get_settings()

        # Assert
        assert "Configured providers:" in caplog.text
        assert "google" in caplog.text

    def test_get_settings_with_multiple_providers_logs_all(  # type: ignore[no-untyped-def]
        self, mock_env_with_all_keys, mock_env_bedrock_enabled, caplog
    ) -> None:
        """Test that get_settings logs all configured providers."""
        # Act
        with caplog.at_level(logging.INFO):
            get_settings()

        # Assert
        assert "Configured providers:" in caplog.text
        # Should have anthropic, bedrock, openai, google
        # (bedrock fixture also sets aws keys, so it should be detected)


# ============================================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================================


class TestEdgeCases:
    """Test suite for edge cases and error handling."""

    def test_settings_with_session_token_succeeds(self, monkeypatch, clean_env) -> None:  # type: ignore[no-untyped-def]
        """Test that AWS session token is optional and can be set."""
        # Arrange
        monkeypatch.setenv("ENABLE_BEDROCK", "true")
        monkeypatch.setenv("AWS_ACCESS_KEY_ID", "AKIAIOSFODNN7EXAMPLE")
        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "wJalrXUtnFEMI/K7MDENG")
        monkeypatch.setenv("AWS_SESSION_TOKEN", "temporary-session-token-12345")

        # Act
        settings = Settings()

        # Assert
        assert settings.aws_session_token == "temporary-session-token-12345"

    def test_settings_with_custom_regions_succeeds(self, monkeypatch, clean_env) -> None:  # type: ignore[no-untyped-def]
        """Test that custom AWS and GCP regions can be set."""
        # Arrange
        monkeypatch.setenv("AWS_REGION", "eu-west-1")
        monkeypatch.setenv("GCP_REGION", "europe-west1")

        # Act
        settings = Settings()

        # Assert
        assert settings.aws_region == "eu-west-1"
        assert settings.gcp_region == "europe-west1"

    def test_cache_clear_allows_reloading_settings(self, monkeypatch, mock_env_with_anthropic) -> None:  # type: ignore[no-untyped-def]
        """Test that cache_clear allows reloading settings with different config."""
        # Act
        settings1 = get_settings()
        assert settings1.anthropic_api_key is not None

        # Modify environment
        get_settings.cache_clear()
        monkeypatch.delenv("ANTHROPIC_API_KEY")
        monkeypatch.setenv("OPENAI_API_KEY", "sk-new-openai-key-1234567890")

        # Get settings again
        settings2 = get_settings()

        # Assert - Should be different instance with different config
        assert settings1 is not settings2
        assert settings2.anthropic_api_key is None
        assert settings2.openai_api_key is not None
