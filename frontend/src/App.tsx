/** Root of the app: keeps the user's choices and decides which screen to show. */

import { useState } from 'react'
import CellBackground from './components/CellBackground'
import WarningBar from './components/WarningBar'
import Landing from './pages/Landing'
import Loading from './pages/Loading'
import Questionnaire from './pages/Questionnaire'
import type { Answers, Mode } from './types'

type Screen = 'landing' | 'questions' | 'loading' | 'result'

export default function App() {
  const [screen, setScreen] = useState<Screen>('landing')
  const [mode, setMode] = useState<Mode>('full')
  const [file, setFile] = useState<File | null>(null)
  const [answers, setAnswers] = useState<Answers>({})

  function start(chosenMode: Mode, chosenFile: File) {
    setMode(chosenMode)
    setFile(chosenFile)
    setScreen('questions')
  }

  function finish(given: Answers) {
    setAnswers(given)
    setScreen('loading')
  }

  return (
    <>
      <CellBackground />
      {screen === 'landing' && <Landing onStart={start} />}
      {screen === 'questions' && <Questionnaire mode={mode} onDone={finish} onExit={() => setScreen('landing')} />}
      {screen === 'loading' && <Loading onDone={() => setScreen('result')} />}
      {screen === 'result' && <Placeholder file={file} answers={answers} onBack={() => setScreen('landing')} />}
      {(screen === 'landing' || screen === 'result') && <WarningBar />}
    </>
  )
}

function Placeholder({ file, answers, onBack }: { file: File | null; answers: Answers; onBack: () => void }) {
  return (
    <main className="flex min-h-full flex-col items-center justify-center gap-4 px-6 pb-24 text-center text-moss">
      <p>{file?.name}</p>
      <pre className="text-left text-xs">{JSON.stringify(answers, null, 2)}</pre>
      <p>Pantalla de resultado: en construcción.</p>
      <button type="button" onClick={onBack} className="text-emerald underline">
        Volver al inicio
      </button>
    </main>
  )
}
