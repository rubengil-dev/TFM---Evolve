/** Answer options as large cards with an icon and a short clarification; tapping one picks it. */

import { IconArmchair, IconGenderFemale, IconGenderMale, IconHistory, IconRun, IconSmoking, IconSmokingNo, IconWalk } from '@tabler/icons-react'
import type { ChoiceOption } from '../types'

type Props = { options: ChoiceOption[]; selected?: string; onPick: (value: string) => void }

const ICONS = {
  female: IconGenderFemale,
  male: IconGenderMale,
  never: IconSmokingNo,
  former: IconHistory,
  current: IconSmoking,
  intense: IconRun,
  moderate: IconWalk,
  none: IconArmchair,
}

export default function ChoiceCards({ options, selected, onPick }: Props) {
  return (
    <div role="radiogroup" className={sideBySide(options) ? 'grid grid-cols-2 gap-3' : 'flex flex-col gap-3'}>
      {options.map((option) => {
        const Icon = ICONS[option.icon]
        const isSelected = option.value === selected
        return (
          <button
            key={option.value}
            type="button"
            role="radio"
            aria-checked={isSelected}
            onClick={() => onPick(option.value)}
            className={`flex items-center gap-4 rounded-2xl border p-4 text-left transition focus-visible:outline-2 focus-visible:outline-emerald ${
              isSelected ? 'border-emerald bg-emerald/12' : 'border-line bg-deep/60 hover:border-emerald/70'
            }`}
          >
            <Icon aria-hidden="true" size={26} stroke={1.6} className="shrink-0 text-emerald" />
            <span>
              <span className="block text-base text-mist">{option.label}</span>
              {option.detail && <span className="mt-0.5 block text-xs text-moss">{option.detail}</span>}
            </span>
          </button>
        )
      })}
    </div>
  )
}

/** Two short options without clarification fit on one line (e.g. woman / man). */
function sideBySide(options: ChoiceOption[]): boolean {
  return options.length === 2 && options.every((option) => !option.detail)
}
