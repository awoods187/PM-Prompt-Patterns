# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
Tests for multi-provider prompt registry.

Tests prompt loading, provider selection, and variant management.
"""

from unittest.mock import patch

import pytest

from ai_models import PromptRegistry, get_prompt, list_prompts, list_variants


class TestPromptRegistry:
    """Test PromptRegistry functionality."""

    def test_list_prompts_returns_available_prompts(self):
        """Test that list_prompts returns available prompt directories."""
        prompts = PromptRegistry.list_prompts()

        assert isinstance(prompts, list)
        # Should include our signal-classification prompt
        assert any("signal-classification" in p for p in prompts)

    def test_list_variants_for_signal_classification(self):
        """Test that signal-classification has all provider variants."""
        variants = PromptRegistry.list_variants("analytics/signal-classification")

        assert "base" in variants
        assert "claude" in variants
        assert "openai" in variants
        assert "gemini" in variants

    def test_get_base_prompt(self):
        """Test loading base prompt without provider."""
        prompt = PromptRegistry.get_prompt("analytics/signal-classification")

        assert prompt is not None
        assert len(prompt) > 0
        assert "Customer Signal Classification" in prompt
        assert "FEATURE_REQUEST" in prompt

    def test_get_claude_variant(self):
        """Test loading Claude-specific variant."""
        prompt = PromptRegistry.get_prompt("analytics/signal-classification", provider="claude")

        assert prompt is not None
        assert "claude" in prompt.lower() or "<" in prompt  # XML tags
        assert "FEATURE_REQUEST" in prompt

    def test_get_openai_variant(self):
        """Test loading OpenAI-specific variant."""
        prompt = PromptRegistry.get_prompt("analytics/signal-classification", provider="openai")

        assert prompt is not None
        assert "openai" in prompt.lower() or "function" in prompt.lower()
        assert "FEATURE_REQUEST" in prompt

    def test_get_gemini_variant(self):
        """Test loading Gemini-specific variant."""
        prompt = PromptRegistry.get_prompt("analytics/signal-classification", provider="gemini")

        assert prompt is not None
        assert "gemini" in prompt.lower() or "context" in prompt.lower()
        assert "FEATURE_REQUEST" in prompt

    def test_auto_detect_provider_from_gpt_model(self):
        """Test auto-detection of OpenAI provider from GPT model name."""
        prompt = PromptRegistry.get_prompt("analytics/signal-classification", model="gpt-4o")

        assert prompt is not None
        # Should load OpenAI variant
        assert "openai" in prompt.lower() or "function" in prompt.lower()

    def test_auto_detect_provider_from_claude_model(self):
        """Test auto-detection of Claude provider from model name."""
        prompt = PromptRegistry.get_prompt(
            "analytics/signal-classification", model="claude-sonnet-4-5"
        )

        assert prompt is not None
        # Should load Claude variant
        assert "claude" in prompt.lower() or "<" in prompt

    def test_auto_detect_provider_from_gemini_model(self):
        """Test auto-detection of Gemini 2.5 Provider from model name."""
        prompt = PromptRegistry.get_prompt(
            "analytics/signal-classification", model="gemini-2-5-flash"
        )

        assert prompt is not None
        # Should load Gemini variant
        assert "gemini" in prompt.lower() or "context" in prompt.lower()

    def test_has_provider_variant_returns_true_for_existing(self):
        """Test checking if provider variant exists."""
        assert PromptRegistry.has_provider_variant("analytics/signal-classification", "claude")
        assert PromptRegistry.has_provider_variant("analytics/signal-classification", "openai")
        assert PromptRegistry.has_provider_variant("analytics/signal-classification", "gemini")

    def test_has_provider_variant_returns_false_for_nonexistent(self):
        """Test checking for non-existent provider variant."""
        assert not PromptRegistry.has_provider_variant(
            "analytics/signal-classification", "nonexistent"
        )

    def test_get_nonexistent_prompt_raises_error(self):
        """Test that requesting non-existent prompt raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            PromptRegistry.get_prompt("nonexistent-prompt")

    def test_provider_and_model_both_specified_raises_error(self):
        """Test that specifying both provider and model raises ValueError."""
        with pytest.raises(ValueError, match="Specify either provider or model"):
            PromptRegistry.get_prompt(
                "analytics/signal-classification", provider="claude", model="gpt-4o"
            )


