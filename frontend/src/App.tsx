/** Root of the app: keeps the user's data between screens, asks the backend and decides which screen to show. */

import { useEffect, useRef, useState } from 'react'
import CellBackground from './components/CellBackground'
import ImpossibleValue, { type Corrections } from './components/ImpossibleValue'
import WarningBar from './components/WarningBar'
import { ERRORS, type ErrorKind } from './config/errors'
import { startingDemo } from './config/example'
import ErrorScreen from './pages/ErrorScreen'
import Landing from './pages/Landing'
import Loading from './pages/Loading'
import Questionnaire from './pages/Questionnaire'
import Result from './pages/Result'
import type { Answers, Mode, Reading, Result as ResultData } from './types'
import { ApiError, calculate, isPdf, readPdf } from './utils/api'
import { buildPerson, missingFrom, withCorrections } from './utils/person'

export type Screen = 'landing' | 'reading' | 'odd_value' | 'questions' | 'calculating' | 'result' | ErrorKind

// Shortest time the loading screen before the result is shown; the one of the PDF lasts what reading it takes
const CALCULATING_MS = 1000

export default function App() {
  const [demo] = useState(startingDemo)
  const [screen, setScreen] = useState<Screen>(demo.screen)
  const [mode, setMode] = useState<Mode>('full')
  const [reading, setReading] = useState<Reading | null>(demo.reading ?? null)
  const [answers, setAnswers] = useState<Answers>(demo.answers ?? {})
  const [result, setResult] = useState<ResultData | null>(demo.result ?? null)

  const home = () => setScreen('landing')
  // What to repeat if the backend does not answer; it lives in this tab, nothing is stored
  const retryRef = useRef<() => void>(home)

  // Every screen opens at the top, also after a reload
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'instant' })
  }, [screen])

  async function start(chosenMode: Mode, file: File) {
    setMode(chosenMode)
    if (!isPdf(file)) return setScreen('unreadable')
    retryRef.current = () => start(chosenMode, file)
    setScreen('reading')
    try {
      const read = await readPdf(file, chosenMode)
      setReading(read)
      setScreen(read.odd.length > 0 ? 'odd_value' : 'questions')
    } catch (error) {
      setScreen(errorScreen(error))
    }
  }

  // Values not corrected stay in the window
  function correct(corrections: Corrections) {
    if (!reading) return
    const corrected = withCorrections(reading, corrections)
    setReading(corrected)
    if (corrected.odd.length === 0) setScreen('questions')
  }

  async function finish(given: Answers) {
    if (!reading) return
    setAnswers(given)
    retryRef.current = () => finish(given)
    setScreen('calculating')
    try {
      setResult(await atLeast(CALCULATING_MS, calculate(buildPerson(reading, given, mode))))
      setScreen('result')
    } catch (error) {
      const kind = errorScreen(error)
      if (kind === 'impossible_bmi') retryRef.current = () => setScreen('questions')
      setScreen(kind)
    }
  }

  return (
    <>
      <CellBackground />
      {screen === 'landing' && <Landing onStart={start} />}
      {screen === 'reading' && <Loading title="Leyendo tu analítica" />}
      {screen === 'odd_value' && reading && (
        <ImpossibleValue odds={reading.odd} onCorrected={correct} onConfirmed={() => setScreen('impossible')} />
      )}
      {screen === 'questions' && reading && (
        <Questionnaire mode={mode} missing={missingFrom(reading)} onDone={finish} onExit={home} />
      )}
      {screen === 'calculating' && <Loading title="Calculando tu edad" durationMs={CALCULATING_MS} />}
      {screen === 'result' && result && (
        <>
          <Result result={result} />
          <WarningBar />
        </>
      )}
      {isError(screen) && <ErrorScreen kind={screen} answers={answers} onUpload={(file) => start(mode, file)} onRetry={() => retryRef.current()} onHome={home} />}
    </>
  )
}

function isError(screen: Screen): screen is ErrorKind {
  return screen in ERRORS
}

function errorScreen(error: unknown): ErrorKind {
  if (error instanceof ApiError) return error.kind
  throw error
}

/** Waits for the task, and at least that time. */
async function atLeast<T>(milliseconds: number, task: Promise<T>): Promise<T> {
  const [done] = await Promise.all([task, new Promise((resolve) => setTimeout(resolve, milliseconds))])
  return done
}
