# Architect-Builder Pattern - OpenAI Optimized

> Extends `prompt.md` with OpenAI-specific optimizations

## Overview

This OpenAI-optimized variant leverages GPT-5's advanced reasoning and auto-routing capabilities, integrating with GitHub Copilot/Codex for code implementation. The two-phase workflow balances strategic design with efficient execution.

**Recommended models:**
- **Phase 1 (Design & Validation)**: GPT-5 for strategic architecture decisions with auto-routing (Instant/Thinking modes) and codebase analysis
- **Phase 2 (Execution)**: GPT-5 mini + GitHub Copilot/Codex for autonomous code generation

---

## System Prompt

```
You are implementing the Architect-Builder Pattern, a two-phase workflow for complex software development. Follow these phases sequentially.

# PHASE 1: ARCHITECTURE, DESIGN & VALIDATION

Use GPT-5 for strategic thinking with auto-routing between Instant and Thinking modes for design and validation.

**Design Request Template:**

I need to design [SYSTEM/FEATURE]. Please provide:

## 1. Architecture Blueprint
- Component diagram with clear boundaries
- Data flow and state management approach
- Interface contracts between components
- Error handling strategy
- Security considerations

## 2. Implementation Checklist
**Critical Path (Must-Have):**
- [Core functionality items]
- [Essential integrations]

**Enhancement Items (Nice-to-Have):**
- [Performance optimizations]
- [Additional features]

**Technical Debt to Avoid:**
- [Known anti-patterns]
- [Common pitfalls]

## 3. Validation Criteria
- How to verify the design works
- Edge cases to test
- Performance benchmarks
- Security requirements

## 4. Implementation Instructions
- Specific file structure to create
- Testing approach (unit/integration/e2e)
- Dependencies to install
- Configuration needed

**Context:** [Include relevant constraints, existing patterns, tech stack, team size]

**Design Principles to Apply:**
- Specificity over generality (be concrete and explicit)
- Examples over explanations (show, don't just tell)
- Structure over prose (use diagrams, lists, clear sections)
- Constraints over freedom (define boundaries clearly)
- Include rollback strategy for high-risk changes

## Then validate the design against your existing codebase:

**Validation Request:**

Please analyze my codebase and validate this design:

[Your design above]

**Check the following:**

### 1. Pattern Consistency
- Does this align with existing patterns in the codebase?
- What modifications are needed for consistency?
- Can we reuse existing components?

### 2. Dependency Analysis
- What existing code will be affected?
- Are there hidden dependencies?
- What's the blast radius of this change?

### 3. Risk Assessment
- What could break?
- What needs extra testing?
- What are the rollback considerations?

### 4. Optimization Opportunities
- Can we simplify the design?
- Are there performance considerations?
- What existing patterns can we leverage?

**Output:** Refined implementation plan with:
- Specific file paths
- Code patterns to follow
- Risk mitigation steps
- Testing strategy

---

# PHASE 2: AUTONOMOUS EXECUTION

Execute the validated design with GitHub Copilot/Codex for systematic implementation.

**Execution Request Template:**

Implement this validated design using GitHub Copilot:

[Paste refined design from Phase 1]

**Execution Parameters:**
- **Mode:** [careful/standard/fast]
- **Testing:** [unit/integration/e2e/all]
- **Documentation:** [inline/separate/both]

**Implementation Order:**
1. **Core Infrastructure First**
   - Database schemas, base classes, interfaces
   - Checkpoint: Verify compilation and type safety

2. **Business Logic Second**
   - Core algorithms, data transformations
   - Checkpoint: Run unit tests

3. **UI/API Layer Third**
   - Endpoints, controllers, views
   - Checkpoint: Run integration tests

4. **Tests Throughout**
   - Write tests alongside implementation
   - Checkpoint: Full test suite passes

**Quality Gates:**
- After each phase: Run relevant tests
- Before completion: Full test suite + linting
- Final: Code review checklist verification

**Proceed autonomously but pause at checkpoints for validation.**
```

---

## OpenAI Optimizations Applied

### 1. Clear Role Definition
- Explicit system message establishes expert architectural role
- Clear phase delineation with numbered sections
- Structured templates for consistent outputs

### 2. Instruction Following
- Direct, imperative language optimized for GPT-5
- Numbered lists for sequential steps
- Concrete action items vs abstract concepts

### 3. Structured Output
- Consistent markdown formatting
- Template-driven responses
- Predictable section structure for parsing

### 4. GitHub Copilot & Codex Integration

OpenAI's model capabilities naturally align with the two-phase approach:

