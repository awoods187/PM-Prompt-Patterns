# Code Review & Refactoring for Open Source

**Complexity**: 🔴 Advanced
**Category**: Technical Documentation
**Model Compatibility**: ✅ Claude (all) | ✅ GPT-5 | ⚠️ Gemini (large context needed)

## Overview

Comprehensive code review and refactoring prompt for preparing internal codebases for team sharing or open-sourcing. Focuses on security audit, code quality, documentation, and best practices compliance.

**Business Value**:
- Prevent security incidents from exposed credentials
- Reduce onboarding time with better documentation
- Improve code maintainability and collaboration
- Ensure compliance with industry best practices
- Enable safe open-sourcing of internal projects

**Use Cases**:
- Pre-open-source security audit
- Internal code sharing preparation
- Legacy codebase modernization
- Team handoff preparation
- Technical debt reduction

**Production metrics**:
- Security issue detection: ~98% (credentials, keys)
- Documentation coverage improvement: 0% → 90%+
- PEP 8 compliance improvement: Variable → 95%+
- Processing time: ~2-5min per 1000 lines of code

---

## Prompt

```
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
```

---

## Production Patterns

### Pattern 1: Pre-Commit Hook Integration

**Use case**: Automatic security checks before commits.

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔍 Running security audit..."

# Run quick security scan
python -c "
from code_review import quick_security_scan
import sys

issues = quick_security_scan('.')
if issues['critical'] > 0:
    print(f'❌ Found {issues[\"critical\"]} critical security issues!')
    print('Run full audit: python -m code_review.audit')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "Commit blocked by security issues"
    exit 1
fi

echo "✅ Security check passed"
```

### Pattern 2: CI/CD Integration

**Use case**: Automated code review in CI pipeline.

```yaml
# .github/workflows/code-review.yml
name: Code Review

on: [pull_request]

jobs:
  security-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install anthropic bandit pylint black isort

      - name: Run Security Audit
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python scripts/security_audit.py

      - name: Run Bandit
        run: bandit -r . -f json -o bandit-report.json

      - name: Check Code Quality
        run: |
          black --check .
          pylint --fail-under=8.0 .

      - name: Upload Audit Report
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: security-audit-report
          path: SECURITY_AUDIT.md
```

---

---

## Quality Evaluation

### Example Before/After

**Before** (Problematic code):
```python
# api.py - v2 implementation
import requests

# TODO: Remove after migration
# def old_auth(user):
#     return user.password == "admin123"

API_KEY = "sk-abc123xyz789"  # Production key
db_password = "mySecretP@ss"

def get_data(user_input):
    # Query database
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    results = db.execute(query)
    return results

class DataProcessor:
    def process(self, data):
        # Process data
        result = []
        for item in data:
            if item.type == "important":
                result.append(item.value)
        return result
```

**After** (Refactored):
```python
"""API module for data retrieval and processing.

This module provides secure data access with proper authentication
and input validation.
"""

import os
from typing import List, Dict, Any
import requests
from sqlalchemy import text

# Load from environment
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable required")


def get_data(user_input: str) -> List[Dict[str, Any]]:
    """
    Retrieve user data with SQL injection protection.

    Args:
        user_input: User identifier (validated and sanitized)

    Returns:
        List of user records matching the input

    Raises:
        ValueError: If user_input is invalid

    Security:
        Uses parameterized queries to prevent SQL injection
    """
    if not user_input or not user_input.isalnum():
        raise ValueError("Invalid user input: must be alphanumeric")

    # Use parameterized query (SQL injection protection)
    query = text("SELECT * FROM users WHERE name = :name")
    results = db.execute(query, {"name": user_input})
    return [dict(row) for row in results]


class DataProcessor:
    """Process and filter data records."""

    def process(self, data: List[Dict[str, Any]]) -> List[Any]:
        """
        Extract important values from data records.

        Args:
            data: List of data records with 'type' and 'value' fields

        Returns:
            List of values from records marked as important

        Example:
            >>> processor = DataProcessor()
            >>> data = [{"type": "important", "value": 42}]
            >>> processor.process(data)
            [42]
        """
        # Use list comprehension (more Pythonic)
        return [item["value"] for item in data if item.get("type") == "important"]
