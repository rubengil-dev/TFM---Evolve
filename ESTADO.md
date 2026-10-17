# Estado

## PRÓXIMA SESIÓN
**Primero, la entrega parcial** (hacia finales de octubre de 2026, fecha por confirmar): incluye los datos que se van a usar y parte del procesado. Me pasas el enunciado y la planificamos.

Después, explorar NHANES (incluida la mortalidad enlazada) para fijar variables:
1. Ver qué ciclos de NHANES tienen mortalidad enlazada y qué biomarcadores hay en cada uno (algunos cambian de nombre o método entre ciclos, p. ej. la PCR frente a la PCR ultrasensible).
2. Cruzar esa lista con los parámetros habituales de una analítica española, para ver qué variables son realistas.
3. Comprobar qué variables de PhenoAge salen normalmente en una analítica española y cuáles no.
4. Ver si NHANES tiene tensión arterial, composición corporal y VO2 max (o aproximación) para los datos opcionales.
5. Antes de esto hay que decidir el entorno mínimo de Python para el análisis (ver decisiones abiertas).

## Plazos
- Entrega final: diciembre de 2026 (día por confirmar).
- Entregas parciales por el camino; la siguiente, datos + parte del procesado (~finales de octubre).

## Hecho
- Entrega 1: documento con las 4 ideas de TFM (`Docs/Entregas/01_ideas_producto.md`). Elegida la Idea 4.
- Setup del proyecto para trabajar con Claude: `CLAUDE.md`, `CONTEXTO.md`, `ESTADO.md`.
- `.gitignore` (excluye `data/` para NHANES, `private/` para analíticas reales, entornos de Python, checkpoints de notebooks y `.env`) y `.gitattributes` (saltos de línea LF en el repo).
- Entrevista de producto hecha; CONTEXTO actualizado con sus conclusiones.

## En curso
Nada.

## Decisiones abiertas
- Variables concretas del modelo y mínimo viable de variables (con qué datos faltantes se deja de calcular).
- Arquitectura del modelo (Cox, modelos de árboles para supervivencia, DL…).
- Estrategia para analíticas incompletas: imputación, un modelo por subconjunto de variables, modelos que toleren valores ausentes…
- Cómo calcular y mostrar el margen ± X años.
- Definición de "mejor/peor parámetro". Propuesta para el MVP: cuánto empuja cada parámetro la edad arriba o abajo frente a una persona media de la misma edad y sexo. La versión "distancia al óptimo de cada parámetro" requiere un modelo no lineal.
- Cuántos parámetros mejores/peores se muestran (3, 5, configurable…).
- Umbral de años por encima para remitir al médico: según el error del modelo y la literatura.
- Datos opcionales (tensión, composición corporal, VO2 max): según lo que haya en NHANES.
- Soporte de Word: solo si algún laboratorio entrega analíticas en Word.
- Analítica de ejemplo (sintética) para probar la app sin PDF propio: lo consulto con el profesor.
- Diseño del parser de PDF y de la normalización de nombres y unidades.
- Stack de front y de backend.
- Hosting.
- Entorno de Python para el análisis (gestor de entornos, notebooks).

## Pendiente
- Estructura de carpetas del repo (se decide junto con el stack).
- Conseguir analíticas de ejemplo de distintos laboratorios españoles para probar el parser (tengo PDFs propios para `private/`).

## Problemas conocidos
Ninguno.
