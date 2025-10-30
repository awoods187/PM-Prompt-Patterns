"""
Basic tests for Bedrock provider (without AWS credentials).

Tests initialization validation and error handling.
"""

import pytest
from pm_prompt_toolkit.providers.bedrock import BedrockProvider


class TestBedrockInitialization:
    """Test Bedrock provider initialization without credentials."""

    def test_init_with_invalid_model_raises_error(self):
        """Test that invalid model raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported Bedrock model"):
            BedrockProvider(model="invalid-model")

    def test_model_id_mapping_exists(self):
        """Test that model ID mapping is defined."""
        from pm_prompt_toolkit.providers.bedrock import BEDROCK_MODEL_IDS
        
        assert isinstance(BEDROCK_MODEL_IDS, dict)
        assert len(BEDROCK_MODEL_IDS) > 0
        assert "claude-sonnet-4-5" in BEDROCK_MODEL_IDS

    def test_model_id_values_are_strings(self):
        """Test that model IDs are properly formatted strings."""
        from pm_prompt_toolkit.providers.bedrock import BEDROCK_MODEL_IDS
        
        for model_name, model_id in BEDROCK_MODEL_IDS.items():
            assert isinstance(model_name, str)
            assert isinstance(model_id, str)
            assert len(model_id) > 0
