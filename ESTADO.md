# Estado

## PRÓXIMA SESIÓN
**Primero, entrevista.** CONTEXTO se escribió a partir de un prompt y de la entrega de ideas, y puede no coincidir con lo que tengo en la cabeza. Hazme preguntas (por bloques, sin agobiar) sobre todo lo que quede ambiguo o sin detallar: producto, usuario, resultado que se muestra, modelo, alcance, plazos y entregas del máster, criterios de evaluación… Con las respuestas, propón los cambios a `CONTEXTO.md` (y a ESTADO si aplica) y espera mi OK antes de aplicarlos.

Después, explorar NHANES (incluida la mortalidad enlazada) para fijar variables:
1. Ver qué ciclos de NHANES tienen mortalidad enlazada y qué biomarcadores hay en cada uno (algunos cambian de nombre o método entre ciclos, p. ej. la PCR frente a la PCR ultrasensible).
2. Cruzar esa lista con los parámetros habituales de una analítica española, para ver qué variables son realistas.
3. Comprobar qué variables de PhenoAge salen normalmente en una analítica española y cuáles no.
4. Antes de esto hay que decidir el entorno mínimo de Python para el análisis (ver decisiones abiertas).

## Hecho
- Entrega 1: documento con las 4 ideas de TFM (`Docs/Entregas/01_ideas_producto.md`). Elegida la Idea 4.
- Setup del proyecto para trabajar con Claude: `CLAUDE.md`, `CONTEXTO.md`, `ESTADO.md`.
- `.gitignore` (excluye `data/` para NHANES, `private/` para analíticas reales, entornos de Python, checkpoints de notebooks y `.env`) y `.gitattributes` (saltos de línea LF en el repo).

## En curso
Nada.

## Decisiones abiertas
- Variables concretas del modelo y mínimo viable de variables.
- Arquitectura del modelo (Cox, modelos de árboles para supervivencia, DL…).
- Estrategia para analíticas incompletas: imputación, un modelo por subconjunto de variables, modelos que toleren valores ausentes…
- Cómo calcular y mostrar la fiabilidad del resultado.
- Diseño del parser de PDF (texto vs. OCR) y de la normalización de nombres y unidades.
- Stack de front y de backend.
- Hosting.
- Idioma de la interfaz.
- Entorno de Python para el análisis (gestor de entornos, notebooks).

## Pendiente
- Estructura de carpetas del repo (se decide junto con el stack).
- Conseguir analíticas de ejemplo (sintéticas o anonimizadas) de distintos laboratorios españoles para probar el parser.

## Problemas conocidos
Ninguno.