class TestConvenienceFunctions:
    """Test convenience functions for prompt access."""

    def test_get_prompt_convenience_function(self):
        """Test get_prompt convenience function."""
        prompt = get_prompt("analytics/signal-classification", provider="openai")

        assert prompt is not None
        assert len(prompt) > 0

    def test_list_prompts_convenience_function(self):
        """Test list_prompts convenience function."""
        prompts = list_prompts()

        assert isinstance(prompts, list)
        assert any("signal-classification" in p for p in prompts)

    def test_list_variants_convenience_function(self):
        """Test list_variants convenience function."""
        variants = list_variants("analytics/signal-classification")

        assert "base" in variants
        assert "claude" in variants
        assert "openai" in variants
        assert "gemini" in variants


class TestProviderDetection:
    """Test provider auto-detection from model names."""

    @pytest.mark.parametrize(
        "model_name,expected_provider",
        [
            ("gpt-4o", "openai"),
            ("gpt-4o-mini", "openai"),
            ("gpt-4o", "openai"),
            ("claude-sonnet-4-5", "claude"),
            ("claude-haiku", "claude"),
            ("claude-opus", "claude"),
            ("gemini-2-5-pro", "gemini"),
            ("gemini-2-5-flash", "gemini"),
            ("gemini-flash-lite", "gemini"),
        ],
    )
    def test_provider_detection_from_model_name(self, model_name, expected_provider):
        """Test that provider is correctly detected from model name."""
        detected = PromptRegistry._detect_provider(model_name)
        assert detected == expected_provider

    def test_unknown_model_returns_none(self):
        """Test that unknown model name returns None."""
        detected = PromptRegistry._detect_provider("unknown-model-123")
        assert detected is None


class TestPromptContent:
    """Test that prompt content is valid and contains expected elements."""

    def test_base_prompt_contains_categories(self):
        """Test that base prompt contains all category definitions."""
        prompt = get_prompt("analytics/signal-classification")

        categories = [
            "FEATURE_REQUEST",
            "BUG_REPORT",
            "CHURN_RISK",
            "EXPANSION_SIGNAL",
            "GENERAL_FEEDBACK",
        ]

        for category in categories:
            assert category in prompt

    def test_claude_variant_contains_xml_tags(self):
        """Test that Claude variant uses XML structure."""
        prompt = get_prompt("analytics/signal-classification", provider="claude")

        # Should contain XML-style tags
        assert "<" in prompt and ">" in prompt
        # Should have category tags
        assert "category" in prompt.lower()

    def test_openai_variant_contains_function_definition(self):
        """Test that OpenAI variant includes function calling setup."""
        prompt = get_prompt("analytics/signal-classification", provider="openai")

        # Should mention function calling or JSON mode
        assert "function" in prompt.lower() or "json" in prompt.lower()
        # Should have schema information
        assert "properties" in prompt.lower() or "parameters" in prompt.lower()

    def test_gemini_variant_contains_json_schema(self):
        """Test that Gemini variant includes JSON schema."""
        prompt = get_prompt("analytics/signal-classification", provider="gemini")

        # Should mention JSON schema or response structure
        assert "json" in prompt.lower() or "schema" in prompt.lower()
        # Should mention context or caching features
        assert (
            "context" in prompt.lower() or "caching" in prompt.lower() or "cache" in prompt.lower()
        )


