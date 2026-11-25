/** Puts together what the backend needs to calculate: what the PDF gave plus the answers. */

import type { Corrections } from '../components/ImpossibleValue'
import type { Answers, Mode, Person, Reading } from '../types'

export function missingFrom(reading: Reading): string[] {
  return (['sex', 'age'] as const).filter((field) => reading[field] === null)
}

/** Corrections are in the unit of the lab; the model uses its own. Corrected values are no longer odd. */
export function withCorrections(reading: Reading, corrections: Corrections): Reading {
  const lab_values = { ...reading.lab_values }
  for (const odd of reading.odd) if (odd.variable in corrections) lab_values[odd.variable] = corrections[odd.variable] * odd.factor
  return { ...reading, lab_values, odd: reading.odd.filter((odd) => !(odd.variable in corrections)) }
}

export function buildPerson(reading: Reading, answers: Answers, mode: Mode): Person {
  const { sex, age, weight, height, smoking, physical_activity, sedentary_hours, sleep_hours } = answers
  return {
    lab_values: reading.lab_values,
    sex: reading.sex ?? sex,
    age: reading.age ?? age,
    weight,
    height,
    habits: mode === 'full' ? { smoking, physical_activity, sedentary_hours, sleep_hours } : null,
  }
}
