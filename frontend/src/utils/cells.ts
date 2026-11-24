/** Drawing of one cell, shared by the animated background and the shared picture. */

// Settings
const STROKE = 'rgba(52, 211, 153, 0.22)'
const FILL = 'rgba(52, 211, 153, 0.05)'
const NUCLEUS = 'rgba(52, 211, 153, 0.25)'

export function drawCellAt(ctx: CanvasRenderingContext2D, x: number, y: number, r: number) {
  ctx.lineWidth = 1.2
  ctx.strokeStyle = STROKE
  ctx.fillStyle = FILL
  ctx.beginPath()
  ctx.arc(x, y, r, 0, Math.PI * 2)
  ctx.fill()
  ctx.stroke()
  ctx.fillStyle = NUCLEUS
  ctx.beginPath()
  ctx.arc(x + r * 0.2, y - r * 0.1, r * 0.28, 0, Math.PI * 2)
  ctx.fill()
}
