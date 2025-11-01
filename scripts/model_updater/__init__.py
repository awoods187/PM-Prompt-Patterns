# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Automated model update system.

This package provides automated fetching, validation, and updating of
AI model definitions from provider APIs and documentation.
"""

from scripts.model_updater.change_detector import ChangeDetector, ChangeReport
from scripts.model_updater.fetchers.base_fetcher import BaseFetcher, ModelData
from scripts.model_updater.pr_creator import PRCreator
from scripts.model_updater.validator import ModelValidator, ValidationResult

__all__ = [
    "BaseFetcher",
    "ModelData",
    "ChangeDetector",
    "ChangeReport",
    "ModelValidator",
    "ValidationResult",
    "PRCreator",
]
