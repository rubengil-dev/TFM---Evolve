/** Cells floating behind every screen, as if under a microscope; a tap on the background bursts a cell or makes a new one. */

import { useEffect, useRef } from 'react'
import { drawCellAt } from '../utils/cells'

type Cell = { x: number; y: number; r: number; vx: number; vy: number; phase: number; grow: number }
type Spark = { x: number; y: number; vx: number; vy: number; life: number }

// Settings
const CELL_COUNT = 14
const MAX_CELLS = 24
const SPARKS_PER_TAP = 12
const SPARK_LIFE = 40 // frames
const GROW_FRAMES = 30
const SPARK = '167, 243, 208'
const INTERACTIVE = 'button, a, input, label, [role="radio"]' // taps here stay quiet

export default function CellBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current!
    const ctx = canvas.getContext('2d')!
    const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    let width = 0
    let height = 0
    let cells: Cell[] = []
    let sparks: Spark[] = []
    let frame = 0
    let tick = 0

    function resize() {
      const ratio = window.devicePixelRatio || 1
      const oldWidth = width
      const oldHeight = height
      width = window.innerWidth
      height = window.innerHeight
      canvas.width = width * ratio
      canvas.height = height * ratio
      ctx.setTransform(ratio, 0, 0, ratio, 0, 0)
      if (cells.length === 0 || oldWidth < 50 || oldHeight < 50) cells = makeCells(width, height)
      else for (const cell of cells) stretch(cell, width / oldWidth, height / oldHeight)
      draw()
    }

    function tap(event: PointerEvent) {
      if ((event.target as Element).closest(INTERACTIVE)) return
      const { clientX: x, clientY: y } = event
      sparks.push(...makeSparks(x, y))
      const hit = cells.findIndex((cell) => Math.hypot(cell.x - x, cell.y - y) < cell.r)
      if (hit >= 0) cells.splice(hit, 1)
      else cells.push(newCell(x, y, width))
      if (cells.length > MAX_CELLS) cells.shift()
    }

    function draw() {
      ctx.clearRect(0, 0, width, height)
      for (const cell of cells) drawCell(ctx, cell, tick)
      for (const spark of sparks) drawSpark(ctx, spark)
    }

    function loop() {
      tick++
      for (const cell of cells) move(cell, width, height)
      for (const spark of sparks) fly(spark)
      sparks = sparks.filter((spark) => spark.life > 0)
      draw()
      frame = requestAnimationFrame(loop)
    }

    resize()
    window.addEventListener('resize', resize)
    if (!still) {
      window.addEventListener('pointerdown', tap)
      frame = requestAnimationFrame(loop)
    }
    return () => {
      cancelAnimationFrame(frame)
      window.removeEventListener('resize', resize)
      window.removeEventListener('pointerdown', tap)
    }
  }, [])

  return <canvas ref={canvasRef} aria-hidden="true" className="fixed inset-0 -z-10 h-full w-full" />
}

function makeCells(width: number, height: number): Cell[] {
  return Array.from({ length: CELL_COUNT }, () => ({ ...newCell(Math.random() * width, Math.random() * height, width), grow: 1 }))
}

function newCell(x: number, y: number, width: number): Cell {
  const scale = Math.max(Math.min(1, width / 900), 0.6)
  return {
    x,
    y,
    r: (14 + Math.random() * 40) * scale,
    vx: (Math.random() - 0.5) * 0.3,
    vy: (Math.random() - 0.5) * 0.3,
    phase: Math.random() * Math.PI * 2,
    grow: 0,
  }
}

function makeSparks(x: number, y: number): Spark[] {
  return Array.from({ length: SPARKS_PER_TAP }, (_, i) => {
    const angle = (i / SPARKS_PER_TAP) * Math.PI * 2 + Math.random() * 0.4
    const speed = 1.2 + Math.random() * 1.6
    return { x, y, vx: Math.cos(angle) * speed, vy: Math.sin(angle) * speed, life: SPARK_LIFE }
  })
}

function stretch(cell: Cell, scaleX: number, scaleY: number) {
  cell.x *= scaleX
  cell.y *= scaleY
}

function move(cell: Cell, width: number, height: number) {
  const margin = 60
  cell.x += cell.vx
  cell.y += cell.vy
  cell.grow = Math.min(1, cell.grow + 1 / GROW_FRAMES)
  if (cell.x < -margin) cell.x = width + margin
  if (cell.x > width + margin) cell.x = -margin
  if (cell.y < -margin) cell.y = height + margin
  if (cell.y > height + margin) cell.y = -margin
}

function fly(spark: Spark) {
  spark.x += spark.vx
  spark.y += spark.vy
  spark.vx *= 0.94
  spark.vy *= 0.94
  spark.life--
}

function drawCell(ctx: CanvasRenderingContext2D, cell: Cell, tick: number) {
  const r = (cell.r + Math.sin(tick * 0.02 + cell.phase) * 2) * easeOut(cell.grow)
  drawCellAt(ctx, cell.x, cell.y, r)
}

function drawSpark(ctx: CanvasRenderingContext2D, spark: Spark) {
  const alpha = spark.life / SPARK_LIFE
  ctx.fillStyle = `rgba(${SPARK}, ${alpha * 0.8})`
  ctx.beginPath()
  ctx.arc(spark.x, spark.y, 1.5 + alpha * 1.5, 0, Math.PI * 2)
  ctx.fill()
}

function easeOut(progress: number): number {
  return 1 - (1 - progress) ** 3
}
