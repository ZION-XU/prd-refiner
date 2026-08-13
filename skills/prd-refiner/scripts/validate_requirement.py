#!/usr/bin/env python3
"""Validate the essential structure and identifiers of a PRD Refiner output package."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_FILES = ("ai-ready-prd.md", "clarification-log.md", "quality-report.md")
REQUIRED_HEADINGS = (
    "# 1. 文档控制",
    "# 2. 背景、目标、范围与非目标",
    "# 5. 功能需求",
    "# 9. 验收标准",
    "# 11. 开放问题、风险与追溯矩阵",
)
HEADING_ID_PATTERN = re.compile(r"^#{1,6}\s+((?:FR|BR|NFR|DATA|AC|CL)-\d{3})\b", re.MULTILINE)


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_requirement.py <output-directory>")
        return 2

    root = Path(sys.argv[1])
    errors: list[str] = []
    if not root.is_dir():
        print(f"ERROR: output directory not found: {root}")
        return 2

    files: dict[str, str] = {}
    for name in REQUIRED_FILES:
        path = root / name
        if not path.is_file():
            fail(f"missing required file: {name}", errors)
            continue
        files[name] = path.read_text(encoding="utf-8")

    prd = files.get("ai-ready-prd.md", "")
    for heading in REQUIRED_HEADINGS:
        if heading not in prd:
            fail(f"ai-ready-prd.md missing heading: {heading}", errors)

    identifiers = HEADING_ID_PATTERN.findall(prd)
    duplicates = sorted({item for item in identifiers if identifiers.count(item) > 1})
    if duplicates:
        fail("duplicate requirement IDs in ai-ready-prd.md: " + ", ".join(duplicates), errors)
    if not any(item.startswith("FR-") for item in identifiers):
        fail("ai-ready-prd.md has no functional requirement ID (FR-xxx)", errors)
    if not any(item.startswith("AC-") for item in identifiers):
        fail("ai-ready-prd.md has no acceptance criterion ID (AC-xxx)", errors)

    log = files.get("clarification-log.md", "")
    if log and "状态：" not in log:
        fail("clarification-log.md has no decision status", errors)

    report = files.get("quality-report.md", "")
    if report and "下游可消费性" not in report:
        fail("quality-report.md has no downstream-consumability conclusion", errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Requirement package validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
