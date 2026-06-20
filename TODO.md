# UniFi MCP Server — Active TODO

**Last Updated:** 2026-06-20
**Current Codebase:** ~215 async tool functions across 40+ modules
**Current Posture:** Phase 3 active; Phase 4 and Phase 5 queued

This TODO mirrors `DEVELOPMENT_PLAN.md` and tracks the work that is still open in the repo.

---

## Active work

### Phase 3 — Protect API integration

- [ ] Implement `src/api/protect_client.py`
- [ ] Add Protect models under `src/models/protect_*.py`
- [ ] Add camera tools (`src/tools/protect_cameras.py`)
- [ ] Add Protect device tools (`src/tools/protect_devices.py`)
- [ ] Add NVR / asset tools (`src/tools/protect_nvr.py`)
- [ ] Add live view / viewer tools (`src/tools/protect_views.py`)
- [ ] Add Protect events / webhook tools (`src/tools/protect_events.py`)
- [ ] Add Protect MCP resources (`src/resources/protect.py`)
- [ ] Build mocked integration tests for Protect
- [ ] Update `API.md` and `UNIFI_API.md` with Protect coverage

### Phase 4 — Testing, polish, minor gaps, developer experience

- [ ] Add tests for all new Phase 1–3 modules
- [ ] Close remaining minor gaps: Dynamic DNS full CRUD
- [ ] Close remaining minor gaps: Tagged MAC management
- [ ] Close remaining minor gaps: Device migration tools
- [ ] Add `NETWORK_PLAYBOOK.md` runbook library
- [ ] Add `skills/` domain knowledge packs
- [ ] Add `Makefile`, `docker-compose.yml`, and `HARBOR_SETUP.md`
- [ ] Synchronize README, API.md, UNIFI_API.md, and CHANGELOG.md
- [ ] Prepare release prep notes and version bump

### Phase 5 — Enterprise scale & operational excellence

- [ ] Add multi-controller / multi-site orchestration
- [ ] Add dry-run / change-safe mode
- [ ] Add tool-level RBAC via API key scopes
- [ ] Add append-only audit logging
- [ ] Add Prometheus metrics endpoint
- [ ] Add A2A agent card and manifest
- [ ] Add webhook event bus with Redis pub/sub
- [ ] Add tool exposure modes for network, protect, access, talk, drive, and read-only sessions
- [ ] Research and map the Access API
- [ ] Implement Access API tools once the endpoint map is confirmed

---

## Ongoing maintenance

- [ ] Keep `README.md` aligned with the current codebase
- [ ] Keep `ROADMAP.md` aligned with `DEVELOPMENT_PLAN.md`
- [ ] Keep `docs/RELEASE_PROCESS.md` aligned with the current release flow
- [ ] Keep `docs/SKILLS.md` aligned with current tool counts and profiles
- [ ] Keep `API.md` and `UNIFI_API.md` synchronized with implementation changes
- [ ] Run `git diff --check` on doc-only syncs before merge

---

## Completed phases

- [x] Phase 0 — Documentation accuracy and housekeeping
- [x] Phase 1 — Network API completion
- [x] Phase 2 — Site Manager API completion