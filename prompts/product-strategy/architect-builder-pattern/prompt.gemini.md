# Architect-Builder Pattern - Gemini Optimized

> Extends `prompt.md` with Gemini-specific optimizations

## Overview

This Gemini-optimized variant leverages Gemini's extended context window, multimodal capabilities, and instruction-following strengths for the two-phase Architect-Builder workflow. Particularly effective for design phases requiring visual diagrams or architectural sketches.

**Recommended models:**
- **Phase 1 (Design & Validation)**: Gemini 1.5 Pro or Gemini 2.0 Flash Exp for strategic architecture decisions and codebase analysis
- **Phase 2 (Execution)**: Gemini 2.0 Flash Exp or Gemini Code Assist for autonomous implementation

---

## System Instruction

```
You are implementing the Architect-Builder Pattern, a two-phase workflow for complex software development. Follow these phases sequentially with clear, structured outputs.

# PHASE 1: ARCHITECTURE, DESIGN & VALIDATION

Use Gemini 1.5 Pro or Gemini 2.0 Flash Exp for strategic thinking and validation.

**Design Request Template:**

I need to design [SYSTEM/FEATURE]. Please provide:

## 1. Architecture Blueprint
Deliverables:
- Component diagram with clear boundaries (describe or draw if diagram provided)
- Data flow and state management approach
- Interface contracts between components
- Error handling strategy
- Security considerations

## 2. Implementation Checklist
**Critical Path (Must-Have):**
1. [Core functionality item 1]
2. [Core functionality item 2]
3. [Essential integrations]

**Enhancement Items (Nice-to-Have):**
1. [Performance optimization 1]
2. [Additional feature 1]

**Technical Debt to Avoid:**
1. [Known anti-pattern 1]
2. [Common pitfall 1]

## 3. Validation Criteria
Testing approach:
- How to verify the design works
- Edge cases to test
- Performance benchmarks (specific metrics)
- Security requirements (specific checks)

## 4. Implementation Instructions
Specific guidance:
- File structure to create (exact paths)
- Testing approach (unit/integration/e2e)
- Dependencies to install (with versions)
- Configuration needed (environment variables, settings)

**Context:** [Include relevant constraints, existing patterns, tech stack, team size]

**Design Principles to Apply:**
1. Specificity over generality (be concrete and explicit)
2. Examples over explanations (show, don't just tell)
3. Structure over prose (use diagrams, lists, clear sections)
4. Constraints over freedom (define boundaries clearly)
5. Include rollback strategy for high-risk changes

## Then validate the design against your existing codebase:

**Validation Request:**

Please analyze my codebase and validate this design:

**Design to validate:**
[Your design above]

**Validation checklist:**

### 1. Pattern Consistency
Questions to answer:
- Does this align with existing patterns in the codebase?
- What modifications are needed for consistency?
- Can we reuse existing components?

### 2. Dependency Analysis
Assess:
- What existing code will be affected?
- Are there hidden dependencies?
- What's the blast radius of this change?

### 3. Risk Assessment
Identify:
- What could break?
- What needs extra testing?
- What are the rollback considerations?

### 4. Optimization Opportunities
Explore:
- Can we simplify the design?
- Are there performance considerations?
- What existing patterns can we leverage?

**Required output format:**
Refined implementation plan with:
1. Specific file paths
2. Code patterns to follow
3. Risk mitigation steps
4. Testing strategy

---

# PHASE 2: AUTONOMOUS EXECUTION

Execute the validated design systematically.

**Execution Request Template:**

Implement this validated design:

**Validated design:**
[Paste refined design from Phase 1]

**Execution parameters:**
- **Mode:** [careful/standard/fast]
- **Testing:** [unit/integration/e2e/all]
- **Documentation:** [inline/separate/both]

**Implementation order (follow strictly):**

1. **Core Infrastructure First**
   Tasks:
   - Create database schemas, base classes, interfaces
   - Checkpoint: Verify compilation and type safety

2. **Business Logic Second**
   Tasks:
   - Implement core algorithms, data transformations
   - Checkpoint: Run unit tests

3. **UI/API Layer Third**
   Tasks:
   - Build endpoints, controllers, views
   - Checkpoint: Run integration tests

4. **Tests Throughout**
   Tasks:
   - Write tests alongside implementation
   - Checkpoint: Full test suite passes

**Quality gates (must pass):**
- After each phase: Run relevant tests
- Before completion: Full test suite + linting
- Final: Code review checklist verification

**Instructions:**
Proceed autonomously but pause at each checkpoint for validation. Report progress after each phase.
```

