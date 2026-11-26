/** ?demo=... links that open a screen directly, with made-up data and without the backend. */

import type { Screen } from '../App'
import type { Answers, Mode, Reading, Result } from '../types'
import { QUESTIONS } from './questions'

// The groups add up to bio_age − age
const EXAMPLE_RESULT: Result = {
  age: 45,
  bio_age: 42.4,
  margin: 2,
  blood: { minerals: null, sugar: 0.4, red_cells: -0.3, defences: 0.2, liver: -0.4, kidney: -0.8, weight: 0.9, other: -1.2 },
  habits: { smoking: -0.9, exercise: -0.7, sitting: 0.3, sleep: -0.1 },
}

const EXAMPLE_READING: Reading = {
  lab_values: {},
  age: 45,
  sex: null,
  odd: [
    { variable: 'potassium', text: '9,8', unit: 'mmol/L', factor: 1 },
    { variable: 'glucose', text: '980', unit: 'mg/dL', factor: 1 },
  ],
}

// Without age nor sex, so every question is asked
const QUESTIONS_READING: Reading = { lab_values: {}, age: null, sex: null, odd: [] }

type Demo = { screen: Screen; result?: Result; reading?: Reading; answers?: Answers; mode?: Mode; question?: string }

// ?demo=<question id> → that question, in the mode with habits
const QUESTION_DEMOS: Record<string, Demo> = Object.fromEntries(
  QUESTIONS.map(({ id }) => [id, { screen: 'questions', reading: QUESTIONS_READING, mode: 'full', question: id }]),
)

// ?demo=<name> → screen it opens and its data
const DEMOS: Record<string, Demo> = {
  ...QUESTION_DEMOS,
  reading: { screen: 'reading' },
  calculating: { screen: 'calculating' },
  result: { screen: 'result', result: EXAMPLE_RESULT },
  older: {
    screen: 'result',
    result: {
      age: 82,
      bio_age: 84.3,
      margin: 5.4,
      blood: { minerals: null, sugar: 0.4, red_cells: 0.6, defences: -0.2, liver: -0.4, kidney: 1.3, weight: -0.3, other: 1.1 },
      habits: { smoking: -0.4, exercise: 0.3, sitting: 0.2, sleep: -0.3 },
    },
  },
  odd_value: { screen: 'odd_value', reading: EXAMPLE_READING },
  impossible: { screen: 'impossible' },
  impossible_bmi: { screen: 'impossible_bmi', answers: { weight: 300, height: 120 } },
  too_young: { screen: 'too_young' },
  too_old: { screen: 'too_old' },
  unreadable: { screen: 'unreadable' },
  too_few: { screen: 'too_few' },
  unavailable: { screen: 'unavailable' },
  failed: { screen: 'failed' },
}

export function startingDemo(): Demo {
  const name = new URLSearchParams(window.location.search).get('demo')
  return (name && DEMOS[name]) || { screen: 'landing' }
}
