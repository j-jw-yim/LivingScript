# Living Script

Most LLM writing tools give you a prompt box and hope. You get slop, or you get something good and have no idea how to repeat it. The problem isn't the model. It's the lack of structure and control.

Living Script treats the script as data. Scenes are nodes in a graph. Each has beats, emotional register, and constraints. You don't prompt. You conduct. Sliders control tension, distance, and silence. Regenerate keeps the structure and rewrites the dialogue. Version history lets you compare, restore, and see what actually changed when you moved a knob.

![Living Script](https://raw.githubusercontent.com/j-jw-yim/LivingScript/main/demo.png)

---

## Prerequisites

- Python 3.10+
- Node.js 18+
- (Optional) OpenAI API key for real generation. Without it, demo mode uses sample dialogue.

---

## Run

```bash
./run.sh
```

Opens backend on port 8000 and frontend on port 5173. Visit http://localhost:5173.

**First time?** The script installs Python and Node dependencies if needed.

**Port already in use?** Run in two terminals:

```bash
# Terminal 1
python3 run_server.py

# Terminal 2
cd ui && npm install && npm run dev
```

**Real generation:** Copy `.env.example` to `.env` and add your `OPENAI_API_KEY`. Without it, Regenerate returns sample dialogue so you can explore the UI.

---

## What You See

| Panel | Purpose |
|-------|---------|
| **Left: Scene graph** | Click a node to load a scene. Edges show transitions. Your path is highlighted. |
| **Center: Script** | Current dialogue. If you ran Diff, shows added/removed lines. |
| **Right: Controls** | Tension, emotional distance, silence density. Regenerate button. Replay (line-by-line playback). |

**Version history** (below the graph): List of past generations. Click to restore. Use Compare (From/To + Diff) to see what changed between versions and how the emotional params shifted.

---

## CLI

```bash
python3 run_graph.py S3              # Show valid next scenes from S3
python3 run_generate.py S1 --dry-run # Preview the prompt (no API call)
python3 run_generate.py S1           # Generate dialogue (saves version)
python3 run_generate.py S1 --tension 0.8 --silence 0.5
python3 run_replay.py S1 latest      # Line-by-line playback (uses saved version)
python3 run_replay.py S1 latest --pace 1.5
```

---

## Extending It

- **Scenes:** Add JSON files to `scripts/scenes/`. Follow `scripts/scenes/schema.json`. Include `scene_id`, `setting`, `emotional_state`, `characters`, `beats`, `transitions`.
- **Characters:** Add JSON to `scripts/characters/`. Include `character_id`, `name`, `voice_notes`, `forbidden_expressions`. Used for prompt injection.
- **Prompts:** Edit `scripts/prompts/base_scene.txt` and `constraints.txt`. Placeholders: `{setting}`, `{beats}`, `{character_voices}`, etc.

---

## Troubleshooting

- **Backend won't start (port 8000 in use):** `lsof -ti:8000 | xargs kill -9`, then try again.
- **UI proxy errors:** Ensure the backend is running first. The UI proxies `/api` to localhost:8000.
- **Image not loading in README:** The demo screenshot uses a raw GitHub URL. If you fork, update the image path in the README.

---

## Built

React, Tailwind, FastAPI, Python. Constraint-first prompting, validation with retry, character voice injection, semantic versioning with metadata.

- [Architecture](docs/architecture.md) — data flow, prompt flow, control loop
- [Design philosophy](docs/design-philosophy.md) — why scripts as graphs, constraints over free generation
- [Postmortem](docs/postmortem.md) — what worked, what didn't, what I'd rebuild
- [Failed ideas](docs/failed-ideas.md) — why naive prompting collapses

---

MIT
