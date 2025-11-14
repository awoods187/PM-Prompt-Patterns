# Architect-Builder Pattern - Claude Optimized

> Extends `prompt.md` with Claude-specific optimizations

## Overview

This Claude-optimized variant leverages Claude's extended context window, XML tag understanding, and prompt caching capabilities for maximum efficiency in the two-phase Architect-Builder workflow.

**Recommended models:**
- **Phase 1 (Design & Validation)**: Claude Opus 4 or Claude Sonnet 4.5 for strategic architecture decisions and codebase analysis
- **Phase 2 (Execution)**: Claude Sonnet 4.5 with Claude Code for autonomous implementation

---

## Prompt

<task>
You are implementing the Architect-Builder Pattern, a two-phase workflow for complex software development. Follow these phases sequentially.

## PHASE 1: ARCHITECTURE, DESIGN & VALIDATION

Use Claude Opus 4 or Claude Sonnet 4.5 for strategic thinking and codebase analysis.

**Design Request Template:**

<design_request>
I need to design [SYSTEM/FEATURE]. Please provide:

### 1. Architecture Blueprint
- Component diagram with clear boundaries
- Data flow and state management approach
- Interface contracts between components
- Error handling strategy
- Security considerations

### 2. Implementation Checklist
**Critical Path (Must-Have):**
- [Core functionality items]
- [Essential integrations]

**Enhancement Items (Nice-to-Have):**
- [Performance optimizations]
- [Additional features]

**Technical Debt to Avoid:**
- [Known anti-patterns]
- [Common pitfalls]

### 3. Validation Criteria
- How to verify the design works
- Edge cases to test
- Performance benchmarks
- Security requirements

### 4. Implementation Instructions
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
</design_request>

### Then validate the design against your existing codebase:

<validation_request>
Please analyze my codebase and validate this design:

<design>
[Your design above]
</design>

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
</validation_request>

---

## PHASE 2: AUTONOMOUS EXECUTION

Execute the validated design with Claude Code for systematic implementation.

**Execution Request Template:**

<execution_request>
Implement this validated design using Claude Code:

<validated_design>
[Paste refined design from Phase 1]
</validated_design>

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
</execution_request>

</task>

---

## Claude Optimizations Applied

### 1. XML Structure
- **`<task>` wrapper**: Clear task delineation for better parsing
- **`<design_request>`, `<validation_request>`, `<execution_request>`**: Structured input sections
- **`<design>`, `<validated_design>`**: Clear content boundaries for phase handoffs

### 2. Prompt Caching
The static prompt structure is cacheable, providing:
- 90%+ cost reduction on repeated uses
- Faster response times for design iterations
- Efficient multi-phase workflows

**Cache strategy:**
- Phase 1 & 2 prompts are fully cacheable
- Phase 3 varies based on design (partial caching)

### 3. Extended Context Window
- Leverages Claude's 200K token context for large codebases
- Can include extensive architectural documentation
- Supports multi-file validation in single request

### 4. Claude Code Integration

Claude Code naturally aligns with this two-phase pattern through its planning and execution modes:

**Planning Mode (Phase 1 - Design & Validation):**
- Use Claude Opus for strategic architectural decisions
- Analyze existing codebase patterns
- Design comprehensive solutions without making changes
- Validate approaches against current implementation

**Execution Mode (Phase 2 - Implementation):**
- Use Claude Sonnet for rapid, autonomous implementation
- Execute the validated design with systematic checkpoints
- Perform file operations, run tests, and create commits
- Complete the implementation with quality gates

This mirrors professional development workflows where senior architects design and experienced developers execute. The separation ensures thoughtful design before committing to implementation.

---

## Usage with Claude Code

### Phase 1: Design & Validation (Claude Web UI or API)

Use Claude Opus 4 or Sonnet 4.5 for strategic design and validation:

```python
import anthropic

client = anthropic.Anthropic(api_key="...")

response = client.messages.create(
    model="claude-opus-4-20250514",  # or claude-sonnet-4-5-20250929
    max_tokens=8000,
    system=[{
        "type": "text",
        "text": open("prompt.claude.md").read(),
        "cache_control": {"type": "ephemeral"}
    }],
    messages=[{
        "role": "user",
        "content": """
        <design_request>
        I need to design a RESTful API refactoring that:
        - Maintains backward compatibility with v1 API
        - Adds versioning support (header-based)
        - Implements rate limiting (100 req/min per user)
        </design_request>
        """
    }]
)

design = response.content[0].text
```

### Phase 2: Execution (Claude Code CLI)

```bash
# Continue in Claude Code session
# Paste the execution request with validated design
# Claude Code will:
# - Read/write files autonomously
# - Run tests at checkpoints
# - Create git commits
# - Report progress
```

