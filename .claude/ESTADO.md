# Estado

## PRÓXIMA SESIÓN
Gold hecho y en `main`. Entrega 02 a falta de mi revisión del documento (`docs/entregas/02_datos_y_preparacion.md`, apartado 1 reescrito: imprescindible/deseable a nivel de qué datos conseguir) y de la muestra `docs/entregas/02_gold_sample.csv`: ambos sin commitear. Orden:
1. Revisar el documento; con el OK, commitear documento y muestra.
2. Empezar la fase de modelo: estrategia de huecos, arquitectura (Cox primero) y elección entre variables correlacionadas.

## CONSTRUIDO

### Estructura del repo
- `docs/entregas/`: entregas. Hecha la 01 (`01_ideas_producto.md`, 4 ideas; elegida la 4). La 02 (`02_datos_y_preparacion.md`) redactada, con su muestra `02_gold_sample.csv`.
- `notebooks/02_gold_sample.ipynb`: saca 100 filas de Gold (semilla 5) a `docs/entregas/02_gold_sample.csv` para la entrega. No es parte del pipeline; no importa nada de `src/`.
- `.claude/`: `CLAUDE.md` (cómo trabajar), `CONTEXTO.md` (decisiones de fondo), `ESTADO.md` (este), `HISTORICO.md` (registro por sesión), `ESTILO.md` (mi estilo de código, portable a otros proyectos).
- Entorno `.venv` (Python 3.11.9) con pandas, numpy, pyarrow, requests, matplotlib, ipykernel, lifelines (modelos de supervivencia) y nbformat/nbclient (ejecutar notebooks); `requirements.txt` generado con `pip freeze`.
- `notebooks/01_exploration_raw.ipynb`: exploración de Silver raw (ejecutado, con resultados guardados). No importa nada de `src/`.
- `data/` (ignorada en git): `01_bronze/`, `02_silver/`, `03_gold/`. Numeradas para que el orden alfabético sea el del proceso.
- `src/`:
  - `main.py`: punto de entrada del pipeline, llama a cada `run()` en orden. Desde la raíz: `.venv/Scripts/python -m src.main`. Es el único con el bloque `if __name__ == "__main__"`.
  - `config/paths.py`: rutas internas (raíz y capas de datos).
  - `config/sources.py`: fuentes externas (URLs, ciclos, tabla de ficheros por dataset y ciclo, ajustes de descarga).
  - `utils/data_download.py`: descarga segura (reintentos, `.part` hasta completar, valida que no sea una página de error).
  - `utils/nhanes.py`: `cycle_label` (1999 → `1999_2000`).
  - `pipeline/download_bronze.py`: `run()` = lista de ficheros → descarga lo que falta → manifiesto → resumen.
  - `pipeline/build_raw_silver.py`: `run()` = por ciclo, unir ficheros → filtrar población → renombrar alias; después apilar → guardar → resumen.
  - `pipeline/build_clean_silver.py`: `run()` = población → correcciones CDC → códigos "no sabe/no contesta" → variables (renombradas, derivadas, tensión, cuestionarios, pesos) → guardar → resumen.
  - `config/study.py`: parámetros del estudio (edad 18-79, ayuno mínimo 8 h, respuestas de frecuencia de alcohol).
  - `config/renames.py`: `RENAMES` (alias de laboratorio entre ciclos; los cuestionarios no se renombran) y `CLEAN_NAMES` (nombre NHANES → nombre legible, con unidades: sirve de diccionario de datos).
  - `config/corrections.py`: ecuaciones de corrección de la CDC (creatinina 1999-2000 y 2005-2006; 13 analitos de 2017-2018 por cambio de analizador).
  - `config/sources.py`: además, códigos de los cuestionarios (días de alcohol por respuesta, códigos de "no sabe/no contesta" por variable).
  - `pipeline/build_gold.py`: `run()` = Silver clean → columnas de Gold + features derivadas → seguimiento 0 → 0,1 meses → guardar → resumen.
  - `config/column_roles.py`: papel de cada columna de Gold (identificación, desenlace, predictores de Silver clean).
  - `utils/features.py`: fórmulas de las features derivadas (compartidas con la futura app) y CKD-EPI 2021.
  - `config/study.py`: además, `FOLLOW_UP_MIN` (0,1 meses).
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
- `data/02_silver/silver_raw.parquet` (24,6 MB): 54.809 personas (18-79 años, elegibles para mortalidad), 6.271 defunciones, 993 columnas, una fila por persona. Defunciones por ciclo de 1.268 (1999-2000) a 86 (2017-2018), por el seguimiento más corto.
- Unión: base = participantes de DEMO. Columnas repetidas entre ficheros: si coinciden (admitiendo redondeo), se rellena y no se repite; si no, `NOMBRE_FICHERO`. Ahora mismo no queda ninguna repetida (el peso de ayunas de 2003-2004 venía redondeado distinto en dos ficheros). DXA 1999-2006: media de las 5 imputaciones.
- Comprobado: SEQN único, edad 18-79, renombres funcionando (HDL, creatinina, vitamina D y orina con datos en todos sus ciclos).

