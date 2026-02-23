import React, { useState, useRef, useEffect } from 'react'

const LINE_PATTERN = /^([A-Za-z0-9_]+):\s*(.+)$/

function parseDialogue(text) {
  if (!text || !text.trim()) return []
  return text
    .trim()
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
    .map((line) => {
      const m = line.match(LINE_PATTERN)
      return m ? { char: m[1], line: m[2] } : { char: '?', line }
    })
}

export default function ReplayPanel({ dialogue, silenceDensity = 0.3, onClose }) {
  const [lines, setLines] = useState([])
  const [currentIndex, setCurrentIndex] = useState(-1)
  const [isPlaying, setIsPlaying] = useState(false)
  const [pace, setPace] = useState(1)
  const timerRef = useRef(null)

  useEffect(() => {
    setLines(parseDialogue(dialogue))
    setCurrentIndex(-1)
    setIsPlaying(false)
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current)
    }
  }, [dialogue])

  const baseDuration = (line) => Math.max(1.5, (line.split(/\s+/).length / 120) * 60)
  const silenceMult = (line) => {
    let m = 1
    if (line.length < 10) m += silenceDensity * 1.5
    if (line.trimEnd().endsWith('...')) m += silenceDensity * 2
    return m
  }

  const playNext = (index) => {
    if (index >= lines.length) {
      setIsPlaying(false)
      return
    }
    setCurrentIndex(index)
    const { line } = lines[index]
    const delay = (baseDuration(line) * silenceMult(line)) / pace
    timerRef.current = setTimeout(() => playNext(index + 1), delay * 1000)
  }

  const handlePlay = () => {
    if (isPlaying) {
      if (timerRef.current) clearTimeout(timerRef.current)
      setIsPlaying(false)
      return
    }
    if (timerRef.current) clearTimeout(timerRef.current)
    setIsPlaying(true)
    playNext(0)
  }

  const handleStop = () => {
    if (timerRef.current) clearTimeout(timerRef.current)
    setIsPlaying(false)
    setCurrentIndex(-1)
  }

  if (!dialogue) return null

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50" onClick={onClose}>
      <div
        className="bg-stone-900 rounded-lg p-6 max-w-lg w-full mx-4 border border-stone-700"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-medium">Replay</h3>
          <button
            onClick={onClose}
            className="text-stone-400 hover:text-stone-200 text-2xl leading-none"
          >
            ×
          </button>
        </div>
        <div className="min-h-[120px] font-mono text-lg mb-4">
          {currentIndex >= 0 && lines[currentIndex] ? (
            <div>
              <span className="text-amber-400">{lines[currentIndex].char}:</span>{' '}
              {lines[currentIndex].line}
            </div>
          ) : (
            <span className="text-stone-500 italic">Press Play</span>
          )}
        </div>
        <div className="flex gap-2 items-center">
          <label className="text-sm text-stone-500">Pace</label>
          <input
            type="range"
            min="0.5"
            max="2"
            step="0.1"
            value={pace}
            onChange={(e) => setPace(parseFloat(e.target.value))}
            className="flex-1 accent-amber-600"
          />
          <span className="text-xs text-stone-500">{pace.toFixed(1)}x</span>
        </div>
        <div className="flex gap-2 mt-4">
          <button
            onClick={handlePlay}
            className="flex-1 py-2 rounded bg-amber-600 hover:bg-amber-500 text-stone-950 font-medium"
          >
            {isPlaying ? 'Pause' : 'Play'}
          </button>
          <button
            onClick={handleStop}
            className="py-2 px-4 rounded bg-stone-700 hover:bg-stone-600"
          >
            Stop
          </button>
        </div>
      </div>
    </div>
  )
}
