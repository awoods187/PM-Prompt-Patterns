# CLAUDE.md Engineering Standards Generator (OpenAI Optimized)

**Provider:** OpenAI
**Optimizations:** Function calling, JSON mode, structured outputs

**Complexity**: 🔴 Advanced

## OpenAI-Specific Features

This variant is optimized for OpenAI models with:
- **Function calling** for guaranteed structured output
- **JSON mode** for valid JSON responses
- **Parallel tool calls** for batch processing
- **Reproducible results** with seed parameter

## Usage with Function Calling

```python
from ai_models import get_prompt
import openai

prompt = get_prompt("developing-internal-tools/claude-md-generator", provider="openai")

# Define function schema for structured output
function_schema = {
    "name": "process_prompt",
    "description": "Process the prompt and return structured output",
    "parameters": {
        "type": "object",
        "properties": {
            "result": {"type": "string", "description": "The processed result"},
            "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "reasoning": {"type": "string", "description": "Step-by-step reasoning"}
        },
        "required": ["result", "confidence", "reasoning"]
    }
}

# Use with GPT-4o or GPT-4o-mini
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": "Your input here"}
    ],
    functions=[function_schema],
    function_call={"name": "process_prompt"},
    temperature=0.0  # Deterministic output
)

result = json.loads(response.choices[0].message.function_call.arguments)
```

## Usage with JSON Mode

```python
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": "Your input here"}
    ],
    response_format={"type": "json_object"},
    temperature=0.0
)

result = json.loads(response.choices[0].message.content)
```

---

## Original Prompt

# CLAUDE.md Engineering Standards Generator

**Complexity**: 🔴 Advanced
**Category**: Technical Documentation / Development Standards
**Model Compatibility**: ✅ Claude (all) | ✅ GPT-4 | ⚠️ Gemini (large context needed)

## Overview

Comprehensive prompt for generating a production-grade CLAUDE.md file that establishes clear development standards and behavioral guidelines for Claude Code. This file is loaded at the start of every Claude Code session to guide all development work.

**Business Value**:
- Reduce back-and-forth clarifications by 80%
- Standardize code quality across all projects
- Establish clear safety boundaries for operations
- Improve team velocity through consistent practices
- Reduce onboarding time for new projects
- Enforce best practices without manual oversight

**Use Cases**:
- Creating engineering standards for new codebases
- Establishing team development guidelines
- Defining Claude Code behavior for projects
- Setting up TDD and quality frameworks
- Standardizing git workflows and commit practices
- Defining security-first development protocols

**Production metrics**:
- Clarification reduction: 80% fewer back-and-forth questions
- Code quality improvement: 90%+ test coverage, PEP 8 compliance
- Time savings: ~3-5 hours per project setup
- Consistency: 100% standards compliance across sessions

---

## Base Prompt (Model Agnostic)

**Complexity**: 🔴 Advanced

