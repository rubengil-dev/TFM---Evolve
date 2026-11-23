/** Root of the app: keeps the user's choices and decides which screen to show. */

import { useState } from 'react'
import CellBackground from './components/CellBackground'
import WarningBar from './components/WarningBar'
import Landing from './pages/Landing'
import type { Mode } from './types'

type Upload = { mode: Mode; file: File }

export default function App() {
  const [upload, setUpload] = useState<Upload | null>(null)

  return (
    <>
      <CellBackground />
      {upload === null ? (
        <Landing onStart={(mode, file) => setUpload({ mode, file })} />
      ) : (
        <Placeholder upload={upload} onBack={() => setUpload(null)} />
      )}
      <WarningBar />
    </>
  )
}

function Placeholder({ upload, onBack }: { upload: Upload; onBack: () => void }) {
  return (
    <main className="flex min-h-full flex-col items-center justify-center gap-4 px-6 pb-24 text-center text-moss">
      <p>
        {upload.file.name} · modo {upload.mode === 'full' ? 'analítica + hábitos' : 'solo analítica'}
      </p>
      <p>Siguiente pantalla: en construcción.</p>
      <button type="button" onClick={onBack} className="text-emerald underline">
        Volver
      </button>
    </main>
  )
}