---

## Gemini Optimizations Applied

### 1. Clear, Numbered Directives
- Explicit step-by-step instructions
- Numbered lists for sequential operations
- Concrete action items with deliverables

### 2. Extended Context Window
- Gemini 1.5 Pro: Up to 2M tokens context
- Can include entire codebases for validation
- Supports long architectural documentation
- Maintains coherence across all 3 phases

### 3. Multimodal Capabilities
Phase 1 can accept:
- Architecture diagrams (images)
- Existing system screenshots
- Whiteboard sketches of design ideas
- UML diagrams as visual context

### 4. Structured Reasoning
- Step-by-step breakdowns for complex analysis
- Clear section markers for parsing
- Explicit validation checklists
- Predictable output formatting

---

## Usage with Google AI Studio / Vertex AI

### Phase 1: Design (Gemini API or AI Studio)

Use Gemini 1.5 Pro or 2.0 Flash Exp for strategic design:

```python
import google.generativeai as genai

genai.configure(api_key="...")

# For complex designs, use Gemini 1.5 Pro
model = genai.GenerativeModel(
    model_name='gemini-1.5-pro',
    system_instruction=open("prompt.gemini.md").read()
)

# Can include diagrams/images alongside text
response = model.generate_content([
    """
    I need to design a RESTful API refactoring that:
    - Maintains backward compatibility with v1 API
    - Adds versioning support (header-based)
    - Implements rate limiting (100 req/min per user)
    - Uses consistent error response format

    Context: Python/FastAPI backend, PostgreSQL, 100K daily active users
    """,
    # Optional: Include existing architecture diagram
    # genai.upload_file("current_architecture.png")
])

design = response.text
print(design)
```

### Phase 2: Validation (Gemini 2.0 Flash Exp + Codebase)

```python
# Use faster model for validation
model = genai.GenerativeModel(
    model_name='gemini-2.0-flash-exp',
    system_instruction="You are validating an architecture design against an existing codebase."
)

# Load codebase files
codebase_files = []
for file_path in ["src/api/routes.py", "src/middleware/auth.py", "src/models/user.py"]:
    with open(file_path) as f:
        codebase_files.append(f"# {file_path}\n{f.read()}")

codebase_context = "\n\n".join(codebase_files)

response = model.generate_content(f"""
Please validate this design:

{design}

Against this codebase:

{codebase_context}

Check for: pattern consistency, dependencies, risks, and optimization opportunities.
Provide a refined implementation plan.
""")

validated_design = response.text
```

### Phase 3: Execution (Gemini Code Assist or Manual)

**Option A: Manual implementation with Gemini assistance**

```python
# Generate implementation for each component
def generate_component(component_spec: str) -> str:
    """Use Gemini to generate implementation from spec."""
    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    response = model.generate_content(f"""
    Generate production-ready Python code with tests for:

    {component_spec}

    Include:
    - Type hints
    - Docstrings
    - Error handling
    - Unit tests
    """)

    return response.text

# Example: Generate rate limiting middleware
rate_limit_spec = """
Create FastAPI middleware for rate limiting:
- 100 requests per minute per user
- Use Redis for distributed rate limiting
- Return 429 status with Retry-After header
- Support both API key and JWT authentication
"""

code = generate_component(rate_limit_spec)
print(code)
```

**Option B: Iterative implementation**

```python
# Implement phase by phase
phases = [
    "Core Infrastructure: Database schemas and base classes",
    "Business Logic: Rate limiting algorithm",
    "API Layer: FastAPI endpoints with rate limiting",
    "Tests: Unit and integration tests"
]

for i, phase in enumerate(phases, 1):
    print(f"\n{'='*60}")
    print(f"PHASE {i}: {phase}")
    print('='*60)

    response = model.generate_content(f"""
    Implement {phase} based on this validated design:

    {validated_design}

    Provide complete, production-ready code.
    """)

    print(response.text)

    # Save to file
    with open(f"phase_{i}_output.py", "w") as f:
        f.write(response.text)
```

---

## Cost Optimization

### Model Selection Strategy

| Phase | Recommended Model | Cost (per 1M tokens) | Why |
|-------|------------------|---------------------|-----|
| Phase 1: Design & Validation | Gemini 1.5 Pro or 2.0 Flash Exp | $1.25/$5.00 or $0 (free) | Strategic decisions, complex reasoning, codebase analysis |
| Phase 2: Execution | Gemini 2.0 Flash Exp | $0 (free tier) | Code generation |

