/** Requests to the backend; every failure becomes the error screen to show. */

import { ERRORS, type ErrorKind } from '../config/errors'
import type { Person, Reading, Result } from '../types'

export class ApiError extends Error {
  kind: ErrorKind

  constructor(kind: ErrorKind) {
    super(kind)
    this.kind = kind
  }
}

// The PDF travels as the raw body: a form could be written to disk in the server
export function readPdf(file: File): Promise<Reading> {
  return post('/api/read', file, 'application/pdf')
}

export function calculate(person: Person): Promise<Result> {
  return post('/api/calculate', JSON.stringify(person), 'application/json')
}

export function isPdf(file: File): boolean {
  return file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')
}

async function post<T>(path: string, body: BodyInit, type: string): Promise<T> {
  let answer: Response
  let data: unknown
  try {
    answer = await fetch(path, { method: 'POST', body, headers: { 'Content-Type': type } })
    data = await answer.json()
  } catch {
    throw new ApiError('unavailable')
  }
  if (!answer.ok) throw new ApiError(errorKind(data))
  return data as T
}

function errorKind(data: unknown): ErrorKind {
  const code = (data as { error?: string }).error
  return code && code in ERRORS ? (code as ErrorKind) : 'unavailable'
}
