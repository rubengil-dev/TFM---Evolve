/** Requests to the backend; every failure becomes the error screen to show. */

import { ERRORS, type ErrorKind } from '../config/errors'
import type { Mode, Person, Reading, Result } from '../types'

export class ApiError extends Error {
  kind: ErrorKind

  constructor(kind: ErrorKind) {
    super(kind)
    this.kind = kind
  }
}

// The PDF travels as the raw body: a form could be written to disk in the server; the mode decides how many values can be missing
export function readPdf(file: File, mode: Mode): Promise<Reading> {
  return post(`/api/read?mode=${mode}`, file, 'application/pdf')
}

export function calculate(person: Person): Promise<Result> {
  return post('/api/calculate', JSON.stringify(person), 'application/json')
}

export function isPdf(file: File): boolean {
  return file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')
}

// The hosting answers these while the server is down or waking up: worth retrying
const NOT_ANSWERING = [502, 503, 504]

async function post<T>(path: string, body: BodyInit, type: string): Promise<T> {
  let answer: Response
  try {
    answer = await fetch(path, { method: 'POST', body, headers: { 'Content-Type': type } })
  } catch {
    throw new ApiError('unavailable')
  }
  const data: unknown = await answer.json().catch(() => null)
  if (answer.ok && data !== null) return data as T
  if (NOT_ANSWERING.includes(answer.status)) throw new ApiError('unavailable')
  throw new ApiError(errorKind(data))
}

// A code the front knows, or failed: the server answered but retrying would fail again
function errorKind(data: unknown): ErrorKind {
  const code = (data as { error?: string } | null)?.error
  return code && code in ERRORS ? (code as ErrorKind) : 'failed'
}
