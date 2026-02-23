"""
FastAPI backend for Living Script.
Serves scenes, generation, versions.
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from engine.graph import load_scenes
from engine.generator import build_prompt, generate
from engine.controls import ModulationParams
from engine.memory import save_version, load_version, list_versions
from engine.diff import text_diff, metadata_diff

app = FastAPI(title="Living Script API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/scenes")
def api_scenes():
    scenes = load_scenes()
    return list(scenes.values())


@app.get("/api/scenes/{scene_id}")
def api_scene(scene_id: str):
    scenes = load_scenes()
    if scene_id not in scenes:
        return {"error": "Scene not found"}
    return scenes[scene_id]


class GenerateRequest(BaseModel):
    scene_id: str
    tension: float = 0.5
    emotional_distance: float = 0.5
    silence_density: float = 0.3


@app.post("/api/generate")
def api_generate(req: GenerateRequest):
    scenes = load_scenes()
    if req.scene_id not in scenes:
        return {"error": "Scene not found"}
    scene = scenes[req.scene_id]
    modulation = ModulationParams(
        tension=req.tension,
        emotional_distance=req.emotional_distance,
        silence_density=req.silence_density,
    )
    try:
        result = generate(scene, modulation=modulation, dry_run=False)
        if result.get("dialogue"):
            save_version(
                req.scene_id,
                result["dialogue"],
                result.get("constraints_snapshot", {}),
                result.get("emotional_params", {}),
            )
        return result
    except Exception as e:
        return {"error": str(e), "dialogue": ""}


@app.get("/api/versions/{scene_id}")
def api_versions(scene_id: str):
    return list_versions(scene_id)


@app.get("/api/versions/{scene_id}/{version_id}")
def api_version(scene_id: str, version_id: str):
    v = load_version(scene_id, version_id)
    if not v:
        return {"error": "Version not found"}
    return v


class DiffRequest(BaseModel):
    scene_id: str
    old_version_id: str
    new_version_id: str


@app.post("/api/diff")
def api_diff(req: DiffRequest):
    """Return text diff and metadata diff between two versions."""
    old_v = load_version(req.scene_id, req.old_version_id)
    new_v = load_version(req.scene_id, req.new_version_id)
    if not old_v or not new_v:
        return {"error": "Version not found"}
    text_diffs = text_diff(old_v.get("text", ""), new_v.get("text", ""))
    meta = metadata_diff(old_v, new_v)
    return {"text_diff": text_diffs, "metadata_diff": meta}
