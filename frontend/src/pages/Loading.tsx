/** Short cosmetic wait before the result: a DNA helix builds itself from top to bottom while a percentage climbs. */

import { useEffect, useRef, useState } from 'react'

type Props = { onDone: () => void }

// Settings
const DURATION_MS = 1000
const RUNGS = 16
const WIDTH = 90
const HEIGHT = 220
const STRAND_A = '#34d399'
const STRAND_B = '#a7f3d0'
const RUNG = 'rgba(157, 181, 170, 0.25)'

export default function Loading({ onDone }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [percent, setPercent] = useState(0)
  const onDoneRef = useRef(onDone)

  useEffect(() => {
    onDoneRef.current = onDone
  }, [onDone])

  useEffect(() => {
    const canvas = canvasRef.current!
    const ctx = canvas.getContext('2d')!
    const ratio = window.devicePixelRatio || 1
    canvas.width = WIDTH * ratio
    canvas.height = HEIGHT * ratio
    ctx.scale(ratio, ratio)

    const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const start = performance.now()
    let frame = 0

    function loop(now: number) {
      const elapsed = now - start
      const progress = still ? 1 : Math.min(1, elapsed / DURATION_MS)
      drawHelix(ctx, progress, still ? 0 : elapsed)
      setPercent(Math.round(progress * 100))
      if (elapsed >= DURATION_MS) onDoneRef.current()
      else frame = requestAnimationFrame(loop)
    }

    frame = requestAnimationFrame(loop)
    return () => cancelAnimationFrame(frame)
  }, [])

  return (
    <main className="flex min-h-full flex-col items-center justify-center px-6 text-center" aria-live="polite">
      <canvas ref={canvasRef} aria-hidden="true" style={{ width: WIDTH, height: HEIGHT }} />
      <h1 className="mt-6 font-display text-3xl font-medium text-mist">Calculando tu edad</h1>
      <p className="mt-2 text-sm text-moss tabular-nums">{percent} %</p>
    </main>
  )
}

function drawHelix(ctx: CanvasRenderingContext2D, progress: number, elapsed: number) {
  ctx.clearRect(0, 0, WIDTH, HEIGHT)
  const shown = Math.ceil(progress * RUNGS)
  const amplitude = WIDTH * 0.36
  for (let i = 0; i < shown; i++) {
    const y = 12 + (i * (HEIGHT - 24)) / (RUNGS - 1)
    const angle = i * 0.55 + elapsed * 0.004
    const offset = Math.sin(angle) * amplitude
    const depth = Math.cos(angle)
    const left = WIDTH / 2 + offset
    const right = WIDTH / 2 - offset

    ctx.strokeStyle = RUNG
    ctx.lineWidth = 1.5
    ctx.beginPath()
    ctx.moveTo(left, y)
    ctx.lineTo(right, y)
    ctx.stroke()

    dot(ctx, left, y, 3.2 + depth * 1.2, STRAND_A, depth > 0 ? 1 : 0.45)
    dot(ctx, right, y, 3.2 - depth * 1.2, STRAND_B, depth < 0 ? 1 : 0.45)
  }
}

function dot(ctx: CanvasRenderingContext2D, x: number, y: number, radius: number, color: string, alpha: number) {
  ctx.globalAlpha = alpha
  ctx.fillStyle = color
  ctx.beginPath()
  ctx.arc(x, y, radius, 0, Math.PI * 2)
  ctx.fill()
  ctx.globalAlpha = 1
}
