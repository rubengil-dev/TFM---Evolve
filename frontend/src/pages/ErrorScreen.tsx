/** Error screen in the style of the home page: big title, icon, what to do in one box, and buttons. */

import { IconAlertTriangle, IconFileAlert, IconListSearch, IconMoodKid } from '@tabler/icons-react'
import { useRef, type ChangeEvent } from 'react'
import WarningBar from '../components/WarningBar'
import { ERRORS, type ErrorKind } from '../config/errors'

type Props = { kind: ErrorKind; onRetry: (file: File) => void; onHome: () => void }

const ICONS = { unreadable: IconFileAlert, too_few: IconListSearch, impossible: IconAlertTriangle, too_young: IconMoodKid }

export default function ErrorScreen({ kind, onRetry, onHome }: Props) {
  const inputRef = useRef<HTMLInputElement>(null)
  const { title, text, steps, warning, canRetry } = ERRORS[kind]
  const Icon = ICONS[kind]

  function handleFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0]
    event.target.value = ''
    if (file) onRetry(file)
  }

  return (
    <>
    <main className="animate-enter mx-auto flex min-h-full max-w-md flex-col items-center justify-center px-6 pt-10 pb-28 text-center">
      <h1 className="font-display text-5xl leading-[1.05] font-medium text-mist">
        {title[0]}
        <br />
        <em className="text-rose">{title[1]}</em>
      </h1>
      <div className="mt-6 flex h-16 w-16 items-center justify-center rounded-full border-[1.5px] border-rose">
        <Icon aria-hidden="true" size={30} stroke={1.6} className="text-rose" />
      </div>
      <p className="mt-4 text-base text-moss">{text}</p>

      {steps.length > 0 && (
        <div className="mt-3 space-y-1 text-sm text-moss">
          {steps.map((step) => (
            <p key={step}>{step}</p>
          ))}
        </div>
      )}

      <div className="mt-8 flex w-full flex-col gap-3">
        {canRetry && (
          <button
            type="button"
            onClick={() => inputRef.current?.click()}
            className="rounded-full bg-emerald px-6 py-3 text-sm font-medium text-emerald-ink transition hover:brightness-110 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-mint"
          >
            Subir otro PDF
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
