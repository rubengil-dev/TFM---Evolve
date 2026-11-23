/** Root of the app: keeps the user's choices and decides which screen to show. */

import { useState } from 'react'
import CellBackground from './components/CellBackground'
import WarningBar from './components/WarningBar'
import { EXAMPLE_RESULT } from './config/example'
import Landing from './pages/Landing'
import Loading from './pages/Loading'
import Questionnaire from './pages/Questionnaire'
import Result from './pages/Result'
import type { Mode } from './types'

type Screen = 'landing' | 'questions' | 'loading' | 'result'

// Until the backend is connected, the PDF and the answers are not sent anywhere and the result is an example
export default function App() {
  const [screen, setScreen] = useState<Screen>('landing')
  const [mode, setMode] = useState<Mode>('full')

  function start(chosenMode: Mode) {
    setMode(chosenMode)
    setScreen('questions')
  }

  const result = mode === 'full' ? EXAMPLE_RESULT : { ...EXAMPLE_RESULT, habits: undefined }

  return (
    <>
      <CellBackground />
      {screen === 'landing' && <Landing onStart={start} />}
      {screen === 'questions' && <Questionnaire mode={mode} onDone={() => setScreen('loading')} onExit={() => setScreen('landing')} />}
      {screen === 'loading' && <Loading onDone={() => setScreen('result')} />}
      {screen === 'result' && <Result result={result} />}
      {(screen === 'landing' || screen === 'result') && <WarningBar />}
    </>
  )
}