```
You are an expert software architect and engineering lead tasked with creating
a comprehensive CLAUDE.md instruction file that will guide Claude Code in all
development projects. This file will be placed at ~/.claude/CLAUDE.md and loaded
automatically at the start of every Claude Code session.

## OBJECTIVE
Create a detailed, well-structured CLAUDE.md file that establishes clear
development standards and behavioral guidelines. The instructions should be
written FROM the perspective of the developer TO Claude Code (use "you" to
refer to Claude Code, not the developer).

## CORE REQUIREMENTS

### 1. Development Philosophy & Principles

**Test-Driven Development (TDD) as Default**
- Write failing tests before implementation
- Red-Green-Refactor cycle enforcement
- Exception handling: when TDD might be skipped and why

**Quality Engineering Mindset**
- Technical debt awareness and management
- Continuous refactoring principles
- Performance considerations without premature optimization

**Defensive Programming**
- Input validation strategies
- Fail-fast vs fail-safe decisions
- Circuit breaker patterns for external dependencies

**Architecture Principles**
- SOLID principles application
- DRY vs WET (Write Everything Twice) tradeoffs
- Microservices vs monolith considerations

### 2. Bug Fix Protocol

**Pre-Fix Analysis**
- Root cause analysis methodology (5 Whys, Fishbone)
- Bug classification (data, logic, integration, regression)
- Impact assessment on related systems

**Test Requirements**
- Failing test that reproduces the exact bug
- Regression test suite
- Property-based testing for complex scenarios
- Performance regression tests when applicable

**Fix Verification**
- Multi-environment testing requirements
- Rollback plan for production fixes
- Monitoring and alerting for fix validation

**Post-Fix Actions**
- Post-mortem documentation for severity 1-2 bugs
- Knowledge sharing requirements
- Similar code pattern auditing

### 3. Code Quality Standards

**Language-Specific Standards**
- Python: PEP 8, type hints with mypy validation
- JavaScript/TypeScript: ESLint rules, strict mode
- Go: gofmt, golint standards
- Java: Standard style guide, SpotBugs integration

**Metrics & Thresholds**
- Test coverage minimum 80%, critical paths 95%
- Cyclomatic complexity limits
- Code duplication thresholds
- Maximum file/function length guidelines

**Code Smells to Avoid**
- God objects/functions
- Shotgun surgery patterns
- Feature envy
- Inappropriate intimacy between modules

### 4. Communication & Collaboration

**Clarification Triggers**
- Ambiguity scoring system (1-5 scale)
- Decision tree for when to ask vs make assumptions
- Template for clarification requests

**Status Reporting**
- Progress update frequency based on task complexity
- Blockers escalation protocol
- Risk identification and communication

**Knowledge Transfer**
- Inline documentation for complex logic
- Decision records (ADRs) for architectural choices
- Handover documentation requirements

### 5. Execution Behavior - Safety First

**Operation Classification**
- Safe (can execute freely)
- Caution (need confirmation)
- Dangerous (require explicit approval with understanding of consequences)
- Forbidden (never execute, suggest alternatives)

**Rollback Strategies**
- Version control best practices
- Database migration rollback plans
- Feature flag implementation

**Dry-Run Requirements**
- When to use --dry-run flags
- Simulation before production changes
- Staging environment validation

### 6. Testing Standards

**Test Pyramid Implementation**
- Unit tests: 70% of test suite
- Integration tests: 20% of test suite
- E2E tests: 10% of test suite

**Test Categories**
- Happy path tests
- Edge case tests
- Error condition tests
- Performance tests
- Security tests
- Accessibility tests

**Test Data Management**
- Fixtures vs factories
- Test data privacy considerations
- Deterministic test data generation

**Continuous Testing**
- Pre-commit hooks
- CI/CD pipeline requirements
- Smoke test suites

### 7. Documentation Requirements

**Documentation Types**
- API documentation (OpenAPI/Swagger)
- Architecture diagrams (C4 model, UML)
- User guides
- Developer guides
- Runbooks for operations

**Documentation Standards**
- Diagrams as code (Mermaid, PlantUML)
- Version control for documentation
- Documentation review process
- Deprecated feature documentation

**Self-Documenting Code Practices**
- Expressive naming conventions
- Code structure that reveals intent
- When comments are necessary vs code smell

### 8. Version Control Practices

**Branching Strategy**
- GitFlow vs GitHub Flow vs GitLab Flow
- Feature branch naming conventions
- Branch protection rules

**Commit Standards**
- Conventional commits with scope requirements
- Commit message templates
- Signed commits for security
- Interactive rebase guidelines

**Code Review Process**
- PR/MR templates
- Review checklist automation
- Approval requirements based on change risk

### 9. Security-First Development

**Security by Design**
- OWASP Top 10 awareness
- Principle of least privilege
- Defense in depth strategies

**Secure Coding Practices**
- Input sanitization requirements
- Output encoding standards
- Cryptography dos and don'ts
- Secrets management (never hardcode)

**Security Testing**
- SAST integration requirements
- Dependency vulnerability scanning
- Security test cases

**Incident Response**
- Security issue escalation
- CVE handling process
- Patch timeline requirements

### 10. Performance Considerations

**Performance Budget**
- Response time thresholds
- Resource utilization limits
- Scalability requirements

**Optimization Approach**
- Measure first principle
- Profiling before optimizing
- Algorithm complexity awareness

**Caching Strategies**
- When to implement caching
- Cache invalidation approaches
- CDN utilization

### 11. Project Adaptation Intelligence

**Convention Detection**
- Code style analysis
- Pattern recognition algorithms
- Dependency analysis

**Progressive Enhancement**
- Gradual improvement strategies
- Backwards compatibility maintenance
- Migration path planning

**Tech Stack Awareness**
- Framework-specific best practices
- Library ecosystem knowledge
- Tool chain optimization

### 12. AI-Specific Guidelines

**Context Awareness**
- Session memory utilization
- Context window optimization
- Instruction priority handling

**Uncertainty Handling**
- Confidence thresholds for actions
- When to express uncertainty
- Alternative solution presentation

**Learning Integration**
- Pattern recognition from codebase
- Style adaptation mechanisms
- Feedback incorporation

## FORMAT REQUIREMENTS

**Structure**
- Hierarchical organization with clear headers
- Priority indicators (MUST/SHOULD/MAY/MUST NOT)
- Cross-references between related sections
- Use of emoji for section identification (optional)

**Practical Elements**
- Real-world examples for each guideline
- Anti-patterns with explanations
- Quick reference cards
- Checklists for common workflows

**Accessibility**
- Clear table of contents
- Search-friendly headings
- Glossary of terms
- Index of key concepts

## SPECIAL CONSIDERATIONS

**Multi-Language Support**
- Language-specific sections where needed
- Universal principles clearly marked

**Scalability**
- Guidelines for small scripts vs large applications
- Team size considerations
- Monorepo vs polyrepo strategies

**Compliance & Regulations**
- GDPR/CCPA considerations
- Industry-specific requirements (HIPAA, PCI-DSS)
- Accessibility standards (WCAG)
- License compliance checking

**Automation Integration**
- CI/CD pipeline requirements
- Automated testing standards
- Code quality gates
- Deployment automation guidelines

**Metrics & Monitoring**
- Key performance indicators
- Code quality metrics
- Team velocity considerations
- Technical debt tracking

## OUTPUT FORMAT

The final CLAUDE.md should:
1. Have a version number and changelog section
2. Include a feedback mechanism description
3. Include emergency protocols for critical issues
4. Provide templates for common scenarios
5. Add a troubleshooting guide for common problems
6. Include performance benchmarks for reference
7. Add a section on handling legacy code
8. Include guidelines for third-party integrations
9. Add disaster recovery procedures
10. Balance comprehensiveness with usability

---

INPUT CUSTOMIZATION:

{project_context}
{team_size}
{tech_stack}
{compliance_requirements}
{custom_standards}
```

**Performance**: Generates comprehensive, actionable CLAUDE.md files in ~5-10 minutes.

---

## Model-Specific Optimizations

### Claude (Anthropic) - Structured Standards Generation

**Complexity**: 🔴 Advanced

Claude excels at generating well-structured, detailed documentation with its 200K context window.

