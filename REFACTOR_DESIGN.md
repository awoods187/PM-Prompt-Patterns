# AI Model Management System Refactor Design

**Status**: Design Phase
**Created**: 2025-10-24
**Owner**: Architecture Team

---

## Executive Summary

This document outlines a comprehensive refactor of the AI model management system to consolidate three fragmented packages (`models/`, `providers/`, `model-configs/`) into a unified, maintainable architecture.

**Key Goals**:
- Single source of truth for model information
- Extensible provider system with dynamic registration
- Explicit capability matrix for model selection
- Centralized pricing management
- Zero breaking changes during migration

**Expected Outcomes**:
- 50% reduction in time to add new models/providers
- Elimination of duplicate/conflicting model information
- Foundation for advanced features (dynamic pricing, smart model selection)

---

## Architecture Decision Records (ADRs)

### ADR-001: Consolidate model-configs into models package

**Status**: ✅ Approved
**Date**: 2025-10-24

**Context**:
The `model-configs/` directory was created to house model-specific optimization guides but:
- All files are empty placeholders (never populated)
- Intended content lives in `MODEL_OPTIMIZATION_GUIDE.md`
- Creates unnecessary cognitive overhead (where should model info go?)
- References outdated model names (gpt-4-turbo, gpt-3.5, etc.)

**Decision**:
Merge configuration guidance into the `models/` package as structured metadata within model definitions.

**Rationale**:
- Single source of truth for all model information
- Reduces package sprawl (3 packages → 1 unified package)
- Co-locates specifications with optimization guidance
- Programmatically accessible (can query capabilities, not just read docs)

**Consequences**:
- ✅ Developers only need to look in one place
- ✅ Model definitions become comprehensive
- ✅ Can version optimization guidance with models
- ⚠️ Larger models/ package scope (acceptable trade-off)
- ⚠️ Need migration script for existing references

