## Description

<!-- Provide a clear, concise description of your changes and the motivation behind them -->

## Type of Change

<!-- Check all that apply -->

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New prompt pattern (new production-tested prompt)
- [ ] 🔧 Code improvement (refactoring, optimization, tooling)
- [ ] 📚 Documentation update (README, guides, examples)
- [ ] ⚡ Performance improvement (cost reduction, speed optimization)
- [ ] 🧪 Test addition/improvement
- [ ] 🔄 Model update (new model version, pricing update)

## Testing Performed

<!-- Describe how you tested your changes -->

### For Code Changes
- [ ] All existing tests pass (`./scripts/run_tests.sh --fast`)
- [ ] Added new tests for new functionality
- [ ] Tested locally with Python [version]
- [ ] No breaking changes to existing APIs

### For Prompt Changes
- [ ] Tested with specified LLM model(s)
- [ ] Validated on test set (size: ___ examples)
- [ ] Documented edge cases and failure modes
- [ ] Compared to baseline or previous version

## Metrics (Required for New Prompts)

<!-- If adding a new prompt, provide quantified results from production or thorough testing -->

**Performance Metrics:**
- **Accuracy/Success Rate:** ___% (tested on ___ examples)
- **Cost per Execution:** $___
- **Average Tokens:** ___ input, ___ output
- **Latency:** ___ ms (p50), ___ ms (p95)

**Model Tested:**
- [ ] Claude Haiku 4.5
- [ ] Claude Sonnet 4.5
- [ ] Claude Opus 4.1
- [ ] GPT-4o
- [ ] GPT-4o mini
- [ ] Gemini 2.5 Pro
- [ ] Gemini 2.5 Flash
- [ ] Other: ___________

**Quality Validation:**
- [ ] Compared against baseline (if applicable)
- [ ] Human evaluation performed (if applicable)
- [ ] Edge cases documented
- [ ] Failure modes identified

## Documentation

<!-- Check all that apply -->

- [ ] Updated relevant README files
- [ ] Added/updated code comments and docstrings
- [ ] Included usage examples
- [ ] Updated CHANGELOG (if applicable)
- [ ] Added references to related prompts/docs

## Breaking Changes

<!-- If this PR introduces breaking changes, describe them and the migration path -->

- [ ] This PR includes breaking changes
- [ ] Migration guide provided (if yes)
- [ ] Deprecation notices added (if applicable)

**Breaking changes description:**
<!-- Describe what breaks and how users should migrate -->

## Checklist

<!-- All items must be checked before merging -->

### Code Quality
- [ ] My code follows the project's style guidelines (Black, Ruff, isort)
- [ ] I have performed a self-review of my changes
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass locally
- [ ] Any dependent changes have been merged and published

### CI/CD Pipeline
- [ ] All CI jobs pass (lint, test, security, build)
- [ ] Code coverage meets or exceeds threshold
- [ ] Pre-commit hooks pass locally (`pre-commit run --all-files`)
- [ ] No security vulnerabilities introduced (Bandit, Safety, pip-audit, Semgrep)
- [ ] Package builds successfully (`python -m build`)
- [ ] Branch is up to date with base branch

## DCO Sign-Off

<!-- All commits MUST include a DCO sign-off -->

- [ ] I have signed off my commits with `git commit -s`
- [ ] All commits in this PR include `Signed-off-by: Your Name <your.email@example.com>`

**If not signed off:** Add `-s` to your commits and force push:
```bash
git commit --amend -s
git push --force
```

## License Agreement

By submitting this pull request, I confirm that:
- [ ] My contribution is made under the MIT License
- [ ] I have the right to submit this contribution
- [ ] I understand this contribution will be publicly available

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details on the DCO and licensing.

## Additional Context

<!-- Add any other context, screenshots, benchmarks, or information that helps reviewers -->

## Related Issues

<!-- Link related issues using keywords: Fixes #123, Closes #456, Related to #789 -->

Fixes #
Related to #

---

**Reviewer Notes:**
<!-- Maintainers: add notes during review -->

