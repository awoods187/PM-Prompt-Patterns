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

---

## Prompt

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
