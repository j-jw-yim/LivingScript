"""
Scene graph loader, validator, and traverser.
Loads scenes from JSON, validates transitions, and supports graph traversal.
"""

import json
from pathlib import Path
from typing import Optional

from engine.paths import SCENES_DIR


def load_scenes(scenes_dir: Optional[Path] = None) -> dict[str, dict]:
    """Load all scene JSON files from the scenes directory."""
    base = scenes_dir or SCENES_DIR
    scenes = {}
    for path in base.glob("*.json"):
        if path.name == "schema.json":
            continue
        with open(path, encoding="utf-8") as f:
            scene = json.load(f)
        scene_id = scene.get("scene_id")
        if scene_id:
            scenes[scene_id] = scene
    return scenes


def validate_transitions(scenes: dict[str, dict]) -> list[str]:
    """
    Validate that all transition targets exist.
    Returns list of error messages (empty if valid).
    """
    errors = []
    scene_ids = set(scenes.keys())
    for scene_id, scene in scenes.items():
        transitions = scene.get("transitions", [])
        for t in transitions:
            target = t.get("target")
            if target and target not in scene_ids:
                errors.append(f"{scene_id} → {target}: target scene not found")
    return errors


def get_next_scenes(scene: dict) -> list[tuple[str, str]]:
    """
    Return list of (target_id, transition_type) for valid next scenes.
    """
    transitions = scene.get("transitions", [])
    return [(t["target"], t.get("type", "default")) for t in transitions if t.get("target")]


def traverse(
    scenes: dict[str, dict],
    start_id: str,
    path: Optional[list[str]] = None,
) -> list[list[str]]:
    """
    Enumerate all paths through the graph from start_id.
    Returns list of paths (each path is a list of scene_ids).
    """
    path = path or [start_id]
    if start_id not in scenes:
        return []
    scene = scenes[start_id]
    next_scenes = get_next_scenes(scene)
    if not next_scenes:
        return [path]  # dead end
    all_paths = []
    for target_id, _ in next_scenes:
        if target_id in path:
            # loop detected — stop and record path up to loop
            all_paths.append(path + [f"{target_id} (loop)"])
        else:
            sub_paths = traverse(scenes, target_id, path + [target_id])
            all_paths.extend(sub_paths)
    return all_paths


def main():
    """CLI: load graph and print valid next scenes for a given scene."""
    import sys
    scenes = load_scenes()
    if not scenes:
        print("No scenes found.", file=sys.stderr)
        sys.exit(1)
    errors = validate_transitions(scenes)
    if errors:
        for e in errors:
            print(f"Warning: {e}", file=sys.stderr)
    scene_id = sys.argv[1] if len(sys.argv) > 1 else list(scenes.keys())[0]
    if scene_id not in scenes:
        print(f"Unknown scene: {scene_id}", file=sys.stderr)
        print(f"Available: {', '.join(scenes)}")
        sys.exit(1)
    scene = scenes[scene_id]
    next_scenes = get_next_scenes(scene)
    print(f"Scene {scene_id}: {scene.get('setting', '?')}")
    print(f"Emotional state: {scene.get('emotional_state', [])}")
    print("Valid next scenes:")
    for target, ttype in next_scenes:
        print(f"  → {target} ({ttype})")
    if not next_scenes:
        print("  (dead end)")


if __name__ == "__main__":
    main()
