"""
Replay mode for generated scenes.
Line-by-line playback, adjustable pacing, optional pause on silence.
"""

import re
import sys
import time
from typing import Callable, Optional

# Pattern: "D: ..." or "J: ..." — character lines
LINE_PATTERN = re.compile(r"^([A-Za-z0-9_]+):\s*(.+)$")


def parse_dialogue(text: str) -> list[tuple[str, str]]:
    """Parse dialogue into (character, line) pairs."""
    lines = []
    for raw in text.strip().split("\n"):
        raw = raw.strip()
        if not raw:
            continue
        m = LINE_PATTERN.match(raw)
        if m:
            lines.append((m.group(1), m.group(2)))
        else:
            # Unmatched line — treat as continuation or narrator, use "?"
            lines.append(("?", raw))
    return lines


def _base_duration(line: str, words_per_min: int = 120) -> float:
    """Base duration in seconds from line length."""
    word_count = max(1, len(line.split()))
    return (word_count / words_per_min) * 60


def _silence_multiplier(line: str, silence_density: float) -> float:
    """Pause longer for lines that suggest silence (short, trailing ...)"""
    if not line or silence_density <= 0:
        return 1.0
    mult = 1.0
    if len(line) < 10:
        mult += silence_density * 1.5  # Short line = possible pause
    if line.rstrip().endswith("..."):
        mult += silence_density * 2.0   # Ellipsis = silence
    return mult


def replay(
    text: str,
    on_line: Callable[[str, str, int, int], None],
    pace: float = 1.0,
    silence_density: float = 0.3,
    words_per_min: int = 120,
) -> None:
    """
    Replay dialogue line by line. Calls on_line(character, line, index, total) for each line.
    pace: 1.0 = normal, 2.0 = 2x speed, 0.5 = half speed.
    silence_density: 0-1, higher = longer pauses on short/elliptical lines.
    """
    lines = parse_dialogue(text)
    total = len(lines)
    for i, (char, line) in enumerate(lines):
        on_line(char, line, i, total)
        base = _base_duration(line, words_per_min)
        mult = _silence_multiplier(line, silence_density)
        delay = (base * mult) / pace
        if delay > 0:
            time.sleep(delay)


def replay_cli(text: str, pace: float = 1.0, silence_density: float = 0.3) -> None:
    """CLI: print lines to stdout with pacing."""

    def on_line(char: str, line: str, i: int, total: int) -> None:
        print(f"{char}: {line}")
        sys.stdout.flush()

    replay(text, on_line, pace=pace, silence_density=silence_density)


def _parse_float_flag(flag: str, default: float) -> float:
    """Parse --flag value from sys.argv."""
    import sys
    try:
        i = sys.argv.index(flag)
        if i + 1 < len(sys.argv):
            return float(sys.argv[i + 1])
    except (ValueError, IndexError):
        pass
    return default


def main():
    """CLI: replay a saved version. python run_replay.py <scene_id> [version_id|latest] [--pace 1.0] [--silence 0.3]"""
    import sys
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))

    from engine.memory import load_version, list_versions

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    pace = _parse_float_flag("--pace", 1.0)
    silence = _parse_float_flag("--silence", 0.3)

    if not args:
        print("Usage: python run_replay.py <scene_id> [version_id|'latest'] [--pace 1.0] [--silence 0.3]", file=sys.stderr)
        sys.exit(1)

    scene_id = args[0]
    version_id = args[1] if len(args) > 1 else "latest"

    if version_id == "latest":
        versions = list_versions(scene_id)
        if not versions:
            print(f"No versions for {scene_id}", file=sys.stderr)
            sys.exit(1)
        version_id = versions[0]["version_id"]
        data = load_version(scene_id, version_id)
    else:
        data = load_version(scene_id, version_id)

    if not data:
        print(f"Version not found: {scene_id} / {version_id}", file=sys.stderr)
        sys.exit(1)

    text = data.get("text", "")
    silence_density = data.get("emotional_params", {}).get("silence_density", 0.3)
    replay_cli(text, pace=pace, silence_density=silence or silence_density)


if __name__ == "__main__":
    main()
