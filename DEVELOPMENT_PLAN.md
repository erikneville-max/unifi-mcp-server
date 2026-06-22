# UniFi MCP Server Development Plan

**Document Version:** 2026-06-20
**API Target:** UniFi Network v10.3.55 + Site Manager v1.0.0 + Protect v6.2.83
**Current Codebase:** ~215 async tool functions across 40+ modules

---

## 1. Executive Summary

This plan maps the path from the current implementation (~215 tools) to full API coverage and enterprise-grade operational maturity. Phases 0–2 are complete. Phase 3 (Protect API) is the next active implementation target.

**Newly incorporated in this revision** are ten scale and enterprise improvements identified through competitive analysis of comparable UniFi MCP server projects (ry-ops, DataKnifeAI, sirkirby). These additions are organized into a new **Phase 5: Enterprise Scale & Operational Excellence** following Phase 4 completion, and individual items are woven into earlier phases where appropriate. The goal is a server that does not merely expose the UniFi API surface, but becomes the definitive platform for managing UniFi environments at scale — multi-site, multi-team, AI-orchestrated, observable, and change-safe.

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
| **Cloud Connector** | Complete | ~10 | Network + Protect proxy tools — `src/tools/connector.py` |
| **Network References** | Complete | ~3 | `get_network_references` — `src/tools/diagnostics.py` |
| **Diagnostics** | Complete | ~8 | Speed test, spectrum scan |

**Total implemented:** ~215 async tool functions.

### 2.2 Known Limitations & Bugs

- **Traffic flow tools `get_flow_trends`, `stream_traffic_flows`, `get_connection_states`** raise `NotImplementedError` — the v2 endpoint has a hard 50-flow rolling cap with no historical or streaming capability. API.md documents the limitation accurately.
- **ZBF Matrix policies:** Read-only / limited due to API endpoint unavailability on real hardware (UDM Pro v10.0.156+). See `docs/archive/ZBF_STATUS.md`.
- **Protect API:** Zero direct coverage (Cloud Connector proxy exists; native client is Phase 3).
- **Multi-controller support:** Single-controller architecture; multi-site orchestration is Phase 5.
- **No dry-run / change-safe mode:** All write tools execute immediately with no preview capability.
- **No audit log:** Write/destructive operations are not persisted to an append-only audit trail.
- **No RBAC on tools:** All API keys have equal access to all tool categories.
- **No Prometheus metrics:** Server performance and tool invocation are not observable via metrics.

---

## 3. Gap Analysis

### 3.1 Critical Gaps (Blocking Full Coverage)

| # | Gap | API Version | Endpoints | Impact |
|---|-----|-------------|-----------|--------|
| G1 | **Protect API** | v6.2.83 | 36+ endpoints (cameras, lights, sensors, chimes, NVR, RTSPS, PTZ, talkback, live views, events) | Largest single gap. Fully documented, zero native code. |
| G2 | **Access API** | v3.x | Doors, credentials, NFC, visitors, access policies | Completely unimplemented; critical for enterprise physical security integration. |
| G3 | **Multi-Controller Orchestration** | N/A | Architecture gap | Single controller assumption blocks ISP and multi-site deployments. |

### 3.2 Documentation Accuracy Debt

All items from the previous revision (D1–D7) are resolved as of Phase 0 completion (2026-05-12).

### 3.3 Minor Gaps

| # | Gap | Notes |
|---|-----|-------|
| G4 | **Dynamic DNS full CRUD** | Completed in `src/tools/wans.py` with local `rest/dynamicdns` list/get/create/update/delete tools. |
| G5 | **Tagged MAC Management** | `/rest/tag` endpoints. Low priority. |
| G6 | **Device Migration** | `/cmd/devmgr/migrate`, `/cmd/devmgr/cancel-migrate`. Low priority. |

### 3.4 Scale & Operational Gaps (New — Competitive Analysis)

These gaps were identified through review of comparable projects and represent features required for production ISP and enterprise deployments that no competing implementation provides.

| # | Gap | Priority | Phase |
|---|-----|----------|-------|
| S1 | **Multi-controller / multi-site orchestration** | Critical | 5 |
| S2 | **Dry-run / change-safe mode** | High | 5 |
| S3 | **Tool-level RBAC via API key scopes** | High | 5 |
| S4 | **Append-only audit log** | High | 5 |
| S5 | **Prometheus metrics endpoint** | High | 5 |
| S6 | **A2A agent card** | Medium | 5 |
| S7 | **AI skills / domain knowledge packs** | Medium | 4 |
| S8 | **NETWORK_PLAYBOOK runbook templates** | Medium | 4 |
| S9 | **Harbor registry + Makefile developer workflow** | Medium | 4 |
| S10 | **Webhook event bus with Redis pub/sub** | Medium | 5 |

