# Copyright (c) 2025 Andy Woods
# Licensed under the MIT License (see LICENSE file)

"""
Additional tests for ai_models/pricing.py to achieve 85%+ coverage.

Focuses on edge cases, error handling, and untested code paths.
"""

from datetime import date
from pathlib import Path
from typing import Any
from unittest.mock import Mock, mock_open, patch

import pytest
import yaml

from ai_models.pricing import Pricing, PricingService, get_pricing_service


class TestPricingToDict:
    """Test Pricing.to_dict() serialization."""

    def test_to_dict_with_all_fields(self) -> None:
        """Test to_dict includes all fields when present."""
        pricing = Pricing(
            model_id="test-model",
            input_per_1m=3.0,
            output_per_1m=15.0,
            cache_write_per_1m=3.75,
            cache_read_per_1m=0.3,
            effective_date=date(2025, 1, 1),
            verified_date=date(2025, 1, 15),
        )

        result = pricing.to_dict()

        assert result["model_id"] == "test-model"
        assert result["input_per_1m"] == 3.0
        assert result["output_per_1m"] == 15.0
        assert result["cache_write_per_1m"] == 3.75
        assert result["cache_read_per_1m"] == 0.3
        assert result["effective_date"] == "2025-01-01"
        assert result["verified_date"] == "2025-01-15"

    def test_to_dict_without_optional_fields(self) -> None:
        """Test to_dict omits None optional fields."""
        pricing = Pricing(
            model_id="test-model",
            input_per_1m=1.0,
            output_per_1m=5.0,
            cache_write_per_1m=None,
            cache_read_per_1m=None,
            effective_date=None,
            verified_date=None,
        )

        result = pricing.to_dict()

        assert result["model_id"] == "test-model"
        assert result["input_per_1m"] == 1.0
        assert result["output_per_1m"] == 5.0
        # Optional fields should not be in dict
        assert "cache_write_per_1m" not in result
        assert "cache_read_per_1m" not in result
        assert "effective_date" not in result
        assert "verified_date" not in result

    def test_to_dict_with_partial_optional_fields(self) -> None:
        """Test to_dict includes only present optional fields."""
        pricing = Pricing(
            model_id="test-model",
            input_per_1m=2.0,
            output_per_1m=10.0,
            cache_write_per_1m=2.5,  # Present
            cache_read_per_1m=None,  # Not present
            effective_date=date(2025, 1, 1),  # Present
            verified_date=None,  # Not present
        )

        result = pricing.to_dict()

        assert "cache_write_per_1m" in result
        assert result["cache_write_per_1m"] == 2.5
        assert "cache_read_per_1m" not in result
        assert "effective_date" in result
        assert "verified_date" not in result


class TestPricingServiceInit:
    """Test PricingService initialization."""

    def test_init_with_custom_definitions_dir(self) -> None:
        """Test initialization with custom definitions directory."""
        custom_dir = Path("/tmp/custom_definitions")

        with patch.object(Path, "exists", return_value=False):
            service = PricingService(definitions_dir=custom_dir)

            assert service.definitions_dir == custom_dir
            assert isinstance(service._pricing_cache, dict)

    def test_init_with_default_definitions_dir(self) -> None:
        """Test initialization uses default directory when not specified."""
        service = PricingService()

        Path(__file__).parent.parent / "ai_models" / "definitions"
        # The actual path will be relative to pricing.py, so just check it's a Path
        assert isinstance(service.definitions_dir, Path)
        assert service.definitions_dir.name == "definitions"


