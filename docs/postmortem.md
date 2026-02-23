# Postmortem: What I Would Rebuild Differently

A reflective look at what worked, what didn't, and what I'd change if starting over.

---

## Constraints That Worked

### Structural constraints

- **Beats as required units** — Telling the model "these beats must appear in order" significantly reduced drift. The model sometimes compressed or rephrased, but rarely invented new plot points.
- **Max lines** — Enforcing a line limit kept scenes tight. Without it, output ballooned. Numbers beat adjectives.
- **No exposition** — Explicitly forbidding "characters explain their feelings" pushed the model toward behavior and subtext. This was one of the highest-leverage constraints.

### Emotional modulation

- **Tension / intensity slider** — Mapped cleanly to prompt language ("higher tension", "sharper beats"). Noticeable effect on output.
- **Silence density** — Harder for the model to "obey" literally (it can't add stage directions), but the instruction to favor shorter lines and pauses did shift rhythm. Replay mode uses it for actual pacing.

### Data design

- **Scene-as-node with transitions** — The graph model was right. Scenes as first-class objects with explicit edges made branching and traversal trivial.
- **Version storage with metadata** — Storing emotional_params and constraints alongside text made diffing and "why did this change?" queries possible.

---

## Constraints That Didn't

### Forbidden words / expressions

- **Character-level forbidden_expressions** — We defined them in the schema but never wired them into the prompt. Even when added, models often found synonyms. "Never say X" is easy to circumvent.
- **Scene-level forbidden_words** — Same. The model sometimes avoided the exact string but used equivalent phrasing. Constraint was weak.

### Subtext-over-text

- **Boolean flag** — We had `subtext_over_text: true` in constraints. The prompt said "subtext over explicit language." Effect was inconsistent. Some runs were beautifully indirect; others still produced "I can't do this anymore." The instruction was too vague. Concrete examples would help: "Instead of 'I'm angry,' show anger through action or refusal to speak."

### Emotional distance

- **Slider semantics** — "Higher = more guarded" is fuzzy. We mapped it to prompt language like "characters hold back, avoid direct statements." Sometimes it worked; often it didn't. The model doesn't have a calibrated notion of "guardness." Might need negative examples: "Avoid phrases like…"

---

## What I Would Rebuild Differently

### 1. Prompt design: examples over rules

Instead of "no exposition" and "subtext over text," I'd provide 2–3 before/after pairs:

```
BAD:  D: I'm upset that you never listen.
GOOD: D: [Looks away. Says nothing for a beat.]
```

Rules are easy to ignore. Examples anchor the model.

### 2. Validation loop, not just prompting

We never implemented "regenerate if constraints violated." The pipeline was: prompt → model → return. I'd add a validator that checks beats, line count, forbidden patterns, and retries (with tightened prompt) up to N times. Generation and validation as separate, testable steps.

### 3. Character voice as injected context

We have `voice_notes` and `forbidden_expressions` in character JSON but never reliably injected them. I'd make character loading a first-class step: each scene load pulls in its characters and prepends their voice notes to the prompt. Version that too.

### 4. Diff in the UI

We built `engine/diff.py` (text_diff, emotional_shift) but the UI never uses it. Side-by-side version comparison with highlighted changes would make "what changed when I moved the tension slider?" visible. High value, low effort.

### 5. Replay as a first-class feature

Replay is CLI-only. I'd add an in-browser replay: line-by-line reveal, optional TTS, pacing from silence_density. "Performance energy without performance space" was a core promise; we built the engine but not the stage.

### 6. Path tracking in the graph

We have `pathHistory` in the UI but never populate it. Clicking through the graph should record the path (S1 → S3 → S5) and highlight it. Would make "where am I in the story?" obvious.

---

## Ethical & Creative Reflections

### Co-authorship and labor

The human sets structure; the model fills texture. That framing is useful but incomplete. The model also *proposes* structure—it chooses which beat to emphasize, which line to cut. The human approves or rejects. Who did the work? Both. The tool should make that visible: "Model suggested X; you chose Y." Attribution supports honest reflection.

### Constraint as creative fuel

Paradoxically, constraints increased creative output. "Write a scene" produces generic mush. "Write a scene with these three beats, under 8 lines, no one explains their feelings" produces something to react to. The constraints are the brief. I'd lean into that: position the system as "constraint-first authoring," not "AI writing assistant."

### Local-first and sovereignty

We kept it local: no cloud, your data, your API key. That choice matters. The script—your script—never leaves your machine unless you choose to share it. For personal, vulnerable work, that's a feature. I'd document this explicitly: "Your words stay yours."

### When the model fails

Sometimes the output is bland, out of character, or constraint-violating. The current UX is "regenerate and hope." I'd add: "Mark this as bad." A simple thumbs-down that could (in a future version) feed into fine-tuning or prompt refinement. Treating failure as data, not noise.

---

## Summary

| Worked | Didn't | Rebuild |
|--------|--------|---------|
| Beats, max lines, no exposition | Forbidden words, vague subtext rules | Examples over rules |
| Tension/silence sliders | Emotional distance semantics | Validation loop |
| Graph as data, version metadata | — | Character voice injection, diff in UI |
| — | — | Replay in browser, path tracking |

The core insight holds: **constraint-first co-creation works when constraints are concrete and enforced.** The rest is iteration.
