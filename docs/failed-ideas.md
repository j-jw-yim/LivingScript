# Failed Ideas

A log of what didn't work and why. Design literacy in public.

---

## "Write a scene" — Naive Prompting Failure Modes

The simplest prompt — *"Write a scene where D and J argue in a kitchen"* — fails in predictable ways.

### Loss of subtext

Characters explain. They say "I'm angry" or "You never listen." The dialogue becomes exposition of emotion instead of *evidence* of it. The model defaults to clarity. Subtext requires constraint.

**Lesson:** You must explicitly forbid direct emotional language and require implication.

### Character collapse

Without voice notes, traits, or forbidden expressions, every character sounds the same. Grammatically correct, vaguely "human," but interchangeable. D and J blur into one voice.

**Lesson:** Character identity must be encoded as data and injected into the prompt. One-off prompting cannot sustain consistency.

### Beat drift

"Write a scene with small talk, deflection, and failed intimacy" — the model may hit one beat, gloss another, invent a fourth. Beats are suggestions, not requirements, unless you structure the prompt to enforce them.

**Lesson:** Beats must be enumerated, ordered, and marked as non-negotiable. Output validation (retry if beats missing) is the next step.

### Length explosion

Unconstrained, models tend to overwrite. A "short" scene becomes a page. Pacing is lost.

**Lesson:** Max-line constraints and explicit "brief" / "terse" instructions are required. Numbers beat adjectives.

---

## What we learned

- Constraints are not optional. They are the product.
- Prompt templates > ad-hoc strings. Version them. Parameterize them.
- Evaluation is part of the pipeline. Generate → validate → retry or reject.
