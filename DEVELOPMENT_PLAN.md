# UniFi MCP Server Development Plan

**Document Version:** 2026-05-12
**API Target:** UniFi Network v10.3.55 + Site Manager v1.0.0 + Protect v6.2.83
**Current Codebase:** ~200 async tool functions across 38 modules

---

## 1. Executive Summary

This plan maps the path from the current implementation (~200 tools) to full API code coverage against the documented UniFi API surface. The current server covers the majority of Network API endpoints, a subset of Site Manager endpoints, and zero Protect endpoints.

**Immediate priority** is resolving documentation accuracy debt in API.md (several documented tools either raise `NotImplementedError` or have wrong parameter signatures), completing the remaining minor Network API gaps, adding Cloud Connector support, and implementing the documented Protect API. The plan is organized into four execution phases with clear deliverables and acceptance criteria.

---

## 2. Current State

### 2.1 Implemented (✅)

| API Area | Status | Tool Count | Notes |
|----------|--------|------------|-------|
| **Devices** | Complete | ~10 | CRUD, adoption, port actions, statistics, pending devices |
| **Clients** | Complete | ~8 | List, details, search, block/unblock, reconnect, DPI |
| **Networks** | Complete | ~8 | VLANs, WAN, corporate, VPN networks; full CRUD |
| **WiFi / WLANs** | Complete | ~6 | SSID CRUD, statistics, radio config |
| **Firewall Zones** | Complete | ~7 | Zone CRUD, assignment, `get_zone_networks` |
| **Firewall Policies** | Complete | ~6 | Policy CRUD via v2 API; zone resolved by name/UUID/ObjectId |
| **ACL Rules** | Complete | ~6 | ACL CRUD, ordering |
| **Firewall Groups** | Complete | ~6 | Address/port group CRUD |
| **Traffic Flows** | Complete | ~13 | Real-time flows (50-flow cap), filtering, analytics, blocking, export |
| **DPI** | Complete | ~5 | Statistics, top applications, client DPI |
| **QoS / Traffic Routes** | Complete | ~4 | Traffic route CRUD (`rest/routing`); QoS profile tools removed (endpoints don't exist on hardware) |
| **Traffic Matching Lists** | Complete | ~5 | CRUD operations |
| **Port Forwarding** | Complete | ~5 | CRUD |
| **Port Profiles** | Complete | ~8 | Profile CRUD + device port overrides |
| **Switching** | Complete | ~6 | Switch stacks, MC-LAG domains, LAGs — `src/tools/switching.py` |
| **RADIUS** | Complete | ~10 | Profile CRUD, account CRUD |
| **Guest Portal / Hotspot** | Complete | ~8 | Portal config, packages, vouchers |
| **Backups** | Complete | ~8 | Trigger, list, download, delete, restore, schedule, status |
| **Topology** | Complete | ~5 | Graph data, connections, port mappings, export (json/graphml/dot), statistics |
| **Site VPN** | Complete | ~4 | Site-to-site tunnels, server list |
| **WAN / DNS** | Complete | ~6 | Connections, DNS, content filtering |
| **DHCP Reservations** | Complete | ~5 | CRUD |
| **Site Manager (partial)** | Partial | ~15 | Aggregated sites, health, inventory, ISP metrics, SD-WAN read, hosts, version control |
| **Device Control** | Complete | ~6 | Upgrade, restart, locate, LED |

**Total implemented:** ~200 async tool functions.

### 2.2 Known Limitations & Bugs

- **Traffic flow tools `get_flow_trends`, `stream_traffic_flows`, `get_connection_states`** raise `NotImplementedError` — the v2 endpoint has a hard 50-flow rolling cap with no historical or streaming capability. API.md incorrectly documents these as working. See §3.2.
- **ZBF Matrix policies:** Read-only / limited due to API endpoint unavailability on real hardware (UDM Pro v10.0.156+). See `docs/archive/ZBF_STATUS.md`.
- **Cloud Connector proxy:** Not yet implemented (requires separate auth flow research).
- **Protect API:** Zero coverage (documented but not coded).
- **API.md documentation debt:** Multiple tools documented with wrong parameters or marked as working when they raise `NotImplementedError`. See §3.2.
- **`health_check` version hardcode:** Returns `"version": "0.2.4"` but `pyproject.toml` is at `0.2.5`.

---

## 3. Gap Analysis

Based on `docs/UNIFI_API.md` (v10.3.55), `API.md`, and direct source code review (2026-05-12).

### 3.1 Critical Gaps (Blocking Full Coverage)

| # | Gap | API Version | Endpoints | Impact |
|---|-----|-------------|-----------|--------|
| G1 | **Protect API** | v6.2.83 | 36+ endpoints (cameras, lights, sensors, chimes, NVR, RTSPS, PTZ, talkback, live views, events) | Largest single gap. Fully documented, zero code. |
| G2 | **Cloud Connector** | v1.0.0 | Network + Protect proxy endpoints (POST/GET/PUT/DELETE/PATCH) | Enables remote cloud management without direct local access. |
| G3 | **Network References** | v10.3.55 | `/api/s/{site}/rest/networkref` | Small gap, used for network dependency mapping. |

### 3.2 Documentation Accuracy Debt

These are **code-correct but API.md is wrong** — documentation must be fixed to match implementation.

| # | Tool / Section | API.md Claim | Actual Behavior | Fix Required |
|---|----------------|--------------|-----------------|--------------|
| D1 | `get_flow_trends` | "Get historical flow trends" with `time_range` / `interval` params | Raises `NotImplementedError` — v2 endpoint has no historical capability | Update API.md to document limitation; remove fake parameters |
| D2 | `stream_traffic_flows` | "Stream real-time traffic flow updates" | Raises `NotImplementedError` — 50-flow cap makes streaming impractical | Update API.md to document limitation |
| D3 | `get_connection_states` | "Get connection states" with `time_range` | Raises `NotImplementedError` — v2 returns completed flows, not live states | Update API.md to document limitation |
| D4 | `download_backup` | `output_path`, `verify_checksum` params | Returns raw `bytes`; no output path or checksum logic | Either implement file-save + checksum, or update API.md to match |
| D5 | `restore_backup` | `create_pre_restore_backup` param | Not in implementation; param silently ignored | Either implement pre-restore backup, or remove from API.md |
| D6 | Configuration table | `UNIFI_HOST`, `UNIFI_VERIFY_SSL`, `UNIFI_SITE`, `UNIFI_RATE_LIMIT` | Actual names: `UNIFI_LOCAL_HOST`, `UNIFI_LOCAL_VERIFY_SSL`, `UNIFI_DEFAULT_SITE`, `UNIFI_RATE_LIMIT_REQUESTS` | Fix env var names in API.md |
| D7 | `health_check` | `"version": "0.1.0"` in example | Hardcoded `"0.2.4"` in `src/main.py:189`; `pyproject.toml` is `0.2.5` | Read version dynamically from package metadata |

### 3.3 Minor Gaps

| # | Gap | Notes |
|---|-----|-------|
| ~~G4~~ | ~~Speed Test~~ | ✅ Complete — `run_speed_test`, `get_speed_test_status`, `get_speed_test_history` in `src/tools/diagnostics.py` |
| ~~G5~~ | ~~Spectrum Scan~~ | ✅ Complete — `get_spectrum_scan`, `list_spectrum_interference` in `src/tools/diagnostics.py` |
| G6 | **Dynamic DNS full CRUD** | GET exists; PUT/POST/DELETE for custom providers missing. |
| G7 | **Tagged MAC Management** | `/rest/tag` endpoints. Low priority. |
| G8 | **Device Migration** | `/cmd/devmgr/migrate`, `/cmd/devmgr/cancel-migrate`. Low priority. |

---

## 4. Phased Implementation Plan

### Phase 0: Documentation Accuracy & Housekeeping (Target: 3-5 days)

**Goal:** Eliminate API.md/code mismatches before adding new features. Stale docs cause more confusion than missing features.

#### 0.1 Fix API.md env var names (D6)
- Replace all instances of `UNIFI_HOST` → `UNIFI_LOCAL_HOST`, `UNIFI_VERIFY_SSL` → `UNIFI_LOCAL_VERIFY_SSL`, `UNIFI_SITE` → `UNIFI_DEFAULT_SITE`, `UNIFI_RATE_LIMIT` → `UNIFI_RATE_LIMIT_REQUESTS`

#### 0.2 Update unsupported tool documentation (D1, D2, D3)
- Mark `get_flow_trends`, `stream_traffic_flows`, `get_connection_states` with a clear ⚠️ NOT SUPPORTED section in API.md explaining the v2 endpoint constraint (50-flow rolling window, no history)

#### 0.3 Fix `download_backup` / `restore_backup` discrepancies (D4, D5)
- **Option A (preferred):** Implement `output_path` saving + SHA-256 checksum in `backups.py` and implement pre-restore backup creation in `restore_backup`
- **Option B:** Strip the unimplemented params from API.md

#### 0.4 Fix `health_check` version (D7)
- Read version from `importlib.metadata.version("unifi-mcp-server")` instead of hardcoding

**Phase 0 Deliverables:** ✅ Complete (PR #78, 2026-05-12)
- [x] API.md env var table corrected
- [x] Unsupported flow tool sections updated with accurate limitations
- [x] `download_backup` and `restore_backup` — verified already correctly implemented; API.md was accurate
- [x] `health_check` returns dynamic version from package metadata
- [x] All pre-commit hooks pass

---

### Phase 1: Network API Completion ✅ Complete (2026-05-13)

**Goal:** Close all remaining Network API v10.3.55 gaps.

All Phase 1 tools were already present in `src/tools/diagnostics.py` and registered in `main.py`. Verified by code review on 2026-05-13.

#### 1.1 Network References ✅
- ~~`list_switch_stacks`, `get_switch_stack`~~ ✅ Complete
- ~~`list_mclag_domains`, `get_mclag_domain`~~ ✅ Complete
- ~~`list_lags`, `get_lag_details`~~ ✅ Complete
- `get_network_references` ✅ Complete — `src/tools/diagnostics.py`, 3 tests

#### 1.2 Speed Test & Spectrum ✅
- `run_speed_test`, `get_speed_test_status`, `get_speed_test_history` ✅ — 7 tests
- `get_spectrum_scan`, `list_spectrum_interference` ✅ — 8 tests

**Phase 1 Deliverables:**
- [x] All 6 tools implemented in `src/tools/diagnostics.py`
- [x] Models in `src/models/diagnostics.py` (`NetworkReference`, `SpeedTestResult`, `SpectrumScan`, `SpectrumInterference`)
- [x] 22 unit tests in `tests/unit/test_diagnostics.py`
- [x] Tools registered in `src/main.py` local tool modules

---

### Phase 2: Site Manager API Completion ✅ Complete (2026-05-13)

**Goal:** Complete Site Manager v1.0.0 coverage and add Cloud Connector foundation.

#### 2.1 Connector Proxy — Network ✅
- `connector_network_get`, `connector_network_post`, `connector_network_put`, `connector_network_patch`, `connector_network_delete` — in `src/tools/connector.py`

#### 2.2 Connector Proxy — Protect ✅
- `connector_protect_get`, `connector_protect_post`, `connector_protect_put`, `connector_protect_patch`, `connector_protect_delete` — in `src/tools/connector.py`

**Phase 2 Deliverables:**
- [x] `src/tools/connector.py` — 10 proxy tools (network + protect)
- [x] `src/api/site_manager_client.py` extended with `post()`, `put()`, `patch()`, `delete()`
- [x] No separate models needed — tools are pure pass-throughs returning raw API responses
- [x] 25 unit tests in `tests/unit/tools/test_connector_tools.py`
- [x] Registered in `_CLOUD_TOOL_MODULES` in `src/main.py` (available in all API modes)

---

### Phase 3: Protect API Integration (Target: 4-6 weeks)

**Goal:** Full Protect v6.2.83 API coverage — the largest single expansion.

This is a new application domain requiring:

- New API client context (`src/api/protect_client.py`) or extension of existing client
- New models (`src/models/protect_*.py`)
- New tool modules (`src/tools/protect_*.py`)
- New resources (`src/resources/protect.py`)

#### 3.1 Core Protect Infrastructure

- Protect API client with NVR base URL discovery
- Authentication reuse (local API key / cloud connector)
- Response normalization for Protect-specific wrappers

#### 3.2 Camera Management

- `list_cameras`, `get_camera`, `update_camera`, `get_camera_snapshot`
- `create_camera_rtsps_stream`, `delete_camera_rtsps_stream`, `get_camera_rtsps_streams`
- `disable_camera_microphone`
- `create_camera_talkback_session`
- `start_camera_ptz_patrol`, `stop_camera_ptz_patrol`, `move_camera_ptz_preset`
- Estimated tools: 12

#### 3.3 Light, Sensor, Chime Management

- `list_lights`, `get_light`, `update_light`
- `list_sensors`, `get_sensor`, `update_sensor`
- `list_chimes`, `get_chime`, `update_chime`
- Estimated tools: 9

#### 3.4 NVR & Device Assets

- `get_nvr_details`
- `upload_device_asset_file`, `get_device_asset_files`
- Estimated tools: 3

#### 3.5 Live Views & Viewer Config

- `get_viewer_details`, `update_viewer_settings`, `list_viewers`
- `get_live_view`, `update_live_view`, `list_live_views`, `create_live_view`
- Estimated tools: 7

#### 3.6 Events & Webhooks

- `get_protect_events`
- `send_alarm_manager_webhook`
- Estimated tools: 2

#### 3.7 Device Updates

- `get_device_update_messages`
- Estimated tools: 1

**Phase 3 Deliverables:**

- [ ] `src/api/protect_client.py` — Protect-specific HTTP client
- [ ] `src/models/protect_*.py` — Camera, Light, Sensor, Chime, NVR, LiveView, Viewer models
- [ ] `src/tools/protect_cameras.py` — Camera + PTZ + RTSPS + talkback
- [ ] `src/tools/protect_devices.py` — Lights, sensors, chimes
- [ ] `src/tools/protect_nvr.py` — NVR and asset files
- [ ] `src/tools/protect_views.py` — Live views and viewer config
- [ ] `src/tools/protect_events.py` — Events and alarm webhooks
- [ ] `src/resources/protect.py` — MCP resources for cameras, events
- [ ] Integration test suite for Protect (mocked NVR responses)
- [ ] `API.md` updated with Protect tool reference
- [ ] `UNIFI_API.md` Protect section annotated with ✅

**Estimated new tools for Phase 3:** 34-36

---

### Phase 4: Testing, Polish, and Minor Gaps (Target: 2-3 weeks)

**Goal:** Reach 80%+ test coverage, close minor gaps, and production-harden.

#### 4.1 Minor Gap Closure

- Dynamic DNS full CRUD (`src/tools/wans.py` extension)
- Tagged MAC management (`src/tools/devices.py` extension or new module)
- Device migration tools
- Spectrum scan (if not done in Phase 1)

#### 4.2 Test Coverage

- Unit tests for all new Phase 1-3 modules
- Integration tests for Connector, Protect
- Target: 80%+ overall coverage

#### 4.3 Documentation

- `API.md`: complete tool reference for all new tools
- `UNIFI_API.md`: mark every implemented endpoint with ✅
- `README.md`: update feature matrix and tool count
- `CHANGELOG.md`: version entry

#### 4.4 Release Preparation

- Version bump to v0.3.0 (or appropriate version)
- Pre-commit hooks pass (`ruff`, `mypy`, `bandit`)
- Docker build verification
- Security scan clean

**Phase 4 Deliverables:**

- [ ] All new code covered by tests
- [ ] Documentation fully synchronized with code
- [ ] CI green
- [ ] Release tag ready

---

## 5. Version Roadmap

| Version | Scope | New Tools | Cumulative | Timeline |
|---------|-------|-----------|------------|----------|
| **v0.2.5** | Current (includes Switching API ✅) | ~200 | ~200 | Now |
| **v0.3.0** | Phase 0 (docs) + Phase 1 (net refs) + Phase 2 (connector) + Phase 4 minor | ~10-15 | ~210-215 | Q2 2026 |
| **v0.4.0** | Phase 3 — Protect API | ~35-40 | ~245-255 | Q3 2026 |
| **v1.0.0** | Multi-application platform, enterprise features | TBD | 300+ | H2 2026 |

---

## 6. Endpoint Inventory

### Fully Implemented ✅

All endpoints below have corresponding MCP tools and models.

- `/api/s/{site}/stat/device` — Devices
- `/api/s/{site}/rest/device` — Device management
- `/api/s/{site}/stat/sta` — Clients
- `/api/s/{site}/rest/user` — Client management
- `/api/s/{site}/rest/networkconf` — Networks
- `/api/s/{site}/rest/wlanconf` — WiFi
- `/api/s/{site}/rest/firewallzone` — Firewall zones
- `/api/s/{site}/rest/firewallrule` / `firewallpolicy` — Firewall policies
- `/api/s/{site}/rest/firewallgroup` — Firewall groups
- `/api/s/{site}/rest/radiusprofile` / `account` — RADIUS
- `/api/s/{site}/rest/hotspotpackage` — Hotspot
- `/api/s/{site}/cmd/hotspot` — Vouchers
- `/api/s/{site}/rest/portforward` — Port forwarding
- `/api/s/{site}/rest/portconf` — Port profiles
- `/api/s/{site}/rest/dhcpgroup` / `dhcpd` — DHCP reservations
- `/api/s/{site}/rest/routing` — Traffic routes (QoS routing)
- `/api/s/{site}/rest/trafficmatch` — Traffic matching lists
- `/proxy/network/v2/api/site/{site}/traffic-flows` — Traffic flows (v2, local only)
- `/api/s/{site}/stat/dpi` — DPI statistics
- `/api/s/{site}/stat/topology` — Topology
- `/api/cmd/backup` / `/api/backup/...` — Backups
- `/api/s/{site}/rest/wanconf` / `rest/dnsfilter` — WAN/DNS
- `/api/s/{site}/rest/vpntunnel` — Site-to-site VPN
- `/integration/v1/sites/{site}/switching/switch-stacks` — Switch stacks ✅
- `/integration/v1/sites/{site}/switching/mc-lag-domains` — MC-LAG domains ✅
- `/integration/v1/sites/{site}/switching/lags` — LAGs ✅
- Site Manager v1: aggregated sites, health, inventory, ISP metrics, SD-WAN read, hosts

### Partially Implemented ⚠️

| Endpoint | Status | Missing |
|----------|--------|---------|
| `/api/s/{site}/rest/dynamicdns` | GET only | PUT/POST/DELETE |
| `/proxy/network/v2/api/site/{site}/traffic-flows` | Works but `get_flow_trends`, `stream_traffic_flows`, `get_connection_states` raise `NotImplementedError` | Historical/streaming not feasible with 50-flow cap; API.md needs update (D1-D3) |
| Backup tools | Implemented but `download_backup` lacks `output_path`/checksum; `restore_backup` lacks pre-restore backup | See D4, D5 |

### Not Implemented ❌

| Endpoint | Category | Planned Phase |
|----------|----------|---------------|
| `/api/s/{site}/rest/networkref` | Networks | Phase 1 |
| `/api/s/{site}/cmd/devmgr/speedtest` | Diagnostics | Phase 1 (stretch) |
| `/api/s/{site}/stat/spectrumscan` | RF | Phase 4 |
| `/v1/connector/.../proxy/network/...` | Site Manager | Phase 2 |
| `/v1/connector/.../proxy/protect/...` | Site Manager | Phase 2 |
| Protect v6.2.83 endpoints (36+) | Protect | Phase 3 |
| `/api/s/{site}/rest/tag` | Devices | Phase 4 |
| `/api/s/{site}/cmd/devmgr/migrate` | Devices | Phase 4 |

---

## 7. Technical Architecture Notes

### 7.1 New Modules Required

```
src/
  api/
    protect_client.py      # Phase 3
  models/
    protect_camera.py      # Phase 3
    protect_light.py       # Phase 3
    protect_sensor.py      # Phase 3
    protect_chime.py       # Phase 3
    protect_nvr.py         # Phase 3
    protect_liveview.py    # Phase 3
    connector.py           # Phase 2
  tools/
    connector.py           # Phase 2
    protect_cameras.py     # Phase 3
    protect_devices.py     # Phase 3
    protect_nvr.py         # Phase 3
    protect_views.py       # Phase 3
    protect_events.py      # Phase 3
  resources/
    protect.py             # Phase 3
```

### 7.2 Data Model Patterns

All new models follow the existing Pydantic v2 pattern with `populate_by_name=True`, `extra="allow"`, and `alias="_id"` for MongoDB ObjectId fields.

### 7.3 Tool Registration

New tool modules are auto-registered via `register_module_tools()` in `src/main.py`. After creating a new module, add the import and registration call:

```python
from .tools import connector as connector_tools
# ...
register_module_tools(mcp, connector_tools, settings)
```

---

## 8. Testing & Quality Targets

| Metric | Current | Phase 0 Target | Phase 3 Target |
|--------|---------|----------------|----------------|
| Unit test coverage | ~84% (core) | 84% (no regression) | 80%+ overall |
| Integration tests | 12 suites | +0 | +1 (protect) |
| API.md accuracy | ❌ Several wrong | ✅ Fixed | ✅ Maintained |
| Lint (ruff) | Pass | Pass | Pass |
| Type check (mypy) | Pass | Pass | Pass |
| Security (bandit) | Pass | Pass | Pass |

---

## 9. Documentation Maintenance

After each phase:

1. Update `docs/UNIFI_API.md` — add ✅ to implemented endpoints
2. Update `API.md` — add new MCP tools to reference tables
3. Update `README.md` — refresh feature matrix and tool count
4. Update `CHANGELOG.md` — version entry with phase summary

---

## 10. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Protect API endpoints differ from docs | Medium | High | Verify against real NVR early in Phase 3; maintain fallback wrappers |
| Cloud Connector requires OAuth changes | Low | Medium | Research auth flow before Phase 2; fallback to API-key proxy if possible |
| Test coverage drops below threshold | Low | Medium | Gate PRs on coverage; add tests before merging features |
| API.md drift recurs | Medium | Medium | Add API.md accuracy check to pre-commit or CI |

---

*Plan maintained by: Development Team / AI coding agents*
*Last updated: 2026-05-12*
*Next review: Phase 0 completion*
