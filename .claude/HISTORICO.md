# Histórico

Una entrada por sesión, la más reciente arriba. Qué se hizo, decisiones con su motivo, incidencias y commits. El detalle de cada cambio está en git (`git show <hash>`).

## 2026-10-18: Gold y redacción de la Entrega 02
- Entregas renombradas a `docs/entregas/` (lo que pide el enunciado; en GitHub las mayúsculas cuentan).
- Silver clean: fuera también las personas sin ningún valor de laboratorio (2.474, 383 defunciones), que ayer se creía que ya estaban filtradas. Quedan 48.495 personas y 5.425 defunciones. Ficheros renombrados a `silver_raw`/`silver_clean` para que se vea la capa.
- Gold (48.495 × 68): recuentos absolutos del hemograma en lugar de % (los % dependen unos de otros); insulina, CPK y hábitos dentro; 12 features derivadas (NLR, PLR, SII, no-HDL, TG/HDL, AST/ALT, globulinas, albúmina/globulina, urea/creatinina, CKD-EPI 2021 sin raza, HOMA-IR, presión de pulso). Fuera `weight_fasting`, `psu`, `strata`.
- Decidido: en Gold solo fórmulas fijas; rellenar, recortar extremos, escalar y codificar van al preprocesado ajustado con train (recortar percentiles con todo el dataset filtraría el test). Las combinaciones lineales (total/HDL/no-HDL…) se guardan todas para elegir el juego en la fase de modelo. Seguimiento 0 → 0,1 meses. Sin puntuación de hábitos (pesos arbitrarios; el modelo los aprende).
- Fórmulas de las features en `utils/features.py` para que la app use las mismas. La muestra para la entrega sale de un notebook aparte (no del pipeline), semilla 5.
- Documento 02 redactado; apartado 1 rehecho tras revisión (imprescindible/deseable = qué datos conseguir, no qué trae el usuario). Revisado por mí y commiteado con la muestra al final de la sesión.
- Commits: `c241c83` (Gold, filtro de laboratorio, renombres), merge a `main` y push.

## 2026-10-17: Bronze y estructura del código
- Decidido NHANES continuo 1999-2018 sin NHANES III: métodos de laboratorio y formato distintos, y 20 años de seguimiento bastan. El seguimiento corto de los últimos ciclos se trata como censura.
- Script de descarga a Bronze. Primero se intentó descargar todo NHANES (scraping del catálogo): se paró porque el producto solo usa analítica y pocos datos más. Se pasó a una lista cerrada de ficheros.
- Nombres de ficheros verificados contra el catálogo oficial de la CDC, huecos incluidos. Añadidos tras revisar el catálogo: vitamina D, albúmina/creatinina en orina, ayuno, tabaco, alcohol, actividad, dieta (comida rápida) y sueño. Descartados: ferritina, PSA, TSH, B12/folato, salud autovalorada, entre otros.
- Incidencia: el servidor de mortalidad (ftp.cdc.gov) estuvo caído un rato; los reintentos del script lo resolvieron.
- Código reorganizado tras revisarlo juntos: `config/` (rutas y fuentes), `utils/` (por tema), `pipeline/` (un archivo por paso con `run()`), `main.py` como único punto de entrada. Quitados hash y argumentos de línea de comandos por innecesarios.
- Datos: capas numeradas (`01_bronze`…) y una carpeta por ciclo con la mortalidad dentro. Ficheros movidos sin volver a descargar.
- Reorganizados los archivos de Claude: CONTEXTO solo con decisiones de fondo, ESTADO en tres secciones, este HISTORICO y ESTILO (estilo de código portable).
- Silver raw: unir ficheros por ciclo → filtrar 18-79 elegibles → renombrar alias de laboratorio → apilar. 54.809 personas, 6.271 defunciones, 993 columnas. Se decidió renombrar antes de apilar (no apilar columnas medio vacías) y no renombrar cuestionarios a ciegas.
- Incidencias: la flecha `→` en un `print` rompe la consola de Windows (cp1252); el peso de ayunas de 2003-2004 salía duplicado por redondeo distinto entre ficheros (corregido comparando con tolerancia).
- Commits: `78cf2f9` (archivos de Claude), `cee68d2` (Silver raw).
- Exploración (notebook 01): criterio de variables = analítica de rutina española + lo que se pide a menudo + lo que el usuario sabe + ~10 preguntas de botones. Embarazadas fuera. Una variable por pareja correlacionada en el modelo; la otra servirá en la app para rellenar.
- Silver clean: 50.969 personas, 5.808 defunciones, 72 columnas. Correcciones oficiales de la CDC (creatinina 1999-2000 y 2005-2006, cambio de analizador en 2017-2018), triglicéridos solo en ayunas, LDL fuera, cuestionarios a respuestas de botón (preguntas saltadas = "nunca"), pesos combinados. VO2 max y DXA fuera.
- Incidencia evitada: una lista global de códigos "no sabe" (7, 9…) habría borrado respuestas numéricas reales; se cambió a códigos por variable.
- Commit: `2f401d7` (Silver clean, notebook, correcciones CDC).
- Cierre: borrador de la Entrega 02 con notas por apartado, para no perder el contexto. Queda Gold, la muestra y redactar.
- Commits: `2f7a0f3` (Bronze + estructura `src/`), merge a `main` y push.

## Antes del 2026-10-17 (reconstruido de git)
- 2026-08-17 a 2026-10-13: setup del repo y Entrega 01 (4 ideas; elegida la 4). Commits `11999eb` … `23326d5`.
- 2026-10-15: setup para trabajar con Claude (CLAUDE, CONTEXTO, ESTADO), `.gitignore` y `.gitattributes` (`d5eb017`, `3cf246e`).
- 2026-10-17: entrevista de producto en CONTEXTO (`3c4a9e7`); entorno Python 3.11 y carpetas (`706a5ba`).
