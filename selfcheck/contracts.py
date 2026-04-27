"""YAML method-contract checks for the offline template."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from selfcheck.base import ApiMethodSpec, ValidationError


def validate_method_contract(spec: ApiMethodSpec, contract_root: Path) -> None:
    if not spec.contract:
        return

    contract_path = contract_root / f"{spec.contract}.yml"
    if not contract_path.exists():
        raise ValidationError(f"contract file not found: {contract_path}")

    payload = _read_yaml(contract_path)
    request = payload.get("request")
    response = payload.get("response")
    if not isinstance(request, dict) or not isinstance(response, dict):
        raise ValidationError(f"contract {spec.contract} must contain request/response objects")

    contract_method = request.get("method")
    contract_path_value = request.get("path")
    contract_envelope = response.get("uses_envelope")

    if contract_method != spec.method:
        raise ValidationError(
            f"contract {spec.contract}: method mismatch "
            f"(expected {contract_method}, got {spec.method})"
        )
    if contract_path_value != spec.path:
        raise ValidationError(
            f"contract {spec.contract}: path mismatch "
            f"(expected {contract_path_value}, got {spec.path})"
        )
    if contract_envelope != spec.uses_envelope:
        raise ValidationError(
            f"contract {spec.contract}: uses_envelope mismatch "
            f"(expected {contract_envelope}, got {spec.uses_envelope})"
        )


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        payload = yaml.safe_load(file)
    if not isinstance(payload, dict):
        raise ValidationError(f"invalid yaml root in {path}")
    return payload
