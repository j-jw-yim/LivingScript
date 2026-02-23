"""
Regeneration controls for emotional modulation.
Sliders map to prompt parameters that transform generation.
"""

from dataclasses import dataclass


@dataclass
class ModulationParams:
    """
    Emotional modulation sliders.
    All values 0–1 or 1–10 depending on semantic (see docstrings).
    """
    tension: float = 0.5          # 0–1; higher = more dramatic, sharper beats
    emotional_distance: float = 0.5  # 0–1; higher = more guarded, less direct
    silence_density: float = 0.3   # 0–1; higher = more pauses, fewer lines

    def to_prompt_params(self) -> dict:
        """
        Convert slider values to generator parameters.
        tension → emotional_intensity (1–10)
        emotional_distance → emotional_distance (1–10, inverted for 'distance')
        silence_density → silence_density (0–1)
        """
        return {
            "emotional_intensity": 1 + self.tension * 9,  # 0–1 → 1–10
            "emotional_distance": 1 + self.emotional_distance * 9,  # 0–1 → 1–10
            "silence_density": self.silence_density,
        }
