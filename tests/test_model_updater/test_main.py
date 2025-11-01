# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
Tests for module: scripts/model_updater/main.py

Coverage Target: 80%
Current Coverage: 0%
Priority: CRITICAL - Main orchestrator, business logic
"""

from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from scripts.model_updater.change_detector import ChangeReport
from scripts.model_updater.fetchers.base_fetcher import ModelData
from scripts.model_updater.main import ModelUpdater
from scripts.model_updater.validator import ValidationResult


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def temp_repo_root(tmp_path: Path) -> Path:
    """Create temporary repository structure."""
    definitions_dir = tmp_path / "ai_models" / "definitions" / "anthropic"
    definitions_dir.mkdir(parents=True)

    # Create a sample YAML file
    yaml_file = definitions_dir / "test-model.yaml"
    yaml_file.write_text(
        """model_id: test-model
provider: test
name: Test Model
api_identifier: test-v1
metadata:
  context_window_input: 100000
  context_window_output: 4096
  knowledge_cutoff: "Jan 2025"
  release_date: "2025-01-01"
  last_verified: "2025-01-01"
  docs_url: "https://example.com"
capabilities:
  - text_input
  - text_output
pricing:
  input_per_1m: 1.0
  output_per_1m: 3.0
optimization:
  recommended_for: []
  best_practices: []
  cost_tier: mid-tier
  speed_tier: balanced
notes: "Test model"
"""
    )

    return tmp_path


@pytest.fixture
def mock_fetcher() -> Mock:
    """Create mock fetcher."""
    fetcher = Mock()
    fetcher.provider_name = "test"
    fetcher.fetch_with_cache.return_value = [
        ModelData(
            model_id="test-model",
            provider="test",
            name="Test Model",
            api_identifier="test-v1",
            context_window_input=100000,
            context_window_output=4096,
            knowledge_cutoff="Jan 2025",
            release_date=date(2025, 1, 1),
            docs_url="https://example.com",
            capabilities=["text_input", "text_output"],
            input_per_1m=1.0,
            output_per_1m=3.0,
            cost_tier="mid-tier",
            speed_tier="balanced",
        )
    ]
    return fetcher


@pytest.fixture
def sample_model_data() -> ModelData:
    """Create sample ModelData for testing."""
    return ModelData(
        model_id="new-model",
        provider="test",
        name="New Model",
        api_identifier="new-model-v1",
        context_window_input=128000,
        context_window_output=None,
        knowledge_cutoff="Jan 2025",
        release_date=date(2025, 1, 1),
        docs_url="https://example.com/new",
        capabilities=["text_input", "text_output", "vision"],
        input_per_1m=2.0,
        output_per_1m=6.0,
        cost_tier="mid-tier",
        speed_tier="fast",
        notes="New test model",
    )


# ============================================================================
# MODEL UPDATER INITIALIZATION TESTS
# ============================================================================


class TestModelUpdaterInitialization:
    """Test suite for ModelUpdater initialization."""

    def test_init_with_valid_path_succeeds(self, temp_repo_root: Path) -> None:
        """Test successful initialization with valid repository path."""
        updater = ModelUpdater(temp_repo_root, dry_run=False)

        assert updater.repo_root == temp_repo_root
        assert updater.dry_run is False
        assert updater.definitions_dir == temp_repo_root / "ai_models" / "definitions"
        assert len(updater.fetchers) == 3  # Anthropic, OpenAI, Google

    def test_init_with_dry_run_mode_sets_flag(self, temp_repo_root: Path) -> None:
        """Test that dry_run mode is properly configured."""
        updater = ModelUpdater(temp_repo_root, dry_run=True)

        assert updater.dry_run is True

    def test_init_creates_component_instances(self, temp_repo_root: Path) -> None:
        """Test that all required components are instantiated."""
        updater = ModelUpdater(temp_repo_root)

        assert updater.change_detector is not None
        assert updater.validator is not None
        assert updater.pr_creator is not None
        assert len(updater.fetchers) > 0


# ============================================================================
# MODEL FETCHING TESTS
# ============================================================================


class TestModelFetching:
    """Test suite for model fetching functionality."""

    def test_fetch_all_models_returns_combined_results(
        self, temp_repo_root: Path, mock_fetcher: Mock
    ) -> None:
        """Test that fetching aggregates results from all providers."""
        updater = ModelUpdater(temp_repo_root)
        updater.fetchers = [mock_fetcher]

        models = updater._fetch_all_models()

        assert len(models) == 1
        assert models[0].model_id == "test-model"
        mock_fetcher.fetch_with_cache.assert_called_once()

    def test_fetch_all_models_handles_fetcher_failure_gracefully(
        self, temp_repo_root: Path
    ) -> None:
        """Test that fetcher failures don't break the entire process."""
        failing_fetcher = Mock()
        failing_fetcher.provider_name = "failing"
        failing_fetcher.fetch_with_cache.side_effect = Exception("API Error")

        working_fetcher = Mock()
        working_fetcher.provider_name = "working"
        working_fetcher.fetch_with_cache.return_value = [
            ModelData(
                model_id="working-model",
                provider="working",
                name="Working Model",
                api_identifier="working-v1",
                context_window_input=100000,
                context_window_output=None,
                knowledge_cutoff="Jan 2025",
                release_date=date(2025, 1, 1),
                docs_url="https://example.com",
                capabilities=["text_input", "text_output"],
                input_per_1m=1.0,
                output_per_1m=3.0,
                cost_tier="mid-tier",
                speed_tier="balanced",
            )
        ]

        updater = ModelUpdater(temp_repo_root)
        updater.fetchers = [failing_fetcher, working_fetcher]

        models = updater._fetch_all_models()

        # Should return models from working fetcher despite failure
        assert len(models) == 1
        assert models[0].model_id == "working-model"

    def test_fetch_all_models_returns_empty_on_all_failures(
        self, temp_repo_root: Path
    ) -> None:
        """Test that empty list is returned when all fetchers fail."""
        failing_fetcher = Mock()
        failing_fetcher.provider_name = "failing"
        failing_fetcher.fetch_with_cache.side_effect = Exception("API Error")

        updater = ModelUpdater(temp_repo_root)
        updater.fetchers = [failing_fetcher]

        models = updater._fetch_all_models()

        assert models == []


