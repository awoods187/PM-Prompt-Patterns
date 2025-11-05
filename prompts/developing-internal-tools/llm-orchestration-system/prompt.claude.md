# Multi-Provider LLM Orchestration System - Claude Optimized

> Extends `prompt.md` with Claude-specific optimizations

## Prompt

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

## Claude Optimizations Applied

- **XML structure**: Uses XML tags for clear task delineation and better parsing
- **Structured thinking**: Encourages use of `<thinking>` tags for complex reasoning
- **Prompt caching**: Static prompt content is cacheable for 90%+ cost savings
- **Extended context**: Leverages Claude's 200K token context window

## Usage

```python
from pm_prompt_toolkit.providers import get_provider

# Initialize Claude provider with caching
provider = get_provider("claude-sonnet-4-5", enable_caching=True)

result = provider.generate(
    system_prompt="<prompt from above>",
    user_message="<your content here>"
)
```

## See Also

- Base prompt: `prompt.md` (examples, testing checklist, business value)
- Provider documentation: `../../docs/provider-specific-prompts.md`
