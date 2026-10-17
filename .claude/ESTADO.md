# Estado

## PRÓXIMA SESIÓN
1. Entrega 02. Hecho Silver raw. Siguiente: notebook de exploración sobre `raw.parquet` → elegir variables juntos (criterio por hablar antes de proponer lista) → Silver `clean` → Gold → muestra pequeña → documento `02_datos_y_preparacion.md` (lo que pide el enunciado, en Pendiente).

## CONSTRUIDO

### Estructura del repo
- `Docs/Entregas/`: entregas. Hecha la 01 (`01_ideas_producto.md`, 4 ideas; elegida la 4).
- `.claude/`: `CLAUDE.md` (cómo trabajar), `CONTEXTO.md` (decisiones de fondo), `ESTADO.md` (este), `HISTORICO.md` (registro por sesión), `ESTILO.md` (mi estilo de código, portable a otros proyectos).
- Entorno `.venv` (Python 3.11.9) con pandas, numpy, pyarrow, requests, matplotlib e ipykernel; `requirements.txt` generado con `pip freeze`.
- `notebooks/`: vacía.
- `data/` (ignorada en git): `01_bronze/`, `02_silver/`, `03_gold/`. Numeradas para que el orden alfabético sea el del proceso.
- `src/`:
  - `main.py`: punto de entrada del pipeline, llama a cada `run()` en orden. Desde la raíz: `.venv/Scripts/python -m src.main`. Es el único con el bloque `if __name__ == "__main__"`.
  - `config/paths.py`: rutas internas (raíz y capas de datos).
  - `config/sources.py`: fuentes externas (URLs, ciclos, tabla de ficheros por dataset y ciclo, ajustes de descarga).
  - `utils/data_download.py`: descarga segura (reintentos, `.part` hasta completar, valida que no sea una página de error).
  - `utils/nhanes.py`: `cycle_label` (1999 → `1999_2000`).
  - `pipeline/download_bronze.py`: `run()` = lista de ficheros → descarga lo que falta → manifiesto → resumen.
  - `pipeline/build_raw_silver.py`: `run()` = por ciclo, unir ficheros → filtrar población → renombrar alias; después apilar → guardar → resumen.
  - `config/study.py`: parámetros del estudio (edad 18-79).
  - `config/renames.py`: alias de variables de laboratorio entre ciclos (misma medida y unidad, otro nombre). Los cuestionarios no se renombran aquí.
  - `utils/nhanes.py`: además de `cycle_label`, `read_xpt` (SEQN entero, ceros falsos de SAS → 0), `read_mortality` (ancho fijo, posiciones en `sources.py`) y `dxa_average_imputations`.

Reglas de código: cada archivo gestiona sus imports; una función va a `utils` (un archivo por tema) cuando no es específica del paso; las específicas se quedan en el paso, con nombres claros para que `run()` se lea como un índice. Las iteraciones se hacen en notebooks; los `.py` son el código definitivo.

### Bronze
- Reanudable: salta lo que ya está en disco. `data/01_bronze/manifest.csv`: fichero, URL, tamaño y fecha de descarga.
- 400 ficheros, ~419 MB. Una carpeta por ciclo (`data/01_bronze/<ciclo>/`) con todo lo del ciclo, mortalidad incluida, con el nombre original de la CDC (en Bronze no se renombra).
- Mortalidad pública con seguimiento hasta 31/12/2019 (la versión hasta 2022 es de acceso restringido).
- Contenido:
  - DEMO, BMX (medidas corporales), BPX (tensión).
  - Analítica: BIOPRO, CBC, GHB, GLU (ayunas), INS (fichero propio desde 2013; antes va dentro de GLU), TCHOL, HDL (dentro de TCHOL hasta 2004), TRIGLY (ayunas, TG y LDL), CRP (estándar hasta 2010, no medida 2011-2014, ultrasensible desde 2015), VID (vitamina D, 2001-2018; 2001-2006 convertida por la CDC a LC-MS/MS), ALB_CR (albúmina/creatinina en orina), FASTQX (horas de ayuno; en 1999-2004 se llama PH).
  - Opcionales: CVX (VO2 max estimado, 1999-2004) y DXX (DXA, 1999-2006 y 2011-2018).
  - Cuestionarios de hábitos (para un posible modo avanzado; el MVP puede no usarlos):
    - SMQ (tabaco), 10 ciclos.
    - ALQ (alcohol): frecuencia (`ALQ120Q/U` hasta 2016, `ALQ121` en 2017) y bebidas por día (`ALQ130`), 10 ciclos. En el formulario, la segunda pregunta solo si no marca "nunca".
    - PAQ (actividad): nivel de ejercicio, 10 ciclos, con formato distinto antes y después de 2007 (`PAD200`/`PAD320` vs. `PAQ650`/`PAQ665`), a armonizar en tres niveles. Tiempo sentado (`PAD680`), 2007-2018.
    - DBQ (dieta): comida rápida (`DBD900`), 2007-2018. Dieta autovalorada (`DBQ700`, 2005-2018): fuera del formulario por subjetiva; se mantiene en los datos por si aporta en el modelo.
    - SLQ (sueño): horas (`SLD010H` 2005-2014, `SLD012` 2015-2018).
- En 1999-2004 los ficheros tienen otros nombres (LAB18, L40_B…); la tabla está en `sources.py`.
- Huecos de la tabla verificados contra el catálogo oficial de la CDC. Revisado también el catálogo completo en busca de ficheros útiles. Descartados: ferritina (solo mujeres 12-49 años y niños), PSA (varones ≥40, 5 ciclos), TSH (5 ciclos), B12/folato/homocisteína/ApoB (cobertura irregular), fuerza de prensión, bioimpedancia, acelerómetro (pocos ciclos o no medibles en casa) y salud general autovalorada (subjetiva).

