# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Updater for model references throughout the codebase.

This module applies updates to files, replacing outdated model references
with current versions.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

from scripts.model_reference_updater import patterns

logger = logging.getLogger(__name__)


@dataclass
class UpdateResults:
    """Results from updating model references."""

    files_updated: int = 0
    total_updates: int = 0
    updates_by_pattern: Dict[str, int] = field(default_factory=dict)
    failed_files: List[Path] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class ReferenceUpdater:
    """Updates model references in files."""

    def __init__(self, dry_run: bool = False):
        """Initialize updater.

        Args:
            dry_run: If True, don't actually write changes to files
        """
        self.dry_run = dry_run
        self.results = UpdateResults()

    def update_file(self, file_path: Path) -> int:
        """Update all model references in a single file.

        Args:
            file_path: Path to file to update

        Returns:
            Number of references updated
        """
        try:
            # Read file content
            original_content = file_path.read_text(encoding="utf-8")
            updated_content = original_content
            updates_made = 0

            # Apply each pattern replacement
            for pattern, replacement, desc in patterns.COMPILED_PATTERNS:
                matches = list(pattern.finditer(updated_content))
                if matches:
                    # Replace all occurrences
                    updated_content = pattern.sub(replacement, updated_content)
                    num_replaced = len(matches)
                    updates_made += num_replaced

                    # Track the update
                    pattern_key = f"{matches[0].group(0)} → {replacement}"
                    self.results.updates_by_pattern[pattern_key] = (
                        self.results.updates_by_pattern.get(pattern_key, 0) + num_replaced
                    )

            # Write updated content if changes were made
            if updates_made > 0:
                if not self.dry_run:
                    file_path.write_text(updated_content, encoding="utf-8")

                self.results.files_updated += 1
                self.results.total_updates += updates_made
                logger.info(f"Updated {file_path}: {updates_made} references")

            return updates_made

        except Exception as e:
            logger.error(f"Error updating {file_path}: {e}")
            self.results.failed_files.append(file_path)
            self.results.errors.append(f"{file_path}: {str(e)}")
            return 0

    def update_files(self, file_paths: List[Path]) -> UpdateResults:
        """Update model references in multiple files.

        Args:
            file_paths: List of file paths to update

        Returns:
            UpdateResults with summary of updates
        """
        logger.info(f"{'[DRY RUN] ' if self.dry_run else ''}Updating {len(file_paths)} files")

        for file_path in file_paths:
            self.update_file(file_path)

        logger.info(
            f"Update complete: {self.results.files_updated} files updated, "
            f"{self.results.total_updates} total updates"
        )

        return self.results

    def preview_changes(self, file_path: Path, max_lines: int = 5) -> str:
        """Preview changes that would be made to a file.

        Args:
            file_path: Path to file
            max_lines: Maximum number of changed lines to show

        Returns:
            String showing preview of changes
        """
        try:
            original_content = file_path.read_text(encoding="utf-8")
            updated_content = original_content

            # Apply patterns
            for pattern, replacement, _ in patterns.COMPILED_PATTERNS:
                updated_content = pattern.sub(replacement, updated_content)

            if original_content == updated_content:
                return "No changes"

            # Show diff
            original_lines = original_content.split("\n")
            updated_lines = updated_content.split("\n")

            preview = []
            changes_shown = 0

            for i, (orig, upd) in enumerate(zip(original_lines, updated_lines), start=1):
                if orig != upd and changes_shown < max_lines:
                    preview.append(f"Line {i}:")
                    preview.append(f"  - {orig}")
                    preview.append(f"  + {upd}")
                    changes_shown += 1

            if changes_shown < len([o for o, u in zip(original_lines, updated_lines) if o != u]):
                remaining = (
                    len([o for o, u in zip(original_lines, updated_lines) if o != u])
                    - changes_shown
                )
                preview.append(f"  ... and {remaining} more changes")

            return "\n".join(preview)

        except Exception as e:
            return f"Error previewing: {e}"
