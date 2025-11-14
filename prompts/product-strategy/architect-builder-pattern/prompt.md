# Architect-Builder Pattern

**Complexity**: 🔴 Advanced
**Category**: Product Strategy / Development Workflow
**Model Compatibility**: ✅ Claude (all) | ✅ GPT-5 | ✅ Gemini

## Overview

A production-grade two-phase workflow that separates strategic architectural design from tactical implementation. This pattern uses a high-capability model for system design and architecture with a validation phase for codebase analysis, and an execution phase for autonomous implementation.

**Business Value**:
- Reduce architecture mistakes that cost >$10K to fix
- 10-20x cost reduction vs using premium models for all implementation
- 3-5x quality improvement vs direct implementation without design
- Enable complex system design with confident execution
- Build institutional knowledge through documented design decisions

**Use Cases**:
- Complex systems requiring both high-level design and detailed implementation
- Multi-file codebases or system refactoring
- Greenfield projects with unclear technical approach
- Legacy system modernization
- API refactoring with backward compatibility
- Database schema evolution
- Microservices architecture design

**Production metrics**:
- Design-to-deploy time: <2 hours for medium complexity features
- First-time success rate: >80% (implementations passing tests without revision)
- Cost per feature: $0.06-0.21 (vs $2-5 for pure premium model usage)
- Pattern reuse rate: >60% after building library
- Quality score: >8/10 on automated checks

---

## Prompt
```
You are implementing the Architect-Builder Pattern, a two-phase workflow for
complex software development. Follow these phases sequentially.

## PHASE 1: ARCHITECTURE & DESIGN

Use your most capable model for strategic thinking.

**Design Request Template:**

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

Then analyze the design against your existing codebase.

**Validation Request Template:**

Please analyze my codebase and validate this design:

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

## PHASE 2: AUTONOMOUS EXECUTION

Execute the validated design with systematic checkpoints.

**Execution Request Template:**

Implement this validated design:

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

---

## WORKFLOW PATTERNS

### Pattern 1: Progressive Enhancement

Start simple, iterate to complex.

**Iteration 1: MVP**
- Design: Core functionality only
- Validate: Check feasibility
- Execute: Basic implementation with tests

**Iteration 2: Robustness**
- Design: Add error handling
- Validate: Check error paths
- Execute: Implement resilience

**Iteration 3: Performance**
- Design: Optimization strategy
- Validate: Profile bottlenecks
- Execute: Optimize critical paths

### Pattern 2: Safety-First (High-Risk Changes)

**Phase 1: Design with Safety**
- Include rollback strategy
- Plan for feature flags
- Design for backward compatibility

**Phase 2: Create Safety Checklist**
- [ ] Database migrations are reversible
- [ ] API changes are backward compatible
- [ ] Feature flags control new behavior
- [ ] Monitoring alerts configured
- [ ] Rollback procedure documented

**Phase 3: Implement with Guards**
- Use feature flags
- Implement incrementally
- Deploy to staging first

### Pattern 3: Parallel Development

For multiple related features:

**Phase 1: Design All Features**
- Create comprehensive architecture
- Identify shared components
- Plan dependency order

**Phase 2: Validate Together**
- Check for conflicts
- Optimize shared code
- Identify integration points

**Phase 3: Execute in Order**
- Implement shared components first
- Build dependent features second
- Integrate and test third

---

## COST OPTIMIZATION

### Smart Model Selection

| Complexity | Design Phase | Validation Phase | Execution Phase |
|------------|--------------|------------------|-----------------|
| High | Premium model | Mid-tier model | Mid-tier model |
| Medium | Premium model | Skip (direct to execution) | Mid-tier model |
| Low | Skip (direct implementation) | - | Mid-tier model |

### Token Management

**Design Phase:**
- Use concise prompts with rich context
- Request structured output (easier to parse)
- Save successful designs for similar problems

**Validation Phase:**
- Reference files instead of pasting code
- Summarize results concisely
- Focus on deltas from design

**Execution Phase:**
- Let the model read files directly
- Use incremental updates
- Cache common patterns

---

## QUALITY CHECKLIST

After execution, verify:

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

## TROUBLESHOOTING

**Issue: Design too abstract**
- Solution: Request specific code examples and pseudocode
- Add: "Include concrete examples for critical sections"

**Issue: Validation finds conflicts**
- Solution: Iterate design with conflicts in mind
- Add: Compatibility requirements to design prompt

**Issue: Execution gets stuck**
- Solution: Break into smaller phases
- Add: More explicit checkpoints and validation steps

**Issue: High token usage**
- Solution: Use file references and summaries
- Add: "Provide summary-only output between phases"

**Issue: Tests failing after execution**
- Solution: More specific test requirements in design
- Add: Test cases and edge cases to Phase 1
```

