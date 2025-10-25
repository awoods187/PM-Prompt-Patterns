# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
Test Model Endpoint Accessibility

Verifies that all models in the ModelRegistry have working API endpoints.
This requires API keys to be set in environment variables.

Environment Variables Required:
    ANTHROPIC_API_KEY - For Claude models
    OPENAI_API_KEY - For GPT models
    GOOGLE_API_KEY - For Gemini models

Usage:
    # Run all endpoint tests (requires all API keys)
    pytest tests/test_model_endpoints.py

    # Run only Anthropic tests
    pytest tests/test_model_endpoints.py -k anthropic

    # Skip endpoint tests (when API keys not available)
    pytest tests/test_model_endpoints.py -m "not endpoint"
"""

import os

import pytest

from models.registry import ModelRegistry

# Skip all tests in this file if no API keys present
pytestmark = pytest.mark.skipif(
    not any(
        [
            os.getenv("ANTHROPIC_API_KEY"),
            os.getenv("OPENAI_API_KEY"),
            os.getenv("GOOGLE_API_KEY"),
        ]
    ),
    reason="No API keys found - skipping endpoint tests",
)


class TestAnthropicEndpoints:
    """Test Anthropic Claude model endpoints."""

    @pytest.fixture(autouse=True)
    def check_api_key(self):
        """Skip Anthropic tests if API key not present."""
        if not os.getenv("ANTHROPIC_API_KEY"):
            pytest.skip("ANTHROPIC_API_KEY not set")

    def test_claude_sonnet_endpoint(self):
        """Verify Claude Sonnet 4.5 endpoint is accessible."""
        try:
            import anthropic
        except ImportError:
            pytest.skip("anthropic package not installed")

        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        model = ModelRegistry.CLAUDE_SONNET_4_5

        response = client.messages.create(
            model=model.api_identifier,
            max_tokens=10,
            messages=[{"role": "user", "content": "test"}],
        )

        assert response.content, "Empty response from Claude Sonnet"
        assert (
            response.model == model.api_identifier
        ), f"Expected {model.api_identifier}, got {response.model}"

    def test_claude_haiku_endpoint(self):
        """Verify Claude Haiku 4.5 endpoint is accessible."""
        try:
            import anthropic
        except ImportError:
            pytest.skip("anthropic package not installed")

        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        model = ModelRegistry.CLAUDE_HAIKU_4_5

        response = client.messages.create(
            model=model.api_identifier,
            max_tokens=10,
            messages=[{"role": "user", "content": "test"}],
        )

        assert response.content, "Empty response from Claude Haiku"
        assert response.model == model.api_identifier

    def test_claude_opus_endpoint(self):
        """Verify Claude Opus 4.1 endpoint is accessible."""
        try:
            import anthropic
        except ImportError:
            pytest.skip("anthropic package not installed")

        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        model = ModelRegistry.CLAUDE_OPUS_4_1

        response = client.messages.create(
            model=model.api_identifier,
            max_tokens=10,
            messages=[{"role": "user", "content": "test"}],
        )

        assert response.content, "Empty response from Claude Opus"
        assert response.model == model.api_identifier

    def test_prompt_caching_available(self):
        """Verify prompt caching feature is available for Claude."""
        try:
            import anthropic
        except ImportError:
            pytest.skip("anthropic package not installed")

        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        model = ModelRegistry.CLAUDE_SONNET_4_5

        # Test with cache_control
        response = client.messages.create(
            model=model.api_identifier,
            max_tokens=10,
            system=[
                {
                    "type": "text",
                    "text": "Test system prompt",
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": "test"}],
        )

        assert response.content, "Prompt caching request failed"


class TestOpenAIEndpoints:
    """Test OpenAI GPT model endpoints."""

    @pytest.fixture(autouse=True)
    def check_api_key(self):
        """Skip OpenAI tests if API key not present."""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")

    def test_gpt_4o_endpoint(self):
        """Verify GPT-4o endpoint is accessible."""
        try:
            import openai
        except ImportError:
            pytest.skip("openai package not installed")

        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        model = ModelRegistry.GPT_4O

        response = client.chat.completions.create(
            model=model.api_identifier,
            max_tokens=10,
            messages=[{"role": "user", "content": "test"}],
        )

        assert response.choices, "Empty response from GPT-4o"
        assert response.choices[0].message.content, "No content in GPT-4o response"

    def test_gpt_4o_mini_endpoint(self):
        """Verify GPT-4o mini endpoint is accessible."""
        try:
            import openai
        except ImportError:
            pytest.skip("openai package not installed")

        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        model = ModelRegistry.GPT_4O_MINI

        response = client.chat.completions.create(
            model=model.api_identifier,
            max_tokens=10,
            messages=[{"role": "user", "content": "test"}],
        )

        assert response.choices, "Empty response from GPT-4o mini"
        assert response.choices[0].message.content

    def test_gpt_4o_vision(self):
        """Verify GPT-4o vision capability is working."""
        try:
            import openai
        except ImportError:
            pytest.skip("openai package not installed")

        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        model = ModelRegistry.GPT_4O

        # Test with a simple data URL (1x1 red pixel)
        data_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="

        response = client.chat.completions.create(
            model=model.api_identifier,
            max_tokens=20,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What color is this pixel?"},
                        {"type": "image_url", "image_url": {"url": data_url}},
                    ],
                }
            ],
        )

        assert response.choices, "Vision request failed"
        assert response.choices[0].message.content, "No vision response"


class TestGoogleGeminiEndpoints:
    """Test Google Gemini model endpoints."""

    @pytest.fixture(autouse=True)
    def check_api_key(self):
        """Skip Gemini tests if API key not present."""
        if not os.getenv("GOOGLE_API_KEY"):
            pytest.skip("GOOGLE_API_KEY not set")

    def test_gemini_2_5_pro_endpoint(self):
        """Verify Gemini 2.5 Pro endpoint is accessible."""
        try:
            import google.generativeai as genai
        except ImportError:
            pytest.skip("google-generativeai package not installed")

        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model_spec = ModelRegistry.GEMINI_2_5_PRO
        model = genai.GenerativeModel(model_spec.api_identifier)

        response = model.generate_content("test")

        assert response.text, "Empty response from Gemini 2.5 Pro"

    def test_gemini_2_5_flash_endpoint(self):
        """Verify Gemini 2.5 Flash endpoint is accessible."""
        try:
            import google.generativeai as genai
        except ImportError:
            pytest.skip("google-generativeai package not installed")

        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model_spec = ModelRegistry.GEMINI_2_5_FLASH
        model = genai.GenerativeModel(model_spec.api_identifier)

        response = model.generate_content("test")

        assert response.text, "Empty response from Gemini 2.5 Flash"

    def test_gemini_2_5_flash_lite_endpoint(self):
        """Verify Gemini 2.5 Flash-Lite endpoint is accessible."""
        try:
            import google.generativeai as genai
        except ImportError:
            pytest.skip("google-generativeai package not installed")

        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model_spec = ModelRegistry.GEMINI_2_5_FLASH_LITE
        model = genai.GenerativeModel(model_spec.api_identifier)

        response = model.generate_content("test")

        assert response.text, "Empty response from Gemini 2.5 Flash-Lite"

    def test_gemini_context_window(self):
        """Verify Gemini can handle large context (1M tokens claim)."""
        try:
            import google.generativeai as genai
        except ImportError:
            pytest.skip("google-generativeai package not installed")

        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model_spec = ModelRegistry.GEMINI_2_5_FLASH
        model = genai.GenerativeModel(model_spec.api_identifier)

        # Test with ~10K tokens (full 1M test would be expensive)
        large_text = "word " * 10000
        response = model.generate_content(f"{large_text}\nCount words.")

        assert response.text, "Failed with large context"


class TestContextWindowLimits:
    """Test that declared context windows are accurate."""

    def test_context_windows_declared(self):
        """Verify all models have context windows declared."""
        for key, spec in ModelRegistry.get_all_current_models().items():
            assert spec.context_window_input > 0, f"{key} has no input context window declared"

    def test_context_window_reasonable(self):
        """Verify context windows are within reasonable ranges."""
        for key, spec in ModelRegistry.get_all_current_models().items():
            assert (
                spec.context_window_input >= 8_000
            ), f"{key} context window too small: {spec.context_window_input}"
            assert (
                spec.context_window_input <= 2_000_000
            ), f"{key} context window unreasonably large: {spec.context_window_input}"


class TestPricingAccuracy:
    """Test that pricing information is present and reasonable."""

    def test_pricing_declared(self):
        """Verify all models have pricing declared."""
        for key, spec in ModelRegistry.get_all_current_models().items():
            assert spec.input_price_per_1m > 0, f"{key} has no input price declared"
            assert spec.output_price_per_1m > 0, f"{key} has no output price declared"

    def test_pricing_reasonable(self):
        """Verify pricing is within reasonable ranges."""
        for key, spec in ModelRegistry.get_all_current_models().items():
            # Input price should be $0.01 to $20 per 1M tokens
            assert (
                0.01 <= spec.input_price_per_1m <= 20
            ), f"{key} input price unreasonable: ${spec.input_price_per_1m}"

            # Output price typically 2-10x input
            assert (
                0.01 <= spec.output_price_per_1m <= 100
            ), f"{key} output price unreasonable: ${spec.output_price_per_1m}"

    def test_output_more_expensive_than_input(self):
        """Verify output tokens cost >= input tokens (industry standard)."""
        for key, spec in ModelRegistry.get_all_current_models().items():
            assert (
                spec.output_price_per_1m >= spec.input_price_per_1m
            ), f"{key} output cheaper than input (unusual)"


class TestModelMetadata:
    """Test model metadata completeness."""

    def test_all_models_have_docs_url(self):
        """Verify all models link to official documentation."""
        for key, spec in ModelRegistry.get_all_current_models().items():
            assert spec.docs_url, f"{key} has no docs_url"
            assert spec.docs_url.startswith(
                "http"
            ), f"{key} docs_url not a valid URL: {spec.docs_url}"

    def test_all_models_recently_verified(self):
        """Verify all models were verified recently (within 90 days)."""
        from datetime import date, timedelta

        stale_threshold = date.today() - timedelta(days=90)

        stale_models = []
        for key, spec in ModelRegistry.get_all_current_models().items():
            if spec.last_verified < stale_threshold:
                days_old = (date.today() - spec.last_verified).days
                stale_models.append((key, days_old))

        if stale_models:
            warnings = "\n".join(
                f"  - {key}: {days} days since verification" for key, days in stale_models
            )
            pytest.fail(
                f"Models not verified in 90+ days:\n{warnings}\n\n"
                f"Update: See UPDATING_MODELS.md for verification procedure"
            )

    def test_all_models_have_knowledge_cutoff(self):
        """Verify all models declare knowledge cutoff."""
        for key, spec in ModelRegistry.get_all_current_models().items():
            assert spec.knowledge_cutoff, f"{key} has no knowledge_cutoff declared"


if __name__ == "__main__":
    """Run tests with verbose output."""
    pytest.main([__file__, "-v", "--tb=short"])