class TestPricingServiceErrorHandling:
    """Test error handling in PricingService."""

    def test_load_all_pricing_with_missing_directory(self) -> None:
        """Test graceful handling when definitions directory doesn't exist."""
        with patch.object(Path, "exists", return_value=False):
            service = PricingService()

            # Should not crash, cache should be empty
            assert len(service._pricing_cache) == 0

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.rglob")
    def test_load_all_pricing_skips_schema_file(self, mock_rglob: Any, mock_exists: Any) -> None:
        """Test that schema.md files are skipped during loading."""
        mock_exists.return_value = True

        schema_file = Mock(spec=Path)
        schema_file.name = "schema.md"

        mock_rglob.return_value = [schema_file]

        service = PricingService()

        # Schema file should be skipped, cache should be empty
        assert len(service._pricing_cache) == 0

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.rglob")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_all_pricing_skips_invalid_yaml(
        self, mock_file: Any, mock_rglob: Any, mock_exists: Any
    ) -> None:
        """Test that YAML files without model_id are skipped."""
        mock_exists.return_value = True

        yaml_path = Mock(spec=Path)
        yaml_path.name = "test.yaml"
        yaml_path.__str__ = Mock(return_value="test.yaml")  # type: ignore[method-assign]
        mock_rglob.return_value = [yaml_path]

        # YAML without model_id
        with patch("yaml.safe_load", return_value={"name": "Test"}):
            service = PricingService()

            # Should skip this file
            assert len(service._pricing_cache) == 0

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.rglob")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_load_all_pricing_handles_yaml_exceptions(
        self, mock_print: Any, mock_file: Any, mock_rglob: Any, mock_exists: Any
    ) -> None:
        """Test exception handling when YAML loading fails."""
        mock_exists.return_value = True

        yaml_path = Mock(spec=Path)
        yaml_path.name = "bad.yaml"
        yaml_path.__str__ = Mock(return_value="bad.yaml")  # type: ignore[method-assign]
        mock_rglob.return_value = [yaml_path]

        # Simulate YAML error
        with patch("yaml.safe_load", side_effect=yaml.YAMLError("Parse error")):
            PricingService()

            # Should print warning
            mock_print.assert_called()
            call_args = str(mock_print.call_args)
            assert "Warning" in call_args or "Failed" in call_args


class TestParseDateMethod:
    """Test _parse_date method."""

    def test_parse_date_with_none(self) -> None:
        """Test _parse_date returns None when input is None."""
        service = PricingService()
        result = service._parse_date(None)
        assert result is None

    def test_parse_date_with_empty_string(self) -> None:
        """Test _parse_date returns None for empty string."""
        service = PricingService()
        result = service._parse_date("")
        assert result is None

    def test_parse_date_with_invalid_format(self) -> None:
        """Test _parse_date returns None for invalid date format."""
        service = PricingService()

        # Invalid format
        result = service._parse_date("not-a-date")
        assert result is None

        # Wrong separator
        result = service._parse_date("2025/01/01")
        assert result is None

    def test_parse_date_with_valid_format(self) -> None:
        """Test _parse_date correctly parses valid ISO dates."""
        service = PricingService()

        result = service._parse_date("2025-01-15")
        assert result == date(2025, 1, 15)

        result = service._parse_date("2024-12-31")
        assert result == date(2024, 12, 31)


class TestGetAllPricing:
    """Test get_all_pricing method."""

    def test_get_all_pricing_returns_copy(self) -> None:
        """Test that get_all_pricing returns a copy, not the original cache."""
        service = PricingService()

        pricing1 = service.get_all_pricing()
        pricing2 = service.get_all_pricing()

        # Should be equal but not the same object
        assert pricing1 == pricing2
        assert pricing1 is not pricing2

        # Modifying one shouldn't affect the other
        pricing1.clear()
        pricing2_after = service.get_all_pricing()
        assert len(pricing2_after) > 0  # Original cache unchanged

    def test_get_all_pricing_includes_all_models(self) -> None:
        """Test get_all_pricing includes all loaded models."""
        service = PricingService()
        all_pricing = service.get_all_pricing()

        assert isinstance(all_pricing, dict)
        # Should have pricing for known models
        assert "claude-sonnet-4-5" in all_pricing
        assert "gpt-4o" in all_pricing
        assert "gemini-2-5-pro" in all_pricing


