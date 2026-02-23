# Living Script

Most LLM writing tools give you a prompt box and hope. You get slop, or you get something good and have no idea how to repeat it. The problem isn't the model. It's the lack of structure and control.

Living Script treats the script as data. Scenes are nodes in a graph. Each has beats, emotional register, and constraints. You don't prompt. You conduct. Sliders control tension, distance, and silence. Regenerate keeps the structure and rewrites the dialogue. Version history lets you compare, restore, and see what actually changed when you moved a knob.

![Living Script](https://raw.githubusercontent.com/j-jw-yim/LivingScript/main/demo.png)

---

## Run

```bash
./run.sh
```

http://localhost:5173. Demo mode works without an API key. For real generation, set `OPENAI_API_KEY` in `.env`.

If the script fails: `python3 run_server.py` in one terminal, `cd ui && npm run dev` in another.

---

## Flow

Graph on the left. Click a scene. Adjust sliders. Regenerate. Compare versions. Replay line by line. CLI: `run_graph.py`, `run_generate.py`, `run_replay.py`.

---

## Built

React, Tailwind, FastAPI, Python. Constraint-first prompting, validation with retry, character voice injection, semantic versioning with metadata. [Architecture](docs/architecture.md). [Design philosophy](docs/design-philosophy.md). [Postmortem](docs/postmortem.md): what worked, what didn't, what I'd rebuild. [Failed ideas](docs/failed-ideas.md): why naive prompting collapses.

---

MIT

