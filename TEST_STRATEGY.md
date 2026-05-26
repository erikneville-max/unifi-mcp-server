# Test Strategy — UniFi MCP Server

## 1. Unit Tests
- Every tool function has a unit test in `tests/unit/tools/test_<module>_tools.py`.
- Mock `UniFiClient` responses using `pytest-mock` and `respx`.
- Target: >= 85% line coverage.

## 2. Integration Tests
- `tests/integration/test_<domain>_suite.py` per domain.
- Use real UniFi controller in isolated test site (e.g., `test-mcp`).
- Run in CI only when `UNIFI_TEST_HOST` secret is available.
- Record and replay: use `vcrpy` or `pytest-recording` for deterministic tests.

## 3. Contract / Schema Validation
- For every new endpoint, commit a recorded JSON response sample.
- Validate response structure against Pydantic model using `model_validate_json`.
- For Protect/Access, validate against upstream OpenAPI spec using `openapi-spec-validator`.

## 4. Safety Tests
- All write tools must fail without `confirm=True` (or equivalent gate).
- Audit log assertions: verify every mutation is logged.

## 5. CI Gates
- `pytest --cov=src --cov-fail-under=85`
- `bandit -r src/`
- `safety check`
- `mypy src/`
- `ruff check src/`