---

## Cost Optimization

### Model Selection Strategy

| Phase | Recommended Model | Why |
|-------|------------------|-----|
| Phase 1: Design & Validation | Claude Opus 4 or Sonnet 4.5 | Strategic decisions, complex reasoning, pattern matching |
| Phase 2: Execution | Claude Sonnet 4.5 + Claude Code | Autonomous implementation, file operations |

### Token Management

**With prompt caching:**
- First design request: ~$0.08 (full cost)
- Subsequent iterations: ~$0.008 (cached)
- Average per feature: $0.06-0.21 (vs $2-5 without caching)

**Best practices:**
- Use same prompt structure for caching benefits
- Include static context in system prompt (cacheable)
- Put variable content in user messages only

---

## Production Workflow Example

### Complete Feature Implementation

```python
import anthropic
import os

client = anthropic.Anthropic()

# Load cached prompt
with open("prompt.claude.md") as f:
    prompt = f.read()

# Phase 1: Design
print("🎨 Phase 1: Designing architecture...")
design_response = client.messages.create(
    model="claude-opus-4-20250514",
    max_tokens=8000,
    system=[{
        "type": "text",
        "text": prompt,
        "cache_control": {"type": "ephemeral"}
    }],
    messages=[{
        "role": "user",
        "content": """
        <design_request>
        Design a user authentication service extraction from monolith:
        - Define service boundaries
        - Design API contract (REST + gRPC)
        - Plan data migration strategy
        - Include failure handling (circuit breakers, timeouts)

        Context: Python/FastAPI monolith, PostgreSQL, 10M users
        </design_request>
        """
    }]
)

design = design_response.content[0].text
print(f"✅ Design complete ({design_response.usage.input_tokens} tokens)")

# Save design for validation phase
with open("design_output.md", "w") as f:
    f.write(design)

print("\n📋 Phase 1 (continued): Validate design against codebase")
print("   Use the same session to validate the design")
print("   Or use Claude Code in planning mode for codebase analysis")

print("\n🚀 Phase 2: Use Claude Code to execute validated design")
print("   $ claude-code")
print("   Switch to execution mode with the validated design")
```

---

## Quality Checklist

After execution with Claude Code, verify:

**Architecture Alignment:**
- [ ] Implementation matches design intent
- [ ] All components properly integrated
- [ ] Interfaces match specifications

**Code Quality:**
- [ ] Tests pass (unit, integration, e2e)
- [ ] Code coverage meets threshold (>80%)
- [ ] Linting passes
- [ ] No security vulnerabilities

**Documentation:**
- [ ] Design decisions documented
- [ ] API/interface documentation complete
- [ ] Runbook/deployment guide updated
- [ ] Known limitations documented

**Operational Readiness:**
- [ ] Error handling comprehensive
- [ ] Logging/monitoring in place
- [ ] Performance benchmarks met
- [ ] Rollback procedure tested

---

## Troubleshooting

### Issue: Design phase output too verbose

**Solution:** Add constraint to design request:
```xml
<design_request>
...
**Output format:** Provide concise bulleted architecture (max 2 pages)
</design_request>
```

### Issue: Claude Code execution gets stuck

**Solution:** Break into smaller checkpoints:
```xml
<execution_request>
...
**Checkpoint strategy:**
- After each file creation: Verify imports
- After each function: Run unit test
- After each module: Run integration test
</execution_request>
```

### Issue: High token usage in validation phase

**Solution:** Use file references instead of pasting code:
```xml
<validation_request>
Please analyze these files in my codebase:
- src/auth/service.py
- src/api/routes.py
- src/models/user.py

[Do not paste code, Claude Code can read files directly]
</validation_request>
```

---

## See Also

- **Base prompt**: `prompt.md` - Complete examples, production patterns, business value
- **OpenAI variant**: `prompt.openai.md` - For use with GitHub Copilot/Codex
- **Gemini variant**: `prompt.gemini.md` - For use with Google AI Studio
- **Provider documentation**: `../../docs/provider-specific-prompts.md`

---

## Version History

**v2.1** (2025-11-14)
- Updated to two-phase workflow (merged validation into design phase)
- Added Claude Code planning and execution mode explanation
- Aligned with professional architect-developer workflow pattern
- Updated all phase references and cross-references

**v2.0** (2025-11-05)
- Renamed from "Opus Code Execution Pattern" to "Architect-Builder Pattern"
- Added Claude-specific XML structure and optimizations
- Integrated Claude Code workflow
- Added prompt caching strategy
- Expanded production examples

**v1.0** (2024)
- Initial Claude Opus + Claude Code workflow
- Basic three-window pattern
