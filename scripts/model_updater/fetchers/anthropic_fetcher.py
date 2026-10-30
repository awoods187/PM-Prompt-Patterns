# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Anthropic Claude model fetcher."""

import os
from typing import TYPE_CHECKING, Any, Optional

from scripts.model_updater.fetchers.base_fetcher import BaseFetcher, ModelData

if TYPE_CHECKING:
    import anthropic

DOCS_URL = "https://platform.claude.com/docs/en/about-claude/models/overview"

# Static specs mirror ai_models/definitions/anthropic/*.yaml (last verified 2026-10-30).
# Keep them in sync: tests/test_model_updater/test_static_specs_match_definitions.py
# fails if a YAML and this table disagree.
_STATIC_SPECS: dict[str, dict[str, Any]] = {
    "claude-fable-5-1": {
        "name": "Claude Fable 5.1",
        "api_identifier": "claude-fable-5-1",
        "context_window_input": 1000000,
        "context_window_output": 128000,
        "knowledge_cutoff": "June 2026",
        "release_date": "2026-09-01",
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
            "input_per_1m": 10.0,
            "output_per_1m": 50.0,
            "cache_write_per_1m": 12.5,
            "cache_read_per_1m": 0.25,
        },
        "cost_tier": "premium",
        "speed_tier": "thorough",
        "recommended_for": [
            "Demanding multi-step reasoning",
            "Long-horizon agentic work",
            "Tasks where Opus 5.5 at high effort still falls short",
        ],
        "best_practices": [
            "Start with claude-opus-5-5 and move up only when evals require it",
            "Thinking is always on; steer depth with the effort parameter",
            "Cache long system prompts: cache reads cost 2.5% of base input",
        ],
        "notes": "Anthropic's most capable generally available model. Retirement not sooner than 2027-09-01.",
    },
    "claude-opus-5-5": {
        "name": "Claude Opus 5.5",
        "api_identifier": "claude-opus-5-5",
        "context_window_input": 1000000,
        "context_window_output": 128000,
        "knowledge_cutoff": "June 2026",
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
        ],
        "pricing": {
            "input_per_1m": 4.0,
            "output_per_1m": 20.0,
            "cache_write_per_1m": 5.0,
            "cache_read_per_1m": 0.2,
        },
        "cost_tier": "premium",
        "speed_tier": "balanced",
        "recommended_for": [
            "Long-running agentic coding",
            "Complex analysis and knowledge work",
            "Default choice for most demanding workloads",
        ],
        "best_practices": [
            "Thinking is always on; steer depth with the effort parameter (default medium)",
            "Do not set temperature, top_p, or top_k",
            "Cache long system prompts: cache reads cost 5% of base input",
        ],
        "notes": "Anthropic's recommended starting model for most workloads. Replaces claude-opus-4-1 in this library. Retirement not sooner than 2027-09-22.",
    },
    "claude-sonnet-5-5": {
        "name": "Claude Sonnet 5.5",
        "api_identifier": "claude-sonnet-5-5",
        "context_window_input": 1000000,
        "context_window_output": 128000,
        "knowledge_cutoff": "June 2026",
        "release_date": "2026-09-28",
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
        "speed_tier": "fast",
        "recommended_for": [
            "Production workhorse applications",
            "Code generation and review",
            "Document analysis and summarization",
            "Multi-step instructions",
        ],
        "best_practices": [
            "Use XML tags for structured prompts",
            "Enable prompt caching for repeated system prompts (cache reads cost 5% of base input)",
            "Do not set temperature, top_p, or top_k",
            "Forced tool use (tool_choice any/tool) returns an error; use auto",
        ],
        "notes": "RECOMMENDED default for most use cases. Replaces claude-sonnet-4-5. Retirement not sooner than 2027-09-28.",
    },
    "claude-haiku-5-5": {
        "name": "Claude Haiku 5.5",
        "api_identifier": "claude-haiku-5-5",
        "context_window_input": 1000000,
        "context_window_output": 128000,
        "knowledge_cutoff": "June 2026",
        "release_date": "2026-10-07",
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
            "input_per_1m": 0.1,
            "output_per_1m": 0.5,
            "cache_write_per_1m": 0.125,
            "cache_read_per_1m": 0.01,
        },
        "cost_tier": "budget",
        "speed_tier": "fast",
        "recommended_for": [
            "High-volume classification and routing",
            "Extraction",
            "Subagent tasks",
            "Latency-sensitive applications",
        ],
        "best_practices": [
            "Keep prompts under 100k tokens to stay on the lower price tier",
            "Do not set temperature, top_p, or top_k",
            "Expect about 30% more tokens than Haiku 4.5 for the same text (newer tokenizer)",
        ],
        "notes": "Prices shown are for prompts up to 100k tokens. Prompts over 100k cost $0.50 input / $2.50 output / $0.625 cache write / $0.05 cache read per 1M. Retirement not sooner than 2027-10-07.",
    },
    "claude-sonnet-4-5": {
        "name": "Claude Sonnet 4.5",
        "api_identifier": "claude-sonnet-4-5-20250929",
        "context_window_input": 200000,
        "context_window_output": None,
        "knowledge_cutoff": "January 2025",
        "release_date": "2025-09-29",
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
            "input_per_1m": 3.0,
            "output_per_1m": 15.0,
            "cache_write_per_1m": 3.75,
            "cache_read_per_1m": 0.3,
        },
        "cost_tier": "mid-tier",
        "speed_tier": "balanced",
        "recommended_for": [
            "Production workhorse applications",
            "Complex analysis and reasoning tasks",
            "Long-form content generation",
            "Code generation and review",
            "Multi-step instructions",
            "Document analysis and summarization",
        ],
        "best_practices": [
            "Use XML tags for structured prompts (Claude's native format)",
            "Enable prompt caching for repeated system prompts (90% cost savings)",
            "Leverage 200k context window for comprehensive analysis",
            "Use function calling for structured outputs",
            "Place examples in system prompt to benefit from caching",
            "Use thinking tags for complex reasoning tasks",
        ],
        "notes": "DEPRECATED: Anthropic deprecated Claude Sonnet 4.5 on 2026-09-30 and retires it on the Claude API on 2026-11-30. Migrate to claude-sonnet-5-5.",
    },
    "claude-haiku-4-5": {
        "name": "Claude Haiku 4.5",
        "api_identifier": "claude-haiku-4-5-20251001",
        "context_window_input": 200000,
        "context_window_output": None,
        "knowledge_cutoff": "February 2025",
        "release_date": "2025-10-01",
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
            "cache_read_per_1m": 0.1,
        },
        "cost_tier": "budget",
        "speed_tier": "fast",
        "recommended_for": [
            "High-volume classification tasks",
            "Fast processing requirements",
            "Real-time applications",
            "Cost-conscious projects",
            "Simple content generation",
            "Data extraction and parsing",
        ],
        "best_practices": [
            "Ideal for tasks under 10 seconds response time",
            "Use for high-frequency API calls (>1000/day)",
            "Enable prompt caching for maximum cost savings",
            "Perfect for customer signal classification",
            "Use XML tags for best structured output",
            "Cascade from Haiku to Sonnet for edge cases",
        ],
        "notes": "Legacy model, still active. Claude Haiku 5.5 is the current Haiku and is cheaper for prompts under 100k tokens.",
    },
    "claude-opus-4-1": {
        "name": "Claude Opus 4.1",
        "api_identifier": "claude-opus-4-1-20250805",
        "context_window_input": 200000,
        "context_window_output": None,
        "knowledge_cutoff": "December 2024",
        "release_date": "2025-08-05",
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
            "input_per_1m": 15.0,
            "output_per_1m": 75.0,
            "cache_write_per_1m": 18.75,
            "cache_read_per_1m": 1.5,
        },
        "cost_tier": "premium",
        "speed_tier": "thorough",
        "recommended_for": [
            "Highest quality reasoning tasks",
            "Complex research and analysis",
            "Expert-level content generation",
            "Legal and medical document review",
            "Scientific reasoning",
            "Creative writing and ideation",
        ],
        "best_practices": [
            "Use when Sonnet quality is insufficient",
            "Leverage for complex multi-step reasoning",
            "Ideal for tasks requiring deep domain expertise",
            "Worth the premium for business-critical decisions",
            "Enable caching to reduce costs on repeated prompts",
            "Use for final review in cascading workflows",
        ],
        "notes": "RETIRED on the Claude API on 2026-08-05 (requests fail). Still offered on Amazon Bedrock and Google-managed Vertex AI on their own schedules. Anthropic's listed replacement is claude-opus-4-8; this library migrates to claude-opus-5-5.",
    },
}


