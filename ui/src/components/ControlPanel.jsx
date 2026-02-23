import React, { useState } from 'react'

export default function ControlPanel({ scene, onRegenerate, onReplay, hasDialogue }) {
  const [tension, setTension] = useState(0.5)
  const [distance, setDistance] = useState(0.5)
  const [silence, setSilence] = useState(0.3)
  const [loading, setLoading] = useState(false)

  const handleRegenerate = async () => {
    if (!scene) return
    setLoading(true)
    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          scene_id: scene.scene_id,
          tension,
          emotional_distance: distance,
          silence_density: silence,
        }),
      })
      const data = await res.json()
      onRegenerate?.(data)
    } catch (e) {
      console.error(e)
      onRegenerate?.(null)
    } finally {
      setLoading(false)
    }
  }

  if (!scene) {
    return (
      <div className="text-stone-500 text-sm">
        Select a scene to access controls.
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <h2 className="text-sm font-medium text-stone-400">Modulation</h2>
      <div>
        <label className="text-xs text-stone-500">Tension</label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.05"
          value={tension}
          onChange={(e) => setTension(parseFloat(e.target.value))}
          className="w-full accent-amber-600"
        />
      </div>
      <div>
        <label className="text-xs text-stone-500">Emotional distance</label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.05"
          value={distance}
          onChange={(e) => setDistance(parseFloat(e.target.value))}
          className="w-full accent-amber-600"
        />
      </div>
      <div>
        <label className="text-xs text-stone-500">Silence density</label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.05"
          value={silence}
          onChange={(e) => setSilence(parseFloat(e.target.value))}
          className="w-full accent-amber-600"
        />
      </div>
      <button
        onClick={handleRegenerate}
        disabled={loading}
        className="w-full py-2 px-4 rounded bg-amber-600 hover:bg-amber-500 disabled:opacity-50 text-stone-950 font-medium text-sm"
      >
        {loading ? 'Generating…' : 'Regenerate'}
      </button>
      {hasDialogue && (
        <button
          onClick={() => onReplay?.()}
          className="w-full py-2 px-4 rounded bg-stone-700 hover:bg-stone-600 text-sm mt-2"
        >
          Replay
        </button>
      )}
    </div>
  )
}
