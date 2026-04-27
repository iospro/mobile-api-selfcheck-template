#!/usr/bin/env python3
"""Run offline mobile API selfcheck template."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from domains import test_chats, test_feed
from selfcheck.base import Scenario
from selfcheck.config import load_domain_config
from selfcheck.reporters import ConsoleReporter, MarkdownReporter
from selfcheck.transports import FixtureTransport


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Offline template for mobile API contract selfchecks."
    )
    parser.add_argument(
        "--test-config",
        default="default",
        help="Config name from test-configs/ or explicit .yml path.",
    )
    parser.add_argument(
        "--scenario",
        choices=[scenario.value for scenario in Scenario],
        default=Scenario.OK.value,
        help="Fixture scenario to run.",
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="Print validation stages for every method.",
    )
    parser.add_argument(
        "--report",
        default="",
        help="Optional markdown report path override.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(__file__).resolve().parent
    config = load_domain_config(project_root, args.test_config)
    report_path = args.report.strip() or config.report_path
    scenario = Scenario(args.scenario)
    transport = FixtureTransport(project_root / "fixtures", scenario)
    contract_root = project_root / "contracts"

    results = []
    results.extend(test_chats.run(transport, config, contract_root))
    results.extend(test_feed.run(transport, config, contract_root))

    ConsoleReporter(trace=args.trace).write(results)
    MarkdownReporter(project_root / report_path).write(results)

    return 1 if any(not result.ok for result in results) else 0


if __name__ == "__main__":
    sys.exit(main())