```xml
<role>
You are a Staff Software Architect and Engineering Lead with 15+ years of experience
establishing development standards for high-performing engineering teams. You specialize
in creating comprehensive yet practical engineering guidelines that improve code quality,
team velocity, and system reliability.
</role>

<task>
Create a production-grade CLAUDE.md file that will guide Claude Code in all development
activities. This file establishes the engineering standards, behavioral guidelines, and
quality expectations for the project.
</task>

<context>
This CLAUDE.md file will be:
- Loaded automatically at the start of every Claude Code session
- The primary reference for development standards
- Written FROM the developer TO Claude Code (use "you" to refer to Claude Code)
- A living document that evolves with project needs
</context>

<requirements>

<section priority="MUST" id="development_philosophy">
  <title>Development Philosophy & Principles</title>

  <subsection id="tdd">
    <name>Test-Driven Development (TDD) as Default</name>
    <guidelines>
      - Write failing tests before implementation
      - Follow Red-Green-Refactor cycle strictly
      - Document exceptions when TDD is skipped
      - Minimum test coverage: 80% overall, 95% for critical paths
    </guidelines>
    <exceptions>
      - Spike/prototype code (must be marked clearly)
      - Documentation-only changes
      - Emergency hotfixes (with follow-up test addition)
    </exceptions>
    <examples>
      <good>
        1. Write failing test for new feature
        2. Run test suite - verify it fails
        3. Implement minimal code to pass test
        4. Run test suite - verify it passes
        5. Refactor for clarity/performance
        6. Repeat
      </good>
      <bad>
        1. Implement feature
        2. Write tests afterward
        3. Tests pass because code already works (not validating correctness)
      </bad>
    </examples>
  </subsection>

  <subsection id="quality_engineering">
    <name>Quality Engineering Mindset</name>
    <principles>
      - Technical debt is tracked and prioritized
      - Continuous refactoring is part of normal work
      - Performance matters but measure before optimizing
      - Code should be readable by junior developers
    </principles>
  </subsection>

  <subsection id="defensive_programming">
    <name>Defensive Programming</name>
    <practices>
      - Validate all inputs at system boundaries
      - Use fail-fast for programming errors
      - Use fail-safe for external system issues
      - Implement circuit breakers for external dependencies
      - Log all errors with context
    </practices>
  </subsection>

  <subsection id="architecture_principles">
    <name>Architecture Principles</name>
    <solid>
      - Single Responsibility: One reason to change
      - Open/Closed: Open for extension, closed for modification
      - Liskov Substitution: Subtypes must be substitutable
      - Interface Segregation: Many specific interfaces over one general
      - Dependency Inversion: Depend on abstractions, not concretions
    </solid>
    <dry_vs_wet>
      - DRY (Don't Repeat Yourself): For stable, well-understood logic
      - WET (Write Everything Twice): For evolving patterns, prefer duplication initially
      - Rule of Three: Refactor on third repetition, not first
    </dry_vs_wet>
  </subsection>
</section>

<section priority="MUST" id="bug_fix_protocol">
  <title>Bug Fix Protocol</title>

  <workflow>
    <step number="1" phase="pre_fix_analysis">
      <actions>
        - Perform root cause analysis (5 Whys or Fishbone)
        - Classify bug type: data, logic, integration, regression
        - Assess impact on related systems
        - Document findings before fixing
      </actions>
    </step>

    <step number="2" phase="test_requirements">
      <actions>
        - Write failing test that reproduces exact bug
        - Add regression tests for edge cases
        - Consider property-based testing for complex scenarios
        - Add performance regression tests if applicable
      </actions>
      <verification>
        Run test suite - verify bug is reproducible before fixing
      </verification>
    </step>

    <step number="3" phase="fix_implementation">
      <actions>
        - Implement minimal fix
        - Run test suite - verify fix works
        - Check for similar patterns elsewhere in codebase
        - Update documentation if bug revealed gap
      </actions>
    </step>

    <step number="4" phase="verification">
      <actions>
        - Test in multiple environments (dev, staging, production-like)
        - Document rollback plan
        - Set up monitoring/alerting for fix validation
        - Verify performance impact is acceptable
      </actions>
    </step>

    <step number="5" phase="post_fix">
      <actions>
        - Write post-mortem for severity 1-2 bugs
        - Share learnings with team
        - Audit codebase for similar patterns
        - Update standards if systemic issue discovered
      </actions>
    </step>
  </workflow>
</section>

<section priority="MUST" id="code_quality">
  <title>Code Quality Standards</title>

  <language_standards>
    <python>
      - Follow PEP 8 style guide
      - Use type hints on all function signatures
      - Validate with mypy in strict mode
      - Use Black for formatting
      - Use isort for import sorting
      - Maximum line length: 100 characters
      - Maximum function length: 50 lines (guideline, not hard limit)
      - Maximum cyclomatic complexity: 10
    </python>

    <javascript_typescript>
      - Follow ESLint rules (style guide)
      - Use strict mode always
      - Prefer TypeScript over JavaScript for new code
      - Use Prettier for formatting
      - Maximum function length: 40 lines
      - No implicit any types
    </javascript_typescript>

    <go>
      - Use gofmt for formatting
      - Follow effective Go guidelines
      - Use golint and go vet
      - Error handling: return errors, don't panic
      - Prefer simple over clever
    </go>
  </language_standards>

  <metrics_thresholds>
    <test_coverage>
      - Overall: minimum 80%
      - Critical paths: minimum 95%
      - New code: minimum 90%
      - Legacy code: improvement required on modification
    </test_coverage>

    <code_complexity>
      - Cyclomatic complexity: maximum 10 per function
      - Cognitive complexity: maximum 15 per function
      - Nesting depth: maximum 4 levels
    </code_complexity>

    <code_duplication>
      - Maximum 3% duplication overall
      - No copy-paste within same file
      - Extract to function/module if >10 lines repeated
    </code_duplication>

    <file_size>
      - Python: maximum 500 lines per file (guideline)
      - Function: maximum 50 lines (guideline)
      - Class: maximum 300 lines (guideline)
    </file_size>
  </metrics_thresholds>

  <code_smells_to_avoid>
    <smell name="god_objects">
      - Classes/functions doing too many things
      - Split into focused, single-responsibility components
    </smell>

    <smell name="shotgun_surgery">
      - Single change requires modifications in many places
      - Indicates poor abstraction or coupling
    </smell>

    <smell name="feature_envy">
      - Method uses more features of another class than its own
      - Consider moving method to the other class
    </smell>

    <smell name="inappropriate_intimacy">
      - Classes knowing too much about each other's internals
      - Use interfaces and encapsulation
    </smell>
  </code_smells_to_avoid>
</section>

<section priority="SHOULD" id="communication">
  <title>Communication & Collaboration</title>

  <clarification_triggers>
    <scale description="1-5 ambiguity scoring">
      <level value="1" action="proceed_with_reasonable_assumptions">
        - Clear requirement with minor implementation details missing
        - Document assumptions in code comments
      </level>

      <level value="2" action="ask_quick_clarification">
        - Multiple valid interpretations
        - Ask single focused question
      </level>

      <level value="3" action="detailed_clarification_needed">
        - Ambiguous requirements
        - Ask 2-3 specific questions with options
      </level>

      <level value="4" action="requirements_workshop_needed">
        - Unclear goals or success criteria
        - Request detailed discussion with examples
      </level>

      <level value="5" action="block_until_clarified">
        - Contradictory requirements
        - Cannot proceed safely without clarification
      </level>
    </scale>
  </clarification_triggers>

  <status_reporting>
    <frequency>
      - Simple tasks (&lt;30 min): Report on completion
      - Medium tasks (30 min - 2 hours): Report every 30 minutes
      - Complex tasks (&gt;2 hours): Report every hour or at major milestones
    </frequency>

    <blocker_escalation>
      - Immediate: If blocked on external dependency
      - Within 30 min: If stuck on technical problem
      - Include: What was attempted, what failed, what's needed
    </blocker_escalation>
  </status_reporting>

  <knowledge_transfer>
    <inline_documentation>
      - Complex algorithms: Explain approach and complexity
      - Non-obvious decisions: Document why, not just what
      - Tricky edge cases: Explain handling and testing
    </inline_documentation>

    <adrs_required_for>
      - Architecture changes affecting multiple components
      - Technology stack additions
      - Major refactoring decisions
      - Performance optimization approaches
      - Security implementation choices
    </adrs_required_for>
  </knowledge_transfer>
</section>

<section priority="MUST" id="safety_operations">
  <title>Execution Behavior - Safety First</title>

  <operation_classification>
    <safe operations="can_execute_freely">
      - Reading files
      - Running tests
      - Linting/formatting code
      - Local builds
      - Git status/log/diff
    </safe>

    <caution operations="confirm_before_execute">
      - Modifying existing code
      - Creating new files
      - Installing dependencies
      - Running migrations in dev environment
      - Git commits
    </caution>

    <dangerous operations="require_explicit_approval">
      - Database operations in production
      - Deployment to production
      - Deleting files/databases
      - Force pushing to shared branches
      - Running destructive migrations
    </dangerous>

    <forbidden operations="never_execute">
      - Direct production database modifications
      - Bypassing CI/CD to deploy
      - Committing secrets/credentials
      - Disabling security checks
      - Removing error handling without replacement
    </forbidden>
  </operation_classification>

  <rollback_strategies>
    <version_control>
      - Feature branches for all changes
      - Commit frequently with meaningful messages
      - Never force push to main/master
      - Use git revert for production fixes
    </version_control>

    <database_migrations>
      - Always write reversible migrations
      - Test rollback before deploying forward
      - Separate data migrations from schema changes
      - Feature flags for major schema changes
    </database_migrations>

    <feature_flags>
      - Use for risky features
      - Allow gradual rollout
      - Enable instant rollback without deployment
    </feature_flags>
  </rollback_strategies>

  <dry_run_requirements>
    <when_to_use>
      - Before database migrations
      - Before bulk data operations
      - Before destructive git operations
      - Before deployment scripts
    </when_to_use>

    <implementation>
      - Support --dry-run or --simulate flag
      - Log what would be done without doing it
      - Validate in staging before production
    </implementation>
  </dry_run_requirements>
</section>

<section priority="MUST" id="testing">
  <title>Testing Standards</title>

  <test_pyramid>
    <unit_tests percentage="70">
      - Test individual functions/methods in isolation
      - Fast execution (&lt;10ms per test)
      - No external dependencies
      - Mock/stub external services
      - Focus on business logic and edge cases
    </unit_tests>

    <integration_tests percentage="20">
      - Test component interactions
      - May use real databases (test instances)
      - Test API contracts
      - Verify data flow between modules
    </integration_tests>

    <e2e_tests percentage="10">
      - Test critical user journeys
      - Use production-like environment
      - Test full stack integration
      - Focus on happy paths and critical failures
    </e2e_tests>
  </test_pyramid>

  <test_categories>
    <happy_path>
      - Verify expected behavior with valid inputs
      - Cover most common use cases
    </happy_path>

    <edge_cases>
      - Empty inputs
      - Maximum/minimum values
      - Boundary conditions
      - Unusual but valid inputs
    </edge_cases>

    <error_conditions>
      - Invalid inputs
      - Network failures
      - Database errors
      - Authentication/authorization failures
    </error_conditions>

    <performance>
      - Response time benchmarks
      - Memory usage limits
      - Scalability thresholds
      - Load testing for critical paths
    </performance>

    <security>
      - Input validation
      - Authentication/authorization
      - SQL injection prevention
      - XSS prevention
      - CSRF protection
    </security>
  </test_categories>

  <test_data_management>
    <fixtures_vs_factories>
      - Fixtures: For simple, stable test data
      - Factories: For complex objects with variations
      - Prefer factories for maintainability
    </fixtures_vs_factories>

    <privacy>
      - Never use real user data in tests
      - Use generated/anonymized data
      - Document test data sources
    </privacy>

    <determinism>
      - Tests must be deterministic
      - Avoid time-dependent tests
      - Seed random generators
      - Isolate tests from each other
    </determinism>
  </test_data_management>

  <continuous_testing>
    <pre_commit_hooks>
      - Run linting
      - Run unit tests
      - Check for merge conflicts
      - Verify no secrets committed
    </pre_commit_hooks>

    <ci_pipeline>
      - Full test suite on every PR
      - Code coverage reporting
      - Security scanning
      - Performance regression tests
    </ci_pipeline>

    <smoke_tests>
      - Quick validation of critical paths
      - Run after deployment
      - Maximum 5 minutes execution time
    </smoke_tests>
  </continuous_testing>
</section>

<section priority="SHOULD" id="documentation">
  <title>Documentation Requirements</title>

  <documentation_types>
    <api_docs format="openapi_swagger">
      - All public APIs documented
      - Include request/response examples
      - Document error codes and handling
      - Keep in sync with implementation
    </api_docs>

    <architecture format="c4_model">
      - System context diagram
      - Container diagram
      - Component diagrams for complex areas
      - Updated with major changes
    </architecture>

    <user_guides>
      - Installation instructions
      - Configuration guide
      - Common workflows
      - Troubleshooting section
    </user_guides>

    <developer_guides>
      - Getting started
      - Development environment setup
      - Testing guide
      - Deployment process
      - Contribution guidelines
    </developer_guides>

    <runbooks>
      - Incident response procedures
      - Common operations
      - Troubleshooting steps
      - Escalation paths
    </runbooks>
  </documentation_types>

  <documentation_standards>
    <diagrams_as_code>
      - Use Mermaid or PlantUML
      - Store in version control
      - Generate in CI/CD pipeline
      - Keep close to related code
    </diagrams_as_code>

    <version_control>
      - Docs live with code
      - Update docs in same PR as code changes
      - Review docs in code reviews
    </version_control>

    <deprecation>
      - Mark deprecated features clearly
      - Provide migration path
      - Set removal timeline
      - Monitor usage before removal
    </deprecation>
  </documentation_standards>

  <self_documenting_code>
    <naming>
      - Use descriptive, searchable names
      - Avoid abbreviations unless standard
      - Use domain language
      - Boolean variables: is/has/can prefixes
    </naming>

    <structure>
      - Code organization reveals architecture
      - Group related functionality
      - Consistent file/folder naming
    </structure>

    <comments>
      <when_necessary>
        - Complex algorithms
        - Non-obvious optimizations
        - Workarounds for known issues
        - TODO/FIXME with context
      </when_necessary>

      <when_code_smell>
        - Explaining what code does (code should be self-explanatory)
        - Commented-out code (use version control)
        - Outdated comments (update or remove)
      </when_code_smell>
    </comments>
  </self_documenting_code>
</section>

<section priority="MUST" id="version_control">
  <title>Version Control Practices</title>

  <branching_strategy type="github_flow">
    <branches>
      - main: Production-ready code, protected
      - feature/*: New features
      - bugfix/*: Bug fixes
      - hotfix/*: Emergency production fixes
      - release/*: Release preparation (if needed)
    </branches>

    <naming_convention>
      - feature/issue-123-add-user-authentication
      - bugfix/issue-456-fix-memory-leak
      - hotfix/critical-security-patch
    </naming_convention>

    <protection_rules>
      - main: Require PR approval, passing CI, up-to-date
      - No direct commits to main
      - Require signed commits
      - Require linear history (rebase, no merge commits)
    </protection_rules>
  </branching_strategy>

  <commit_standards format="conventional_commits">
    <types>
      - feat: New feature
      - fix: Bug fix
      - docs: Documentation only
      - style: Formatting, no code change
      - refactor: Code restructuring, no behavior change
      - perf: Performance improvement
      - test: Adding/updating tests
      - chore: Build/tooling changes
    </types>

    <format>
      <template>
type(scope): subject

body (optional)

footer (optional)
      </template>

      <example>
feat(auth): add JWT token refresh mechanism

Implement automatic token refresh 5 minutes before expiration.
Includes retry logic for network failures.

Closes #123
      </example>
    </format>

    <requirements>
      - Subject: Imperative mood, no period, &lt;50 chars
      - Body: Wrap at 72 chars, explain what and why
      - Footer: Reference issues, breaking changes
      - Sign commits: git commit -s
    </requirements>
  </commit_standards>

  <code_review>
    <pr_template>
      - What: Summary of changes
      - Why: Motivation and context
      - How: Implementation approach
      - Testing: How it was tested
      - Screenshots: For UI changes
      - Checklist: Tests pass, docs updated, etc.
    </pr_template>

    <review_checklist>
      - Code follows style guide
      - Tests are adequate
      - No security issues
      - Performance is acceptable
      - Documentation is updated
      - No unnecessary complexity
    </review_checklist>

    <approval_requirements>
      - Small changes (&lt;100 lines): 1 approval
      - Medium changes (100-500 lines): 2 approvals
      - Large changes (&gt;500 lines): 2 approvals + architect review
      - Security changes: Security team approval
    </approval_requirements>
  </code_review>
</section>

<section priority="MUST" id="security">
  <title>Security-First Development</title>

  <security_by_design>
    <owasp_top_10>
      - Injection: Use parameterized queries, input validation
      - Broken Authentication: Use established libraries, MFA
      - Sensitive Data Exposure: Encrypt at rest and in transit
      - XML External Entities: Disable XXE in parsers
      - Broken Access Control: Deny by default, verify on every request
      - Security Misconfiguration: Secure defaults, minimal attack surface
      - XSS: Output encoding, Content Security Policy
      - Insecure Deserialization: Validate before deserializing
      - Using Components with Known Vulnerabilities: Monitor dependencies
      - Insufficient Logging &amp; Monitoring: Log security events
    </owasp_top_10>

    <principle_of_least_privilege>
      - Grant minimum permissions necessary
      - Use separate accounts for different roles
      - Rotate credentials regularly
      - Revoke unused permissions
    </principle_of_least_privilege>

    <defense_in_depth>
      - Multiple layers of security
      - Assume each layer can be breached
      - Validate at every boundary
      - Monitor for anomalies
    </defense_in_depth>
  </security_by_design>

  <secure_coding>
    <input_sanitization>
      - Validate all input at boundaries
      - Whitelist over blacklist
      - Use type checking and validation libraries
      - Reject invalid input, don't try to clean
    </input_sanitization>

    <output_encoding>
      - Encode based on context (HTML, URL, JSON, SQL)
      - Use framework-provided encoding functions
      - Never trust user input in output
    </output_encoding>

    <cryptography>
      <dos>
        - Use established libraries (don't roll your own)
        - Use strong algorithms (AES-256, RSA-2048+)
        - Use cryptographically secure random generators
        - Use HTTPS everywhere
      </dos>

      <donts>
        - Never implement own crypto algorithms
        - No MD5 or SHA1 for security purposes
        - No hardcoded keys or secrets
        - No custom authentication schemes
      </donts>
    </cryptography>

    <secrets_management>
      - Never commit secrets to version control
      - Use environment variables or secret managers
      - Rotate secrets regularly
      - Use different secrets per environment
      - Encrypt secrets at rest
    </secrets_management>
  </secure_coding>

  <security_testing>
    <sast>
      - Run static analysis on every commit
      - Block PRs with high/critical findings
      - Tools: Bandit (Python), ESLint security plugins
    </sast>

    <dependency_scanning>
      - Scan dependencies for known vulnerabilities
      - Update vulnerable dependencies promptly
      - Tools: Dependabot, Snyk, npm audit
    </dependency_scanning>

    <security_test_cases>
      - SQL injection attempts
      - XSS payloads
      - Authentication bypass attempts
      - Authorization boundary tests
      - Rate limiting validation
    </security_test_cases>
  </security_testing>

  <incident_response>
    <escalation>
      - Critical: Immediate notification, all hands
      - High: Within 1 hour notification
      - Medium: Within 24 hours
      - Low: Track in backlog
    </escalation>

    <cve_handling>
      - Assess severity and exploitability
      - Patch critical CVEs within 24 hours
      - Patch high CVEs within 1 week
      - Document decision to defer/accept risk
    </cve_handling>
  </incident_response>
</section>

<section priority="SHOULD" id="performance">
  <title>Performance Considerations</title>

  <performance_budget>
    <thresholds>
      - API response time: p95 &lt; 200ms
      - Page load time: p95 &lt; 2s
      - Database query: p95 &lt; 100ms
      - Memory usage: &lt; 80% of available
    </thresholds>

    <monitoring>
      - Track metrics in production
      - Alert on threshold violations
      - Regular performance reviews
    </monitoring>
  </performance_budget>

  <optimization_approach>
    <measure_first>
      - Profile before optimizing
      - Identify actual bottlenecks
      - Quantify improvement opportunities
      - Set measurable goals
    </measure_first>

    <premature_optimization>
      - Avoid until proven necessary
      - Optimize hot paths only
      - Maintain code clarity
      - Document performance-critical sections
    </premature_optimization>

    <algorithm_complexity>
      - Prefer O(1) or O(log n) over O(n) or O(n²)
      - Document complexity in comments
      - Consider scalability implications
    </algorithm_complexity>
  </optimization_approach>

  <caching_strategies>
    <when_to_cache>
      - Expensive computations
      - Frequently accessed data
      - External API responses
      - Rendered content
    </when_to_cache>

    <cache_invalidation>
      - Time-based expiration
      - Event-driven invalidation
      - Manual cache clearing when needed
      - Document cache lifetime decisions
    </cache_invalidation>

    <cdn_utilization>
      - Static assets always via CDN
      - Cache-Control headers properly set
      - Versioned asset URLs for cache busting
    </cdn_utilization>
  </caching_strategies>
</section>

</requirements>

<output_format>
Generate a complete CLAUDE.md file with:

1. Title and version number
2. Table of contents
3. All sections from requirements above
4. Practical examples for key concepts
5. Checklists for common workflows
6. Emergency protocols section
7. Changelog section
8. Customization for specific project needs: {project_context}
</output_format>

<guidelines>
1. Be comprehensive but practical - avoid theoretical fluff
2. Include real examples and anti-patterns
3. Balance strictness with flexibility
4. Prioritize using MUST/SHOULD/MAY/MUST NOT
5. Make it scannable with clear headings and structure
6. Include quick reference sections
7. Keep total length under 10,000 words (aim for clarity, not verbosity)
8. Use markdown formatting for readability
9. Add emoji sparingly for visual navigation
10. Cross-reference related sections
</guidelines>

<project_customization>
{project_context}
{tech_stack}
{team_size}
{compliance_requirements}
</project_customization>
```

