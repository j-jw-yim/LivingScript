# Architecture Overview

## Data Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  scripts/       │     │  engine/        │     │  data/          │
│  scenes/*.json  │────▶│  graph.py       │     │  versions/      │
│  characters/    │     │  Load, validate │     │  S1/*.json      │
│  prompts/       │     │  Traverse       │     │  Scene versions │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │  engine/generator.py    │
                    │  build_prompt()        │
                    │  call_model()          │
                    └────────────┬───────────┘
                                 │
                    ┌────────────┴───────────┐
                    │  engine/controls.py     │
                    │  ModulationParams      │
                    │  tension, distance,     │
                    │  silence_density        │
                    └───────────────────────┘
```

## Prompt Flow

```
Scene JSON                    ModulationParams
(beats, setting,              (sliders)
 constraints)
        │                            │
        └────────────┬──────────────┘
                     ▼
        ┌────────────────────────────┐
        │  scripts/prompts/           │
        │  base_scene.txt             │
        │  constraints.txt            │
        └────────────┬───────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │  Merged prompt               │
        │  (parameterized)             │
        └────────────┬───────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │  LLM (OpenAI-compatible)    │
        │  Returns raw dialogue       │
        └────────────┬───────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │  engine/memory.py           │
        │  save_version()             │
        │  text + metadata            │
        └────────────────────────────┘
```

## Control Loop (UI)

```
┌──────────────────────────────────────────────────────────────────┐
│                         React UI                                  │
├────────────┬─────────────────────────────┬───────────────────────┤
│ Scene Graph│  Script Panel                │  Control Panel         │
│            │                              │                        │
│ • Nodes    │  • Current dialogue          │  • Tension slider      │
│ • Edges    │  • Regenerated output        │  • Distance slider    │
│ • Click    │  • Diff highlight (future)   │  • Silence slider     │
│            │                              │  • Regenerate button   │
│ Version    │                              │  • Loading state      │
│ History    │                              │                        │
│ • List     │                              │                        │
│ • Restore  │                              │                        │
└─────┬──────┴─────────────┬────────────────┴───────────┬────────────┘
      │                    │                            │
      ▼                    ▼                            ▼
   /api/scenes        /api/versions               /api/generate
   /api/versions/:id  (GET full version)          (POST + modulation)
```

## Component Responsibilities

| Component    | Responsibility                              |
|-------------|---------------------------------------------|
| graph.py    | Load scenes, validate transitions, traverse |
| constraints | (in scene JSON) max_lines, no_exposition    |
| controls.py | Slider → prompt param mapping               |
| generator.py| Build prompt, call LLM, return dialogue      |
| memory.py   | Save/load versions with metadata            |
| diff.py     | Text diff, emotional shift detection        |
| replay.py   | Line-by-line playback, pace, silence        |
