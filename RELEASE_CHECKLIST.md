# Release Checklist — UniFi MCP Server

## Pre-Release
- [ ] All CI gates pass (tests, lint, security, coverage).
- [ ] `CHANGELOG.md` updated with user-facing changes.
- [ ] Version bumped in `pyproject.toml` and `package.json`.
- [ ] `mcp-registry.json` version aligned.
- [ ] Roadmap milestone marked complete.

## Coverage Validation
- [ ] Coverage matrix `COVERAGE_MATRIX.csv` regenerated.
- [ ] No `missing` entries for read-only endpoints in target phase.
- [ ] All write endpoints have integration tests.

## Security Review
- [ ] No secrets in diff (`detect-secrets` clean).
- [ ] Bandit score >= Low.
- [ ] Safety check passes (no known CVEs in deps).

## Documentation
- [ ] `README.md` updated with new domains/tools.
- [ ] `API.md` updated (or auto-generated from docstrings).
- [ ] Skill docs added for new agent workflows.

## Post-Release
- [ ] Git tag `vX.Y.Z` pushed.
- [ ] PyPI publish successful.
- [ ] GitHub Release notes published.
- [ ] Announcement drafted (if major/minor).