---

## 4. Phased Implementation Plan

### Phase 0: Documentation Accuracy & Housekeeping ✅ Complete (2026-05-12)

All deliverables complete. See prior plan revision for details.

---

### Phase 1: Network API Completion ✅ Complete (2026-05-13)

All deliverables complete. See prior plan revision for details.

---

### Phase 2: Site Manager API Completion ✅ Complete (2026-05-13)

All deliverables complete. `src/tools/connector.py` ships 10 proxy tools.

---

### Phase 3: Protect API Integration (Target: 4–6 weeks)

**Goal:** Full Protect v6.2.83 API coverage — the largest single expansion.

This is a new application domain requiring new API client context, models, and tool modules. The Cloud Connector proxy tools from Phase 2 provide a bridge during development; the native client provides full capability and avoids connector latency for local deployments.

#### 3.1 Core Protect Infrastructure

- `src/api/protect_client.py` — Protect-specific HTTP client with NVR base URL discovery
- Authentication reuse (local API key / cloud connector fallback)
- Response normalization for Protect-specific wrappers

#### 3.2 Camera Management (~12 tools)

- `list_cameras`, `get_camera`, `update_camera`, `get_camera_snapshot`
- `create_camera_rtsps_stream`, `delete_camera_rtsps_stream`, `get_camera_rtsps_streams`
- `disable_camera_microphone`, `create_camera_talkback_session`
- `start_camera_ptz_patrol`, `stop_camera_ptz_patrol`, `move_camera_ptz_preset`

#### 3.3 Light, Sensor, Chime Management (~9 tools)

- `list_lights`, `get_light`, `update_light`
- `list_sensors`, `get_sensor`, `update_sensor`
- `list_chimes`, `get_chime`, `update_chime`

#### 3.4 NVR & Device Assets (~3 tools)

- `get_nvr_details`, `upload_device_asset_file`, `get_device_asset_files`

#### 3.5 Live Views & Viewer Config (~7 tools)

- `get_viewer_details`, `update_viewer_settings`, `list_viewers`
- `get_live_view`, `update_live_view`, `list_live_views`, `create_live_view`

#### 3.6 Events & Webhooks (~2 tools)

- `get_protect_events`, `send_alarm_manager_webhook`

#### 3.7 Device Updates (~1 tool)

- `get_device_update_messages`

**Phase 3 Deliverables:**

- [ ] `src/api/protect_client.py`
- [ ] `src/models/protect_*.py` — Camera, Light, Sensor, Chime, NVR, LiveView, Viewer models
- [ ] `src/tools/protect_cameras.py`, `protect_devices.py`, `protect_nvr.py`, `protect_views.py`, `protect_events.py`
- [ ] `src/resources/protect.py` — MCP resources for cameras, events
- [ ] Integration test suite for Protect (mocked NVR responses)
- [ ] `API.md` updated with Protect tool reference
- [ ] `UNIFI_API.md` Protect section annotated with ✅

**Estimated new tools for Phase 3:** 34–36

---

### Phase 4: Testing, Polish, Minor Gaps & Developer Experience (Target: 2–3 weeks)

**Goal:** 80%+ test coverage, close minor gaps, production hardening, and developer/operator experience improvements drawn from competitive analysis.

#### 4.1 Minor Gap Closure

- Dynamic DNS full CRUD (`src/tools/wans.py` extension) - complete
- Tagged MAC management (`src/tools/devices.py` extension or new module)
- Device migration tools
- Access API foundational research (door/credential list tools as preview)

#### 4.2 Test Coverage

- Unit tests for all new Phase 1–3 modules
- Integration tests for Connector, Protect
- Target: 80%+ overall coverage

#### 4.3 NETWORK_PLAYBOOK Runbook Templates (S8)

Inspired by the ry-ops project pattern, add `NETWORK_PLAYBOOK.md` — a structured collection of common operational runbooks written as AI-readable MCP prompt templates. These guide AI agents through multi-step procedures (VLAN provisioning, guest portal setup, firewall rule review, device adoption, WAN failover testing) without requiring the operator to explain each step.

- `NETWORK_PLAYBOOK.md` — runbook library (initial 10–15 scenarios)
- Runbooks registered as MCP Prompts via `@mcp.prompt()` decorators in `src/prompts/`
- Each runbook declares prerequisite tool calls, expected outputs, and error handling paths

#### 4.4 AI Skills / Domain Knowledge Packs (S7)

Inspired by the sirkirby project, add a `skills/` directory containing structured UniFi domain knowledge documents accessible as MCP Resources. AI agents can retrieve these during sessions to reason correctly about UniFi architecture without per-session explanation.

