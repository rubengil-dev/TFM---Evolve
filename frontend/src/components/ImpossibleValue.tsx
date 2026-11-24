/** Window over the blurred result when a value is outside what is possible: correct it in place (button or tap on it), or confirm it. */

import { IconAlertTriangle, IconPencil } from '@tabler/icons-react'
import { useState } from 'react'

/** A value as read from the PDF; `text` keeps its decimals, e.g. "9,8". */
export type OddValue = { label: string; text: string; unit: string }

type Props = { odd: OddValue; onCorrected: (value: number) => void; onConfirmed: () => void }

export default function ImpossibleValue({ odd, onCorrected, onConfirmed }: Props) {
  const [editing, setEditing] = useState(false)
  const [typed, setTyped] = useState(odd.text)
  const decimals = decimalsOf(odd.text)
  const isValid = matchesFormat(typed, decimals)

  return (
    <div role="dialog" aria-modal="true" aria-labelledby="odd-title" className="fixed inset-0 z-20 flex items-center justify-center bg-deep/40 px-6">
      <div className="animate-enter w-full max-w-sm rounded-3xl border border-rose/40 bg-deep p-6 shadow-2xl">
        <div className="flex items-center gap-2">
          <IconAlertTriangle aria-hidden="true" size={22} className="text-rose" />
          <h2 id="odd-title" className="font-display text-xl font-medium text-mist">
            Un valor no cuadra
          </h2>
        </div>

        <label
          htmlFor="odd-value"
          onClick={() => setEditing(true)}
          className={`mt-4 flex items-center justify-between gap-3 rounded-xl bg-line/25 px-4 py-3 text-sm ${editing ? '' : 'cursor-pointer hover:bg-line/40'}`}
        >
          <span>{odd.label}</span>
          {editing ? (
            <span className="flex items-center gap-2">
              <input
                id="odd-value"
                type="text"
                inputMode="decimal"
                autoFocus
                value={typed}
                onChange={(event) => setTyped(event.target.value)}
                className="w-20 rounded-lg border border-emerald bg-deep px-2 py-1 text-right text-mist tabular-nums focus:outline-none"
              />
              <span className="text-moss">{odd.unit}</span>
            </span>
          ) : (
            <span className="flex items-center gap-2 text-rose tabular-nums">
              {odd.text} {odd.unit}
              <IconPencil aria-hidden="true" size={16} className="text-moss" />
            </span>
          )}
        </label>

        {editing ? (
          <>
            <p className={`mt-3 text-xs ${isValid ? 'text-moss' : 'text-rose'}`}>
              Escríbelo como en tu analítica, con {decimals === 0 ? 'ningún decimal' : decimals === 1 ? 'un decimal' : `${decimals} decimales`}
              {decimals > 0 && `: por ejemplo ${example(decimals)}`}
            </p>
            <div className="mt-6 flex gap-3">
              <Button onClick={() => setEditing(false)}>Atrás</Button>
              <Button primary onClick={() => isValid && onCorrected(Number(typed.replace(',', '.')))}>
                Guardar
              </Button>
            </div>
          </>
        ) : (
          <>
            <p className="mt-4 text-sm leading-relaxed text-moss">
              Está fuera de lo posible en una analítica normal. Puede que lo haya leído mal del PDF.
            </p>
            <div className="mt-6 flex gap-3">
              <Button onClick={onConfirmed}>Es correcto</Button>
              <Button primary onClick={() => setEditing(true)}>
                Corregirlo
              </Button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

function Button({ primary = false, onClick, children }: { primary?: boolean; onClick: () => void; children: string }) {
  const look = primary ? 'bg-emerald font-medium text-emerald-ink hover:brightness-110' : 'border border-line text-mint hover:border-emerald hover:text-emerald'
  return (
    <button type="button" onClick={onClick} className={`flex-1 rounded-full px-5 py-3 text-sm transition focus-visible:outline-2 focus-visible:outline-emerald ${look}`}>
      {children}
    </button>
  )
}

/** Lab results always keep the decimals of their analyte, so the correction must have the same number of them. */
function decimalsOf(text: string): number {
  const [, fraction = ''] = text.split(/[.,]/)
  return fraction.length
}

function matchesFormat(text: string, decimals: number): boolean {
  const pattern = decimals === 0 ? /^\d+$/ : new RegExp(`^\\d+[.,]\\d{${decimals}}$`)
  return pattern.test(text.trim())
}

function example(decimals: number): string {
  return `4,${'2'.padEnd(decimals, '0')}`
}
