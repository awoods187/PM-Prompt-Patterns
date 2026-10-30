# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Google Gemini model fetcher."""

import os
from typing import Any, Optional

from scripts.model_updater.fetchers.base_fetcher import BaseFetcher, ModelData

DOCS_URL = "https://ai.google.dev/gemini-api/docs/models"

# Static specs mirror ai_models/definitions/google/*.yaml (last verified 2026-10-30).
# Keep them in sync: tests/test_model_updater/test_static_specs_match_definitions.py
# fails if a YAML and this table disagree.
_STATIC_SPECS: dict[str, dict[str, Any]] = {
    "gemini-4-argon": {
        "name": "Gemini 4 Argon",
        "api_identifier": "gemini-4-argon",
        "context_window_input": 1048576,
        "context_window_output": 65536,
        "knowledge_cutoff": "Not published",
        "release_date": "2026-10-13",
        "capabilities": [
            "text_input",
            "text_output",
            "function_calling",
            "vision",
            "large_context",
            "prompt_caching",
            "streaming",
            "json_mode",
            "code_execution",
            "search",
        ],
        "pricing": {
            "input_per_1m": 2.0,
            "output_per_1m": 10.0,
            "cache_read_per_1m": 0.1,
        },
        "cost_tier": "premium",
        "speed_tier": "thorough",
        "recommended_for": [
            "Hardest reasoning and agentic tasks",
            "Multimodal analysis (text, image, video, audio, PDF)",
        ],
        "best_practices": [
            "Only implicit caching is supported",
            "Up to 1M output tokens with long decode; 65,536 by default",
        ],
        "notes": "Google flagship. Launch pricing through 2026-11-30; from 2026-12-01 it rises to $4.00 input / $20.00 output / $0.20 cache read per 1M. Not on the free tier.",
    },
    "gemini-3-8-flash": {
        "name": "Gemini 3.8 Flash",
        "api_identifier": "gemini-3.8-flash",
        "context_window_input": 1048576,
        "context_window_output": 65536,
        "knowledge_cutoff": "Not published",
        "release_date": "2026-09-02",
        "capabilities": [
            "text_input",
            "text_output",
            "function_calling",
            "vision",
            "large_context",
            "prompt_caching",
            "streaming",
            "json_mode",
            "code_execution",
            "search",
        ],
        "pricing": {
            "input_per_1m": 0.75,
            "output_per_1m": 3.75,
            "cache_read_per_1m": 0.075,
        },
        "cost_tier": "mid-tier",
        "speed_tier": "fast",
        "recommended_for": [
            "General production workloads",
            "Replacement for gemini-2-5-pro and gemini-2-5-flash",
        ],
        "best_practices": [
            "Thinking levels low/medium/high; minimal returns an error",
            "Use Batch or Flex inference for non-urgent work",
        ],
        "notes": "RECOMMENDED Gemini default in this library. Launch pricing through 2026-12-31; from 2027-01-01 it rises to $1.50 input / $7.50 output / $0.15 cache read per 1M.",
    },
    "gemini-3-5-flash-lite": {
        "name": "Gemini 3.5 Flash-Lite",
        "api_identifier": "gemini-3.5-flash-lite",
        "context_window_input": 1048576,
        "context_window_output": 65536,
        "knowledge_cutoff": "Not published",
        "release_date": "2026-07-21",
        "capabilities": [
            "text_input",
            "text_output",
            "function_calling",
            "vision",
            "large_context",
            "prompt_caching",
            "streaming",
            "json_mode",
        ],
        "pricing": {
            "input_per_1m": 0.3,
            "output_per_1m": 2.5,
            "cache_read_per_1m": 0.03,
        },
        "cost_tier": "budget",
        "speed_tier": "fast",
        "recommended_for": [
            "High-volume, low-latency tasks",
            "Replacement for gemini-2-5-flash-lite",
        ],
        "best_practices": [
            "Use Batch or Flex inference for non-urgent work",
        ],
        "notes": "Context caching storage is billed separately at $1.00 per 1M tokens per hour.",
    },
    "gemini-2-5-pro": {
        "name": "Gemini 2.5 Pro",
        "api_identifier": "gemini-2.5-pro",
        "context_window_input": 1048576,
        "context_window_output": 65536,
        "knowledge_cutoff": "January 2025",
        "release_date": "2025-06-17",
        "capabilities": [
            "text_input",
            "text_output",
            "function_calling",
            "vision",
            "large_context",
            "prompt_caching",
            "streaming",
            "json_mode",
            "code_execution",
        ],
        "pricing": {
            "input_per_1m": 1.25,
            "output_per_1m": 10.0,
            "cache_read_per_1m": 0.125,
        },
        "cost_tier": "mid-tier",
        "speed_tier": "balanced",
        "recommended_for": [
            "Massive context processing (up to 1M tokens)",
            "Long document analysis",
            "Codebase understanding",
            "Multi-file reasoning",
            "Research paper analysis",
            "Book summarization",
        ],
        "best_practices": [
            "Leverage 1M token context for comprehensive analysis",
            "Use context caching for large repeated contexts",
            "Native code execution capability",
            "Excellent for multi-document tasks",
            "Use for processing entire codebases",
            "Strong at long-form content generation",
        ],
        "notes": "Not deprecated, but Google limits access to existing users and recommends gemini-3-8-flash for new projects. Prices shown are for prompts up to 200k tokens; longer prompts cost $2.50 input / $15.00 output per 1M.",
    },
    "gemini-2-5-flash": {
        "name": "Gemini 2.5 Flash",
        "api_identifier": "gemini-2.5-flash",
        "context_window_input": 1048576,
        "context_window_output": 65536,
        "knowledge_cutoff": "January 2025",
        "release_date": "2025-06-17",
        "capabilities": [
            "text_input",
            "text_output",
            "function_calling",
            "vision",
            "large_context",
            "prompt_caching",
            "streaming",
            "json_mode",
            "code_execution",
        ],
        "pricing": {
            "input_per_1m": 0.3,
            "output_per_1m": 2.5,
            "cache_read_per_1m": 0.03,
        },
        "cost_tier": "budget",
        "speed_tier": "fast",
        "recommended_for": [
            "High-speed processing",
            "Cost-optimized applications",
            "Large document processing",
            "Real-time analysis",
            "High-frequency API calls",
            "Multimodal tasks (text + vision)",
        ],
        "best_practices": [
            "Fastest model with 1M context window",
            "Excellent price-to-performance ratio",
            "Use for high-volume workflows",
            "Context caching reduces costs further",
            "Strong vision capabilities",
            "Code execution built-in",
        ],
        "notes": "Not deprecated, but Google limits access to existing users and recommends gemini-3-8-flash for new projects. Audio input costs $1.00 per 1M.",
    },
    "gemini-2-5-flash-lite": {
        "name": "Gemini 2.5 Flash-Lite",
        "api_identifier": "gemini-2.5-flash-lite",
        "context_window_input": 1048576,
        "context_window_output": 65536,
        "knowledge_cutoff": "January 2025",
        "release_date": "2025-07-22",
        "capabilities": [
            "text_input",
            "text_output",
            "vision",
            "large_context",
            "streaming",
        ],
        "pricing": {
            "input_per_1m": 0.1,
            "output_per_1m": 0.4,
            "cache_read_per_1m": 0.01,
        },
        "cost_tier": "budget",
        "speed_tier": "fast",
        "recommended_for": [
            "Experimental projects",
            "Prototyping and testing",
            "Educational use cases",
            "Low-cost POCs",
            "Simple text tasks",
            "Vision tasks (free tier)",
        ],
        "best_practices": [
            "Free tier with rate limits",
            "No function calling or caching",
            "Good for learning and experimentation",
            "Rate limits apply - check quotas",
            "Use for non-production workloads",
            "Upgrade to Flash for production",
        ],
        "notes": "Not deprecated, but Google limits access to existing users and recommends gemini-3-5-flash-lite for new projects. Paid model ($0.10/$0.40 per 1M); audio input costs $0.30 per 1M.",
    },
}