**Code example** (Python + Anthropic SDK):
```python
import anthropic
from pathlib import Path

client = anthropic.Anthropic(api_key="...")

def generate_claude_md(
    project_context: str,
    tech_stack: list[str],
    team_size: str,
    compliance: list[str]
) -> str:
    """
    Generate a customized CLAUDE.md file for a project.

    Args:
        project_context: Description of project and goals
        tech_stack: List of technologies used
        team_size: "solo", "small" (2-5), "medium" (6-20), "large" (20+)
        compliance: List of compliance requirements (HIPAA, PCI-DSS, etc.)

    Returns:
        Complete CLAUDE.md content as string

    Example:
        >>> content = generate_claude_md(
        ...     project_context="B2B SaaS platform for customer analytics",
        ...     tech_stack=["Python", "FastAPI", "PostgreSQL", "React"],
        ...     team_size="medium",
        ...     compliance=["SOC2", "GDPR"]
        ... )
        >>> Path("~/.claude/CLAUDE.md").expanduser().write_text(content)
    """

    customization = f"""
Project Context:
{project_context}

Tech Stack:
{', '.join(tech_stack)}

Team Size: {team_size}

Compliance Requirements:
{', '.join(compliance) if compliance else 'None'}
"""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=16000,
        temperature=0,  # Consistent, deterministic output
        messages=[{
            "role": "user",
            "content": f"""
<project_customization>
{customization}
</project_customization>

Generate the CLAUDE.md file.
"""
        }]
    )

    return response.content[0].text


# Example usage
if __name__ == "__main__":
    content = generate_claude_md(
        project_context="""
        Building a real-time analytics platform for B2B SaaS companies.
        System processes 10K+ events per second.
        High reliability requirements (99.9% uptime).
        Team follows agile/scrum methodology.
        """,
        tech_stack=["Python 3.11", "FastAPI", "PostgreSQL", "Redis", "React", "TypeScript"],
        team_size="medium",
        compliance=["SOC2", "GDPR"]
    )

    # Save to standard location
    claude_md_path = Path("~/.claude/CLAUDE.md").expanduser()
    claude_md_path.parent.mkdir(parents=True, exist_ok=True)
    claude_md_path.write_text(content)

    print(f"✅ Generated CLAUDE.md ({len(content)} chars)")
    print(f"   Saved to: {claude_md_path}")

    # Validate key sections present
    required_sections = [
        "Development Philosophy",
        "Bug Fix Protocol",
        "Code Quality",
        "Testing Standards",
        "Security-First",
        "Version Control"
    ]

    missing = [s for s in required_sections if s not in content]
    if missing:
        print(f"⚠️  Warning: Missing sections: {missing}")
    else:
        print("✅ All required sections present")
```

