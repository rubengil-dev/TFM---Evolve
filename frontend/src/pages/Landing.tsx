/** Home screen: title and the two buttons that pick the mode and open the file picker. */

import { useRef, type ChangeEvent } from 'react'
import type { Mode } from '../types'

type Props = { onStart: (mode: Mode, file: File) => void }

export default function Landing({ onStart }: Props) {
  const inputRef = useRef<HTMLInputElement>(null)
  const modeRef = useRef<Mode>('full')

  function pick(chosen: Mode) {
    modeRef.current = chosen
    inputRef.current?.click()
  }

  function handleFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0]
    event.target.value = ''
    if (file) onStart(modeRef.current, file)
  }

  return (
    <main className="flex min-h-full flex-col items-center justify-center px-6 pt-10 pb-24 text-center">
      <h1 className="font-display text-5xl leading-[1.05] font-medium text-mist sm:text-6xl">
        Calcula tu
        <br />
        <em className="text-emerald">edad biológica</em>
      </h1>
      <p className="mt-4 max-w-md text-base text-moss">Tu analítica de sangre dice más de lo que parece.</p>

      <div className="mt-8 flex w-full max-w-md flex-col-reverse gap-3 sm:w-auto sm:max-w-none sm:flex-row">
        <button
          type="button"
          onClick={() => pick('quick')}
          className="rounded-full border border-line px-6 py-3 text-sm text-mint transition hover:border-emerald hover:text-emerald focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald"
        >
          Solo analítica
        </button>
        <button
          type="button"
          onClick={() => pick('full')}
          className="rounded-full bg-emerald px-6 py-3 text-sm font-medium text-emerald-ink transition hover:brightness-110 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-mint"
        >
          Analítica + hábitos
        </button>
      </div>
      <p className="mt-4 text-xs text-moss">Solo PDF. No guardamos nada: tu analítica se procesa y se descarta.</p>

      <input ref={inputRef} type="file" accept="application/pdf,.pdf" className="hidden" onChange={handleFile} />
    </main>
  )
}
