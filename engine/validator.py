"""
Post-generation validation. Checks beats, line count, forbidden words.
Returns validation result; triggers retry if invalid.
"""

import re
from typing import Any

# Character line pattern: "D: ..." or "J: ..."
LINE_PATTERN = re.compile(r"^[A-Za-z0-9_]+:\s*.+$")


def _dialogue_lines(text: str) -> list[str]:
    """Extract dialogue lines (character: line) from text."""
    return [l.strip() for l in text.strip().split("\n") if l.strip() and LINE_PATTERN.match(l.strip())]


def validate(
    text: str,
    scene: dict,
    characters: list[dict] | None = None,
) -> dict[str, Any]:
    """
    Validate generated dialogue against scene constraints.
    Returns {"valid": bool, "errors": list[str], "warnings": list[str]}.
    """
    errors = []
    warnings = []
    lines = _dialogue_lines(text)

    # Max lines
    max_lines = scene.get("constraints", {}).get("max_lines", 999)
    if len(lines) > max_lines:
        errors.append(f"Too many lines: {len(lines)} (max {max_lines})")

    # Beats (soft check - look for keywords)
    beats = scene.get("beats", [])
    text_lower = text.lower()
    for beat in beats:
        # Simple keyword presence - beat words should appear somewhere
        words = beat.lower().split()
        if not any(w in text_lower for w in words if len(w) > 2):
            warnings.append(f"Beat '{beat}' may be missing or weakly represented")

    # Forbidden expressions (from characters and scene)
    forbidden = list(scene.get("constraints", {}).get("forbidden_words", []))
    if characters:
        for c in characters:
            forbidden.extend(c.get("forbidden_expressions", []))
    forbidden = [f.lower() for f in forbidden if f]

    for phrase in forbidden:
        if phrase.lower() in text.lower():
            errors.append(f"Forbidden phrase: '{phrase}'")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "line_count": len(lines),
    }
