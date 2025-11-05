# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Report generator for model reference updates.

This module generates comprehensive reports of scans and updates.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

from scripts.model_reference_updater.reference_scanner import ScanResults
from scripts.model_reference_updater.reference_updater import UpdateResults

logger = logging.getLogger(__name__)


class ChangeReporter:
    """Generates reports for model reference updates."""

    @staticmethod
    def generate_scan_report(results: ScanResults, output_path: Optional[Path] = None) -> str:
        """Generate report from scan results.

        Args:
            results: Scan results to report
            output_path: Optional path to save report

        Returns:
            Formatted report string
        """
        report_lines = [
            "# Model Reference Synchronization - Scan Report",
            "",
            "## Scan Summary",
            f"- **Files scanned**: {results.files_scanned:,}",
            f"- **Files with model references**: {results.files_with_references:,}",
            f"- **Total references found**: {results.total_references:,}",
            f"- **Outdated references**: {results.outdated_references:,}",
            "",
        ]

        # Files by type
        if results.files_by_type:
            report_lines.extend(
                [
                    "## Files Scanned by Type",
                    "",
                ]
            )
            for file_type, count in sorted(results.files_by_type.items()):
                report_lines.append(f"- {file_type}: {count} files")
            report_lines.append("")

        # Outdated references by pattern
        if results.references_by_pattern:
            report_lines.extend(
                [
                    "## Outdated References by Pattern",
                    "",
                    "| Pattern | Count |",
                    "|---------|-------|",
                ]
            )
            sorted_patterns = sorted(
                results.references_by_pattern.items(), key=lambda x: x[1], reverse=True
            )
            for pattern, count in sorted_patterns[:20]:  # Top 20
                # Escape pipes in pattern for markdown table
                pattern_escaped = pattern.replace("|", "\\|")
                report_lines.append(f"| `{pattern_escaped}` | {count} |")
            report_lines.append("")

        # Top files needing updates
        if results.references_by_file:
            report_lines.extend(
                [
                    "## Top Files Requiring Updates",
                    "",
                    "| File | References |",
                    "|------|------------|",
                ]
            )
            sorted_files = sorted(
                results.references_by_file.items(), key=lambda x: len(x[1]), reverse=True
            )
            for file_path, refs in sorted_files[:15]:  # Top 15
                rel_path = file_path.relative_to(file_path.parents[len(file_path.parents) - 1])
                report_lines.append(f"| `{rel_path}` | {len(refs)} |")
            report_lines.append("")

        # Category breakdown
        # Categorize files by type
        categories: Dict[str, List[Path]] = {
            "Python files": [],
            "Markdown docs": [],
            "YAML configs": [],
            "Prompt patterns": [],
            "Examples": [],
            "Tests": [],
            "Other": [],
        }

        for file_path in results.references_by_file.keys():
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

        # Count references per category
        category_ref_counts = {}
        for category, files in categories.items():
            total_refs = sum(len(results.references_by_file.get(f, [])) for f in files)
            if total_refs > 0:
                category_ref_counts[category] = (len(files), total_refs)

        if category_ref_counts:
            report_lines.extend(
                [
                    "## Outdated References by Category",
                    "",
                    "| Category | Files | References |",
                    "|----------|-------|------------|",
                ]
            )
            for category, (file_count, ref_count) in sorted(
                category_ref_counts.items(), key=lambda x: x[1][1], reverse=True
            ):
                report_lines.append(f"| {category} | {file_count} | {ref_count} |")
            report_lines.append("")

        report = "\n".join(report_lines)

        # Save to file if requested
        if output_path:
            output_path.write_text(report, encoding="utf-8")
            logger.info(f"Scan report saved to {output_path}")

        return report

    @staticmethod
    def generate_update_report(
        update_results: UpdateResults, scan_results: ScanResults, output_path: Optional[Path] = None
    ) -> str:
        """Generate report from update results.

        Args:
            update_results: Update results to report
            scan_results: Original scan results for comparison
            output_path: Optional path to save report

        Returns:
            Formatted report string
        """
        report_lines = [
            "# Model Reference Synchronization - Update Report",
            "",
            "## Update Summary",
            f"- **Files updated**: {update_results.files_updated:,}",
            f"- **Total references updated**: {update_results.total_updates:,}",
            (
                f"- **Update success rate**: {(update_results.files_updated / scan_results.files_with_references * 100):.1f}%"
                if scan_results.files_with_references > 0
                else "N/A"
            ),
            "",
        ]

        # Updates by pattern
        if update_results.updates_by_pattern:
            report_lines.extend(
                [
                    "## Updates by Model Transition",
                    "",
                    "| Transition | Count |",
                    "|------------|-------|",
                ]
            )
            sorted_updates = sorted(
                update_results.updates_by_pattern.items(), key=lambda x: x[1], reverse=True
            )
            for pattern, count in sorted_updates[:20]:
                pattern_escaped = pattern.replace("|", "\\|")
                report_lines.append(f"| `{pattern_escaped}` | {count} |")
            report_lines.append("")

        # Errors if any
        if update_results.failed_files:
            report_lines.extend(
                [
                    "## Errors",
                    "",
                    f"Failed to update {len(update_results.failed_files)} files:",
                    "",
                ]
            )
            for file_path in update_results.failed_files:
                report_lines.append(f"- `{file_path}`")
            report_lines.append("")

            if update_results.errors:
                report_lines.extend(
                    [
                        "### Error Details",
                        "",
                    ]
                )
                for error in update_results.errors:
                    report_lines.append(f"- {error}")
                report_lines.append("")

        report = "\n".join(report_lines)

        # Save to file if requested
        if output_path:
            output_path.write_text(report, encoding="utf-8")
            logger.info(f"Update report saved to {output_path}")

        return report

    @staticmethod
    def generate_combined_report(
        scan_results: ScanResults, update_results: UpdateResults, output_path: Optional[Path] = None
    ) -> str:
        """Generate combined scan and update report.

        Args:
            scan_results: Scan results
            update_results: Update results
            output_path: Optional path to save report

        Returns:
            Formatted report string
        """
        scan_report = ChangeReporter.generate_scan_report(scan_results)
        update_report = ChangeReporter.generate_update_report(update_results, scan_results)

        combined = f"{scan_report}\n\n---\n\n{update_report}"

        if output_path:
            output_path.write_text(combined, encoding="utf-8")
            logger.info(f"Combined report saved to {output_path}")

        return combined
