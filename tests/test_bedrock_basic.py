"""
Basic tests for Bedrock provider (without AWS credentials).

Tests initialization validation and error handling.
"""

import pytest

# Skip all tests in this module if boto3 is not installed
boto3 = pytest.importorskip("boto3", reason="boto3 not installed")

from pm_prompt_toolkit.providers.bedrock import (  # noqa: E402
    BEDROCK_MODEL_IDS,
    BedrockProvider,
)


class TestBedrockInitialization:
    """Test Bedrock provider initialization without credentials."""

    def test_init_with_invalid_model_raises_error(self):
        """Test that invalid model raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported Bedrock model"):
            BedrockProvider(model="invalid-model")

    def test_model_id_mapping_exists(self):
        """Test that model ID mapping is defined."""
        assert isinstance(BEDROCK_MODEL_IDS, dict)
        assert len(BEDROCK_MODEL_IDS) > 0
        assert "claude-sonnet-4-5" in BEDROCK_MODEL_IDS

    def test_model_id_values_are_strings(self):
        """Test that model IDs are properly formatted strings."""
        for model_name, model_id in BEDROCK_MODEL_IDS.items():
            assert isinstance(model_name, str)
            assert isinstance(model_id, str)
            assert len(model_id) > 0
