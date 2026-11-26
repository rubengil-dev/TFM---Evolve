/** Types shared by several files: the modes, the questions and the answers. */

/** quick = blood test only; full = blood test + habits questionnaire. */
export type Mode = 'quick' | 'full'

/** Answers by question id (a number or the value of the chosen option). */
export type Answers = Record<string, number | string>

export type ChoiceOption = {
  value: string
  label: string
  detail?: string
  icon: 'female' | 'male' | 'never' | 'former' | 'current' | 'intense' | 'moderate' | 'none'
}

type BaseQuestion = {
  id: string
  title: string
  hint?: string
  modes: Mode[]
  onlyIfMissing?: boolean
}

export type ChoiceQuestion = BaseQuestion & { kind: 'choice'; options: ChoiceOption[] }

export type NumberQuestion = BaseQuestion & {
  kind: 'number'
  min: number
  max: number
  step: number
  start: number
  unit: string
}

export type Question = ChoiceQuestion | NumberQuestion

/** Years a group adds (+) or takes away (−) against a typical person of the same age and sex; null = not in the blood test. */
export type GroupYears = Record<string, number | null>

/** A value outside what is possible, as the PDF shows it; `text` keeps its decimals, e.g. "9,8". */
export type OddValue = {
  variable: string
  text: string
  unit: string
  /** Lab unit → model unit. */
  factor: number
}

/** What the backend corrected, in model units, and what is still impossible. */
export type Correction = {
  lab_values: Record<string, number>
  odd: OddValue[]
}

/** What the backend reads from a PDF (schemas.py); null = the PDF lacks it. */
export type Reading = {
  lab_values: Record<string, number>
  age: number | null
  sex: string | null
  odd: OddValue[]
}

/** What the backend needs to calculate (schemas.py, which checks it); habits only in the full mode. */
export type Person = {
  lab_values: Record<string, number>
  age: number | string
  sex: number | string
  weight: number | string
  height: number | string
  habits: Answers | null
}

/** What the backend returns for one person (schemas.py). */
export type Result = {
  age: number
  bio_age: number
  margin: number | null
  blood: GroupYears
  habits: Record<string, number> | null
}
