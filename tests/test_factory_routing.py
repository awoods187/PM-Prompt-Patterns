"""
Tests for module: pm_prompt_toolkit/providers/factory.py

Coverage Target: 85%
Current Coverage: 41.28%
Priority: COMPLEX

The factory router implements three-tier routing logic (explicit prefix → enabled providers → fallback).
Tests focus on routing correctness, provider selection, configuration validation, and edge cases.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from pm_prompt_toolkit.providers.factory import (
    get_provider,
    _get_provider_by_prefix,
    ConfigurationError,
)
from pm_prompt_toolkit.providers.base import LLMProvider
from pm_prompt_toolkit.providers.claude import ClaudeProvider
from pm_prompt_toolkit.providers.bedrock import BedrockProvider
from pm_prompt_toolkit.providers.vertex import VertexProvider
from pm_prompt_toolkit.providers.mock import MockProvider
from pm_prompt_toolkit.providers.openai import OpenAIProvider
from pm_prompt_toolkit.providers.gemini import GeminiProvider


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_settings_default():
    """Provide settings with all providers disabled (default state)."""
    settings = Mock()
    settings.enable_bedrock = False
    settings.enable_vertex = False
    settings.enable_openai = False
    return settings


@pytest.fixture
def mock_settings_bedrock_enabled():
    """Provide settings with Bedrock enabled."""
    settings = Mock()
    settings.enable_bedrock = True
    settings.enable_vertex = False
    settings.enable_openai = False
    # Mock AWS credentials
    settings.aws_access_key_id = "AKIA..."
    settings.aws_secret_access_key = "secret"
    settings.aws_region = "us-east-1"
    return settings


@pytest.fixture
def mock_settings_vertex_enabled():
    """Provide settings with Vertex enabled."""
    settings = Mock()
    settings.enable_bedrock = False
    settings.enable_vertex = True
    settings.enable_openai = False
    # Mock GCP credentials
    settings.gcp_project_id = "test-project"
    settings.gcp_region = "us-central1"
    settings.gcp_credentials_path = None
    return settings


@pytest.fixture
def mock_settings_all_enabled():
    """Provide settings with all providers enabled."""
    settings = Mock()
    settings.enable_bedrock = True
    settings.enable_vertex = True
    settings.enable_openai = True
    # Mock credentials
    settings.aws_access_key_id = "AKIA..."
    settings.aws_secret_access_key = "secret"
    settings.aws_region = "us-east-1"
    settings.gcp_project_id = "test-project"
    settings.gcp_region = "us-central1"
    settings.gcp_credentials_path = None
    settings.openai_api_key = "sk-..."
    return settings


# ============================================================================
# TIER 1: EXPLICIT PREFIX ROUTING TESTS
# ============================================================================

class TestExplicitPrefixRouting:
    """Test suite for explicit provider prefix routing (Tier 1)."""

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    @patch('pm_prompt_toolkit.providers.factory.MockProvider')
    def test_mock_prefix_routes_to_mock_provider(self, mock_provider_class, mock_get_settings):
        """Test that 'mock:' prefix routes to MockProvider."""
        # Arrange
        mock_get_settings.return_value = Mock(enable_bedrock=False)
        mock_provider_class.return_value = Mock(spec=MockProvider)

        # Act
        result = get_provider("mock:claude-sonnet")

        # Assert
        mock_provider_class.assert_called_once_with(model="claude-sonnet", enable_caching=True)

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    @patch('pm_prompt_toolkit.providers.factory.BedrockProvider')
    def test_bedrock_prefix_with_enabled_routes_to_bedrock(self, mock_bedrock, mock_get_settings):
        """Test that 'bedrock:' prefix routes to BedrockProvider when enabled."""
        # Arrange
        mock_settings = Mock()
        mock_settings.enable_bedrock = True
        mock_get_settings.return_value = mock_settings
        mock_bedrock.return_value = Mock(spec=BedrockProvider)

        # Act
        result = get_provider("bedrock:claude-sonnet-4-5")

        # Assert
        mock_bedrock.assert_called_once_with(model="claude-sonnet-4-5", enable_caching=True)

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    def test_bedrock_prefix_with_disabled_raises_configuration_error(self, mock_get_settings):
        """Test that 'bedrock:' prefix with disabled provider raises ConfigurationError."""
        # Arrange
        mock_settings = Mock()
        mock_settings.enable_bedrock = False
        mock_get_settings.return_value = mock_settings

        # Act & Assert
        with pytest.raises(ConfigurationError, match="enable_bedrock=False"):
            get_provider("bedrock:claude-sonnet")

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    @patch('pm_prompt_toolkit.providers.factory.VertexProvider')
    def test_vertex_prefix_with_enabled_routes_to_vertex(self, mock_vertex, mock_get_settings):
        """Test that 'vertex:' prefix routes to VertexProvider when enabled."""
        # Arrange
        mock_settings = Mock()
        mock_settings.enable_vertex = True
        mock_get_settings.return_value = mock_settings
        mock_vertex.return_value = Mock(spec=VertexProvider)

        # Act
        result = get_provider("vertex:claude-opus-4")

        # Assert
        mock_vertex.assert_called_once_with(model="claude-opus-4", enable_caching=True)

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    def test_vertex_prefix_with_disabled_raises_configuration_error(self, mock_get_settings):
        """Test that 'vertex:' prefix with disabled provider raises ConfigurationError."""
        # Arrange
        mock_settings = Mock()
        mock_settings.enable_vertex = False
        mock_get_settings.return_value = mock_settings

        # Act & Assert
        with pytest.raises(ConfigurationError, match="enable_vertex=False"):
            get_provider("vertex:claude-haiku")

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    @patch('pm_prompt_toolkit.providers.factory.ClaudeProvider')
    def test_anthropic_prefix_routes_to_claude_provider(self, mock_claude, mock_get_settings):
        """Test that 'anthropic:' prefix routes to ClaudeProvider."""
        # Arrange
        mock_get_settings.return_value = Mock()
        mock_claude.return_value = Mock(spec=ClaudeProvider)

        # Act
        result = get_provider("anthropic:claude-sonnet")

        # Assert
        mock_claude.assert_called_once_with(model="claude-sonnet", enable_caching=True)

    @pytest.mark.parametrize("invalid_prefix", [
        "unknown:claude-sonnet",
        "aws:claude-sonnet",
        "gcp:claude-sonnet",
        "invalid:model",
    ])
    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    def test_unknown_prefix_raises_value_error(self, mock_get_settings, invalid_prefix):
        """Test that unknown prefixes raise ValueError."""
        # Arrange
        mock_get_settings.return_value = Mock()

        # Act & Assert
        with pytest.raises(ValueError, match="Unknown provider prefix"):
            get_provider(invalid_prefix)


# ============================================================================
# TIER 2: ENABLED PROVIDERS ROUTING TESTS
# ============================================================================

class TestEnabledProvidersRouting:
    """Test suite for enabled providers routing (Tier 2)."""

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    @patch('pm_prompt_toolkit.providers.factory.BedrockProvider')
    def test_claude_model_with_bedrock_enabled_routes_to_bedrock(self, mock_bedrock, mock_get_settings):
        """Test that Claude models route to Bedrock when enabled."""
        # Arrange
        mock_settings = Mock()
        mock_settings.enable_bedrock = True
        mock_settings.enable_vertex = False
        mock_get_settings.return_value = mock_settings
        mock_bedrock.return_value = Mock(spec=BedrockProvider)

        # Act
        result = get_provider("claude-sonnet-4-5")

        # Assert
        mock_bedrock.assert_called_once()
        assert "claude-sonnet-4-5" in str(mock_bedrock.call_args)

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    @patch('pm_prompt_toolkit.providers.factory.VertexProvider')
    def test_claude_model_with_vertex_enabled_routes_to_vertex(self, mock_vertex, mock_get_settings):
        """Test that Claude models route to Vertex when enabled (and Bedrock disabled)."""
        # Arrange
        mock_settings = Mock()
        mock_settings.enable_bedrock = False
        mock_settings.enable_vertex = True
        mock_get_settings.return_value = mock_settings
        mock_vertex.return_value = Mock(spec=VertexProvider)

        # Act
        result = get_provider("claude-haiku")

        # Assert
        mock_vertex.assert_called_once()

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    @patch('pm_prompt_toolkit.providers.factory.BedrockProvider')
    @patch('pm_prompt_toolkit.providers.factory.VertexProvider')
    def test_bedrock_takes_precedence_over_vertex_when_both_enabled(
        self, mock_vertex, mock_bedrock, mock_get_settings
    ):
        """Test that Bedrock has higher priority than Vertex when both enabled."""
        # Arrange
        mock_settings = Mock()
        mock_settings.enable_bedrock = True
        mock_settings.enable_vertex = True
        mock_get_settings.return_value = mock_settings
        mock_bedrock.return_value = Mock(spec=BedrockProvider)

        # Act
        result = get_provider("claude-sonnet")

        # Assert
        mock_bedrock.assert_called_once()
        mock_vertex.assert_not_called()  # Vertex should not be called

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    @patch('pm_prompt_toolkit.providers.factory.BedrockProvider')
    @patch('pm_prompt_toolkit.providers.factory.VertexProvider')
    @patch('pm_prompt_toolkit.providers.factory.ClaudeProvider')
    def test_fallback_to_vertex_when_bedrock_fails(
        self, mock_claude, mock_vertex, mock_bedrock, mock_get_settings
    ):
        """Test that routing falls back to Vertex if Bedrock initialization fails."""
        # Arrange
        mock_settings = Mock()
        mock_settings.enable_bedrock = True
        mock_settings.enable_vertex = True
        mock_get_settings.return_value = mock_settings
        mock_bedrock.side_effect = Exception("Bedrock initialization failed")
        mock_vertex.return_value = Mock(spec=VertexProvider)

        # Act
        result = get_provider("claude-sonnet")

        # Assert
        mock_bedrock.assert_called_once()
        mock_vertex.assert_called_once()


    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    @patch('pm_prompt_toolkit.providers.factory.BedrockProvider')
    @patch('pm_prompt_toolkit.providers.factory.VertexProvider')
    @patch('pm_prompt_toolkit.providers.factory.ClaudeProvider')
    def test_fallback_to_anthropic_when_all_cloud_providers_fail(
        self, mock_claude, mock_vertex, mock_bedrock, mock_get_settings
    ):
        """Test final fallback to direct Anthropic API when all cloud providers fail."""
        # Arrange
        mock_settings = Mock()
        mock_settings.enable_bedrock = True
        mock_settings.enable_vertex = True
        mock_get_settings.return_value = mock_settings
        mock_bedrock.side_effect = Exception("Bedrock failed")
        mock_vertex.side_effect = Exception("Vertex failed")
        mock_claude.return_value = Mock(spec=ClaudeProvider)

        # Act
        result = get_provider("claude-sonnet")

        # Assert
        mock_bedrock.assert_called_once()
        mock_vertex.assert_called_once()
        mock_claude.assert_called_once()


# ============================================================================
# TIER 3: FALLBACK ROUTING TESTS
# ============================================================================

class TestFallbackRouting:
    """Test suite for fallback routing (Tier 3)."""

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    @patch('pm_prompt_toolkit.providers.factory.ClaudeProvider')
    def test_claude_model_with_no_providers_enabled_uses_anthropic(
        self, mock_claude, mock_get_settings
    ):
        """Test that Claude models use direct Anthropic API when no providers enabled."""
        # Arrange
        mock_settings = Mock()
        mock_settings.enable_bedrock = False
        mock_settings.enable_vertex = False
        mock_get_settings.return_value = mock_settings
        mock_claude.return_value = Mock(spec=ClaudeProvider)

        # Act
        result = get_provider("claude-opus")

        # Assert
        mock_claude.assert_called_once_with(model="claude-opus", enable_caching=True)

    @pytest.mark.parametrize("claude_model", [
        "claude-sonnet-4-5",
        "claude-sonnet-4",
        "claude-opus-4-1",
        "claude-opus-4",
        "claude-sonnet",
        "claude-haiku",
        "claude-opus",
    ])
    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    @patch('pm_prompt_toolkit.providers.factory.ClaudeProvider')
    def test_all_claude_models_route_correctly(self, mock_claude, mock_get_settings, claude_model):
        """Test that all Claude model names route to ClaudeProvider."""
        # Arrange
        mock_settings = Mock()
        mock_settings.enable_bedrock = False
        mock_settings.enable_vertex = False
        mock_get_settings.return_value = mock_settings
        mock_claude.return_value = Mock(spec=ClaudeProvider)

        # Act
        result = get_provider(claude_model)

        # Assert
        mock_claude.assert_called_once()


# ============================================================================
# MODEL NAME NORMALIZATION TESTS
# ============================================================================

class TestModelNameNormalization:
    """Test suite for model name case normalization."""

    @pytest.mark.parametrize("model_variant", [
        "CLAUDE-SONNET",
        "Claude-Sonnet",
        "claude-SONNET",
        "ClAuDe-SoNnEt",
    ])
    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    @patch('pm_prompt_toolkit.providers.factory.ClaudeProvider')
    def test_model_names_normalized_to_lowercase(self, mock_claude, mock_get_settings, model_variant):
        """Test that model names are normalized to lowercase."""
        # Arrange
        mock_settings = Mock()
        mock_settings.enable_bedrock = False
        mock_settings.enable_vertex = False
        mock_settings.enable_openai = False
        mock_get_settings.return_value = mock_settings
        mock_claude.return_value = Mock(spec=ClaudeProvider)

        # Act
        result = get_provider(model_variant)

        # Assert
        # Verify that the model was normalized to lowercase
        call_args = mock_claude.call_args
        assert call_args.kwargs['model'] == "claude-sonnet"

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    @patch('pm_prompt_toolkit.providers.factory.MockProvider')
    def test_explicit_prefix_normalizes_model_name(self, mock_provider, mock_get_settings):
        """Test that explicit prefix also normalizes model names."""
        # Arrange
        mock_get_settings.return_value = Mock()
        mock_provider.return_value = Mock(spec=MockProvider)

        # Act
        result = get_provider("mock:CLAUDE-SONNET")

        # Assert
        call_args = mock_provider.call_args
        assert call_args.kwargs['model'] == "claude-sonnet"


# ============================================================================
# OPENAI ROUTING TESTS
# ============================================================================

class TestOpenAIRouting:
    """Test suite for OpenAI model routing."""

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    def test_gpt4_with_openai_disabled_raises_not_implemented(self, mock_get_settings):
        """Test that GPT-4 with OpenAI disabled raises NotImplementedError."""
        # Arrange
        mock_settings = Mock()
        mock_settings.enable_openai = False
        mock_get_settings.return_value = mock_settings

        # Act & Assert
        with pytest.raises(NotImplementedError, match="OpenAI provider"):
            get_provider("gpt-4")

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    def test_gpt4_with_openai_enabled_routes_to_openai(self, mock_get_settings):
        """Test that GPT-4 routes to OpenAI when enabled (raises NotImplementedError)."""
        # Arrange
        mock_settings = Mock()
        mock_settings.enable_openai = True
        mock_get_settings.return_value = mock_settings

        # Act & Assert - OpenAIProvider __init__ will raise NotImplementedError
        with pytest.raises(NotImplementedError, match="OpenAI provider not yet implemented"):
            get_provider("gpt-4")

    @pytest.mark.parametrize("model", [
        "gpt-4",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-3.5",
        "GPT-4",  # Case insensitive
    ])
    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    def test_openai_models_detected(self, mock_get_settings, model):
        """Test that various OpenAI model names are detected."""
        # Arrange
        mock_settings = Mock()
        mock_settings.enable_openai = False
        mock_get_settings.return_value = mock_settings

        # Act & Assert
        with pytest.raises(NotImplementedError, match="OpenAI provider"):
            get_provider(model)


# ============================================================================
# GEMINI ROUTING TESTS
# ============================================================================

class TestGeminiRouting:
    """Test suite for Gemini model routing."""

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    @patch('pm_prompt_toolkit.providers.factory.GeminiProvider')
    def test_gemini_pro_routes_to_gemini_provider(self, mock_gemini, mock_get_settings):
        """Test that Gemini Pro routes to GeminiProvider."""
        # Arrange
        mock_get_settings.return_value = Mock()
        # GeminiProvider raises NotImplementedError in __init__
        mock_gemini.side_effect = NotImplementedError("Gemini provider not yet implemented")

        # Act & Assert
        with pytest.raises(NotImplementedError):
            get_provider("gemini-pro")

    @pytest.mark.parametrize("model", [
        "gemini-pro",
        "gemini-flash",
        "gemini-1.5",
        "GEMINI-PRO",  # Case insensitive
    ])
    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    @patch('pm_prompt_toolkit.providers.factory.GeminiProvider')
    def test_gemini_models_detected(self, mock_gemini, mock_get_settings, model):
        """Test that various Gemini model names are detected."""
        # Arrange
        mock_get_settings.return_value = Mock()
        mock_gemini.side_effect = NotImplementedError()

        # Act & Assert
        with pytest.raises(NotImplementedError):
            get_provider(model)


# ============================================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================================

class TestEdgeCases:
    """Test suite for edge cases and error handling."""

    @pytest.mark.parametrize("empty_model", [
        "",
        "   ",
        "\n",
        "\t",
    ])
    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    def test_empty_model_name_raises_value_error(self, mock_get_settings, empty_model):
        """Test that empty or whitespace model names raise ValueError."""
        # Arrange
        mock_get_settings.return_value = Mock()

        # Act & Assert
        with pytest.raises(ValueError, match="Unknown model"):
            get_provider(empty_model)

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    def test_unknown_model_raises_value_error(self, mock_get_settings):
        """Test that unknown model names raise ValueError with helpful message."""
        # Arrange
        mock_get_settings.return_value = Mock()

        # Act & Assert
        with pytest.raises(ValueError, match="Unknown model.*Supported models"):
            get_provider("totally-unknown-model")

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    @patch('pm_prompt_toolkit.providers.factory.ClaudeProvider')
    def test_caching_parameter_passed_through(self, mock_claude, mock_get_settings):
        """Test that enable_caching parameter is passed to provider."""
        # Arrange
        mock_settings = Mock()
        mock_settings.enable_bedrock = False
        mock_settings.enable_vertex = False
        mock_settings.enable_openai = False
        mock_get_settings.return_value = mock_settings
        mock_claude.return_value = Mock(spec=ClaudeProvider)

        # Act
        result = get_provider("claude-sonnet", enable_caching=False)

        # Assert
        mock_claude.assert_called_once_with(model="claude-sonnet", enable_caching=False)

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    def test_model_with_colon_but_empty_prefix_handled(self, mock_get_settings):
        """Test that model names with colon but empty prefix are handled."""
        # Arrange
        mock_get_settings.return_value = Mock()

        # Act & Assert
        with pytest.raises((ValueError, NotImplementedError)):
            get_provider(":claude-sonnet")


# ============================================================================
# PROVIDER PREFIX HELPER FUNCTION TESTS
# ============================================================================

class TestGetProviderByPrefix:
    """Test suite for _get_provider_by_prefix helper function."""

    @patch('pm_prompt_toolkit.providers.factory.MockProvider')
    def test_get_provider_by_prefix_mock_always_available(self, mock_provider):
        """Test that mock provider is always available regardless of settings."""
        # Arrange
        settings = Mock()
        settings.enable_bedrock = False
        settings.enable_vertex = False
        mock_provider.return_value = Mock(spec=MockProvider)

        # Act
        result = _get_provider_by_prefix("mock", "claude-sonnet", True, settings)

        # Assert
        mock_provider.assert_called_once()

    @patch('pm_prompt_toolkit.providers.factory.BedrockProvider')
    def test_get_provider_by_prefix_bedrock_with_enabled(self, mock_bedrock):
        """Test bedrock prefix routing with enabled setting."""
        # Arrange
        settings = Mock()
        settings.enable_bedrock = True
        mock_bedrock.return_value = Mock(spec=BedrockProvider)

        # Act
        result = _get_provider_by_prefix("bedrock", "claude-sonnet", True, settings)

        # Assert
        mock_bedrock.assert_called_once()

    def test_get_provider_by_prefix_bedrock_with_disabled_raises_error(self):
        """Test bedrock prefix with disabled setting raises ConfigurationError."""
        # Arrange
        settings = Mock()
        settings.enable_bedrock = False

        # Act & Assert
        with pytest.raises(ConfigurationError, match="enable_bedrock=False"):
            _get_provider_by_prefix("bedrock", "claude-sonnet", True, settings)

    @pytest.mark.parametrize("prefix,expected_error", [
        ("unknown", ValueError),
        ("invalid", ValueError),
        ("test", ValueError),
    ])
    def test_get_provider_by_prefix_unknown_raises_value_error(self, prefix, expected_error):
        """Test that unknown prefixes raise ValueError."""
        # Arrange
        settings = Mock()

        # Act & Assert
        with pytest.raises(expected_error, match="Unknown provider prefix"):
            _get_provider_by_prefix(prefix, "model", True, settings)


# ============================================================================
# ADDITIONAL COVERAGE TESTS
# ============================================================================

class TestAdditionalCoverage:
    """Tests to cover remaining factory.py lines."""

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    def test_openai_prefix_with_enabled_logs_message(self, mock_get_settings, caplog):
        """Test that OpenAI prefix with enabled provider logs info message."""
        # Arrange
        import logging
        mock_settings = Mock()
        mock_settings.enable_openai = True
        mock_get_settings.return_value = mock_settings

        # Act
        with caplog.at_level(logging.INFO):
            try:
                get_provider("openai:gpt-4")
            except NotImplementedError:
                pass  # Expected - OpenAI not implemented

        # Assert
        assert "Using OpenAI provider" in caplog.text
        assert "explicit prefix" in caplog.text

    @patch('pm_prompt_toolkit.providers.factory.get_settings')
    def test_gemini_prefix_logs_message(self, mock_get_settings, caplog):
        """Test that Gemini prefix logs info message."""
        # Arrange
        import logging
        mock_settings = Mock()
        mock_get_settings.return_value = mock_settings

        # Act
        with caplog.at_level(logging.INFO):
            try:
                get_provider("gemini:gemini-pro")
            except NotImplementedError:
                pass  # Expected - Gemini not implemented

        # Assert
        assert "Using Gemini provider" in caplog.text
        assert "explicit prefix" in caplog.text