---

## Production Patterns

### Pattern 1: API Refactoring with Backward Compatibility

**Phase 1: Design**
```
Design a RESTful API refactoring that:
- Maintains backward compatibility with v1 API
- Adds versioning support (header-based)
- Implements rate limiting (100 req/min per user)
- Uses consistent error response format
- Includes OpenAPI/Swagger documentation
Check existing API patterns in /src/api:
- Which endpoints follow REST conventions?
- What's our current error response format?
- How do we currently handle authentication?
- What rate limiting exists (if any)?
```

**Phase 2: Execute**
```
Implement the validated API design:
1. Create versioning middleware
2. Migrate one endpoint as proof of concept
3. Add comprehensive tests (unit + integration)
4. Update OpenAPI documentation
5. Deploy to staging with monitoring
```

### Pattern 2: Database Schema Evolution

**Phase 1: Design**
```
Design a migration strategy from MongoDB to PostgreSQL:
- Handle 10M records with <1hr downtime
- Maintain data integrity (checksums, validation)
- Include rollback plan
- Zero data loss tolerance
- Preserve query performance
Analyze current data access patterns:
- Which queries are most frequent? (top 10)
- What's the current schema structure?
- Identify migration risks (data types, relationships)
- Check for data inconsistencies
```

**Phase 2: Execute**
```
Execute phased migration:
Phase 1: Set up PostgreSQL schema and indexes
Phase 2: Implement dual-write pattern (write to both DBs)
Phase 3: Migrate historical data in batches (1M at a time)
Phase 4: Switch reads to PostgreSQL (gradual rollout)
Phase 5: Verify data integrity, then remove MongoDB code
```

### Pattern 3: Microservices Extraction

**Phase 1: Design**
```
Extract user authentication service from monolith:
- Define service boundaries (what stays, what moves)
- Design API contract (REST + gRPC)
- Plan data migration strategy
- Include service discovery approach
- Design failure handling (circuit breakers, timeouts)
Analyze monolith dependencies:
- What code depends on auth module?
- Are there circular dependencies?
- What shared state exists?
- Performance impact of network calls?
```

**Phase 3: Execute**
```
Extract service incrementally:
1. Create new service with same interface
2. Implement facade pattern in monolith
3. Route 10% of traffic to new service
4. Monitor error rates and latency
5. Gradually increase traffic to 100%
6. Remove old code from monolith
```

---

## Quality Evaluation

### Success Criteria

**Design Phase:**
- [ ] Architecture diagram is clear and complete
- [ ] All components have defined responsibilities
- [ ] Interfaces are explicitly specified
- [ ] Error handling strategy is comprehensive
- [ ] Rollback plan exists for high-risk changes

**Validation Phase:**
- [ ] Codebase patterns identified and documented
- [ ] Risks assessed with mitigation strategies
- [ ] Dependencies mapped completely
- [ ] Performance implications understood
- [ ] Testing strategy is comprehensive

**Execution Phase:**
- [ ] All tests pass (unit, integration, e2e)
- [ ] Code coverage >80% for new code
- [ ] Linting passes with zero warnings
- [ ] Documentation complete and accurate
- [ ] Monitoring and logging in place

### Evaluation Metrics

| Metric               | Target | Measurement Method                     |
|----------------------|--------|----------------------------------------|
| Design Completeness  | 100%   | All sections of design template filled |
| Architecture Clarity | >8/10  | Team review score                      |
| Test Coverage        | >80%   | Automated coverage tool                |
| First-Time Success   | >80%   | Tests pass without code changes        |
| Pattern Consistency  | >90%   | Code review checklist                  |
| Documentation Quality| >7/10  | Peer review score                      |

---

