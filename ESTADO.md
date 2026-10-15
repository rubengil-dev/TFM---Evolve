# Estado

## PRÓXIMA SESIÓN
Explorar NHANES (incluida la mortalidad enlazada) para fijar variables:
1. Ver qué ciclos de NHANES tienen mortalidad enlazada y qué biomarcadores hay en cada uno (algunos cambian de nombre o método entre ciclos, p. ej. la PCR frente a la PCR ultrasensible).
2. Cruzar esa lista con los parámetros habituales de una analítica española, para ver qué variables son realistas.
3. Comprobar qué variables de PhenoAge salen normalmente en una analítica española y cuáles no.
4. Antes de esto hay que decidir el entorno mínimo de Python para el análisis (ver decisiones abiertas).

## Hecho
- Entrega 1: documento con las 4 ideas de TFM (`Docs/Entregas/01_ideas_producto.md`). Elegida la Idea 4.
- Setup del proyecto para trabajar con Claude: `CLAUDE.md`, `CONTEXTO.md`, `ESTADO.md`.

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
- Estructura de carpetas del repo y `.gitignore` (datos de NHANES y analíticas reales fuera del repo).
- Conseguir analíticas de ejemplo (sintéticas o anonimizadas) de distintos laboratorios españoles para probar el parser.

## Problemas conocidos
- En git el archivo de la entrega figura como `01_ideas_producto.MD` (mayúsculas) y en disco como `.md`. En Windows no da problemas, pero conviene unificarlo.
- La rama local `main` va 1 commit por delante de `origin/main` ("Idea 4 Selected", sin push).