# ============================================================================
# MODEL LOADING TESTS
# ============================================================================


class TestModelLoading:
    """Test suite for loading current model definitions."""

    def test_load_current_models_returns_yaml_dict(self, temp_repo_root: Path) -> None:
        """Test loading current models from YAML files."""
        updater = ModelUpdater(temp_repo_root)

        models = updater._load_current_models()

        assert "test-model" in models
        assert models["test-model"]["provider"] == "test"
        assert models["test-model"]["name"] == "Test Model"

    def test_load_current_models_handles_missing_directory(
        self, tmp_path: Path
    ) -> None:
        """Test graceful handling when definitions directory doesn't exist."""
        updater = ModelUpdater(tmp_path)

        models = updater._load_current_models()

        assert models == {}

    def test_load_current_models_skips_invalid_yaml(self, temp_repo_root: Path) -> None:
        """Test that invalid YAML files are skipped gracefully."""
        definitions_dir = temp_repo_root / "ai_models" / "definitions" / "test"
        definitions_dir.mkdir(parents=True)

        # Create invalid YAML file
        invalid_file = definitions_dir / "invalid.yaml"
        invalid_file.write_text("invalid: yaml: content:")

        updater = ModelUpdater(temp_repo_root)

        models = updater._load_current_models()

        # Should still load the valid test-model
        assert "test-model" in models


# ============================================================================
# YAML FILE UPDATE TESTS
# ============================================================================


class TestYAMLFileUpdates:
    """Test suite for updating YAML files."""

    def test_update_yaml_files_creates_new_files(
        self, temp_repo_root: Path, sample_model_data: ModelData
    ) -> None:
        """Test that new YAML files are created for new models."""
        updater = ModelUpdater(temp_repo_root, dry_run=False)

        updater._update_yaml_files([sample_model_data])

        yaml_file = temp_repo_root / "ai_models" / "definitions" / "test" / "new-model.yaml"
        assert yaml_file.exists()

        content = yaml_file.read_text()
        assert "model_id: new-model" in content
        assert "provider: test" in content
        assert "New Model" in content

    def test_update_yaml_files_updates_existing_files(
        self, temp_repo_root: Path
    ) -> None:
        """Test that existing YAML files are updated."""
        # Create model with updated data
        updated_model = ModelData(
            model_id="test-model",
            provider="test",
            name="Test Model Updated",
            api_identifier="test-v2",
            context_window_input=200000,  # Updated
            context_window_output=8192,
            knowledge_cutoff="Feb 2025",  # Updated
            release_date=date(2025, 1, 1),
            docs_url="https://example.com",
            capabilities=["text_input", "text_output", "vision"],  # Added vision
            input_per_1m=1.5,  # Updated
            output_per_1m=4.0,  # Updated
            cost_tier="mid-tier",
            speed_tier="balanced",
            notes="Updated test model",
        )

        updater = ModelUpdater(temp_repo_root, dry_run=False)

        updater._update_yaml_files([updated_model])

        yaml_file = (
            temp_repo_root / "ai_models" / "definitions" / "test" / "test-model.yaml"
        )
        content = yaml_file.read_text()

        assert "context_window_input: 200000" in content
        assert "vision" in content
        assert "input_per_1m: 1.5" in content