- `skills/unifi-vlan-design.md` — VLAN design patterns, trunking, inter-VLAN routing
- `skills/unifi-qos-and-traffic.md` — QoS profiles, traffic shaping, DPI policy logic
- `skills/unifi-vpn-topologies.md` — Site-to-site VPN design, failover, split tunneling
- `skills/unifi-protect-overview.md` — Camera placement, NVR sizing, RTSPS integration
- `skills/unifi-isp-operations.md` — Multi-site ISP patterns, RADIUS, captive portal, SLA monitoring
- Skills served as `resource://skills/{name}` URIs via `src/resources/skills.py`

#### 4.5 Harbor Registry & Makefile Developer Workflow (S9)

Inspired by the DataKnifeAI project, add a `Makefile` and `HARBOR_SETUP.md` to standardize the developer and deployment workflow:

```makefile
make dev          # Start local dev server with hot reload
make test         # Run full test suite
make lint         # ruff + mypy + bandit
make docker-build # Build production Docker image
make docker-push  # Push to configured registry (Harbor or Docker Hub)
make release      # Bump version, tag, push image
```

- `Makefile` with all standard targets
- `HARBOR_SETUP.md` — guide for private Harbor registry deployment (relevant to air-gapped edge DC environments)
- `docker-compose.yml` with health checks, restart policies, and `env_file` reference
- `.env.harbor.example` — template for Harbor registry credentials

#### 4.6 Documentation Synchronization

- `API.md`: complete tool reference for all new Phase 3–4 tools
- `UNIFI_API.md`: mark every implemented endpoint with ✅
- `README.md`: update feature matrix and tool count
- `CHANGELOG.md`: version entry

#### 4.7 Release Preparation

- Version bump to v0.4.0
- Pre-commit hooks pass (`ruff`, `mypy`, `bandit`)
- Docker build verification
- Security scan clean (`bandit`, `.secrets.baseline`)

**Phase 4 Deliverables:**

- [ ] All new code covered by tests; 80%+ overall coverage
- [ ] `NETWORK_PLAYBOOK.md` with 10+ runbooks; `src/prompts/` registered
- [ ] `skills/` directory with 5 initial domain knowledge packs; `src/resources/skills.py`
- [ ] `Makefile` with full target suite
- [ ] `docker-compose.yml` with health checks
- [ ] `HARBOR_SETUP.md`
- [ ] Documentation fully synchronized
- [ ] CI green; release tag ready

---

### Phase 5: Enterprise Scale & Operational Excellence (Target: v1.0.0, H2 2026)

**Goal:** Elevate the server from a capable API bridge to a purpose-built platform for managing UniFi environments at scale — multi-site ISPs, enterprise campuses, edge data center deployments. All features in this phase are differentiated from every competing implementation.

---

#### 5.1 Multi-Controller / Multi-Site Orchestration (S1)

**This is the single highest-impact scale feature.** No competing UniFi MCP server supports managing multiple controllers from a single server instance. For ISPs and MSPs managing tens or hundreds of sites, this is a hard blocker.

**Architecture:**

```python
# settings.py — controllers config map
UNIFI_CONTROLLERS = {
    "hq":      {"host": "192.168.1.1", "api_key": "...", "site": "default"},
    "site-a":  {"host": "10.0.1.1",   "api_key": "...", "site": "default"},
    "site-b":  {"host": "10.0.2.1",   "api_key": "...", "site": "default"},
}
UNIFI_DEFAULT_CONTROLLER = "hq"
```

**New tools:**

- `list_controllers` — enumerate all configured controllers with connection status
- `switch_controller(name)` — set the active controller for the current session
- `get_active_controller` — return current controller context
- `query_all_controllers(tool_name, **kwargs)` — fan-out a read tool call across all controllers and aggregate results (e.g., find a client MAC across all sites)
- `compare_controllers(controller_a, controller_b, resource)` — diff configuration state between two sites

**Implementation notes:**

- `src/api/client_manager.py` — named client pool, lazy initialization, connection pooling
- `src/context/controller_context.py` — async context var for per-session active controller
- All existing tools route through the active controller context transparently; no per-tool changes required
- `UNIFI_CONTROLLERS` supports both env vars (JSON-encoded map) and a YAML config file at `$UNIFI_CONFIG_FILE`
- Controller credentials stored in environment; never in config files committed to version control

**Deliverables:**

- [ ] `src/api/client_manager.py`
- [ ] `src/context/controller_context.py`
- [ ] `src/tools/orchestration.py` — `list_controllers`, `switch_controller`, `get_active_controller`, `query_all_controllers`, `compare_controllers`
- [ ] `MULTI_CONTROLLER.md` — configuration guide
- [ ] Unit tests for client manager and context routing

---

#### 5.2 Dry-Run / Change-Safe Mode (S2)

