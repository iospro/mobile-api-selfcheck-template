"""Feed domain examples."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from selfcheck.base import ApiMethodSpec, Transport, run_method
from selfcheck.config import DomainConfig
from selfcheck.validation import (
    enum_value,
    optional_dict,
    require_bool,
    require_dict,
    require_int,
    require_list,
    require_str,
)


COMMENT_TYPES = {"comment", "system"}


def run(
    transport: Transport,
    config: DomainConfig,
    contract_root: Path,
):
    spec = ApiMethodSpec(
        domain="Feed",
        name="Feed list",
        method="POST",
        path="/api/feed",
        body={
            "limit": config.feed_limit,
            "offset": config.feed_offset,
        },
        fixture="feed/list_{scenario}.json",
        uses_envelope=True,
        contract="methods/feed/list",
        validator=validate_feed_list,
    )
    return [run_method(spec, transport, contract_root)]


def validate_feed_list(data: Any, stages: list[str]) -> int:
    groups = require_list(data, "data")
    warnings: list[str] = []
    stages.append(f"dto: FeedGroupDTO[] count={len(groups)}")

    for group_index, group in enumerate(groups):
        group_path = f"data[{group_index}]"
        if not isinstance(group, dict):
            raise TypeError(f"{group_path} must be object")
        validate_feed_group(group, group_path, warnings)

    if warnings:
        stages.append(f"dto warnings: {'; '.join(warnings)}")
    stages.append("dto: FeedGroupDTO[] valid")
    return len(groups)


def validate_feed_group(
    group: dict[str, Any], path: str, warnings: list[str]
) -> None:
    task = require_dict(group, "task", path)
    validate_task_link(task, f"{path}.task")
    comments = require_list(group.get("comments"), f"{path}.comments")
    for comment_index, comment in enumerate(comments):
        comment_path = f"{path}.comments[{comment_index}]"
        if not isinstance(comment, dict):
            raise TypeError(f"{comment_path} must be object")
        validate_comment(comment, comment_path, warnings)


def validate_task_link(value: dict[str, Any], path: str) -> None:
    require_int(value, "id", path)
    require_str(value, "title", path)
    attributes = require_dict(value, "attributes", path)
    require_str(attributes, "subcatName", f"{path}.attributes")
    style = require_dict(attributes, "style", f"{path}.attributes")
    require_str(style, "color", f"{path}.attributes.style")
    require_str(style, "icon", f"{path}.attributes.style")


def validate_comment(
    value: dict[str, Any], path: str, warnings: list[str]
) -> None:
    require_int(value, "id", path)
    enum_value(value, "type", path, COMMENT_TYPES, warnings)
    require_str(value, "text", path)
    require_bool(value, "isRead", path)
    author = optional_dict(value, "author", path)
    if author is not None:
        require_int(author, "id", f"{path}.author")
        require_str(author, "name", f"{path}.author")
