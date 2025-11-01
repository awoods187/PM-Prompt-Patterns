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
        "model_ids": ["claude-haiku-4-5", "claude-sonnet-4-5", "claude-opus-4-1"],
        "api_identifiers": [
            "claude-haiku-4-5-20251001",
            "claude-sonnet-4-5-20250929",
            "claude-opus-4-1-20250805",
        ],
        "names": ["Claude Haiku 4.5", "Claude Sonnet 4.5", "Claude Opus 4.1"],
    },
    "openai": {
        "model_ids": ["gpt-4o", "gpt-4o-mini"],
        "api_identifiers": ["gpt-4o-2024-08-06", "gpt-4o-mini-2024-07-18"],
        "names": ["GPT-4o", "GPT-4o Mini"],
    },
    "google": {
        "model_ids": ["gemini-2-5-pro", "gemini-2-5-flash", "gemini-2-5-flash-lite"],
        "api_identifiers": [
            "gemini-2.5-pro-002",
            "gemini-2.5-flash-002",
            "gemini-2.5-flash-lite-002",
        ],
        "names": ["Gemini 2.5 Pro", "Gemini 2.5 Flash", "Gemini 2.5 Flash-Lite"],
    },
}

# ============================================================================
# OUTDATED PATTERNS → CURRENT MODEL MAPPINGS
# ============================================================================