**Performance**:
- Generation time: ~30-60 seconds
- Output length: ~8,000-12,000 words
- Customization quality: 95%+ relevant to project context
- Cost: ~$0.15-0.30 per generation

---

## Production Patterns

### Pattern 1: Team-Specific CLAUDE.md Generator

**Use case**: Generate standardized CLAUDE.md for multiple projects in an organization.

```python
from pathlib import Path
from typing import Dict
import yaml

class OrganizationCLAUDEMDGenerator:
    """
    Generate team-standardized CLAUDE.md files for multiple projects.

    Maintains organization-wide standards while allowing project customization.
    """

    def __init__(self, org_standards_path: Path):
        """
        Initialize with organization standards.

        Args:
            org_standards_path: Path to org_standards.yaml file
        """
        with open(org_standards_path) as f:
            self.org_standards = yaml.safe_load(f)

    def generate_for_project(
        self,
        project_name: str,
        project_config: Dict
    ) -> str:
        """
        Generate CLAUDE.md for specific project.

        Args:
            project_name: Name of the project
            project_config: Project-specific configuration

        Returns:
            Complete CLAUDE.md content
        """

        # Merge org standards with project config
        tech_stack = self.org_standards['standard_tech_stack'] + \
                     project_config.get('additional_tech', [])

        compliance = self.org_standards['compliance_requirements'] + \
                    project_config.get('additional_compliance', [])

        # Generate using merged configuration
        return generate_claude_md(
            project_context=f"""
Organization: {self.org_standards['org_name']}
Project: {project_name}
Description: {project_config['description']}

Organization Standards:
- Code review: {self.org_standards['code_review_policy']}
- Testing: {self.org_standards['testing_policy']}
- Security: {self.org_standards['security_policy']}

Project-Specific:
{project_config.get('notes', '')}
""",
            tech_stack=tech_stack,
            team_size=project_config.get('team_size', 'medium'),
            compliance=compliance
        )

    def generate_all_projects(self, projects_config_path: Path) -> None:
        """Generate CLAUDE.md for all projects in organization."""

        with open(projects_config_path) as f:
            projects = yaml.safe_load(f)

        for project_name, project_config in projects['projects'].items():
            print(f"\n🔨 Generating CLAUDE.md for {project_name}...")

            content = self.generate_for_project(project_name, project_config)

            # Save to project directory
            project_path = Path(project_config['path'])
            claude_md = project_path / ".claude" / "CLAUDE.md"
            claude_md.parent.mkdir(parents=True, exist_ok=True)
            claude_md.write_text(content)

            print(f"   ✅ Saved to {claude_md}")


# Example: org_standards.yaml
"""
org_name: "Acme Corporation Engineering"
standard_tech_stack:
  - Python 3.11+
  - PostgreSQL
  - Docker
  - Kubernetes

compliance_requirements:
  - SOC2
  - GDPR

code_review_policy: "All PRs require 2 approvals"
testing_policy: "Minimum 80% coverage, 95% for critical paths"
security_policy: "SAST required, dependency scanning daily"
"""

# Example: projects.yaml
"""
projects:
  customer-analytics:
    path: "/code/customer-analytics"
    description: "Real-time customer behavior analytics"
    team_size: "large"
    additional_tech:
      - Redis
      - Apache Kafka
    additional_compliance:
      - HIPAA
    notes: |
      High-throughput system processing 50K events/sec.
      99.99% uptime SLA.

  payment-processing:
    path: "/code/payment-processing"
    description: "Payment gateway integration service"
    team_size: "small"
    additional_tech:
      - Stripe API
    additional_compliance:
      - PCI-DSS
    notes: |
      Security-critical system.
      All changes require security team review.
"""

# Usage
if __name__ == "__main__":
    generator = OrganizationCLAUDEMDGenerator(
        org_standards_path=Path("org_standards.yaml")
    )

    generator.generate_all_projects(
        projects_config_path=Path("projects.yaml")
    )

    print("\n✅ Generated CLAUDE.md for all projects")
```