### Exploración de raw (notebook 01)
- Criterio de variables acordado: todo lo de una analítica de rutina española, lo que se pide a menudo (p. ej. vitamina D), lo que el usuario sabe sin pensar (edad, sexo, peso, talla) y un cuestionario de ~10 preguntas de botones (tabaco, alcohol x2, actividad, sedentarismo, sueño, comida rápida). Sin etnia. VO2 max y DXA, probablemente fuera (el usuario no los sabe). Entre variables con correlación > 0,8-0,85, solo una.
- 76 candidatas mirando cobertura, distribuciones, saltos entre ciclos, correlaciones y Cox por variable ajustado por edad y sexo.
- Población: 50.969 personas y 5.808 defunciones tras quitar 2.253 sin examen y 1.587 embarazadas (exclusión decidida: analítica alterada).
- Cobertura: analítica general ~93-95% en todos los ciclos; subgrupo en ayunas (glucosa plasmática, LDL, TG, insulina) ~45%; CPK solo 2011-2018.
- Parejas con r ≥ 0,8: colesterol total de los dos ficheros (0,98), TG con y sin ayuno (0,98), hemoglobina-hematocrito (0,96), glucosa con y sin ayuno (0,93), neutrófilos-linfocitos % (−0,93), leucocitos-neutrófilos (0,91), colesterol total-LDL (0,91), IMC-cintura (0,91), VCM-HCM (0,90), peso-IMC/cintura, eosinófilos %-absolutos, hematíes-hematocrito.
- Saltos entre ciclos (>15% en la mediana): fosfatasa alcalina y LDH más altas en 1999-2000 y 2017-2018, urea en 2017-2018 (posible cambio de analizador); bilirrubina y basófilos son artefacto de valores muy redondeados.
- Asociación con mortalidad (orientativa) coherente: PCR, albúmina (protectora), albúmina en orina, RDW, vitamina D (protectora), fosfatasa alcalina, GGT, glucosa, HbA1c, creatinina. VO2 max y % grasa DXA no significativos (pocas defunciones). LDL sale protector (causalidad inversa conocida).

### Silver clean
- `data/02_silver/silver_clean.parquet`: 48.495 personas, 5.425 defunciones, 72 columnas. Fuera: sin examen, embarazadas y sin ningún valor de laboratorio (2.474 personas, 383 defunciones).
- Decisiones aplicadas:
  - Colesterol total: una sola columna (fichero de lípidos, rellenado con bioquímica). LDL fuera (calculado con Friedewald, solo en ayunas, causalidad inversa).
  - Glucosa: suero, todas las personas (el ayuno apenas cambia la mediana). Triglicéridos: solo con ayuno ≥ 8 h (51%).
  - PCR en mg/L en una columna (estándar hasta 2010 + ultrasensible desde 2015). Urea = BUN × 2,14. Cociente albúmina/creatinina en orina en mg/g (coincide con el de NHANES).
  - Correcciones CDC aplicadas y comprobadas (creatinina 1999-2000 de 0,70 a 0,86; fosfatasa alcalina y LDH de 2017-2018 alineadas con el resto).
  - Tensión: media de hasta 4 lecturas; diastólica 0 → vacío.
  - Cuestionarios con respuestas de botón: tabaco (never/former/current), alcohol (never/less_than_weekly/weekly/daily + bebidas por día, 0 si never), actividad (sedentary/moderate/intense), horas sentado, comidas de comida rápida/semana, horas de sueño. Preguntas saltadas → "never"/0.
  - Pesos combinados para 10 ciclos (`weight_exam`, `weight_fasting`), suman ~212 millones.
  - VO2 max y DXA fuera. No se recortan extremos ni se rellenan huecos (eso es Gold).
