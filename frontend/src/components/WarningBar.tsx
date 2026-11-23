/** Yellow hazard strip with the medical disclaimer, pinned to the bottom. */

import { IconBiohazard } from '@tabler/icons-react'

export default function WarningBar() {
  return (
    <div
      role="note"
      className="fixed inset-x-0 bottom-0 z-10 flex min-h-12 items-center justify-center gap-2 bg-hazard px-4 py-2 text-center text-sm font-medium text-hazard-ink"
    >
      <IconBiohazard aria-hidden="true" size={20} stroke={1.8} className="shrink-0" />
      <span>Esto no es consejo médico ni un diagnóstico</span>
    </div>
  )
}
