# Qué hay en este archivo y cómo usarlo
- **Contiene:** una entrada por sesión, la más reciente arriba: fecha, qué se hizo en pocas líneas y los hashes de commit. El detalle de cada cambio está en git (`git show <hash>`).
- **No contiene:** cifras, decisiones con su porqué ni el estado actual.
- **Se actualiza:** al cerrar cada sesión, después del commit del trabajo.

## 2026-11-12 a 2026-11-13: revisión completa y bloque 1 de mejoras
- Revisión completa del proyecto (la última, el 2026-10-19) con mejoras de código, de estructura y una propuesta de MLOps (tests, DVC y MLflow), ordenadas en un plan de tres bloques en ESTADO (`a0fa2c0`).
- Bloque 1, en la rama `mejoras-bloque-1`:
  - Predicción separada del entrenamiento; tests de los modelos (edades de referencia) y de la configuración; CI con GitHub Actions; cada modelo guarda la huella de sus datos, el commit y las versiones, y falla al cargar si no coinciden (`e1703a1`).
  - Modelos reentrenados después de commitear el código, para que apunten a un commit limpio; las edades no cambian (`e86a6f3`).
  - Test de las personas de test de la evaluación final; requisitos de la app separados de los del análisis; README (`0a93f40`).
  - ESTADO, TECNICO y DECISIONES al día (`94b3392`), merge `b4bdc72` a `main` y primer push con CI.
- Incidencia: el reentreno tarda unos 6,5 minutos, no unos 3 como decía TECNICO.

## 2026-11-11: Entrega 03
- Documento de la Entrega 03 redactado a partir de DECISIONES y de los notebooks de los niveles y de la evaluación final, y revisado por mí; `final_evaluation` se enlaza tal cual como código reproducible (`e6f73ea`).
- ESTADO: Entrega 03 hecha; la próxima sesión, revisión completa del proyecto (la última, el 2026-10-19) y arranque de la fase de app (`31c1ab4`).

## 2026-11-09 a 2026-11-10: evaluación final en test y modelo final con todos los datos
- Criterios de aprobado fijados antes de mirar el test y evaluación final ejecutada una sola vez: todos los saltos entre niveles son reales y PhenoAge queda igualada o superada; la infraestimación en los deciles de riesgo bajo queda como limitación. La fórmula de PhenoAge pasa a `src/utils/` (`e5b81f5`).
- Incidencia: el criterio de infraestimación en años estaba mal planteado (inestable con riesgo bajo; también lo suspende el baseline). No se cambió a posteriori: se documenta como limitación.
- `s5_build_model` entrena el modelo final con toda Gold; el notebook de evaluación entrena los suyos con train mediante `build_level`. Reentrenar no cambia ningún signo y mueve poco la edad biológica (`700c846`, merge `39a2d68` de `modelo-final-todos-los-datos`).
- Fase de modelo cerrada.

## 2026-11-07 a 2026-11-09: niveles 2 a 4, edad biológica, PhenoAge y modelos guardados
- Niveles 2, 3 y 4 con Cox simple: Base + 10 Extras (`66e5157`), Base + 4 hábitos (`51fddfa`) y los dos juntos (`3c80ce5`).
- Edad biológica: referencia propia de cada nivel con la mediana por edad y sexo; el RDW sale de todos los modelos por el salto del analizador (`c7bb4b4`).
- Comparación con PhenoAge en train: el nivel 1 la iguala y el nivel 2 la supera (`45b6955`). Incidencia: el riesgo de PhenoAge se redondeaba a 1 en casos graves y daba edades infinitas; se calculó desde la puntuación.
- `s5_build_model` entrena con train los niveles 1 a 4 y los guarda en `models/`, en git (`7d39d82`).
- Incidencia: los notebooks se ejecutan con el Python de `.venv`; el Jupyter global no tiene scikit-survival.

## 2026-11-06: nivel 1 del modelo
- Notebook del nivel 1: los cuatro contendientes con valores fijos, optimización con Optuna, bootstrap frente al baseline, pesos de cada variable y variantes de Base. Elegido Cox simple y Base reducida a 19 variables (`aeb3acd`).
- Notebooks sin prefijo numérico, reservado a los entregables (`base_correlations`, `models_lvl1`).
- Los niveles quedan en Base + Extras, Base + Cuestionario y, si es pertinente, los dos juntos; PhenoAge se mide al final.

## 2026-11-04: código del modelo, hasta la evaluación
- Salto del RDW: la CDC lo atribuye al cambio de analizador; se deja sin corregir y se medirá su efecto (`bf8a65e`).
- Split 80/20 estratificado con 5 bloques en train (`cc20882`). Pipeline numerado de `s1` a `s5`, con `s5_build_model` como paso del modelo (`ab7e21e`).
- Preprocesado reescrito como `Pipeline` de scikit-learn, siguiendo el de un proyecto anterior (`a01ae42`).
- Cuatro contendientes con valores fijos; XGBoost sustituye al gradient boosting de scikit-survival, demasiado lento (`2d2e650`).
- Evaluación a 10 años con resumen por nivel; notebooks por nivel, no por modelo; orden cambiado: entrenar y evaluar antes de traducir a edad (`7bad730`).
- Incidencia: una tabla de resultados de un comando de prueba se presentó como si fueran resultados; solo sirvió para probar el código y no se usó para decidir.

## 2026-11-03: bloques de variables del modelo
- Bloques Base, Extras y Cuestionario fijados y lista de descartadas con su motivo en `model_sets.py`; elección de parejas y combinaciones lineales en DECISIONES; salto del RDW apuntado como limitación; notebook de correlaciones de las candidatas a Base; esqueleto de `src/models/` y `src/train.py`, solo con docstrings (`196e6bd`).
- Incidencia: un primer análisis de lo que aporta cada variable frente a la mortalidad se hizo en scripts temporales, fuera de notebooks y sin acordarlo; se descartó y no se usó para decidir.

## 2026-11-03: validación de Gold y diseño del modelo
- Resumen de la vuelta tras una semana, con los apuntes de la clase del profesor y el enunciado de la Entrega 03 en ESTADO y DECISIONES (`ee487aa`).
- Validación de Gold antes de guardar, en su propio módulo con sus umbrales; rangos posibles por variable con criterio ambulatorio (emergencia o artefacto), con rango normal y porqué; valores fuera de rango vaciados en Silver clean; vitamina D a ng/mL (`168cbc4`, `258f68c` merge de `validacion-gold`, `c7ee1e7`).
- `codes.py` renombrado a `nhanes_codes.py`; definición del problema: supervivencia a 10 años, 80/20 estratificado, columnas de contexto fuera de los predictores (`ae2e380`).
- Diseño del modelo: escalera de niveles con cuatro contendientes, variables anidadas, imputación para analíticas incompletas, modelo de la app y estructura de `src/models/`; notebooks de trabajo pueden importar del código (`ce5abfa`).

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
