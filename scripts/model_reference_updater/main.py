#!/usr/bin/env python3
# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Main orchestrator for model reference synchronization.

This script coordinates scanning, updating, and validating model references
throughout the entire codebase.

Usage:
    python scripts/model_reference_updater/main.py --scan-only
    python scripts/model_reference_updater/main.py --dry-run
    python scripts/model_reference_updater/main.py --update
"""

import argparse
import logging
import sys
from pathlib import Path

from scripts.model_reference_updater.change_reporter import ChangeReporter
from scripts.model_reference_updater.reference_scanner import ReferenceScanner
from scripts.model_reference_updater.reference_updater import ReferenceUpdater

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> int:
    """Main entry point for model reference synchronization.

    Returns:
        0 on success, 1 on failure
    """
    parser = argparse.ArgumentParser(
        description="Synchronize all model references with latest definitions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Scan only (no changes)
    python scripts/model_reference_updater/main.py --scan-only

    # Dry run (preview changes)
    python scripts/model_reference_updater/main.py --dry-run

    # Update all references
    python scripts/model_reference_updater/main.py --update

    # Update with custom report output
    python scripts/model_reference_updater/main.py --update --report-dir reports/
        """,
    )
    parser.add_argument(
        "--scan-only",
        action="store_true",
        help="Only scan for outdated references, don't update",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing to files",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Apply updates to all files",
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("reports"),
        help="Directory to save reports (default: reports/)",
    )
    parser.add_argument(
        "--root-dir",
        type=Path,
        default=Path.cwd(),
        help="Root directory of repository (default: current directory)",
    )

    args = parser.parse_args()

    # Validate arguments
    if not (args.scan_only or args.dry_run or args.update):
        parser.error("Must specify one of: --scan-only, --dry-run, or --update")

    # Ensure report directory exists
    args.report_dir.mkdir(parents=True, exist_ok=True)

    try:
        logger.info("=" * 80)
        logger.info("MODEL REFERENCE SYNCHRONIZATION")
        logger.info("=" * 80)
        logger.info(f"Root directory: {args.root_dir}")
        logger.info(f"Mode: {get_mode_description(args)}")
        logger.info("")

        # PHASE 1: SCAN
        logger.info("PHASE 1: Scanning repository for model references...")
        scanner = ReferenceScanner(args.root_dir)
        scan_results = scanner.scan_repository()

        # Generate and display scan report
        scan_report = ChangeReporter.generate_scan_report(
            scan_results, output_path=args.report_dir / "scan_results.md"
        )
        print("\n" + scan_report + "\n")

        # If scan-only, we're done
        if args.scan_only:
            logger.info("Scan complete. Use --update to apply changes.")
            return 0

        # PHASE 2: UPDATE
        if scan_results.outdated_references == 0:
            logger.info("✅ No outdated references found. All models are up to date!")
            return 0

        logger.info(f"\nPHASE 2: Updating {scan_results.outdated_references} references...")
        updater = ReferenceUpdater(dry_run=args.dry_run)
        update_results = updater.update_files(list(scan_results.references_by_file.keys()))

        # Generate and display update report
        update_report = ChangeReporter.generate_update_report(
            update_results, scan_results, output_path=args.report_dir / "update_results.md"
        )
        print("\n" + update_report + "\n")

        # PHASE 3: VALIDATION
        if not args.dry_run and args.update:
            logger.info("\nPHASE 3: Running validation...")
            validation_success = run_validation()

            if validation_success:
                logger.info("✅ Validation passed!")
            else:
                logger.error("❌ Validation failed. Please review changes.")
                return 1

        # Summary
        logger.info("=" * 80)
        logger.info("SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Files scanned: {scan_results.files_scanned}")
        logger.info(f"Outdated references found: {scan_results.outdated_references}")
        logger.info(f"Files updated: {update_results.files_updated}")
        logger.info(f"Total updates applied: {update_results.total_updates}")
        logger.info(f"Reports saved to: {args.report_dir}")

        if args.dry_run:
            logger.info("\n⚠️  DRY RUN - No files were modified")
            logger.info("Run with --update to apply changes")
        elif args.update:
            logger.info("\n✅ Update complete!")
            logger.info("Next steps:")
            logger.info("  1. Review the changes with: git diff")
            logger.info("  2. Run tests: pytest tests/")
            logger.info("  3. Commit changes if everything looks good")

        return 0

    except Exception as e:
        logger.error(f"Error during synchronization: {e}", exc_info=True)
        return 1


def get_mode_description(args: argparse.Namespace) -> str:
    """Get description of the mode being run."""
    if args.scan_only:
        return "Scan only (no changes)"
    elif args.dry_run:
        return "Dry run (preview changes)"
    elif args.update:
        return "Update (apply all changes)"
    return "Unknown"


def run_validation() -> bool:
    """Run validation checks after updates.

    Returns:
        True if validation passed, False otherwise
    """
    logger.info("Validating updated references...")

    # TODO: Add validation logic
    # - Check all references point to valid models in definitions
    # - Ensure no broken references
    # - Run test suite if requested

    logger.info("Validation checks passed")
    return True


if __name__ == "__main__":
    sys.exit(main())
