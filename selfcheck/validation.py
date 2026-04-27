"""Small DTO validation helpers."""

from __future__ import annotations

from typing import Any

from selfcheck.base import ValidationError


def require_dict(value: dict[str, Any], key: str, path: str) -> dict[str, Any]:
    nested = _require_key(value, key, path)
    if not isinstance(nested, dict):
        raise ValidationError(f"{path}.{key} must be object, got {_type_name(nested)}")
    return nested


def require_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValidationError(f"{path} must be array, got {_type_name(value)}")
    return value


def require_int(value: dict[str, Any], key: str, path: str) -> int:
    item = _require_key(value, key, path)
    if isinstance(item, bool) or not isinstance(item, int):
        raise ValidationError(f"{path}.{key} is required int, got {_type_name(item)}")
    return item


def require_bool(value: dict[str, Any], key: str, path: str) -> bool:
    item = _require_key(value, key, path)
    if not isinstance(item, bool):
        raise ValidationError(f"{path}.{key} is required bool, got {_type_name(item)}")
    return item


def require_str(value: dict[str, Any], key: str, path: str) -> str:
    item = _require_key(value, key, path)
    if not isinstance(item, str) or not item:
        raise ValidationError(f"{path}.{key} is required string, got {_type_name(item)}")
    return item


def optional_str(value: dict[str, Any], key: str, path: str) -> str | None:
    if key not in value or value[key] is None:
        return None
    if not isinstance(value[key], str):
        raise ValidationError(f"{path}.{key} must be string or null")
    return value[key]


def optional_dict(value: dict[str, Any], key: str, path: str) -> dict[str, Any] | None:
    if key not in value or value[key] is None:
        return None
    if not isinstance(value[key], dict):
        raise ValidationError(f"{path}.{key} must be object or null")
    return value[key]


def enum_value(
    value: dict[str, Any],
    key: str,
    path: str,
    allowed: set[str],
    warnings: list[str],
) -> str:
    item = require_str(value, key, path)
    if item not in allowed:
        warnings.append(f"{path}.{key} has unknown enum value: {item}")
    return item


def _require_key(value: dict[str, Any], key: str, path: str) -> Any:
    if key not in value:
        raise ValidationError(f"{path}.{key} is required")
    if value[key] is None:
        raise ValidationError(f"{path}.{key} is required, got null")
    return value[key]


def _type_name(value: Any) -> str:
    if value is None:
        return "null"
    return type(value).__name__
