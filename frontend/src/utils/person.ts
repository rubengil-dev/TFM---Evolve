/** Puts together what the backend needs to calculate: what the PDF gave plus the answers. */

import { BMI } from '../config/limits'
import type { Answers, Correction, Mode, Person, Reading } from '../types'

export function missingFrom(reading: Reading): string[] {
  return (['sex', 'age'] as const).filter((field) => reading[field] === null)
}

/** What the backend corrected joins the values; what is still impossible stays odd, in its place, with what was typed. */
export function withCorrection(reading: Reading, correction: Correction): Reading {
  const stillOdd = new Map(correction.odd.map((odd) => [odd.variable, odd]))
  const odd = reading.odd.filter((odd) => !(odd.variable in correction.lab_values)).map((odd) => stillOdd.get(odd.variable) ?? odd)
  return { ...reading, lab_values: { ...reading.lab_values, ...correction.lab_values }, odd }
}

/** Kilos and centimetres that can go together; the backend checks it too. */
export function isPossibleBmi(weight: number, height: number): boolean {
  const bmi = weight / (height / 100) ** 2
  return bmi >= BMI[0] && bmi <= BMI[1]
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