**For change-management workflows and safe AI agent operation**, a dry-run mode intercepts all write and destructive tool calls and returns a structured execution plan describing what *would* happen — without executing it. This is critical for environments with formal change management, for testing AI agent reasoning, and for operators reviewing proposed changes before approval.

**Mechanism:**

```bash
DRY_RUN=true  # Enable globally via environment variable
```

When `DRY_RUN=true`, all tools decorated with `@write_tool` or `@destructive_tool`:
1. Validate input parameters normally (Pydantic parsing, existence checks)
2. Build the HTTP request payload
3. Return a `DryRunResult` object instead of executing:

```json
{
  "dry_run": true,
  "tool": "update_firewall_policy",
  "method": "PUT",
  "url": "https://192.168.1.1/api/s/default/rest/firewallpolicy/abc123",
  "payload": { "name": "Block IoT Outbound", "action": "drop" },
  "estimated_impact": "Updates firewall policy 'Block IoT Outbound' on site 'default'",
  "rollback_hint": "Restore previous policy state via get_firewall_policy(id='abc123') before applying"
}
```

**Implementation notes:**

- `src/decorators/dry_run.py` — `@write_tool` and `@destructive_tool` decorators
- Decorator checks `settings.dry_run` and returns `DryRunResult` early
- Read-only tools (`get_*`, `list_*`, `stat_*`) are never intercepted
- `DRY_RUN` can also be passed as a per-request MCP tool parameter for selective preview
- `get_dry_run_status` tool — returns current dry-run mode and list of intercepted tool categories

**Deliverables:**

- [ ] `src/decorators/dry_run.py`
- [ ] `src/models/dry_run.py` — `DryRunResult` Pydantic model
- [ ] Decorator applied to all write/destructive tools across all modules
- [ ] `DRY_RUN` env var documented in `.env.example` and `API.md`
- [ ] Unit tests for dry-run interception on a representative set of write tools

---

#### 5.3 Tool-Level RBAC via API Key Scopes (S3)

**For multi-team ISP and enterprise deployments**, different consumers of the MCP server require different levels of access. A monitoring agent should only call `get_*` and `list_*` tools. A provisioning agent needs write access but not destructive access. A full admin key has unrestricted access.

**Scope model:**

| Scope | Allowed Tools | Use Case |
|-------|--------------|----------|
| `read` | `get_*`, `list_*`, `stat_*`, `search_*` | Monitoring agents, dashboards |
| `write` | `read` + `create_*`, `update_*`, `configure_*` | Provisioning agents, AI assistants |
| `destructive` | `write` + `delete_*`, `block_*`, `migrate_*`, `restore_*` | Privileged operators |
| `admin` | All tools | Full administrative access |

**Configuration:**

```bash
UNIFI_MCP_API_KEYS='[
  {"key": "mon-key-abc", "scope": "read",       "description": "Monitoring agent"},
  {"key": "prov-key-xyz","scope": "write",      "description": "Provisioning agent"},
  {"key": "admin-key",   "scope": "admin",      "description": "Admin operator"}
]'
```

**Implementation notes:**

- `src/auth/rbac.py` — key registry, scope resolution, tool category mapping
- Incoming MCP requests authenticated via `Authorization: Bearer <key>` header or `X-API-Key` header
- Tool categories defined via decorator: `@tool_category("destructive")` in tool modules
- Unauthorized tool calls return a structured `PermissionDeniedError` (not a 401 — the MCP session is valid, the specific tool call is denied)
- `list_permitted_tools` tool — returns the set of tools permitted for the current API key scope

**Deliverables:**

- [ ] `src/auth/rbac.py` — key registry and scope enforcement middleware
- [ ] `@tool_category` decorator applied to all tool modules
- [ ] `UNIFI_MCP_API_KEYS` env var and `.env.example` documentation
- [ ] `list_permitted_tools` tool in `src/tools/meta.py`
- [ ] Unit tests for scope enforcement across all categories

---

#### 5.4 Append-Only Audit Log (S4)

**All write and destructive operations** executed via the MCP server are recorded in an append-only structured audit log. This is required for change management compliance in enterprise and ISP environments, and provides a clear history of AI agent actions for debugging and accountability.

**Log entry schema:**

```json
{
  "timestamp": "2026-06-20T21:14:33.412Z",
  "session_id": "mcp-sess-abc123",
  "api_key_id": "prov-key-xyz",
  "tool": "update_firewall_policy",
  "controller": "hq",
  "site": "default",
  "parameters": { "policy_id": "abc123", "action": "drop" },
  "result": "success",
  "http_status": 200,
  "duration_ms": 42
}
```

**New MCP tools:**

- `get_audit_log(limit, since, tool_filter, result_filter)` — query the audit log with filters
- `export_audit_log(format, since, until)` — export as JSON or CSV