**Phase 1 (Design & Validation):**
- GPT-5 auto-routes between Thinking mode for complex architectural decisions
- Instant mode for quick pattern matching and code analysis
- Strategic design with comprehensive reasoning capabilities

**Phase 2 (Execution):**
- GPT-5 mini with Codex provides rapid, cost-effective implementation
- GitHub Copilot integration enables inline suggestions and completions
- Function/class generation, test creation, and documentation

This mirrors professional development workflows similar to Claude Code's planning and execution modes, where senior architects design (GPT-5 Thinking) and experienced developers execute (Codex/GPT-5 mini).

---

## Usage with GitHub Copilot/Codex

### Phase 1: Design & Validation (GPT-5 API or ChatGPT)

Use GPT-5 for strategic design and validation with auto-routing:

```python
from openai import OpenAI

client = OpenAI(api_key="...")

response = client.chat.completions.create(
    model="gpt-5",  # Auto-routes to Instant or Thinking mode
    messages=[
        {
            "role": "system",
            "content": open("prompt.openai.md").read()
        },
        {
            "role": "user",
            "content": """
            I need to design a RESTful API refactoring that:
            - Maintains backward compatibility with v1 API
            - Adds versioning support (header-based)
            - Implements rate limiting (100 req/min per user)
            - Uses consistent error response format

            Context: Node.js/Express backend, PostgreSQL, 50K daily active users
            """
        }
    ],
    temperature=0.7,
    max_tokens=4000
)

design = response.choices[0].message.content
print(design)
```

### Phase 1 (continued): Validation with Codebase Context

```python
# Load relevant codebase files
codebase_context = ""
for file in ["src/api/routes.js", "src/middleware/auth.js", "src/models/user.js"]:
    with open(file) as f:
        codebase_context += f"\n\n// {file}\n{f.read()}"

response = client.chat.completions.create(
    model="gpt-5-mini",  # Cost-effective for analysis
    messages=[
        {
            "role": "system",
            "content": "You are validating an architecture design against an existing codebase."
        },
        {
            "role": "user",
            "content": f"""
            Please validate this design:

            {design}

            Against this codebase:

            {codebase_context}

            Check for: pattern consistency, dependencies, risks, and optimization opportunities.
            """
        }
    ],
    temperature=0.3,
    max_tokens=4000
)

validated_design = response.choices[0].message.content
```

### Phase 2: Execution (GitHub Copilot in VS Code/Cursor)

**Manual workflow with Copilot:**

1. **Open your IDE** with GitHub Copilot enabled
2. **Create implementation plan** in comments:
   ```javascript
   // Phase 1: Core Infrastructure
   // TODO: Create versioning middleware
   // TODO: Update route registration to support versioned endpoints
   // TODO: Add rate limiting middleware

   // Phase 2: Business Logic
   // TODO: Migrate existing endpoints to v2
   // TODO: Maintain v1 compatibility layer

   // Phase 3: Testing
   // TODO: Add integration tests for v1 backward compatibility
   // TODO: Add unit tests for rate limiting
   ```

3. **Let Copilot suggest implementations** for each TODO
4. **Run tests at each checkpoint** as defined in the design

**Programmatic workflow with Codex:**

```python
# Generate code for each component
def generate_component(component_spec: str) -> str:
    """Use GPT-5 mini to generate implementation from spec."""
    response = client.chat.completions.create(
        model="gpt-5-mini",  # Fast and cost-effective for code generation
        messages=[
            {
                "role": "system",
                "content": "You are a code generation assistant. Generate production-ready code with tests."
            },
            {
                "role": "user",
                "content": f"Implement this component:\n\n{component_spec}"
            }
        ],
        temperature=0.2
    )
    return response.choices[0].message.content

# Example: Generate rate limiting middleware
rate_limit_spec = """
Create Express middleware for rate limiting:
- 100 requests per minute per user
- Use Redis for distributed rate limiting
- Return 429 status with Retry-After header
- Include comprehensive error handling
"""

code = generate_component(rate_limit_spec)
print(code)
```

---

## Cost Optimization

### Model Selection Strategy

| Phase | Recommended Model | Cost (per 1M tokens) | Why |
|-------|------------------|---------------------|-----|
| Phase 1: Design & Validation | GPT-5 | $3.00 input, $12.00 output | Auto-routing, advanced reasoning, 256k context |
| Phase 2: Execution | GPT-5 mini + Codex | $0.20 input, $0.80 output | High-volume code generation, IDE integration |

### Token Management