class GoogleFetcher(BaseFetcher):
    """Fetcher for Google Gemini models."""

    # Models tracked in ai_models/definitions/google/.
    MODEL_IDS = tuple(_STATIC_SPECS)

    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return "google"

    def fetch_models(self) -> list[ModelData]:
        """Fetch Gemini models.

        Returns:
            List of ModelData objects
        """
        try:
            return self.fetch_from_api()
        except Exception as e:
            self.logger.warning(f"API fetch failed: {e}. Falling back to docs parsing.")
            return self.fetch_from_docs()

    def fetch_from_api(self) -> list[ModelData]:
        """Fetch models using Google Generative AI API.

        Returns:
            List of ModelData objects
        """
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not set")

        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("google-generativeai package not installed")

        genai.configure(api_key=api_key)

        # The API lists models as "models/<api_identifier>", e.g. "models/gemini-2.5-pro".
        api_id_to_model_id = {
            _STATIC_SPECS[model_id]["api_identifier"]: model_id for model_id in self.MODEL_IDS
        }

        models = []
        seen_model_ids = set()  # Track already-added models to avoid duplicates

        for model_info in genai.list_models():
            api_name = model_info.name.split("/")[-1]
            model_id = api_id_to_model_id.get(api_name)
            if model_id is None or model_id in seen_model_ids:
                continue

            specs = self._get_static_model_specs(model_id)
            if specs:
                models.append(self._model_data_from_specs(model_id, specs, DOCS_URL, "google_api"))
                seen_model_ids.add(model_id)

        # If no models found via API, fall back to static specs
        if not models:
            raise ValueError("No tracked Gemini models found via API")

        return models

    def _get_static_model_specs(self, model_id: str) -> Optional[dict]:
        """Get static model specifications.

        Args:
            model_id: Model identifier

        Returns:
            Dictionary of model specifications
        """
        return _STATIC_SPECS.get(model_id)

    def fetch_from_docs(self) -> list[ModelData]:
        """Fetch models from static specifications (docs fallback).

        Returns:
            List of ModelData objects
        """
        self.logger.info("Using static model specifications")

        models = []
        for model_id in self.MODEL_IDS:
            specs = self._get_static_model_specs(model_id)
            if specs:
                models.append(self._model_data_from_specs(model_id, specs, DOCS_URL, "google_docs"))

        return models