**Implementation notes:**

- `src/audit/logger.py` — async structured logger, appends to `audit.jsonl` (newline-delimited JSON)
- Integrated into the `@write_tool` and `@destructive_tool` decorators from §5.2 — one decorator, two behaviors
- Audit log path configurable via `UNIFI_AUDIT_LOG_PATH` env var
- Log rotation via `RotatingFileHandler` with configurable max size and backup count
- For production deployments: optional syslog forwarding (`UNIFI_AUDIT_SYSLOG=true`, `UNIFI_AUDIT_SYSLOG_HOST`)

**Deliverables:**

- [ ] `src/audit/logger.py`
- [ ] `src/tools/meta.py` — `get_audit_log`, `export_audit_log`
- [ ] Audit logging integrated into all write/destructive tool decorators
- [ ] `UNIFI_AUDIT_LOG_PATH` and syslog vars in `.env.example`
- [ ] Unit tests for log writing and query filtering

---

#### 5.5 Prometheus Metrics Endpoint (S5)

**Expose an HTTP `/metrics` endpoint** in Prometheus text format, enabling integration with existing Prometheus/Grafana monitoring stacks. This makes the MCP server itself a first-class observable service.

**Metrics exposed:**

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `unifi_mcp_tool_calls_total` | Counter | `tool`, `controller`, `result` | Total tool invocations |
| `unifi_mcp_tool_duration_seconds` | Histogram | `tool`, `controller` | Tool execution latency |
| `unifi_mcp_api_errors_total` | Counter | `controller`, `status_code` | UniFi API errors by controller and HTTP status |
| `unifi_mcp_cache_hits_total` | Counter | `cache_key_prefix` | Cache hit count |
| `unifi_mcp_cache_misses_total` | Counter | `cache_key_prefix` | Cache miss count |
| `unifi_mcp_active_sessions` | Gauge | — | Currently active MCP sessions |
| `unifi_mcp_controller_up` | Gauge | `controller` | 1 if controller reachable, 0 if not |

**Implementation notes:**

- `prometheus-client` dependency added to `pyproject.toml`
- Metrics server runs on a separate port (default `9090`, configurable via `UNIFI_METRICS_PORT`)
- Metrics collection integrated into `@write_tool`, `@tool_category`, and `src/cache.py`
- `UNIFI_METRICS_ENABLED=true` env var (default: `false` to avoid dep impact on minimal installs)
- `controller_up` gauge updated by a background health-check task polling each configured controller every 30s

**Deliverables:**

- [ ] `src/metrics/collector.py` — metric definitions and collection helpers
- [ ] `src/metrics/server.py` — async Prometheus HTTP server
- [ ] Metrics integration in decorators and cache layer
- [ ] `UNIFI_METRICS_ENABLED`, `UNIFI_METRICS_PORT` vars in `.env.example`
- [ ] `METRICS.md` — Grafana dashboard JSON export and setup guide
- [ ] Unit tests for metric increment and label correctness

---

#### 5.6 A2A Agent Card (S6)

**Add an `agent-card.json`** conforming to the Google A2A (Agent-to-Agent) protocol specification, enabling this MCP server to be discovered and orchestrated by multi-agent platforms automatically. This is the only UniFi MCP server to implement the A2A manifest pattern.

**File location:** `agent-card.json` at the repository root and served at `/.well-known/agent-card.json`.

**Key fields:**

```json
{
  "name": "unifi-mcp-server",
  "description": "MCP server for managing UniFi Network, Protect, and Site Manager APIs",
  "version": "1.0.0",
  "protocol": "MCP/1.0",
  "capabilities": ["network-management", "protect", "multi-site", "audit-log", "dry-run"],
  "authentication": {
    "schemes": ["bearer", "api-key"],
    "scopes": ["read", "write", "destructive", "admin"]
  },
  "tools_manifest_url": "/mcp/tools",
  "contact": { "url": "https://github.com/enuno/unifi-mcp-server" }
}
```

**Deliverables:**

- [ ] `agent-card.json` — static A2A manifest at repo root
- [ ] `/.well-known/agent-card.json` endpoint served by the MCP server's HTTP layer
- [ ] `A2A.md` — documentation on A2A integration and supported orchestration platforms

---

#### 5.7 Event-Driven Webhook Event Bus (S10)

**Extend the existing `src/webhooks/` module** into a full event bus architecture where UniFi controller webhook pushes (client connect/disconnect, device offline, IDS alerts, Protect motion events) propagate as MCP `notification` messages and optionally trigger registered AI agent callbacks.

**Architecture:**

