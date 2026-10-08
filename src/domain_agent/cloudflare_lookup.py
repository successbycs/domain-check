"""Read-only Cloudflare Registrar availability checks."""

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Protocol

import requests

from domain_agent.models import AvailabilityCheck, AvailabilityStatus

CLOUDFLARE_PROVIDER = "Cloudflare Registrar"
MAX_DOMAINS_PER_REQUEST = 20


class HttpResponse(Protocol):
    """The small part of an HTTP response required by this module."""

    def json(self) -> dict[str, Any]:
        """Return the response body as decoded JSON."""


class HttpSession(Protocol):
    """The small part of requests.Session required by this module."""

    def post(self, url: str, **kwargs: Any) -> HttpResponse:
        """Send a POST request to Cloudflare's Registrar API."""


class CloudflareRegistrarClient:
    """Check domain availability without buying, reserving, or changing domains."""

    def __init__(
        self,
        *,
        account_id: str,
        api_token: str,
        session: HttpSession | None = None,
    ) -> None:
        self.account_id = account_id
        self.api_token = api_token
        self.session = session or requests.Session()

    def check_domains(self, domains: list[str]) -> dict[str, AvailabilityCheck]:
        """Return one timestamped, read-only availability result per domain."""
        if not domains:
            return {}
        if len(domains) > MAX_DOMAINS_PER_REQUEST:
            raise ValueError(
                f"Cloudflare accepts at most {MAX_DOMAINS_PER_REQUEST} domains per check."
            )

        checked_at = datetime.now(timezone.utc)
        url = (
            "https://api.cloudflare.com/client/v4/accounts/"
            f"{self.account_id}/registrar/domain-check"
        )
        try:
            response = self.session.post(
                url,
                headers={
                    "Authorization": f"Bearer {self.api_token}",
                    "Content-Type": "application/json",
                },
                json={"domains": domains},
                timeout=20,
            )
            body = response.json()
        except requests.RequestException as error:
            return _unknown_results(domains, checked_at, f"Cloudflare request failed: {error}")
        except ValueError as error:
            return _unknown_results(domains, checked_at, f"Cloudflare returned invalid JSON: {error}")

        if not body.get("success"):
            errors = body.get("errors", [])
            return _unknown_results(
                domains,
                checked_at,
                f"Cloudflare API reported an error: {errors}",
            )

        returned_domains = body.get("result", {}).get("domains", [])
        results_by_name = {
            result["name"]: result
            for result in returned_domains
            if isinstance(result, dict) and "name" in result
        }
        return {
            domain: _availability_from_cloudflare(
                results_by_name.get(domain),
                checked_at,
            )
            for domain in domains
        }


def _availability_from_cloudflare(
    result: dict[str, Any] | None,
    checked_at: datetime,
) -> AvailabilityCheck:
    """Convert one Cloudflare result without overstating what it proves."""
    if result is None:
        return AvailabilityCheck(
            status=AvailabilityStatus.UNKNOWN,
            provider=CLOUDFLARE_PROVIDER,
            checked_at=checked_at,
            error="Cloudflare returned no result for this domain.",
        )

    if result.get("registrable") is True:
        pricing = result.get("pricing", {})
        return AvailabilityCheck(
            status=AvailabilityStatus.AVAILABLE,
            provider=CLOUDFLARE_PROVIDER,
            checked_at=checked_at,
            price=_parse_price(pricing.get("registration_cost")),
            currency=pricing.get("currency"),
        )

    reason = result.get("reason", "Cloudflare did not provide a reason.")
    if reason == "domain_unavailable":
        return AvailabilityCheck(
            status=AvailabilityStatus.UNAVAILABLE,
            provider=CLOUDFLARE_PROVIDER,
            checked_at=checked_at,
            error=reason,
        )

    return AvailabilityCheck(
        status=AvailabilityStatus.UNKNOWN,
        provider=CLOUDFLARE_PROVIDER,
        checked_at=checked_at,
        error=reason,
    )


def _unknown_results(
    domains: list[str], checked_at: datetime, error: str
) -> dict[str, AvailabilityCheck]:
    """Return an honest unknown result for every requested domain."""
    return {
        domain: AvailabilityCheck(
            status=AvailabilityStatus.UNKNOWN,
            provider=CLOUDFLARE_PROVIDER,
            checked_at=checked_at,
            error=error,
        )
        for domain in domains
    }


def _parse_price(value: Any) -> Decimal | None:
    """Return a precise price when Cloudflare supplies a valid amount."""
    if value is None:
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None