**Alternatives Considered**:
1. **Keep separate** - Rejected: Adds no value, just complexity
2. **Delete model-configs/** - Rejected: Loses intended functionality
3. **Populate model-configs/** - Rejected: Duplicates info from registry

**Implementation**:
```python
# Model definition includes optimization guidance
ModelDefinition = {
    "specs": {...},           # From current models/registry.py
    "optimization": {...},    # From MODEL_OPTIMIZATION_GUIDE.md
    "capabilities": {...},    # New capability matrix
    "pricing_ref": "..."     # Reference to pricing service
}
```

---

### ADR-002: Implement Registry Pattern for Provider Management

**Status**: ✅ Approved
**Date**: 2025-10-24

**Context**:
Current state:
- Providers partially use registry pattern (factory.py exists)
- Still have hardcoded pricing in `claude.py`: `CLAUDE_PRICING = {...}`
- Model IDs now import from registry (good!) but pricing doesn't
- Adding new providers requires editing multiple files

**Decision**:
Complete migration to full registry pattern with:
- Dynamic provider registration (no hardcoded imports)
- Runtime provider discovery
- Standardized provider interface (already exists via base.py)
- All configuration external (no hardcoded prices)

**Rationale**:
- Extensible: New providers can register without core changes
- Testable: Easy to mock providers for testing
- Flexible: Can swap providers at runtime
- Maintainable: Clear separation of concerns

**Consequences**:
- ✅ Plugin architecture for providers
- ✅ Runtime provider discovery and selection
- ✅ Easier testing with mock providers
- ✅ No core code changes to add providers
- ⚠️ Additional abstraction layer (minimal cost)
- ⚠️ Need to update existing provider implementations

**Implementation**:
```python
# Provider registry pattern
class ProviderRegistry:
    _providers = {}

    @classmethod
    def register(cls, name: str, provider_class: Type[LLMProvider]):
        """Register a provider."""
        cls._providers[name] = provider_class

    @classmethod
    def get(cls, name: str) -> LLMProvider:
        """Get registered provider."""
        return cls._providers[name]

# Providers self-register
@ProviderRegistry.register("claude")
class ClaudeProvider(LLMProvider):
    ...
```

**Migration Path**:
1. Phase 1: Implement registry alongside existing code
2. Phase 2: Update providers to use registry
3. Phase 3: Remove old factory pattern
4. Phase 4: Deprecate direct imports

---

### ADR-003: Extract Pricing as First-Class Concern

**Status**: ✅ Approved
**Date**: 2025-10-24

**Context**:
Current problems:
- Pricing hardcoded in providers: `CLAUDE_PRICING = {(0.25, 1.25), ...}`
- Pricing also in models/registry.py: `input_price_per_1m=3.00`
- Same info in two places → drift and inconsistency
- Can't track historical pricing
- Can't implement dynamic pricing strategies

**Example of current duplication**:
```python
# In providers/claude.py (WRONG - hardcoded)
CLAUDE_PRICING = {
    "claude-haiku": (0.25, 1.25),  # ❌ Outdated! Should be (1.00, 5.00)
}

# In models/registry.py (CORRECT)
CLAUDE_HAIKU = ModelSpec(
    input_price_per_1m=1.00,  # ✅ Current
    output_price_per_1m=5.00,
)
```

**Decision**:
Create a dedicated pricing service that both models and providers can query.

**Rationale**:
- Single source of truth for pricing
- Support for versioned pricing (track changes over time)
- Enable dynamic pricing strategies (volume discounts, regional pricing)
- Historical pricing for cost analysis

**Consequences**:
- ✅ Single place to update pricing (no more drift)
- ✅ Support for dynamic pricing strategies
- ✅ Historical pricing tracking capability
- ✅ Can implement cost optimization recommendations
- ⚠️ Additional service to maintain
- ⚠️ Need to ensure pricing service is performant (caching)

**Implementation**:
```python
# Pricing service
class PricingService:
    def get_pricing(self, model_id: str, date: Optional[datetime] = None) -> Pricing:
        """Get pricing for model at specific date (defaults to today)."""
        ...

    def calculate_cost(self, model_id: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for token usage."""
        ...

    def get_pricing_history(self, model_id: str) -> List[PricingVersion]:
        """Get historical pricing for cost analysis."""
        ...
```

**Pricing Data Format**:
```yaml
# pricing/data/anthropic.yaml
models:
  claude-sonnet-4-5:
    versions:
      - effective_date: 2025-10-24
        input_per_1m: 3.00
        output_per_1m: 15.00
        notes: "Current pricing"
      - effective_date: 2025-01-24
        input_per_1m: 3.00
        output_per_1m: 15.00
        notes: "Initial 4.5 pricing"
```

---

### ADR-004: Implement Model Capability Matrix

**Status**: ✅ Approved
**Date**: 2025-10-24

**Context**:
Current state:
- Model capabilities are implicit (must read docs)
- No programmatic way to check "does this model support function calling?"
- Model selection is manual and error-prone
- Can't implement smart routing based on capabilities

**Example of implicit capabilities**:
```python
# Current: Must know from documentation
if model == "gpt-4o":
    # Can use vision
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {"type": "image_url", "image_url": {"url": url}}
            ]
        }]
    )
```

**Decision**:
Add explicit capability declarations to model definitions with runtime validation.

**Rationale**:
- Self-documenting: Capabilities visible in code
- Runtime checking: Catch errors before API calls
- Smart selection: Choose models based on required capabilities
- Clear feature support: No guessing what works

**Consequences**:
- ✅ Runtime capability checking prevents errors
- ✅ Better model selection algorithms
- ✅ Clear feature support matrix
- ✅ Can warn when using unsupported features
- ⚠️ Requires comprehensive capability taxonomy
- ⚠️ Need to keep capabilities up-to-date

**Capability Taxonomy**:
```python
class ModelCapability(Enum):
    """Standard model capabilities."""
    # Input modalities
    TEXT_INPUT = "text_input"
    IMAGE_INPUT = "image_input"
    AUDIO_INPUT = "audio_input"
    VIDEO_INPUT = "video_input"

    # Output modalities
    TEXT_OUTPUT = "text_output"
    IMAGE_OUTPUT = "image_output"

    # Advanced features
    FUNCTION_CALLING = "function_calling"
    JSON_MODE = "json_mode"
    STREAMING = "streaming"

    # Context features
    LARGE_CONTEXT = "large_context"  # >100K tokens
    PROMPT_CACHING = "prompt_caching"

    # Reasoning
    EXTENDED_THINKING = "extended_thinking"
    CHAIN_OF_THOUGHT = "chain_of_thought"
```

**Implementation**:
```python
# Model with capabilities
CLAUDE_SONNET = ModelSpec(
    ...
    capabilities={
        ModelCapability.TEXT_INPUT,
        ModelCapability.TEXT_OUTPUT,
        ModelCapability.FUNCTION_CALLING,
        ModelCapability.LARGE_CONTEXT,
        ModelCapability.PROMPT_CACHING,
        ModelCapability.EXTENDED_THINKING,
    },
    ...
)

# Runtime checking
def validate_request(model: ModelSpec, requires: Set[ModelCapability]):
    """Validate model supports required capabilities."""
    missing = requires - model.capabilities
    if missing:
        raise UnsupportedCapabilityError(
            f"Model {model.name} missing: {missing}"
        )
```

---

## Implementation Roadmap

### Phase 1: Foundation (Prerequisites)

**Goal**: Establish baseline and safety net before refactor

#### Task 1.1: Audit Current State [Simple]
**Estimated time**: 2 hours
**Owner**: TBD

**Deliverables**:
- Complete inventory of all models in use
- List of all provider implementations
- Documentation of all public APIs
- Dependency map (what uses what)

**Acceptance Criteria**:
- [ ] All models documented
- [ ] All providers documented
- [ ] Public API surface mapped
- [ ] Dependencies visualized

---

#### Task 1.2: Create Test Suite [Medium]
**Estimated time**: 1 day
**Owner**: TBD

**Deliverables**:
- Comprehensive regression test suite
- Performance benchmarks
- Integration tests for existing functionality

**Acceptance Criteria**:
- [ ] >80% coverage of existing code
- [ ] All public APIs tested
- [ ] Performance baseline established
- [ ] All tests passing

**Key Tests**:
```python
def test_model_registry_get_all():
    """Baseline: Registry returns all current models."""
    models = ModelRegistry.get_all_current_models()
    assert len(models) == 8  # Current count
    assert "claude-sonnet-4.5" in models

def test_provider_factory_creates_claude():
    """Baseline: Factory creates Claude provider."""
    provider = get_provider("claude-sonnet")
    assert isinstance(provider, ClaudeProvider)

def test_classification_end_to_end():
    """Baseline: Full classification workflow works."""
    provider = get_provider("claude-sonnet")
    result = provider.classify("Need SSO integration")
    assert result.category == SignalCategory.FEATURE_REQUEST
```

---

#### Task 1.3: Setup Migration Scripts [Simple]
**Estimated time**: 4 hours
**Owner**: TBD

**Deliverables**:
- Script to backup current state
- Script to validate data integrity
- Rollback procedures

**Acceptance Criteria**:
- [ ] Backup script tested
- [ ] Validation script working
- [ ] Rollback procedure documented
- [ ] All scripts executable

---

### Phase 2: Core Refactor

**Goal**: Implement foundational new components

#### Task 2.1: Design Unified Model Schema [Medium]
**Estimated time**: 1 day
**Owner**: TBD

**Deliverables**:
- JSON/YAML schema specification
- Python dataclass implementation
- Schema validation logic
- Migration mapping (old → new)

**Schema Structure**:
```yaml
# Model definition schema
model_id: string
provider: string  # anthropic, openai, google

metadata:
  name: string
  version: string
  context_window_input: integer
  context_window_output: integer | null
  knowledge_cutoff: string
  last_verified: date

capabilities:
  - capability_enum_values

optimization:
  recommended_for:
    - use_case_strings
  best_practices:
    - practice_strings
  tips:
    - tip_strings
  pitfalls:
    - pitfall_strings

pricing_ref: string  # References pricing service

documentation:
  url: string
  notes: string
```

**Acceptance Criteria**:
- [ ] Schema covers all current model fields
- [ ] Schema includes optimization guidance from MODEL_OPTIMIZATION_GUIDE.md
- [ ] Validation logic implemented
- [ ] Can convert all existing models

---

#### Task 2.2: Build Pricing Service [Complex]
**Estimated time**: 2 days
**Owner**: TBD

**Deliverables**:
- PricingService class implementation
- Pricing data files (YAML)
- Version tracking logic
- Cost calculation utilities

**Implementation**:
```python
# pricing/service.py
class PricingService:
    def __init__(self, data_path: Path = DEFAULT_PRICING_PATH):
        self._pricing_data = self._load_pricing(data_path)
        self._cache = {}  # LRU cache for performance

    def get_pricing(
        self,
        model_id: str,
        effective_date: Optional[datetime] = None
    ) -> Pricing:
        """Get pricing for model at specific date."""
        ...

    def calculate_cost(
        self,
        model_id: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Calculate total cost for token usage."""
        pricing = self.get_pricing(model_id)
        input_cost = (input_tokens / 1_000_000) * pricing.input_per_1m
        output_cost = (output_tokens / 1_000_000) * pricing.output_per_1m
        return input_cost + output_cost

    def get_pricing_history(
        self,
        model_id: str
    ) -> List[PricingVersion]:
        """Get all pricing versions for analysis."""
        ...
```

**Pricing Data Format**:
```yaml
# pricing/data/anthropic.yaml
provider: anthropic

models:
  claude-sonnet-4-5-20250929:
    display_name: "Claude Sonnet 4.5"
    pricing_versions:
      - effective_date: 2025-10-24
        input_per_1m_tokens: 3.00
        output_per_1m_tokens: 15.00
        currency: USD
        notes: "Current pricing"

  claude-haiku-4-5-20251001:
    display_name: "Claude Haiku 4.5"
    pricing_versions:
      - effective_date: 2025-10-24
        input_per_1m_tokens: 1.00
        output_per_1m_tokens: 5.00
        currency: USD
        notes: "4x increase from Haiku 3.x"
```

**Acceptance Criteria**:
- [ ] Can load pricing from YAML files
- [ ] Supports historical pricing queries
- [ ] Cost calculation accurate to 0.01 cents
- [ ] Caching implemented for performance
- [ ] All current models have pricing data

---

#### Task 2.3: Complete Provider Registry [Medium]
**Estimated time**: 1 day
**Owner**: TBD

**Deliverables**:
- ProviderRegistry implementation
- Provider self-registration mechanism
- Discovery and listing functionality

**Implementation**:
```python
# providers/registry.py
class ProviderRegistry:
    """Central registry for provider implementations."""

    _providers: Dict[str, Type[LLMProvider]] = {}

    @classmethod
    def register(cls, name: str, aliases: List[str] = None):
        """Decorator to register a provider."""
        def decorator(provider_class: Type[LLMProvider]):
            cls._providers[name] = provider_class
            for alias in (aliases or []):
                cls._providers[alias] = provider_class
            return provider_class
        return decorator

    @classmethod
    def get(cls, name: str) -> Type[LLMProvider]:
        """Get provider class by name."""
        if name not in cls._providers:
            raise ProviderNotFoundError(f"Provider '{name}' not registered")
        return cls._providers[name]

    @classmethod
    def list_providers(cls) -> List[str]:
        """List all registered providers."""
        return list(cls._providers.keys())

# Usage in provider files
@ProviderRegistry.register("claude", aliases=["anthropic"])
class ClaudeProvider(LLMProvider):
    ...

@ProviderRegistry.register("gpt", aliases=["openai"])
class OpenAIProvider(LLMProvider):
    ...
```

**Acceptance Criteria**:
- [ ] All existing providers registered
- [ ] Can discover providers at runtime
- [ ] Aliases work correctly
- [ ] Error handling for unknown providers

---

#### Task 2.4: Implement Capability Matrix [Medium]
**Estimated time**: 1 day
**Owner**: TBD

**Deliverables**:
- ModelCapability enum
- Capability validation logic
- Capability-based selection helper

**Implementation**:
```python
# models/capabilities.py
class ModelCapability(str, Enum):
    """Comprehensive model capability taxonomy."""

    # Input modalities
    TEXT_INPUT = "text_input"
    IMAGE_INPUT = "image_input"
    AUDIO_INPUT = "audio_input"
    VIDEO_INPUT = "video_input"
    DOCUMENT_INPUT = "document_input"  # PDF, DOCX, etc.

    # Output modalities
    TEXT_OUTPUT = "text_output"
    IMAGE_OUTPUT = "image_output"
    STRUCTURED_OUTPUT = "structured_output"  # JSON schema

    # Advanced features
    FUNCTION_CALLING = "function_calling"
    JSON_MODE = "json_mode"
    STREAMING = "streaming"
    BATCH_API = "batch_api"

    # Context features
    LARGE_CONTEXT = "large_context"  # >100K tokens
    EXTRA_LARGE_CONTEXT = "extra_large_context"  # >1M tokens
    PROMPT_CACHING = "prompt_caching"

    # Reasoning & specialized tasks
    EXTENDED_THINKING = "extended_thinking"
    CODE_GENERATION = "code_generation"
    MATH_REASONING = "math_reasoning"

    # Safety & control
    CONTENT_FILTERING = "content_filtering"
    SYSTEM_MESSAGES = "system_messages"

# Validation utilities
def validate_capabilities(
    model: ModelSpec,
    required: Set[ModelCapability],
    warn_only: bool = False
) -> bool:
    """Validate model has required capabilities."""
    missing = required - model.capabilities

    if missing:
        msg = f"Model {model.name} missing capabilities: {missing}"
        if warn_only:
            warnings.warn(msg)
            return False
        else:
            raise UnsupportedCapabilityError(msg)

    return True

def find_models_with_capabilities(
    required: Set[ModelCapability],
    preferred: Set[ModelCapability] = None
) -> List[ModelSpec]:
    """Find models supporting required (and optionally preferred) capabilities."""
    ...
```

**Acceptance Criteria**:
- [ ] All current models have capabilities declared
- [ ] Validation works correctly
- [ ] Selection helper finds appropriate models
- [ ] Documentation for all capabilities

---

### Phase 3: Migration

**Goal**: Move existing data to new structure

#### Task 3.1: Migrate Model Definitions [Simple]
**Estimated time**: 1 day
**Owner**: TBD

**Process**:
1. Convert current `models/registry.py` entries to new schema
2. Incorporate content from `MODEL_OPTIMIZATION_GUIDE.md`
3. Add capability declarations
4. Link to pricing service

**Example Migration**:
```python
# OLD (models/registry.py)
CLAUDE_SONNET_4_5 = ModelSpec(
    provider=Provider.ANTHROPIC,
    name="Claude Sonnet 4.5",
    api_identifier="claude-sonnet-4-5-20250929",
    context_window_input=200_000,
    input_price_per_1m=3.00,
    output_price_per_1m=15.00,
    ...
)

# NEW (models/definitions/anthropic/claude_sonnet_4_5.yaml)
model_id: claude-sonnet-4-5-20250929
provider: anthropic

metadata:
  name: Claude Sonnet 4.5
  version: 4.5
  api_identifier: claude-sonnet-4-5-20250929
  context_window_input: 200000
  context_window_output: null
  knowledge_cutoff: "January 2025"
  last_verified: 2025-10-24

capabilities:
  - text_input
  - text_output
  - function_calling
  - large_context
  - prompt_caching
  - extended_thinking
  - streaming

optimization:
  recommended_for:
    - "Production workhorse"
    - "Analysis and reasoning"
    - "Long-form writing"
    - "Code generation"

  best_practices:
    - "Use XML structure for complex prompts"
    - "Enable prompt caching for repeated patterns"
    - "Cache system prompts, vary user input"

  tips:
    - "RECOMMENDED for most use cases"
    - "1M token context available in beta"
    - "Native XML understanding"

  pitfalls:
    - "Don't exceed 200K context in production"
    - "Caching only works with messages API"

pricing_ref: claude-sonnet-4-5-20250929

documentation:
  url: https://docs.claude.com/en/docs/about-claude/models
  notes: "Training data: July 2025"
```

**Acceptance Criteria**:
- [ ] All 8 current models migrated
- [ ] Optimization content from guide included
- [ ] All capabilities declared
- [ ] Pricing references correct

---

#### Task 3.2: Update Provider Implementations [Medium]
**Estimated time**: 1 day
**Owner**: TBD

**Changes needed**:
1. Remove hardcoded pricing (use PricingService)
2. Use ProviderRegistry decorator
3. Validate capabilities before API calls
4. Remove model ID maps (use ModelRegistry)

**Example**:
```python
# OLD
CLAUDE_PRICING = {  # ❌ Hardcoded
    "claude-haiku": (0.25, 1.25),
    "claude-sonnet": (3.0, 15.0),
}

class ClaudeProvider(LLMProvider):
    def __init__(self, model="claude-sonnet"):
        self.model = model
        self.pricing = CLAUDE_PRICING[model]

# NEW
@ProviderRegistry.register("claude", aliases=["anthropic"])
class ClaudeProvider(LLMProvider):
    def __init__(self, model_id: str, pricing_service: PricingService):
        self.model_spec = ModelRegistry.get_spec(model_id)
        self.pricing_service = pricing_service

        # Validate model supports required capabilities
        validate_capabilities(
            self.model_spec,
            required={ModelCapability.TEXT_INPUT, ModelCapability.TEXT_OUTPUT}
        )

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        return self.pricing_service.calculate_cost(
            self.model_spec.api_identifier,
            input_tokens,
            output_tokens
        )
```

**Acceptance Criteria**:
- [ ] All providers use PricingService
- [ ] All providers registered with ProviderRegistry
- [ ] All providers validate capabilities
- [ ] No hardcoded configuration remains

---

#### Task 3.3: Port Configuration Content [Simple]
**Estimated time**: 4 hours
**Owner**: TBD

**Process**:
1. Extract optimization content from `MODEL_OPTIMIZATION_GUIDE.md`
2. Map to model definitions
3. Verify completeness

**Content to port**:
- Recommended use cases
- Best practices
- Optimization tips
- Common pitfalls
- Model selection criteria

**Acceptance Criteria**:
- [ ] All content from guide mapped to models
- [ ] No information lost
- [ ] Content is structured and queryable

---

### Phase 4: Validation

**Goal**: Ensure refactor succeeded without breaking anything

#### Task 4.1: Integration Testing [Medium]
**Estimated time**: 1 day
**Owner**: TBD

**Test Scenarios**:
```python
def test_full_workflow_unchanged():
    """Verify end-to-end workflow still works."""
    # Get provider
    provider = get_provider("claude-sonnet")

    # Classify
    result = provider.classify("Need SSO")

    # Verify
    assert result.category == SignalCategory.FEATURE_REQUEST
    assert result.cost > 0  # Pricing service working

def test_model_selection_by_capability():
    """New capability: Select model by feature requirement."""
    models = find_models_with_capabilities(
        required={ModelCapability.IMAGE_INPUT}
    )

    assert GPT_4O in models
    assert CLAUDE_SONNET not in models  # No vision

def test_pricing_service_accurate():
    """Pricing matches expected values."""
    pricing = PricingService()

    cost = pricing.calculate_cost(
        "claude-sonnet-4-5-20250929",
        input_tokens=1_000_000,
        output_tokens=1_000_000
    )

    assert cost == 18.00  # $3 + $15

def test_backward_compatibility():
    """Old API still works."""
    from models.registry import CLAUDE_SONNET

    assert CLAUDE_SONNET.api_identifier == "claude-sonnet-4-5-20250929"
    assert CLAUDE_SONNET.input_price_per_1m == 3.00
```

**Acceptance Criteria**:
- [ ] All integration tests pass
- [ ] Backward compatibility verified
- [ ] New features work correctly

---

#### Task 4.2: Performance Testing [Simple]
**Estimated time**: 4 hours
**Owner**: TBD

**Benchmarks**:
```python
def benchmark_model_lookup():
    """Model registry lookup performance."""
    # Should be <1ms

def benchmark_pricing_calculation():
    """Pricing service calculation performance."""
    # Should be <1ms with caching

def benchmark_provider_creation():
    """Provider instantiation performance."""
    # Should be <10ms
```

**Acceptance Criteria**:
- [ ] No performance regression >5%
- [ ] All benchmarks within targets
- [ ] Memory usage acceptable

---

#### Task 4.3: Documentation Update [Simple]
**Estimated time**: 4 hours
**Owner**: TBD

**Documents to update**:
- README.md
- MODEL_OPTIMIZATION_GUIDE.md (point to new structure)
- UPDATING_MODELS.md (new procedures)
- API documentation
- Migration guide

**Acceptance Criteria**:
- [ ] All docs reflect new structure
- [ ] Migration guide complete
- [ ] Examples updated
- [ ] No broken links

---

## Success Metrics

### Quantitative Metrics

| Metric | Target | Measurement Method | Current Baseline |
|--------|--------|-------------------|------------------|
| API Compatibility | 100% | All existing tests pass | N/A |
| Performance | <5% latency increase | Benchmark suite | TBD |
| Test Coverage | >90% | pytest-cov | 100% (58/58 tests) |
| Migration Success | 100% | All 8 models migrated | 0% |
| Memory Usage | <10% increase | Memory profiler | TBD |
| Time to Add Model | <30 min | Manual timing | ~2 hours |
| Lines of Code | 20% reduction | cloc | TBD |

---

### Qualitative Metrics

| Metric | Current State | Target State | Validation |
|--------|---------------|--------------|------------|
| Developer Experience | Must check 3 places for model info | Check 1 place | User survey |
| Maintainability | Duplicated logic in providers | DRY principle followed | Code review |
| Documentation | Scattered across files | Comprehensive and co-located | Doc review |
| Extensibility | Edit core files for new provider | Plugin-based registration | Add test provider |

---

## Risk Register

### Risk 1: Breaking Changes to Production Systems

**Probability**: Medium
**Impact**: High
**Risk Score**: 🔴 High

**Description**:
Refactoring core model/provider logic could break existing integrations.

**Mitigation Strategies**:
1. **Parallel implementations**: Keep old code working during migration
2. **Feature flags**: Gradual rollout with `USE_NEW_REGISTRY=true/false`
3. **Comprehensive regression tests**: 100% coverage of public APIs
4. **Staged deployment**:
   - Week 1: Development environment
   - Week 2: Staging environment
   - Week 3: Production (10% canary)
   - Week 4: Production (100%)

**Contingency Plan**:
- Immediate rollback capability via feature flag
- Keep old code in `legacy/` directory for 2 releases
- Automated monitoring alerts for errors
- Rollback procedure documented and tested

**Early Warning Signs**:
- Test failures in regression suite
- Performance degradation in benchmarks
- Errors in staging environment

---

### Risk 2: Performance Degradation

**Probability**: Low
**Impact**: Medium
**Risk Score**: 🟡 Medium

**Description**:
Additional abstraction layers (registry, pricing service) could slow down operations.

**Mitigation Strategies**:
1. **Benchmark before and after**: Establish baseline, measure changes
2. **Profile critical paths**: Use cProfile/memory_profiler
3. **Implement caching**: LRU cache for frequently accessed data
4. **Optimize hot paths**: Prioritize performance in common operations

**Performance Targets**:
- Model lookup: <1ms
- Pricing calculation: <1ms
- Provider creation: <10ms
- Full classification: <5% increase

**Contingency Plan**:
- If >5% regression: Optimize before shipping
- If >10% regression: Reconsider architecture
- Cache everything that's cacheable
- Lazy loading for rarely-used features

---

### Risk 3: Incomplete Migration Due to Unknown Dependencies

**Probability**: Medium
**Impact**: Medium
**Risk Score**: 🟡 Medium

**Description**:
Hidden dependencies on current structure could be missed during analysis.

**Mitigation Strategies**:
1. **Thorough dependency analysis**: Use import analysis tools
2. **Maintain backward compatibility layer**: Adapter pattern for old APIs
3. **Document all discovered dependencies**: Keep running list
4. **Incremental migration**: Don't remove old code immediately

**Detection Methods**:
- Static analysis: `pipreqs`, `pydeps`
- Runtime analysis: Instrument code to log usage
- Grep for imports: `grep -r "from models import"`
- Developer interviews: Ask team about integrations

**Contingency Plan**:
- Keep old imports working via re-exports
- Deprecation warnings with migration instructions
- Extended support period (2-3 releases)
- Documented migration path for each pattern

---

### Risk 4: Pricing Service Becomes Bottleneck

**Probability**: Low
**Impact**: High
**Risk Score**: 🟡 Medium

**Description**:
If pricing service is slow or unavailable, entire system could be affected.

**Mitigation Strategies**:
1. **Implement caching layer**: In-memory LRU cache for pricing data
2. **Support bulk queries**: Batch pricing lookups
3. **Async pricing updates**: Don't block on pricing file loads
4. **Fallback pricing**: Use cached/default values if service unavailable

**Implementation**:
```python
class PricingService:
    def __init__(self):
        self._cache = LRUCache(maxsize=1000)
        self._fallback_pricing = self._load_fallback()

    @lru_cache(maxsize=1000)
    def get_pricing(self, model_id: str) -> Pricing:
        try:
            return self._fetch_pricing(model_id)
        except Exception:
            logger.warning(f"Pricing service error, using fallback")
            return self._fallback_pricing.get(model_id)
```

**Performance Targets**:
- Cache hit rate: >95%
- Cache miss latency: <10ms
- Fallback always available

---

### Risk 5: Over-Engineering the Solution

**Probability**: Medium
**Impact**: Low
**Risk Score**: 🟢 Low

**Description**:
Adding unnecessary complexity that doesn't provide value.

**Mitigation Strategies**:
1. **Start with MVP**: Implement minimum viable refactor
2. **Iterate based on usage**: Add features when needed
3. **Regular architecture reviews**: Checkpoint complexity
4. **YAGNI principle**: "You Aren't Gonna Need It"

**Red Flags**:
- Feature not used in first month → Remove
- Abstraction used in <3 places → Inline
- Code harder to understand → Simplify

**Decision Framework**:
```
Should we add feature X?
- Is it solving a real problem? (Yes/No)
- Will it be used immediately? (Yes/No)
- Is there a simpler alternative? (Yes/No)

If 2+ "No" answers → Don't add it
```

---

## Migration Guide

### For Developers

**Phase 1: Enable new system**
```python
# In your code, set feature flag
USE_NEW_MODEL_REGISTRY = True
```

**Phase 2: Update imports**
```python
# OLD
from models.registry import CLAUDE_SONNET
from providers.factory import get_provider

# NEW (backward compatible)
from ai_models.registry import CLAUDE_SONNET  # Still works!
from ai_models.providers import get_provider   # Still works!
```

**Phase 3: Use new features**
```python
# New: Capability-based selection
from ai_models.capabilities import ModelCapability
from ai_models.registry import find_models_with_capabilities

models = find_models_with_capabilities(
    required={ModelCapability.IMAGE_INPUT, ModelCapability.FUNCTION_CALLING}
)

# New: Historical pricing
from ai_models.pricing import PricingService

pricing = PricingService()
history = pricing.get_pricing_history("claude-sonnet-4-5-20250929")
```

---

### For Model Maintainers

**Adding a new model**:

```yaml
# 1. Create model definition file
# ai_models/models/definitions/anthropic/claude_opus_5_0.yaml

model_id: claude-opus-5-0-20260101
provider: anthropic

metadata:
  name: Claude Opus 5.0
  version: 5.0
  api_identifier: claude-opus-5-0-20260101
  context_window_input: 200000
  knowledge_cutoff: "June 2025"
  last_verified: 2026-01-01

capabilities:
  - text_input
  - text_output
  - image_input
  - function_calling

optimization:
  recommended_for:
    - "Highest quality reasoning"
  best_practices:
    - "Use for critical decisions"

pricing_ref: claude-opus-5-0-20260101

documentation:
  url: https://docs.claude.com/models
```

```yaml
# 2. Add pricing
# ai_models/pricing/data/anthropic.yaml

models:
  claude-opus-5-0-20260101:
    display_name: "Claude Opus 5.0"
    pricing_versions:
      - effective_date: 2026-01-01
        input_per_1m_tokens: 20.00
        output_per_1m_tokens: 100.00
```

**That's it!** Model automatically available via registry.

---

## Appendix

### File Structure Reference

```
ai_models/
├── __init__.py
├── registry/
│   ├── __init__.py
│   ├── model_registry.py       # Central model registry
│   └── provider_registry.py    # Provider registration
├── models/
│   ├── __init__.py
│   ├── base.py                 # ModelSpec dataclass
│   ├── capabilities.py         # Capability enums
│   └── definitions/            # Model definition files (YAML)
│       ├── anthropic/
│       │   ├── claude_sonnet_4_5.yaml
│       │   ├── claude_haiku_4_5.yaml
│       │   └── claude_opus_4_1.yaml
│       ├── openai/
│       │   ├── gpt_4o.yaml
│       │   └── gpt_4o_mini.yaml
│       └── google/
│           ├── gemini_2_5_pro.yaml
│           ├── gemini_2_5_flash.yaml
│           └── gemini_2_5_flash_lite.yaml
├── providers/
│   ├── __init__.py
│   ├── base.py                 # LLMProvider base class
│   ├── claude_provider.py
│   ├── openai_provider.py
│   └── google_provider.py
├── pricing/
│   ├── __init__.py
│   ├── service.py              # PricingService class
│   ├── models.py               # Pricing dataclasses
│   └── data/                   # Pricing data (YAML)
│       ├── anthropic.yaml
│       ├── openai.yaml
│       └── google.yaml
└── utils/
    ├── __init__.py
    ├── validation.py           # Schema validation
    └── caching.py              # LRU cache utilities
```

---

### Timeline Estimate

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| **Phase 1: Foundation** | 2-3 days | None |
| **Phase 2: Core Refactor** | 5-6 days | Phase 1 complete |
| **Phase 3: Migration** | 2-3 days | Phase 2 complete |
| **Phase 4: Validation** | 2 days | Phase 3 complete |
| **Buffer** | 2 days | Contingency |
| **Total** | **13-16 days** | ~3 weeks |

**Critical Path**: Phase 1 → 2 → 3 → 4

**Parallel Work Opportunities**:
- Documentation can start during Phase 3
- Pricing data can be prepared during Phase 2
- Model definitions can be drafted during Phase 2

---

### Next Steps

1. **Review and approve this design** (1-2 days)
2. **Assign owners to each phase** (1 day)
3. **Set up project tracking** (1 day)
4. **Begin Phase 1: Foundation** (2-3 days)

**Decision needed**: Approve to proceed? Any concerns or changes?

---

**Document Version**: 1.0
**Last Updated**: 2025-10-24
**Status**: ✅ Ready for Review
**Next Review**: After Phase 1 completion