```
UniFi Controller → POST /webhooks/{site} → Event Normalizer → Event Bus
                                                                    ↓
                                              MCP Notification (server-sent)
                                                                    ↓
                                              Optional: Redis pub/sub (multi-instance)
                                                                    ↓
                                              Registered AI Agent Callbacks
```

**New tools and endpoints:**

- `register_webhook_handler(event_type, callback_url)` — register an external callback for event types
- `list_webhook_handlers` — enumerate registered handlers
- `get_webhook_event_log(limit, since, event_type)` — query recent webhook events
- `POST /webhooks/{site}` — UniFi webhook receiver endpoint (already partially implemented)
- `POST /webhooks/protect/{nvr_id}` — Protect alarm webhook receiver

**Redis pub/sub (optional, for multi-instance deployments):**

- `UNIFI_WEBHOOK_REDIS_URL` env var enables Redis-backed event bus
- Without Redis: events are in-process only (single instance)
- With Redis: events published to `unifi:events:{site}` channels; multiple server instances fan-out

**Deliverables:**

- [ ] `src/webhooks/event_bus.py` — normalized event model, routing, Redis pub/sub integration
- [ ] `src/webhooks/handlers/` — per-event-type normalizers (network, protect, access)
- [ ] `src/tools/webhooks.py` — `register_webhook_handler`, `list_webhook_handlers`, `get_webhook_event_log`
- [ ] `WEBHOOK_SETUP.md` — UniFi controller webhook configuration guide
- [ ] `UNIFI_WEBHOOK_REDIS_URL` in `.env.example`
- [ ] Unit tests for event normalization and routing

---

#### 5.8 Access API Integration

**Full UniFi Access v3.x API coverage** — doors, credentials, NFC cards, visitor management, and access policies. This completes the full UniFi product suite alongside Network, Protect, and Site Manager.

**Estimated tools:** 20–30
**Target modules:** `src/tools/access_doors.py`, `src/tools/access_credentials.py`, `src/tools/access_visitors.py`
**Target models:** `src/models/access_*.py`
**Target resources:** `src/resources/access.py`

**Note:** Access API research and endpoint mapping is required before implementation begins. Add to `docs/UNIFI_API.md` as endpoints are confirmed.

---

#### 5.9 Tool Exposure Modes for Context Reduction

**Reduce LLM context-window bloat by exposing only the tools relevant to the task domain.** The server should support named modes that register a smaller, purpose-built tool surface instead of loading every tool into every session.

**Planned modes:**

- `network` — clients, devices, switching, WiFi, VLANs, traffic, and other core network tools
- `protect` — cameras, NVR, events, talkback, and related Protect tools
- `access` — doors, readers, credentials, visitors, and access-control workflows
- `talk` — UniFi Talk devices, lines, calls, and telephony workflows
- `drive` — UniFi Drive storage, files, sharing, and drive-related workflows
- `read-only` — `get_*`, `list_*`, `stat_*`, and `search_*` tools only; no mutating actions

**Configuration concept:**

- `UNIFI_PROFILE` selects the active mode for a session or deployment
- A null / unset profile continues to expose the full tool set for compatibility
- Profile selection should be safe to use alongside multi-controller routing and future RBAC controls

**Implementation notes:**

- `src/profiles/` — profile registry and mode-to-tool mapping
- `src/tools/meta.py` — helper for enumerating permitted tools by mode
- Tool registration should be filtered before the MCP manifest is emitted so hidden tools never reach the LLM context
- Profiles should be defined declaratively so new UniFi product areas can be added without changing every tool module

**Deliverables:**

- [ ] `src/profiles/` mode registry
- [ ] `UNIFI_PROFILE` documentation in `.env.example`, README, and skill docs
- [ ] `list_permitted_tools` / profile inspection helper
- [ ] Unit tests for all named modes and the read-only profile

---

## 5. Version Roadmap

| Version | Scope | New Tools | Cumulative | Timeline |
|---------|-------|-----------|------------|----------|
| **v0.2.5** | Current (Switching API ✅) | — | ~200 | Shipped |
| **v0.3.0** | Phases 0–2 (docs + net refs + connector) | ~15 | ~215 | Shipped |
| **v0.4.0** | Phase 3 — Protect API | ~35 | ~250 | Q3 2026 |
| **v0.5.0** | Phase 4 — Testing, polish, skills, playbooks, Makefile | ~5 | ~255 | Q3 2026 |
| **v1.0.0** | Phase 5 — Multi-controller, dry-run, RBAC, audit, metrics, A2A, webhook bus | ~15 | ~270 | Q4 2026 |
| **v1.1.0** | Phase 5.8 — Access API | ~25 | ~295 | Q1 2027 |

---

## 6. Endpoint Inventory

