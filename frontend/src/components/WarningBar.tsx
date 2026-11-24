/** Yellow hazard strip: the medical disclaimer by default, pinned to the screen or at the bottom of a section (home page). */

import { IconAlertTriangle, IconBiohazard } from '@tabler/icons-react'

type Props = { placement?: 'screen' | 'bottom-of-section'; urgent?: string }

// urgent → triangle icon and that text instead of the disclaimer
export default function WarningBar({ placement = 'screen', urgent }: Props) {
  const position = placement === 'screen' ? 'fixed z-10' : 'absolute'
  const Icon = urgent ? IconAlertTriangle : IconBiohazard
  return (
    <div
      role={urgent ? 'alert' : 'note'}
      className={`${position} inset-x-0 bottom-0 flex min-h-12 items-center justify-center gap-2 bg-hazard px-4 py-2 text-center text-sm font-medium text-hazard-ink`}
    >
      <Icon aria-hidden="true" size={20} stroke={1.8} className="shrink-0" />
      <span>{urgent ?? 'No es consejo médico ni diagnóstico. Ante cualquier duda sobre tu analítica, acude a un profesional.'}</span>
    </div>
  )
}
