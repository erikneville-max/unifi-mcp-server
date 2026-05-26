# Gap Report — UniFi MCP Server

Generated: 2026-05-25

## Executive Summary
- Current tools: 215
- Missing Network endpoints: 31
- Missing Protect endpoints: 40 (entire domain)
- Missing Access endpoints: 66 (entire domain)
- Total gap: 137 endpoints

## Network Gaps (mcp-unifi-applications)
| # | Endpoint | Method | Path | Risk |
|---|----------|--------|------|------|
| 1 | connectorpost | POST | `/v1/connector/consoles/{id}/*path` | write |
| 2 | connectorget | GET | `/v1/connector/consoles/{id}/*path` | read |
| 3 | connectorput | PUT | `/v1/connector/consoles/{id}/*path` | write |
| 4 | connectordelete | DELETE | `/v1/connector/consoles/{id}/*path` | destructive |
| 5 | connectorpatch | PATCH | `/v1/connector/consoles/{id}/*path` | write |
| 6 | getsiteoverviewpage | GET | `/v1/sites` | read |
| 7 | getadopteddeviceoverviewpage | GET | `/v1/sites/{siteId}/devices` | read |
| 8 | executeadopteddeviceaction | POST | `/v1/sites/{siteId}/devices/{deviceId}/actions` | write |
| 9 | getadopteddevicedetails | GET | `/v1/sites/{siteId}/devices/{deviceId}` | read |
| 10 | removedevice | DELETE | `/v1/sites/{siteId}/devices/{deviceId}` | destructive |
| 11 | getadopteddevicelateststatistics | GET | `/v1/sites/{siteId}/devices/{deviceId}/statistics/latest` | read |
| 12 | getpendingdevicepage | GET | `/v1/pending-devices` | read |
| 13 | executeconnectedclientaction | POST | `/v1/sites/{siteId}/clients/{clientId}/actions` | write |
| 14 | getconnectedclientoverviewpage | GET | `/v1/sites/{siteId}/clients` | read |
| 15 | getconnectedclientdetails | GET | `/v1/sites/{siteId}/clients/{clientId}` | read |
| 16 | getnetworksoverviewpage | GET | `/v1/sites/{siteId}/networks` | read |
| 17 | getwifibroadcastdetails | GET | `/v1/sites/{siteId}/wifi/broadcasts/{wifiBroadcastId}` | read |
| 18 | updatewifibroadcast | PUT | `/v1/sites/{siteId}/wifi/broadcasts/{wifiBroadcastId}` | write |
| 19 | deletewifibroadcast | DELETE | `/v1/sites/{siteId}/wifi/broadcasts/{wifiBroadcastId}` | destructive |
| 20 | getwifibroadcastpage | GET | `/v1/sites/{siteId}/wifi/broadcasts` | read |
| 21 | createwifibroadcast | POST | `/v1/sites/{siteId}/wifi/broadcasts` | write |
| 22 | patchfirewallpolicy | PATCH | `/v1/sites/{siteId}/firewall/policies/{firewallPolicyId}` | write |
| 23 | getdnspolicy | GET | `/v1/sites/{siteId}/dns/policies/{dnsPolicyId}` | read |
| 24 | updatednspolicy | PUT | `/v1/sites/{siteId}/dns/policies/{dnsPolicyId}` | write |
| 25 | deletednspolicy | DELETE | `/v1/sites/{siteId}/dns/policies/{dnsPolicyId}` | destructive |
| 26 | getdnspolicypage | GET | `/v1/sites/{siteId}/dns/policies` | read |
| 27 | creatednspolicy | POST | `/v1/sites/{siteId}/dns/policies` | write |
| 28 | getwansoverviewpage | GET | `/v1/sites/{siteId}/wans` | read |
| 29 | getvpnserverpage | GET | `/v1/sites/{siteId}/vpn/servers` | read |
| 30 | getdevicetagpage | GET | `/v1/sites/{siteId}/device-tags` | read |
| 31 | getdpiapplicationcategories | GET | `/v1/dpi/categories` | read |