# ============================================================================
# MAIN RUN WORKFLOW TESTS
# ============================================================================


class TestMainRunWorkflow:
    """Test suite for the main run() workflow."""

    @patch("scripts.model_updater.main.ModelUpdater._fetch_all_models")
    @patch("scripts.model_updater.main.ModelUpdater._load_current_models")
    def test_run_returns_true_when_no_changes_detected(
        self,
        mock_load: Mock,
        mock_fetch: Mock,
        temp_repo_root: Path,
    ) -> None:
        """Test that run returns True when no changes detected."""
        # Setup mocks
        mock_fetch.return_value = [
            ModelData(
                model_id="test-model",
                provider="test",
                name="Test Model",
                api_identifier="test-v1",
                context_window_input=100000,
                context_window_output=4096,
                knowledge_cutoff="Jan 2025",
                release_date=date(2025, 1, 1),
                docs_url="https://example.com",
                capabilities=["text_input", "text_output"],
                input_per_1m=1.0,
                output_per_1m=3.0,
                cost_tier="mid-tier",
                speed_tier="balanced",
            )
        ]

        mock_load.return_value = {
            "test-model": {
                "model_id": "test-model",
                "provider": "test",
                "metadata": {
                    "context_window_input": 100000,
                    "context_window_output": 4096,
                },
                "pricing": {"input_per_1m": 1.0, "output_per_1m": 3.0},
                "capabilities": ["text_input", "text_output"],
            }
        }

        updater = ModelUpdater(temp_repo_root, dry_run=True)
        result = updater.run(create_pr=False)

        assert result is True

    @patch("scripts.model_updater.main.ModelUpdater._fetch_all_models")
    def test_run_returns_false_when_no_models_fetched(
        self, mock_fetch: Mock, temp_repo_root: Path
    ) -> None:
        """Test that run returns False when fetching fails."""
        mock_fetch.return_value = []

        updater = ModelUpdater(temp_repo_root)
        result = updater.run(create_pr=False)

        assert result is False

    @patch("scripts.model_updater.main.ModelUpdater._fetch_all_models")
    def test_run_handles_validation_failures(
        self, mock_fetch: Mock, temp_repo_root: Path
    ) -> None:
        """Test that invalid models are filtered out but run continues."""
        # Return model with invalid data
        mock_fetch.return_value = [
            ModelData(
                model_id="",  # Invalid - empty
                provider="test",
                name="",  # Invalid - empty
                api_identifier="test",
                context_window_input=-1,  # Invalid - negative
                context_window_output=None,
                knowledge_cutoff="",
                release_date=date.today(),
                docs_url="",  # Invalid - empty
                capabilities=[],  # Invalid - empty
                input_per_1m=-1.0,  # Invalid - negative
                output_per_1m=-1.0,  # Invalid - negative
                cost_tier="invalid",  # Invalid tier
                speed_tier="invalid",  # Invalid tier
            )
        ]

        updater = ModelUpdater(temp_repo_root, dry_run=True)
        result = updater.run(create_pr=False)

        # Should handle gracefully - detects existing model as removed
        # because no valid fetched models match
        assert result is True


# ============================================================================
# GITHUB OUTPUT TESTS
# ============================================================================


class TestGitHubOutput:
    """Test suite for GitHub Actions output."""

    def test_set_github_output_writes_to_file_when_env_set(
        self, temp_repo_root: Path, tmp_path: Path
    ) -> None:
        """Test that GitHub output is written when GITHUB_OUTPUT is set."""
        output_file = tmp_path / "github_output.txt"

        with patch.dict("os.environ", {"GITHUB_OUTPUT": str(output_file)}):
            updater = ModelUpdater(temp_repo_root)
            updater._set_github_output("test_var", "test_value")

            assert output_file.exists()
            content = output_file.read_text()
            assert "test_var=test_value\n" in content

    def test_set_github_output_handles_missing_env_gracefully(
        self, temp_repo_root: Path
    ) -> None:
        """Test that missing GITHUB_OUTPUT env var is handled gracefully."""
        with patch.dict("os.environ", {}, clear=True):
            updater = ModelUpdater(temp_repo_root)
            # Should not raise
            updater._set_github_output("test_var", "test_value")


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================