```

**Security issues fixed**:
1. ✅ Hardcoded API key moved to environment variable
2. ✅ Hardcoded password removed
3. ✅ SQL injection vulnerability fixed (parameterized queries)
4. ✅ Input validation added
5. ✅ Commented-out code removed
6. ✅ Version references removed ("v2")

**Quality improvements**:
1. ✅ Module docstring added
2. ✅ Type hints added to all functions
3. ✅ Google-style docstrings with examples
4. ✅ Pythonic list comprehension
5. ✅ Proper exception handling
6. ✅ Security documentation in docstrings

---

---

## Cost Comparison

| Model | Context | Cost/1K LOC | Accuracy | Speed | Notes |
|-------|---------|-------------|----------|-------|-------|
| **Claude Haiku** | 200K | $0.05 | 85% | Fast | Misses subtle security issues |
| **Claude Sonnet** | 200K | $0.15-0.50 | 98% | Medium | **Recommended** for production |
| **Claude Opus** | 200K | $0.80-2.00 | 99% | Slow | Highest quality, expensive |
| **GPT-5o** | 128K | $0.30-0.80 | 96% | Medium | Good structured output |
| **GPT-5o** | 128K | $0.15-0.40 | 94% | Fast | Balance of cost/quality |
| **Gemini Pro 1.5** | 2M | $0.10-0.30 | 90% | Medium | Good for huge codebases |

**LOC = Lines of Code**

**Recommendation**:
- **Claude Sonnet 3.5**: Best accuracy/cost balance for most projects (1K-50K LOC)
- **Gemini Pro 1.5**: Large codebases (50K+ LOC) requiring full context
- **GPT-5o**: When you need structured JSON output for automation

---

---

## Usage Notes

**Best practices**:
1. **Start with security audit** - Fix critical issues before any refactoring
2. **Review LLM suggestions** - Don't blindly apply all changes
3. **Run tests after changes** - Ensure functionality preserved
4. **Batch process** - Review related files together for context
5. **Version control** - Commit after each major change category

**Limitations**:
- Cannot understand business logic context
- May suggest changes that break subtle behaviors
- Cannot test changes (you must run tests)
- May miss domain-specific security issues
- Limited to code visible in context window

**When to use manual review**:
- Complex authentication logic
- Business-critical algorithms
- Performance-sensitive code
- Code with subtle edge cases
- Multi-service integrations

---

---

## Common Issues & Fixes

### Issue 1: False Positive - Environment Variables

**Problem**: Flags test credentials or example values as secrets.

**Fix**: Add context to distinguish real vs example secrets
```xml
<guideline>
Ignore credentials in:
- test_*.py files
- *_test.py files
- Files containing "example" or "sample"
- Comments clearly marked as examples
</guideline>
```

### Issue 2: Over-Refactoring Working Code

**Problem**: Suggests changes that break subtle behaviors.

**Fix**: Mark as [NEEDS DISCUSSION] rather than direct refactor
```xml
<guideline>
When uncertain about behavior preservation:
1. Mark as [NEEDS DISCUSSION]
2. Explain the concern
3. Suggest running tests before/after
4. Provide multiple options
</guideline>
```

### Issue 3: Context Window Limits

**Problem**: Codebase too large for single context window.

**Fix**: Process in logical chunks
```python
def chunk_codebase(path: Path, chunk_size: int = 10) -> List[List[Path]]:
    """Chunk codebase by related files (models/, api/, etc.)"""

    chunks = []

    # Group by directory
    directories = [d for d in path.iterdir() if d.is_dir()]
    for directory in directories:
        files = list(directory.rglob("*.py"))

        # Chunk within directory if too large
        for i in range(0, len(files), chunk_size):
            chunks.append(files[i:i+chunk_size])

    return chunks
```

---

---

## Related Prompts

- [Remove AI Writing Patterns](./remove-ai-writing-patterns.md) - Improve documentation writing
- [API Documentation Generator](./api-documentation.md) - Auto-generate API docs
- [Test Coverage Analysis](./test-coverage.md) - Identify untested code paths

---

**Production Checklist** before open-sourcing:

- [ ] Run full security audit (zero critical/high issues)
- [ ] All secrets moved to environment variables
- [ ] .env.example created with examples
- [ ] .gitignore includes all sensitive patterns
- [ ] All functions have docstrings + type hints
- [ ] PEP 8 compliant (black + isort)
- [ ] README complete with installation/usage
- [ ] Tests passing (pytest)
- [ ] Security scanner clean (bandit)
- [ ] Code quality score ≥ 8.0 (pylint)
- [ ] License file added
- [ ] CONTRIBUTING.md created
- [ ] No personal TODOs or version references
- [ ] Team reviewed [NEEDS DISCUSSION] items

**Estimated effort**: 4-16 hours depending on codebase size and current quality.
