"""Tests for read-only Cloudflare Registrar availability checks."""

from typing import Any

from domain_agent.cloudflare_lookup import CloudflareRegistrarClient
from domain_agent.models import AvailabilityStatus


class FakeResponse:
    """A no-network response carrying pre-arranged Cloudflare JSON."""

    def __init__(self, body: dict[str, Any]) -> None:
        self.body = body

    def json(self) -> dict[str, Any]:
        return self.body


class FakeSession:
    """Records a request instead of sending it to Cloudflare."""

    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.call_arguments: dict[str, Any] | None = None

    def post(self, url: str, **kwargs: Any) -> FakeResponse:
        self.call_arguments = {"url": url, **kwargs}
        return self.response


def test_check_domains_preserves_available_unavailable_and_unknown_results() -> None:
    """Unsupported extensions remain unknown instead of being called available."""
    session = FakeSession(
        FakeResponse(
            {
                "success": True,
                "result": {
                    "domains": [
                        {
                            "name": "available.co.nz",
                            "registrable": True,
                            "pricing": {
                                "currency": "NZD",
                                "registration_cost": "24.50",
                            },
                        },
                        {
                            "name": "taken.co.nz",
                            "registrable": False,
                            "reason": "domain_unavailable",
                        },
                        {
                            "name": "unsupported.co.nz",
                            "registrable": False,
                            "reason": "extension_not_supported_via_api",
                        },
                    ]
                },
            }
        )
    )
    client = CloudflareRegistrarClient(
        account_id="account-test",
        api_token="token-test",
        session=session,
    )

    results = client.check_domains(
        ["available.co.nz", "taken.co.nz", "unsupported.co.nz"]
    )

    assert session.call_arguments is not None
    assert session.call_arguments["json"] == {
        "domains": ["available.co.nz", "taken.co.nz", "unsupported.co.nz"]
    }
    assert results["available.co.nz"].status == AvailabilityStatus.AVAILABLE
    assert results["available.co.nz"].price == 24.50
    assert results["taken.co.nz"].status == AvailabilityStatus.UNAVAILABLE
    assert results["unsupported.co.nz"].status == AvailabilityStatus.UNKNOWN
    assert results["unsupported.co.nz"].error == "extension_not_supported_via_api"


def test_check_domains_rejects_more_than_twenty_domains() -> None:
    """The client enforces Cloudflare's documented request limit locally."""
    client = CloudflareRegistrarClient(
        account_id="account-test",
        api_token="token-test",
        session=FakeSession(FakeResponse({})),
    )

    domains = [f"candidate-{number}.co.nz" for number in range(21)]

    try:
        client.check_domains(domains)
    except ValueError as error:
        assert "at most 20" in str(error)
    else:
        raise AssertionError("Expected a ValueError for more than 20 domains.")