### Fully Implemented ✅

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
- `/api/s/{site}/rest/routing` — Traffic routes
- `/api/s/{site}/rest/trafficmatch` — Traffic matching lists
- `/proxy/network/v2/api/site/{site}/traffic-flows` — Traffic flows (v2, local only, 50-flow cap)
- `/api/s/{site}/stat/dpi` — DPI statistics
- `/api/s/{site}/stat/topology` — Topology
- `/api/cmd/backup` / `/api/backup/...` — Backups
- `/api/s/{site}/rest/wanconf` / `rest/dnsfilter` — WAN/DNS
- `/api/s/{site}/rest/vpntunnel` — Site-to-site VPN
- `/integration/v1/sites/{site}/switching/*` — Switch stacks, MC-LAG, LAGs ✅
- `/v1/connector/...` — Cloud Connector proxy (Network + Protect) ✅
- Site Manager v1: aggregated sites, health, inventory, ISP metrics, SD-WAN read, hosts
- `/api/s/{site}/stat/networkref` — Network references

### Partially Implemented ⚠️

| Endpoint | Status | Missing |
|----------|--------|---------|
| `/api/s/{site}/rest/dynamicdns` | GET only | PUT/POST/DELETE |
| `/proxy/network/v2/api/site/{site}/traffic-flows` | Works; `get_flow_trends` etc. raise `NotImplementedError` | Historical/streaming not feasible (50-flow cap) |

### Not Implemented ❌

| Endpoint | Category | Planned Phase |
|----------|----------|---------------|
| Protect v6.2.83 endpoints (36+) | Protect | Phase 3 |
| `/api/s/{site}/rest/tag` | Devices | Phase 4 |
| `/api/s/{site}/cmd/devmgr/migrate` | Devices | Phase 4 |
| Access v3.x endpoints (20+) | Access | Phase 5.8 |

---

## 7. Technical Architecture Notes

### 7.1 New Modules Required

```
src/
  api/
    protect_client.py        # Phase 3
    client_manager.py        # Phase 5 — multi-controller pool
  models/
    protect_camera.py        # Phase 3
    protect_light.py         # Phase 3
    protect_sensor.py        # Phase 3
    protect_chime.py         # Phase 3
    protect_nvr.py           # Phase 3
    protect_liveview.py      # Phase 3
    dry_run.py               # Phase 5
    access_*.py              # Phase 5.8
  tools/
    protect_cameras.py       # Phase 3
    protect_devices.py       # Phase 3
    protect_nvr.py           # Phase 3
    protect_views.py         # Phase 3
    protect_events.py        # Phase 3
    orchestration.py         # Phase 5 — multi-controller tools
    meta.py                  # Phase 5 — audit, dry-run status, permitted tools
    webhooks.py              # Phase 5 — webhook event bus tools
    access_doors.py          # Phase 5.8
    access_credentials.py    # Phase 5.8
    access_visitors.py       # Phase 5.8
  resources/
    protect.py               # Phase 3
    skills.py                # Phase 4
    access.py                # Phase 5.8
  auth/
    rbac.py                  # Phase 5 — key registry, scope enforcement
  audit/
    logger.py                # Phase 5 — append-only audit log
  metrics/
    collector.py             # Phase 5 — Prometheus metric definitions
    server.py                # Phase 5 — Prometheus HTTP server
  decorators/
    dry_run.py               # Phase 5 — @write_tool, @destructive_tool
    tool_category.py         # Phase 5 — @tool_category
  context/
    controller_context.py    # Phase 5 — per-session active controller
  webhooks/
    event_bus.py             # Phase 5 — normalized event routing + Redis pub/sub
    handlers/                # Phase 5 — per-event-type normalizers
  prompts/
    network_playbook.py      # Phase 4 — runbook MCP prompts
skills/
  unifi-vlan-design.md       # Phase 4
  unifi-qos-and-traffic.md   # Phase 4
  unifi-vpn-topologies.md    # Phase 4
  unifi-protect-overview.md  # Phase 4
  unifi-isp-operations.md    # Phase 4
```

### 7.2 Data Model Patterns

All new models follow the existing Pydantic v2 pattern with `populate_by_name=True`, `extra="allow"`, and `alias="_id"` for MongoDB ObjectId fields.

### 7.3 Tool Registration

New tool modules are auto-registered via `register_module_tools()` in `src/main.py`. After creating a new module, add the import and registration call:

```python
from .tools import orchestration as orchestration_tools
register_module_tools(mcp, orchestration_tools, settings)
```

### 7.4 Decorator Stack

As of Phase 5, write and destructive tools carry a composed decorator stack:

```python
@mcp.tool()
@tool_category("destructive")
@write_tool  # → injects: dry_run check + audit logging + metrics
async def delete_network(network_id: str) -> dict:
    ...
```

