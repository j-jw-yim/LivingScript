"""
Constrained dialogue generation pipeline.
Merges scene + constraints → prompt, calls model, returns structured output.
"""

from typing import TYPE_CHECKING, Any, Optional

from engine.paths import PROMPTS_DIR
from engine.characters import load_characters_for_scene
from engine.validator import validate

if TYPE_CHECKING:
    from engine.controls import ModulationParams


def load_template(name: str) -> str:
    """Load a prompt template from scripts/prompts/."""
    path = PROMPTS_DIR / name
    return path.read_text(encoding="utf-8")


def format_constraints(
    scene: dict,
    emotional_intensity: float = 5.0,
    emotional_distance: float = 5.0,
    silence_density: float = 0.3,
    characters: Optional[list[dict]] = None,
) -> str:
    """Render the constraints block from scene + modulation params."""
    template = load_template("constraints.txt")
    constraints = scene.get("constraints", {})
    forbidden = list(constraints.get("forbidden_words", []))
    if characters:
        for c in characters:
            forbidden.extend(c.get("forbidden_expressions", []))
    forbidden_str = ", ".join(f'"{w}"' for w in forbidden) if forbidden else "none"
    return template.format(
        max_lines=constraints.get("max_lines", 10),
        emotional_intensity=emotional_intensity,
        emotional_distance=emotional_distance,
        silence_density=silence_density,
        subtext_over_text=constraints.get("subtext_over_text", True),
        no_exposition=constraints.get("no_exposition", True),
        forbidden_language=forbidden_str,
    )


def _format_character_voices(characters: list[dict]) -> str:
    """Format character voice notes and forbidden expressions."""
    if not characters:
        return ""
    lines = []
    for c in characters:
        name = c.get("name", c.get("character_id", "?"))
        voice = c.get("voice_notes", "")
        forbidden = c.get("forbidden_expressions", [])
        if voice:
            lines.append(f"- {name}: {voice}")
        if forbidden:
            lines.append(f"  Never says: {', '.join(forbidden)}")
    if not lines:
        return ""
    return "\n" + "\n".join(lines)


def build_prompt(
    scene: dict,
    emotional_intensity: float = 5.0,
    emotional_distance: float = 5.0,
    silence_density: float = 0.3,
    characters: Optional[list[dict]] = None,
) -> str:
    """Merge scene + constraints into full prompt."""
    if characters is None:
        characters = load_characters_for_scene(scene)
    template = load_template("base_scene.txt")
    constraints_block = format_constraints(
        scene, emotional_intensity, emotional_distance, silence_density, characters
    )
    character_voices = _format_character_voices(characters)
    return template.format(
        setting=scene.get("setting", ""),
        characters=", ".join(scene.get("characters", [])),
        character_voices=character_voices,
        beats="\n".join(f"- {b}" for b in scene.get("beats", [])),
        emotional_state=", ".join(scene.get("emotional_state", [])),
        constraints_block=constraints_block,
    )


def _mock_dialogue(scene: dict) -> str:
    """Return sample dialogue when no API key (demo mode)."""
    chars = scene.get("characters", ["D", "J"])
    beats = scene.get("beats", ["beat 1", "beat 2"])
    lines = []
    for i, beat in enumerate(beats[:4]):
        c = chars[i % len(chars)]
        lines.append(f"{c}: [Generated for '{beat}']")
    return "\n".join(lines)


def call_model(prompt: str, scene: dict | None = None, use_mock: bool = False) -> str:
    """
    Call LLM with prompt. Uses OpenAI-compatible API.
    Set OPENAI_API_KEY for real generation. If missing or use_mock=True, returns sample dialogue.
    """
    if use_mock and scene:
        return _mock_dialogue(scene)
    try:
        import os
        if not os.environ.get("OPENAI_API_KEY"):
            if scene:
                return _mock_dialogue(scene)
            return ""
        from openai import OpenAI
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        if scene:
            return _mock_dialogue(scene)
        raise RuntimeError(f"Model call failed: {e}") from e


