/** Home screen: title, the two buttons that pick the mode and open the file picker, and the fine print below. */

import { useRef, type ChangeEvent, type MouseEvent } from 'react'
import WarningBar from '../components/WarningBar'
import type { Mode } from '../types'

type Props = { onStart: (mode: Mode, file: File) => void; onWrongFile: () => void }

export default function Landing({ onStart, onWrongFile }: Props) {
  const inputRef = useRef<HTMLInputElement>(null)
  const modeRef = useRef<Mode>('full')

  function pick(chosen: Mode) {
    modeRef.current = chosen
    inputRef.current?.click()
  }

  function handleFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0]
    event.target.value = ''
    if (!file) return
    if (isPdf(file)) onStart(modeRef.current, file)
    else onWrongFile()
  }

  return (
    <>
      <section className="relative flex min-h-svh flex-col items-center justify-center px-6 pt-10 pb-24 text-center">
        <h1 className="font-display text-5xl leading-[1.05] font-medium text-mist sm:text-6xl">
          Calcula tu
          <br />
          <em className="text-emerald">edad biológica</em>
        </h1>
        <p className="mt-4 text-base text-moss">Para adultos de 18 a 79 años.</p>

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
        <p className="mt-4 text-xs text-moss">
          No guardamos nada: tu analítica se procesa y se descarta
          <a
            href="#letra-pequena"
            onClick={showFinePrint}
            aria-label="Ver la letra pequeña" className="ml-0.5 align-super text-[10px] text-emerald hover:underline">
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
    <footer id="letra-pequena" className="mx-auto max-w-2xl px-6 pt-10 pb-16 text-[11px] leading-relaxed text-moss/80">
      <h2 className="mb-3 text-xs font-medium text-moss">(1) Letra pequeña</h2>
      <ul className="list-disc space-y-2 pl-4">
        <li>
          <b className="font-medium text-moss">Qué hacemos con tus datos.</b> Al subir tu analítica y responder las preguntas aceptas que las
          procesemos con un único fin: calcular tu edad biológica. Son datos de salud: se procesan en memoria y se descartan al terminar. No
          los guardamos, no creamos cuentas y no los compartimos con nadie.
        </li>
        <li>
          <b className="font-medium text-moss">Responsable.</b> Proyecto académico (Trabajo Fin de Máster en Data Science e IA, EVOLVE).
          Como no conservamos nada, no hay datos tuyos que consultar, corregir ni borrar después.
        </li>
        <li>
          <b className="font-medium text-moss">Cómo se calcula.</b> Un modelo entrenado con datos públicos de salud de Estados Unidos
          (NHANES, 1999-2018) en adultos de 18 a 79 años estima tu riesgo a 10 años y lo traduce a la edad de una persona típica con ese
          riesgo.
        </li>
        <li>
          <b className="font-medium text-moss">Qué no es.</b> No es un consejo médico ni un diagnóstico, y no sustituye la opinión de un
          profesional sanitario.
        </li>
      </ul>
    </footer>
  )
}

/** Scrolls to the fine print without leaving #letra-pequena in the address, so a reload opens at the top. */
function showFinePrint(event: MouseEvent<HTMLAnchorElement>) {
  event.preventDefault()
  document.getElementById('letra-pequena')?.scrollIntoView({ behavior: 'smooth' })
}

function isPdf(file: File): boolean {
  return file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')
}
