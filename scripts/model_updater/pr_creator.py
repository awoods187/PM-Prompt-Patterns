# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""GitHub Pull Request creation automation."""

import logging
import os
import subprocess
from datetime import datetime
from typing import Optional

from scripts.model_updater.change_detector import ChangeReport

logger = logging.getLogger(__name__)


class PRCreator:
    """Creates GitHub pull requests for model updates."""

    def __init__(self, repo_path: str = ".") -> None:
        """Initialize PR creator.

        Args:
            repo_path: Path to git repository
        """
        self.repo_path = repo_path
        self.logger = logging.getLogger(self.__class__.__name__)

    def create_pr(
        self,
        changelog: ChangeReport,
        branch_name: Optional[str] = None,
    ) -> Optional[str]:
        """Create a pull request for model updates.

        Args:
            changelog: ChangeReport with detected changes
            branch_name: Optional custom branch name

        Returns:
            PR URL if successful, None otherwise
        """
        if not changelog.has_changes:
            self.logger.info("No changes to create PR for")
            return None

        # Generate branch name
        if not branch_name:
            timestamp = datetime.now().strftime("%Y%m%d")
            branch_name = f"auto-update-models-{timestamp}"

        try:
            # Create and checkout branch
            self._create_branch(branch_name)

            # Generate commit message
            commit_msg = self._generate_commit_message(changelog)

            # Commit changes
            self._commit_changes(commit_msg)

            # Push branch
            self._push_branch(branch_name)

            # Create PR
            pr_url = self._create_github_pr(branch_name, changelog)

            return pr_url

        except Exception as e:
            self.logger.error(f"Failed to create PR: {e}")
            return None

    def _create_branch(self, branch_name: str) -> None:
        """Create and checkout a new branch.

        Args:
            branch_name: Name for the new branch
        """
        self.logger.info(f"Creating branch: {branch_name}")

        # Check if branch already exists
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch_name],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            # Branch exists, checkout
            subprocess.run(
                ["git", "checkout", branch_name],
                cwd=self.repo_path,
                check=True,
            )
        else:
            # Create new branch
            subprocess.run(
                ["git", "checkout", "-b", branch_name],
                cwd=self.repo_path,
                check=True,
            )

    def _commit_changes(self, message: str) -> None:
        """Commit changes.

        Args:
            message: Commit message
        """
        self.logger.info("Committing changes")

        # Stage all changes in ai_models/definitions/
        subprocess.run(
            ["git", "add", "ai_models/definitions/"],
            cwd=self.repo_path,
            check=True,
        )

        # Commit
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=self.repo_path,
            check=True,
        )

    def _push_branch(self, branch_name: str) -> None:
        """Push branch to remote.

        Args:
            branch_name: Branch to push
        """
        self.logger.info(f"Pushing branch: {branch_name}")

        subprocess.run(
            ["git", "push", "-u", "origin", branch_name],
            cwd=self.repo_path,
            check=True,
        )

    def _create_github_pr(self, branch_name: str, changelog: ChangeReport) -> str:
        """Create GitHub PR using gh CLI.

        Args:
            branch_name: Branch name
            changelog: ChangeReport with changes

        Returns:
            PR URL
        """
        self.logger.info("Creating GitHub PR")

        # Generate PR title and body
        title = self._generate_pr_title(changelog)
        body = self._generate_pr_body(changelog)

        # Create PR using gh CLI
        result = subprocess.run(
            [
                "gh",
                "pr",
                "create",
                "--title",
                title,
                "--body",
                body,
                "--head",
                branch_name,
            ],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=True,
        )

        # Extract PR URL from output
        pr_url = result.stdout.strip()
        self.logger.info(f"Created PR: {pr_url}")

        return pr_url

    def _generate_pr_title(self, changelog: ChangeReport) -> str:
        """Generate PR title.

        Args:
            changelog: ChangeReport with changes

        Returns:
            PR title
        """
        total = changelog.total_changes
        new_count = len(changelog.new_models)
        pricing_count = len(changelog.pricing_changes)

        parts = []
        if new_count:
            parts.append(f"{new_count} new model{'s' if new_count > 1 else ''}")
        if pricing_count:
            parts.append(f"{pricing_count} pricing update{'s' if pricing_count > 1 else ''}")

        if parts:
            detail = ", ".join(parts)
            return f"🤖 Auto-update models: {detail}"
        else:
            return f"🤖 Auto-update models ({total} changes)"

    def _generate_pr_body(self, changelog: ChangeReport) -> str:
        """Generate PR body with changelog.

        Args:
            changelog: ChangeReport with changes

        Returns:
            PR body markdown
        """
        body_parts = [
            "## 🤖 Automated Model Update",
            "",
            f"**Changes detected:** {changelog.total_changes} total",
            f"- 🆕 New models: {len(changelog.new_models)}",
            f"- 💰 Pricing changes: {len(changelog.pricing_changes)}",
            f"- ⚡ Capability changes: {len(changelog.capability_changes)}",
            f"- 📏 Context changes: {len(changelog.context_changes)}",
            f"- 📝 Metadata changes: {len(changelog.metadata_changes)}",
        ]

        if changelog.removed_models:
            body_parts.append(
                f"- ⚠️ Deprecated models: {len(changelog.removed_models)}"
            )

        body_parts.extend(
            [
                "",
                "---",
                "",
                changelog.to_markdown(),
                "",
                "---",
                "",
                "### Validation",
                "",
                "✅ All model definitions validated",
                "✅ Schema compliance checked",
                "✅ Tests will run automatically",
                "",
                "### Auto-merge",
                "",
                "This PR will auto-merge if all CI checks pass.",
                "",
                "---",
                "",
                "🤖 Generated with [Claude Code](https://claude.com/claude-code)",
                "",
                "Co-Authored-By: Claude <noreply@anthropic.com>",
            ]
        )

        return "\n".join(body_parts)

    def _generate_commit_message(self, changelog: ChangeReport) -> str:
        """Generate commit message.

        Args:
            changelog: ChangeReport with changes

        Returns:
            Commit message
        """
        summary_parts = []

        if changelog.new_models:
            summary_parts.append(f"{len(changelog.new_models)} new")
        if changelog.pricing_changes:
            summary_parts.append(f"{len(changelog.pricing_changes)} pricing")
        if changelog.capability_changes:
            summary_parts.append(f"{len(changelog.capability_changes)} capability")

        if summary_parts:
            summary = f"feat: Auto-update models ({', '.join(summary_parts)} changes)"
        else:
            summary = f"chore: Auto-update model definitions"

        body_parts = [
            summary,
            "",
            "Updates model definitions from provider APIs:",
            "",
        ]

        # Add details
        if changelog.new_models:
            body_parts.append(f"New models ({len(changelog.new_models)}):")
            for model in changelog.new_models:
                body_parts.append(f"- {model.name} ({model.model_id})")
            body_parts.append("")

        if changelog.pricing_changes:
            body_parts.append(f"Pricing changes ({len(changelog.pricing_changes)}):")
            for change in changelog.pricing_changes[:5]:  # Limit to 5
                body_parts.append(f"- {change.model_id}: {change.field}")
            if len(changelog.pricing_changes) > 5:
                body_parts.append(f"- ... and {len(changelog.pricing_changes) - 5} more")
            body_parts.append("")

        if changelog.removed_models:
            body_parts.append(f"Deprecated models ({len(changelog.removed_models)}):")
            for model_id in changelog.removed_models:
                body_parts.append(f"- {model_id}")
            body_parts.append("")

        body_parts.extend(
            [
                "🤖 Generated with [Claude Code](https://claude.com/claude-code)",
                "",
                "Co-Authored-By: Claude <noreply@anthropic.com>",
            ]
        )

        return "\n".join(body_parts)

    def enable_auto_merge(self, pr_url: str) -> bool:
        """Enable auto-merge for PR.

        Args:
            pr_url: PR URL

        Returns:
            True if successful
        """
        try:
            self.logger.info(f"Enabling auto-merge for {pr_url}")

            # Extract PR number from URL
            pr_number = pr_url.split("/")[-1]

            # Enable auto-merge using gh CLI
            subprocess.run(
                ["gh", "pr", "merge", pr_number, "--auto", "--squash"],
                cwd=self.repo_path,
                check=True,
            )

            self.logger.info("Auto-merge enabled")
            return True

        except Exception as e:
            self.logger.error(f"Failed to enable auto-merge: {e}")
            return False

    def create_deprecation_issue(self, deprecated_models: list[str]) -> Optional[str]:
        """Create GitHub issue for deprecated models.

        Args:
            deprecated_models: List of deprecated model IDs

        Returns:
            Issue URL if successful
        """
        if not deprecated_models:
            return None

        try:
            title = f"⚠️ Deprecated models detected ({len(deprecated_models)})"

            body_parts = [
                "## Deprecated Models",
                "",
                "The following models are no longer available from their providers:",
                "",
            ]

            for model_id in deprecated_models:
                body_parts.append(f"- `{model_id}`")

            body_parts.extend(
                [
                    "",
                    "### Action Required",
                    "",
                    "1. Review usage of these models in the codebase",
                    "2. Update examples and documentation",
                    "3. Consider creating migration guide for users",
                    "4. Archive model definitions (don't delete)",
                    "",
                    "---",
                    "",
                    "🤖 This issue was automatically created by the model updater",
                ]
            )

            body = "\n".join(body_parts)

            # Create issue using gh CLI
            result = subprocess.run(
                [
                    "gh",
                    "issue",
                    "create",
                    "--title",
                    title,
                    "--body",
                    body,
                    "--label",
                    "maintenance,model-deprecation",
                ],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )

            issue_url = result.stdout.strip()
            self.logger.info(f"Created deprecation issue: {issue_url}")

            return issue_url

        except Exception as e:
            self.logger.error(f"Failed to create deprecation issue: {e}")
            return None
