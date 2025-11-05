# Code Review & Refactoring for Open Source - Claude Optimized

> Extends `prompt.md` with Claude-specific optimizations

## Prompt

<task>
You are a Staff Software Engineer preparing this codebase for internal team
sharing and potential open-sourcing. Conduct a comprehensive code review and
refactoring with these priorities:

## 1. SECURITY AUDIT (FIRST PRIORITY)
- Identify and flag ALL hardcoded credentials, API keys, tokens, or secrets
- Move sensitive configuration to environment variables
- Create .env.example with sanitized examples
- Validate .gitignore excludes all sensitive files
- Review authentication/authorization implementation
- Validate and sanitize external inputs

## 2. CODE QUALITY & DOCUMENTATION
- Add docstrings to all functions/classes (Google Style Guide format)
- Add type hints to all function signatures
- Comment complex logic and non-obvious design decisions
- Flag unclear code with # TODO: [REVIEW]
- Follow PEP 8 naming conventions
- Remove ALL commented-out code

## 3. CODEBASE STRUCTURE
Reorganize following Python best practices:
- Standard project layout (models/, utils/, config/, tests/)
- Proper __init__.py files
- Separation of concerns
- DRY principle throughout

Make code more Pythonic:
- Use comprehensions over verbose loops
- Context managers for resource management
- Proper exception handling patterns

## 4. LEGACY CLEANUP
Remove ALL:
- v1/v2 or deprecated version references
- Migration scripts for old versions
- Personal TODOs and single-developer notes
- "Temporary" fixes and workarounds
- Dead/unreachable code

## 5. DOCUMENTATION
Create/update README.md with:
- Project purpose and description
- Installation steps (detailed)
- Configuration requirements
- Usage examples with expected outputs
- Testing instructions
- System requirements
- Contributing guidelines

## OUTPUT FORMAT
For each modified file, provide:
1. **Security Issues:** [CRITICAL/HIGH/MEDIUM/LOW] + description
2. **Major Changes:** Summary of key modifications
3. **Breaking Changes:** List any breaking changes
4. **Discussion Items:** Tag architectural concerns as [NEEDS DISCUSSION]

## QUALITY CHECKLIST
Before completion, verify:
- [ ] Zero hardcoded secrets
- [ ] All functions documented with type hints
- [ ] Python conventions followed throughout
- [ ] No legacy version references
- [ ] README complete and tested
- [ ] PEP 8 compliant
- [ ] All TODOs resolved or tagged for review

**Priority Order:** Security → Organization → Documentation

**Note:** Flag questionable architectural decisions for team discussion
rather than making assumptions about intent.

---

CODEBASE TO REVIEW:

{paste_code_here}
</task>

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
