# UniFi MCP Server — Development Roadmap

This roadmap is synchronized with `DEVELOPMENT_PLAN.md` and reflects the current repo posture: phases 0–2 are complete, Phase 3 is the active implementation target, and Phases 4–5 define the next expansion steps.

## Current posture

- Phases 0–2: complete
- Phase 3: Protect API integration (active)
- Phase 4: testing, polish, minor gaps, developer experience
- Phase 5: enterprise scale & operational excellence

---

## Phase 3: Protect API Integration (active)

Goal: deliver native Protect coverage on top of the existing Network, Site Manager, and Cloud Connector foundations.

### Deliverables

- `src/api/protect_client.py`
- Protect models under `src/models/protect_*.py`
- Tool modules for cameras, devices, NVR, views, and events
- Protect MCP resources for cameras and events
- Integration tests with mocked NVR responses
- API documentation updates for all new Protect tools

### Scope

- Camera management: list, get, update, snapshot, RTSPS, talkback, PTZ
- Light, sensor, and chime management
- NVR details and device asset files
- Live views and viewer settings
- Protect events and alarm webhooks
- Device update messages

### Exit criteria

- Protect tool coverage is complete for the documented endpoint set
- Tests cover all new tools and response shapes
- API docs and implementation stay in sync

---

## Phase 4: Testing, polish, minor gaps, and developer experience

Goal: harden the server, close the remaining small gaps, and add AI-friendly operational assets.

### Deliverables

- Full test coverage for new Phase 1–3 modules
- Dynamic DNS full CRUD - complete
- Tagged MAC management
- Device migration tools
- `NETWORK_PLAYBOOK.md` runbook library
- `skills/` domain knowledge packs
- `Makefile`, `docker-compose.yml`, and `HARBOR_SETUP.md`
- Release prep updates across README, API.md, UNIFI_API.md, and CHANGELOG.md

### Exit criteria

- Coverage target reached and stable
- Developer workflow is standardized
- Docs reflect the implemented feature set

---

## Phase 5: Enterprise scale & operational excellence

Goal: turn the server into a multi-site, multi-team operating platform with strong safety and observability controls.

### Deliverables

- Multi-controller / multi-site orchestration
- Dry-run / change-safe mode
- Tool-level RBAC via API key scopes
- Append-only audit log
- Prometheus metrics endpoint
- A2A agent card and manifest
- Webhook event bus with Redis pub/sub
- Access API integration
- Tool exposure modes for network, protect, access, talk, drive, and read-only sessions

### Exit criteria

- Multi-controller routing is isolated and testable
- Write operations are previewable, auditable, and scoped
- Server observability is first-class
- The Access domain is mapped and implemented
- Named tool exposure modes keep per-session tool lists small and task-relevant

---

## Version roadmap

| Version | Scope | Notes |
|---------|-------|-------|
| v0.2.5 | Current stable release | Baseline release artifact |
| v0.3.0 | Phases 0–2 completion | Docs sync, Network refs, connector foundation |
| v0.4.0 | Phase 3 | Protect API integration |
| v0.5.0 | Phase 4 | Testing, polish, minor gaps, developer experience |
| v1.0.0 | Phase 5 | Enterprise scale & operational excellence |
| v1.1.0+ | Post-Phase 5 | Access API and follow-on expansion |