- Se mantienen las dos variables de cada pareja correlacionada (para las ecuaciones de relleno de la app); Gold elige cuál entra al modelo.
- Limitaciones vistas: fosfatasa alcalina y LDH más altas en 1999-2000 (sin ecuación CDC); urea algo más alta en 2017-2018 incluso corregida; actividad física con salto en 2007 por el cambio de cuestionario (intensa 37% → 22%); alcohol sin dato para 18-19 años en 1999-2006 (cuestionario solo para mayores de 20).

### Gold
- `data/03_gold/gold.parquet` (4,6 MB): 48.495 personas, 5.425 defunciones, 68 columnas. Una fila = una persona.
- Columnas: identificación (`seqn`, `cycle`, `weight_exam`), desenlace (`follow_up_months`, `death`), edad y sexo, hemograma (12, recuentos absolutos, no %), bioquímica (27, insulina y CPK incluidas), IMC y tensión, hábitos (7) y 12 derivadas: `nlr`, `plr`, `sii`, `non_hdl`, `tg_hdl`, `ast_alt`, `globulin`, `albumin_globulin`, `urea_creatinine`, `egfr` (CKD-EPI 2021 sin raza), `homa_ir`, `pulse_pressure`.
- Fuera de Gold: hematocrito, HCM, neutrófilos (% y absolutos; entran vía NLR/SII), resto de %, peso, talla, cintura, `weight_fasting`, `psu`, `strata`, `death_cause`, `fasting_hours`. Siguen en Silver clean para las ecuaciones de relleno de la app.
- Seguimiento 0 meses (5 defunciones) → 0,1 meses.
- Sin rellenar huecos, sin recortar extremos, sin escalar ni codificar (sexo y hábitos como texto): todo eso aprende de los datos y va al preprocesado, ajustado solo con train.
- Se guardan a propósito variables que son combinación lineal de otras (colesterol total/HDL/no-HDL; proteínas/albúmina/globulinas; sistólica/diastólica/presión de pulso) para elegir el juego en la fase de modelo: en Cox no pueden entrar las tres.
- Correlaciones de Spearman ≥ 0,8 de las derivadas: HOMA-IR-insulina 0,96, TG/HDL-triglicéridos 0,94, no-HDL-colesterol total 0,92, globulinas-albúmina/globulina −0,91, NLR-SII 0,85.
- Cobertura < 90%: CPK 41%, insulina y HOMA-IR 47%, comida rápida 50%, triglicéridos y TG/HDL 54%, horas sentado 64%, sueño 73%, PCR 78%, alcohol 87%, vitamina D 89%.
- Pipeline completo (sin descarga): ~45 s.

## PENDIENTE

### Plazos
- Entrega 02 (datos y preparación): ~finales de octubre de 2026, fecha por confirmar.
- Entrega final: diciembre de 2026, día por confirmar.

### Entrega 02 "Datos y preparación"
- Documento y muestra hechos según el enunciado (5 apartados, muestra pequeña, `src.main` reproduce hasta Gold). El notebook de muestra está commiteado; documento y CSV, pendientes de mi revisión.

### Tareas
- Revisión por mi parte de lo descargado en `data/01_bronze/`. Lo que sobre se quita de `DATASETS` en `sources.py`, no se borra a mano.
- Conseguir analíticas de ejemplo de distintos laboratorios españoles para probar el parser (tengo PDFs propios para `private/`).
- Preguntar al profesor si los notebooks deben quedarse en el repo final.

### Notas para la app
- Relleno desde la pareja: si el usuario trae la variable "pareja" y no la que usa el modelo (p. ej. hematocrito sin hemoglobina), estimarla con una ecuación sacada de NHANES. Solo para parejas con correlación alta.
- El filtrado glomerular (CKD-EPI) suele venir en las analíticas españolas: no es variable del modelo (redundante con creatinina, edad y sexo), pero el parser puede usarlo para recuperar la creatinina si falta.
- Triglicéridos: el modelo se entrena con valores en ayunas; la analítica española es en ayunas. Mejora futura: usar también los valores sin ayuno corrigiéndolos.

### Decisiones abiertas
- Variables concretas del modelo (las candidatas están en Gold) y mínimo viable de variables (con qué datos faltantes se deja de calcular).
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