### Pattern 2: Interactive CLAUDE.md Builder

**Use case**: Interactive CLI tool to build CLAUDE.md through Q&A.

```python
import anthropic
from typing import Optional

client = anthropic.Anthropic(api_key="...")

def interactive_claude_md_builder():
    """
    Interactive CLI to build CLAUDE.md through questions.
    """

    print("=" * 70)
    print("CLAUDE.md INTERACTIVE BUILDER")
    print("=" * 70)

    # Gather information
    print("\n📝 Let's build your CLAUDE.md file!\n")

    # Project info
    project_name = input("Project name: ").strip()
    project_desc = input("Project description (1-2 sentences): ").strip()

    # Tech stack
    print("\n🔧 Tech Stack")
    print("Enter technologies (one per line, empty line when done):")
    tech_stack = []
    while True:
        tech = input("  - ").strip()
        if not tech:
            break
        tech_stack.append(tech)

    # Team size
    print("\n👥 Team Size")
    print("1. Solo")
    print("2. Small (2-5)")
    print("3. Medium (6-20)")
    print("4. Large (20+)")
    team_choice = input("Select (1-4): ").strip()
    team_map = {"1": "solo", "2": "small", "3": "medium", "4": "large"}
    team_size = team_map.get(team_choice, "medium")

    # Compliance
    print("\n📋 Compliance Requirements")
    print("Enter requirements (one per line, empty line when done):")
    print("Examples: SOC2, GDPR, HIPAA, PCI-DSS")
    compliance = []
    while True:
        req = input("  - ").strip()
        if not req:
            break
        compliance.append(req)

    # Development approach
    print("\n🎯 Development Approach")
    tdd = input("Enforce TDD (Test-Driven Development)? (y/n): ").lower() == 'y'
    coverage = input("Minimum test coverage % (default 80): ").strip() or "80"

    # Git workflow
    print("\n🌿 Git Workflow")
    print("1. GitHub Flow (simple, continuous deployment)")
    print("2. Git Flow (structured, release-based)")
    print("3. Trunk-Based Development")
    git_flow = input("Select (1-3): ").strip()
    git_map = {
        "1": "GitHub Flow",
        "2": "Git Flow",
        "3": "Trunk-Based Development"
    }
    git_workflow = git_map.get(git_flow, "GitHub Flow")

    # Special requirements
    print("\n⚡ Special Requirements")
    print("Any special requirements or notes (optional)?")
    print("(Press Enter twice when done)")
    notes_lines = []
    while True:
        line = input()
        if line == "" and len(notes_lines) > 0 and notes_lines[-1] == "":
            break
        notes_lines.append(line)
    notes = "\n".join(notes_lines[:-1]) if notes_lines else ""

    # Generate
    print("\n🔨 Generating your CLAUDE.md...")

    project_context = f"""
Project: {project_name}
Description: {project_desc}

Development Approach:
- TDD Enforced: {'Yes' if tdd else 'No'}
- Test Coverage Target: {coverage}%
- Git Workflow: {git_workflow}

{notes}
"""

    content = generate_claude_md(
        project_context=project_context,
        tech_stack=tech_stack,
        team_size=team_size,
        compliance=compliance
    )

    # Preview
    print("\n" + "=" * 70)
    print("GENERATED CLAUDE.md PREVIEW")
    print("=" * 70)
    print(content[:1000] + "...\n")

    # Save
    print(f"\n💾 Save to ~/.claude/CLAUDE.md?")
    save = input("(y/n): ").lower()

    if save == 'y':
        claude_md_path = Path("~/.claude/CLAUDE.md").expanduser()
        claude_md_path.parent.mkdir(parents=True, exist_ok=True)
        claude_md_path.write_text(content)

        print(f"\n✅ Saved to {claude_md_path}")
        print(f"   Size: {len(content)} characters")
    else:
        # Save to current directory
        local_path = Path("CLAUDE.md")
        local_path.write_text(content)
        print(f"\n✅ Saved to {local_path}")

    print("\n🎉 Done! Your CLAUDE.md is ready to use.")


if __name__ == "__main__":
    interactive_claude_md_builder()
```

