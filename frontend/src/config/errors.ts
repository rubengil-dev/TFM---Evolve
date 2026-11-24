/** Texts of each error screen: title (plain and highlighted line), what happened, what to do and an optional warning. */

export type ErrorKind = 'unreadable' | 'too_few' | 'impossible' | 'too_young'

type ErrorText = { title: [string, string]; text: string; steps: string[]; warning?: string; canRetry: boolean }

// Youngest age the app calculates for; below it a blood test reads differently and extrapolating makes no sense
export const MIN_AGE = 16

// unreadable also covers a file that is not a PDF or a PDF that is not a blood test
export const ERRORS: Record<ErrorKind, ErrorText> = {
  unreadable: {
    title: ['No puedo', 'leer este PDF'],
    text: 'No encuentro en él los valores de una analítica de sangre.',
    steps: [
      'Descarga el PDF original desde la web o la app de tu laboratorio',
      'No uses fotos, capturas ni escaneos',
      'Comprueba que es una analítica de sangre',
    ],
    canRetry: true,
  },
  too_few: {
    title: ['No puedo', 'calcular tu edad'],
    text: 'Tu analítica no trae suficientes valores para calcularla con fiabilidad.',
    steps: ['Prueba con una analítica más completa: hemograma y bioquímica', 'Comprueba que el PDF tiene todas sus páginas'],
    canRetry: true,
  },
  impossible: {
    title: ['No puedo', 'calcular tu edad'],
    text: 'Con un valor así, darte una edad sería engañoso: no es lo habitual en una analítica de rutina.',
    steps: ['Comprueba que el valor es el que aparece en tu analítica', 'Si lo he leído mal, sube el PDF otra vez y corrígelo'],
    warning: 'Si el valor es real, acude a un médico con urgencia.',
    canRetry: true,
  },
  too_young: {
    title: ['No puedo', 'calcular tu edad'],
    text: `La calculadora es a partir de ${MIN_AGE} años: antes, los valores normales de una analítica son otros.`,
    steps: [],
    canRetry: false,
  },
}
