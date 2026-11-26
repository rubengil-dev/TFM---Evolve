/** Questions one per screen, Typeform style: options move on by themselves, numbers need "Siguiente". */

import { useState } from 'react'
import ChoiceCards from '../components/ChoiceCards'
import NumberSlider from '../components/NumberSlider'
import ProgressBar from '../components/ProgressBar'
import type { ErrorKind } from '../config/errors'
import { MAX_AGE, MIN_AGE } from '../config/limits'
import { QUESTIONS } from '../config/questions'
import type { Answers, Mode, Question } from '../types'
import { isPossibleBmi } from '../utils/person'
import ErrorScreen from './ErrorScreen'
import ImpossibleBmi from './ImpossibleBmi'

// startAt: id of the question to open at (demos); the first one if not given
type Props = { mode: Mode; missing: string[]; startAt?: string; onDone: (answers: Answers) => void; onExit: () => void }

const AUTO_ADVANCE_MS = 280
const BODY_MEASURES = ['weight', 'height']

export default function Questionnaire({ mode, missing, startAt, onDone, onExit }: Props) {
  const questions = QUESTIONS.filter(
    (question) => question.modes.includes(mode) && (!question.onlyIfMissing || missing.includes(question.id)),
  )
  const [index, setIndex] = useState(() => Math.max(0, questions.findIndex(({ id }) => id === startAt)))
  const [answers, setAnswers] = useState<Answers>(() => startingAnswers(questions))
  // An answer that stops the flow right when it is given
  const [stop, setStop] = useState<ErrorKind | null>(null)
  const question = questions[index]
  const isLast = index === questions.length - 1

  function next(updated: Answers) {
    const stopping = stopFor(updated)
    if (stopping) setStop(stopping)
    else advance(updated)
  }

  function stopFor(updated: Answers): ErrorKind | null {
    const age = Number(updated.age)
    if (question.id === 'age' && age < MIN_AGE) return 'too_young'
    if (question.id === 'age' && age > MAX_AGE) return 'too_old'
    if (completesBmi() && !isPossibleBmi(Number(updated.weight), Number(updated.height))) return 'impossible_bmi'
    return null
  }

  function advance(updated: Answers) {
    if (isLast) onDone(updated)
    else setIndex(index + 1)
  }

  // Last body measure asked: both are known
  function completesBmi() {
    const later = questions.slice(index + 1)
    return BODY_MEASURES.includes(question.id) && !later.some(({ id }) => BODY_MEASURES.includes(id))
  }

  function correctMeasures(weight: number, height: number) {
    const updated = { ...answers, weight, height }
    setAnswers(updated)
    setStop(null)
    advance(updated)
  }

  function answer(value: number | string, movesOn: boolean) {
    const updated = { ...answers, [question.id]: value }
    setAnswers(updated)
    if (movesOn) setTimeout(() => next(updated), AUTO_ADVANCE_MS)
  }

  function back() {
    if (index === 0) onExit()
    else setIndex(index - 1)
  }

  if (stop === 'impossible_bmi') return <ImpossibleBmi answers={answers} onCorrected={correctMeasures} onHome={onExit} />
  if (stop) return <ErrorScreen kind={stop} onUpload={onExit} onRetry={onExit} onHome={onExit} />

  return (
    <main className="mx-auto flex min-h-full w-full max-w-md flex-col px-6 pt-6 pb-10">
      <ProgressBar current={index + 1} total={questions.length} onBack={back} />

      <section key={question.id} className="animate-enter mt-10 flex flex-1 flex-col">
        <h1 className="font-display text-3xl leading-tight font-medium text-mist">{question.title}</h1>
        {question.hint ? <p className="mt-2 mb-8 text-sm text-moss">{question.hint}</p> : <div className="mb-8" />}

        {question.kind === 'choice' ? (
          <ChoiceCards options={question.options} selected={answers[question.id] as string | undefined} onPick={(value) => answer(value, true)} />
        ) : (
          <>
            <NumberSlider {...question} value={answers[question.id] as number} onChange={(value) => answer(value, false)} />
            <button
              type="button"
              onClick={() => next(answers)}
              className="mx-auto mt-10 rounded-full bg-emerald px-8 py-3 text-sm font-medium text-emerald-ink transition hover:brightness-110 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-mint"
            >
              {isLast ? 'Ver mi edad biológica' : 'Continuar'}
            </button>
          </>
        )}

      </section>
    </main>
  )
}

function startingAnswers(questions: Question[]): Answers {
  const answers: Answers = {}
  for (const question of questions) if (question.kind === 'number') answers[question.id] = question.start
  return answers
}
