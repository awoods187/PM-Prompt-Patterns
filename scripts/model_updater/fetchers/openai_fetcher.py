# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""OpenAI GPT model fetcher."""

import os
from typing import Any, Optional

from scripts.model_updater.fetchers.base_fetcher import BaseFetcher, ModelData

DOCS_URL = "https://developers.openai.com/api/docs/models"

# Static specs mirror ai_models/definitions/openai/*.yaml (last verified 2026-10-30).
# Keep them in sync: tests/test_model_updater/test_static_specs_match_definitions.py
# fails if a YAML and this table disagree.
_STATIC_SPECS: dict[str, dict[str, Any]] = {
    "gpt-6-astra": {
        "name": "GPT-6 Astra",
        "api_identifier": "gpt-6-astra",
        "context_window_input": 922000,
        "context_window_output": 128000,
        "knowledge_cutoff": "April 2026",
        "release_date": "2026-09-03",
        "capabilities": [
            "text_input",
            "text_output",
            "function_calling",
            "vision",
            "large_context",
            "prompt_caching",
            "streaming",
            "json_mode",
            "search",
        ],
        "pricing": {
            "input_per_1m": 10.0,
            "output_per_1m": 50.0,
            "cache_write_per_1m": 12.5,
            "cache_read_per_1m": 1.0,
        },
        "cost_tier": "premium",
        "speed_tier": "thorough",
        "recommended_for": [
            "Hardest reasoning and agentic tasks",
            "OpenAI's suggested starting point",
        ],
        "best_practices": [
            "Use the Responses API for function calling",
            "Keep prompts under 272k input tokens to avoid 2x input / 1.5x output pricing",
        ],
        "notes": "OpenAI flagship. 1.05M total context (922k input, 128k output). Prompts over 272k input tokens cost 2x input and cache rates and 1.5x output.",
    },
    "gpt-6.1-sol": {
        "name": "GPT-6.1 Sol",
        "api_identifier": "gpt-6.1-sol",
        "context_window_input": 922000,
        "context_window_output": 128000,
        "knowledge_cutoff": "April 2026",
        "release_date": "2026-09-29",
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
            "input_per_1m": 2.0,
            "output_per_1m": 10.0,
            "cache_write_per_1m": 2.5,
            "cache_read_per_1m": 0.1,
        },
        "cost_tier": "mid-tier",
        "speed_tier": "balanced",
        "recommended_for": [
            "General production workloads",
            "Coding and analysis",
            "Replacement for gpt-5 and o3",
        ],
        "best_practices": [
            "Use the Responses API for function calling",
            "Keep prompts under 272k input tokens to avoid 2x input / 1.5x output pricing",
        ],
        "notes": "RECOMMENDED OpenAI default in this library. 1.05M total context (922k input, 128k output). Prompts over 272k input tokens cost 2x input and cache rates and 1.5x output.",
    },
    "gpt-6.1-terra": {
        "name": "GPT-6.1 Terra",
        "api_identifier": "gpt-6.1-terra",
        "context_window_input": 922000,
        "context_window_output": 128000,
        "knowledge_cutoff": "June 2026",
        "release_date": "2026-10-26",
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
            "input_per_1m": 1.0,
            "output_per_1m": 5.0,
            "cache_write_per_1m": 1.25,
            "cache_read_per_1m": 0.05,
        },
        "cost_tier": "mid-tier",
        "speed_tier": "fast",
        "recommended_for": [
            "Cost-sensitive production workloads",
            "Replacement for gpt-5-mini and o4-mini",
        ],
        "best_practices": [
            "Keep prompts under 272k input tokens to avoid 2x input / 1.5x output pricing",
        ],
        "notes": "1.05M total context (922k input, 128k output).",
    },
    "gpt-6-luna": {
        "name": "GPT-6 Luna",
        "api_identifier": "gpt-6-luna",
        "context_window_input": 922000,
        "context_window_output": 128000,
        "knowledge_cutoff": "May 2026",
        "release_date": "2026-09-22",
        "capabilities": [
            "text_input",
            "text_output",
            "function_calling",
            "vision",
            "large_context",
            "prompt_caching",
            "streaming",
            "json_mode",
            "search",
        ],
        "pricing": {
            "input_per_1m": 0.1,
            "output_per_1m": 0.5,
            "cache_write_per_1m": 0.125,
            "cache_read_per_1m": 0.01,
        },
        "cost_tier": "budget",
        "speed_tier": "fast",
        "recommended_for": [
            "High-volume, low-cost tasks",
            "Classification and extraction",
            "Replacement for gpt-4o, gpt-4o-mini, gpt-4.1, and gpt-4.1-mini",
        ],
        "best_practices": [
            "On Chat Completions, function calling requires reasoning_effort set to none",
            "Use Batch or Flex for 50% off non-urgent work",
        ],
        "notes": "OpenAI's lowest-cost current model. 1.05M total context (922k input, 128k output).",
    },
    "gpt-5": {
        "name": "GPT-5",
        "api_identifier": "gpt-5-2025-08-07",
        "context_window_input": 272000,
        "context_window_output": 128000,
        "knowledge_cutoff": "September 2024",
        "release_date": "2025-08-07",
        "capabilities": [
            "text_input",
            "text_output",
            "function_calling",
            "vision",
            "large_context",
            "streaming",
            "json_mode",
            "auto_routing",
            "advanced_reasoning",
        ],
        "pricing": {
            "input_per_1m": 1.25,
            "output_per_1m": 10.0,
            "cache_read_per_1m": 0.125,
        },
        "cost_tier": "mid-tier",
        "speed_tier": "balanced",
        "recommended_for": [
            "Default choice for most tasks",
            "Auto-routing between Instant (fast) and Thinking (complex) modes",
            "General-purpose applications with highest quality",
            "Complex reasoning and analysis",
            "Multimodal applications (text + vision)",
            "Function calling workflows",
            "Structured JSON output",
        ],
        "best_practices": [
            "GPT-5 automatically routes to Instant mode for simple tasks and Thinking mode for complex reasoning",
            "Use JSON mode for guaranteed structured outputs",
            "Leverage function calling for tool integration",
            "Vision capability for image understanding",
            "Set max_tokens to control output costs",
            "Use system messages for consistent behavior",
            "Stream responses for better UX",
            "Ideal for production applications requiring best quality",
        ],
        "notes": "DEPRECATED: OpenAI shuts down gpt-5 on 2026-12-11. OpenAI lists gpt-5.6-sol as the replacement; this library migrates to gpt-6.1-sol. Context window is 400k total (272k input, 128k output).",
    },
    "gpt-5-mini": {
        "name": "GPT-5 mini",
        "api_identifier": "gpt-5-mini-2025-08-07",
        "context_window_input": 272000,
        "context_window_output": 128000,
        "knowledge_cutoff": "May 2024",
        "release_date": "2025-08-07",
        "capabilities": [
            "text_input",
            "text_output",
            "function_calling",
            "vision",
            "large_context",
            "streaming",
            "json_mode",
        ],
        "pricing": {
            "input_per_1m": 0.25,
            "output_per_1m": 2.0,
            "cache_read_per_1m": 0.025,
        },
        "cost_tier": "budget",
        "speed_tier": "fast",
        "recommended_for": [
            "Fast, efficient GPT-5 variant",
            "Budget-conscious applications",
            "High-volume classification tasks",
            "Simpler reasoning tasks",
            "Function calling for structured outputs",
            "JSON mode applications",
            "Real-time applications requiring low latency",
        ],
        "best_practices": [
            "Excellent balance of speed, cost, and capability",
            "Use JSON mode for structured outputs",
            "Leverage function calling for tool integration",
            "Set temperature=0 for deterministic outputs",
            "Batch requests for cost efficiency",
            "Stream responses for better UX",
            "Ideal for simple to moderate complexity tasks",
        ],
        "notes": "DEPRECATED: OpenAI shuts down gpt-5-mini on 2026-12-11. OpenAI lists gpt-5.6-terra as the replacement; this library migrates to gpt-6.1-terra.",
    },
    "gpt-4.1": {
        "name": "GPT-4.1",
        "api_identifier": "gpt-4.1-2025-04-14",
        "context_window_input": 1047576,
        "context_window_output": 32768,
        "knowledge_cutoff": "June 2024",
        "release_date": "2025-04-14",
        "capabilities": [
            "text_input",
            "text_output",
            "function_calling",
            "vision",
            "large_context",
            "streaming",
            "json_mode",
            "code_generation",
            "tool_use",
        ],
        "pricing": {
            "input_per_1m": 2.0,
            "output_per_1m": 8.0,
            "cache_read_per_1m": 0.5,
        },
        "cost_tier": "mid-tier",
        "speed_tier": "balanced",
        "recommended_for": [
            "Code generation and review",
            "Precise instruction following for web development",
            "Tool use and function calling",
            "API integration and structured outputs",
            "Long context without reasoning overhead",
            "Technical documentation",
            "Debugging and code analysis",
        ],
        "best_practices": [
            "Specialized for coding tasks with precise instructions",
            "Excels at web development and technical tasks",
            "Use function calling for tool integration",
            "Leverages 200k context for large codebases",
            "Set temperature=0 for deterministic code generation",
            "Use JSON mode for structured outputs",
            "Ideal for code-heavy applications",
        ],
        "notes": "DEPRECATED: OpenAI shuts down gpt-4.1 on 2027-01-14. Replacement: gpt-6-luna.",
    },
    "gpt-4.1-mini": {
        "name": "GPT-4.1 mini",
        "api_identifier": "gpt-4.1-mini-2025-04-14",
        "context_window_input": 1047576,
        "context_window_output": 32768,
        "knowledge_cutoff": "June 2024",
        "release_date": "2025-04-14",
        "capabilities": [
            "text_input",
            "text_output",
            "function_calling",
            "vision",
            "large_context",
            "streaming",
            "json_mode",
            "code_generation",
            "tool_use",
        ],
        "pricing": {
            "input_per_1m": 0.4,
            "output_per_1m": 1.6,
            "cache_read_per_1m": 0.1,
        },
        "cost_tier": "budget",
        "speed_tier": "fast",
        "recommended_for": [
            "Fast coding model (replaced GPT-4o mini)",
            "Budget-friendly code generation",
            "High-volume coding tasks",
            "Tool use and function calling",
            "Structured outputs for APIs",
            "Simple to moderate coding tasks",
            "Real-time code assistance",
        ],
        "best_practices": [
            "Excellent for budget-conscious coding applications",
            "Fast small model specialized for code",
            "Use function calling for tool integration",
            "Set temperature=0 for deterministic code",
            "Use JSON mode for structured outputs",
            "Batch requests for cost efficiency",
            "Ideal replacement for GPT-4o mini",
        ],
        "notes": "DEPRECATED: OpenAI shuts down gpt-4.1-mini on 2027-01-14. Replacement: gpt-6-luna.",
    },
    "gpt-4o": {
        "name": "GPT-4o",
        "api_identifier": "gpt-4o-2024-08-06",
        "context_window_input": 128000,
        "context_window_output": 16384,
        "knowledge_cutoff": "October 2023",
        "release_date": "2024-08-06",
        "capabilities": [
            "text_input",
            "text_output",
            "function_calling",
            "vision",
            "voice",
            "realtime_api",
            "large_context",
            "streaming",
            "json_mode",
        ],
        "pricing": {
            "input_per_1m": 2.5,
            "output_per_1m": 10.0,
            "cache_read_per_1m": 1.25,
        },
        "cost_tier": "mid-tier",
        "speed_tier": "balanced",
        "recommended_for": [
            "Multimodal specialist (voice, vision, text)",
            "GPT-4o Realtime API for live audio",
            "Voice-based applications",
            "Vision-heavy applications",
            "Low-latency multimodal tasks",
            "Function calling workflows",
            "Structured JSON output",
        ],
        "best_practices": [
            "Primary use case: multimodal applications requiring voice or vision",
            "Use GPT-4o Realtime API for live audio applications",
            "Leverage vision capability for image understanding",
            "Use JSON mode for structured outputs",
            "Function calling for tool integration",
            "Set max_tokens to control output costs",
            "Stream responses for better UX",
            "For general tasks, consider GPT-5 instead",
        ],
        "notes": "DEPRECATED: OpenAI shuts down gpt-4o-2024-08-06 on 2027-01-14. Replacement: gpt-6-luna.",
    },
    "gpt-4o-mini": {
        "name": "GPT-4o Mini",
        "api_identifier": "gpt-4o-mini-2024-07-18",
        "context_window_input": 128000,
        "context_window_output": 16384,
        "knowledge_cutoff": "October 2023",
        "release_date": "2024-07-18",
        "capabilities": [
            "text_input",
            "text_output",
            "function_calling",
            "vision",
            "large_context",
            "streaming",
            "json_mode",
        ],
        "pricing": {
            "input_per_1m": 0.15,
            "output_per_1m": 0.6,
            "cache_read_per_1m": 0.075,
        },
        "cost_tier": "budget",
        "speed_tier": "fast",
        "recommended_for": [
            "DEPRECATED: Use gpt-6-luna instead",
            "Legacy applications only",
        ],
        "best_practices": [
            "Migrate to gpt-6-luna before the 2027-01-14 shutdown",
            "Existing applications should plan migration",
        ],
        "notes": "DEPRECATED: OpenAI shuts down gpt-4o-mini on 2027-01-14. Replacement: gpt-6-luna.",
    },
    "o3": {
        "name": "o3",
        "api_identifier": "o3-2025-04-16",
        "context_window_input": 200000,
        "context_window_output": 100000,
        "knowledge_cutoff": "June 2024",
        "release_date": "2025-04-16",
        "capabilities": [
            "text_input",
            "text_output",
            "function_calling",
            "vision",
            "large_context",
            "streaming",
            "json_mode",
            "advanced_reasoning",
            "tool_use",
            "scientific_analysis",
        ],
        "pricing": {
            "input_per_1m": 2.0,
            "output_per_1m": 8.0,
            "cache_read_per_1m": 0.5,
        },
        "cost_tier": "premium",
        "speed_tier": "thorough",
        "recommended_for": [
            "Advanced reasoning and complex analysis",
            "Scientific problems and research",
            "Mathematical reasoning",
            "Multi-step problem solving",
            "Full tool access for complex workflows",
            "High-stakes decisions requiring thorough analysis",
            "Edge cases and ambiguous scenarios",
        ],
        "best_practices": [
            "Most capable reasoning model before GPT-5",
            "Full tool access for complex workflows",
            "Excels at scientific and mathematical reasoning",
            "Use for high-value, complex reasoning tasks",
            "Leverage function calling for multi-tool workflows",
            "Set higher max_tokens for complex reasoning chains",
            "Ideal for problems requiring deep analysis",
        ],
        "notes": "DEPRECATED: OpenAI shuts down o3 on 2026-12-11. OpenAI lists gpt-5.6-sol as the replacement; this library migrates to gpt-6.1-sol.",
    },
    "o4-mini": {
        "name": "o4-mini",
        "api_identifier": "o4-mini-2025-04-16",
        "context_window_input": 200000,
        "context_window_output": 100000,
        "knowledge_cutoff": "June 2024",
        "release_date": "2025-04-16",
        "capabilities": [
            "text_input",
            "text_output",
            "function_calling",
            "vision",
            "large_context",
            "streaming",
            "json_mode",
            "advanced_reasoning",
            "tool_use",
            "visual_reasoning",
        ],
        "pricing": {
            "input_per_1m": 1.1,
            "output_per_1m": 4.4,
            "cache_read_per_1m": 0.275,
        },
        "cost_tier": "budget",
        "speed_tier": "fast",
        "recommended_for": [
            "Fast, cost-efficient reasoning",
            "Math and coding tasks",
            "Visual reasoning (think with images)",
            "Sketches, diagrams, low-quality images",
            "Higher usage limits than o3",
            "Budget-friendly reasoning tasks",
            "Real-time reasoning applications",
        ],
        "best_practices": [
            "Can 'think with images' - analyzes sketches, diagrams, low-quality images",
            "Higher usage limits than o3 models",
            "Excellent for math and coding reasoning",
            "Use for cost-effective reasoning at scale",
            "Leverage visual reasoning for diagram analysis",
            "Set appropriate max_tokens for reasoning chains",
            "Ideal for high-volume reasoning workloads",
        ],
        "notes": "SHUT DOWN by OpenAI on 2026-10-23 (requests fail). OpenAI lists gpt-5.6-terra as the replacement; this library migrates to gpt-6.1-terra.",
    },
}


