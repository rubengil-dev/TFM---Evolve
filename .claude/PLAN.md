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
  - [*] Front en React, completo: portada con la elección de modo, preguntas, revisión, carga, errores y resultado, con el diseño visual definitivo. Primero con datos de ejemplo y después conectado al backend.
  - [x] API: leer el PDF (de momento, una persona inventada) y calcular, conectada al front.
  - [x] Elección del modelo: Extras desde 3, o 4 con cuestionario, medido al entrenar.
  - [x] Edad fuera de 18-79: la diferencia se calcula como si tuviera 18 o 79 y se suma a la edad real.
  - [ ] Entrega 04: `docs/entregas/04_diseno_frontal_ux.md` con capturas de la app.
  - [/] Parser del PDF, con la normalización de nombres y unidades, probado con mis PDFs.
  - [ ] Corrección de un valor imposible en el backend (`POST /api/correct`, con el contrato ya escrito): pasa el valor a la unidad del modelo con su factor, comprueba que ya es posible y, si no, se vuelve a preguntar. Con el parser, porque usa su tabla de unidades; `factor` deja de viajar al front.
  - [ ] Pantalla de revisión, solo para los valores que el parser marca como dudosos, y solo si las pruebas del parser muestran que hace falta.
  - [x] Preguntas de sexo y edad, solo si el PDF no las trae.
  - [x] Pantallas de error: PDF ilegible o que no es una analítica, faltan demasiados datos y valor imposible; aviso rojo de edad fuera de 18-79 en el resultado.
  - [x] Letra pequeña de la portada (privacidad y cómo se calcula).
  - [x] Logo: icono de la pestaña y marca de agua de la imagen compartida.
  - [x] Validación de lo que entra al modelo: columnas, tipos, categorías, edades, valores imposibles, IMC imposible y mínimo de datos (5 valores de Routine que faltan, u 8 con cuestionario), también al leer el PDF.
  - [ ] Cuestionario de hábitos.
  - [ ] Pantalla de resultado, presentada como edad equivalente según la referencia de NHANES: edad ± X, tabla de grupos y, con cuestionario, tabla de hábitos.
  - [*] Aportación en años de cada grupo de variables frente a la persona típica de su edad y sexo: hecha y revisada; falta reentrenar con el código commiteado.
  - [x] Margen ± de la edad, medido al entrenar (`modeling/s7_margin.py`) y guardado en cada modelo, con el aviso gris si llega a 5 años.
  - [x] Línea "De 16 a 90 años" en la portada.
  - [ ] Logs de la app en JSON, sin valores de salud: modelo, nivel, variables recibidas, latencia, estado y código de error.
  - [ ] Añadir las librerías del stack a las dependencias del proyecto (`pyproject.toml`) y completar el README.
  - [ ] Revisión completa de todos los textos de todas las pantallas, también las de error. Lo último, con la app acabada.
- [ ] **Fase 5, despliegue:** web pública en un hosting gratuito *(se afina al llegar)*
- [ ] **Fase 6, MLOps:** versionado de datos y de modelos; los tests, la CI y la trazabilidad ya están hechos en la fase 3. Va después de la Entrega 04, salvo que el profesor lo pida antes *(se afina al llegar)*
  - [/] DVC para los datos y el pipeline: una etapa por paso, llamando al código actual; los modelos siguen en git y DVC solo anota su huella; la descarga no se borra al repetir. Es el versionado de datos que pide el máster: liga cada modelo a sus datos y detecta cambios en los ficheros de la CDC. Al añadirlo, quitar `code_version` de `utils/provenance.py`: DVC ya anota la huella del código.
  - [/] MLflow: una función de registro llamada desde los notebooks y desde el paso del modelo, sin tocar la evaluación. Hoy los resultados solo viven en las salidas de los notebooks.
  - [ ] Reejecutar los notebooks de los niveles 1 a 4, `biological_age`, `phenoage`, `final_evaluation` y `routine_correlations`, uno a uno y revisando juntos: sus salidas quedaron desfasadas al quitar el RDW, al pasar a importar las funciones comunes y con el reentreno de la revisión de código (Gold sin una persona, otro split y la curva ponderada), y las cifras pueden moverse respecto a las ya escritas. De paso, "Base" pasa a "Routine" en sus textos.
  - [ ] Documentación final: horizonte del riesgo (10 años), población de referencia, un ejemplo de entrada y salida y qué es "edad equivalente".
  - [ ] Entrega final.
