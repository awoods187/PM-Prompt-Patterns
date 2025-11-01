# Multi-Provider LLM Orchestration System

**Complexity**: 🔴 Advanced
**Category**: Code Generation / System Architecture
**Model Compatibility**: ✅ Claude Opus (best) | ✅ Claude Sonnet 4 | ⚠️ GPT-4 (may need more guidance)

## Overview

Production-grade prompt for building a Python library that provides unified access to multiple LLM providers (OpenAI, Anthropic, Google Gemini, AWS Bedrock, Google Vertex AI) with dynamic model discovery, intelligent fallback, and comprehensive cost tracking.

**Business Value**:
- Reduce vendor lock-in with provider-agnostic interface
- Enable cost optimization through provider/model selection across 5 major providers
- Improve reliability with automatic within-provider fallback
- Gain visibility into LLM usage and costs across applications
- Simplify integration with single unified API
- Support multi-cloud deployments (AWS, GCP, direct APIs)

**Use Cases**:
- Building LLM-powered applications that need provider flexibility
- Creating cost-aware AI systems with usage tracking
- Migrating between LLM providers without code changes
- Prototyping with multiple models from single codebase
- Enterprise applications requiring cost accountability
- AWS-native applications leveraging Bedrock
- GCP-native applications leveraging Vertex AI
- Multi-cloud architectures with provider diversity

**Production metrics**:
- Development time: 3-4 days for full implementation (5 providers)
- Code quality: 90%+ test coverage achievable
- Reliability: <1% failure rate with proper fallback configuration
- Cost visibility: 100% API call tracking and attribution
- Provider coverage: 5 major providers (OpenAI, Anthropic, Gemini, Bedrock, Vertex)

---

## Base Prompt (Model Agnostic)

**Complexity**: 🔴 Advanced

```
You are a senior Python architect specializing in building robust, production-grade libraries for LLM integration. Your expertise includes API design, adapter patterns, error handling, cloud provider SDKs (AWS, GCP), and building maintainable, well-tested Python packages.

## YOUR TASK

Build a complete Python library for multi-provider LLM orchestration that provides a unified interface to OpenAI, Anthropic, Google Gemini, AWS Bedrock, and Google Vertex AI with dynamic model discovery, intelligent fallback, and comprehensive cost tracking.

---

## SYSTEM REQUIREMENTS

### Core Architecture

**Language & Standards**:
- Python 3.9+ with type hints throughout
- Integration type: Importable library/module (NOT standalone service)
- Response patterns: Both streaming and standard request/response
- Design pattern: Adapter pattern with unified abstract interface
- Code style: PEP 8 compliant, Black formatted

**Dependencies**:
```python
# pyproject.toml or requirements.txt
openai>=1.0.0
anthropic>=0.18.0
google-generativeai>=0.3.0
google-cloud-aiplatform>=1.38.0  # For Vertex AI
boto3>=1.28.0  # For AWS Bedrock
pyyaml>=6.0
pydantic>=2.0  # For config validation
```

---

## IMPLEMENTATION PLAN

Implement in this exact order for incremental testing:

### Phase 1: Base Provider Adapters (Day 1-2)

**1.1 Abstract Base Class**

Create `providers/base.py`:
```python
from abc import ABC, abstractmethod
from typing import Dict, List, Iterator, Optional
from dataclasses import dataclass

@dataclass
class LLMResponse:
    """Normalized response format across all providers."""
    content: str
    model: str
    tokens_used: Dict[str, int]  # {"prompt": X, "completion": Y, "total": Z}
    provider: str
    raw_response: Optional[Dict] = None

