import React from 'react'
import DiffView from './DiffView'

export default function ScriptPanel({ scene, dialogue, diffData, onDialogueChange }) {
  if (!scene) {
    return (
      <div className="text-stone-500 italic">
        Select a scene from the graph to load or generate dialogue.
      </div>
    )
  }

  return (
    <div>
      <div className="mb-4">
        <h2 className="text-lg font-medium">{scene.scene_id}</h2>
        <p className="text-sm text-stone-400">{scene.setting}</p>
        <p className="text-xs text-stone-500 mt-1">
          {scene.emotional_state?.join(', ')}
        </p>
      </div>
      {diffData?.text_diff ? (
        <div className="space-y-2">
          <div className="text-xs text-stone-500">Version diff (old → new)</div>
          <DiffView diff={diffData.text_diff} metadataDiff={diffData.metadata_diff} />
        </div>
      ) : (
        <div className="font-mono text-sm whitespace-pre-wrap bg-stone-900/50 rounded p-4 min-h-[200px]">
          {dialogue || (
            <span className="text-stone-500 italic">
              No dialogue yet. Use Regenerate to generate.
            </span>
          )}
        </div>
      )}
    </div>
  )
}
