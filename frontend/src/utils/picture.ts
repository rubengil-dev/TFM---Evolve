/** Picture to share: the result card with the cells around it and the watermark in the bottom right corner. */

import { toCanvas } from 'html-to-image'
import { drawCellAt } from './cells'

// Settings (CSS pixels)
const FILE_NAME = 'mi-edad-biologica.png'
const BACKGROUND = '#06120d'
const SCALE = 2
const MARGIN = 56
const WATERMARK_GAP = 22
const REFERENCE_WIDTH = 720

// Cells around the card: x and y as fractions of the picture, radius at the reference width
const CELLS = [
  [0.05, 0.06, 40], [0.3, 0.02, 18],  [0.62, 0.035, 30], [0.96, 0.1, 46],
  [0.02, 0.27, 24], [0.97, 0.31, 20], [0.2, 0.37, 26],   [0.06, 0.5, 44],
  [0.95, 0.54, 38], [0.72, 0.46, 18], [0.03, 0.74, 20],  [0.55, 0.68, 34],
  [0.97, 0.79, 28], [0.09, 0.92, 48], [0.36, 0.965, 22], [0.56, 0.93, 14],
]

export async function makePicture(card: HTMLElement, watermark: HTMLElement): Promise<File> {
  const cardCanvas = await toCanvas(card, { pixelRatio: SCALE })
  const markCanvas = await toCanvas(watermark, { pixelRatio: SCALE })
  const cardBox = size(cardCanvas)
  const markBox = size(markCanvas)
  const width = cardBox.width + MARGIN * 2
  const height = MARGIN + cardBox.height + WATERMARK_GAP * 2 + markBox.height

  const canvas = document.createElement('canvas')
  canvas.width = width * SCALE
  canvas.height = height * SCALE
  const ctx = canvas.getContext('2d')!
  ctx.scale(SCALE, SCALE)

  ctx.fillStyle = BACKGROUND
  ctx.fillRect(0, 0, width, height)
  const cellScale = Math.max(Math.min(1, width / REFERENCE_WIDTH), 0.75)
  for (const [x, y, r] of CELLS) drawCellAt(ctx, x * width, y * height, r * cellScale)
  ctx.drawImage(cardCanvas, MARGIN, MARGIN, cardBox.width, cardBox.height)
  ctx.drawImage(markCanvas, width - WATERMARK_GAP - markBox.width, height - WATERMARK_GAP - markBox.height, markBox.width, markBox.height)

  const blob = await new Promise<Blob | null>((resolve) => canvas.toBlob(resolve, 'image/png'))
  if (!blob) throw new Error('empty picture')
  return new File([blob], FILE_NAME, { type: 'image/png' })
}

function size(canvas: HTMLCanvasElement) {
  return { width: canvas.width / SCALE, height: canvas.height / SCALE }
}
