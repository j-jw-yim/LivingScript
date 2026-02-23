import React, { useEffect, useState } from 'react'

export default function VersionHistory({
  sceneId,
  selectedVersion,
  compareVersion,
  onSelectVersion,
  onCompareVersion,
  onClearDiff,
  setCompareVersion,
  refreshTrigger,
}) {
  const [versions, setVersions] = useState([])
  const [compareFrom, setCompareFrom] = useState(null)
  const [compareTo, setCompareTo] = useState(null)

  useEffect(() => {
    if (!sceneId) return
    fetch(`/api/versions/${sceneId}`)
      .then((r) => r.json())
      .then(setVersions)
      .catch(() => setVersions([]))
  }, [sceneId, refreshTrigger])

  if (!sceneId) {
    return (
      <div className="p-3 text-stone-500 text-sm">
        Select a scene for version history.
      </div>
    )
  }

  const list = Array.isArray(versions) ? versions : []
  const canCompare = list.length >= 2 && compareFrom && compareTo && compareFrom !== compareTo

  return (
    <div className="p-3 overflow-auto h-full">
      <h2 className="text-sm font-medium text-stone-400 mb-2">Versions</h2>
      <div className="space-y-1 mb-2">
        {list.length === 0 ? (
          <p className="text-stone-500 text-xs italic">No versions yet</p>
        ) : (
          list.map((v) => (
            <button
              key={v.version_id || v.timestamp}
              onClick={() => onSelectVersion(v)}
              className={`w-full text-left px-2 py-1.5 rounded text-xs ${
                selectedVersion?.version_id === v.version_id
                  ? 'bg-amber-600/30 text-amber-200'
                  : 'text-stone-500 hover:bg-stone-800 hover:text-stone-300'
              }`}
            >
              {v.timestamp?.slice(0, 19) || v.version_id || 'Unknown'}
            </button>
          ))
        )}
      </div>
      {list.length >= 2 && (
        <div className="border-t border-stone-700 pt-2 space-y-1">
          <div className="text-xs text-stone-500 mb-1">Compare</div>
          <select
            className="w-full bg-stone-800 rounded px-1 py-0.5 text-xs mb-1"
            value={compareFrom || ''}
            onChange={(e) => setCompareFrom(e.target.value || null)}
          >
            <option value="">From...</option>
            {list.map((v) => (
              <option key={v.version_id} value={v.version_id}>
                {v.timestamp?.slice(11, 19)}
              </option>
            ))}
          </select>
          <select
            className="w-full bg-stone-800 rounded px-1 py-0.5 text-xs mb-1"
            value={compareTo || ''}
            onChange={(e) => setCompareTo(e.target.value || null)}
          >
            <option value="">To...</option>
            {list.map((v) => (
              <option key={v.version_id} value={v.version_id}>
                {v.timestamp?.slice(11, 19)}
              </option>
            ))}
          </select>
          <div className="flex gap-1">
            <button
              onClick={() => canCompare && onCompareVersion?.(compareFrom, compareTo)}
              disabled={!canCompare}
              className="flex-1 py-1 rounded bg-stone-700 hover:bg-stone-600 disabled:opacity-50 text-xs"
            >
              Diff
            </button>
            <button
              onClick={() => { setCompareFrom(null); setCompareTo(null); onClearDiff?.(); }}
              className="py-1 px-2 rounded bg-stone-700 hover:bg-stone-600 text-xs"
            >
              Clear
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
