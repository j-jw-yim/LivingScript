import React, { useEffect, useState, useMemo } from 'react'

export default function SceneGraph({ selectedScene, onSelectScene, pathHistory }) {
  const [scenes, setScenes] = useState([])

  useEffect(() => {
    fetch('/api/scenes')
      .then((r) => r.json())
      .then(setScenes)
      .catch(() => setScenes([]))
  }, [])

  const selectedId = selectedScene?.scene_id
  const pathSet = new Set(pathHistory?.map((s) => s?.scene_id || s) || [])

  // Build edges from transitions
  const edges = useMemo(() => {
    const out = []
    for (const s of scenes) {
      for (const t of s.transitions || []) {
        if (t.target) out.push({ from: s.scene_id, to: t.target, type: t.type })
      }
    }
    return out
  }, [scenes])

  // Simple grid layout: 3 columns
  const layout = useMemo(() => {
    const positions = {}
    scenes.forEach((s, i) => {
      const row = Math.floor(i / 3)
      const col = i % 3
      positions[s.scene_id] = { x: col * 70 + 45, y: row * 55 + 35 }
    })
    return positions
  }, [scenes])

  const nodeRadius = 22

  return (
    <div className="overflow-auto">
      <svg
        viewBox="0 0 220 280"
        className="w-full min-h-[200px]"
        style={{ overflow: 'visible' }}
      >
        {/* Edges */}
        <g stroke="currentColor" strokeOpacity="0.3" fill="none">
          {edges.map((e, i) => {
            const from = layout[e.from]
            const to = layout[e.to]
            if (!from || !to) return null
            const dx = to.x - from.x
            const dy = to.y - from.y
            const len = Math.sqrt(dx * dx + dy * dy) || 1
            const ux = dx / len
            const uy = dy / len
            const startX = from.x + ux * nodeRadius
            const startY = from.y + uy * nodeRadius
            const endX = to.x - ux * nodeRadius
            const endY = to.y - uy * nodeRadius
            const midX = (startX + endX) / 2
            const midY = (startY + endY) / 2
            const inPath = pathSet.has(e.from) && pathSet.has(e.to)
            return (
              <path
                key={i}
                d={`M ${startX} ${startY} Q ${midX + uy * 15} ${midY - ux * 15} ${endX} ${endY}`}
                strokeWidth={inPath ? 2 : 1}
                strokeOpacity={inPath ? 0.6 : 0.3}
              />
            )
          })}
        </g>
        {/* Nodes */}
        {scenes.map((scene) => {
          const pos = layout[scene.scene_id]
          if (!pos) return null
          const isSelected = scene.scene_id === selectedId
          const inPath = pathSet.has(scene.scene_id)
          return (
            <g
              key={scene.scene_id}
              cursor="pointer"
              onClick={() => onSelectScene(scene)}
            >
              <circle
                cx={pos.x}
                cy={pos.y}
                r={nodeRadius}
                fill={isSelected ? 'rgb(217 119 6 / 0.4)' : inPath ? 'rgb(68 64 60)' : 'rgb(41 37 36)'}
                stroke={isSelected ? 'rgb(245 158 11)' : 'rgb(87 83 78)'}
                strokeWidth={isSelected ? 2 : 1}
              />
              <text
                x={pos.x}
                y={pos.y}
                textAnchor="middle"
                dominantBaseline="middle"
                fill="rgb(231 229 228)"
                fontSize="11"
              >
                {scene.scene_id}
              </text>
            </g>
          )
        })}
      </svg>
    </div>
  )
}