## Usage Notes

### When to Use This Pattern

✅ **Ideal for:**
- Complex systems requiring both high-level design and detailed implementation
- Projects where architecture mistakes are expensive (>$10K impact)
- Multi-file codebases or system refactoring
- Greenfield projects with unclear technical approach
- Legacy system modernization
- Team knowledge building (design docs become documentation)

❌ **Not ideal for:**
- Simple CRUD operations or single-file scripts
- Well-understood problems with established patterns
- Rapid prototyping where architecture can evolve
- Time-critical hotfixes (skip to direct implementation)
- Trivial bug fixes

### Model Selection Guidance

**Design Phase (Premium Model):**
- Use for strategic thinking and architecture
- Worth the cost for complex decisions
- Saves money by preventing costly mistakes
- Pattern matching and code analysis
- Cost-effective for systematic checks
- Can skip for low-risk changes

**Execution Phase (Mid-Tier Model):**
- Tactical implementation
- Follows explicit design
- More cost-effective than premium for execution

### Integration with Development Workflow

**With Version Control:**
```bash
# Design phase
git checkout -b feature/design
# Create design doc, commit
git commit -m "docs: Add architecture design"

# Validation phase
git checkout -b feature/validation
# Update design based on validation
git commit -m "docs: Refine design based on validation"

# Execution phase
git checkout -b feature/implementation
# Implement and test
git commit -m "feat: Implement validated design"
```

**With CI/CD:**
- Trigger validation checks on design commit
- Auto-run tests after execution
- Deploy successful implementations to staging
- Monitor metrics in production

---

## Common Issues & Fixes

### Issue 1: Design Phase Takes Too Long

**Symptoms:**
- Design phase exceeds 10 minutes
- Multiple iterations needed
- Unclear or vague outputs

**Root Cause:**
- Insufficient context provided
- Problem not well-scoped
- Too ambitious for single pass

**Solution:**
```
1. Break down into smaller sub-problems
2. Provide more specific constraints
3. Include concrete examples in design request
4. Reference similar existing systems
```

### Issue 2: Validation Finds Major Conflicts

**Symptoms:**
- Design doesn't fit existing patterns
- High risk of breaking changes
- Significant refactoring needed

**Root Cause:**
- Codebase patterns not understood before design
- Design made in isolation
- Existing constraints not communicated

**Solution:**
```
1. Run validation earlier (before full design)
2. Include codebase constraints in design phase
3. Request incremental design (start small)
4. Consider alternative approaches
```

### Issue 3: Execution Deviates from Design

**Symptoms:**
- Implementation doesn't match design
- Unexpected technical challenges
- Design assumptions proven wrong

**Root Cause:**
- Design too abstract
- Technical feasibility not validated
- Implementation details missing

**Solution:**
```
1. Request more concrete design with code examples
2. Add proof-of-concept phase before full implementation
3. Include validation checkpoints in execution
4. Iterate design based on execution learnings
```

### Issue 4: High Cost / Token Usage

**Symptoms:**
- Costs exceed $1 per feature
- Long context windows
- Repeated information

**Root Cause:**
- Inefficient prompting
- Not using file references
- Redundant context

**Solution:**
```
1. Use file references instead of pasting code
2. Request summary-only outputs
3. Build template library for common patterns
4. Cache successful designs for reuse
```

---

## Related Prompts

- [`developing-internal-tools/code-review-refactoring`](../../developing-internal-tools/code-review-refactoring/prompt.md) - For refactoring existing code
- [`product-strategy/meta-prompt-designer`](../meta-prompt-designer/prompt.md) - For designing new prompts
- [`developing-internal-tools/github-actions-python-cicd`](../../developing-internal-tools/github-actions-python-cicd/prompt.md) - For CI/CD setup

---

## Version History

**v2.0** (2025-11-14)
- Renamed from "Opus Code Execution Pattern" to "Architect-Builder Pattern"
- Made model-agnostic (works with any LLM providers)
- Expanded with detailed production patterns
- Added comprehensive troubleshooting guide
- Included cost optimization strategies
- Added success metrics and evaluation criteria

**v1.0** (2025-10-01)
- Initial version focused on Claude Opus + Claude Code
- Basic three-window workflow
- Limited examples and patterns
