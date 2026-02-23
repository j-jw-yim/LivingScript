"""Centralized path constants for the engine."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
SCENES_DIR = SCRIPTS_DIR / "scenes"
PROMPTS_DIR = SCRIPTS_DIR / "prompts"
VERSIONS_DIR = PROJECT_ROOT / "data" / "versions"