class TestPromptMetadata:
    """Test that prompts include proper metadata and documentation."""

    def test_all_variants_have_category_info(self):
        """Test that all variants include category information."""
        for provider in ["base", "claude", "openai", "gemini"]:
            if provider == "base":
                prompt = get_prompt("analytics/signal-classification")
            else:
                prompt = get_prompt("analytics/signal-classification", provider=provider)

            # Should describe what categories exist
            assert "FEATURE_REQUEST" in prompt
            assert "BUG_REPORT" in prompt

    def test_variants_include_examples(self):
        """Test that variants include usage examples."""
        for provider in ["base", "claude", "openai", "gemini"]:
            if provider == "base":
                prompt = get_prompt("analytics/signal-classification")
            else:
                prompt = get_prompt("analytics/signal-classification", provider=provider)

            # Should have some form of example or usage guidance
            assert "example" in prompt.lower() or "usage" in prompt.lower()


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_list_variants_for_nonexistent_prompt(self):
        """Test list_variants returns empty dict for non-existent prompt."""
        variants = PromptRegistry.list_variants("nonexistent-prompt")
        assert variants == {}

    def test_has_provider_variant_for_nonexistent_prompt(self):
        """Test has_provider_variant returns False for non-existent prompt."""
        assert not PromptRegistry.has_provider_variant("nonexistent-prompt", "claude")

    def test_resolve_prompt_path_with_md_extension(self):
        """Test that .md extension is stripped from prompt name."""
        # If someone accidentally includes .md, it should still work
        prompt = PromptRegistry.get_prompt("analytics/signal-classification.md")
        assert prompt is not None
        assert "FEATURE_REQUEST" in prompt

    def test_fallback_to_base_when_provider_variant_missing(self):
        """Test fallback to base prompt when provider variant doesn't exist."""
        # Request a provider that doesn't have a variant
        prompt = PromptRegistry.get_prompt(
            "analytics/signal-classification", provider="nonexistent-provider"
        )
        # Should fall back to base prompt
        assert prompt is not None
        assert "Customer Signal Classification" in prompt

    def test_auto_detect_with_unknown_model_uses_base(self):
        """Test that unknown model names fall back to base prompt."""
        prompt = PromptRegistry.get_prompt(
            "analytics/signal-classification", model="unknown-model-xyz"
        )
        # Should use base prompt since provider can't be detected
        assert prompt is not None
        assert "Customer Signal Classification" in prompt

    def test_list_prompts_is_sorted(self):
        """Test that list_prompts returns sorted list."""
        prompts = PromptRegistry.list_prompts()
        assert prompts == sorted(prompts)

    def test_get_prompt_with_provider_prefers_provider_variant(self):
        """Test that specifying provider loads provider variant, not base."""
        claude_prompt = PromptRegistry.get_prompt(
            "analytics/signal-classification", provider="claude"
        )
        base_prompt = PromptRegistry.get_prompt("analytics/signal-classification")

        # Claude variant should be different from base
        # (it has XML tags and chain-of-thought instructions)
        assert claude_prompt != base_prompt
        assert "<classification_task>" in claude_prompt

    def test_prompt_path_resolution_case_sensitivity(self):
        """Test that prompt path resolution works correctly."""
        # This tests the _resolve_prompt_path method
        path = PromptRegistry._resolve_prompt_path("analytics/signal-classification")
        assert path is not None
        assert path.exists()
        assert path.is_dir()

    def test_prompt_path_resolution_returns_none_for_invalid(self):
        """Test that invalid prompt path returns None."""
        path = PromptRegistry._resolve_prompt_path("invalid/nonexistent/path")
        assert path is None

    def test_error_when_directory_exists_but_no_prompt_files(self, tmp_path):
        """Test error when prompt directory exists but has no .md files."""
        # Create a temporary prompt directory structure
        test_prompts_dir = tmp_path / "prompts"
        test_prompts_dir.mkdir()
        test_dir = test_prompts_dir / "test-empty"
        test_dir.mkdir()

        # Create a non-prompt file to ensure directory isn't empty
        (test_dir / "README.txt").write_text("This is not a prompt file")

        # Temporarily override PROMPTS_DIR
        with patch.object(PromptRegistry, "PROMPTS_DIR", test_prompts_dir):
            with pytest.raises(FileNotFoundError, match="No prompt files found"):
                PromptRegistry.get_prompt("test-empty")

    def test_list_prompts_when_no_prompts_dir(self, tmp_path):
        """Test list_prompts returns empty list when PROMPTS_DIR doesn't exist."""
        non_existent_dir = tmp_path / "nonexistent"

        # Temporarily override PROMPTS_DIR to non-existent directory
        with patch.object(PromptRegistry, "PROMPTS_DIR", non_existent_dir):
            prompts = PromptRegistry.list_prompts()
            assert prompts == []
