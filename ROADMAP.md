# UniFi MCP Server — Development Roadmap

## Phase 1: Foundation Hardening (v0.3.0)
**Goal:** Stabilize existing 215 tools, close Network domain gaps, establish test discipline.

### Milestones
1. **P1a — Connector parity** (1 week)
   - Implement 5 connector proxy tools for Network + Protect (POST/GET/PUT/PATCH/DELETE).
   - Add integration tests against mock connector console.
2. **P1b — Network v1 integration API gaps** (2 weeks)
   - Implement 26 missing Network endpoints from mcp-unifi-applications reference.
   - Priority: read-only first (getsiteoverviewpage, getadopteddeviceoverviewpage, getconnectedclientoverviewpage, getnetworksoverviewpage, getwifibroadcastpage, getdnspolicypage, getwansoverviewpage, getvpnserverpage, getdevicetagpage, getdpiapplicationcategories).
   - Then low-risk writes (createwifibroadcast, creatednspolicy, updatewifibroadcast, updatednspolicy, patchfirewallpolicy).
   - Finally destructive (deletewifibroadcast, deletednspolicy, removedevice).
3. **P1c — Test coverage gate** (1 week)
   - Raise unit-test coverage threshold to 85%.
   - Add contract tests for all P1b endpoints using recorded JSON samples.
   - Add schema-validation tests for request/response models.

### Acceptance Criteria
- All P1 endpoints have typed Pydantic models.
- All P1 write endpoints have integration tests.
- CI passes with coverage >= 85%.
- No `unknown` mutability classification remains.

---

## Phase 2: Protect Domain (v0.4.0)
**Goal:** Add UniFi Protect as a first-class domain with 40+ tools.

### Milestones
1. **P2a — Protect read-only observability** (2 weeks)
   - Cameras, lights, sensors, chimes, viewers, liveviews, NVRs.
   - RTSP stream management, snapshots, subscriptions.
2. **P2b — Protect control surfaces** (2 weeks)
   - PTZ patrol/goto, alarm-manager webhooks, mic disable.
   - Liveview CRUD, viewer patching.
3. **P2c — Protect safety gates** (1 week)
   - All mutating actions require explicit `confirm` parameter.
   - Audit logging for every Protect tool execution.

### Acceptance Criteria
- Protect domain has >= 35 tools.
- All camera control actions are behind `confirm=True` gate.
- Integration tests for Protect connector proxy.

---

## Phase 3: Access Domain (v0.5.0)
**Goal:** Add UniFi Access with full user/visitor/credential lifecycle.

### Milestones
1. **P3a — Access users & groups** (2 weeks)
   - CRUD for users, user groups, access policies.
   - NFC cards, PIN codes, license plates, touch passes.
2. **P3b — Access visitors & doors** (2 weeks)
   - Visitor CRUD, QR codes, door groups, doors.
   - Webhook event subscriptions.
3. **P3c — Access safety & audit** (1 week)
   - Credential revocation requires `confirm`.
   - Least-privilege auth checks.

### Acceptance Criteria
- Access domain has >= 50 tools.
- All credential mutations are gated.
- Contract tests against OpenAPI schema.

---

## Phase 4: Continuous Alignment (v0.6.0+)
**Goal:** Automated upstream tracking, schema drift detection, release automation.

### Milestones
1. **P4a — Upstream scraper pipeline** (2 weeks)
   - Re-run scraper weekly against UniFi API docs.
   - Diff against committed spec snapshots.
   - Auto-open issues for new/deprecated endpoints.
2. **P4b — Schema validation layer** (1 week)
   - JSON Schema validation for all responses.
   - Pydantic model generation from OpenAPI specs where available.
3. **P4c — Release automation** (1 week)
   - Auto-generate changelog from commit messages.
   - Version-bump + tag + PyPI publish on merge to main.

### Acceptance Criteria
- Weekly upstream diff runs in CI.
- Schema validation fails CI on drift.
- Release checklist is fully automated.
