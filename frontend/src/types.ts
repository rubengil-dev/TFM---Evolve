/** Types shared by several files: the modes, the questions and the answers. */

/** quick = blood test only; full = blood test + habits questionnaire. */
export type Mode = 'quick' | 'full'

/** Answers by question id (a number or the value of the chosen option). */
export type Answers = Record<string, number | string>

export type ChoiceOption = {
  value: string
  label: string
  detail?: string
  icon: 'never' | 'former' | 'current' | 'intense' | 'moderate' | 'none'
}

type BaseQuestion = {
  id: string
  title: string
  hint: string
  modes: Mode[]
  note?: string
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
