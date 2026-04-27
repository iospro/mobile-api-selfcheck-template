"""Chats domain examples."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from selfcheck.base import ApiMethodSpec, Transport, run_method
from selfcheck.config import DomainConfig
from selfcheck.validation import (
    enum_value,
    optional_dict,
    optional_str,
    require_bool,
    require_dict,
    require_int,
    require_list,
    require_str,
)


CHAT_TYPES = {"private", "group", "task"}


def run(
    transport: Transport,
    config: DomainConfig,
    contract_root: Path,
):
    spec = ApiMethodSpec(
        domain="Chats",
        name="Search chats",
        method="GET",
        path="/api/chats",
        query={
            "limit": config.chats_limit,
            "offset": config.chats_offset,
            "queryString": config.chats_query,
        },
        fixture="chats/search_{scenario}.json",
        uses_envelope=True,
        contract="methods/chats/search",
        validator=validate_chat_list,
    )
    return [run_method(spec, transport, contract_root)]


def validate_chat_list(data: Any, stages: list[str]) -> int:
    chats = require_list(data, "data")
    warnings: list[str] = []
    stages.append(f"dto: ChatDTO[] count={len(chats)}")

    for index, chat in enumerate(chats):
        path = f"data[{index}]"
        if not isinstance(chat, dict):
            raise TypeError(f"{path} must be object")
        validate_chat(chat, path, warnings)

    if warnings:
        stages.append(f"dto warnings: {'; '.join(warnings)}")
    stages.append("dto: ChatDTO[] valid")
    return len(chats)


def validate_chat(chat: dict[str, Any], path: str, warnings: list[str]) -> None:
    require_int(chat, "id", path)
    require_str(chat, "title", path)
    require_bool(chat, "isClosed", path)
    enum_value(chat, "chatType", path, CHAT_TYPES, warnings)
    optional_str(chat, "avatarUrl", path)

    last_message = optional_dict(chat, "lastMessage", path)
    if last_message is not None:
        validate_last_message(last_message, f"{path}.lastMessage")


def validate_last_message(value: dict[str, Any], path: str) -> None:
    require_int(value, "id", path)
    require_str(value, "text", path)
    author = require_dict(value, "author", path)
    require_int(author, "id", f"{path}.author")
    require_str(author, "name", f"{path}.author")
