/** Texts of each error screen: title (plain and highlighted line), what happened, what to do and an optional warning. */

import { MAX_AGE, MIN_AGE } from './limits'

export type ErrorKind = 'unreadable' | 'too_few' | 'impossible' | 'too_young' | 'too_old' | 'unavailable'

type ErrorText = { title: [string, string]; text: string; steps: string[]; warning?: string; action?: 'upload' | 'retry' }

// unreadable also covers a file that is not a PDF or a PDF that is not a blood test;
// unavailable (no answer from the backend) is the only one the backend does not send
export const ERRORS: Record<ErrorKind, ErrorText> = {
  unreadable: {
    title: ['No puedo', 'leer este PDF'],
    text: 'No encuentro en él los valores de una analítica de sangre.',
    steps: [
      'Descarga el PDF original desde la web o la app de tu laboratorio.',
      'No uses fotos, capturas ni escaneos.',
      'Comprueba que es una analítica de sangre.',
    ],
    action: 'upload',
  },
  too_few: {
    title: ['No puedo', 'calcular tu edad'],
    text: 'Tu analítica no trae suficientes valores para calcularla con fiabilidad.',
    steps: ['Prueba con una analítica más completa: hemograma y bioquímica.', 'Comprueba que el PDF tiene todas sus páginas.'],
    action: 'upload',
  },
  impossible: {
    title: ['No puedo', 'calcular tu edad'],
    text: 'Con un valor así, darte una edad sería engañoso: no es lo habitual en una analítica de rutina.',
    steps: ['Comprueba que el valor es el que aparece en tu analítica.', 'Si lo he leído mal, sube el PDF otra vez y corrígelo.'],
    warning: 'Si el valor es real, acude a un médico con urgencia.',
    action: 'upload',
  },
  too_young: {
    title: ['No puedo', 'calcular tu edad'],
    text: `La calculadora es a partir de ${MIN_AGE} años: antes, los valores normales de una analítica son otros.`,
    steps: [],
  },
  too_old: {
    title: ['No puedo', 'calcular tu edad'],
    text: 'Has vivido tanto que te has salido de mi calculadora.',
    steps: [`Solo llega hasta los ${MAX_AGE} años. ¡Enhorabuena!`],
  },
  unavailable: {
    title: ['No puedo', 'calcular tu edad'],
    text: 'Ups, ha ocurrido un error.',
    steps: ['Vuelve a intentarlo.', 'Si sigue sin funcionar, te sugiero que le des un golpe al ordenador.'],
    action: 'retry',
  },
}