---

## Usage Examples

### Example 1: Solo Developer Python Project

**Input**:
```python
generate_claude_md(
    project_context="Personal finance tracking app with ML predictions",
    tech_stack=["Python", "FastAPI", "SQLite", "Scikit-learn"],
    team_size="solo",
    compliance=[]
)
```

**Output Highlights**:
- Relaxed code review requirements (self-review acceptable)
- Emphasis on documentation for future self
- Simplified git workflow (main + feature branches)
- Focus on testing ML models
- No compliance overhead

### Example 2: Enterprise Healthcare Application

**Input**:
```python
generate_claude_md(
    project_context="""
    Healthcare patient management system.
    Handles PHI (Protected Health Information).
    99.95% uptime SLA required.
    """,
    tech_stack=["Java", "Spring Boot", "PostgreSQL", "React", "FHIR"],
    team_size="large",
    compliance=["HIPAA", "SOC2", "GDPR"]
)
```

**Output Highlights**:
- Strict security requirements (HIPAA compliance)
- Mandatory security review for all changes
- PHI handling guidelines
- Audit logging requirements
- Encryption at rest and in transit
- Access control standards
- Incident response procedures

### Example 3: Fintech Payment Processing

**Input**:
```python
generate_claude_md(
    project_context="""
    Payment processing microservice.
    Handles financial transactions.
    PCI-DSS compliance required.
    """,
    tech_stack=["Node.js", "TypeScript", "MongoDB", "Stripe API"],
    team_size="medium",
    compliance=["PCI-DSS", "SOC2"]
)
```

