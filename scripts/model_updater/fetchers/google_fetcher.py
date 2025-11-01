# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Google Gemini model fetcher."""

import os
from datetime import date
from typing import Optional

from scripts.model_updater.fetchers.base_fetcher import BaseFetcher, ModelData


class GoogleFetcher(BaseFetcher):
    """Fetcher for Google Gemini models."""

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

        # List available models
        available_models = genai.list_models()

        # Filter for Gemini 2.5 models
        target_model_ids = [
            "gemini-2-5-flash-lite",
            "gemini-2-5-flash",
            "gemini-2-5-pro",
        ]

        models = []
        for model_info in available_models:
            # Extract base model name
            model_name = (
                model_info.name.split("/")[-1] if "/" in model_info.name else model_info.name
            )

            # Check if this is one of our target models
            for target_id in target_model_ids:
                if target_id in model_name or model_name.startswith("gemini-2.5"):
                    # Get specs from static knowledge
                    specs = self._get_static_model_specs(target_id)
                    if specs:
                        models.append(
                            ModelData(
                                model_id=target_id,
                                provider="google",
                                name=specs["name"],
                                api_identifier=specs["api_identifier"],
                                context_window_input=specs["context_window_input"],
                                context_window_output=specs.get("context_window_output"),
                                knowledge_cutoff=specs["knowledge_cutoff"],
                                release_date=date.fromisoformat(specs["release_date"]),
                                docs_url="https://ai.google.dev/gemini-api/docs/models/gemini",
                                capabilities=specs["capabilities"],
                                input_per_1m=specs["pricing"]["input_per_1m"],
                                output_per_1m=specs["pricing"]["output_per_1m"],
                                recommended_for=specs.get("recommended_for", []),
                                best_practices=specs.get("best_practices", []),
                                cost_tier=specs.get("cost_tier", "mid-tier"),
                                speed_tier=specs.get("speed_tier", "balanced"),
                                notes=specs.get("notes", ""),
                                source="google_api",
                            )
                        )
                    break

        # If no models found via API, fall back to static specs
        if not models:
            raise ValueError("No Gemini 2.5 models found via API")

        return models

    def _get_static_model_specs(self, model_id: str) -> Optional[dict]:
        """Get static model specifications.

        Args:
            model_id: Model identifier

        Returns:
            Dictionary of model specifications
        """
        specs = {
            "gemini-2-5-flash-lite": {
                "name": "Gemini 2.5 Flash Lite",
                "api_identifier": "gemini-2.5-flash-lite-latest",
                "context_window_input": 1000000,
                "context_window_output": 8192,
                "knowledge_cutoff": "August 2024",
                "release_date": "2025-02-01",
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
                    "input_per_1m": 0.075,
                    "output_per_1m": 0.30,
                },
                "cost_tier": "budget",
                "speed_tier": "fast",
                "recommended_for": [
                    "Ultra-high-volume applications",
                    "Cost-critical workloads",
                    "Real-time applications",
                    "Mobile and edge deployments",
                    "Batch processing at scale",
                ],
                "best_practices": [
                    "Leverage 1M token context for document analysis",
                    "Use for simple to moderate complexity tasks",
                    "Enable streaming for responsive UX",
                    "Good for high-frequency API calls",
                    "Monitor quality vs ultra-low cost",
                ],
                "notes": "Most cost-effective Gemini model. 1M token context window. Excellent for high-volume use cases.",
            },
            "gemini-2-5-flash": {
                "name": "Gemini 2.5 Flash",
                "api_identifier": "gemini-2.5-flash-latest",
                "context_window_input": 1000000,
                "context_window_output": 8192,
                "knowledge_cutoff": "August 2024",
                "release_date": "2025-02-01",
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
                    "Fast response requirements",
                    "Document analysis with 1M context",
                    "Multimodal workflows",
                    "Cost-conscious production deployments",
                ],
                "best_practices": [
                    "Leverage 1M token context window",
                    "Use for document understanding tasks",
                    "Enable function calling for structured outputs",
                    "Stream responses for better UX",
                    "Good balance of speed and capability",
                ],
                "notes": "Fast and cost-effective. 1M token context window. Strong vision and reasoning capabilities.",
            },
            "gemini-2-5-pro": {
                "name": "Gemini 2.5 Pro",
                "api_identifier": "gemini-2.5-pro-latest",
                "context_window_input": 2000000,
                "context_window_output": 8192,
                "knowledge_cutoff": "August 2024",
                "release_date": "2025-02-01",
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
                    "input_per_1m": 1.25,
                    "output_per_1m": 5.00,
                },
                "cost_tier": "mid-tier",
                "speed_tier": "balanced",
                "recommended_for": [
                    "Complex reasoning and analysis",
                    "Advanced multimodal tasks",
                    "Large document processing (2M context)",
                    "Code generation and review",
                    "Research and synthesis",
                ],
                "best_practices": [
                    "Leverage 2M token context for comprehensive analysis",
                    "Use for complex reasoning tasks",
                    "Enable function calling for tool integration",
                    "Good for multi-turn conversations",
                    "Balance of cost and capability",
                ],
                "notes": "Most capable Gemini model. 2M token context window. Industry-leading multimodal performance.",
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
        for model_id in ["gemini-2-5-flash-lite", "gemini-2-5-flash", "gemini-2-5-pro"]:
            specs = self._get_static_model_specs(model_id)
            if specs:
                models.append(
                    ModelData(
                        model_id=model_id,
                        provider="google",
                        name=specs["name"],
                        api_identifier=specs["api_identifier"],
                        context_window_input=specs["context_window_input"],
                        context_window_output=specs.get("context_window_output"),
                        knowledge_cutoff=specs["knowledge_cutoff"],
                        release_date=date.fromisoformat(specs["release_date"]),
                        docs_url="https://ai.google.dev/gemini-api/docs/models/gemini",
                        capabilities=specs["capabilities"],
                        input_per_1m=specs["pricing"]["input_per_1m"],
                        output_per_1m=specs["pricing"]["output_per_1m"],
                        recommended_for=specs.get("recommended_for", []),
                        best_practices=specs.get("best_practices", []),
                        cost_tier=specs.get("cost_tier", "mid-tier"),
                        speed_tier=specs.get("speed_tier", "balanced"),
                        notes=specs.get("notes", ""),
                        source="google_docs",
                    )
                )

        return models
