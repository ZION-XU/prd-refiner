"""Register the shared PRD Refiner skill with Hermes Agent."""

from pathlib import Path


def _skill_path() -> Path:
    here = Path(__file__).resolve().parent
    candidates = (
        here.parent / "skills" / "prd-refiner" / "SKILL.md",
        here / "skills" / "prd-refiner" / "SKILL.md",
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise RuntimeError("prd-refiner plugin: shared SKILL.md was not found")


def register(ctx):
    ctx.register_skill("prd-refiner", _skill_path())