The `@write_tool` decorator is the integration point for dry-run, audit, and metrics — apply it once, get all three behaviors.

---

## 8. Testing & Quality Targets

| Metric | Current | Phase 4 Target | Phase 5 Target |
|--------|---------|----------------|----------------|
| Unit test coverage | ~84% (core) | 80%+ overall | 85%+ overall |
| Integration tests | 12 suites | +1 (protect) | +3 (orchestration, RBAC, audit) |
| API.md accuracy | ✅ Clean | ✅ Maintained | ✅ Maintained |
| Lint (ruff) | Pass | Pass | Pass |
| Type check (mypy) | Pass | Pass | Pass |
| Security (bandit) | Pass | Pass | Pass |
| Dry-run coverage | N/A | N/A | 100% of write/destructive tools |
| RBAC enforcement coverage | N/A | N/A | 100% of tool categories |

---

## 9. Documentation Maintenance

After each phase:

1. Update `docs/UNIFI_API.md` — add ✅ to implemented endpoints
2. Update `API.md` — add new MCP tools to reference tables
3. Update `README.md` — refresh feature matrix and tool count
4. Update `CHANGELOG.md` — version entry with phase summary

New documents introduced across phases:

| Document | Phase | Purpose |
|----------|-------|---------|
| `NETWORK_PLAYBOOK.md` | 4 | AI-readable operational runbooks |
| `HARBOR_SETUP.md` | 4 | Private registry deployment guide |
| `MULTI_CONTROLLER.md` | 5 | Multi-site configuration guide |
| `METRICS.md` | 5 | Prometheus metrics reference + Grafana dashboard |
| `WEBHOOK_SETUP.md` | 5 | UniFi webhook configuration guide |
| `A2A.md` | 5 | A2A agent card integration guide |
| `agent-card.json` | 5 | A2A protocol machine-readable manifest |

---

## 10. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Protect API endpoints differ from docs | Medium | High | Verify against real NVR early in Phase 3; Cloud Connector proxy as fallback |
| Multi-controller context leaks across sessions | Medium | High | Enforce async context vars; add isolation tests before Phase 5 merge |
| Dry-run decorator applied inconsistently | Medium | Medium | Automated check in CI: scan for write operations not decorated with `@write_tool` |
| Redis unavailable in webhook event bus | Low | Medium | Graceful in-process fallback when `UNIFI_WEBHOOK_REDIS_URL` not set |
| RBAC misconfiguration grants excess access | Low | High | Default-deny posture: unrecognized API keys get `read` scope only |
| Metrics cardinality explosion (per-tool labels) | Low | Medium | Cap tool label cardinality; use tool module prefix if needed |
| A2A spec evolves before v1.0.0 | Medium | Low | Track google/A2A repo; treat agent-card.json as best-effort until spec stabilizes |
| API.md drift recurs post-Phase 5 | Medium | Medium | CI check: `@write_tool` and `@tool_category` decorator presence validated against API.md entries |

---

## 11. Competitive Differentiation Summary

The following table summarizes how Phase 4 and Phase 5 deliverables position this server relative to the three most active competing implementations.

| Feature | enuno (this project) | ry-ops | DataKnifeAI | sirkirby |
|---------|---------------------|--------|-------------|---------|
| Tool count | ~270 (v1.0 target) | ~50 | ~40 | ~80 |
| API domains | Network, Protect, Site Manager, Access | Network | Network | Network, partial Protect |
| Multi-controller | ✅ Phase 5 | ❌ | ❌ | ❌ |
| Dry-run mode | ✅ Phase 5 | ❌ | ❌ | ❌ |
| Tool-level RBAC | ✅ Phase 5 | ❌ | ❌ | ❌ |
| Audit log | ✅ Phase 5 | ❌ | ❌ | ❌ |
| Prometheus metrics | ✅ Phase 5 | ❌ | ❌ | ❌ |
| A2A agent card | ✅ Phase 5 | ✅ | ❌ | ❌ |
| AI skills packs | ✅ Phase 4 | ❌ | ❌ | ✅ |
| Network playbook | ✅ Phase 4 | ✅ | ❌ | ❌ |
| Webhook event bus | ✅ Phase 5 | ❌ | ❌ | ❌ |
| MCP Resources | ✅ Now | ❌ | ❌ | ❌ |
| Harbor + Makefile | ✅ Phase 4 | ❌ | ✅ | ❌ |
| Tool registry | ✅ Now | ❌ | ❌ | ✅ (plugins) |
| Caching layer | ✅ Now | ❌ | Partial | ❌ |
| Secret scanning | ✅ Now | ❌ | ❌ | ❌ |

---

*Plan maintained by: Development Team / AI coding agents*
*Last updated: 2026-06-20*
*Next review: Phase 3 completion (Protect API)*
