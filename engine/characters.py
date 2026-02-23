"""Load characters from scripts/characters/."""

import json
from pathlib import Path

from engine.paths import SCRIPTS_DIR

CHARACTERS_DIR = SCRIPTS_DIR / "characters"


def load_characters() -> dict[str, dict]:
    """Load all character JSON files, indexed by character_id."""
    chars = {}
    if not CHARACTERS_DIR.exists():
        return chars
    for path in CHARACTERS_DIR.glob("*.json"):
        if path.name == "schema.json":
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            cid = data.get("character_id")
            if cid:
                chars[cid] = data
        except (json.JSONDecodeError, KeyError):
            continue
    return chars


def load_characters_for_scene(scene: dict) -> list[dict]:
    """Load character dicts for characters in the scene."""
    all_chars = load_characters()
    return [all_chars[c] for c in scene.get("characters", []) if c in all_chars]
