/** Thin bar at the top of the questionnaire with the back arrow and "question X of N". */

import { IconArrowLeft } from '@tabler/icons-react'

type Props = { current: number; total: number; onBack: () => void }

export default function ProgressBar({ current, total, onBack }: Props) {
  return (
    <div>
      <div className="flex items-center justify-between text-sm text-moss">
        <button type="button" onClick={onBack} aria-label="Volver" className="-m-2 p-2 transition hover:text-emerald">
          <IconArrowLeft aria-hidden="true" size={20} />
        </button>
        <span>
          {current} de {total}
        </span>
      </div>
      <div className="mt-3 h-1 overflow-hidden rounded-full bg-line/50">
        <div className="h-full rounded-full bg-emerald transition-all duration-300" style={{ width: `${(current / total) * 100}%` }} />
      </div>
    </div>
  )
}