class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers."""

    @abstractmethod
    def __init__(self, api_key: str, **config):
        """Initialize provider with API key and optional config."""
        pass

    @abstractmethod
    def send_request(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Send non-streaming request. Returns normalized response."""
        pass

    @abstractmethod
    def send_streaming_request(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Iterator[str]:
        """Send streaming request. Yields content chunks as strings."""
        pass

    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Fetch current model list from provider API."""
        pass

    @abstractmethod
    def validate_model(self, model: str) -> bool:
        """Test if model is available via API call."""
        pass
```

**1.2 OpenAI Adapter**

Create `providers/openai_adapter.py`:
```python
from openai import OpenAI
from .base import BaseLLMProvider, LLMResponse
# Implement all abstract methods
# Map OpenAI errors to common exceptions
# Handle streaming with proper chunk parsing
```

**1.3 Anthropic Adapter**

Create `providers/anthropic_adapter.py`:
```python
from anthropic import Anthropic
from .base import BaseLLMProvider, LLMResponse
# Implement all abstract methods
# Convert Anthropic message format to common format
# Handle streaming events properly
```

**1.4 Gemini Adapter**

Create `providers/gemini_adapter.py`:
```python
import google.generativeai as genai
from .base import BaseLLMProvider, LLMResponse
# Implement all abstract methods
# Convert Gemini format to common format
# Handle safety settings and streaming
```

### Phase 2: Model Registry (Day 1-2)

**2.1 Model Registry Implementation**

Create `models/registry.py`:
```python
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class ModelInfo:
    """Model metadata."""
    name: str
    provider: str
    deprecated: bool = False
    last_validated: Optional[datetime] = None

class ModelRegistry:
    """Manages model discovery and caching."""

    def __init__(self, providers: Dict[str, BaseLLMProvider]):
        self.providers = providers
        self.cache: Dict[str, List[ModelInfo]] = {}
        self.cache_timestamp: Optional[datetime] = None

    def refresh_models(self, provider_name: Optional[str] = None):
        """
        Fetch fresh model lists from provider APIs.

        Args:
            provider_name: Specific provider to refresh, or None for all
        """
        # Call provider.get_available_models()
        # Update cache with timestamps
        # Mark models not in new list as deprecated (don't remove)
        pass

    def get_available_models(
        self,
        provider_name: str,
        include_deprecated: bool = False
    ) -> List[ModelInfo]:
        """Get cached model list for provider."""
        pass

    def is_model_deprecated(self, provider_name: str, model_name: str) -> bool:
        """Check if model is marked deprecated."""
        pass

    def validate_model(self, provider_name: str, model_name: str) -> bool:
        """Test model availability with actual API call."""
        pass
```

**Requirements**:
- Cache model lists with timestamps
- Manual refresh via `refresh_models()` method
- Validate models through test API calls
- Mark deprecated models (maintain backward compatibility)
- Exclude fine-tuned models (base models only)
- Filter out models with "ft-" prefix or similar

### Phase 3: Configuration System (Day 2)

**3.1 Configuration Schema**

Create `config/manager.py`:
```python
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional
import yaml
import os

class ProviderConfig(BaseModel):
    api_key: str
    fallback_models: List[str] = []

    @validator('api_key')
    def resolve_env_var(cls, v):
        """Resolve ${VAR_NAME} to environment variable."""
        if v.startswith('${') and v.endswith('}'):
            var_name = v[2:-1]
            return os.getenv(var_name, '')
        return v

class CostTrackingConfig(BaseModel):
    enabled: bool = True
    log_path: str = "./llm_costs.log"

class OrchestratorConfig(BaseModel):
    active_provider: str
    active_model: str
    providers: Dict[str, ProviderConfig]
    cost_tracking: CostTrackingConfig = CostTrackingConfig()

    @validator('active_provider')
    def validate_provider(cls, v, values):
        """Ensure active_provider exists in providers dict."""
        if 'providers' in values and v not in values['providers']:
            raise ValueError(f"active_provider '{v}' not in providers")
        return v

class ConfigManager:
    """Handles YAML config loading and validation."""

    @staticmethod
    def load_config(config_path: str) -> OrchestratorConfig:
        """Load and validate YAML configuration."""
        with open(config_path) as f:
            raw_config = yaml.safe_load(f)

        # Pydantic validation
        config = OrchestratorConfig(**raw_config)
        return config
```

**Configuration File Format**:
```yaml
# config.yaml
active_provider: "openai"
active_model: "gpt-4"

providers:
  openai:
    api_key: "${OPENAI_API_KEY}"
    fallback_models:
      - "gpt-4"
      - "gpt-4o-mini"

  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
    fallback_models:
      - "claude-opus-4-20250514"
      - "claude-sonnet-4-5"

  bedrock:
    region_name: "us-east-1"
    # Optional: If not provided, uses AWS credential chain
    # aws_access_key_id: "${AWS_ACCESS_KEY_ID}"
    # aws_secret_access_key: "${AWS_SECRET_ACCESS_KEY}"
    fallback_models:
      - "anthropic.claude-sonnet-4-5-v1:0"
      - "amazon.titan-text-express-v1"

  vertex:
    project_id: "my-gcp-project"
    location: "us-central1"
    # Optional: If not provided, uses Application Default Credentials
    # credentials_path: "${GOOGLE_APPLICATION_CREDENTIALS}"
    fallback_models:
      - "gemini-2-5-pro"
      - "gemini-2-5-flash"

  gemini:
    api_key: "${GEMINI_API_KEY}"
    fallback_models:
      - "gemini-2-5-pro"

cost_tracking:
  enabled: true
  log_path: "./llm_costs.log"
```

### Phase 4: Request Orchestration (Day 2-3)

**4.1 Orchestrator Implementation**

Create `orchestrator.py`:
```python
from typing import Dict, List, Iterator, Optional
from .config.manager import ConfigManager, OrchestratorConfig
from .providers.base import BaseLLMProvider, LLMResponse
from .models.registry import ModelRegistry
from .cost_tracker import CostTracker
from .exceptions import AllFallbacksFailedError, ProviderError
import logging

class LLMOrchestrator:
    """Main orchestration class."""

    def __init__(self, config_path: str):
        """Initialize with config file path."""
        self.config = ConfigManager.load_config(config_path)
        self.providers = self._initialize_providers()
        self.registry = ModelRegistry(self.providers)
        self.cost_tracker = CostTracker(
            enabled=self.config.cost_tracking.enabled,
            log_path=self.config.cost_tracking.log_path
        )
        self.session_id = self._generate_session_id()

        # Refresh models on initialization
        self.registry.refresh_models()

    def send_request(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Send non-streaming request with automatic fallback.

        Falls back to next model in fallback_models list (same provider only).
        Raises AllFallbacksFailedError if all models fail.
        """
        provider_name = self.config.active_provider
        provider = self.providers[provider_name]
        fallback_models = self.config.providers[provider_name].fallback_models

        last_error = None
        for model in fallback_models:
            try:
                response = provider.send_request(
                    messages=messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )

                # Track cost
                self.cost_tracker.log_usage(
                    provider=provider_name,
                    model=model,
                    tokens=response.tokens_used,
                    session_id=self.session_id
                )

                return response

            except Exception as e:
                logging.warning(f"Model {model} failed: {e}. Trying next fallback...")
                last_error = e
                continue

        raise AllFallbacksFailedError(
            f"All fallback models failed for {provider_name}. Last error: {last_error}"
        )

    def send_streaming_request(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Iterator[str]:
        """
        Send streaming request with automatic fallback.

        Yields content chunks as strings.
        """
        provider_name = self.config.active_provider
        provider = self.providers[provider_name]
        fallback_models = self.config.providers[provider_name].fallback_models

        # Similar fallback logic as send_request
        # Yield chunks from streaming iterator
        pass

    def get_available_models(self, provider_name: str) -> List[str]:
        """Get available models for specific provider."""
        return self.registry.get_available_models(provider_name)

    def refresh_models(self):
        """Manually refresh model lists from all providers."""
        self.registry.refresh_models()

    def get_session_cost(self) -> float:
        """Get total cost for current session."""
        return self.cost_tracker.get_session_cost(self.session_id)
```

**Fallback Logic Requirements**:
- ONLY fallback within same provider
- Iterate through `fallback_models` list in order
- Log each fallback attempt
- Raise `AllFallbacksFailedError` if all fail
- NEVER switch providers automatically

### Phase 5: Cost Tracking (Day 3)

**5.1 Cost Tracker Implementation**

Create `cost_tracker.py`:
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
import json
import csv

@dataclass
class UsageRecord:
    """Single API usage record."""
    timestamp: datetime
    provider: str
    model: str
    tokens: Dict[str, int]  # {"prompt": X, "completion": Y, "total": Z}
    cost: float
    session_id: str

class CostTracker:
    """Tracks LLM usage and costs."""

    # Pricing table (tokens per million)
    PRICING = {
        "openai": {
            "gpt-4": {"input": 30.0, "output": 60.0},
            "gpt-4o": {"input": 5.0, "output": 15.0},
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
            "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
        },
        "anthropic": {
            "claude-opus-4-20250514": {"input": 15.0, "output": 75.0},
            "claude-sonnet-4-20250514": {"input": 3.0, "output": 15.0},
            "claude-opus-4-1": {"input": 15.0, "output": 75.0},
            "claude-sonnet-4-5": {"input": 3.0, "output": 15.0},
            "claude-haiku-4-5": {"input": 0.25, "output": 1.25},
        },
        "gemini": {
            "gemini-2-5-pro": {"input": 0.50, "output": 1.50},
            "gemini-pro-vision": {"input": 0.50, "output": 1.50},
        },
        "bedrock": {
            # Anthropic Claude on Bedrock (us-east-1 pricing)
            "anthropic.claude-opus-4-1-v1:0": {"input": 15.0, "output": 75.0},
            "anthropic.claude-sonnet-4-5-v1:0": {"input": 3.0, "output": 15.0},
            "anthropic.claude-haiku-4-5-v1:0": {"input": 0.25, "output": 1.25},
            # Amazon Titan
            "amazon.titan-text-express-v1": {"input": 0.80, "output": 1.60},
            "amazon.titan-text-lite-v1": {"input": 0.30, "output": 0.40},
            # AI21 Labs
            "ai21.j2-ultra-v1": {"input": 15.0, "output": 15.0},
            "ai21.j2-mid-v1": {"input": 12.5, "output": 12.5},
            # Cohere
            "cohere.command-text-v14": {"input": 1.50, "output": 2.00},
            "cohere.command-light-text-v14": {"input": 0.30, "output": 0.60},
            # Meta Llama
            "meta.llama2-13b-chat-v1": {"input": 0.75, "output": 1.00},
            "meta.llama2-70b-chat-v1": {"input": 1.95, "output": 2.56},
        },
        "vertex": {
            "gemini-2-5-pro": {"input": 0.50, "output": 1.50},
            "gemini-2-5-pro": {"input": 3.50, "output": 10.50},
            "gemini-2-5-flash": {"input": 0.35, "output": 1.05},
            "gemini-pro-vision": {"input": 0.50, "output": 1.50},
        }
    }

    def __init__(self, enabled: bool = True, log_path: str = "./llm_costs.log"):
        self.enabled = enabled
        self.log_path = log_path
        self.records: List[UsageRecord] = []

    def log_usage(
        self,
        provider: str,
        model: str,
        tokens: Dict[str, int],
        session_id: str
    ):
        """Log API usage with cost calculation."""
        if not self.enabled:
            return

        cost = self._calculate_cost(provider, model, tokens)

        record = UsageRecord(
            timestamp=datetime.now(),
            provider=provider,
            model=model,
            tokens=tokens,
            cost=cost,
            session_id=session_id
        )

        self.records.append(record)
        self._write_to_log(record)

    def _calculate_cost(
        self,
        provider: str,
        model: str,
        tokens: Dict[str, int]
    ) -> float:
        """Calculate cost based on pricing table."""
        pricing = self.PRICING.get(provider, {}).get(model)
        if not pricing:
            return 0.0

        input_cost = (tokens["prompt"] / 1_000_000) * pricing["input"]
        output_cost = (tokens["completion"] / 1_000_000) * pricing["output"]

        return input_cost + output_cost

    def get_session_cost(self, session_id: str) -> float:
        """Get total cost for specific session."""
        return sum(
            r.cost for r in self.records
            if r.session_id == session_id
        )

    def get_usage_report(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """Generate usage report with aggregations."""
        # Filter by date range
        # Aggregate by provider, model, session
        # Return summary statistics
        pass

    def export_to_csv(self, output_path: str):
        """Export usage records to CSV."""
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "provider", "model",
                "prompt_tokens", "completion_tokens",
                "total_tokens", "cost", "session_id"
            ])

            for record in self.records:
                writer.writerow([
                    record.timestamp.isoformat(),
                    record.provider,
                    record.model,
                    record.tokens["prompt"],
                    record.tokens["completion"],
                    record.tokens["total"],
                    f"${record.cost:.4f}",
                    record.session_id
                ])
```

### Phase 6: Exception Handling (Day 3)

**6.1 Custom Exceptions**

Create `exceptions.py`:
```python
class OrchestratorError(Exception):
    """Base exception for orchestrator."""
    pass

class ProviderError(OrchestratorError):
    """Provider-specific error."""
    pass

class AllFallbacksFailedError(OrchestratorError):
    """All fallback models failed."""
    pass

class ConfigurationError(OrchestratorError):
    """Invalid configuration."""
    pass

class ModelNotFoundError(OrchestratorError):
    """Requested model not available."""
    pass
```

---

## MODULE STRUCTURE

Create this exact directory structure:

```
llm_orchestrator/
├── __init__.py                 # Export main classes
├── providers/
│   ├── __init__.py
│   ├── base.py                 # Abstract base class
│   ├── openai_adapter.py       # OpenAI implementation
│   ├── anthropic_adapter.py    # Anthropic implementation
│   ├── gemini_adapter.py       # Gemini implementation
│   ├── bedrock_adapter.py      # AWS Bedrock implementation
│   └── vertex_adapter.py       # Google Vertex AI implementation
├── models/
│   ├── __init__.py
│   └── registry.py             # Model discovery and caching
├── config/
│   ├── __init__.py
│   └── manager.py              # YAML config handling
├── orchestrator.py             # Main orchestration logic
├── cost_tracker.py             # Usage and cost tracking
├── exceptions.py               # Custom exceptions
└── tests/
    ├── __init__.py
    ├── test_model_discovery.py
    ├── test_providers.py
    ├── test_bedrock.py         # Bedrock-specific tests
    ├── test_vertex.py          # Vertex-specific tests
    ├── test_config.py
    ├── test_cost_tracking.py
    └── conftest.py             # pytest fixtures
```

---

## TESTING REQUIREMENTS

### Test 1: Model Discovery (`test_model_discovery.py`)

```python
import pytest
from llm_orchestrator.models.registry import ModelRegistry
from unittest.mock import Mock, patch

def test_fetch_openai_models():
    """Verify OpenAI API returns model list."""
    # Use real API call with try/except for CI
    # Verify structure: list of strings
    # Check for expected models (gpt-4, gpt-4o-mini)
    pass

def test_model_caching():
    """Verify caching mechanism works."""
    # Call refresh_models()
    # Check cache is populated
    # Call get_available_models()
    # Verify no API call is made (use mock)
    pass

def test_deprecated_model_marking():
    """Test deprecated flag when model removed."""
    # Mock first API response with 3 models
    # Mock second API response with 2 models
    # Verify missing model marked deprecated
    pass

@pytest.mark.integration
def test_all_providers_model_discovery():
    """Integration test for all five providers."""
    # Requires real API keys
    # Test each provider returns models
    # Validate response structure
    pass
```

### Test 2: Provider Integration (`test_providers.py`)

```python
import pytest

@pytest.mark.integration
def test_openai_request():
    """Test OpenAI adapter with real API."""
    # Use cheapest model (gpt-4o-mini)
    # Send simple request
    # Verify response normalization
    # Check token counting
    pass

@pytest.mark.integration
def test_streaming_response():
    """Test streaming for all providers."""
    # Test iterator pattern
    # Verify chunks are strings
    # Check final content matches expected
    pass

def test_error_handling():
    """Test provider error mapping."""
    # Mock API errors (rate limit, auth, invalid model)
    # Verify mapped to common exceptions
    pass
```

### Test 3: Configuration (`test_config.py`)

```python
def test_yaml_parsing():
    """Test YAML config loading."""
    # Create temp config file
    # Load with ConfigManager
    # Verify structure
    pass

def test_env_var_resolution():
    """Test ${VAR} replacement."""
    # Set environment variable
    # Load config with ${VAR}
    # Verify resolved value
    pass

def test_invalid_config():
    """Test validation errors."""
    # Missing required fields
    # Invalid provider name
    # Should raise ConfigurationError
    pass
```

### Test 4: Cost Tracking (`test_cost_tracking.py`)

```python
def test_cost_calculation():
    """Test cost calculation accuracy."""
    # Mock usage with known token counts
    # Calculate expected cost
    # Verify CostTracker.calculate_cost() matches
    pass

def test_session_cost_aggregation():
    """Test per-session cost tracking."""
    # Log multiple requests with same session_id
    # Call get_session_cost()
    # Verify sum is correct
    pass

def test_csv_export():
    """Test CSV export format."""
    # Log some usage
    # Export to temp file
    # Read CSV and verify structure
    pass
```

---

## USAGE EXAMPLE

The system should be used like this:

```python
from llm_orchestrator import LLMOrchestrator

# Initialize with config file
orchestrator = LLMOrchestrator("config.yaml")

# Check available models for each provider
openai_models = orchestrator.get_available_models("openai")
bedrock_models = orchestrator.get_available_models("bedrock")
vertex_models = orchestrator.get_available_models("vertex")

print(f"OpenAI: {len(openai_models)} models")
print(f"Bedrock: {len(bedrock_models)} models")
print(f"Vertex: {len(vertex_models)} models")

# Send non-streaming request
response = orchestrator.send_request(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is 2+2?"}
    ],
    temperature=0.7
)

print(f"Response: {response.content}")
print(f"Tokens used: {response.tokens_used}")

# Send streaming request
print("Streaming response:")
for chunk in orchestrator.send_streaming_request(
    messages=[{"role": "user", "content": "Count to 10"}],
    temperature=0.5
):
    print(chunk, end='', flush=True)

# Get session cost
cost = orchestrator.get_session_cost()
print(f"\nTotal session cost: ${cost:.4f}")

# Refresh model list (manual)
orchestrator.refresh_models()

# Export cost report
orchestrator.cost_tracker.export_to_csv("usage_report.csv")
```

---

## KEY CONSTRAINTS

**DO NOT**:
- ❌ Implement provider switching mid-conversation
- ❌ Implement automatic cross-provider fallback
- ❌ Include fine-tuned model support
- ❌ Implement request queuing or rate limiting in v1
- ❌ Implement hot-reload configuration
- ❌ Use hardcoded model lists

**DO**:
- ✅ Maintain backward compatibility for deprecated models
- ✅ Use type hints throughout
- ✅ Implement proper error handling and logging
- ✅ Follow adapter pattern strictly
- ✅ Write comprehensive tests
- ✅ Document all public methods

---

## IMPLEMENTATION CHECKLIST

Phase 1 - Base Adapters:
- [ ] Create abstract base class with all required methods
- [ ] Implement OpenAI adapter with error mapping
- [ ] Implement Anthropic adapter with message format conversion
- [ ] Implement Gemini adapter with safety settings
- [ ] Test each adapter independently

Phase 2 - Model Registry:
- [ ] Implement model caching with timestamps
- [ ] Add refresh_models() method
- [ ] Add deprecated model tracking
- [ ] Filter out fine-tuned models
- [ ] Test caching and deprecation logic

Phase 3 - Configuration:
- [ ] Create Pydantic models for config validation
- [ ] Implement environment variable resolution
- [ ] Add config file loading
- [ ] Test validation edge cases

Phase 4 - Orchestration:
- [ ] Implement request routing
- [ ] Add within-provider fallback logic
- [ ] Add conversation context management
- [ ] Implement both streaming and non-streaming
- [ ] Test fallback scenarios

Phase 5 - Cost Tracking:
- [ ] Implement cost calculation with pricing table
- [ ] Add usage logging to file
- [ ] Implement session cost tracking
- [ ] Add CSV export functionality
- [ ] Test cost calculation accuracy

Phase 6 - Testing:
- [ ] Write unit tests for all components
- [ ] Write integration tests with real APIs
- [ ] Add CI/CD with mocked tests
- [ ] Verify 90%+ code coverage

---

## OUTPUT REQUIREMENTS

Provide complete, production-ready code including:

1. **All module files** with proper docstrings and type hints
2. **Complete test suite** with pytest fixtures
3. **Example config.yaml** file
4. **requirements.txt** or pyproject.toml
5. **README.md** with:
   - Installation instructions
   - Quick start guide
   - Configuration reference
   - API documentation
   - Testing instructions
6. **Example usage scripts** demonstrating common scenarios

Generate code that is:
- PEP 8 compliant
- Fully type-hinted
- Well-documented with docstrings
- Tested with pytest
- Production-ready (error handling, logging, validation)
```

**Performance**: Generates complete library implementation in 30-45 minutes with Claude Opus.

---

## Model-Specific Optimizations

### Claude (Anthropic) - System Architecture Design

**Complexity**: 🔴 Advanced

Claude Opus excels at complex system design with multiple interacting components and proper separation of concerns.

```xml
<role>
You are a senior Python architect with 10+ years of experience building production-grade
libraries for enterprise applications. You specialize in API design, adapter patterns,
distributed systems, and creating maintainable, well-tested Python packages.
</role>

<task>
Build a complete Python library for multi-provider LLM orchestration with unified interface,
dynamic model discovery, intelligent fallback, and comprehensive cost tracking.
</task>

<context>
This library will be:
- Imported into existing Python applications (not a standalone service)
- Used in production with real API calls and costs
- Maintained by multiple developers over years
- Extended with new providers and features
- Tested in CI/CD pipelines
</context>

<architecture_requirements>

<core_principles>
  - Adapter pattern for provider abstraction
  - Dependency injection for testability
  - Configuration-driven behavior
  - Fail-fast validation
  - Comprehensive error handling
  - Production-grade logging
</core_principles>

<implementation_phases>
  <phase number="1" name="Base Provider Adapters">
    <deliverables>
      - Abstract base class (providers/base.py)
      - LLMResponse dataclass with normalized fields
      - OpenAI adapter with error mapping
      - Anthropic adapter with message conversion
      - Gemini adapter with safety settings
    </deliverables>

    <validation>
      - Each adapter passes unit tests
      - Response format is identical across providers
      - Errors are properly caught and mapped
      - Streaming works for all providers
    </validation>
  </phase>

  <phase number="2" name="Model Registry">
    <deliverables>
      - ModelRegistry class with caching
      - refresh_models() method
      - Deprecated model tracking
      - Fine-tuned model filtering
    </deliverables>

    <requirements>
      - Cache models with timestamps
      - Manual refresh only (no auto-refresh)
      - Mark removed models as deprecated (don't delete)
      - Exclude models with "ft-" prefix
    </requirements>
  </phase>

  <phase number="3" name="Configuration System">
    <deliverables>
      - Pydantic models for validation
      - YAML loading with env var resolution
      - ConfigManager class
    </deliverables>

    <config_schema>
<![CDATA[
active_provider: str
active_model: str
providers:
  <provider_name>:
    api_key: str  # Supports ${ENV_VAR} syntax
    fallback_models: List[str]
cost_tracking:
  enabled: bool
  log_path: str
]]>
    </config_schema>
  </phase>

  <phase number="4" name="Request Orchestration">
    <deliverables>
      - LLMOrchestrator main class
      - send_request() method
      - send_streaming_request() method
      - Fallback logic (within provider only)
    </deliverables>

    <fallback_logic>
      <rules>
        - Only fallback within same provider
        - Iterate through fallback_models in order
        - Log each fallback attempt
        - Raise AllFallbacksFailedError if all fail
        - NEVER switch providers automatically
      </rules>
    </fallback_logic>
  </phase>

  <phase number="5" name="Cost Tracking">
    <deliverables>
      - CostTracker class
      - Pricing table (hardcoded for v1)
      - log_usage() method
      - get_session_cost() method
      - CSV export functionality
    </deliverables>

    <tracking_fields>
      - timestamp
      - provider
      - model
      - tokens (prompt, completion, total)
      - calculated cost
      - session_id
    </tracking_fields>
  </phase>

  <phase number="6" name="Testing">
    <deliverables>
      - test_model_discovery.py
      - test_providers.py (integration tests)
      - test_config.py
      - test_cost_tracking.py
      - conftest.py with fixtures
    </deliverables>

    <coverage_targets>
      - Overall: 90%+
      - Core logic: 95%+
      - Adapters: 85%+ (some provider-specific code)
    </coverage_targets>
  </phase>
</implementation_phases>

</architecture_requirements>

<code_standards>
  <python_version>3.9+</python_version>

  <type_hints>
    - All function signatures must have type hints
    - All class attributes must have type annotations
    - Use typing.Optional, typing.Dict, etc.
  </type_hints>

  <docstrings>
    - All public methods need docstrings
    - Use Google style docstrings
    - Include Args, Returns, Raises sections
  </docstrings>

  <error_handling>
    - Catch provider-specific errors
    - Map to common exception types
    - Log all errors with context
    - Provide helpful error messages
  </error_handling>

  <logging>
    - Use Python logging module
    - Log at appropriate levels (DEBUG, INFO, WARNING, ERROR)
    - Include context in log messages
    - Don't log sensitive data (API keys)
  </logging>
</code_standards>

<testing_strategy>
  <unit_tests>
    - Test individual methods in isolation
    - Use mocks for external dependencies
    - Fast execution (&lt;100ms per test)
  </unit_tests>

  <integration_tests>
    - Mark with @pytest.mark.integration
    - Use real API calls (smallest/cheapest models)
    - May be skipped in CI without API keys
    - Verify end-to-end functionality
  </integration_tests>

  <test_fixtures>
    - Mock provider responses
    - Sample configuration files
    - Reusable test data
  </test_fixtures>
</testing_strategy>

<module_structure>
<![CDATA[
llm_orchestrator/
├── __init__.py                 # Export LLMOrchestrator
├── providers/
│   ├── __init__.py
│   ├── base.py                 # BaseLLMProvider, LLMResponse
│   ├── openai_adapter.py
│   ├── anthropic_adapter.py
│   └── gemini_adapter.py
├── models/
│   ├── __init__.py
│   └── registry.py             # ModelRegistry
├── config/
│   ├── __init__.py
│   └── manager.py              # ConfigManager, Pydantic models
├── orchestrator.py             # LLMOrchestrator
├── cost_tracker.py             # CostTracker
├── exceptions.py               # Custom exceptions
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_model_discovery.py
    ├── test_providers.py
    ├── test_config.py
    └── test_cost_tracking.py
]]>
</module_structure>

<constraints>
  <forbidden>
    - NO provider switching mid-conversation
    - NO automatic cross-provider fallback
    - NO fine-tuned model support
    - NO request queuing in v1
    - NO hot-reload configuration
    - NO hardcoded model lists
  </forbidden>

  <required>
    - Backward compatibility for deprecated models
    - Type hints throughout
    - Proper error handling
    - Adapter pattern strictly followed
    - Comprehensive tests (90%+ coverage)
    - Complete documentation
  </required>
</constraints>

<output_format>
  <deliverables>
    1. Complete source code for all modules
    2. Full test suite with pytest
    3. requirements.txt or pyproject.toml
    4. Example config.yaml
    5. README.md with:
       - Installation instructions
       - Quick start guide
       - Configuration reference
       - API documentation
       - Testing guide
    6. Example usage scripts
  </deliverables>

  <code_quality>
    - PEP 8 compliant
    - Black formatted
    - Fully type-hinted
    - Docstrings on all public APIs
    - Production-ready error handling
    - Proper logging throughout
  </code_quality>
</output_format>

</xml>
```

**Performance**:
- Code generation: 30-45 minutes with Claude Opus
- Test coverage: 90-95% achievable
- Lines of code: ~1500-2000 total
- Cost: ~$2-5 for complete generation

---

## Production Patterns

### Pattern 1: Gradual Provider Migration

**Use case**: Migrate from one provider to another without downtime.

```python
# Week 1: Add new provider to config
# config.yaml
active_provider: "openai"  # Still using OpenAI
active_model: "gpt-4"

providers:
  openai:
    api_key: "${OPENAI_API_KEY}"
    fallback_models: ["gpt-4", "gpt-4o-mini"]

  anthropic:  # Add Anthropic
    api_key: "${ANTHROPIC_API_KEY}"
    fallback_models: ["claude-opus-4-20250514"]

# Week 2: Test Anthropic integration
from llm_orchestrator import LLMOrchestrator

orchestrator = LLMOrchestrator("config.yaml")

# Verify Anthropic models available
anthropic_models = orchestrator.get_available_models("anthropic")
print(f"Anthropic ready: {len(anthropic_models)} models")

# Week 3: Switch active provider
# config.yaml
active_provider: "anthropic"  # Switch!
active_model: "claude-opus-4-20250514"

# No code changes needed - just config update
```

### Pattern 2: Cost-Aware Model Selection

**Use case**: Track costs across different models to optimize spending.

```python
from llm_orchestrator import LLMOrchestrator
import pandas as pd

# Run experiment with different models
configs = [
    ("openai", "gpt-4"),
    ("openai", "gpt-4o-mini"),
    ("anthropic", "claude-sonnet-4-5"),
]

results = []

for provider, model in configs:
    # Update config
    orchestrator = LLMOrchestrator("config.yaml")

    # Run same prompt 100 times
    for i in range(100):
        response = orchestrator.send_request(
            messages=[{"role": "user", "content": "Summarize quantum physics in 50 words"}],
            temperature=0.7
        )

    # Get cost
    cost = orchestrator.get_session_cost()
    results.append({
        "provider": provider,
        "model": model,
        "cost": cost,
        "cost_per_request": cost / 100
    })

# Analyze results
df = pd.DataFrame(results)
print(df.sort_values("cost"))

# Output:
#     provider                          model      cost  cost_per_request
# 1    openai              gpt-4o-mini   0.42          0.0042
# 2  anthropic  claude-sonnet-4-5   1.85          0.0185
# 0    openai                      gpt-4   6.30          0.0630
```

### Pattern 3: Multi-Environment Configuration

**Use case**: Different configs for dev/staging/production.

```python
# config.dev.yaml (cheap models for testing)
active_provider: "openai"
active_model: "gpt-4o-mini"

providers:
  openai:
    api_key: "${OPENAI_API_KEY}"
    fallback_models: ["gpt-4o-mini"]

cost_tracking:
  enabled: true
  log_path: "./dev_costs.log"

# config.prod.yaml (production models)
active_provider: "anthropic"
active_model: "claude-opus-4-20250514"

providers:
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
    fallback_models:
      - "claude-opus-4-20250514"
      - "claude-sonnet-4-5"  # Fallback to cheaper

cost_tracking:
  enabled: true
  log_path: "/var/log/llm_costs.log"

# Application code
import os
from llm_orchestrator import LLMOrchestrator

env = os.getenv("ENVIRONMENT", "dev")
config_file = f"config.{env}.yaml"

orchestrator = LLMOrchestrator(config_file)
```

---

## Usage Examples

### Example 1: Simple Chatbot Integration

**Input**:
```python
from llm_orchestrator import LLMOrchestrator

# Initialize
orchestrator = LLMOrchestrator("config.yaml")

# Chatbot loop
conversation = []

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break

    conversation.append({"role": "user", "content": user_input})

    response = orchestrator.send_request(
        messages=conversation,
        temperature=0.7
    )

    print(f"Bot: {response.content}")
    conversation.append({"role": "assistant", "content": response.content})

# Show session cost
cost = orchestrator.get_session_cost()
print(f"\nTotal cost: ${cost:.4f}")
```

**Expected Output**:
```
You: Hello!
Bot: Hello! How can I help you today?
You: What's the weather like?
Bot: I don't have access to real-time weather data...
You: quit

Total cost: $0.0023
```

---

### Example 2: Streaming Response for UI

**Input**:
```python
from llm_orchestrator import LLMOrchestrator
import sys

orchestrator = LLMOrchestrator("config.yaml")

print("Asking for story... (streaming)\n")

for chunk in orchestrator.send_streaming_request(
    messages=[{
        "role": "user",
        "content": "Write a 3-sentence story about a robot."
    }],
    temperature=0.8
):
    print(chunk, end='', flush=True)
    sys.stdout.flush()

print("\n\nDone!")
```

**Expected Output**:
```
Asking for story... (streaming)

Once upon a time, there was a robot named Bolt who dreamed of becoming a chef.
He practiced day and night, learning to cook with precision and care.
Eventually, he opened the first robot-run restaurant, delighting customers
with perfectly prepared meals.

Done!
```

---

### Example 3: Cost Reporting Dashboard

**Input**:
```python
from llm_orchestrator import LLMOrchestrator
from datetime import datetime, timedelta

orchestrator = LLMOrchestrator("config.yaml")

# Generate usage report
report = orchestrator.cost_tracker.get_usage_report(
    start_date=datetime.now() - timedelta(days=7),
    end_date=datetime.now()
)

print("=== 7-Day Usage Report ===")
print(f"Total Requests: {report['total_requests']}")
print(f"Total Tokens: {report['total_tokens']:,}")
print(f"Total Cost: ${report['total_cost']:.2f}")

print("\nBy Provider:")
for provider, data in report['by_provider'].items():
    print(f"  {provider}: ${data['cost']:.2f} ({data['requests']} requests)")

print("\nBy Model:")
for model, data in report['by_model'].items():
    print(f"  {model}: ${data['cost']:.2f}")

# Export to CSV
orchestrator.cost_tracker.export_to_csv("usage_last_7_days.csv")
print("\nExported to usage_last_7_days.csv")
```

**Expected Output**:
```
=== 7-Day Usage Report ===
Total Requests: 1,247
Total Tokens: 823,491
Total Cost: $12.34

By Provider:
  openai: $8.23 (892 requests)
  anthropic: $4.11 (355 requests)

By Model:
  gpt-4: $6.50
  gpt-4o-mini: $1.73
  claude-opus-4-20250514: $4.11

Exported to usage_last_7_days.csv
```

---

## Quality Evaluation

### Before (Direct Provider Integration)

**Problems**:
- ❌ Different API for each provider (openai vs anthropic vs genai)
- ❌ No unified error handling
- ❌ Manual cost tracking with spreadsheets
- ❌ Hard to switch providers (code changes required)
- ❌ No fallback logic (single point of failure)
- ❌ No model discovery (hardcoded model names)

**Code Example**:
```python
# Different code for each provider
import openai
import anthropic

# OpenAI
openai_response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)

# Anthropic (completely different API)
anthropic_client = anthropic.Anthropic(api_key="...")
anthropic_response = anthropic_client.messages.create(
    model="claude-opus-4-20250514",
    messages=[{"role": "user", "content": "Hello"}]
)

# No unified interface - can't swap easily
```

### After (Orchestrator Implementation)

**Improvements**:
- ✅ Single unified interface for all providers
- ✅ Automatic fallback within provider
- ✅ Comprehensive cost tracking and reporting
- ✅ Easy provider switching via config
- ✅ Dynamic model discovery
- ✅ Production-ready error handling

**Code Example**:
```python
from llm_orchestrator import LLMOrchestrator

# Same code works for any provider
orchestrator = LLMOrchestrator("config.yaml")

# Works regardless of active provider
response = orchestrator.send_request(
    messages=[{"role": "user", "content": "Hello"}]
)

# Automatic fallback, cost tracking, error handling
print(response.content)
print(f"Cost: ${orchestrator.get_session_cost():.4f}")

# Switch providers: just edit config.yaml, no code changes
```

---

## Cost Comparison

| Approach | Development Time | Maintenance | Flexibility | Cost Visibility |
|----------|------------------|-------------|-------------|-----------------|
| **Direct integration** | 2-3 days per provider | High (3 codebases) | Low | Manual tracking |
| **Wrapper functions** | 3-4 days | Medium | Medium | Basic logging |
| **This orchestrator** | 2-3 days (one time) | Low (unified) | High | Complete tracking |

**ROI Calculation**:
- Initial development: 2-3 days
- Savings per provider addition: 1-2 days
- Maintenance reduction: 60-70%
- Cost visibility: Priceless (enables optimization)
- **Payback**: After 2nd provider integration

---

## Customization Tips

1. **Add New Provider**
   - Create new adapter class extending `BaseLLMProvider`
   - Implement all abstract methods
   - Add pricing to `CostTracker.PRICING`
   - Add tests in `test_providers.py`
   - Update config schema if needed

2. **Custom Cost Tracking**
   - Extend `CostTracker` with additional fields
   - Add methods for custom aggregations (by user, by feature, etc.)
   - Implement custom export formats (JSON, Parquet, etc.)

3. **Provider-Specific Features**
   - Add optional kwargs to adapter methods
   - Pass through to provider APIs
   - Document which kwargs work with which providers
   - Example: `tools` for OpenAI, `system` for Anthropic

4. **Cross-Provider Fallback** (Future)
   - Add `cross_provider_fallback: true` to config
   - Implement provider switching logic in orchestrator
   - Handle conversation history conversion
   - Add tests for cross-provider scenarios

5. **Request Queuing** (Future)
   - Add `queue_config` section to YAML
   - Implement request queue with rate limiting
   - Add priority levels for requests
   - Monitor queue depth and latency

---

## Testing Checklist

### Unit Tests
- [ ] All adapter methods have unit tests
- [ ] Config validation tested with invalid inputs
- [ ] Cost calculation tested with known values
- [ ] Model registry caching logic tested
- [ ] Fallback logic tested with mocked failures

### Integration Tests
- [ ] OpenAI adapter works with real API
- [ ] Anthropic adapter works with real API
- [ ] Gemini adapter works with real API
- [ ] Streaming works for all providers
- [ ] Model discovery returns expected formats

### System Tests
- [ ] End-to-end chatbot scenario
- [ ] Provider switching via config change
- [ ] Cost tracking accuracy over 100 requests
- [ ] Fallback works with real API failures
- [ ] Session cost aggregation is correct

### Quality Criteria
- Code coverage: 90%+
- All integration tests pass with API keys
- No hardcoded secrets or API keys
- All public methods have docstrings
- Type hints on all function signatures
- PEP 8 compliant

### Common Failure Modes

| Failure | Symptom | Fix |
|---------|---------|-----|
| **API key not found** | `KeyError` on initialization | Check environment variables are set |
| **Model not available** | `ModelNotFoundError` | Refresh models, check spelling |
| **All fallbacks fail** | `AllFallbacksFailedError` | Check API keys, rate limits, model availability |
| **Cost calculation wrong** | Negative or zero cost | Update pricing table with current rates |
| **Streaming hangs** | Iterator never completes | Check for unclosed connections, add timeouts |

---

## Common Issues & Fixes

### Issue 1: Import Errors

**Problem**: `ModuleNotFoundError: No module named 'llm_orchestrator'`

**Fix**: Install in development mode
```bash
# From project root
pip install -e .

# Or install dependencies
pip install -r requirements.txt
```

### Issue 2: API Keys Not Resolved

**Problem**: Config shows `${OPENAI_API_KEY}` literally instead of actual key.

**Fix**: Ensure environment variables are set
```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="..."

# Verify
echo $OPENAI_API_KEY
```

### Issue 3: Model Not Found

**Problem**: `ModelNotFoundError: gpt-4o not found`

**Fix**: Refresh model registry
```python
orchestrator = LLMOrchestrator("config.yaml")
orchestrator.refresh_models()  # Fetch latest models

# Check available models
models = orchestrator.get_available_models("openai")
print(models)
```

### Issue 4: Streaming Not Working

**Problem**: Streaming request returns all content at once.

**Fix**: Ensure you're iterating properly
```python
# Wrong - consumes iterator immediately
response = orchestrator.send_streaming_request(messages)
print(response)  # Iterator object, not content

# Correct - iterate over chunks
for chunk in orchestrator.send_streaming_request(messages):
    print(chunk, end='', flush=True)
```

---

## Related Prompts

- [Code Review & Refactoring](./code-review-refactoring.md) - For reviewing generated code
- [Enterprise README Generator](./enterprise-readme-generator.md) - For creating library documentation

---

**Success Metrics**:

After implementing this system, you should achieve:
- ✅ Single unified interface for 5 major providers
- ✅ 90%+ test coverage
- ✅ <1% request failure rate with fallback
- ✅ 100% cost visibility and tracking across all providers
- ✅ <5 minute provider switching time
- ✅ Zero vendor lock-in
- ✅ Multi-cloud deployment ready (AWS + GCP)
- ✅ 30-70% cost reduction through provider optimization
- ✅ Support for 20+ different models
- ✅ Enterprise-grade security (IAM, Workload Identity)

**Real-World Impact**:
- **Development Time Saved**: 2-3 days per additional provider integration
- **Maintenance Reduction**: 60-70% less code to maintain vs separate integrations
- **Cost Optimization**: $500-5000/month savings through optimal model selection
- **Flexibility**: Switch providers in <5 minutes vs days of refactoring
- **Reliability**: <0.5% failure rate with 3-model fallback chains

**Remember**: This is production infrastructure - prioritize reliability, testability, maintainability, and security over features. Build incrementally and test thoroughly at each phase. Use appropriate authentication methods for each environment (dev vs production). Consider cloud provider egress charges and regional availability when selecting providers. Always follow security best practices for credential management.
