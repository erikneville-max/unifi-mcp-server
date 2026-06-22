"""WAN connection management tools."""

from typing import Any

from ..api.client import UniFiClient
from ..config import APIType, Settings
from ..models import WANConnection
from ..utils import APIError, get_logger, log_audit, sanitize_log_message
from ..utils.validators import coerce_bool, validate_confirmation

logger = get_logger(__name__)


def _ensure_local_api(settings: Settings) -> None:
    if settings.api_type != APIType.LOCAL:
        raise NotImplementedError("Dynamic DNS tools require UNIFI_API_TYPE='local'.")


def _unwrap_response(response: Any) -> list[dict[str, Any]]:
    if isinstance(response, list):
        return [item for item in response if isinstance(item, dict)]
    if isinstance(response, dict):
        data = response.get("data")
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
        if isinstance(data, dict):
            return [data]
    return []


def _dynamic_dns_endpoint(site_id: str, dynamic_dns_id: str | None = None) -> str:
    endpoint = f"/ea/sites/{site_id}/rest/dynamicdns"
    if dynamic_dns_id:
        endpoint = f"{endpoint}/{dynamic_dns_id}"
    return endpoint


def _normalize_dynamic_dns(item: dict[str, Any]) -> dict[str, Any]:
    """Normalize a Dynamic DNS API record without returning stored secrets."""
    return {
        "id": item.get("_id") or item.get("id"),
        "_id": item.get("_id") or item.get("id"),
        "host_name": item.get("host_name"),
        "service": item.get("service"),
        "custom_service": item.get("custom_service"),
        "server": item.get("server"),
        "interface": item.get("interface"),
        "login": item.get("login"),
        "options": item.get("options", []),
        "password_configured": bool(item.get("x_password")),
    }


