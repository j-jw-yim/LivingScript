"""Living Script engine — graph, controls, generator, memory, diff, replay."""

from engine.graph import load_scenes, validate_transitions, get_next_scenes, traverse
from engine.controls import ModulationParams
from engine.generator import build_prompt, generate, call_model
from engine.memory import save_version, load_version, list_versions
from engine.diff import text_diff, changed_lines, emotional_shift, metadata_diff, unified_diff_text
from engine.replay import parse_dialogue, replay, replay_cli

__all__ = [
    "load_scenes",
    "validate_transitions",
    "get_next_scenes",
    "traverse",
    "ModulationParams",
    "build_prompt",
    "generate",
    "call_model",
    "save_version",
    "load_version",
    "list_versions",
    "text_diff",
    "changed_lines",
    "emotional_shift",
    "metadata_diff",
    "unified_diff_text",
    "parse_dialogue",
    "replay",
    "replay_cli",
]
