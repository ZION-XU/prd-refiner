#!/usr/bin/env python3
"""Validate shared paths and version alignment for PRD Refiner adapters."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BASE_VERSION = "1.0.0"

JSON_VERSIONS = {
    "package.json": ("version",),
    ".claude-plugin/plugin.json": ("version",),
    ".claude-plugin/marketplace.json": ("plugins", 0, "version"),
    ".cursor-plugin/plugin.json": ("version",),
    ".devin-plugin/plugin.json": ("version",),
    ".kimi-plugin/plugin.json": ("version",),
    "gemini-extension.json": ("version",),
}

REQUIRED_PATHS = (
    ".codex-plugin/plugin.json",
    ".claude-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
    ".devin-plugin/plugin.json",
    ".kimi-plugin/plugin.json",
    ".hermes-plugin/plugin.yaml",
    ".hermes-plugin/__init__.py",
    ".opencode/plugins/prd-refiner.js",
    ".pi/extensions/prd-refiner.ts",
    "gemini-extension.json",
    "GEMINI.md",
    "package.json",
    "skills/prd-refiner/SKILL.md",
)


def nested(data, path):
    for key in path:
        data = data[key]
    return data


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED_PATHS:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required path: {relative}")

    for relative, key_path in JSON_VERSIONS.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        value = nested(json.loads(path.read_text(encoding="utf-8")), key_path)
        if value != BASE_VERSION:
            errors.append(f"{relative} version is {value!r}, expected {BASE_VERSION!r}")

    codex_path = ROOT / ".codex-plugin/plugin.json"
    if codex_path.is_file():
        codex = json.loads(codex_path.read_text(encoding="utf-8"))
        version = codex.get("version", "").split("+", 1)[0]
        if version != BASE_VERSION:
            errors.append(f"Codex base version is {version!r}, expected {BASE_VERSION!r}")
        if codex.get("skills") != "./skills/":
            errors.append("Codex manifest must reference ./skills/")

    hermes_path = ROOT / ".hermes-plugin/plugin.yaml"
    if hermes_path.is_file():
        match = re.search(r"^version:\s*(\S+)\s*$", hermes_path.read_text(encoding="utf-8"), re.MULTILINE)
        if not match or match.group(1) != BASE_VERSION:
            errors.append("Hermes version is missing or out of sync")

    skill_text = (ROOT / "skills/prd-refiner/SKILL.md").read_text(encoding="utf-8")
    if "不要因普通对话提及 PRD 而自动调用" not in skill_text:
        errors.append("core Skill lost the explicit-invocation guard")

    if errors:
        print("Cross-platform validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Cross-platform plugin layout validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
