/** Root of the app: keeps the user's choices and decides which screen to show. */

import { useEffect, useState } from 'react'
import CellBackground from './components/CellBackground'
import ImpossibleValue from './components/ImpossibleValue'
import WarningBar from './components/WarningBar'
import { ERRORS, type ErrorKind } from './config/errors'
import { EXAMPLE_MISSING, EXAMPLE_ODD_VALUE, EXAMPLE_RESULT, startingDemo } from './config/example'
import ErrorScreen from './pages/ErrorScreen'
import Landing from './pages/Landing'
import Loading from './pages/Loading'
import Questionnaire from './pages/Questionnaire'
import Result from './pages/Result'
import type { Mode } from './types'

export type Screen = 'landing' | 'questions' | 'loading' | 'result' | 'odd_value' | ErrorKind

// Until the backend is connected, the PDF and the answers are not sent anywhere and the result is an example
export default function App() {
  const demo = startingDemo()
  const [screen, setScreen] = useState<Screen>(demo.screen)
  const [mode, setMode] = useState<Mode>('full')

  function start(chosenMode: Mode) {
    setMode(chosenMode)
    setScreen('questions')
  }

  const home = () => setScreen('landing')

  // Every screen opens at the top, also after a reload
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'instant' })
  }, [screen])
  const result = { ...EXAMPLE_RESULT, ...demo.result, habits: mode === 'full' ? EXAMPLE_RESULT.habits : undefined }

  return (
    <>
      <CellBackground />
      {screen === 'landing' && <Landing onStart={start} onWrongFile={() => setScreen('unreadable')} />}
      {screen === 'questions' && <Questionnaire mode={mode} missing={EXAMPLE_MISSING} onDone={() => setScreen('loading')} onExit={home} />}
      {screen === 'loading' && <Loading onDone={() => setScreen('result')} />}
      {(screen === 'result' || screen === 'odd_value') && <Result result={result} blurred={screen === 'odd_value'} />}
      {screen === 'odd_value' && (
        <ImpossibleValue odd={EXAMPLE_ODD_VALUE} onCorrected={() => setScreen('loading')} onConfirmed={() => setScreen('impossible')} />
      )}
      {isError(screen) && <ErrorScreen kind={screen} onRetry={() => setScreen('questions')} onHome={home} />}
      {(screen === 'result' || screen === 'odd_value') && <WarningBar />}
    </>
  )
}

function isError(screen: Screen): screen is ErrorKind {
  return screen in ERRORS
}
