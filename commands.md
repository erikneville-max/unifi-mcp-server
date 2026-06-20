# UniFi MCP Server — Commands

A compact command reference for day-to-day development, testing, and release work in this repository.

## Setup

```bash
# Create / refresh an editable dev environment
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg
```

## Run the server

```bash
# Default local subprocess mode
unifi-mcp-server

# SSE transport
MCP_SERVER_TRANSPORT=sse MCP_SERVER_PORT=3000 unifi-mcp-server

# HTTP transport
MCP_SERVER_TRANSPORT=http MCP_SERVER_PORT=3000 unifi-mcp-server

# Streamable HTTP transport
MCP_SERVER_TRANSPORT=streamable_http MCP_SERVER_PORT=3000 unifi-mcp-server
```

## Tool exposure profiles

Use these when you want fewer tools loaded into context for a session or deployment.

```bash
# Network-focused surface
UNIFI_PROFILE=network unifi-mcp-server

# Protect-focused surface
UNIFI_PROFILE=protect unifi-mcp-server

# Access-focused surface
UNIFI_PROFILE=access unifi-mcp-server

# Talk-focused surface
UNIFI_PROFILE=talk unifi-mcp-server

# Drive-focused surface
UNIFI_PROFILE=drive unifi-mcp-server

# Read-only surface
UNIFI_PROFILE=read-only unifi-mcp-server
```

## Testing

```bash
# Run all unit tests
pytest tests/unit/

# Run with coverage
pytest tests/unit/ --cov=src --cov-report=html --cov-report=term-missing

# Run a specific test file
pytest tests/unit/test_zbf_tools.py -v

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

## Quality checks

```bash
# Lint
ruff check src tests

# Type check
mypy src

# Security scan
bandit -r src/

# Full local quality pass
pytest tests/unit/ --cov=src --cov-fail-under=85 && ruff check src tests && mypy src && bandit -r src/
```

## Docker

```bash
# Build the image
docker build -t unifi-mcp-server:local .

# Run it with local gateway settings
docker run --rm -it \
  -e UNIFI_API_KEY=your-api-key \
  -e UNIFI_API_TYPE=local \
  -e UNIFI_LOCAL_HOST=192.168.2.1 \
  -e MCP_SERVER_TRANSPORT=sse \
  -p 3000:3000 \
  unifi-mcp-server:local
```

## Release

```bash
# Tag a release
git tag -a v0.2.5 -m "Release v0.2.5"

git push origin v0.2.5

# Install the published package
pip install unifi-mcp-server==0.2.5

# Pull the release image
docker pull ghcr.io/enuno/unifi-mcp-server:v0.2.5
```

## Documentation

```bash
# Re-read the development plan
sed -n '1,220p' DEVELOPMENT_PLAN.md

# Inspect API references
sed -n '1,220p' API.md
sed -n '1,220p' UNIFI_API.md

# Check doc formatting before committing
git diff --check -- README.md DEVELOPMENT_PLAN.md ROADMAP.md TODO.md API.md UNIFI_API.md docs/*.md
```

## Git

```bash
# Review local changes
git status --short --branch

git diff

# Commit after verification
git add <files>
git commit -m "docs: update commands reference"

# Push the branch
git push origin main
```

## Notes

- `UNIFI_PROFILE` is intended to reduce context-window bloat by exposing a smaller tool surface per mode.
- `read-only` is safest when you only need lookup tools.
- Keep `commands.md`, `README.md`, and `DEVELOPMENT_PLAN.md` aligned when the developer workflow changes.