class OpenAIFetcher(BaseFetcher):
    """Fetcher for OpenAI GPT models."""

    # Models tracked in ai_models/definitions/openai/, deprecated ones included.
    MODEL_IDS = tuple(_STATIC_SPECS)

    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return "openai"

    def fetch_models(self) -> list[ModelData]:
        """Fetch GPT models using OpenAI API.

        Returns:
            List of ModelData objects
        """
        try:
            return self.fetch_from_api()
        except Exception as e:
            self.logger.warning(f"API fetch failed: {e}. Falling back to docs parsing.")
            return self.fetch_from_docs()

    def fetch_from_api(self) -> list[ModelData]:
        """Fetch models using OpenAI API.

        Returns:
            List of ModelData objects
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")

        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package not installed") from None

        client = OpenAI(api_key=api_key)

        # Note: OpenAI API provides model list but not detailed specs
        # We use static specs and verify model exists via API
        _models_list = client.models.list()  # Verify API connection

        models = []
        for model_id in self.MODEL_IDS:
            try:
                # Verify model exists
                _model_info = client.models.retrieve(model_id)

                # Get specs from static knowledge (API doesn't provide full specs)
                specs = self._get_static_model_specs(model_id)
                if not specs:
                    self.logger.warning(f"No specs found for {model_id}, skipping")
                    continue

                models.append(self._model_data_from_specs(model_id, specs, DOCS_URL, "openai_api"))
            except Exception as e:
                self.logger.warning(f"Failed to fetch {model_id}: {e}")

        return models

    def _get_static_model_specs(self, model_id: str) -> Optional[dict]:
        """Get static model specifications.

        OpenAI's API doesn't provide detailed specs like context windows
        and pricing, so we maintain these from documentation.

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
                models.append(self._model_data_from_specs(model_id, specs, DOCS_URL, "openai_docs"))

        return models
