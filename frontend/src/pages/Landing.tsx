/** Home screen: title, the two buttons that pick the mode and open the file picker, and the fine print below. */

import { useRef, type ChangeEvent, type MouseEvent } from 'react'
import WarningBar from '../components/WarningBar'
import { MAX_AGE, MIN_AGE } from '../config/limits'
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
    <>
      <section className="relative flex min-h-svh flex-col items-center justify-center px-6 pt-10 pb-24 text-center">
        <h1 className="font-display text-5xl leading-[1.05] font-medium text-mist sm:text-6xl">
          Calcula tu
          <br />
          <em className="text-emerald">edad biológica</em>
        </h1>
        <p className="mt-4 text-base text-moss">De {MIN_AGE} a {MAX_AGE} años.</p>

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
            Analítica y hábitos
          </button>
        </div>
        <p className="mt-4 text-xs text-moss">
          Sube un PDF con tu analítica y calcula tu edad
          <a
            href="#letra-pequena"
            onClick={showFinePrint}
            aria-label="Ver la letra pequeña"
            className="ml-0.5 align-super text-[10px] text-emerald hover:underline">
            1
          </a>
        </p>

        <input ref={inputRef} type="file" accept="application/pdf,.pdf" className="hidden" onChange={handleFile} />
        <WarningBar placement="bottom-of-section" />
      </section>

      <FinePrint />
    </>
  )
}

function FinePrint() {
  return (
    <footer id="letra-pequena" className="mx-auto max-w-2xl space-y-5 px-6 pt-10 pb-16 text-xs leading-relaxed text-moss/80">
      <h2 className="text-xs font-medium tracking-widest text-moss uppercase">Lo que debes saber acerca de tus datos</h2>
      <section>
        <h3 className="mb-1 font-medium text-moss">¿Qué hago con tus datos?</h3>
        <p>
          Esto es un proyecto personal y académico. Tus datos solo se usan para calcular tu edad biológica: no se guardan ni se envían a
          terceros. Si quieres comprobarlo tú mismo, el código está en{' '}
          <a href={REPOSITORY} target="_blank" rel="noreferrer" className="text-emerald underline">
            GitHub
          </a>
          .
        </p>
        <p className="mt-3 font-medium text-moss">IMPORTANTE: al subir el PDF con tu analítica aceptas que lo use para esto.</p>
      </section>
      <section>
        <h3 className="mb-1 font-medium text-moss">¿Cómo calculo la edad biológica?</h3>
        <p>
          Con datos de encuestas públicas de salud de EE. UU. (NHANES, 1999-2018) he entrenado un modelo de IA que predice el riesgo de
          morir en los próximos 10 años. Ese riesgo se traduce a edad biológica comparándolo con el de una persona típica de tu mismo sexo
          en cada edad.
        </p>
      </section>
      <section>
        <h3 className="mb-1 font-medium text-moss">¿Por qué no es un diagnóstico médico?</h3>
        <p>
          En el proceso no han intervenido médicos ni lo ha revisado ninguna autoridad sanitaria. Esta predicción no sustituye el consejo
          médico.
        </p>
      </section>
    </footer>
  )
}

const REPOSITORY = 'https://github.com/rubengil-dev/TFM---Evolve'

/** Scrolls to the fine print without leaving #letra-pequena in the address, so a reload opens at the top. */
function showFinePrint(event: MouseEvent<HTMLAnchorElement>) {
  event.preventDefault()
  document.getElementById('letra-pequena')?.scrollIntoView({ behavior: 'smooth' })
}
