/** Icon of each result group: anatomical organs, a drop of blood, a shield for the defences, "kg" for weight. */

import { IconArmchair, IconDiamond, IconDotsCircleHorizontal, IconDroplet, IconMoon, IconRun, IconShield, IconSmoking } from '@tabler/icons-react'
import type { GroupId } from '../config/groups'
import { KgIcon, KidneyIcon, LiverIcon, SugarIcon } from './OrganIcons'

const SIZE = 20

export default function GroupIcon({ id }: { id: GroupId }) {
  switch (id) {
    case 'minerals':
      return <IconDiamond aria-hidden="true" size={SIZE} stroke={1.7} />
    case 'sugar':
      return <SugarIcon size={SIZE} />
    case 'red_cells':
      return <IconDroplet aria-hidden="true" size={SIZE} stroke={1.7} />
    case 'defences':
      return <IconShield aria-hidden="true" size={SIZE} stroke={1.7} />
    case 'liver':
      return <LiverIcon size={SIZE} />
    case 'kidney':
      return <KidneyIcon size={SIZE} />
    case 'weight':
      return <KgIcon size={SIZE} />
    case 'other':
      return <IconDotsCircleHorizontal aria-hidden="true" size={SIZE} stroke={1.7} />
    case 'smoking':
      return <IconSmoking aria-hidden="true" size={SIZE} stroke={1.7} />
    case 'exercise':
      return <IconRun aria-hidden="true" size={SIZE} stroke={1.7} />
    case 'sitting':
      return <IconArmchair aria-hidden="true" size={SIZE} stroke={1.7} />
    case 'sleep':
      return <IconMoon aria-hidden="true" size={SIZE} stroke={1.7} />
  }
}
