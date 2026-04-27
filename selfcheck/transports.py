"""Transports used by the template."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from selfcheck.base import ApiMethodSpec, Scenario


class FixtureTransport:
    """Offline transport that reads prepared JSON responses from fixtures."""

    def __init__(self, fixtures_root: Path, scenario: Scenario) -> None:
        self.fixtures_root = fixtures_root
        self.scenario = scenario

    def request(self, spec: ApiMethodSpec) -> Any:
        path = self.fixtures_root / spec.fixture.format(scenario=self.scenario.value)
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
