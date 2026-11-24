/** Share the result as a picture (phone share sheet) or download it; the picture is made in the browser, nothing is uploaded. */

import { IconDownload, IconShare } from '@tabler/icons-react'
import { useRef, useState, type RefObject } from 'react'
import { makePicture } from '../utils/picture'
import Logo from './Logo'

type Props = { cardRef: RefObject<HTMLDivElement | null> }

export default function ShareButtons({ cardRef }: Props) {
  const watermarkRef = useRef<HTMLDivElement>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const canShareFiles = typeof navigator.canShare === 'function'

  async function run(action: (file: File) => Promise<void>) {
    setBusy(true)
    setError('')
    try {
      await action(await makePicture(cardRef.current!, watermarkRef.current!))
    } catch (caught) {
      if (!(caught instanceof DOMException && caught.name === 'AbortError')) setError('No he podido crear la imagen. Prueba otra vez.')
    } finally {
      setBusy(false)
    }
  }

  async function share(file: File) {
    const data = { files: [file] }
    if (navigator.canShare(data)) await navigator.share(data)
    else download(file)
  }

  return (
    <div className="mt-10 flex flex-col items-center gap-3">
      <div className="flex gap-3">
        {/* The highlighted button goes on the right, closer to the thumb */}
        <button
          type="button"
          disabled={busy}
          onClick={() => run(async (file) => download(file))}
          className={`${BUTTON} ${canShareFiles ? 'border border-line text-mint hover:border-emerald hover:text-emerald' : 'bg-emerald font-medium text-emerald-ink hover:brightness-110'}`}
        >
          <IconDownload aria-hidden="true" size={18} />
          Descargar
        </button>
        {canShareFiles && (
          <button type="button" disabled={busy} onClick={() => run(share)} className={`${BUTTON} bg-emerald font-medium text-emerald-ink hover:brightness-110`}>
            <IconShare aria-hidden="true" size={18} />
            Compartir
          </button>
        )}
      </div>
      {error && <p className="text-xs text-rose">{error}</p>}

      {/* Off screen: only drawn in the picture */}
      <div aria-hidden="true" className="pointer-events-none fixed top-0 -left-[9999px]">
        <div ref={watermarkRef} className="flex w-fit items-center gap-2.5 font-display text-2xl text-mist">
          <Logo size={44} />
          <span>
            Bio<em className="text-emerald">Age</em>
          </span>
        </div>
      </div>
    </div>
  )
}

const BUTTON =
  'flex items-center gap-2 rounded-full px-6 py-3 text-sm transition focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald disabled:opacity-50'

function download(file: File) {
  const url = URL.createObjectURL(file)
  const link = document.createElement('a')
  link.href = url
  link.download = file.name
  link.click()
  URL.revokeObjectURL(url)
}
