#!/usr/bin/env python3
"""Validate the essential structure and identifiers of a PRD Refiner output package."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_FILES = (
    "ai-ready-prd.md",
    "interaction-spec.md",
    "clarification-log.md",
    "traceability-matrix.md",
    "quality-report.md",
    "evaluation-scorecard.md",
)
REQUIRED_HEADINGS = (
    "# 1. 文档控制",
    "# 2. 背景、目标、范围与非目标",
    "# 5. 功能需求",
    "# 9. 验收标准",
    "# 11. 开放问题、风险与决策摘要",
)
HEADING_ID_PATTERN = re.compile(r"^#{1,6}\s+((?:FR|BR|NFR|DATA|AC|CL)-\d{3})\b", re.MULTILINE)
CL_ID_PATTERN = re.compile(r"^#{1,6}\s+(CL-\d{3})\b", re.MULTILINE)
UI_ID_PATTERN = re.compile(r"^#{1,6}\s+(UI-\d{3})\b", re.MULTILINE)
PLACEHOLDER_PATTERN = re.compile(r"<[^>\n]+>")


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
    if PLACEHOLDER_PATTERN.search(prd):
        fail("ai-ready-prd.md contains unresolved template placeholders", errors)
    if "来源" not in prd and "追溯" not in prd:
        fail("ai-ready-prd.md has no source or traceability section", errors)

    interaction = files.get("interaction-spec.md", "")
    for heading in ("# 1. 输入与解析边界", "# 4. PRD与原型对齐检查"):
        if interaction and heading not in interaction:
            fail(f"interaction-spec.md missing heading: {heading}", errors)
    ui_ids = UI_ID_PATTERN.findall(interaction)
    duplicate_ui_ids = sorted({item for item in ui_ids if ui_ids.count(item) > 1})
    if duplicate_ui_ids:
        fail(
            "duplicate interaction IDs in interaction-spec.md: "
            + ", ".join(duplicate_ui_ids),
            errors,
        )
    if interaction and not ui_ids and "不适用" not in interaction and "未提供原型" not in interaction:
        fail("interaction-spec.md has no UI-xxx record or explicit not-applicable statement", errors)
    if PLACEHOLDER_PATTERN.search(interaction):
        fail("interaction-spec.md contains unresolved template placeholders", errors)

    log = files.get("clarification-log.md", "")
    if log and "状态：" not in log:
        fail("clarification-log.md has no decision status", errors)
    clarification_ids = CL_ID_PATTERN.findall(log)
    duplicate_clarifications = sorted(
        {item for item in clarification_ids if clarification_ids.count(item) > 1}
    )
    if duplicate_clarifications:
        fail(
            "duplicate clarification IDs in clarification-log.md: "
            + ", ".join(duplicate_clarifications),
            errors,
        )
    if log and not clarification_ids and "无澄清" not in log:
        fail("clarification-log.md has no CL-xxx record", errors)
    if PLACEHOLDER_PATTERN.search(log):
        fail("clarification-log.md contains unresolved template placeholders", errors)

    matrix = files.get("traceability-matrix.md", "")
    for heading in ("# 需求追溯矩阵", "## 2. 正向追溯矩阵", "## 3. 反向覆盖检查"):
        if matrix and heading not in matrix:
            fail(f"traceability-matrix.md missing heading: {heading}", errors)
    for keyword in ("来源", "需求", "原型", "澄清", "验收"):
        if matrix and keyword not in matrix:
            fail(f"traceability-matrix.md missing mapping dimension: {keyword}", errors)
    if matrix and "FR-" not in matrix:
        fail("traceability-matrix.md has no functional requirement reference", errors)
    if matrix and "AC-" not in matrix:
        fail("traceability-matrix.md has no acceptance criterion reference", errors)
    if PLACEHOLDER_PATTERN.search(matrix):
        fail("traceability-matrix.md contains unresolved template placeholders", errors)

    report = files.get("quality-report.md", "")
    if report and "下游可消费性" not in report:
        fail("quality-report.md has no downstream-consumability conclusion", errors)
    if report and "待确认" not in report:
        fail("quality-report.md does not report unresolved items", errors)
    if PLACEHOLDER_PATTERN.search(report):
        fail("quality-report.md contains unresolved template placeholders", errors)

    evaluation = files.get("evaluation-scorecard.md", "")
    for keyword in (
        "完整性",
        "清晰性",
        "一致性",
        "可追溯性",
        "可测试性",
        "AI可消费性",
        "人工可理解性",
        "下游可用性",
        "总分",
    ):
        if evaluation and keyword not in evaluation.replace(" ", ""):
            fail(f"evaluation-scorecard.md missing evaluation dimension: {keyword}", errors)
    if evaluation and ("原始" not in evaluation or "优化后" not in evaluation):
        fail("evaluation-scorecard.md must compare original and optimized requirements", errors)
    if PLACEHOLDER_PATTERN.search(evaluation):
        fail("evaluation-scorecard.md contains unresolved template placeholders", errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Requirement package validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
