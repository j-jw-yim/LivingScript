import React from 'react'
import SceneGraph from './components/SceneGraph'
import ScriptPanel from './components/ScriptPanel'
import ControlPanel from './components/ControlPanel'
import VersionHistory from './components/VersionHistory'
import ReplayPanel from './components/ReplayPanel'

export default function App() {
  const [selectedScene, setSelectedScene] = React.useState(null)
  const [dialogue, setDialogue] = React.useState('')
  const [pathHistory, setPathHistory] = React.useState([])
  const [selectedVersion, setSelectedVersion] = React.useState(null)
  const [compareVersion, setCompareVersion] = React.useState(null)
  const [diffData, setDiffData] = React.useState(null)
  const [versionRefresh, setVersionRefresh] = React.useState(0)
  const [showReplay, setShowReplay] = React.useState(false)
  const [silenceDensity, setSilenceDensity] = React.useState(0.3)

  const handleSelectScene = (scene) => {
    setSelectedScene(scene)
    setPathHistory((prev) => {
      const ids = prev.map((s) => (typeof s === 'string' ? s : s?.scene_id))
      if (ids.includes(scene?.scene_id)) return prev
      return [...prev, scene]
    })
  }

  const handleRegenerate = (result) => {
    if (result?.dialogue) setDialogue(result.dialogue)
    setSilenceDensity(result?.emotional_params?.silence_density ?? 0.3)
    setVersionRefresh((v) => v + 1)
    setDiffData(null)
  }

  return (
    <div className="h-screen flex flex-col bg-stone-950 text-stone-200">
      <header className="flex-none px-4 py-2 border-b border-stone-700">
        <h1 className="text-xl font-medium">Living Script</h1>
      </header>
      <div className="flex-1 flex min-h-0">
        {/* Left: Graph + Version history */}
        <aside className="w-80 flex flex-col border-r border-stone-700 overflow-hidden">
          <div className="flex-1 min-h-0 overflow-auto p-3">
            <h2 className="text-sm font-medium text-stone-400 mb-2">Scene Graph</h2>
            <SceneGraph
              selectedScene={selectedScene}
              onSelectScene={handleSelectScene}
              pathHistory={pathHistory}
            />
          </div>
          <div className="flex-none border-t border-stone-700 overflow-hidden" style={{ height: '180px' }}>
            <VersionHistory
              sceneId={selectedScene?.scene_id}
              selectedVersion={selectedVersion}
              compareVersion={compareVersion}
              onSelectVersion={async (v) => {
                setSelectedVersion(v)
                setCompareVersion(null)
                setDiffData(null)
                if (v?.version_id && selectedScene?.scene_id) {
                  const res = await fetch(`/api/versions/${selectedScene.scene_id}/${v.version_id}`)
                  const data = await res.json()
                  if (data?.text) setDialogue(data.text)
                }
              }}
              onCompareVersion={async (oldId, newId) => {
                if (!oldId || !newId || !selectedScene?.scene_id) return
                const res = await fetch('/api/diff', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    scene_id: selectedScene.scene_id,
                    old_version_id: oldId,
                    new_version_id: newId,
                  }),
                })
                const data = await res.json()
                setDiffData(data)
              }}
              onClearDiff={() => setDiffData(null)}
              setCompareVersion={setCompareVersion}
              refreshTrigger={versionRefresh}
            />
          </div>
        </aside>
        {/* Center: Script text */}
        <main className="flex-1 overflow-auto p-6">
          <ScriptPanel
            scene={selectedScene}
            dialogue={dialogue}
            diffData={diffData}
            onDialogueChange={setDialogue}
          />
        </main>
        {/* Right: Controls */}
        <aside className="w-72 flex-none border-l border-stone-700 p-4 overflow-auto">
          <ControlPanel
            scene={selectedScene}
            onRegenerate={handleRegenerate}
            onReplay={() => setShowReplay(true)}
            hasDialogue={!!dialogue}
          />
        </aside>
      </div>
      {showReplay && (
        <ReplayPanel
          dialogue={dialogue}
          silenceDensity={silenceDensity}
          onClose={() => setShowReplay(false)}
        />
      )}
    </div>
  )
}