### Silver raw
- `data/02_silver/raw.parquet` (24,6 MB): 54.809 personas (18-79 años, elegibles para mortalidad), 6.271 defunciones, 993 columnas, una fila por persona. Defunciones por ciclo de 1.268 (1999-2000) a 86 (2017-2018), por el seguimiento más corto.
- Unión: base = participantes de DEMO. Columnas repetidas entre ficheros: si coinciden (admitiendo redondeo), se rellena y no se repite; si no, `NOMBRE_FICHERO`. Ahora mismo no queda ninguna repetida (el peso de ayunas de 2003-2004 venía redondeado distinto en dos ficheros). DXA 1999-2006: media de las 5 imputaciones.
- Comprobado: SEQN único, edad 18-79, renombres funcionando (HDL, creatinina, vitamina D y orina con datos en todos sus ciclos).

### Para Silver clean / Gold
- 2.253 personas (~4%) solo hicieron la entrevista en casa (cuestionarios) y no fueron al examen: sin analítica ni medidas. Decidido: fuera en la limpieza.
- DXA 2011-2018 solo en ~50% (en esos ciclos se hizo a 8-59 años). VO2 max solo ~28% (1999-2004, 12-49 años).
- Glucosa, insulina, TG y LDL solo en el subgrupo de ayunas, con su propio peso muestral.
- Cuestionarios con códigos que cambian entre ciclos: armonizar revisando cada codebook.
- En el modelo: el seguimiento corto de los últimos ciclos se trata como censura, sin repesar. Hay que usar los pesos muestrales de NHANES.

## PENDIENTE

### Plazos
- Entrega 02 (datos y preparación): ~finales de octubre de 2026, fecha por confirmar.
- Entrega final: diciembre de 2026, día por confirmar.

### Entrega 02 "Datos y preparación"
Lo que pide el enunciado:
- Documento `docs/entregas/02_datos_y_preparacion.md` con 5 apartados: (1) qué datos necesita el producto (qué es una observación, imprescindibles vs. deseables, granularidad); (2) fuentes, acceso, cobertura, actualización, estabilidad y alternativa si la fuente falla; (3) licencia, privacidad y minimización; (4) flujo Bronze → Silver → Gold, dejando claro qué es cada fila del Gold y sus columnas principales; (5) riesgos y limitaciones en 3-5 líneas.
- Muestra pequeña de los datos o instrucciones de acceso (nada de datasets grandes).
- Script o notebook ordenado que reproduzca las transformaciones hasta el Gold (basta con `.py`, sin notebook espejo).
- No hay que entrenar ningún modelo. Pensado para dos semanas: mejor pequeño y bien explicado que sobredimensionado.

Ideas ya habladas para el documento: NHANES es de dominio público y viene desidentificado (la mortalidad pública está perturbada por el NCHS), así que no hay que anonimizar, solo minimizar variables. Alternativa si NHANES no estuviera disponible: UK Biobank (requiere solicitud y es de pago). En NHANES cada ciclo es una muestra independiente: una fila del Gold = una persona.

### Tareas
- Revisión por mi parte de lo descargado en `data/01_bronze/`. Lo que sobre se quita de `DATASETS` en `sources.py`, no se borra a mano.
- Conseguir analíticas de ejemplo de distintos laboratorios españoles para probar el parser (tengo PDFs propios para `private/`).
- Preguntar al profesor si los notebooks deben quedarse en el repo final.
- Ruta de entregas: el enunciado pide `docs/entregas/` y el repo usa `Docs/Entregas/` (en GitHub son rutas distintas).

### Decisiones abiertas
- Variables concretas del modelo y mínimo viable de variables (con qué datos faltantes se deja de calcular).
- Arquitectura del modelo (Cox, modelos de árboles para supervivencia, DL…).
- Estrategia para analíticas incompletas: imputación, un modelo por subconjunto de variables, modelos que toleren valores ausentes… Ojo: en NHANES los huecos van por ciclo (CRP, sueño, dieta), mientras que en la app dependen de cada usuario; un modelo que aprenda de los nulos podría confundir "falta el dato" con "es de tal época".
- Modo avanzado con hábitos. Idea mía (no cerrada): dos pestañas arriba, con "simple" (solo subir analítica) por defecto y "avanzada" (cuestionario de botones + analítica). Así se calcula una sola vez y cada uno elige. Descartado de momento "primero simple y luego afinar": son dos procesos y da pereza.
- Uno o dos modelos (solo analítica / analítica + hábitos) o uno que tolere nulos: se decide en la fase de modelo comparando C-index.
- Cómo calcular y mostrar el margen ± X años.
- Definición de "mejor/peor parámetro". Propuesta para el MVP: cuánto empuja cada parámetro la edad arriba o abajo frente a una persona media de la misma edad y sexo. La versión "distancia al óptimo de cada parámetro" requiere un modelo no lineal.
- Cuántos parámetros mejores/peores se muestran (3, 5, configurable…).
- Umbral de años por encima para remitir al médico: según el error del modelo y la literatura.
- Datos opcionales en la app: en NHANES hay tensión (10 ciclos), DXA (8) y VO2 max (3). Decidir cuáles se piden.
- Soporte de Word: solo si algún laboratorio entrega analíticas en Word.
- Analítica de ejemplo (sintética) para probar la app sin PDF propio: lo consulto con el profesor.
- Diseño del parser de PDF y de la normalización de nombres y unidades.
- Stack de front y de backend, y estructura de carpetas de la app.
- Hosting.
- Separar dependencias de la app y del análisis en el despliegue (el `pip freeze` actual incluye Jupyter).

### Problemas conocidos
Ninguno.
