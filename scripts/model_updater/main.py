#!/usr/bin/env python3
# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Main orchestrator for automated model updates.

This script:
1. Fetches latest model data from all providers
2. Detects changes vs current definitions
3. Validates fetched data
4. Updates YAML files
5. Creates PR with changes (if running in CI)

Usage:
    python scripts/model_updater/main.py [--dry-run] [--no-pr]

Environment variables:
    ANTHROPIC_API_KEY: Optional, for Anthropic API access
    OPENAI_API_KEY: Optional, for OpenAI API access
    GOOGLE_API_KEY: Optional, for Google API access
    GITHUB_TOKEN: Required for PR creation
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Any

import yaml

from scripts.model_updater.change_detector import ChangeDetector
from scripts.model_updater.fetchers.anthropic_fetcher import AnthropicFetcher
from scripts.model_updater.fetchers.base_fetcher import ModelData
from scripts.model_updater.fetchers.google_fetcher import GoogleFetcher
from scripts.model_updater.fetchers.openai_fetcher import OpenAIFetcher
from scripts.model_updater.pr_creator import PRCreator
from scripts.model_updater.validator import ModelValidator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ModelUpdater:
    """Main orchestrator for model updates."""

    def __init__(self, repo_root: Path, dry_run: bool = False) -> None:
        """Initialize updater.

        Args:
            repo_root: Path to repository root
            dry_run: If True, don't write files or create PRs
        """
        self.repo_root = repo_root
        self.dry_run = dry_run
        self.definitions_dir = repo_root / "ai_models" / "definitions"

        # Initialize components
        self.fetchers = [
            AnthropicFetcher(),
            OpenAIFetcher(),
            GoogleFetcher(),
        ]
        self.change_detector = ChangeDetector()
        self.validator = ModelValidator()
        self.pr_creator = PRCreator(str(repo_root))

        logger.info(f"Initialized ModelUpdater (dry_run={dry_run})")

    def run(self, create_pr: bool = True) -> bool:
        """Run the full update process.

        Args:
            create_pr: If True, create PR for changes

        Returns:
            True if successful
        """
        logger.info("Starting model update process")

        try:
            # Step 1: Fetch models from all providers
            logger.info("Step 1: Fetching models from providers")
            fetched_models = self._fetch_all_models()

            if not fetched_models:
                logger.warning("No models fetched")
                return False

            logger.info(f"Fetched {len(fetched_models)} models")

            # Step 2: Validate fetched models
            logger.info("Step 2: Validating fetched models")
            validation_results = self.validator.validate_batch(fetched_models)

            # Check for validation failures
            invalid_models = [
                model_id for model_id, result in validation_results.items() if not result.is_valid
            ]
            if invalid_models:
                logger.error(
                    f"Validation failed for {len(invalid_models)} models: {invalid_models}"
                )
                # Continue with valid models only
                fetched_models = [
                    m for m in fetched_models if validation_results[m.model_id].is_valid
                ]

            summary = self.validator.get_validation_summary(validation_results)
            logger.info(f"Validation summary: {summary}")

            # Step 3: Load current models
            logger.info("Step 3: Loading current model definitions")
            current_models = self._load_current_models()
            logger.info(f"Loaded {len(current_models)} current models")

            # Step 4: Detect changes
            logger.info("Step 4: Detecting changes")
            changelog = self.change_detector.detect_changes(current_models, fetched_models)

            if not changelog.has_changes:
                logger.info("No changes detected. Models are up to date!")
                return True

            logger.info(f"Detected {changelog.total_changes} changes")

            # Print changelog
            print("\n" + "=" * 80)
            print(changelog.to_markdown())
            print("=" * 80 + "\n")

            # Step 5: Update YAML files
            if not self.dry_run:
                logger.info("Step 5: Updating YAML files")
                self._update_yaml_files(fetched_models)
                logger.info("YAML files updated")
            else:
                logger.info("Step 5: Skipping YAML update (dry-run mode)")

            # Step 6: Create deprecation issues if needed
            if changelog.removed_models and not self.dry_run:
                logger.info("Step 6: Creating deprecation issue")
                self.pr_creator.create_deprecation_issue(changelog.removed_models)

            # Step 7: Create PR
            if create_pr and not self.dry_run:
                logger.info("Step 7: Creating pull request")
                pr_url = self.pr_creator.create_pr(changelog)

                if pr_url:
                    logger.info(f"Pull request created: {pr_url}")

                    # Enable auto-merge
                    self.pr_creator.enable_auto_merge(pr_url)

                    # Set GitHub Actions output
                    self._set_github_output("changes_detected", "true")
                    self._set_github_output("pr_url", pr_url)
                else:
                    logger.error("Failed to create pull request")
                    return False
            else:
                logger.info("Step 7: Skipping PR creation")

            logger.info("Model update process completed successfully")
            return True

        except Exception as e:
            logger.error(f"Model update failed: {e}", exc_info=True)
            return False

    def _fetch_all_models(self) -> list[ModelData]:
        """Fetch models from all providers.

        Returns:
            List of all fetched models
        """
        all_models = []

        for fetcher in self.fetchers:
            try:
                logger.info(f"Fetching from {fetcher.provider_name}")
                models = fetcher.fetch_with_cache()
                logger.info(f"Fetched {len(models)} models from {fetcher.provider_name}")
                all_models.extend(models)
            except Exception as e:
                logger.error(f"Failed to fetch from {fetcher.provider_name}: {e}")
                # Continue with other providers

        return all_models

    def _load_current_models(self) -> dict[str, dict[str, Any]]:
        """Load current model definitions from YAML files.

        Returns:
            Dictionary mapping model_id to model definition
        """
        models = {}

        if not self.definitions_dir.exists():
            logger.warning(f"Definitions directory not found: {self.definitions_dir}")
            return models

        # Load all YAML files
        for yaml_file in self.definitions_dir.rglob("*.yaml"):
            try:
                with open(yaml_file) as f:
                    data = yaml.safe_load(f)

                if data and "model_id" in data:
                    models[data["model_id"]] = data
            except Exception as e:
                logger.warning(f"Failed to load {yaml_file}: {e}")

        return models

    def _update_yaml_files(self, models: list[ModelData]) -> None:
        """Update YAML files with fetched model data.

        Args:
            models: List of ModelData objects to write
        """
        for model in models:
            # Determine file path based on provider
            provider_dir = self.definitions_dir / model.provider
            provider_dir.mkdir(parents=True, exist_ok=True)

            yaml_file = provider_dir / f"{model.model_id}.yaml"

            # Convert to YAML dict
            yaml_dict = model.to_yaml_dict()

            # Add header comment
            header = f"# {model.name} Model Definition\n"
            header += f"# Last verified: {yaml_dict['metadata']['last_verified']}\n"
            header += f"# Source: {model.docs_url}\n\n"

            # Write file
            try:
                with open(yaml_file, "w") as f:
                    f.write(header)
                    yaml.dump(
                        yaml_dict,
                        f,
                        default_flow_style=False,
                        sort_keys=False,
                        allow_unicode=True,
                    )

                logger.info(f"Updated {yaml_file}")
            except Exception as e:
                logger.error(f"Failed to write {yaml_file}: {e}")

    def _set_github_output(self, name: str, value: str) -> None:
        """Set GitHub Actions output variable.

        Args:
            name: Output variable name
            value: Output value
        """
        import os

        github_output = os.getenv("GITHUB_OUTPUT")
        if github_output:
            with open(github_output, "a") as f:
                f.write(f"{name}={value}\n")


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(description="Automated model updater")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without making changes",
    )
    parser.add_argument(
        "--no-pr",
        action="store_true",
        help="Don't create pull request",
    )
    args = parser.parse_args()

    # Determine repo root (assumes script is in scripts/model_updater/)
    repo_root = Path(__file__).parent.parent.parent
    logger.info(f"Repository root: {repo_root}")

    # Run updater
    updater = ModelUpdater(repo_root, dry_run=args.dry_run)
    success = updater.run(create_pr=not args.no_pr)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
