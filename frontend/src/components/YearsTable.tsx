/** One result table in two columns: groups that take years away (left) and groups that add them (right). */

import type { Group } from '../config/groups'
import type { GroupYears } from '../types'
import GroupIcon from './GroupIcon'

type Props = { title: string; groups: Group[]; years: GroupYears }
type Tone = 'good' | 'bad'

export default function YearsTable({ title, groups, years }: Props) {
  const value = (group: Group) => years[group.id] as number
  const known = groups.filter((group) => years[group.id] != null)
  const younger = known.filter((group) => value(group) < 0).sort((a, b) => value(a) - value(b))
  const older = known.filter((group) => value(group) >= 0).sort((a, b) => value(b) - value(a))
  const missing = groups.filter((group) => years[group.id] == null)

  return (
    <section className="mt-10">
      <h2 className="font-display text-xl font-medium text-mist">{title}</h2>
      <div className="mt-3 grid grid-cols-2 gap-4 sm:gap-8">
        <Column heading="Te quitan años" tone="good" groups={younger} value={value} />
        <Column heading="Te suman años" tone="bad" groups={older} value={value} />
      </div>
      {missing.length > 0 && (
        <p className="mt-3 text-xs text-moss/70">
          Sin datos en tu analítica: {missing.map((group) => group.label.toLowerCase()).join(', ')}
        </p>
      )}
    </section>
  )
}

function Column({ heading, tone, groups, value }: { heading: string; tone: Tone; groups: Group[]; value: (group: Group) => number }) {
  const color = tone === 'good' ? 'text-emerald' : 'text-rose'
  return (
    <div>
      <h3 className={`mb-1 text-xs ${color}`}>{heading}</h3>
      {groups.length === 0 && <p className="py-2 text-xs text-moss/70">Ninguno</p>}
      <ul>
        {groups.map((group) => (
          <li key={group.id} className="flex items-center justify-between gap-2 border-b border-line/40 py-2 text-sm">
            <span className="flex min-w-0 items-center gap-2">
              <span className={`shrink-0 ${color}`}>
                <GroupIcon id={group.id} />
              </span>
              <span className="leading-tight">{group.label}</span>
            </span>
            <span className={`shrink-0 tabular-nums ${color}`}>{signed(value(group))}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

function signed(value: number): string {
  const text = Math.abs(value).toLocaleString('es-ES', { minimumFractionDigits: 1, maximumFractionDigits: 1 })
  return `${value < 0 ? '−' : '+'}${text}`
}
