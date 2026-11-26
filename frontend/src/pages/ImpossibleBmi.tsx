/** Ogre screen of an impossible BMI: weight and height are corrected right there, and it carries on once they fit. */

import { useState } from 'react'
import { HEIGHT, WEIGHT } from '../config/limits'
import type { Answers } from '../types'
import { isPossibleBmi } from '../utils/person'
import ErrorScreen from './ErrorScreen'

type Props = { answers: Answers; onCorrected: (weight: number, height: number) => void; onHome: () => void }

// Field → its label, unit and the range of its question
const FIELDS = [
  { id: 'weight', label: 'Peso', unit: 'kg', range: WEIGHT },
  { id: 'height', label: 'Altura', unit: 'cm', range: HEIGHT },
] as const

export default function ImpossibleBmi({ answers, onCorrected, onHome }: Props) {
  const [typed, setTyped] = useState({ weight: String(answers.weight ?? ''), height: String(answers.height ?? '') })
  const weight = toWhole(typed.weight, WEIGHT)
  const height = toWhole(typed.height, HEIGHT)
  const isComplete = weight !== null && height !== null
  const fits = isComplete && isPossibleBmi(weight, height)
  const isChanged = typed.weight !== String(answers.weight) || typed.height !== String(answers.height)

  return (
    <ErrorScreen kind="impossible_bmi" answers={answers} canRetry={fits} onUpload={onHome} onRetry={() => fits && onCorrected(weight, height)} onHome={onHome}>
      <div className="mt-6 w-full space-y-3 text-left">
        {FIELDS.map(({ id, label, unit, range }) => (
          <label key={id} htmlFor={`bmi-${id}`} className="flex items-center justify-between gap-3 rounded-xl bg-line/25 px-4 py-3 text-sm text-mist">
            <span>{label}</span>
            <span className="flex items-center gap-2">
              <input
                id={`bmi-${id}`}
                type="text"
                inputMode="numeric"
                value={typed[id]}
                onChange={(event) => setTyped({ ...typed, [id]: event.target.value })}
                className={`w-20 rounded-lg border bg-deep px-2 py-1 text-right text-mist tabular-nums focus:outline-none ${toWhole(typed[id], range) === null ? 'border-rose' : 'border-emerald'}`}
              />
              <span className="w-6 text-moss">{unit}</span>
            </span>
          </label>
        ))}
        {isChanged && isComplete && !fits && <p className="px-1 text-xs text-rose">Siguen sin cuadrar.</p>}
      </div>
    </ErrorScreen>
  )
}

/** Whole number within the range of its question, or null. */
function toWhole(text: string, [min, max]: readonly number[]): number | null {
  if (!/^\d+$/.test(text.trim())) return null
  const value = Number(text)
  return value >= min && value <= max ? value : null
}
