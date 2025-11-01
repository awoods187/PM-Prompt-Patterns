# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""OpenAI GPT model fetcher."""

import os
from datetime import date
from typing import Optional

from scripts.model_updater.fetchers.base_fetcher import BaseFetcher, ModelData


class OpenAIFetcher(BaseFetcher):
    """Fetcher for OpenAI GPT models."""

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
            raise ImportError("openai package not installed")

        client = OpenAI(api_key=api_key)

        # Get list of models
        models_response = client.models.list()

        # Filter for GPT-4o models (our current focus)
        target_models = ["gpt-4o", "gpt-4o-mini"]
        models = []

        for model_id in target_models:
            try:
                # Get model details
                model_obj = client.models.retrieve(model_id)

                # Get specs from static knowledge (API doesn't provide full specs)
                specs = self._get_static_model_specs(model_id)
                if not specs:
                    self.logger.warning(f"No specs found for {model_id}, skipping")
                    continue

                models.append(
                    ModelData(
                        model_id=model_id,
                        provider="openai",
                        name=specs["name"],
                        api_identifier=specs["api_identifier"],
                        context_window_input=specs["context_window_input"],
                        context_window_output=specs["context_window_output"],
                        knowledge_cutoff=specs["knowledge_cutoff"],
                        release_date=date.fromisoformat(specs["release_date"]),
                        docs_url=f"https://platform.openai.com/docs/models/{model_id}",
                        capabilities=specs["capabilities"],
                        input_per_1m=specs["pricing"]["input_per_1m"],
                        output_per_1m=specs["pricing"]["output_per_1m"],
                        recommended_for=specs.get("recommended_for", []),
                        best_practices=specs.get("best_practices", []),
                        cost_tier=specs.get("cost_tier", "mid-tier"),
                        speed_tier=specs.get("speed_tier", "balanced"),
                        notes=specs.get("notes", ""),
                        source="openai_api",
                    )
                )
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
        specs = {
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
                    "large_context",
                    "streaming",
                    "json_mode",
                ],
                "pricing": {
                    "input_per_1m": 2.50,
                    "output_per_1m": 10.00,
                },
                "cost_tier": "mid-tier",
                "speed_tier": "balanced",
                "recommended_for": [
                    "Multimodal applications (text + vision)",
                    "Complex reasoning tasks",
                    "Function calling workflows",
                    "Structured JSON output",
                    "General purpose API integration",
                    "Cost-effective GPT-4 level quality",
                ],
                "best_practices": [
                    "Use JSON mode for structured outputs",
                    "Leverage function calling for tool integration",
                    "Vision capability for image understanding",
                    "Set max_tokens to control output costs",
                    "Use system messages for consistent behavior",
                    "Stream responses for better UX",
                ],
                "notes": "OpenAI's flagship model. Good balance of capability and cost. 128k context window.",
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
                    "output_per_1m": 0.60,
                },
                "cost_tier": "budget",
                "speed_tier": "fast",
                "recommended_for": [
                    "High-volume applications",
                    "Cost-sensitive workloads",
                    "Simple to moderate tasks",
                    "Fast response requirements",
                    "Batch processing",
                    "Development and testing",
                ],
                "best_practices": [
                    "Use for high-throughput scenarios",
                    "Good replacement for GPT-3.5 Turbo",
                    "Leverage vision for image tasks at lower cost",
                    "Batch similar requests for efficiency",
                    "Enable streaming for responsiveness",
                    "Monitor quality vs cost tradeoff",
                ],
                "notes": "Budget-friendly option. Excellent for high-volume applications. Similar capabilities to GPT-4o at much lower cost.",
            },
        }

        return specs.get(model_id)

    def fetch_from_docs(self) -> list[ModelData]:
        """Fetch models from static specifications (docs fallback).

        Returns:
            List of ModelData objects
        """
        self.logger.info("Using static model specifications")

        models = []
        for model_id in ["gpt-4o", "gpt-4o-mini"]:
            specs = self._get_static_model_specs(model_id)
            if specs:
                models.append(
                    ModelData(
                        model_id=model_id,
                        provider="openai",
                        name=specs["name"],
                        api_identifier=specs["api_identifier"],
                        context_window_input=specs["context_window_input"],
                        context_window_output=specs["context_window_output"],
                        knowledge_cutoff=specs["knowledge_cutoff"],
                        release_date=date.fromisoformat(specs["release_date"]),
                        docs_url=f"https://platform.openai.com/docs/models/{model_id}",
                        capabilities=specs["capabilities"],
                        input_per_1m=specs["pricing"]["input_per_1m"],
                        output_per_1m=specs["pricing"]["output_per_1m"],
                        recommended_for=specs.get("recommended_for", []),
                        best_practices=specs.get("best_practices", []),
                        cost_tier=specs.get("cost_tier", "mid-tier"),
                        speed_tier=specs.get("speed_tier", "balanced"),
                        notes=specs.get("notes", ""),
                        source="openai_docs",
                    )
                )

        return models
