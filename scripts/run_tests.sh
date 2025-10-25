#!/bin/bash
#
# Test Runner Script for PM Prompt Patterns
#
# Usage:
#   ./scripts/run_tests.sh              # Run fast tests only
#   ./scripts/run_tests.sh --all        # Run all tests including endpoints (requires API keys)
#   ./scripts/run_tests.sh --endpoints  # Run only endpoint tests
#   ./scripts/run_tests.sh --help       # Show help

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default options
RUN_FAST=true
RUN_ENDPOINTS=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --all)
            RUN_FAST=true
            RUN_ENDPOINTS=true
            shift
            ;;
        --endpoints)
            RUN_FAST=false
            RUN_ENDPOINTS=true
            shift
            ;;
        --fast)
            RUN_FAST=true
            RUN_ENDPOINTS=false
            shift
            ;;
        --help|-h)
            echo "Test Runner for PM Prompt Patterns"
            echo ""
            echo "Usage:"
            echo "  $0              Run fast tests only (default)"
            echo "  $0 --all        Run all tests including endpoints"
            echo "  $0 --endpoints  Run only endpoint tests"
            echo "  $0 --fast       Run only fast tests (no API calls)"
            echo "  $0 --help       Show this help"
            echo ""
            echo "Fast tests (no API keys required):"
            echo "  - Model registry validation (27 tests)"
            echo "  - Deprecated model detection (12 tests)"
            echo "  - Pricing consistency checks (23 tests)"
            echo "  - AI models system (35 tests)"
            echo ""
            echo "Endpoint tests (API keys required):"
            echo "  - Actual API calls to verify models work"
            echo "  - Requires: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}PM Prompt Patterns - Test Suite${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Add project root to PYTHONPATH so tests can import models
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}ERROR: pytest not found${NC}"
    echo "Install with: pip install pytest"
    exit 1
fi

# Track overall success
OVERALL_SUCCESS=true

# Run fast tests
if [ "$RUN_FAST" = true ]; then
    echo -e "${BLUE}Running fast tests (no API calls)...${NC}"
    echo ""

    # Registry validation
    echo -e "${YELLOW}→ Model registry validation${NC}"
    if pytest tests/test_model_registry.py -v; then
        echo -e "${GREEN}✓ Registry validation passed${NC}"
    else
        echo -e "${RED}✗ Registry validation failed${NC}"
        OVERALL_SUCCESS=false
    fi
    echo ""

    # Deprecated model detection
    echo -e "${YELLOW}→ Deprecated model detection${NC}"
    if pytest tests/test_deprecated_models.py -v; then
        echo -e "${GREEN}✓ No deprecated models found${NC}"
    else
        echo -e "${RED}✗ Deprecated models detected${NC}"
        OVERALL_SUCCESS=false
    fi
    echo ""

    # Pricing consistency
    echo -e "${YELLOW}→ Pricing consistency checks${NC}"
    if pytest tests/test_pricing_consistency.py -v; then
        echo -e "${GREEN}✓ Pricing validation passed${NC}"
    else
        echo -e "${RED}✗ Pricing validation failed${NC}"
        OVERALL_SUCCESS=false
    fi
    echo ""

    # New AI models system
    echo -e "${YELLOW}→ AI models system tests${NC}"
    if pytest tests/test_ai_models.py -v; then
        echo -e "${GREEN}✓ AI models system passed${NC}"
    else
        echo -e "${RED}✗ AI models system failed${NC}"
        OVERALL_SUCCESS=false
    fi
    echo ""
fi

# Run endpoint tests
if [ "$RUN_ENDPOINTS" = true ]; then
    echo -e "${BLUE}Running endpoint tests (requires API keys)...${NC}"
    echo ""

    # Check for API keys
    MISSING_KEYS=()
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        MISSING_KEYS+=("ANTHROPIC_API_KEY")
    fi
    if [ -z "$OPENAI_API_KEY" ]; then
        MISSING_KEYS+=("OPENAI_API_KEY")
    fi
    if [ -z "$GOOGLE_API_KEY" ]; then
        MISSING_KEYS+=("GOOGLE_API_KEY")
    fi

    if [ ${#MISSING_KEYS[@]} -gt 0 ]; then
        echo -e "${YELLOW}⚠ Warning: Missing API keys (some tests will be skipped):${NC}"
        for key in "${MISSING_KEYS[@]}"; do
            echo -e "  - $key"
        done
        echo ""
    fi

    echo -e "${YELLOW}→ Model endpoint verification${NC}"
    if pytest tests/test_model_endpoints.py -v; then
        echo -e "${GREEN}✓ Endpoint tests passed${NC}"
    else
        echo -e "${RED}✗ Endpoint tests failed${NC}"
        OVERALL_SUCCESS=false
    fi
    echo ""
fi

# Summary
echo -e "${BLUE}========================================${NC}"
if [ "$OVERALL_SUCCESS" = true ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi
