# Design Philosophy

## Scripts as Graphs, Not Documents

A traditional script is a linear document: Scene 1 → Scene 2 → Scene 3. You scroll. You search. The structure is implicit in the page order.

Living Script inverts this. The script is a **graph of scenes** — nodes connected by emotional transitions, thematic continuities, and user-driven choices. Each scene is a first-class object with:

- **Setting** — where and when
- **Emotional state** — the affective register (avoidant, tense, tender)
- **Characters** — who is present
- **Beats** — the narrative units that must land
- **Constraints** — the rules that govern generation

Scenes connect not by sequence alone but by *relationship*. Two scenes can share an emotional arc. A branch can diverge on a choice. You navigate the story by traversing the graph, not by scrolling a page.

This shift enables:

- **Branching** — multiple futures from a single node
- **Remix** — reassemble the same beats in different emotional keys
- **Inspection** — see the whole structure at once, not buried in prose

---

## Constraints Over Free Generation

"Write a scene" is a weak prompt. It invites the model to do whatever it wants. The result is often generic, emotionally flat, or tonally inconsistent.

Living Script is **constraint-first**. Instead of "write a scene," you say:

> Rewrite Scene S3, preserving beats and emotional arc, increasing tension by 15%, keeping dialogue under 8 lines, and avoiding direct emotional language.

You lock what matters (beats, structure) and tune the rest (intensity, density, clarity). The LLM fills in the texture within guardrails.

Why this matters:

- **Control** — You steer. The model executes.
- **Repeatability** — Same constraints → comparable outputs. You can iterate.
- **Co-creation** — The human defines the game; the AI plays it. Both contribute.

We do not treat the LLM as an autonomous author. We treat it as an instrument you play.
