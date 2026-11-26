/** Error screen in the style of the home page: big title, icon, what to do in one box, and buttons (upload another PDF, try again or correct the answers). */

import { IconAlertTriangle, IconFileAlert, IconInfinity, IconListSearch, IconMoodKid, IconPlugConnectedX } from '@tabler/icons-react'
import { useRef, type ChangeEvent } from 'react'
import OgreIcon from '../components/OgreIcon'
import WarningBar from '../components/WarningBar'
import { ERRORS, type ErrorKind } from '../config/errors'
import type { Answers } from '../types'

type Props = { kind: ErrorKind; answers?: Answers; onUpload: (file: File) => void; onRetry: () => void; onHome: () => void }

const ICONS = {
  unreadable: IconFileAlert,
  too_few: IconListSearch,
  impossible: IconAlertTriangle,
  impossible_bmi: OgreIcon,
  too_young: IconMoodKid,
  too_old: IconInfinity,
  unavailable: IconPlugConnectedX,
}

const LONG_TITLE = 16 // letters
const BUTTONS = { upload: 'Subir otro PDF', retry: 'Reintentar', correct: 'Corregirlos' }

export default function ErrorScreen({ kind, answers = {}, onUpload, onRetry, onHome }: Props) {
  const inputRef = useRef<HTMLInputElement>(null)
  const { title, text, steps, warning, action } = ERRORS[kind]
  const Icon = ICONS[kind]

  function handleFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0]
    event.target.value = ''
    if (file) onUpload(file)
  }

  return (
    <>
    <main className="animate-enter mx-auto flex min-h-full max-w-md flex-col items-center justify-center px-6 pt-10 pb-28 text-center">
      <h1 className={`font-display leading-[1.05] font-medium text-mist ${title[1].length > LONG_TITLE ? 'text-4xl' : 'text-5xl'}`}>
        {title[0]}
        <br />
        <em className="text-rose">{title[1]}</em>
      </h1>
      <div className="mt-6 flex h-16 w-16 items-center justify-center rounded-full border-[1.5px] border-rose">
        <Icon aria-hidden="true" size={kind === 'impossible_bmi' ? 38 : 30} stroke={1.6} className="text-rose" />
      </div>
      <p className="mt-4 text-base text-moss">{filled(text, answers)}</p>

      {steps.length > 0 && (
        <div className="mt-4 space-y-3 text-sm text-moss">
          {steps.map((step) => (
            <p key={step}>{step}</p>
          ))}
        </div>
      )}

      <div className="mt-8 flex w-full flex-col gap-3">
        {action && (
          <button
            type="button"
            onClick={() => (action === 'upload' ? inputRef.current?.click() : onRetry())}
            className="rounded-full bg-emerald px-6 py-3 text-sm font-medium text-emerald-ink transition hover:brightness-110 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-mint"
          >
            {BUTTONS[action]}
          </button>
        )}
        <button
          type="button"
          onClick={onHome}
          className="rounded-full border border-line px-6 py-3 text-sm text-mint transition hover:border-emerald hover:text-emerald focus-visible:outline-2 focus-visible:outline-emerald"
        >
          Volver al inicio
        </button>
      </div>

      <input ref={inputRef} type="file" accept="application/pdf,.pdf" className="hidden" onChange={handleFile} />
    </main>
    {warning && <WarningBar urgent={warning} />}
    </>
  )
}

function filled(text: string, answers: Answers): string {
  return text.replace(/\{(\w+)\}/g, (_, id) => Number(answers[id] ?? 0).toLocaleString('es-ES'))
}
