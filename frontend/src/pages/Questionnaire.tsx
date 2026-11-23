/** Questions one per screen, Typeform style: options move on by themselves, numbers need "Siguiente". */

import { IconGlass } from '@tabler/icons-react'
import { useState } from 'react'
import ChoiceCards from '../components/ChoiceCards'
import NumberSlider from '../components/NumberSlider'
import ProgressBar from '../components/ProgressBar'
import { QUESTIONS } from '../config/questions'
import type { Answers, Mode, Question } from '../types'

type Props = { mode: Mode; onDone: (answers: Answers) => void; onExit: () => void }

const AUTO_ADVANCE_MS = 280

export default function Questionnaire({ mode, onDone, onExit }: Props) {
  const questions = QUESTIONS.filter((question) => question.modes.includes(mode))
  const [index, setIndex] = useState(0)
  const [answers, setAnswers] = useState<Answers>(() => startingAnswers(questions))
  const question = questions[index]
  const isLast = index === questions.length - 1

  function next(updated: Answers) {
    if (isLast) onDone(updated)
    else setIndex(index + 1)
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

  return (
    <main className="mx-auto flex min-h-full w-full max-w-md flex-col px-6 pt-6 pb-10">
      <ProgressBar current={index + 1} total={questions.length} onBack={back} />

      <section key={question.id} className="animate-enter mt-10 flex flex-1 flex-col">
        <h1 className="font-display text-3xl leading-tight font-medium text-mist">{question.title}</h1>
        <p className="mt-2 mb-8 text-sm text-moss">{question.hint}</p>

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
              {isLast ? 'Ver mi resultado' : 'Siguiente'}
            </button>
          </>
        )}

        {question.note && (
          <p className="mt-8 flex gap-3 rounded-2xl border border-dashed border-line p-4 text-xs leading-relaxed text-moss">
            <IconGlass aria-hidden="true" size={18} className="shrink-0 text-emerald" />
            {question.note}
          </p>
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
