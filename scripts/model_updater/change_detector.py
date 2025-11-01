# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""Change detection logic for model updates."""

import logging
from dataclasses import dataclass, field
from typing import Any, Optional

from scripts.model_updater.fetchers.base_fetcher import ModelData

logger = logging.getLogger(__name__)


@dataclass
class ModelChange:
    """Represents a change to a model."""

    model_id: str
    change_type: str  # 'new', 'removed', 'pricing', 'capability', 'metadata'
    field: Optional[str] = None
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    description: str = ""


@dataclass
class ChangeReport:
    """Report of all detected changes."""

    new_models: list[ModelData] = field(default_factory=list)
    removed_models: list[str] = field(default_factory=list)  # model_ids
    pricing_changes: list[ModelChange] = field(default_factory=list)
    capability_changes: list[ModelChange] = field(default_factory=list)
    metadata_changes: list[ModelChange] = field(default_factory=list)
    context_changes: list[ModelChange] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        """Check if any changes were detected."""
        return bool(
            self.new_models
            or self.removed_models
            or self.pricing_changes
            or self.capability_changes
            or self.metadata_changes
            or self.context_changes
        )

    @property
    def total_changes(self) -> int:
        """Total number of changes."""
        return (
            len(self.new_models)
            + len(self.removed_models)
            + len(self.pricing_changes)
            + len(self.capability_changes)
            + len(self.metadata_changes)
            + len(self.context_changes)
        )

    def to_markdown(self) -> str:
        """Generate markdown changelog.

        Returns:
            Formatted markdown string
        """
        lines = ["# Model Update Changelog\n"]

        if not self.has_changes:
            lines.append("No changes detected.\n")
            return "\n".join(lines)

        # Summary
        lines.append(f"**Total Changes:** {self.total_changes}\n")

        # New models
        if self.new_models:
            lines.append(f"## 🆕 New Models ({len(self.new_models)})\n")
            for model in self.new_models:
                lines.append(f"### {model.name} (`{model.model_id}`)\n")
                lines.append(f"- **Provider:** {model.provider}")
                lines.append(f"- **API ID:** `{model.api_identifier}`")
                lines.append(
                    f"- **Context:** {model.context_window_input:,} input"
                    + (
                        f" / {model.context_window_output:,} output"
                        if model.context_window_output
                        else ""
                    )
                )
                lines.append(
                    f"- **Pricing:** ${model.input_per_1m:.2f} / ${model.output_per_1m:.2f} per 1M tokens"
                )
                lines.append(f"- **Tier:** {model.cost_tier} ({model.speed_tier})")
                lines.append(f"- **Capabilities:** {', '.join(model.capabilities)}\n")

        # Removed models (deprecated)
        if self.removed_models:
            lines.append(f"## ⚠️ Deprecated Models ({len(self.removed_models)})\n")
            lines.append("These models are no longer available from the provider:\n")
            for model_id in self.removed_models:
                lines.append(f"- `{model_id}`")
            lines.append("\n")

        # Pricing changes
        if self.pricing_changes:
            lines.append(f"## 💰 Pricing Changes ({len(self.pricing_changes)})\n")
            for change in self.pricing_changes:
                symbol = "📈" if change.new_value > change.old_value else "📉"
                pct_change = (
                    ((change.new_value - change.old_value) / change.old_value * 100)
                    if change.old_value
                    else 0
                )
                lines.append(
                    f"{symbol} **{change.model_id}** - {change.field}: "
                    f"${change.old_value:.2f} → ${change.new_value:.2f} "
                    f"({pct_change:+.1f}%)"
                )
            lines.append("\n")

        # Context window changes
        if self.context_changes:
            lines.append(f"## 📏 Context Window Changes ({len(self.context_changes)})\n")
            for change in self.context_changes:
                symbol = "📈" if change.new_value > change.old_value else "📉"
                lines.append(
                    f"{symbol} **{change.model_id}** - {change.field}: "
                    f"{change.old_value:,} → {change.new_value:,} tokens"
                )
            lines.append("\n")

        # Capability changes
        if self.capability_changes:
            lines.append(f"## ⚡ Capability Changes ({len(self.capability_changes)})\n")
            for change in self.capability_changes:
                lines.append(f"- **{change.model_id}**: {change.description}")
            lines.append("\n")

        # Metadata changes
        if self.metadata_changes:
            lines.append(f"## 📝 Metadata Changes ({len(self.metadata_changes)})\n")
            for change in self.metadata_changes:
                lines.append(
                    f"- **{change.model_id}** - {change.field}: "
                    f"`{change.old_value}` → `{change.new_value}`"
                )
            lines.append("\n")

        return "\n".join(lines)


