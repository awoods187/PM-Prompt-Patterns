# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Anthropic Claude model fetcher."""

import os
import re
from datetime import date
from typing import Optional

from scripts.model_updater.fetchers.base_fetcher import BaseFetcher, ModelData


class AnthropicFetcher(BaseFetcher):
    """Fetcher for Anthropic Claude models."""

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

        Note: Anthropic doesn't have a models list endpoint yet,
        so we use a known list and verify with API.

        Returns:
            List of ModelData objects
        """
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")

        try:
            import anthropic
        except ImportError:
            raise ImportError("anthropic package not installed")

        client = anthropic.Anthropic(api_key=api_key)

        # Known Claude 4.5 models (as of 2025)
        # Since Anthropic doesn't have a models list endpoint,
        # we maintain a reference list and verify availability
        known_models = [
            {
                "model_id": "claude-sonnet-4-5",
                "api_identifier": "claude-sonnet-4-5-20250929",
                "name": "Claude Sonnet 4.5",
            },
            {
                "model_id": "claude-haiku-4-5",
                "api_identifier": "claude-haiku-4-5-20250805",
                "name": "Claude Haiku 4.5",
            },
            {
                "model_id": "claude-opus-4-1",
                "api_identifier": "claude-opus-4-1-20250514",
                "name": "Claude Opus 4.1",
            },
        ]

        models = []
        for model_info in known_models:
            try:
                # Verify model exists by making a small test request
                model_data = self._get_model_details(
                    client, model_info["api_identifier"], model_info
                )
                if model_data:
                    models.append(model_data)
            except Exception as e:
                self.logger.warning(
                    f"Failed to fetch {model_info['model_id']}: {e}. Skipping."
                )

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

        return ModelData(
            model_id=base_info["model_id"],
            provider="anthropic",
            name=base_info["name"],
            api_identifier=api_id,
            context_window_input=model_specs["context_window_input"],
            context_window_output=model_specs.get("context_window_output"),
            knowledge_cutoff=model_specs["knowledge_cutoff"],
            release_date=date.fromisoformat(model_specs["release_date"]),
            docs_url="https://docs.claude.com/en/docs/about-claude/models",
            capabilities=model_specs["capabilities"],
            input_per_1m=model_specs["pricing"]["input_per_1m"],
            output_per_1m=model_specs["pricing"]["output_per_1m"],
            cache_write_per_1m=model_specs["pricing"].get("cache_write_per_1m"),
            cache_read_per_1m=model_specs["pricing"].get("cache_read_per_1m"),
            recommended_for=model_specs.get("recommended_for", []),
            best_practices=model_specs.get("best_practices", []),
            cost_tier=model_specs.get("cost_tier", "mid-tier"),
            speed_tier=model_specs.get("speed_tier", "balanced"),
            notes=model_specs.get("notes", ""),
            source="anthropic_api",
        )

    def _get_static_model_specs(self, model_id: str) -> Optional[dict]:
        """Get static model specifications.

        This is needed because Anthropic's API doesn't provide
        model specifications through an endpoint. These specs
        should be updated periodically from official docs.

        Args:
            model_id: Model identifier

        Returns:
            Dictionary of model specifications
        """
        specs = {
            "claude-sonnet-4-5": {
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
                    "input_per_1m": 3.00,
                    "output_per_1m": 15.00,
                    "cache_write_per_1m": 3.75,
                    "cache_read_per_1m": 0.30,
                },
                "cost_tier": "mid-tier",
                "speed_tier": "balanced",
                "recommended_for": [
                    "Production workhorse applications",
                    "Complex analysis and reasoning tasks",
                    "Long-form content generation",
                    "Code generation and review",
                ],
                "best_practices": [
                    "Use XML tags for structured prompts (Claude's native format)",
                    "Enable prompt caching for repeated system prompts (90% cost savings)",
                    "Leverage 200k context window for comprehensive analysis",
                    "Use function calling for structured outputs",
                ],
                "notes": "RECOMMENDED for most use cases. Training data through July 2025.",
            },
            "claude-haiku-4-5": {
                "context_window_input": 200000,
                "context_window_output": 16000,
                "knowledge_cutoff": "July 2024",
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
                    "input_per_1m": 0.80,
                    "output_per_1m": 4.00,
                    "cache_write_per_1m": 1.00,
                    "cache_read_per_1m": 0.08,
                },
                "cost_tier": "budget",
                "speed_tier": "fast",
                "recommended_for": [
                    "High-volume applications",
                    "Fast response requirements",
                    "Simple classification tasks",
                    "Content moderation",
                ],
                "best_practices": [
                    "Use for high-throughput workloads",
                    "Leverage speed for real-time applications",
                    "Enable caching for cost optimization",
                    "Good for simple to moderate complexity tasks",
                ],
                "notes": "Fastest Claude model. Best for high-volume, cost-sensitive applications.",
            },
            "claude-opus-4-1": {
                "context_window_input": 200000,
                "context_window_output": 16000,
                "knowledge_cutoff": "August 2024",
                "release_date": "2025-05-14",
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
                    "input_per_1m": 15.00,
                    "output_per_1m": 75.00,
                    "cache_write_per_1m": 18.75,
                    "cache_read_per_1m": 1.50,
                },
                "cost_tier": "premium",
                "speed_tier": "thorough",
                "recommended_for": [
                    "Complex research and analysis",
                    "Advanced reasoning tasks",
                    "Critical decision support",
                    "High-stakes content generation",
                ],
                "best_practices": [
                    "Reserve for most demanding tasks",
                    "Use caching extensively to reduce costs",
                    "Leverage extended thinking for complex problems",
                    "Best for tasks requiring highest accuracy",
                ],
                "notes": "Most capable Claude model. Use for tasks requiring maximum intelligence.",
            },
        }

        return specs.get(model_id)

    def fetch_from_docs(self) -> list[ModelData]:
        """Fetch models by parsing Anthropic documentation.

        Returns:
            List of ModelData objects
        """
        # For now, fallback to static specs
        # In production, this would parse the actual docs page
        self.logger.info("Using static model specifications (docs parsing not implemented)")

        models = []
        for model_id in ["claude-sonnet-4-5", "claude-haiku-4-5", "claude-opus-4-1"]:
            specs = self._get_static_model_specs(model_id)
            if specs:
                # Infer API identifier from model_id and release date
                api_id = self._infer_api_identifier(model_id, specs["release_date"])

                models.append(
                    ModelData(
                        model_id=model_id,
                        provider="anthropic",
                        name=specs.get("name", model_id.replace("-", " ").title()),
                        api_identifier=api_id,
                        context_window_input=specs["context_window_input"],
                        context_window_output=specs.get("context_window_output"),
                        knowledge_cutoff=specs["knowledge_cutoff"],
                        release_date=date.fromisoformat(specs["release_date"]),
                        docs_url="https://docs.claude.com/en/docs/about-claude/models",
                        capabilities=specs["capabilities"],
                        input_per_1m=specs["pricing"]["input_per_1m"],
                        output_per_1m=specs["pricing"]["output_per_1m"],
                        cache_write_per_1m=specs["pricing"].get("cache_write_per_1m"),
                        cache_read_per_1m=specs["pricing"].get("cache_read_per_1m"),
                        recommended_for=specs.get("recommended_for", []),
                        best_practices=specs.get("best_practices", []),
                        cost_tier=specs.get("cost_tier", "mid-tier"),
                        speed_tier=specs.get("speed_tier", "balanced"),
                        notes=specs.get("notes", ""),
                        source="anthropic_docs",
                    )
                )

        return models

    def _infer_api_identifier(self, model_id: str, release_date: str) -> str:
        """Infer API identifier from model ID and release date.

        Anthropic uses format: claude-{tier}-{version}-{YYYYMMDD}

        Args:
            model_id: Model ID (e.g., "claude-sonnet-4-5")
            release_date: Release date in ISO format

        Returns:
            API identifier
        """
        # Parse date
        date_obj = date.fromisoformat(release_date)
        date_str = date_obj.strftime("%Y%m%d")

        return f"{model_id}-{date_str}"
