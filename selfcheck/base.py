"""Core models used by domain tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from time import perf_counter
from typing import Any, Callable, Protocol


class Scenario(str, Enum):
    OK = "ok"
    DTO_FAIL = "dto-fail"
    ENVELOPE_ERROR = "envelope-error"


class ValidationError(Exception):
    """Raised when a response does not match the expected DTO contract."""


@dataclass(frozen=True)
class ApiMethodSpec:
    domain: str
    name: str
    method: str
    path: str
    fixture: str
    uses_envelope: bool
    query: dict[str, Any] | None = None
    body: dict[str, Any] | None = None
    contract: str | None = None
    validator: Callable[[Any, list[str]], int] | None = None


@dataclass
class TestResult:
    domain: str
    name: str
    method: str
    path: str
    query: dict[str, Any] | None
    body: dict[str, Any] | None
    ok: bool
    count: int | None
    duration: float
    stages: list[str] = field(default_factory=list)
    error: str | None = None


class Transport(Protocol):
    def request(self, spec: ApiMethodSpec) -> Any:
        """Return decoded JSON for the given API method spec."""


def run_method(
    spec: ApiMethodSpec,
    transport: Transport,
    contract_root: Path | None = None,
) -> TestResult:
    stages: list[str] = []
    started = perf_counter()
    count: int | None = None

    try:
        _validate_contract(spec, contract_root, stages)
        stages.append(_request_stage(spec))
        response = transport.request(spec)
        stages.append(f"transport: fixture {spec.fixture}")
        payload = _extract_payload(spec, response, stages)

        if spec.validator is not None:
            count = spec.validator(payload, stages)
        else:
            stages.append("dto: no validator")

        stages.append("result: OK")
        return TestResult(
            domain=spec.domain,
            name=spec.name,
            method=spec.method,
            path=spec.path,
            query=spec.query,
            body=spec.body,
            ok=True,
            count=count,
            duration=perf_counter() - started,
            stages=stages,
        )
    except Exception as exc:
        stages.append("result: FAIL")
        return TestResult(
            domain=spec.domain,
            name=spec.name,
            method=spec.method,
            path=spec.path,
            query=spec.query,
            body=spec.body,
            ok=False,
            count=count,
            duration=perf_counter() - started,
            stages=stages,
            error=str(exc),
        )


def _validate_contract(
    spec: ApiMethodSpec,
    contract_root: Path | None,
    stages: list[str],
) -> None:
    if spec.contract is None:
        stages.append("contract: no method contract")
        return
    if contract_root is None:
        raise ValidationError("contract root is required when method contract is set")

    from selfcheck.contracts import validate_method_contract  # local import to avoid cycle

    validate_method_contract(spec, contract_root)
    stages.append(f"contract: {spec.contract} OK")


def _request_stage(spec: ApiMethodSpec) -> str:
    params = ""
    if spec.query:
        query = "&".join(f"{key}={value}" for key, value in spec.query.items())
        params = f" ?{query}"
    if spec.body:
        params = f" body={spec.body}"
    return f"request: {spec.method} {spec.path}{params}"


def _extract_payload(
    spec: ApiMethodSpec, response: Any, stages: list[str]
) -> Any:
    if not spec.uses_envelope:
        stages.append("envelope: skipped, root object expected")
        return response

    if not isinstance(response, dict):
        raise ValidationError("envelope must be an object")

    errors = response.get("errors")
    if errors:
        stages.append("envelope: errors found")
        raise ValidationError(f"api returned errors: {errors}")

    if "data" not in response:
        raise ValidationError("envelope.data is required")

    stages.append("envelope: data found, errors empty")
    return response["data"]
