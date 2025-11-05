# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Scanner for finding model references throughout the codebase.

This module scans all relevant files in the repository and identifies
model references that need to be updated.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

from scripts.model_reference_updater import patterns

logger = logging.getLogger(__name__)


@dataclass
class FileReference:
    """Represents a model reference found in a file."""

    file_path: Path
    line_number: int
    line_content: str
    matched_text: str
    replacement: str
    pattern_desc: str


@dataclass
class ScanResults:
    """Results from scanning the repository."""

    files_scanned: int = 0
    files_with_references: int = 0
    total_references: int = 0
    outdated_references: int = 0
    current_references: int = 0
    references_by_file: Dict[Path, List[FileReference]] = field(default_factory=dict)
    references_by_pattern: Dict[str, int] = field(default_factory=dict)
    files_by_type: Dict[str, int] = field(default_factory=dict)

    def add_reference(self, ref: FileReference) -> None:
        """Add a reference to the results."""
        self.total_references += 1
        self.outdated_references += 1

        if ref.file_path not in self.references_by_file:
            self.references_by_file[ref.file_path] = []
            self.files_with_references += 1

        self.references_by_file[ref.file_path].append(ref)

        # Track by pattern
        pattern_key = f"{ref.matched_text} → {ref.replacement}"
        self.references_by_pattern[pattern_key] = self.references_by_pattern.get(pattern_key, 0) + 1


class ReferenceScanner:
    """Scans repository for model references."""

    def __init__(self, root_dir: Path):
        """Initialize scanner.

        Args:
            root_dir: Root directory of the repository
        """
        self.root_dir = root_dir
        self.results = ScanResults()

    def scan_repository(self) -> ScanResults:
        """Scan entire repository for model references.

        Returns:
            ScanResults with all found references
        """
        logger.info(f"Scanning repository: {self.root_dir}")

        # Find all scannable files
        files_to_scan = self._find_scannable_files()
        logger.info(f"Found {len(files_to_scan)} files to scan")

        # Scan each file
        for file_path in files_to_scan:
            self._scan_file(file_path)

        logger.info(
            f"Scan complete: {self.results.files_scanned} files scanned, "
            f"{self.results.outdated_references} outdated references found"
        )

        return self.results

    def _find_scannable_files(self) -> List[Path]:
        """Find all files that should be scanned.

        Returns:
            List of file paths to scan
        """
        scannable_files = []

        for path in self.root_dir.rglob("*"):
            # Skip directories
            if path.is_dir():
                continue

            # Skip excluded directories
            if any(excluded in path.parts for excluded in patterns.EXCLUDE_DIRS):
                continue

            # Check file extension
            if path.suffix in patterns.SCANNABLE_EXTENSIONS:
                scannable_files.append(path)

                # Track file type
                file_type = path.suffix
                self.results.files_by_type[file_type] = (
                    self.results.files_by_type.get(file_type, 0) + 1
                )

        return sorted(scannable_files)

    def _scan_file(self, file_path: Path) -> None:
        """Scan a single file for model references.

        Args:
            file_path: Path to file to scan
        """
        self.results.files_scanned += 1

        try:
            # Read file content
            content = file_path.read_text(encoding="utf-8")

            # Scan line by line for better precision
            lines = content.split("\n")
            for line_num, line in enumerate(lines, start=1):
                # Find outdated references
                refs = patterns.find_outdated_references(line)
                for matched_text, replacement, desc in refs:
                    ref = FileReference(
                        file_path=file_path,
                        line_number=line_num,
                        line_content=line.strip(),
                        matched_text=matched_text,
                        replacement=replacement,
                        pattern_desc=desc,
                    )
                    self.results.add_reference(ref)

        except Exception as e:
            logger.warning(f"Error scanning {file_path}: {e}")

    def get_top_files_needing_updates(self, limit: int = 10) -> List[tuple]:
        """Get top files with most outdated references.

        Args:
            limit: Maximum number of files to return

        Returns:
            List of (file_path, reference_count) tuples
        """
        file_counts = [(path, len(refs)) for path, refs in self.results.references_by_file.items()]
        return sorted(file_counts, key=lambda x: x[1], reverse=True)[:limit]

    def get_references_by_category(self) -> Dict[str, List[Path]]:
        """Categorize files with references by type.

        Returns:
            Dictionary mapping category to list of files
        """
        categories: Dict[str, List[Path]] = {
            "Python files": [],
            "Markdown docs": [],
            "YAML configs": [],
            "Prompt patterns": [],
            "Examples": [],
            "Tests": [],
            "Other": [],
        }

        for file_path in self.results.references_by_file.keys():
            if file_path.suffix == ".py":
                if "test" in file_path.name.lower():
                    categories["Tests"].append(file_path)
                else:
                    categories["Python files"].append(file_path)
            elif file_path.suffix == ".md":
                categories["Markdown docs"].append(file_path)
            elif file_path.suffix in {".yaml", ".yml"}:
                categories["YAML configs"].append(file_path)
            elif "prompts" in file_path.parts:
                categories["Prompt patterns"].append(file_path)
            elif "examples" in file_path.parts:
                categories["Examples"].append(file_path)
            else:
                categories["Other"].append(file_path)

        # Remove empty categories
        return {k: v for k, v in categories.items() if v}
