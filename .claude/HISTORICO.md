# Qué hay en este archivo y cómo usarlo
- **Contiene:** una entrada por sesión, la más reciente arriba: fecha, qué se hizo en pocas líneas y los hashes de commit. El detalle de cada cambio está en git (`git show <hash>`).
- **No contiene:** cifras, decisiones con su porqué ni el estado actual.
- **Se actualiza:** al cerrar cada sesión, después del commit del trabajo.

## 2026-10-19: revisión del código y tabaco juvenil
- Revisión integral del código contra la documentación de la CDC: nuevas correcciones de insulina (llevada a la escala de 2013-2018), PCR ultrasensible de 2017-2018 y creatinina en orina antes de 2007; códigos de los cuestionarios en su propio archivo; resumen de cada capa compartido; DEMO como base explícita de Silver raw; eGFR vacío si falta el sexo; limpieza de estilo.
- Tabaco de los de 18-19 años hasta 2012 completado con las preguntas juveniles de NHANES; el alcohol juvenil se descarta. Espacios finales quitados de las entregas.
- Commits: `cf873e8`, `2cc9e89` (merge de `revision-codigo`), `db61bc9`, `dd02e58` (merge de `tabaco-juvenil`), `53eeb8d` (histórico).

## 2026-10-18: Gold, Entrega 02 y nueva forma de trabajar con Claude
- Silver clean: fuera también las personas sin ningún valor de laboratorio. Ficheros renombrados a `silver_raw`/`silver_clean`.
- Gold con features derivadas, recuentos absolutos del hemograma, insulina, CPK y hábitos.
- Entregas movidas a `docs/entregas/`. Documento y muestra de la Entrega 02 redactados, revisados y entregados en Classroom.
- Commits: `c241c83` (Gold), `14e3342` (histórico), `298008b` (Entrega 02).
- Archivos de Claude rehechos en 8, cada uno con una función y una cabecera común: CLAUDE (arranque e índice), PAUTAS (cómo trabajar conmigo, con lo que sé), CONTEXTO, ESTADO, ESTILO, TECNICO, DECISIONES e HISTORICO. Revisados uno a uno; los cambios de `.claude/` se revisan ahora en el editor y se commitean con cada OK.
- ESTILO: docstrings de función en una línea cuando caben, con los de `src/` ajustados; ejemplo de función principal.
- Gold: entran las parejas correlacionadas (hematocrito, HCM, neutrófilos), peso, talla y cintura, porque Gold es la única capa de la que leen el modelo y la app. Entrega 02 y su muestra actualizadas.
- Incidencia: el script que ajustó los docstrings reescribió los `.py` con saltos de línea de Windows; se devolvieron a LF antes de commitear.
- Commits: `75d4a1b`, `4b54c86` (primera limpieza), `237ca17` (CLAUDE, PAUTAS, CONTEXTO), `1894b89` (ESTADO), `0608818` (ESTILO y docstrings), `14f3f6f` (TECNICO), `25c63f1` (Gold y DECISIONES), `c249700` (histórico), `780733d` (merge de `gold-parejas`).

## 2026-10-17: Bronze, Silver y estructura del código
- Entrevista de producto en CONTEXTO (`3c4a9e7`); entorno Python 3.11 y carpetas (`706a5ba`).
- Descarga a Bronze con una lista cerrada de ficheros y estructura de `src/` (`2f7a0f3`). Incidencia: el servidor de mortalidad de la CDC estuvo caído un rato; lo resolvieron los reintentos.
- Archivos de Claude reorganizados (`78cf2f9`).
- Silver raw (`cee68d2`). Incidencias: la flecha `→` en un `print` rompía la consola de Windows; el peso de ayunas de 2003-2004 salía duplicado por redondeo.
- Notebook de exploración y Silver clean (`2f401d7`).
- Borrador de la Entrega 02 (`dd85326`), merge a `main` y push.

## Antes del 2026-10-17 (reconstruido de git)
- 2026-08-17 a 2026-10-13: setup del repo y Entrega 01 (4 ideas; elegida la 4). Commits `11999eb` … `23326d5`.
- 2026-10-15: setup para trabajar con Claude, `.gitignore` y `.gitattributes` (`d5eb017`, `3cf246e`).
