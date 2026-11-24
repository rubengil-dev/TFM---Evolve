/** Number picker: a slider for the rough value and − / + buttons at its ends for the fine tuning. */

import { IconMinus, IconPlus } from '@tabler/icons-react'
import type { CSSProperties, ReactNode } from 'react'

type Props = { min: number; max: number; step: number; value: number; unit: string; onChange: (value: number) => void }

export default function NumberSlider({ min, max, step, value, unit, onChange }: Props) {
  function nudge(direction: 1 | -1) {
    onChange(clamp(round(value + direction * step), min, max))
  }

  return (
    <div>
      <div className="mb-8 text-center font-display text-6xl leading-none text-emerald">
        {format(value)}
        <span className="ml-1 text-2xl text-moss">{unit}</span>
      </div>
      <div className="flex items-center gap-3">
        <StepButton label={`Menos ${format(step)} ${unit}`} disabled={value <= min} onClick={() => nudge(-1)}>
          <IconMinus aria-hidden="true" size={20} />
        </StepButton>
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value}
          aria-valuetext={`${format(value)} ${unit}`}
          onChange={(event) => onChange(Number(event.target.value))}
          style={{ '--fill': `${((value - min) / (max - min)) * 100}%` } as CSSProperties}
          className="range-slider min-w-0 flex-1"
        />
        <StepButton label={`Más ${format(step)} ${unit}`} disabled={value >= max} onClick={() => nudge(1)}>
          <IconPlus aria-hidden="true" size={20} />
        </StepButton>
      </div>
      <div className="mt-2 flex justify-between px-14 text-xs text-moss">
        <span>{format(min)}</span>
        <span>{format(max)}</span>
      </div>
    </div>
  )
}

function StepButton({ label, disabled, onClick, children }: { label: string; disabled: boolean; onClick: () => void; children: ReactNode }) {
  return (
    <button
      type="button"
      aria-label={label}
      disabled={disabled}
      onClick={onClick}
      className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-line text-mint transition hover:border-emerald hover:text-emerald focus-visible:outline-2 focus-visible:outline-emerald disabled:opacity-30"
    >
      {children}
    </button>
  )
}

function round(value: number): number {
  return Math.round(value * 10) / 10
}

function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value))
}

function format(value: number): string {
  return value.toLocaleString('es-ES')
}
