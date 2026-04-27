"""Console and markdown reporters."""

from __future__ import annotations

import json
from pathlib import Path

from selfcheck.base import TestResult


class ConsoleReporter:
    def __init__(self, trace: bool) -> None:
        self.trace = trace

    def write(self, results: list[TestResult]) -> None:
        failed = [result for result in results if not result.ok]
        print(f"API selfcheck: {'FAILED' if failed else 'OK'}")
        print(f"Methods: {len(results)}")
        print(f"Errors: {len(failed)}")
        print()

        for result in results:
            self._write_result(result)

    def _write_result(self, result: TestResult) -> None:
        status = "OK" if result.ok else "FAIL"
        count = f" | Count: {result.count}" if result.count is not None else ""
        print(f"[{result.domain}] {result.name}")
        print(f"Result: {status} | Time: {result.duration:.2f}s{count}")
        print(f"{result.method} {result.path}")
        if result.query:
            print(f"query: {_format_mapping(result.query)}")
        if result.body:
            print(f"body: {json.dumps(result.body, ensure_ascii=False)}")
        if result.error:
            print(f"error: {result.error}")
        if self.trace:
            for stage in result.stages:
                print(f"  - {stage}")
        print()


class MarkdownReporter:
    def __init__(self, path: Path) -> None:
        self.path = path

    def write(self, results: list[TestResult]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        failed = [result for result in results if not result.ok]
        lines = [
            "# API Selfcheck Report",
            "",
            f"Status: {'FAILED' if failed else 'OK'}",
            f"Methods: {len(results)}",
            f"Errors: {len(failed)}",
            "",
        ]

        if failed:
            lines.extend(["## Errors", ""])
            for result in failed:
                lines.extend([f"- [{result.domain}] {result.name}: {result.error}"])
            lines.append("")

        for result in results:
            lines.extend(_markdown_result(result))

        self.path.write_text("\n".join(lines), encoding="utf-8")


def _markdown_result(result: TestResult) -> list[str]:
    status = "OK" if result.ok else "FAIL"
    count = f" | Count: {result.count}" if result.count is not None else ""
    lines = [
        f"## [{result.domain}] {result.name}",
        "",
        f"Result: {status} | Time: {result.duration:.2f}s{count}",
        "",
        f"{result.method} `{result.path}`",
        "",
    ]
    if result.query:
        lines.extend([f"query: `{_format_mapping(result.query)}`", ""])
    if result.body:
        lines.extend([f"body: `{json.dumps(result.body, ensure_ascii=False)}`", ""])
    if result.error:
        lines.extend([f"error: `{result.error}`", ""])
    lines.extend(["Stages:", ""])
    for stage in result.stages:
        lines.append(f"- {stage}")
    lines.append("")
    return lines


def _format_mapping(value: dict[str, object]) -> str:
    return "&".join(f"{key}={item}" for key, item in value.items())
