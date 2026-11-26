/** Result screen: biological age with its margin, the gap to the real age, the tables of years and share / download. */

import { IconAlertCircle, IconInfoCircle } from '@tabler/icons-react'
import { useRef } from 'react'
import ShareButtons from '../components/ShareButtons'
import YearsTable from '../components/YearsTable'
import { BLOOD_GROUPS, HABIT_GROUPS } from '../config/groups'
import { DATA_MAX_AGE, DATA_MIN_AGE } from '../config/limits'
import type { Result as ResultData } from '../types'

type Props = { result: ResultData }

// Ages outside the training data: biological ones are shown as limits, real ones get a warning
const LOWEST_AGE = 18
const HIGHEST_AGE = 90
// Margin from which the result gets a note asking for caution (years)
const CAUTION_MARGIN = 5

export default function Result({ result }: Props) {
  const { age, bio_age, margin } = result
  // Whole years, .5 up; a margin of 0 is not shown
  const shownMargin = margin === null ? 0 : Math.round(margin)
  const cardRef = useRef<HTMLDivElement>(null)

  return (
    <main className="mx-auto w-full max-w-2xl px-6 pt-8 pb-32">
      <div ref={cardRef} className="rounded-3xl border border-line/70 bg-deep/80 px-5 py-8 sm:px-8">
        <div className="flex items-baseline justify-center gap-3">
          <span className="font-display text-[8rem] leading-none font-medium text-mist sm:text-[10rem]">{shownAge(bio_age)}</span>
          {shownMargin > 0 && <span className="text-xl text-moss">± {shownMargin}</span>}
        </div>
        <p className="mt-4 text-center text-base">
          <Gap age={age} bio_age={bio_age} /> que tu edad real
        </p>
        {(age < DATA_MIN_AGE || age > DATA_MAX_AGE) && (
          <p className="mx-auto mt-3 flex w-fit max-w-sm items-center gap-2 rounded-2xl border border-rose/40 bg-rose/10 px-3 py-2 text-left text-xs text-rose">
            <IconAlertCircle aria-hidden="true" size={16} className="shrink-0" />
            Tienes {age} años, fuera de las edades de mis datos ({DATA_MIN_AGE}-{DATA_MAX_AGE}): el resultado puede ser menos preciso
          </p>
        )}
        {shownMargin >= CAUTION_MARGIN && (
          <p className="mx-auto mt-3 flex w-fit max-w-sm items-center gap-2 rounded-2xl border border-line bg-line/20 px-3 py-2 text-left text-xs text-moss">
            <IconInfoCircle aria-hidden="true" size={16} className="shrink-0" />
            Este resultado es menos preciso de lo normal: tómalo con más precaución
          </p>
        )}
        {age >= DATA_MIN_AGE && age <= DATA_MAX_AGE && bio_age > DATA_MAX_AGE && bio_age <= HIGHEST_AGE && (
          <p className="mt-2 text-center text-xs text-moss">Orientativo: por encima de {DATA_MAX_AGE} años hay pocos datos</p>
        )}

        <YearsTable title="Tu analítica" groups={BLOOD_GROUPS} years={result.blood} />
        {result.habits && <YearsTable title="Tus hábitos" groups={HABIT_GROUPS} years={result.habits} />}
      </div>

      <ShareButtons cardRef={cardRef} />
    </main>
  )
}

function Gap({ age, bio_age }: { age: number; bio_age: number }) {
  const years = Math.round(bio_age) - age
  if (years === 0) return <span className="text-emerald">Igual</span>
  const unit = Math.abs(years) === 1 ? 'año' : 'años'
  if (years < 0) return <span className="text-emerald">{`${-years} ${unit} menos`}</span>
  return <span className="text-rose">{`${years} ${unit} más`}</span>
}

function shownAge(bio_age: number): string {
  if (bio_age < LOWEST_AGE) return `<${LOWEST_AGE}`
  if (bio_age > HIGHEST_AGE) return `>${HIGHEST_AGE}`
  return String(Math.round(bio_age))
}
