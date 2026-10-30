# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Regex patterns for finding and updating model references.

This module defines comprehensive patterns for finding all model references
throughout the codebase, including outdated patterns that need migration.
"""

import re
from typing import List, Pattern, Tuple

# ============================================================================
# CURRENT MODELS (Source of Truth from ai_models/definitions/)
# ============================================================================

CURRENT_MODELS = {
    "anthropic": {
        "model_ids": [
            "claude-fable-5-1",
            "claude-opus-5-5",
            "claude-sonnet-5-5",
            "claude-haiku-5-5",
        ],
        "api_identifiers": [
            "claude-fable-5-1",
            "claude-opus-5-5",
            "claude-sonnet-5-5",
            "claude-haiku-5-5",
        ],
        "names": ["Claude Fable 5.1", "Claude Opus 5.5", "Claude Sonnet 5.5", "Claude Haiku 5.5"],
    },
    "openai": {
        "model_ids": ["gpt-6-astra", "gpt-6.1-sol", "gpt-6.1-terra", "gpt-6-luna"],
        "api_identifiers": ["gpt-6-astra", "gpt-6.1-sol", "gpt-6.1-terra", "gpt-6-luna"],
        "names": ["GPT-6 Astra", "GPT-6.1 Sol", "GPT-6.1 Terra", "GPT-6 Luna"],
    },
    "google": {
        "model_ids": ["gemini-4-argon", "gemini-3-8-flash", "gemini-3-5-flash-lite"],
        "api_identifiers": ["gemini-4-argon", "gemini-3.8-flash", "gemini-3.5-flash-lite"],
        "names": ["Gemini 4 Argon", "Gemini 3.8 Flash", "Gemini 3.5 Flash-Lite"],
    },
}

# ============================================================================
# OUTDATED PATTERNS → CURRENT MODEL MAPPINGS
# ============================================================================

# Each pattern maps: (regex_pattern, replacement_model_id, description)
OUTDATED_PATTERNS: List[Tuple[str, str, str]] = [
    # -------------------------------------------------------------------------
    # Anthropic Claude - deprecated/retired → replacement (verified 2026-10-30)
    # -------------------------------------------------------------------------
    (
        r"claude-sonnet-4-5(-20\d{6})?",
        "claude-sonnet-5-5",
        "Claude Sonnet 4.5 (retires 2026-11-30)",
    ),
    (r"Claude Sonnet 4\.5", "Claude Sonnet 5.5", "Claude Sonnet 4.5 name"),
    (r"claude-opus-4-1(-20\d{6})?", "claude-opus-5-5", "Claude Opus 4.1 (retired 2026-08-05)"),
    (r"Claude Opus 4\.1", "Claude Opus 5.5", "Claude Opus 4.1 name"),
    (r"claude-haiku-4-5(-20\d{6})?", "claude-haiku-5-5", "Claude Haiku 4.5 (legacy)"),
    (r"Claude Haiku 4\.5", "Claude Haiku 5.5", "Claude Haiku 4.5 name"),
    # -------------------------------------------------------------------------
    # OpenAI - deprecated/shut down → replacement
    # -------------------------------------------------------------------------
    (r"gpt-5-mini(-2025-08-07)?", "gpt-6.1-terra", "GPT-5 mini (shuts down 2026-12-11)"),
    (r"gpt-5(-2025-08-07)?(?![.\w-])", "gpt-6.1-sol", "GPT-5 (shuts down 2026-12-11)"),
    (r"\bo3(-2025-04-16)?(?![\w-])", "gpt-6.1-sol", "o3 (shuts down 2026-12-11)"),
    (r"\bo4-mini(-2025-04-16)?(?![\w-])", "gpt-6.1-terra", "o4-mini (shut down 2026-10-23)"),
    (r"gpt-4\.1-mini(-2025-04-14)?", "gpt-6-luna", "GPT-4.1 mini (shuts down 2027-01-14)"),
    (r"gpt-4\.1(-2025-04-14)?(?![\w-])", "gpt-6-luna", "GPT-4.1 (shuts down 2027-01-14)"),
    (r"gpt-4o-mini(-2024-07-18)?", "gpt-6-luna", "GPT-4o mini (shuts down 2027-01-14)"),
    (r"gpt-4o(-20\d{2}-\d{2}-\d{2})?(?![\w-])", "gpt-6-luna", "GPT-4o (shuts down 2027-01-14)"),
    # -------------------------------------------------------------------------
    # Google Gemini - limited to existing users → recommended replacement
    # -------------------------------------------------------------------------
    (r"gemini-2[-.]5-flash-lite(-\d{3})?", "gemini-3-5-flash-lite", "Gemini 2.5 Flash-Lite"),
    (r"gemini-2[-.]5-flash(-\d{3})?(?!-)", "gemini-3-8-flash", "Gemini 2.5 Flash"),
    (r"gemini-2[-.]5-pro(-\d{3})?", "gemini-4-argon", "Gemini 2.5 Pro"),
]

# Compile patterns for efficiency
COMPILED_PATTERNS: List[Tuple[Pattern, str, str]] = [
    (re.compile(pattern, re.IGNORECASE), replacement, desc)
    for pattern, replacement, desc in OUTDATED_PATTERNS
]

# ============================================================================
# FILE PATTERNS
# ============================================================================

# File extensions to scan
SCANNABLE_EXTENSIONS = {
    ".py",
    ".md",
    ".yaml",
    ".yml",
    ".json",
    ".txt",
    ".sh",
    ".toml",
    ".cfg",
    ".ini",
    ".rst",
}

# Directories to exclude from scanning
EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
    "env",
    ".env",
    ".pytest_cache",
    ".mypy_cache",
    ".tox",
    "dist",
    "build",
    "*.egg-info",
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def get_all_current_models() -> List[str]:
    """Get list of all current model IDs."""
    all_models = []
    for provider_models in CURRENT_MODELS.values():
        all_models.extend(provider_models["model_ids"])
    return all_models


def get_all_current_model_names() -> List[str]:
    """Get list of all current model display names."""
    all_names = []
    for provider_models in CURRENT_MODELS.values():
        all_names.extend(provider_models["names"])
    return all_names


def is_outdated_pattern(text: str) -> bool:
    """Check if text contains any outdated model patterns."""
    for pattern, _, _ in COMPILED_PATTERNS:
        if pattern.search(text):
            return True
    return False


def find_outdated_references(text: str) -> List[Tuple[str, str, str]]:
    """Find all outdated model references in text.

    Returns:
        List of tuples: (matched_text, replacement, description)
    """
    references = []
    for pattern, replacement, desc in COMPILED_PATTERNS:
        matches = pattern.finditer(text)
        for match in matches:
            references.append((match.group(0), replacement, desc))
    return references
