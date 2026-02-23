import React from 'react'

export default function DiffView({ diff, metadataDiff }) {
  if (!diff || !Array.isArray(diff)) return null

  return (
    <div className="space-y-4">
      <div className="font-mono text-sm space-y-0">
        {diff.map((hunk, i) => (
          <div
            key={i}
            className={`px-2 py-0.5 ${
              hunk.type === 'added'
                ? 'bg-green-900/30 text-green-200'
                : hunk.type === 'removed'
                ? 'bg-red-900/30 text-red-200'
                : 'text-stone-500'
            }`}
          >
            {hunk.type === 'added' && '+'}
            {hunk.type === 'removed' && '-'}
            {hunk.lines?.map((line, j) => (
              <div key={j}>{line}</div>
            ))}
          </div>
        ))}
      </div>
      {metadataDiff?.emotional_shift?.length > 0 && (
        <div className="text-xs text-stone-400 border-t border-stone-700 pt-2">
          <div className="font-medium mb-1">Emotional shifts</div>
          {metadataDiff.emotional_shift.map((s, i) =>
            s.direction !== 'same' ? (
              <div key={i}>
                {s.param}: {s.old?.toFixed(2)} → {s.new?.toFixed(2)} ({s.direction})
              </div>
            ) : null
          )}
        </div>
      )}
    </div>
  )
}