def _dynamic_dns_payload(
    *,
    host_name: str | None = None,
    service: str | None = None,
    interface: str | None = None,
    login: str | None = None,
    password: str | None = None,
    server: str | None = None,
    custom_service: str | None = None,
    options: list[str] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if host_name is not None:
        payload["host_name"] = host_name
    if service is not None:
        payload["service"] = service
    if interface is not None:
        payload["interface"] = interface
    if login is not None:
        payload["login"] = login
    if password is not None:
        payload["x_password"] = password
    if server is not None:
        payload["server"] = server
    if custom_service is not None:
        payload["custom_service"] = custom_service
    if options is not None:
        payload["options"] = list(options)
    return payload


def _redact_dynamic_dns_payload(payload: dict[str, Any]) -> dict[str, Any]:
    redacted = dict(payload)
    if "x_password" in redacted:
        redacted["x_password"] = "***REDACTED***"
    return redacted


async def list_wan_connections(site_id: str, settings: Settings) -> list[dict]:
    """List all WAN connections for a site.

    Args:
        site_id: Site identifier
        settings: Application settings

    Returns:
        List of WAN connections
    """
    async with UniFiClient(settings) as client:
        logger.info(sanitize_log_message(f"Listing WAN connections for site {site_id}"))

        if not client.is_authenticated:
            await client.authenticate()

        response = await client.get(f"/integration/v1/sites/{site_id}/wans")
        data = response if isinstance(response, list) else response.get("data", [])

        return [WANConnection(**wan).model_dump() for wan in data]


async def list_dynamic_dns(site_id: str, settings: Settings) -> list[dict[str, Any]]:
    """List Dynamic DNS configurations for a site.

    Dynamic DNS is exposed by the local UniFi Network legacy REST API under
    ``rest/dynamicdns``. Returned records redact password material and expose
    ``password_configured`` instead.
    """
    _ensure_local_api(settings)

    async with UniFiClient(settings) as client:
        logger.info(sanitize_log_message(f"Listing Dynamic DNS records for site {site_id}"))

        if not client.is_authenticated:
            await client.authenticate()

        try:
            response = await client.get(_dynamic_dns_endpoint(site_id))
        except APIError:
            logger.exception(
                sanitize_log_message(f"Failed to list Dynamic DNS records for site {site_id}")
            )
            raise

        return [_normalize_dynamic_dns(item) for item in _unwrap_response(response)]


async def get_dynamic_dns(
    dynamic_dns_id: str,
    site_id: str,
    settings: Settings,
) -> dict[str, Any]:
    """Get one Dynamic DNS configuration by ID."""
    _ensure_local_api(settings)

    async with UniFiClient(settings) as client:
        logger.info(
            sanitize_log_message(f"Getting Dynamic DNS record {dynamic_dns_id} for site {site_id}")
        )

        if not client.is_authenticated:
            await client.authenticate()

        try:
            response = await client.get(_dynamic_dns_endpoint(site_id, dynamic_dns_id))
        except APIError:
            logger.exception(
                sanitize_log_message(f"Failed to get Dynamic DNS record {dynamic_dns_id}")
            )
            raise

        items = _unwrap_response(response)
        return _normalize_dynamic_dns(items[0] if items else {})


async def create_dynamic_dns(
    site_id: str,
    settings: Settings,
    host_name: str,
    service: str = "custom",
    interface: str = "wan",
    login: str | None = None,
    password: str | None = None,
    server: str = "",
    custom_service: str | None = None,
    options: list[str] | None = None,
    confirm: bool | str = False,
    dry_run: bool | str = False,
) -> dict[str, Any]:
    """Create a Dynamic DNS configuration.

    Args:
        site_id: Site identifier
        settings: Application settings (must be local)
        host_name: Dynamic DNS hostname to update
        service: Provider service name. Use ``"custom"`` with
            ``custom_service``/``server``/``options`` for custom providers.
        interface: WAN interface identifier used by UniFi (commonly ``wan``)
        login: Provider username/login
        password: Provider password or token, sent as ``x_password``
        server: Provider server for custom configurations
        custom_service: Custom provider protocol/service label
        options: Provider-specific options
        confirm: REQUIRED True
        dry_run: Preview without applying
    """
    _ensure_local_api(settings)
    validate_confirmation(confirm, "create_dynamic_dns", dry_run)

    payload = _dynamic_dns_payload(
        host_name=host_name,
        service=service,
        interface=interface,
        login=login,
        password=password,
        server=server,
        custom_service=custom_service,
        options=options,
    )

    if coerce_bool(dry_run):
        return {
            "dry_run": True,
            "would_create": _redact_dynamic_dns_payload(payload),
        }

    async with UniFiClient(settings) as client:
        logger.info(sanitize_log_message(f"Creating Dynamic DNS record for site {site_id}"))

        if not client.is_authenticated:
            await client.authenticate()

        try:
            response = await client.post(_dynamic_dns_endpoint(site_id), json_data=payload)
        except APIError:
            logger.exception(
                sanitize_log_message(f"Failed to create Dynamic DNS record for site {site_id}")
            )
            raise

        log_audit(
            operation="create_dynamic_dns",
            parameters={"site_id": site_id, **_redact_dynamic_dns_payload(payload)},
            result="success",
            site_id=site_id,
        )

        items = _unwrap_response(response)
        return _normalize_dynamic_dns(items[0] if items else {})


async def update_dynamic_dns(
    dynamic_dns_id: str,
    site_id: str,
    settings: Settings,
    host_name: str | None = None,
    service: str | None = None,
    interface: str | None = None,
    login: str | None = None,
    password: str | None = None,
    server: str | None = None,
    custom_service: str | None = None,
    options: list[str] | None = None,
    confirm: bool | str = False,
    dry_run: bool | str = False,
) -> dict[str, Any]:
    """Update a Dynamic DNS configuration."""
    _ensure_local_api(settings)
    validate_confirmation(confirm, "update_dynamic_dns", dry_run)

    payload = _dynamic_dns_payload(
        host_name=host_name,
        service=service,
        interface=interface,
        login=login,
        password=password,
        server=server,
        custom_service=custom_service,
        options=options,
    )

    if coerce_bool(dry_run):
        return {
            "dry_run": True,
            "dynamic_dns_id": dynamic_dns_id,
            "would_update": _redact_dynamic_dns_payload(payload),
        }

    async with UniFiClient(settings) as client:
        logger.info(
            sanitize_log_message(f"Updating Dynamic DNS record {dynamic_dns_id} for site {site_id}")
        )

        if not client.is_authenticated:
            await client.authenticate()

        try:
            response = await client.put(
                _dynamic_dns_endpoint(site_id, dynamic_dns_id),
                json_data=payload,
            )
        except APIError:
            logger.exception(
                sanitize_log_message(f"Failed to update Dynamic DNS record {dynamic_dns_id}")
            )
            raise

        log_audit(
            operation="update_dynamic_dns",
            parameters={
                "site_id": site_id,
                "dynamic_dns_id": dynamic_dns_id,
                **_redact_dynamic_dns_payload(payload),
            },
            result="success",
            site_id=site_id,
        )

        items = _unwrap_response(response)
        return _normalize_dynamic_dns(items[0] if items else {})


async def delete_dynamic_dns(
    dynamic_dns_id: str,
    site_id: str,
    settings: Settings,
    confirm: bool | str = False,
    dry_run: bool | str = False,
) -> dict[str, Any]:
    """Delete a Dynamic DNS configuration."""
    _ensure_local_api(settings)
    validate_confirmation(confirm, "delete_dynamic_dns", dry_run)

    if coerce_bool(dry_run):
        return {
            "dry_run": True,
            "would_delete": dynamic_dns_id,
        }

    async with UniFiClient(settings) as client:
        logger.info(
            sanitize_log_message(f"Deleting Dynamic DNS record {dynamic_dns_id} for site {site_id}")
        )

        if not client.is_authenticated:
            await client.authenticate()

        try:
            response = await client.delete(_dynamic_dns_endpoint(site_id, dynamic_dns_id))
        except APIError:
            logger.exception(
                sanitize_log_message(f"Failed to delete Dynamic DNS record {dynamic_dns_id}")
            )
            raise

        log_audit(
            operation="delete_dynamic_dns",
            parameters={"site_id": site_id, "dynamic_dns_id": dynamic_dns_id},
            result="success",
            site_id=site_id,
        )

        return {"status": "deleted", "dynamic_dns_id": dynamic_dns_id, "response": response}
