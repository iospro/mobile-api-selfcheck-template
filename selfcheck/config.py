"""Test-config loader for offline template runs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class DomainConfig:
    chats_limit: int
    chats_offset: int
    chats_query: str
    feed_limit: int
    feed_offset: int
    report_path: str


def load_domain_config(project_root: Path, name_or_path: str) -> DomainConfig:
    config_path = _resolve_config_path(project_root, name_or_path)
    with config_path.open("r", encoding="utf-8") as file:
        payload = yaml.safe_load(file)

    if not isinstance(payload, dict):
        raise ValueError(f"invalid config root in {config_path}")

    domains = payload.get("domains")
    if not isinstance(domains, dict):
        raise ValueError(f"missing domains section in {config_path}")

    chats = _require_mapping(domains, "chats", config_path)
    chats_query = _require_mapping(chats, "query", config_path)
    feed = _require_mapping(domains, "feed", config_path)
    feed_body = _require_mapping(feed, "body", config_path)
    report = _require_mapping(payload, "report", config_path)

    return DomainConfig(
        chats_limit=_require_int(chats_query, "limit", config_path),
        chats_offset=_require_int(chats_query, "offset", config_path),
        chats_query=_require_str(chats_query, "queryString", config_path),
        feed_limit=_require_int(feed_body, "limit", config_path),
        feed_offset=_require_int(feed_body, "offset", config_path),
        report_path=_require_str(report, "path", config_path),
    )


def _resolve_config_path(project_root: Path, name_or_path: str) -> Path:
    value = name_or_path.strip()
    if not value:
        value = "default"

    path = Path(value)
    if not path.is_absolute():
        if "/" in value or value.endswith(".yml"):
            path = project_root / value
        else:
            path = project_root / "test-configs" / f"{value}.yml"

    if not path.exists():
        raise FileNotFoundError(f"test-config not found: {path}")
    return path


def _require_mapping(value: dict[str, Any], key: str, path: Path) -> dict[str, Any]:
    item = value.get(key)
    if not isinstance(item, dict):
        raise ValueError(f"{path}: '{key}' must be object")
    return item


def _require_int(value: dict[str, Any], key: str, path: Path) -> int:
    item = value.get(key)
    if isinstance(item, bool) or not isinstance(item, int):
        raise ValueError(f"{path}: '{key}' must be int")
    return item


def _require_bool(value: dict[str, Any], key: str, path: Path) -> bool:
    item = value.get(key)
    if not isinstance(item, bool):
        raise ValueError(f"{path}: '{key}' must be bool")
    return item


def _require_str(value: dict[str, Any], key: str, path: Path) -> str:
    item = value.get(key)
    if not isinstance(item, str) or not item.strip():
        raise ValueError(f"{path}: '{key}' must be non-empty string")
    return item
