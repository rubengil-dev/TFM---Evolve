# Metadatos

## Qué contiene
Qué hay que construir para completar el MVP y en qué orden, como una checklist por fases. Solo cosas que construir, programar o diseñar.

Lo que no encaje en esta descripción no va aquí. Las decisiones pendientes no son casillas: van a `NOTAS.md` o, si bloquean algo, a `ESTADO.md`.

## Actualización
- Cada fase es una casilla grande con sus casillas dentro. Las casillas son frases cortas.
- Estados de una casilla: `[ ]` pendiente, `[*]` activa, `[x]` hecha, `[/]` bloqueada (el motivo va en `ESTADO.md`).
- Al terminar algo se marca su casilla. La fase se marca cuando todas las suyas lo están.
- Al terminar una fase, sus casillas se condensan en menos casillas, más gruesas (como las de las fases lejanas), para que el archivo se mantenga corto.
- Las fases son lineales: solo hay una activa a la vez.
- El plan no es inamovible: cuando aparece algo nuevo, se añaden, parten o reordenan casillas y fases.
- La fase activa se detalla casilla a casilla. Las lejanas van más gruesas, con la nota "se afina al llegar", y se desglosan al llegar a ellas.


# Contenido

## Fases
- [x] **Fase 0, arranque:** repo, entorno de Python y estructura de carpetas.
  - [x] Entrega 01: ideas de producto.
- [x] **Fase 1, datos:** descarga de NHANES y de su mortalidad a Bronze.
- [x] **Fase 2, preparación:** de Bronze a la tabla del modelo.
  - [x] Silver raw y Silver clean.
  - [x] Gold, con sus features derivadas y su validación.
  - [x] Entrega 02: datos y preparación.
- [x] **Fase 3, modelo:** del riesgo de mortalidad a la edad biológica.
  - [x] Split, preprocesado, algoritmos y evaluación.
  - [x] Niveles 1 a 4, traducción del riesgo a edad y comparación con PhenoAge.
  - [x] Evaluación final en test y modelo final de cada nivel guardado.
  - [x] Tests, CI y trazabilidad de los modelos.
  - [x] Entrega 03: Machine Learning.
- [*] **Fase 4, app:** lectura del PDF, pantalla de revisión, cuestionario, resultado y front.
  - [/] Flujo de pantallas, con la elección de modo.
  - [/] Parser del PDF, con la normalización de nombres y unidades.
  - [/] Pantalla de revisión y corrección de los datos extraídos.
  - [/] Validación de lo que entra al modelo, en el módulo de predicción: columnas, tipos, categorías, rangos posibles y edad, con errores con código que el front traduce. Hoy una columna ausente o un número como texto dan un error técnico, y un valor imposible devuelve una edad sin avisar.
  - [/] Cuestionario de hábitos.
  - [/] Pantalla de resultado.
  - [/] Añadir las librerías del stack a las dependencias del proyecto (`pyproject.toml`) y completar el README.
  - [ ] Entrega 04: solución UX.
- [ ] **Fase 5, despliegue:** web pública en un hosting gratuito *(se afina al llegar)*
- [ ] **Fase 6, MLOps:** versionado de datos y de modelos; los tests, la CI y la trazabilidad ya están hechos en la fase 3. Va después de la Entrega 04, salvo que el profesor lo pida antes *(se afina al llegar)*
  - [/] DVC para los datos y el pipeline: una etapa por paso, llamando al código actual; los modelos siguen en git y DVC solo anota su huella; la descarga no se borra al repetir. Es el versionado de datos que pide el máster: liga cada modelo a sus datos y detecta cambios en los ficheros de la CDC.
  - [/] MLflow: una función de registro llamada desde los notebooks y desde el paso del modelo, sin tocar la evaluación. Hoy los resultados solo viven en las salidas de los notebooks.
  - [ ] Reejecutar los notebooks de los niveles 1 a 4, nivel a nivel y revisando juntos: sus salidas quedaron desfasadas al quitar el RDW y al pasar a importar las funciones comunes, y las cifras pueden moverse respecto a las ya escritas.
  - [ ] Entrega final.