### Token Management

**Typical costs per feature:**
- Phase 1 (Design & Validation with 1.5 Pro): $0.05-0.15
- Phase 1 (Design & Validation with 2.0 Flash Exp): $0 (free tier)
- Phase 2 (Execution): $0 (free tier)
- **Total: $0-0.15** (extremely cost-effective)

**Best practices:**
- Use Gemini 2.0 Flash Exp for validation and execution (free tier)
- Reserve 1.5 Pro for complex architectural decisions only
- Leverage 2M token context to include entire codebases
- Use multimodal inputs to reduce text descriptions

---

## Multimodal Design Example

### Including Architecture Diagrams

```python
import PIL.Image

# Upload existing architecture diagram
current_arch = genai.upload_file("current_system.png")

model = genai.GenerativeModel('gemini-1.5-pro')

response = model.generate_content([
    current_arch,
    """
    Based on this current architecture diagram, design a migration to microservices:
    - Identify service boundaries
    - Propose communication patterns (REST, gRPC, events)
    - Plan data migration strategy
    - Maintain backward compatibility during transition

    Provide updated architecture diagram description and implementation plan.
    """
])

print(response.text)
```

### Including Code Sketches

```python
# Upload whiteboard sketch of design idea
sketch = genai.upload_file("design_sketch.jpg")

response = model.generate_content([
    sketch,
    """
    Convert this whiteboard sketch into:
    1. Formal architecture blueprint
    2. Component specifications
    3. Interface definitions
    4. Implementation plan

    Follow the Architect-Builder Pattern structure.
    """
])
```

---

## Quality Checklist

After execution, verify:

**Architecture Alignment:**
- [ ] Implementation matches design intent
- [ ] All components properly integrated
- [ ] Interfaces match specifications

**Code Quality:**
- [ ] Tests pass (unit, integration, e2e)
- [ ] Code coverage meets threshold (>80%)
- [ ] Linting passes (pylint, mypy, etc.)
- [ ] No security vulnerabilities

**Documentation:**
- [ ] Design decisions documented
- [ ] API documentation complete
- [ ] Deployment guide updated
- [ ] Known limitations documented

**Operational Readiness:**
- [ ] Error handling comprehensive
- [ ] Logging/monitoring in place
- [ ] Performance benchmarks met
- [ ] Rollback procedure tested

---

## Troubleshooting

### Issue: Design output too abstract

**Solution:** Request concrete examples in prompt:
```
Provide architecture design with:
- Specific class/module names
- Code snippets for critical interfaces
- Exact database schema DDL
- Sample API request/response payloads
```

### Issue: Validation missing context

**Solution:** Leverage extended context window:
```python
# Include entire codebase (Gemini 1.5 Pro supports 2M tokens)
all_files = []
for root, dirs, files in os.walk("src"):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path) as f:
                all_files.append(f"# {path}\n{f.read()}")

# Send entire codebase for validation
codebase = "\n\n".join(all_files)
response = model.generate_content(f"Validate design against:\n{codebase}")
```

### Issue: Execution phase lacks detail

**Solution:** Request step-by-step implementation:
```
Implement this design in phases:

Phase 1: Core Infrastructure
- Generate complete code for database models
- Include migration scripts
- Show testing commands

Phase 2: Business Logic
...

For each phase, provide:
- Complete, runnable code
- Setup instructions
- Test commands
- Validation steps
```

---

## See Also

- **Base prompt**: `prompt.md` - Complete examples, production patterns, business value
- **Claude variant**: `prompt.claude.md` - For use with Claude Code
- **OpenAI variant**: `prompt.openai.md` - For use with GitHub Copilot/Codex
- **Provider documentation**: `../../docs/provider-specific-prompts.md`

---

## Version History

**v2.1** (2025-11-14)
- Updated to two-phase workflow (merged validation into design phase)
- Aligned with professional architect-developer workflow pattern
- Updated all phase references and cost calculations

**v2.0** (2025-11-05)
- Renamed from "Opus Code Execution Pattern" to "Architect-Builder Pattern"
- Made model-agnostic with Gemini-specific optimizations
- Added multimodal design examples (diagrams, sketches)
- Leveraged Gemini's extended context window (2M tokens)
- Added cost-effective execution strategies

**v1.0** (2024)
- Initial version focused on Claude Opus + Claude Code
