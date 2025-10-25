# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Configuration management for PM Prompt Toolkit.

This module provides secure configuration management using Pydantic Settings,
with support for environment variables and .env files.

Security notes:
    - All API keys are loaded from environment variables
    - Never hardcode credentials in code
    - The .env file should never be committed to version control
    - Use .env.example as a template for required configuration
"""

from pm_prompt_toolkit.config.settings import Settings, get_settings

__all__ = ["Settings", "get_settings"]