class ChangeDetector:
    """Detects changes between current and fetched models."""

    def __init__(self) -> None:
        """Initialize change detector."""
        self.logger = logging.getLogger(self.__class__.__name__)

    def detect_changes(
        self,
        current_models: dict[str, dict[str, Any]],
        fetched_models: list[ModelData],
    ) -> ChangeReport:
        """Detect changes between current and fetched models.

        Args:
            current_models: Dictionary of current model definitions (from YAML)
            fetched_models: List of fetched ModelData objects

        Returns:
            ChangeReport with all detected changes
        """
        report = ChangeReport()

        # Convert fetched models to dict for easier lookup
        fetched_dict = {m.model_id: m for m in fetched_models}

        # Detect new models
        for model_id, model_data in fetched_dict.items():
            if model_id not in current_models:
                report.new_models.append(model_data)
                self.logger.info(f"New model detected: {model_id}")

        # Detect removed models
        for model_id in current_models:
            if model_id not in fetched_dict:
                report.removed_models.append(model_id)
                self.logger.warning(f"Model removed: {model_id}")

        # Detect changes in existing models
        for model_id, fetched_model in fetched_dict.items():
            if model_id in current_models:
                current = current_models[model_id]
                changes = self._compare_models(model_id, current, fetched_model)

                # Categorize changes
                for change in changes:
                    if "pricing" in change.change_type:
                        report.pricing_changes.append(change)
                    elif "capability" in change.change_type:
                        report.capability_changes.append(change)
                    elif "context" in change.change_type:
                        report.context_changes.append(change)
                    else:
                        report.metadata_changes.append(change)

        return report

    def _compare_models(
        self, model_id: str, current: dict[str, Any], fetched: ModelData
    ) -> list[ModelChange]:
        """Compare a single model for changes.

        Args:
            model_id: Model identifier
            current: Current model definition (from YAML)
            fetched: Fetched model data

        Returns:
            List of detected changes
        """
        changes = []

        # Check pricing changes
        current_pricing = current.get("pricing", {})
        if current_pricing.get("input_per_1m") != fetched.input_per_1m:
            changes.append(
                ModelChange(
                    model_id=model_id,
                    change_type="pricing",
                    field="input_per_1m",
                    old_value=current_pricing.get("input_per_1m"),
                    new_value=fetched.input_per_1m,
                    description=f"Input pricing changed",
                )
            )

        if current_pricing.get("output_per_1m") != fetched.output_per_1m:
            changes.append(
                ModelChange(
                    model_id=model_id,
                    change_type="pricing",
                    field="output_per_1m",
                    old_value=current_pricing.get("output_per_1m"),
                    new_value=fetched.output_per_1m,
                    description=f"Output pricing changed",
                )
            )

        # Check cache pricing
        if current_pricing.get("cache_write_per_1m") != fetched.cache_write_per_1m:
            changes.append(
                ModelChange(
                    model_id=model_id,
                    change_type="pricing",
                    field="cache_write_per_1m",
                    old_value=current_pricing.get("cache_write_per_1m"),
                    new_value=fetched.cache_write_per_1m,
                    description=f"Cache write pricing changed",
                )
            )

        if current_pricing.get("cache_read_per_1m") != fetched.cache_read_per_1m:
            changes.append(
                ModelChange(
                    model_id=model_id,
                    change_type="pricing",
                    field="cache_read_per_1m",
                    old_value=current_pricing.get("cache_read_per_1m"),
                    new_value=fetched.cache_read_per_1m,
                    description=f"Cache read pricing changed",
                )
            )

        # Check context window changes
        current_metadata = current.get("metadata", {})
        if current_metadata.get("context_window_input") != fetched.context_window_input:
            changes.append(
                ModelChange(
                    model_id=model_id,
                    change_type="context",
                    field="context_window_input",
                    old_value=current_metadata.get("context_window_input"),
                    new_value=fetched.context_window_input,
                    description=f"Input context window changed",
                )
            )

        if current_metadata.get("context_window_output") != fetched.context_window_output:
            changes.append(
                ModelChange(
                    model_id=model_id,
                    change_type="context",
                    field="context_window_output",
                    old_value=current_metadata.get("context_window_output"),
                    new_value=fetched.context_window_output,
                    description=f"Output context window changed",
                )
            )

        # Check capability changes
        current_caps = set(current.get("capabilities", []))
        fetched_caps = set(fetched.capabilities)

        added_caps = fetched_caps - current_caps
        removed_caps = current_caps - fetched_caps

        if added_caps:
            changes.append(
                ModelChange(
                    model_id=model_id,
                    change_type="capability",
                    field="capabilities",
                    old_value=None,
                    new_value=list(added_caps),
                    description=f"Added capabilities: {', '.join(added_caps)}",
                )
            )

        if removed_caps:
            changes.append(
                ModelChange(
                    model_id=model_id,
                    change_type="capability",
                    field="capabilities",
                    old_value=list(removed_caps),
                    new_value=None,
                    description=f"Removed capabilities: {', '.join(removed_caps)}",
                )
            )

        # Check knowledge cutoff changes
        if current_metadata.get("knowledge_cutoff") != fetched.knowledge_cutoff:
            changes.append(
                ModelChange(
                    model_id=model_id,
                    change_type="metadata",
                    field="knowledge_cutoff",
                    old_value=current_metadata.get("knowledge_cutoff"),
                    new_value=fetched.knowledge_cutoff,
                    description=f"Knowledge cutoff updated",
                )
            )

        # Check API identifier changes
        if current.get("api_identifier") != fetched.api_identifier:
            changes.append(
                ModelChange(
                    model_id=model_id,
                    change_type="metadata",
                    field="api_identifier",
                    old_value=current.get("api_identifier"),
                    new_value=fetched.api_identifier,
                    description=f"API identifier updated",
                )
            )

        return changes