class TestCalculateCostMethod:
    """Test PricingService.calculate_cost method."""

    def test_calculate_cost_raises_for_unknown_model(self) -> None:
        """Test calculate_cost raises ValueError for unknown model."""
        service = PricingService()

        with pytest.raises(ValueError) as exc_info:
            service.calculate_cost("nonexistent-model", 1000, 500)

        assert "Pricing not found" in str(exc_info.value)
        assert "nonexistent-model" in str(exc_info.value)

    def test_calculate_cost_with_valid_model(self) -> None:
        """Test calculate_cost works for valid model."""
        service = PricingService()

        # Claude Haiku: $1.00 input, $5.00 output per 1M tokens
        cost = service.calculate_cost("claude-haiku-4-5", 1000, 500)

        # (1000/1M * 1.00) + (500/1M * 5.00) = 0.001 + 0.0025 = 0.0035
        assert cost == pytest.approx(0.0035, rel=1e-6)

    def test_calculate_cost_with_caching(self) -> None:
        """Test calculate_cost includes caching costs."""
        service = PricingService()

        # Claude Sonnet has caching: $3.00 input, $15.00 output, $0.30 cache read
        # 1000 input (900 cached), 500 output
        cost = service.calculate_cost("claude-sonnet-4-5", 1000, 500, cached_input_tokens=900)

        # (100/1M * 3.00) + (900/1M * 0.30) + (500/1M * 15.00)
        # = 0.0003 + 0.00027 + 0.0075 = 0.00807
        assert cost == pytest.approx(0.00807, rel=1e-5)


class TestGetPricingService:
    """Test get_pricing_service singleton function."""

    def test_get_pricing_service_returns_singleton(self) -> None:
        """Test get_pricing_service returns the same instance."""
        # Reset singleton
        import ai_models.pricing

        ai_models.pricing._pricing_service = None

        service1 = get_pricing_service()
        service2 = get_pricing_service()

        # Should be the exact same object
        assert service1 is service2

    def test_get_pricing_service_returns_pricing_service(self) -> None:
        """Test get_pricing_service returns PricingService instance."""
        import ai_models.pricing

        ai_models.pricing._pricing_service = None

        service = get_pricing_service()

        assert isinstance(service, PricingService)
        assert hasattr(service, "get_pricing")
        assert hasattr(service, "calculate_cost")


class TestPricingDataclass:
    """Test Pricing dataclass behavior."""

    def test_pricing_is_frozen(self) -> None:
        """Test that Pricing dataclass is immutable (frozen)."""
        pricing = Pricing(
            model_id="test-model",
            input_per_1m=1.0,
            output_per_1m=5.0,
        )

        # Should not be able to modify frozen dataclass
        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            pricing.input_per_1m = 2.0  # type: ignore[misc]

    def test_pricing_defaults(self) -> None:
        """Test Pricing dataclass default values."""
        pricing = Pricing(
            model_id="test-model",
            input_per_1m=1.0,
            output_per_1m=5.0,
        )

        assert pricing.cache_write_per_1m is None
        assert pricing.cache_read_per_1m is None
        assert pricing.effective_date is None
        assert pricing.verified_date is None


class TestGetPricing:
    """Test PricingService.get_pricing method."""

    def test_get_pricing_returns_none_for_unknown_model(self) -> None:
        """Test get_pricing returns None for unknown model."""
        service = PricingService()
        pricing = service.get_pricing("nonexistent-model")
        assert pricing is None

    def test_get_pricing_returns_pricing_for_known_model(self) -> None:
        """Test get_pricing returns Pricing object for known model."""
        service = PricingService()
        pricing = service.get_pricing("claude-sonnet-4-5")

        assert pricing is not None
        assert isinstance(pricing, Pricing)
        assert pricing.model_id == "claude-sonnet-4-5"
        assert pricing.input_per_1m > 0
        assert pricing.output_per_1m > 0

    def test_get_pricing_ignores_as_of_date_for_now(self) -> None:
        """Test get_pricing ignores as_of_date parameter (future feature)."""
        service = PricingService()

        # Should return same pricing regardless of as_of_date
        pricing1 = service.get_pricing("claude-haiku-4-5", as_of_date=date(2024, 1, 1))
        pricing2 = service.get_pricing("claude-haiku-4-5", as_of_date=date(2025, 1, 1))

        assert pricing1 == pricing2
