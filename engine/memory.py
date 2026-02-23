"""
Scene versioning with semantic metadata.
Stores text, constraints, emotional parameters, timestamp.
JSON-based storage — no external DB required.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from engine.paths import VERSIONS_DIR


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _version_path(scene_id: str, version_id: str) -> Path:
    return VERSIONS_DIR / scene_id / f"{version_id}.json"


def save_version(
    scene_id: str,
    text: str,
    constraints: dict[str, Any],
    emotional_params: dict[str, float],
    parent_version_id: str | None = None,
) -> str:
    """
    Save a scene version. Returns version_id.
    """
    _ensure_dir(VERSIONS_DIR / scene_id)
    now = datetime.now(timezone.utc)
    timestamp = now.isoformat()
    version_id = f"{scene_id}_{now.strftime('%Y%m%d_%H%M%S')}"
    path = _version_path(scene_id, version_id)
    data = {
        "version_id": version_id,
        "scene_id": scene_id,
        "text": text,
        "constraints": constraints,
        "emotional_params": emotional_params,
        "timestamp": timestamp,
        "parent_version_id": parent_version_id,
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return version_id


def load_version(scene_id: str, version_id: str) -> dict[str, Any] | None:
    """Load a specific version. Returns None if not found."""
    path = _version_path(scene_id, version_id)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def list_versions(scene_id: str) -> list[dict[str, Any]]:
    """
    List all versions for a scene, newest first.
    Returns list of version metadata (without full text).
    """
    dir_path = VERSIONS_DIR / scene_id
    if not dir_path.exists():
        return []
    versions = []
    for f in dir_path.glob("*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            versions.append({
                "version_id": data["version_id"],
                "scene_id": data["scene_id"],
                "timestamp": data["timestamp"],
                "emotional_params": data.get("emotional_params", {}),
                "constraints": data.get("constraints", {}),
            })
        except (json.JSONDecodeError, KeyError):
            continue
    return sorted(versions, key=lambda v: v["timestamp"], reverse=True)