# Each pattern maps: (regex_pattern, replacement_model_id, description)
OUTDATED_PATTERNS: List[Tuple[str, str, str]] = [
    # -------------------------------------------------------------------------
    # Anthropic Claude - Old model IDs and names
    # -------------------------------------------------------------------------
    # Claude Sonnet 4.5 (various formats)
    (r"claude-sonnet-4-5-20\d{6}", "claude-sonnet-4-5", "Claude Sonnet 4.5 dated API ID"),
    (r"claude-sonnet-4-5", "claude-sonnet-4-5", "Claude Sonnet 4.5 model ID"),
    (r"claude-sonnet-4-5", "claude-sonnet-4-5", "Claude 35 Sonnet alternate"),
    (r"Claude 3\.5 Sonnet", "Claude Sonnet 4.5", "Claude Sonnet 4.5 name"),
    (r"Claude Sonnet 4.5", "Claude Sonnet 4.5", "Claude Sonnet 4.5 name variant"),
    # Claude Haiku 4.5
    (r"claude-haiku-4-5-20\d{6}", "claude-haiku-4-5", "Claude Haiku 4.5 dated API ID"),
    (r"claude-haiku-4-5", "claude-haiku-4-5", "Claude Haiku 4.5 model ID"),
    (r"claude-haiku-4-5", "claude-haiku-4-5", "Claude 35 Haiku alternate"),
    (r"Claude 3\.5 Haiku", "Claude Haiku 4.5", "Claude Haiku 4.5 name"),
    (r"Claude Haiku 4.5", "Claude Haiku 4.5", "Claude Haiku 4.5 name variant"),
    # Claude Opus 4.1
    (r"claude-opus-4-1-20\d{6}", "claude-opus-4-1", "Claude Opus 4.1 dated API ID"),
    (r"claude-opus-4-1", "claude-opus-4-1", "Claude Opus 4.1 model ID"),
    (r"Claude Opus 4.1", "Claude Opus 4.1", "Claude Opus 4.1 name"),
    # Claude Sonnet 4.5 (older)
    (r"claude-sonnet-4-5-20\d{6}", "claude-sonnet-4-5", "Claude Sonnet 4.5 dated API ID"),
    (r"claude-sonnet-4-5", "claude-sonnet-4-5", "Claude Sonnet 4.5 model ID"),
    (r"Claude Sonnet 4.5", "Claude Sonnet 4.5", "Claude Sonnet 4.5 name"),
    # Claude Haiku 4.5 (older)
    (r"claude-haiku-4-5-20\d{6}", "claude-haiku-4-5", "Claude Haiku 4.5 dated API ID"),
    (r"claude-haiku-4-5", "claude-haiku-4-5", "Claude Haiku 4.5 model ID"),
    (r"Claude Haiku 4.5", "Claude Haiku 4.5", "Claude Haiku 4.5 name"),
    # Claude Haiku 4.5 (very old)
    (r"claude-haiku-4-5-\d+", "claude-haiku-4-5", "Claude Haiku 4.5 model"),
    (r"claude-haiku-4-5", "claude-haiku-4-5", "Claude Haiku 4.5 generic"),
    (r"Claude Haiku 4.5", "Claude Haiku 4.5", "Claude Haiku 4.5 name"),
    # -------------------------------------------------------------------------
    # OpenAI GPT - Old model IDs and names
    # -------------------------------------------------------------------------
    # GPT-4o (various formats)
    (r"gpt-4o-20\d{4}-\d{2}-\d{2}", "gpt-4o", "GPT-4o dated"),
    (r"gpt-4o", "gpt-4o", "GPT-4o preview"),
    (r"gpt-4o", "gpt-4o", "GPT-4 1106 preview"),
    (r"gpt-4o", "gpt-4o", "GPT-4 0125 preview"),
    (r"gpt-4o", "gpt-4o", "GPT-4o generic"),
    (r"GPT-4o", "GPT-4o", "GPT-4o name"),
    (r"gpt-4o", "GPT-4o", "gpt-4o name variant"),
    # GPT-4o Mini (various formats)
    (r"gpt-4o-mini-\d{4}", "gpt-4o-mini", "GPT-4o Mini dated"),
    (r"gpt-4o-mini", "gpt-4o-mini", "GPT-4o Mini 16k"),
    (r"gpt-4o-mini", "gpt-4o-mini", "GPT-4o Mini generic"),
    (r"gpt-4o-mini", "gpt-4o-mini", "GPT-35 Turbo variant"),
    (r"GPT-3\.5 Turbo", "GPT-4o Mini", "GPT-4o Mini name"),
    (r"GPT-4o Mini", "GPT-4o Mini", "GPT-4o Mini name variant"),
    # GPT-3.5 older
    (r"gpt-4o-mini", "gpt-4o-mini", "gpt-4o-mini"),
    (r"gpt-4o-mini", "gpt-4o-mini", "gpt-4o-mini"),
    # -------------------------------------------------------------------------
    # Google Gemini - Old model IDs and names
    # -------------------------------------------------------------------------
    # Gemini 2.5 Pro
    (r"gemini-2-5-pro-\d+", "gemini-2-5-pro", "Gemini 2.5 Pro dated"),
    (r"gemini-1\.5-pro-\d+", "gemini-2-5-pro", "Gemini 2.5 Pro dot dated"),
    (r"gemini-2-5-pro", "gemini-2-5-pro", "Gemini 2.5 Pro model ID"),
    (r"gemini-1\.5-pro", "gemini-2-5-pro", "Gemini 2.5 Pro dot model ID"),
    (r"Gemini 1\.5 Pro", "Gemini 2.5 Pro", "Gemini 2.5 Pro name"),
    (r"Gemini 2.5 Pro", "Gemini 2.5 Pro", "Gemini 2.5 Pro name variant"),
    # Gemini 2.5 Flash
    (r"gemini-2-5-flash-\d+", "gemini-2-5-flash", "Gemini 2.5 Flash dated"),
    (r"gemini-1\.5-flash-\d+", "gemini-2-5-flash", "Gemini 2.5 Flash dot dated"),
    (r"gemini-2-5-flash", "gemini-2-5-flash", "Gemini 2.5 Flash model ID"),
    (r"gemini-1\.5-flash", "gemini-2-5-flash", "Gemini 2.5 Flash dot model ID"),
    (r"Gemini 1\.5 Flash", "Gemini 2.5 Flash", "Gemini 2.5 Flash name"),
    (r"Gemini 2.5 Flash", "Gemini 2.5 Flash", "Gemini 2.5 Flash name variant"),
    # Gemini 2.5 Pro (very old)
    (r"gemini-2-5-pro", "gemini-2-5-pro", "Gemini 2.5 Pro model ID"),
    (r"gemini-1\.0-pro", "gemini-2-5-pro", "Gemini 2.5 Pro dot model ID"),
    (r"Gemini 1\.0 Pro", "Gemini 2.5 Pro", "Gemini 2.5 Pro name"),
    # Gemini 2.5 Pro/Flash (no version)
    (r"gemini-2-5-pro(?!-)", "gemini-2-5-pro", "Gemini 2.5 Pro generic"),
    (r"Gemini 2.5 Pro(?! \d)", "Gemini 2.5 Pro", "Gemini 2.5 Pro name"),
    (r"gemini-2-5-flash(?!-)", "gemini-2-5-flash", "Gemini 2.5 Flash generic"),
    (r"Gemini 2.5 Flash(?! \d)", "Gemini 2.5 Flash", "Gemini 2.5 Flash name"),
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
