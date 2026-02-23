"""
Diffing between scene versions.
Highlights: changed lines, emotional shifts, text diff + metadata diff.
"""

from typing import Any
import difflib


def _lines(text: str) -> list[str]:
    return [line.strip() for line in text.strip().split("\n") if line.strip()]


def text_diff(old_text: str, new_text: str) -> list[dict[str, Any]]:
    """
    Return list of diff hunks. Each hunk: {"type": "added"|"removed"|"unchanged", "lines": [...]}
    """
    old_lines = _lines(old_text)
    new_lines = _lines(new_text)
    matcher = difflib.SequenceMatcher(None, old_lines, new_lines)
    result = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            result.append({"type": "unchanged", "lines": old_lines[i1:i2]})
        elif tag == "replace":
            result.append({"type": "removed", "lines": old_lines[i1:i2]})
            result.append({"type": "added", "lines": new_lines[j1:j2]})
        elif tag == "delete":
            result.append({"type": "removed", "lines": old_lines[i1:i2]})
        elif tag == "insert":
            result.append({"type": "added", "lines": new_lines[j1:j2]})
    return result


def changed_lines(old_text: str, new_text: str) -> tuple[list[str], list[str]]:
    """Return (removed_lines, added_lines)."""
    old_lines = set(_lines(old_text))
    new_lines = set(_lines(new_text))
    removed = sorted(old_lines - new_lines)
    added = sorted(new_lines - old_lines)
    return removed, added


def emotional_shift(
    old_params: dict[str, float],
    new_params: dict[str, float],
) -> list[dict[str, Any]]:
    """
    Return list of emotional parameter shifts.
    Each: {"param": str, "old": float, "new": float, "direction": "up"|"down"|"same"}
    """
    shifts = []
    all_keys = set(old_params) | set(new_params)
    for k in all_keys:
        old_v = old_params.get(k, 0)
        new_v = new_params.get(k, 0)
        if old_v < new_v:
            direction = "up"
        elif old_v > new_v:
            direction = "down"
        else:
            direction = "same"
        shifts.append({"param": k, "old": old_v, "new": new_v, "direction": direction})
    return shifts


def metadata_diff(
    old_version: dict[str, Any],
    new_version: dict[str, Any],
) -> dict[str, Any]:
    """
    Compare constraints and emotional params between versions.
    Returns {"emotional_shift": [...], "constraint_changes": {...}}
    """
    old_params = old_version.get("emotional_params", {})
    new_params = new_version.get("emotional_params", {})
    emotional_shift_list = emotional_shift(old_params, new_params)
    old_constraints = old_version.get("constraints", {})
    new_constraints = new_version.get("constraints", {})
    constraint_changes = {}
    for k in set(old_constraints) | set(new_constraints):
        o, n = old_constraints.get(k), new_constraints.get(k)
        if o != n:
            constraint_changes[k] = {"old": o, "new": n}
    return {
        "emotional_shift": emotional_shift_list,
        "constraint_changes": constraint_changes,
    }


def unified_diff_text(old_text: str, new_text: str, old_label: str = "old", new_label: str = "new") -> str:
    """Standard unified diff output."""
    return "".join(
        difflib.unified_diff(
            old_text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile=old_label,
            tofile=new_label,
            lineterm="",
        )
    )
