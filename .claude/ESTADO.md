# Estado

## PRÓXIMA SESIÓN
1. Comprobar que `CLAUDE.md` se carga desde `.claude/` (si al empezar ya sabes que hay que leer CONTEXTO y ESTADO, funciona).
2. Decidir qué ciclos de NHANES se usan (los continuos 1999-2018 tienen mortalidad enlazada hasta 2019; NHANES III, 1988-1994, aporta más seguimiento y defunciones pero tiene otro formato).
3. Script/notebook de descarga a Bronze (`data/bronze/`).

## Plazos
- Entrega 02 (datos y preparación): ~finales de octubre de 2026, fecha por confirmar.
- Entrega final: diciembre de 2026, día por confirmar.

## En curso: Entrega 02 "Datos y preparación"
Lo que pide el enunciado:
- Documento `docs/entregas/02_datos_y_preparacion.md` con 5 apartados: (1) qué datos necesita el producto (qué es una observación, imprescindibles vs. deseables, granularidad); (2) fuentes, acceso, cobertura, actualización, estabilidad y alternativa si la fuente falla; (3) licencia, privacidad y minimización; (4) flujo Bronze → Silver → Gold, dejando claro qué es cada fila del Gold y sus columnas principales; (5) riesgos y limitaciones en 3-5 líneas.
- Muestra pequeña de los datos o instrucciones de acceso (nada de datasets grandes).
- Script o notebook ordenado que reproduzca las transformaciones hasta el Gold.
- No hay que entrenar ningún modelo. Pensado para dos semanas: mejor pequeño y bien explicado que sobredimensionado.

Ideas ya habladas para el documento: NHANES es de dominio público y viene desidentificado (la mortalidad pública está perturbada por el NCHS), así que no hay que anonimizar, solo minimizar variables. Alternativa si NHANES no estuviera disponible: UK Biobank (requiere solicitud y es de pago). En NHANES cada ciclo es una muestra independiente: una fila del Gold = una persona.

## Hecho
- Entrega 1: documento con las 4 ideas de TFM (`Docs/Entregas/01_ideas_producto.md`). Elegida la Idea 4.
- Setup para trabajar con Claude (`CLAUDE.md`, `CONTEXTO.md` y `ESTADO.md` en `.claude/`), `.gitignore` y `.gitattributes`.
- Entrevista de producto hecha; conclusiones en CONTEXTO.
- Entorno `.venv` (Python 3.11.9) con pandas, numpy, pyarrow, requests, matplotlib e ipykernel; `requirements.txt` generado.
- Carpetas `notebooks/`, `src/` y `data/{bronze,silver,gold}`.

## Decisiones abiertas
- Ciclos de NHANES a usar (con o sin NHANES III).
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
- Stack de front y de backend, y estructura de carpetas de la app.
- Hosting.
- Separar dependencias de la app y del análisis en el despliegue (el `pip freeze` actual incluye Jupyter).

## Pendiente
- Conseguir analíticas de ejemplo de distintos laboratorios españoles para probar el parser (tengo PDFs propios para `private/`).
- Preguntar al profesor si los notebooks deben quedarse en el repo final.
- Ruta de entregas: el enunciado pide `docs/entregas/` y el repo usa `Docs/Entregas/` (en GitHub son rutas distintas).

## Problemas conocidos
Ninguno.
