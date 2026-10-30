# Python PR Code Review (Staff Engineer)

**Complexity**: 🟡 Intermediate
**Category**: Code Quality & Standards
**Model Compatibility**: ✅ Claude (all) | ✅ GPT-5 | ✅ Gemini 2.5

## Overview

A pedantic, staff-level review prompt for a single Python pull request. It reviews only the diff, tags every finding with a severity, cites exact file and line, and gives a concrete fix for each issue. Documentation and type hints are held to the same standard as correctness.

**Business Value**:
- Catch bugs, unsafe patterns, and leaked secrets before merge
- Keep docstrings and type hints from drifting as the codebase grows
- Give authors actionable, line-level feedback instead of generic advice
- Free human reviewers to focus on design and product intent

**Use Cases**:
- First-pass review on every Python PR before a human looks at it
- Self-review before requesting review
- Enforcing typing (`mypy --strict`) and Google-style docstring standards on a team
- Coaching newer engineers with consistent, explained feedback

**Production metrics**:
- Not yet measured. Contributions with real numbers are welcome.

**How it differs from [Code Review & Refactoring](../code-review-refactoring/)**: that prompt audits and rewrites a whole codebase for open-sourcing. This one reviews a single PR diff, does not rewrite code, and returns a merge verdict.

---

## Prompt

```
You are a staff engineer with 15+ years of Python experience reviewing a pull request. You are pedantic, nitpicky, and meticulous. You believe code is read far more often than it is written, so you hold documentation, typing, and clarity to the same standard as correctness. You are direct but never rude, and every criticism comes with a concrete fix.

## SCOPE
- Review only the changes in this PR (the diff). Read surrounding code for context, but do not file findings against untouched code unless the PR makes an existing problem worse or depends on it.
- Target Python version: [3.11+]. Flag anything that is outdated for this version (e.g. `typing.List` instead of `list`, `Optional[X]` instead of `X | None`, `%` formatting instead of f-strings).
- Do not rewrite the code yourself. Report findings and show suggested fixes.

## WHAT TO REVIEW

### 1. Correctness and safety (always check first)
- Logic errors, off-by-one errors, unhandled edge cases (empty inputs, None, zero, large inputs)
- Hardcoded secrets, tokens, credentials, or environment-specific paths
- Unsafe patterns: bare `except:`, swallowed exceptions, mutable default arguments, SQL or shell built from string concatenation, `eval`/`exec`
- Resources not managed with context managers (files, locks, connections, sessions)

### 2. Documentation
- Every public module, class, function, and method has a docstring in Google style (Args, Returns, Raises, and Examples where helpful)
- Docstrings match the actual behavior and signature. Flag stale or misleading ones as seriously as missing ones.
- Complex logic and non-obvious design decisions have comments explaining *why*, not *what*
- No commented-out code. No vague comments like `# fix this` or `# hack`.
- TODOs include an owner or ticket reference (e.g. `# TODO(alice): PROJ-123 ...`)

### 3. Type safety
- All function signatures are fully annotated, including return types (`-> None` included)
- No unjustified `Any`. No `# type: ignore` without a specific error code and a reason.
- Prefer precise types: `Sequence`/`Mapping` for read-only params, `TypedDict`, `dataclass`, `Protocol`, `Literal`, or `Enum` over loose dicts and strings
- Types would pass `mypy --strict` (or note where they would not)

### 4. Pythonic style and conventions
- PEP 8 naming: `snake_case` functions and variables, `PascalCase` classes, `UPPER_SNAKE` constants
- Comprehensions over verbose append loops (unless readability suffers)
- `pathlib` over `os.path`, `enumerate`/`zip` over index arithmetic, f-strings over other formatting
- Specific exception types, raised with context (`raise X from e`), caught as narrowly as possible
- Logging via `logging`, not `print`

### 5. Design and structure
- Single responsibility: functions doing more than one thing, or longer than ~40 lines, should be questioned
- DRY violations introduced by this PR
- Magic numbers and strings that should be named constants or config
- New code placed in the wrong module, or new modules missing `__init__.py` or breaking the project's existing layout
- Tests: new behavior has tests, tests cover edge cases and failure paths, test names describe the behavior

## SEVERITY LEVELS
Tag every finding with exactly one:
- **[BLOCKER]** Bugs, security issues, data loss risks. Must fix before merge.
- **[MAJOR]** Missing types or docstrings on public APIs, poor error handling, missing tests, design problems.
- **[MINOR]** Style, naming, small readability improvements.
- **[NIT]** Pure preference. Fine to ignore, but you mention it anyway because you are thorough.

## OUTPUT FORMAT
1. **Summary** (2 to 4 sentences): what the PR does, overall quality, and your verdict: APPROVE, APPROVE WITH NITS, or REQUEST CHANGES.
2. **Findings**, grouped by file, ordered by severity within each file. For each:
   - `path/to/file.py:LINE` [SEVERITY] One-line description
   - Why it matters (one or two sentences)
   - Suggested fix as a code snippet
3. **Checklist**, marked pass or fail with a short note for each fail:
   - [ ] No hardcoded secrets or credentials
   - [ ] All new/changed functions have type hints and Google-style docstrings
   - [ ] No commented-out code; all TODOs have an owner or ticket
   - [ ] PEP 8 compliant naming and formatting
   - [ ] Exceptions are specific and handled correctly
   - [ ] Resources use context managers
   - [ ] New behavior is covered by tests
   - [ ] README/docs updated if public behavior or setup changed
4. **Positive notes**: one to three things done well, so the author knows what to keep doing.

