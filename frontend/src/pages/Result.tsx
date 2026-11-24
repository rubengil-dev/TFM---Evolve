/** Result screen: biological age with its margin, the gap to the real age, the tables of years and share / download. */

import { IconAlertCircle } from '@tabler/icons-react'
import { useRef } from 'react'
import ShareButtons from '../components/ShareButtons'
import YearsTable from '../components/YearsTable'
import { BLOOD_GROUPS, HABIT_GROUPS } from '../config/groups'
import type { Result as ResultData } from '../types'

type Props = { result: ResultData; blurred?: boolean }

// Ages outside the training data: biological ones are shown as limits, real ones get a warning
const LOWEST_AGE = 18
const HIGHEST_AGE = 90
const DATA_MIN_AGE = 18
const DATA_MAX_AGE = 79

export default function Result({ result, blurred = false }: Props) {
  const { age, bioAge, margin } = result
  const cardRef = useRef<HTMLDivElement>(null)

  return (
    <main
      aria-hidden={blurred}
      className={`mx-auto w-full max-w-2xl px-6 pt-8 pb-32 ${blurred ? 'pointer-events-none blur-md select-none' : ''}`}
    >
      <div ref={cardRef} className="rounded-3xl border border-line/70 bg-deep/80 px-5 py-8 sm:px-8">
        <div className="flex items-baseline justify-center gap-3">
          <span className="font-display text-[8rem] leading-none font-medium text-mist sm:text-[10rem]">{shownAge(bioAge)}</span>
          <span className="text-xl text-moss">± {Math.round(margin)}</span>
        </div>
        <p className="mt-4 text-center text-base">
          <Gap age={age} bioAge={bioAge} /> que tu edad real
        </p>
        {(age < DATA_MIN_AGE || age > DATA_MAX_AGE) && (
          <p className="mx-auto mt-3 flex w-fit max-w-sm items-center gap-2 rounded-2xl border border-rose/40 bg-rose/10 px-3 py-2 text-left text-xs text-rose">
            <IconAlertCircle aria-hidden="true" size={16} className="shrink-0" />
            Tienes {age} años, fuera de las edades de mis datos (18-79): el resultado puede ser menos preciso
          </p>
        )}
        {age >= DATA_MIN_AGE && age <= DATA_MAX_AGE && bioAge > DATA_MAX_AGE && bioAge <= HIGHEST_AGE && (
          <p className="mt-2 text-center text-xs text-moss">Orientativo: por encima de 79 años hay pocos datos</p>
        )}

        <YearsTable title="Tu analítica" groups={BLOOD_GROUPS} years={result.blood} />
        {result.habits && <YearsTable title="Tus hábitos" groups={HABIT_GROUPS} years={result.habits} />}
      </div>

      <ShareButtons cardRef={cardRef} />
    </main>
  )
}

function Gap({ age, bioAge }: { age: number; bioAge: number }) {
  const years = Math.round(bioAge) - age
  if (years === 0) return <span className="text-emerald">Igual</span>
  const unit = Math.abs(years) === 1 ? 'año' : 'años'
  if (years < 0) return <span className="text-emerald">{`${-years} ${unit} menos`}</span>
  return <span className="text-rose">{`${years} ${unit} más`}</span>
}

function shownAge(bioAge: number): string {
  if (bioAge < LOWEST_AGE) return `<${LOWEST_AGE}`
  if (bioAge > HIGHEST_AGE) return `>${HIGHEST_AGE}`
  return String(Math.round(bioAge))
}
