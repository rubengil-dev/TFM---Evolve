# Estado

## PRÓXIMA SESIÓN
1. Revisión del código juntos. Ya revisados y OK: `config/paths.py`, `config/sources.py`, `utils/nhanes.py`, `main.py`. Faltan, línea a línea y por separado: `utils/data_download.py` → `pipeline/download_bronze.py`. Imports sin comentarios, con una línea en blanco entre externos e internos (`src…`). Yo corrijo los comentarios y Claude aprende el estilo; al terminar, el estilo de comentarios se documenta en `CLAUDE.md`.
2. Revisión por mi parte de lo descargado en `data/01_bronze/`. Lo que sobre se quita de `DATASETS` en `sources.py`, no se borra a mano.
3. Silver: leer los `.xpt` y la mortalidad (`.dat` de ancho fijo), armonizar nombres de variables entre ciclos, unir por SEQN.

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

Datos decididos: **NHANES continuo 1999-2018** (10 ciclos), sin NHANES III (otros métodos de laboratorio y otro formato). Mortalidad pública con seguimiento hasta 31/12/2019 (existe versión hasta 2022, pero es de acceso restringido). El seguimiento corto de los últimos ciclos se trata como censura en el modelo de supervivencia, sin repesar; sí habrá que usar los pesos muestrales de NHANES.

Estructura de código (todo en `src/`, cada archivo gestiona sus propios imports):
- `src/config/paths.py`: rutas internas (raíz, capas de datos).
- `src/config/sources.py`: fuentes externas (URLs, ciclos, tabla de ficheros por ciclo, ajustes de descarga).
- `src/pipeline/`: un archivo por paso con una función `run()`: `download_bronze.py` y, más adelante, `build_silver.py` y `build_gold.py`. Sin bloque `if __name__ == "__main__"`: solo `main` arranca cosas.
- `src/utils/`: funciones compartidas, un archivo por tema (`data_download.py`: descarga segura; `nhanes.py`: nombres de ciclo). Regla: una función sale a `utils` cuando no es específica del paso; las específicas se quedan en el paso, como funciones con nombre claro para que `run()` se lea como un índice.
- `src/main.py`: punto de entrada del pipeline, llama a cada `run()` en orden. Se ejecuta desde la raíz: `.venv/Scripts/python -m src.main`. La app tendrá su propio punto de entrada.
- Las iteraciones se hacen en notebooks; los `.py` son el código definitivo.

Bronze (reanudable: salta lo que ya está en disco; `data/01_bronze/manifest.csv` con fichero, URL, tamaño y fecha de descarga): 400 ficheros, ~419 MB. Una carpeta por ciclo (`data/01_bronze/<ciclo>/`) con todo lo del ciclo, incluida la mortalidad, y el nombre original de la CDC (no se renombra en Bronze). Capas numeradas para que el orden alfabético sea el del proceso: `01_bronze`, `02_silver`, `03_gold`. Solo lo que sirve al producto:
- DEMO, BMX (medidas corporales), BPX (tensión).
- Analítica: BIOPRO, CBC, GHB, GLU (ayunas), INS (fichero propio desde 2013; antes va dentro de GLU), TCHOL, HDL (dentro de TCHOL hasta 2004), TRIGLY (ayunas, TG y LDL), CRP (estándar hasta 2010, no medida 2011-2014, ultrasensible desde 2015), VID (vitamina D, 2001-2018; 2001-2006 convertida por la CDC a LC-MS/MS), ALB_CR (albúmina/creatinina en orina), FASTQX (horas de ayuno; en 1999-2004 se llama PH).
- Cuestionarios de hábitos (para un posible modo "avanzado"; se descargan aunque el MVP no los use):
  - SMQ (tabaco), 10 ciclos.
  - ALQ (alcohol): frecuencia (`ALQ120Q/U` hasta 2016, `ALQ121` en 2017) y bebidas por día (`ALQ130`), 10 ciclos. En el formulario, la segunda pregunta solo si no marca "nunca".
  - PAQ (actividad): nivel de ejercicio, 10 ciclos, pero con formato distinto antes y después de 2007 (`PAD200`/`PAD320` vs. `PAQ650`/`PAQ665`): hay que armonizar. Tiempo sentado (`PAD680`), 2007-2018.
  - DBQ (dieta): comida rápida (`DBD900`), 2007-2018. Dieta autovalorada (`DBQ700`), 2005-2018: dudosa por subjetiva.
  - SLQ (sueño): horas (`SLD010H` 2005-2014, `SLD012` 2015-2018).
  - No se incluye la salud general autovalorada (HSQ): subjetiva y poco informativa.
- Opcionales: CVX (VO2 max estimado, 1999-2004) y DXX (DXA, 1999-2006 y 2011-2018).
- En 1999-2004 los ficheros de laboratorio tienen otros nombres (LAB18, L40_B…); la tabla está en `sources.py`.
- Huecos de la tabla verificados contra el catálogo oficial de la CDC. Revisado también el catálogo completo (laboratorio, exploración, cuestionarios) en busca de ficheros útiles no incluidos. Descartados: ferritina (solo mujeres 12-49 años y niños), PSA (varones ≥40, 5 ciclos), TSH (5 ciclos), B12/folato/homocisteína/ApoB (cobertura irregular), fuerza de prensión, bioimpedancia y acelerómetro (pocos ciclos o no medibles en casa).

A tener en cuenta en Silver: DXX ocupa casi la mitad de Bronze; la DXA de 1999-2006 viene con imputación múltiple (varias filas por SEQN), a comprobar. Glucosa, insulina, TG y LDL solo en el subgrupo de ayunas, con su propio peso muestral.

## Hecho
- Entrega 1: documento con las 4 ideas de TFM (`Docs/Entregas/01_ideas_producto.md`). Elegida la Idea 4.
- Setup para trabajar con Claude (`CLAUDE.md`, `CONTEXTO.md` y `ESTADO.md` en `.claude/`), `.gitignore` y `.gitattributes`.
- Entrevista de producto hecha; conclusiones en CONTEXTO.
- Entorno `.venv` (Python 3.11.9) con pandas, numpy, pyarrow, requests, matplotlib e ipykernel; `requirements.txt` generado.
- Carpetas `notebooks/`, `src/` y `data/{bronze,silver,gold}`.

## Decisiones abiertas
- Variables concretas del modelo y mínimo viable de variables (con qué datos faltantes se deja de calcular).
- Arquitectura del modelo (Cox, modelos de árboles para supervivencia, DL…).
- Estrategia para analíticas incompletas: imputación, un modelo por subconjunto de variables, modelos que toleren valores ausentes… Ojo: en NHANES los huecos van por ciclo (CRP, sueño, dieta), mientras que en la app dependen de cada usuario; un modelo que aprenda de los nulos podría confundir "falta el dato" con "es de tal época".
- Modo avanzado con hábitos. Idea mía (no cerrada): dos pestañas arriba, con "simple" (solo subir analítica) por defecto y "avanzada" (cuestionario de botones + analítica). Así se calcula una sola vez y cada uno elige. Descartado de momento "primero simple y luego afinar": son dos procesos y da pereza.
- Uno o dos modelos (solo analítica / analítica + hábitos) o uno que tolere nulos: se decide en la fase de modelo comparando C-index.
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
- El enunciado de la Entrega 02 acepta "script o notebook": basta con `.py` en `src/`, sin notebook espejo.
- Ruta de entregas: el enunciado pide `docs/entregas/` y el repo usa `Docs/Entregas/` (en GitHub son rutas distintas).

## Problemas conocidos
Ninguno.