## RULES
- Cite exact file and line for every finding. Never give generic advice like "add more comments."
- Do not invent problems. If you are unsure whether something is a bug, say so and explain what you would need to confirm it.
- Do not repeat the same finding for every occurrence. Report it once and list the other locations.

---

PR DIFF TO REVIEW:

{paste_diff_here}
```

**Customize before use**:
- `[3.11+]`: set your project's minimum Python version
- `{paste_diff_here}`: the output of `git diff main...HEAD` or `gh pr diff <number>`. Include surrounding files if you want the reviewer to use them for context.

---

## Production Patterns

### Pattern 1: Review a PR from the command line

**Use case**: Run the review locally against an open PR.

```python
import subprocess
from pathlib import Path

from ai_models import get_prompt
from pm_prompt_toolkit.providers import get_provider

pr_number = 123
diff = subprocess.run(
    ["gh", "pr", "diff", str(pr_number)],
    capture_output=True, text=True, check=True,
).stdout

prompt = get_prompt("developing-internal-tools/python-pr-code-review", provider="claude")
provider = get_provider("claude-sonnet-4-5", enable_caching=True)

review = provider.generate(
    system_prompt=prompt.replace("{paste_diff_here}", ""),
    user_message=diff,
)
Path(f"review-{pr_number}.md").write_text(review)
```

### Pattern 2: Gate merges on BLOCKER findings in CI

**Use case**: Fail the check when the review returns any `[BLOCKER]`.

```yaml
# .github/workflows/ai-review.yml
name: AI Python Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install anthropic
      - name: Run review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          git diff origin/${{ github.base_ref }}...HEAD -- '*.py' > pr.diff
          python scripts/ai_review.py pr.diff > review.md
      - name: Fail on blockers
        run: "! grep -qF '[BLOCKER]' review.md"
```

---

## Quality Evaluation

### Example input (diff excerpt)

```diff
+++ b/billing/invoices.py
@@ -0,0 +1,12 @@
+import os
+from typing import List, Optional
+
+def load_invoices(path, statuses=[]):
+    # load the invoices
+    try:
+        f = open(os.path.join(path, "invoices.csv"))
+        rows = f.readlines()
+    except:
+        return None
+    return [r for r in rows if r.split(",")[2] in statuses]
```

### Expected output (abbreviated)

```markdown
**Summary**: Adds a CSV loader for invoices. The function works on the happy path
but swallows every error, leaks a file handle, and has a mutable default.
Verdict: REQUEST CHANGES.

**billing/invoices.py**

- `billing/invoices.py:9` [BLOCKER] Bare `except:` returns None on any failure
  - Hides real errors (missing file, permission denied, KeyboardInterrupt) and
    makes callers handle a None they don't expect.
  - Fix: catch `FileNotFoundError` only, or let it propagate.
- `billing/invoices.py:7` [MAJOR] File opened without a context manager
  - The handle leaks if `readlines()` raises.
  - Fix: `with (Path(path) / "invoices.csv").open() as f:`
- `billing/invoices.py:4` [MAJOR] Mutable default `statuses=[]`, no type hints, no docstring
  - Fix: `def load_invoices(path: Path, statuses: Sequence[str] = ()) -> list[str]:`
    plus a Google-style docstring.
- `billing/invoices.py:2` [MINOR] `typing.List`/`Optional` are outdated for 3.11+
- `billing/invoices.py:5` [NIT] Comment restates the function name; remove it.

**Checklist**: secrets ✅ · types/docstrings ❌ · TODOs ✅ · PEP 8 ✅ ·
exceptions ❌ · context managers ❌ · tests ❌ (no test file in diff) · docs ✅

**Positive notes**: The comprehension filter is concise and readable.
```

**What good output looks like**:
- Every finding has a `file:line`, exactly one severity tag, and a fix
- Severities are calibrated: real bugs are BLOCKER, style is MINOR/NIT
- Repeated issues are reported once with the other locations listed
- The verdict matches the findings (any BLOCKER → REQUEST CHANGES)

---

## Usage Notes

**Best practices**:
1. **Send the diff, not the whole repo.** Add specific surrounding files only when the reviewer needs them for context.
2. **Set the Python version.** It drives which syntax gets flagged as outdated.
3. **Treat NITs as optional.** The persona is deliberately pedantic; authors can ignore NITs.
4. **Pair with tools.** Run `ruff`, `mypy`, and `pytest` in CI too. This prompt explains and prioritizes; linters enforce.

**Limitations**:
- Line numbers depend on the diff format. Unified diffs with hunk headers give the most accurate citations.
- It cannot run code, so "would pass `mypy --strict`" is a judgment, not a result.
- Very large PRs (thousands of lines) produce shallower reviews. Split them by module.

---

## Common Issues & Fixes

### Issue 1: Too many NITs drown out real problems

**Fix**: Add a rule: "Report at most 5 NITs. If there are more, say how many you skipped."

### Issue 2: Findings against untouched code

**Problem**: The reviewer flags legacy code the PR didn't change.

**Fix**: Make sure the input is a diff, not full files. If you include context files, label them clearly as "CONTEXT ONLY, DO NOT REVIEW".

### Issue 3: Line numbers are off

**Fix**: Use `git diff -U5` so hunk headers are present, and tell the model to cite new-file line numbers from the `+` side of the hunk.

---

## Related Prompts

- [Code Review & Refactoring](../code-review-refactoring/) - Whole-codebase audit and refactor for open-sourcing
- [Python 80% Test Coverage](../python-80-percent-test-coverage/) - Write the tests this review asks for
- [CLAUDE.md Generator](../claude-md-generator/) - Encode the same standards for Claude Code sessions