def generate(
    scene: dict,
    modulation: Optional["ModulationParams"] = None,
    emotional_intensity: float = 5.0,
    emotional_distance: float = 5.0,
    silence_density: float = 0.3,
    dry_run: bool = False,
) -> dict[str, Any]:
    """
    Full pipeline: build prompt → call model → return structured output.
    Returns dict with prompt, dialogue, scene_id, emotional_params, constraints_snapshot.
    If dry_run=True, only builds prompt (no API call).
    modulation overrides individual intensity/distance/silence params.
    """
    if modulation:
        params = modulation.to_prompt_params()
        emotional_intensity = params["emotional_intensity"]
        emotional_distance = params["emotional_distance"]
        silence_density = params["silence_density"]

    characters = load_characters_for_scene(scene)
    prompt = build_prompt(
        scene, emotional_intensity, emotional_distance, silence_density, characters
    )

    if dry_run:
        return {
            "prompt": prompt,
            "dialogue": "",
            "scene_id": scene.get("scene_id", ""),
            "emotional_params": {},
            "constraints_snapshot": {},
        }

    max_retries = 3
    for attempt in range(max_retries):
        dialogue = call_model(prompt, scene=scene)
        validation = validate(dialogue, scene, characters)
        if validation["valid"] or attempt == max_retries - 1:
            break
        # Retry with tightened prompt hint
        prompt = prompt + f"\n\n[RETRY {attempt+2}/{max_retries}]: Previous output had issues: {'; '.join(validation['errors'])}. Please fix."

    if modulation:
        pp = modulation.to_prompt_params()
        emotional_params = {
            "tension": pp["emotional_intensity"] / 10,
            "emotional_distance": pp["emotional_distance"] / 10,
            "silence_density": pp["silence_density"],
        }
    else:
        emotional_params = {"tension": 0.5, "emotional_distance": 0.5, "silence_density": 0.3}
    constraints_snapshot = {
        "max_lines": scene.get("constraints", {}).get("max_lines", 10),
        "no_exposition": scene.get("constraints", {}).get("no_exposition", True),
        "subtext_over_text": scene.get("constraints", {}).get("subtext_over_text", True),
    }
    return {
        "prompt": prompt,
        "dialogue": dialogue,
        "scene_id": scene.get("scene_id", ""),
        "emotional_params": emotional_params,
        "constraints_snapshot": constraints_snapshot,
    }


def main():
    """CLI: generate dialogue for a scene.
    Usage: python run_generate.py [scene_id] [--dry-run] [--tension 0.7] [--distance 0.4] [--silence 0.5]
    """
    import sys
    from engine.graph import load_scenes
    from engine.controls import ModulationParams

    scenes = load_scenes()
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry_run = "--dry-run" in sys.argv

    def parse_float(flag: str, default: float) -> float:
        try:
            i = sys.argv.index(flag)
            if i + 1 < len(sys.argv):
                return float(sys.argv[i + 1])
        except (ValueError, IndexError):
            pass
        return default

    tension = parse_float("--tension", 0.5)
    distance = parse_float("--distance", 0.5)
    silence = parse_float("--silence", 0.3)
    modulation = ModulationParams(tension=tension, emotional_distance=distance, silence_density=silence)

    scene_id = args[0] if args else list(scenes.keys())[0]
    if scene_id not in scenes:
        print(f"Unknown scene: {scene_id}", file=sys.stderr)
        print(f"Available: {', '.join(scenes)}")
        sys.exit(1)

    scene = scenes[scene_id]
    result = generate(scene, modulation=modulation, dry_run=dry_run)
    if not dry_run and result.get("dialogue"):
        from engine.memory import save_version
        save_version(
            scene_id,
            result["dialogue"],
            result.get("constraints_snapshot", {}),
            result.get("emotional_params", {}),
        )
    if dry_run:
        print("=== PROMPT (dry run) ===")
        print(result["prompt"])
    else:
        print("=== DIALOGUE ===")
        print(result["dialogue"])


if __name__ == "__main__":
    main()