## Protect Gaps (mcp-unifi-applications)
| # | Endpoint | Method | Path | Risk |
|---|----------|--------|------|------|
| 1 | connectorpost | POST | `/v1/connector/consoles/{id}/*path` | write |
| 2 | connectorget | GET | `/v1/connector/consoles/{id}/*path` | read |
| 3 | connectorput | PUT | `/v1/connector/consoles/{id}/*path` | write |
| 4 | connectordelete | DELETE | `/v1/connector/consoles/{id}/*path` | destructive |
| 5 | connectorpatch | PATCH | `/v1/connector/consoles/{id}/*path` | write |
| 6 | get-v1metainfo | GET | `/v1/meta/info` | read |
| 7 | get-v1viewersid | GET | `/v1/viewers/{id}` | read |
| 8 | patch-v1viewersid | PATCH | `/v1/viewers/{id}` | write |
| 9 | get-v1viewers | GET | `/v1/viewers` | read |
| 10 | get-v1liveviewsid | GET | `/v1/liveviews/{id}` | read |
| 11 | patch-v1liveviewsid | PATCH | `/v1/liveviews/{id}` | write |
| 12 | get-v1liveviews | GET | `/v1/liveviews` | read |
| 13 | post-v1liveviews | POST | `/v1/liveviews` | write |
| 14 | get-v1subscribedevices | GET | `/v1/subscribe/devices` | read |
| 15 | get-v1subscribeevents | GET | `/v1/subscribe/events` | read |
| 16 | post-v1camerasidptzpatrolstartslot | POST | `/v1/cameras/{id}/ptz/patrol/start/{slot}` | write |
| 17 | post-v1camerasidptzpatrolstop | POST | `/v1/cameras/{id}/ptz/patrol/stop` | write |
| 18 | post-v1camerasidptzgotoslot | POST | `/v1/cameras/{id}/ptz/goto/{slot}` | write |
| 19 | post-v1alarm-managerwebhookid | POST | `/v1/alarm-manager/webhook/{id}` | write |
| 20 | get-v1lightsid | GET | `/v1/lights/{id}` | read |
| 21 | patch-v1lightsid | PATCH | `/v1/lights/{id}` | write |
| 22 | get-v1lights | GET | `/v1/lights` | read |
| 23 | get-v1camerasid | GET | `/v1/cameras/{id}` | read |
| 24 | patch-v1camerasid | PATCH | `/v1/cameras/{id}` | write |
| 25 | get-v1cameras | GET | `/v1/cameras` | read |
| 26 | post-v1camerasidrtsps-stream | POST | `/v1/cameras/{id}/rtsps-stream` | write |
| 27 | delete-v1camerasidrtsps-stream | DELETE | `/v1/cameras/{id}/rtsps-stream` | destructive |
| 28 | get-v1camerasidrtsps-stream | GET | `/v1/cameras/{id}/rtsps-stream` | read |
| 29 | get-v1camerasidsnapshot | GET | `/v1/cameras/{id}/snapshot` | read |
| 30 | post-v1camerasiddisable-mic-permanently | POST | `/v1/cameras/{id}/disable-mic-permanently` | write |
| 31 | post-v1camerasidtalkback-session | POST | `/v1/cameras/{id}/talkback-session` | write |
| 32 | get-v1sensorsid | GET | `/v1/sensors/{id}` | read |
| 33 | patch-v1sensorsid | PATCH | `/v1/sensors/{id}` | write |
| 34 | get-v1sensors | GET | `/v1/sensors` | read |
| 35 | get-v1nvrs | GET | `/v1/nvrs` | read |
| 36 | post-v1filesfiletype | POST | `/v1/files/{fileType}` | write |
| 37 | get-v1filesfiletype | GET | `/v1/files/{fileType}` | read |
| 38 | get-v1chimesid | GET | `/v1/chimes/{id}` | read |
| 39 | patch-v1chimesid | PATCH | `/v1/chimes/{id}` | write |
| 40 | get-v1chimes | GET | `/v1/chimes` | read |

