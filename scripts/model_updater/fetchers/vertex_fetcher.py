# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Google Vertex AI model fetcher."""

from typing import Optional

from scripts.model_updater.fetchers.base_fetcher import BaseFetcher, ModelData


class VertexFetcher(BaseFetcher):
    """Fetcher for Google Vertex AI models.

    Note: Vertex AI fetching is complex due to:
    - GCP project and region configuration
    - GCP credentials requirements
    - Multiple model providers on Vertex AI (Claude, PaLM, etc.)
    - Regional availability differences

    For now, this uses static specifications.
    Production implementation would use Vertex AI SDK with proper GCP config.
    """

    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return "vertex"

    def fetch_models(self) -> list[ModelData]:
        """Fetch Vertex AI models.

        Currently uses static specs. Production version would use Vertex AI SDK.

        Returns:
            List of ModelData objects
        """
        # For initial version, use static specs
        # Production would use Vertex AI SDK to list models
        return self.fetch_from_docs()

    def fetch_from_api(self) -> list[ModelData]:
        """Fetch models using Vertex AI API.

        Note: Requires GCP credentials and proper IAM permissions.

        Returns:
            List of ModelData objects
        """
        try:
            import anthropic  # noqa: F401
        except ImportError:
            raise ImportError("anthropic[vertex] package not installed")

        # This would require GCP credentials configuration
        # Commenting out for now as it's complex to set up
        raise NotImplementedError(
            "Vertex AI API fetching requires GCP credentials. " "Use static specs for now."
        )

        # Future implementation:
        # from anthropic import AnthropicVertex
        # client = AnthropicVertex(region="us-east5", project_id=project_id)
        # response = client.messages.create(...)
        # ...

    def fetch_from_docs(self) -> list[ModelData]:
        """Fetch models from static specifications.

        Returns:
            List of ModelData objects
        """
        self.logger.info("Using static Vertex AI model specifications")

        # Note: Vertex AI hosts multiple providers (Claude via Anthropic, PaLM/Gemini via Google)
        # For this project, we might not track Vertex AI separately
        # since we already track Anthropic and Google models directly

        # Return empty list for now - Vertex AI models are tracked via direct providers
        return []

    def _get_static_model_specs(self, model_id: str) -> Optional[dict]:
        """Get static model specifications for Vertex AI models.

        Args:
            model_id: Model identifier

        Returns:
            Dictionary of model specifications
        """
        # Vertex AI model specifications would go here
        # For now, return None as we track providers directly
        return None
