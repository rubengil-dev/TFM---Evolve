/** Questions one per screen, Typeform style: options move on by themselves, numbers need "Siguiente". */

import { useState } from 'react'
import ChoiceCards from '../components/ChoiceCards'
import NumberSlider from '../components/NumberSlider'
import ProgressBar from '../components/ProgressBar'
import { QUESTIONS } from '../config/questions'
import type { Answers, Mode, Question } from '../types'
import { isPossibleBmi } from '../utils/person'
import ErrorScreen from './ErrorScreen'

type Props = { mode: Mode; missing: string[]; onDone: (answers: Answers) => void; onExit: () => void }

const AUTO_ADVANCE_MS = 280
const BODY_MEASURES = ['weight', 'height']

export default function Questionnaire({ mode, missing, onDone, onExit }: Props) {
  const questions = QUESTIONS.filter(
    (question) => question.modes.includes(mode) && (!question.onlyIfMissing || missing.includes(question.id)),
  )
  const [index, setIndex] = useState(0)
  const [answers, setAnswers] = useState<Answers>(() => startingAnswers(questions))
  const [isImpossible, setIsImpossible] = useState(false)
  const question = questions[index]
  const isLast = index === questions.length - 1

  function next(updated: Answers) {
    if (completesBmi() && !isPossibleBmi(Number(updated.weight), Number(updated.height))) setIsImpossible(true)
    else if (isLast) onDone(updated)
    else setIndex(index + 1)
  }

  // Last body measure asked: both are known
  function completesBmi() {
    const later = questions.slice(index + 1)
    return BODY_MEASURES.includes(question.id) && !later.some(({ id }) => BODY_MEASURES.includes(id))
  }

  function correctMeasures() {
    setIsImpossible(false)
    setIndex(questions.findIndex(({ id }) => BODY_MEASURES.includes(id)))
  }

  function answer(value: number | string, advance: boolean) {
    const updated = { ...answers, [question.id]: value }
    setAnswers(updated)
    if (advance) setTimeout(() => next(updated), AUTO_ADVANCE_MS)
  }

  function back() {
    if (index === 0) onExit()
    else setIndex(index - 1)
  }

  if (isImpossible) return <ErrorScreen kind="impossible_bmi" answers={answers} onUpload={onExit} onRetry={correctMeasures} onHome={onExit} />

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