## Access Gaps (unifi-access-api-openapi)
| # | Resource | Path |
|---|----------|------|
| 1 | users | `/api/v1/developer/users` |
| 2 | users | `/api/v1/developer/users/{id}` |
| 3 | users | `/api/v1/developer/users/{id}/access_policies` |
| 4 | users | `/api/v1/developer/users/{id}/nfc_cards` |
| 5 | users | `/api/v1/developer/users/{id}/nfc_cards/delete` |
| 6 | users | `/api/v1/developer/users/{id}/pin_codes` |
| 7 | user_groups | `/api/v1/developer/user_groups` |
| 8 | user_groups | `/api/v1/developer/user_groups/{id}` |
| 9 | user_groups | `/api/v1/developer/user_groups/{id}/users` |
| 10 | user_groups | `/api/v1/developer/user_groups/{id}/users/delete` |
| 11 | user_groups | `/api/v1/developer/user_groups/{id}/users/all` |
| 12 | user_groups | `/api/v1/developer/user_groups/{id}/access_policies` |
| 13 | users | `/api/v1/developer/users/search` |
| 14 | users | `/api/v1/developer/users/{user_id}/touch_passes/{touch_pass_id}` |
| 15 | users | `/api/v1/developer/users/touch_passes/assign` |
| 16 | users | `/api/v1/developer/users/{id}/license_plates` |
| 17 | users | `/api/v1/developer/users/{user_id}/license_plates/{license_plate_id}` |
| 18 | users | `/api/v1/developer/users/{id}/avatar` |
| 19 | visitors | `/api/v1/developer/visitors` |
| 20 | visitors | `/api/v1/developer/visitors/{id}` |
| 21 | visitors | `/api/v1/developer/visitors/{id}/nfc_cards` |
| 22 | visitors | `/api/v1/developer/visitors/{id}/nfc_cards/delete` |
| 23 | visitors | `/api/v1/developer/visitors/{id}/pin_codes` |
| 24 | visitors | `/api/v1/developer/visitors/{id}/qr_codes` |
| 25 | visitors | `/api/v1/developer/visitors/{id}/license_plates` |
| 26 | visitors | `/api/v1/developer/visitors/{visitor_id}/license_plates/{license_plate_id}` |
| 27 | access_policies | `/api/v1/developer/access_policies` |
| 28 | access_policies | `/api/v1/developer/access_policies/{id}` |
| 29 | access_policies | `/api/v1/developer/access_policies/holiday_groups` |
| 30 | access_policies | `/api/v1/developer/access_policies/holiday_groups/{id}` |
| 31 | access_policies | `/api/v1/developer/access_policies/schedules` |
| 32 | access_policies | `/api/v1/developer/access_policies/schedules/{id}` |
| 33 | credentials | `/api/v1/developer/credentials/pin_codes` |
| 34 | credentials | `/api/v1/developer/credentials/nfc_cards/sessions` |
| 35 | credentials | `/api/v1/developer/credentials/nfc_cards/sessions/{id}` |
| 36 | credentials | `/api/v1/developer/credentials/nfc_cards/tokens/{token}` |
| 37 | credentials | `/api/v1/developer/credentials/nfc_cards/tokens` |
| 38 | credentials | `/api/v1/developer/credentials/touch_passes` |
| 39 | credentials | `/api/v1/developer/credentials/touch_passes/search` |
| 40 | credentials | `/api/v1/developer/credentials/touch_passes/assignable` |
| 41 | credentials | `/api/v1/developer/credentials/touch_passes/{id}` |
| 42 | credentials | `/api/v1/developer/credentials/qr_codes/download/{visitor_id}` |
| 43 | credentials | `/api/v1/developer/credentials/nfc_cards/import` |
| 44 | door_groups | `/api/v1/developer/door_groups/topology` |
| 45 | door_groups | `/api/v1/developer/door_groups` |
| 46 | door_groups | `/api/v1/developer/door_groups/{id}` |
| 47 | doors | `/api/v1/developer/doors/{id}` |
| 48 | doors | `/api/v1/developer/doors` |
| 49 | doors | `/api/v1/developer/doors/{id}/unlock` |
| 50 | doors | `/api/v1/developer/doors/{id}/lock_rule` |
| 51 | doors | `/api/v1/developer/doors/settings/emergency` |
| 52 | devices | `/api/v1/developer/devices` |
| 53 | devices | `/api/v1/developer/devices/{device_id}/settings` |
| 54 | devices | `/api/v1/developer/devices/{device_id}/doorbell` |
| 55 | system | `/api/v1/developer/system/logs` |
| 56 | system | `/api/v1/developer/system/logs/export` |
| 57 | system | `/api/v1/developer/system/logs/resource/{id}` |
| 58 | system | `/api/v1/developer/system/static/{path}` |
| 59 | users | `/api/v1/developer/users/identity/invitations` |
| 60 | users | `/api/v1/developer/users/identity/assignments` |
| 61 | users | `/api/v1/developer/users/{id}/identity/assignments` |
| 62 | user_groups | `/api/v1/developer/user_groups/{id}/identity/assignments` |
| 63 | devices | `/api/v1/developer/devices/notifications` |
| 64 | webhooks | `/api/v1/developer/webhooks/endpoints` |
| 65 | webhooks | `/api/v1/developer/webhooks/endpoints/{id}` |
| 66 | api_server | `/api/v1/developer/api_server/certificates` |