class TestErrorHandling:
    """Test suite for error handling."""

    @patch("scripts.model_updater.main.ModelUpdater._fetch_all_models")
    def test_run_handles_exception_gracefully(
        self, mock_fetch: Mock, temp_repo_root: Path
    ) -> None:
        """Test that exceptions in run are caught and logged."""
        mock_fetch.side_effect = Exception("Unexpected error")

        updater = ModelUpdater(temp_repo_root, dry_run=True)
        result = updater.run(create_pr=False)

        assert result is False

    @patch("scripts.model_updater.main.ModelUpdater._fetch_all_models")
    @patch("scripts.model_updater.main.ModelUpdater._load_current_models")
    @patch("scripts.model_updater.main.PRCreator.create_deprecation_issue")
    def test_run_creates_deprecation_issue_for_removed_models(
        self,
        mock_create_issue: Mock,
        mock_load: Mock,
        mock_fetch: Mock,
        temp_repo_root: Path,
    ) -> None:
        """Test that deprecation issues are created for removed models."""
        # Setup: one new model, one existing model removed
        mock_fetch.return_value = [
            ModelData(
                model_id="new-model",
                provider="test",
                name="New Model",
                api_identifier="new-v1",
                context_window_input=100000,
                context_window_output=None,
                knowledge_cutoff="Jan 2025",
                release_date=date(2025, 1, 1),
                docs_url="https://example.com",
                capabilities=["text_input", "text_output"],
                input_per_1m=1.0,
                output_per_1m=3.0,
                cost_tier="mid-tier",
                speed_tier="balanced",
            )
        ]
        mock_load.return_value = {
            "removed-model": {
                "model_id": "removed-model",
                "provider": "test",
                "metadata": {
                    "context_window_input": 100000,
                },
                "pricing": {"input_per_1m": 1.0},
                "capabilities": ["text_input"],
            }
        }

        updater = ModelUpdater(temp_repo_root, dry_run=False)
        result = updater.run(create_pr=False)

        # Should create deprecation issue for removed model
        mock_create_issue.assert_called_once_with(["removed-model"])
        assert result is True


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


class TestEndToEndWorkflow:
    """Integration tests for complete workflow."""

    @patch("scripts.model_updater.main.PRCreator.create_pr")
    @patch("scripts.model_updater.main.PRCreator.enable_auto_merge")
    @patch("scripts.model_updater.main.ModelUpdater._fetch_all_models")
    @patch("scripts.model_updater.main.ModelUpdater._load_current_models")
    def test_full_workflow_with_changes_creates_pr(
        self,
        mock_load: Mock,
        mock_fetch: Mock,
        mock_auto_merge: Mock,
        mock_create_pr: Mock,
        temp_repo_root: Path,
    ) -> None:
        """Test complete workflow when changes are detected."""
        # Setup: fetched model has different pricing
        mock_fetch.return_value = [
            ModelData(
                model_id="test-model",
                provider="test",
                name="Test Model",
                api_identifier="test-v1",
                context_window_input=100000,
                context_window_output=4096,
                knowledge_cutoff="Jan 2025",
                release_date=date(2025, 1, 1),
                docs_url="https://example.com",
                capabilities=["text_input", "text_output"],
                input_per_1m=2.0,  # Changed from 1.0
                output_per_1m=6.0,  # Changed from 3.0
                cost_tier="mid-tier",
                speed_tier="balanced",
            )
        ]

        mock_load.return_value = {
            "test-model": {
                "model_id": "test-model",
                "provider": "test",
                "metadata": {
                    "context_window_input": 100000,
                    "context_window_output": 4096,
                },
                "pricing": {"input_per_1m": 1.0, "output_per_1m": 3.0},
                "capabilities": ["text_input", "text_output"],
            }
        }

        mock_create_pr.return_value = "https://github.com/test/repo/pull/1"

        updater = ModelUpdater(temp_repo_root, dry_run=False)
        result = updater.run(create_pr=True)

        assert result is True
        mock_create_pr.assert_called_once()
        mock_auto_merge.assert_called_once_with("https://github.com/test/repo/pull/1")
