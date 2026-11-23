/** Made-up data used until the backend is connected, and ?demo=... links to open any screen directly. */

import type { Screen } from '../App'
import type { OddValue } from '../components/ImpossibleValue'
import type { Result } from '../types'

export const EXAMPLE_RESULT: Result = {
  age: 45,
  bioAge: 41.6,
  margin: 2,
  blood: { minerals: null, sugar: 0.4, heart: -1.2, red_cells: -0.3, defences: 0.2, liver: -0.4, kidney: -0.8, weight: 0.9 },
  habits: { smoking: -0.9, exercise: -0.7, sitting: 0.3, sleep: -0.1 },
}

// What the PDF lacks; the backend will tell
export const EXAMPLE_MISSING = ['sex']

export const EXAMPLE_ODD_VALUE: OddValue = { label: 'Potasio', text: '9,8', unit: 'mmol/L' }

// ?demo=<name> → screen it opens and changes to the example result
const DEMOS: Record<string, { screen: Screen; result?: Partial<Result> }> = {
  result: { screen: 'result' },
  older: { screen: 'result', result: { age: 82, bioAge: 84.3, margin: 3 } },
  odd_value: { screen: 'odd_value' },
  impossible: { screen: 'impossible' },
  too_young: { screen: 'too_young' },
  unreadable: { screen: 'unreadable' },
  too_few: { screen: 'too_few' },
}

export function startingDemo(): { screen: Screen; result?: Partial<Result> } {
  const name = new URLSearchParams(window.location.search).get('demo')
  return (name && DEMOS[name]) || { screen: 'landing' }
}
