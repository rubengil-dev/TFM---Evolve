/** Window shown after reading the PDF with every value outside what is possible: correct them in place (button or tap on one), or confirm them. */

import { IconAlertTriangle, IconPencil } from '@tabler/icons-react'
import { useState } from 'react'
import { VARIABLE_NAMES } from '../config/variables'
import type { OddValue } from '../types'

/** New value of each corrected variable, in the unit of the lab. */
export type Corrections = Record<string, number>

type Props = { odds: OddValue[]; onCorrected: (corrections: Corrections) => void; onConfirmed: () => void }

export default function ImpossibleValue({ odds, onCorrected, onConfirmed }: Props) {
  // Text of each value being corrected; a variable that is not here is only shown
  const [typed, setTyped] = useState<Record<string, string>>({})
  const editing = odds.filter((odd) => odd.variable in typed)
  const isEditing = editing.length > 0
  const isValid = editing.every((odd) => matchesFormat(typed[odd.variable], odd.text))
  const several = odds.length > 1

  const edit = (chosen: OddValue[]) => setTyped({ ...typed, ...Object.fromEntries(chosen.filter((odd) => !(odd.variable in typed)).map((odd) => [odd.variable, odd.text])) })

  // A value left as it was is not a correction: it stays in the window
  function save() {
    if (!isValid) return
    const changed = editing.filter((odd) => toNumber(typed[odd.variable]) !== toNumber(odd.text))
    setTyped({})
    onCorrected(Object.fromEntries(changed.map((odd) => [odd.variable, toNumber(typed[odd.variable])])))
  }

  return (
    <div role="dialog" aria-modal="true" aria-labelledby="odd-title" className="fixed inset-0 z-20 flex overflow-y-auto bg-deep/40 px-6 py-6">
      <div className="animate-enter m-auto w-full max-w-sm rounded-3xl border border-rose/40 bg-deep p-6 shadow-2xl">
        <div className="flex items-center gap-2">
          <IconAlertTriangle aria-hidden="true" size={22} className="text-rose" />
          <h2 id="odd-title" className="font-display text-xl font-medium text-mist">
            {several ? 'Algunos valores no cuadran' : 'Un valor no cuadra'}
          </h2>
        </div>

        <div className="mt-4 space-y-3">
          {odds.map((odd) => (
            <Row
              key={odd.variable}
              odd={odd}
              typed={typed[odd.variable]}
              focused={odd === editing[0]}
              onEdit={() => edit([odd])}
              onType={(text) => setTyped({ ...typed, [odd.variable]: text })}
            />
          ))}
        </div>

        {isEditing ? (
          <div className="mt-6 flex gap-3">
            <Button onClick={() => setTyped({})}>Atrás</Button>
            <Button primary onClick={save}>
              Guardar
            </Button>
          </div>
        ) : (
          <>
            <p className="mt-4 text-sm leading-relaxed text-moss">
              {several
                ? 'Están fuera de lo posible en una analítica normal. Puede que los haya leído mal del PDF.'
                : 'Está fuera de lo posible en una analítica normal. Puede que lo haya leído mal del PDF.'}
            </p>
            <div className="mt-6 flex gap-3">
              <Button onClick={onConfirmed}>{several ? 'Son correctos' : 'Es correcto'}</Button>
              <Button primary onClick={() => edit(odds)}>
                {several ? 'Corregirlos' : 'Corregirlo'}
              </Button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

type RowProps = { odd: OddValue; typed: string | undefined; focused: boolean; onEdit: () => void; onType: (text: string) => void }

function Row({ odd, typed, focused, onEdit, onType }: RowProps) {
  const isEditing = typed !== undefined
  const decimals = decimalsOf(odd.text)
  const id = `odd-${odd.variable}`

  return (
    <div>
      <label
        htmlFor={id}
        onClick={isEditing ? undefined : onEdit}
        className={`flex items-center justify-between gap-3 rounded-xl bg-line/25 px-4 py-3 text-sm ${isEditing ? '' : 'cursor-pointer hover:bg-line/40'}`}
      >
        <span>{VARIABLE_NAMES[odd.variable]}</span>
        {isEditing ? (
          <span className="flex items-center gap-2">
            <input
              id={id}
              type="text"
              inputMode="decimal"
              autoFocus={focused}
              value={typed}
              onChange={(event) => onType(event.target.value)}
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
      {isEditing && (
        <p className={`mt-1 px-1 text-xs ${matchesFormat(typed, odd.text) ? 'text-moss' : 'text-rose'}`}>
          Como en tu analítica, con {decimals === 0 ? 'ningún decimal' : decimals === 1 ? 'un decimal' : `${decimals} decimales`}
          {decimals > 0 && `: por ejemplo ${example(decimals)}`}
        </p>
      )}
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

function toNumber(text: string): number {
  return Number(text.trim().replace(',', '.'))
}

/** Lab results always keep the decimals of their analyte, so the correction must have the same number of them. */
function decimalsOf(text: string): number {
  const [, fraction = ''] = text.split(/[.,]/)
  return fraction.length
}

function matchesFormat(typed: string, original: string): boolean {
  const decimals = decimalsOf(original)
  const pattern = decimals === 0 ? /^\d+$/ : new RegExp(`^\\d+[.,]\\d{${decimals}}$`)
  return pattern.test(typed.trim())
}

function example(decimals: number): string {
  return `4,${'2'.padEnd(decimals, '0')}`
}
