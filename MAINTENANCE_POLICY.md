# Maintenance Policy — UniFi MCP Server

## Upstream Tracking
1. **Weekly:** Run `scripts/scraper/scrape-api-docs.js` against latest UniFi API docs.
2. **Weekly:** Compare committed spec snapshots in `docs/specs/` against scraped output.
3. **On drift:** Open a tracking issue labeled `upstream-drift` with diff summary.

## Dependency Updates
1. **Dependabot:** Enabled for Python (`pyproject.toml`) and GitHub Actions.
2. **Security patches:** Applied within 7 days of CVE publication.
3. **Major version bumps:** Evaluated in monthly maintainer sync.

## Issue Triage
| Label | SLA | Action |
|-------|-----|--------|
| `bug` | 48h | Reproduce, add regression test, fix. |
| `upstream-drift` | 1 week | Assess impact, schedule into next phase. |
| `missing-coverage` | 2 weeks | Assign to domain worker agent. |
| `security` | 24h | Hotfix branch, bypass normal cycle if needed. |

## Model / Schema Versioning
- Pydantic models are versioned per UniFi OS release (e.g., `v9.x`).
- Breaking schema changes trigger a minor version bump.
- Deprecated fields kept for 2 minor versions with `DeprecationWarning`.

## Worker Agent Rotation
- Domain worker agents rotate monthly to prevent knowledge staleness.
- Handoff requires updated coverage matrix and gap report.
