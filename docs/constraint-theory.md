# Constraint Theory

## Beats Are Sacred

A beat is a discrete narrative unit: a moment of action, revelation, or shift. "Small talk" → "deflection" → "failed intimacy." Beats are the skeleton; dialogue is the flesh.

In Living Script, **beats are not optional**. When you regenerate a scene, the beats are preserved. The model may rephrase, compress, or expand, but each beat must land. If regeneration drops a beat, the output is invalid.

This reflects a core principle: **structure precedes prose**. You decide what happens; the AI decides how it sounds. Beats anchor the human's intent so the model cannot drift into irrelevant territory.

---

## Emotion ≠ Explicit Language

"Subtext > text." Characters rarely say what they feel. "I'm angry" is weak. A slammed door, a clipped reply, a refusal to make eye contact — that's the work.

Living Script constrains *how* emotion is expressed, not *that* it's expressed. You can set:

- `"no exposition"` — no characters explaining their feelings
- `"subtext > text"` — implication over declaration
- `"silence density": 0.3` — more pauses, fewer words

The emotional state of a scene (e.g., `["avoidant", "tense"]`) informs the *register*, not the vocabulary. The model is prompted to evoke those states through behavior, rhythm, and omission — not through emotional labels.

This produces dialogue that feels earned. The audience infers. The script doesn't explain.