class AnthropicFetcher(BaseFetcher):
    """Fetcher for Anthropic Claude models."""

    # Models tracked in ai_models/definitions/anthropic/, deprecated ones included.
    MODEL_IDS = tuple(_STATIC_SPECS)

    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return "anthropic"

    def fetch_models(self) -> list[ModelData]:
        """Fetch Claude models.

        Tries API first if ANTHROPIC_API_KEY is available,
        falls back to documentation parsing.

        Returns:
            List of ModelData objects
        """
        try:
            # Try API first
            return self.fetch_from_api()
        except Exception as e:
            self.logger.warning(f"API fetch failed: {e}. Falling back to docs parsing.")
            try:
                return self.fetch_from_docs()
            except Exception as doc_error:
                self.logger.error(f"Docs parsing failed: {doc_error}")
                raise

    def fetch_from_api(self) -> list[ModelData]:
        """Fetch models using Anthropic API.

        The API doesn't expose pricing or context specs, so we use the
        static table and verify availability with the API.

        Returns:
            List of ModelData objects
        """
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")

        try:
            import anthropic
        except ImportError:
            raise ImportError("anthropic package not installed") from None

        client = anthropic.Anthropic(api_key=api_key)

        known_models = [
            {
                "model_id": model_id,
                "api_identifier": _STATIC_SPECS[model_id]["api_identifier"],
                "name": _STATIC_SPECS[model_id]["name"],
            }
            for model_id in self.MODEL_IDS
        ]

        models = []
        for model_info in known_models:
            try:
                model_data = self._get_model_details(
                    client, model_info["api_identifier"], model_info
                )
                if model_data:
                    models.append(model_data)
            except Exception as e:
                self.logger.warning(f"Failed to fetch {model_info['model_id']}: {e}. Skipping.")

        return models

    def _get_model_details(
        self, client: "anthropic.Anthropic", api_id: str, base_info: dict
    ) -> Optional[ModelData]:
        """Get detailed model information.

        Args:
            client: Anthropic client
            api_id: API identifier for the model
            base_info: Base model information

        Returns:
            ModelData object or None if model not available
        """
        # Fetch from static knowledge (API doesn't provide model specs)
        model_specs = self._get_static_model_specs(base_info["model_id"])
        if not model_specs:
            return None

        specs = {**model_specs, "name": base_info["name"], "api_identifier": api_id}
        return self._model_data_from_specs(base_info["model_id"], specs, DOCS_URL, "anthropic_api")

    def _get_static_model_specs(self, model_id: str) -> Optional[dict]:
        """Get static model specifications.

        This is needed because Anthropic's API doesn't provide
        model specifications through an endpoint.

        Args:
            model_id: Model identifier

        Returns:
            Dictionary of model specifications
        """
        return _STATIC_SPECS.get(model_id)

    def fetch_from_docs(self) -> list[ModelData]:
        """Fetch models from the static specifications (docs fallback).

        Returns:
            List of ModelData objects
        """
        # Docs parsing isn't implemented; the static table is the fallback.
        self.logger.info("Using static model specifications (docs parsing not implemented)")

        models = []
        for model_id in self.MODEL_IDS:
            specs = self._get_static_model_specs(model_id)
            if specs:
                models.append(
                    self._model_data_from_specs(model_id, specs, DOCS_URL, "anthropic_docs")
                )

        return models