**Typical costs per feature:**
- Phase 1 (Design & Validation): $0.19-0.55 (GPT-5 with auto-routing)
- Phase 2 (Execution): $0.02-0.08 (GPT-5 mini + Codex)
- **Total: $0.21-0.63** (vs $1.50-3.00 for pure GPT-5 usage)

**Best practices:**
- Use GPT-5 mini for code generation (93% cost reduction vs GPT-5)
- GPT-5 auto-routes to Instant mode for simple tasks, Thinking mode for complex reasoning
- Use function calling for structured outputs (reduces token usage)
- Batch related operations in single requests
- Leverage GPT-5's 256k context window for large architectural designs

---

## Production Workflow Example

### Complete Feature Implementation

```python
from openai import OpenAI
import os

client = OpenAI()

# Load prompt
with open("prompt.openai.md") as f:
    system_prompt = f.read()

# Phase 1: Design
print("🎨 Phase 1: Designing architecture...")
design_response = client.chat.completions.create(
    model="gpt-5",  # Auto-routing for optimal performance
    messages=[
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": """
            Design a user authentication service extraction from monolith:
            - Define service boundaries
            - Design API contract (REST endpoints)
            - Plan data migration strategy
            - Include failure handling (circuit breakers, retries)

            Context: Node.js/Express monolith, MongoDB, 5M users, deployed on AWS
            """
        }
    ],
    temperature=0.7,
    max_tokens=4000
)

design = design_response.choices[0].message.content
print(f"✅ Design complete ({design_response.usage.total_tokens} tokens)")

# Save design
with open("design_output.md", "w") as f:
    f.write(design)

# Phase 2: Validation
print("\n📋 Phase 2: Validating design...")
# (Load codebase context as shown above)

# Phase 3: Execution
print("\n🚀 Phase 3: Use GitHub Copilot in your IDE")
print("   Open VS Code/Cursor with Copilot enabled")
print("   Create implementation files following the validated design")
print("   Let Copilot suggest code for each component")
```

---

## Quality Checklist

After execution with GitHub Copilot, verify:

**Architecture Alignment:**
- [ ] Implementation matches design intent
- [ ] All components properly integrated
- [ ] Interfaces match specifications

**Code Quality:**
- [ ] Tests pass (unit, integration, e2e)
- [ ] Code coverage meets threshold (>80%)
- [ ] ESLint/TSLint passes
- [ ] No security vulnerabilities (npm audit)

**Documentation:**
- [ ] Design decisions documented
- [ ] API documentation complete (OpenAPI/Swagger)
- [ ] Deployment guide updated
- [ ] Known limitations documented

**Operational Readiness:**
- [ ] Error handling comprehensive
- [ ] Logging/monitoring in place
- [ ] Performance benchmarks met
- [ ] Rollback procedure tested

---

## Troubleshooting

### Issue: Design phase output not specific enough

**Solution:** Add constraints to user message:
```
Provide architecture design with:
- Specific file names and directory structure
- Code snippets for critical interfaces
- Exact API endpoint definitions
- Database schema DDL statements
```

### Issue: Copilot suggestions don't match design

**Solution:** Include design context in file comments:
```javascript
/**
 * Rate Limiting Middleware
 *
 * Design requirements:
 * - 100 requests per minute per user
 * - Redis-backed distributed rate limiting
 * - Return 429 with Retry-After header
 * - Support both API key and JWT authentication
 */
```

### Issue: High cost for validation phase

**Solution:** Use GPT-5 mini for cost-effective validation:
```python
response = client.chat.completions.create(
    model="gpt-5-mini",  # Fast and cost-effective
    messages=[...],
    temperature=0.3
)
```

---

## See Also

- **Base prompt**: `prompt.md` - Complete examples, production patterns, business value
- **Claude variant**: `prompt.claude.md` - For use with Claude Code
- **Gemini variant**: `prompt.gemini.md` - For use with Google AI Studio
- **Provider documentation**: `../../docs/provider-specific-prompts.md`

---

## Version History

**v2.1** (2025-11-14)
- Updated to two-phase workflow (merged validation into design phase)
- Added Codex/GPT-5 capability explanation mirroring Claude Code's approach
- Aligned with professional architect-developer workflow pattern
- Updated all phase references and cost calculations

**v2.0** (2025-11-05)
- Renamed from "Opus Code Execution Pattern" to "Architect-Builder Pattern"
- Made model-agnostic with OpenAI-specific optimizations
- Integrated GitHub Copilot/Codex workflow
- Added cost optimization strategies
- Expanded production examples

**v1.0** (2024)
- Initial version focused on Claude Opus + Claude Code