**Output Highlights**:
- PCI-DSS specific security requirements
- Tokenization guidelines
- Never log sensitive payment data
- Secure API key management
- Penetration testing requirements
- Fraud detection considerations

---

## Quality Evaluation

### Before (No CLAUDE.md)

**Issues**:
- ❌ Inconsistent code style across sessions
- ❌ Frequent clarification questions
- ❌ Unclear testing expectations
- ❌ Inconsistent git commit messages
- ❌ No security guidelines
- ❌ Variable code quality

**Example Interaction**:
```
User: "Fix the authentication bug"

Claude: "I see there's an authentication issue. Before I proceed:
1. Which authentication method is being used?
2. What's the expected behavior?
3. Are there existing tests I should update?
4. What's your git workflow?
5. Should I commit the changes?"

[5 clarification questions before starting]
```

### After (With CLAUDE.md)

**Improvements**:
- ✅ Consistent code style (follows defined standards)
- ✅ 80% fewer clarification questions
- ✅ Tests written automatically (TDD enforced)
- ✅ Proper commit messages (conventional commits)
- ✅ Security checks automatic
- ✅ Predictable high quality

**Example Interaction**:
```
User: "Fix the authentication bug"

Claude: "I'll fix the authentication bug following our protocol:

1. Pre-Fix Analysis (5 Whys root cause)
2. Write failing test that reproduces bug
3. Implement minimal fix
4. Verify fix with test suite
5. Check for similar patterns in codebase
6. Create PR with conventional commit

Starting with step 1..."

[Follows established protocol automatically]
```

---

## Cost Comparison

| Approach | Setup Time | Clarifications per Task | Code Quality | Consistency |
|----------|------------|------------------------|--------------|-------------|
| **No CLAUDE.md** | 0 min | 3-5 questions | Variable | Low |
| **Basic CLAUDE.md** | 30 min | 1-2 questions | Good | Medium |
| **Generated CLAUDE.md** | 5-10 min | 0-1 questions | Excellent | High |
| **Org-Wide Standards** | 1 hour initial | 0 questions | Excellent | Very High |

**ROI Calculation**:
- Time saved per task: ~10 minutes (fewer clarifications)
- Tasks per week: ~20-50
- Weekly time savings: 200-500 minutes (3-8 hours)
- Monthly time savings: 12-32 hours
- **Payback period**: Less than 1 week

---

## Usage Notes

**When to use this prompt**:
- ✅ Starting new projects
- ✅ Standardizing existing projects
- ✅ Onboarding new team members
- ✅ Establishing organization-wide standards
- ✅ Ensuring compliance requirements are followed
- ✅ Improving code quality consistency

**When to customize manually**:
- ❌ Highly specialized domains (medical devices, aerospace)
- ❌ Unique workflow requirements
- ❌ Legacy systems with unusual constraints
- ❌ Temporary/throwaway projects

**Best practices**:
1. **Start with generated version** - Get 90% there automatically
2. **Customize for your needs** - Add project-specific requirements
3. **Version control** - Track changes to CLAUDE.md
4. **Review quarterly** - Update as practices evolve
5. **Share across team** - Consistency across projects
6. **Collect feedback** - Improve based on usage

---

## Common Issues & Fixes

### Issue 1: Too Prescriptive

**Problem**: Generated CLAUDE.md is too strict for team culture.

**Fix**: Add flexibility markers
```markdown
## Code Review

**Requirement Level**: SHOULD (not MUST)
**Flexibility**: Teams can adjust based on change size and risk

- Small changes: Optional peer review
- Medium changes: 1 approval recommended
- Large changes: 2 approvals required
```

### Issue 2: Missing Domain-Specific Standards

**Problem**: Generic standards don't cover specialized domain.

**Fix**: Add domain section in project_context
```python
generate_claude_md(
    project_context="""
    ... standard context ...

    Domain-Specific Standards:
    - Medical Device: IEC 62304 compliance
    - All algorithms require clinical validation
    - Code changes require regulatory review
    - Maintain complete audit trail
    """,
    ...
)
```

### Issue 3: Team Resistance to Standards

**Problem**: Team finds standards too rigid.

**Fix**: Use tiered approach
```markdown
## Standards Levels

**Level 1 - MUST** (Required for all code):
- Tests pass
- No security vulnerabilities
- Follows language conventions

**Level 2 - SHOULD** (Recommended, enforced in code review):
- 80% test coverage
- Documentation updated
- Performance acceptable

**Level 3 - MAY** (Nice to have):
- 100% type coverage
- Performance optimizations
- Comprehensive edge case tests
```

---

## Version History

| Version | Date | Changes | Adoption Rate |
|---------|------|---------|---------------|
| v1.0 | Initial | Basic standards template | 60% team adoption |
| v1.5 | +1 month | Added security and compliance sections | 75% adoption |
| v2.0 | +2 months | Model-specific optimizations, examples | 85% adoption |
| v2.1 | +3 months | Interactive builder, org-wide standards | 92% adoption |
| v2.2 | Current | Domain-specific customization, tiered standards | 95% adoption |

---

## Related Prompts

- [Code Review & Refactoring](./code-review-refactoring.md) - Implement code review standards
- [Remove AI Writing Patterns](./remove-ai-writing-patterns.md) - Improve documentation
- [Meta-Prompt Designer](../product-strategy/meta-prompt-designer.md) - Design custom prompts

---

**Success Metrics**:

After implementing CLAUDE.md, you should see:
- ✅ 80% reduction in clarification questions
- ✅ 90%+ code quality scores (linting, testing)
- ✅ 100% consistency in commit messages
- ✅ Faster onboarding (new team members productive day 1)
- ✅ Fewer bugs reaching production
- ✅ Better documentation coverage

**Remember**: The best CLAUDE.md is one that's actually followed. Start simple, iterate based on real usage, and involve the team in refinements.


---

## Model Recommendations

- **GPT-4o-mini**: Best value, 94% of GPT-4o accuracy ($0.15/$0.60 per 1M tokens)
- **GPT-4o**: Balanced performance ($2.50/$10.00 per 1M tokens)
- **gpt-4o**: For complex reasoning ($10/$30 per 1M tokens)
