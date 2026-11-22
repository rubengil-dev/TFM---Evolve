# Metadatos

## Qué contiene
El stack del proyecto (qué tecnologías y servicios se usan y por qué), el resto de decisiones técnicas con su porqué, las restricciones técnicas y las trampas técnicas que no se deducen del código.

Lo que no encaje en esta descripción no va aquí. Librerías y versiones, comandos, endpoints, modelo de datos y contratos de funciones tampoco: eso sale del código, del archivo de dependencias o de git.

## Actualización
- Casi inmutable. Se añade un punto cuando se toma una decisión técnica o se descubre una restricción o una trampa.
- Las decisiones sencillas y rápidas (tecnologías, servicios) van en `Stack`, una línea cada una. Las que necesitan más explicación (arquitectura, patrones) van en `Otras decisiones`.
- Cada decisión ocupa una línea, con cómo se decidió entre paréntesis y, solo si aporta, `Descartado: X, motivo corto.` en la misma línea (ver "Cómo anotar decisiones relevantes" en `PROTOCOLOS.md`). Una restricción lleva etiqueta solo si fue una decisión.
- Si una decisión cambia, se reescribe el punto y su porqué cuenta el cambio: "porque antes había X y pasó Y".
- Una trampa se apunta cuando ya ha costado tiempo y no es evidente leyendo el código. Va con su porqué.
- Si crece demasiado, avísame para dividirlo.


# Contenido

## Stack
- **Python 3.11:** la soportan todas las librerías y tiene soporte hasta 2027. Descartado: 3.14, demasiado nueva.
- **uv:** entorno y dependencias, con `uv.lock` en git. Las dependencias del proyecto son solo las de la app (lo que necesita un modelo guardado para predecir) y el análisis va en el grupo `dev`, para que el hosting gratuito no instale las librerías de entrenamiento. Todo fijado con `==`, porque un modelo guardado solo se carga bien con las mismas versiones. Antes había dos `requirements` mantenidos a mano y un test que comparaba sus versiones; con un solo lock ya no pueden divergir. (Rubén, de acuerdo)
- **NHANES continuo 1999-2018** con la mortalidad pública enlazada hasta 2019: los datos de entrenamiento, descargados como una lista cerrada de ficheros verificada contra el catálogo de la CDC. Descartado: NHANES III, con métodos de laboratorio y formato distintos; mortalidad hasta 2022, de acceso restringido.
- **scikit-survival y XGBoost:** los modelos de supervivencia. Descartado: el gradient boosting de scikit-survival, unos 46 minutos por entrenamiento frente a segundos.
- **`Pipeline` de scikit-learn:** el preprocesado se ajusta solo con train, se guarda entero con el modelo y la app aplica exactamente el mismo objeto.
- **pytest y GitHub Actions:** ruff y tests en cada push. El trabajo de tests instala solo las dependencias de la app más pytest (grupo `test`), lo que demuestra que bastan para predecir, y no tiene `data/`: los tests que la necesitan se saltan.
- **ruff y pre-commit:** ruff revisa y formatea, con líneas de 120 caracteres; pre-commit lo ejecuta junto con los tests antes de cada commit, con las versiones de `uv.lock` (hooks locales, sin repetir la versión de ruff en otro archivo). Los archivos de `config/` quedan fuera del formateo y las tablas alineadas del resto van entre `# fmt: off` y `# fmt: on`, porque el formateador deshace las columnas. Los notebooks quedan fuera de ruff para no reescribir celdas con salidas guardadas. (Claude, autónomo)
- **GitHub:** `rubengil-dev/TFM---Evolve`, rama principal `main`.
- [pendiente: stack de front y backend y hosting; son bloqueos de `ESTADO.md`.]

## Otras decisiones

### Arquitectura
- **Enfoque:** un modelo de supervivencia estima el riesgo de morir a 10 años y ese riesgo se traduce a edad biológica, al estilo de PhenoAge (Levine et al., 2018), que es la referencia externa. No existe una etiqueta de edad biológica real y la mortalidad sí se observa; 10 años es el horizonte de PhenoAge, a 5 hay pocas muertes y a 15 solo 3 de los 10 ciclos tienen seguimiento completo.
- **Población de referencia:** la de EE. UU. (NHANES), asumiendo que equivale a la española.
- **El modelo y la app leen solo de Gold:** con un único punto de lectura se sabe qué datos usan y Silver se puede cambiar sin romperlos; por eso Gold guarda también las parejas correlacionadas que el modelo no usa. Lo pide el profesor.
- **Gold solo lleva fórmulas fijas:** rellenar huecos, recortar, escalar y codificar van al preprocesado, porque hacerlo con todo el dataset filtraría información del test.
- **Las fórmulas de las features derivadas viven en un único módulo** compartido por el pipeline y la app: tienen que calcularlas exactamente igual.
- **Gold se valida antes de guardar:** bloquean la estructura, el tamaño mínimo (personas y defunciones), la cobertura, el desenlace, la población, las respuestas permitidas, los rangos posibles y los valores infinitos; las coherencias entre variables solo avisan. Una Gold rota no avisa por sí sola y falsearía el modelo.
- **Código del modelo: un archivo por paso, no por modelo,** con prefijo `s1_`…`s5_`: los cuatro modelos son el mismo proceso con otra lista de variables, y Python no importa módulos que empiezan por número.
- **Predicción separada del entrenamiento:** la app carga un modelo y calcula la edad sin instalar las librerías de entrenamiento. Lo que ejecuta la app vive en `src/bioage/app/` y nada del entrenamiento importa de ahí: la app tira del resto, no al revés. (Rubén, de acuerdo)
- **Los modelos van en git, uno por nivel y entrenados con todos los datos (train y test):** el servidor no puede regenerarlos sin descargar NHANES y pesan poco. La evaluación final no los carga, entrena los suyos con train con la misma función: si los cargara, evaluaría con gente ya vista y daría cifras infladas sin avisar.
- **Cada modelo guarda su origen:** la huella de los datos, el commit del código y las versiones de Python y de las librerías, y falla al cargar si las instaladas no coinciden. Sin fecha, porque con ella cada reentreno cambiaba los archivos aunque nada hubiera cambiado.
- **Test de referencia:** la edad biológica de unas personas inventadas en los cuatro niveles, con un margen de 0,01 años. Avisa de cualquier cambio sin querer en el modelo, el preprocesado o las librerías, que de otro modo moverían edades en silencio.

### Datos y preparación
- **Población del estudio:** adultos de 18 a 79 años elegibles para mortalidad, sin embarazadas ni personas sin examen físico o sin ningún valor de laboratorio. NHANES agrupa las edades de 80 en adelante y el embarazo altera la analítica.
- **Ficheros descartados:** ferritina, PSA, TSH y B12/folato/homocisteína/ApoB (solo en subgrupos o en pocos ciclos); fuerza de prensión, bioimpedancia, acelerómetro, DXA y VO2 max (el usuario no los conoce); y la salud autovalorada (subjetiva).
- **Los cambios de método de laboratorio se corrigen con las ecuaciones oficiales de la CDC** (creatinina, bioquímica y PCR de 2017-2018, insulina y creatinina en orina): sin corregir, el modelo confundiría el cambio de analizador con un cambio real de la población.
- **Unidades del laboratorio español** desde Silver clean (urea, PCR en mg/L, cociente albúmina/creatinina en mg/g, vitamina D en ng/mL): así no hay que convertir al recibir la analítica.
- **Los valores imposibles se vacían en Silver clean** con una tabla de rangos posibles por variable, con el criterio de un adulto que va por su pie a una analítica programada; los extremos de una enfermedad conocida se quedan. No son outliers, son errores o emergencias; la app usa la misma tabla.
- **Hemograma en recuentos absolutos,** no en porcentajes: los porcentajes dependen unos de otros.
- **LDL fuera, triglicéridos solo con ayuno de 8 horas o más y glucosa en todas las personas:** el LDL de NHANES es calculado, solo existe en ayunas y sale protector por causalidad inversa; el ayuno cambia los triglicéridos pero apenas la glucosa.

### Modelo
- **Escalera de niveles anidados:** 0, baseline (Cox con edad y sexo, que equivale a decir que la edad biológica es la cronológica); 1, Routine; 2, Routine + Extras; 3, Routine + Cuestionario; 4, todo. Cada salto mide solo lo que aporta el bloque nuevo y responde a una pregunta del producto.
- **Los bloques responden a qué trae el usuario, no a cuánto predice cada variable:** Routine es la analítica de rutina más edad, sexo e IMC; Extras, lo que se pide a menudo o es opcional; Cuestionario, los hábitos. Las listas y las variables descartadas, con su motivo, viven en `src/bioage/config/model_levels.py`.
- **Cox simple en los cuatro niveles:** compitió en igualdad con Cox elastic net, random survival forest y XGBoost, y XGBoost optimizado con Optuna no llegó al listón fijado de antemano (+0,02 de C-index misma edad); no compensa perder la explicabilidad. Descartado: deep learning, más difícil de explicar y de desplegar en un plan gratuito.
- **Split 80/20 estratificado por ciclo y muerte, y el test se mira una sola vez:** todas las decisiones se toman con validación cruzada de 5 bloques dentro de train. Descartado: separar por ciclos, dejaría un test con muy pocas muertes.
- **Métrica principal: C-index de Uno dentro del mismo grupo de edad, a 10 años.** La edad sola ya ordena muy bien, así que es la que dice si la analítica aporta algo; un nivel mejora de verdad si el intervalo por bootstrap de la diferencia no incluye el 0.
- **Infraestimar la edad biológica es el error peor:** da una falsa tranquilidad, mientras que sobreestimar solo manda al médico. Con métricas parecidas se prefiere el modelo con menos errores grandes.
- **Pesos muestrales de NHANES solo en la curva de referencia de la edad biológica:** la "persona típica" de cada edad y sexo tiene que ser la de la población y no la de la muestra, que sobrerrepresenta a propósito a mayores y minorías. Antes no se usaban en ningún paso; el entrenamiento y la evaluación siguen sin ellos, porque el Cox de scikit-survival no los admite y el usuario es español, y se declara como limitación. (Rubén, de acuerdo)
- **Una variable con efecto claro contrario al conocido no entra aunque suba el C-index, y las preguntas de un mismo hábito se juzgan juntas:** por eso sale el alcohol, que resulta protector por la causalidad inversa de quienes lo dejaron por enfermedad. Cuesta 0,004 de C-index misma edad.
- **De cada pareja o combinación lineal entran las variables que vienen escritas en el PDF** (hemoglobina, hematíes y CHCM; los cinco tipos de leucocitos; el IMC en lugar de peso y talla): así la app no tiene que calcular nada. Fuera insulina, HOMA-IR y los cocientes derivados.
- **RDW fuera de todos los niveles:** el cambio de analizador de 2012, sin corrección oficial, mueve la edad biológica de 1,8 a 2,8 años, por encima del límite de 1 año fijado antes. En la app sería un sesgo de todo un laboratorio que el usuario no puede ver ni corregir.
- **Traducción del riesgo a edad:** la edad a la que la persona típica del mismo sexo tiene el mismo riesgo a 10 años, con una referencia propia de cada nivel: la mediana del riesgo de train por edad y sexo, ponderada con los pesos del examen, en escala log(−log(1 − riesgo)), con una curva de segundo grado por sexo que fuera de 18-79 sigue en línea recta. Descartado: una referencia común (el baseline, como PhenoAge), la persona típica salía hasta 5 años más joven; la media en vez de la mediana, 1-2 años por debajo.
- **Preprocesado, en este orden:** recorte a los percentiles 0,1 y 99,9; huecos con la mediana (o la respuesta más frecuente) de su sexo y grupo de edad; logaritmo si la asimetría pasa de 2; escalado; una columna 0/1 por categoría; y término al cuadrado en IMC y horas de sueño. Con la mediana general, una persona mayor con un hueco parecería más joven, que es el error peor.
- **Analíticas incompletas: los cuatro modelos más imputación, sin usar los nulos como información:** en NHANES un hueco suele significar "ciclo sin esa prueba", y un modelo que aprendiera de los nulos aprendería el ciclo.
- **Evaluación final con los criterios fijados antes de abrir el test:** se cumplen todos menos la infraestimación en los deciles de riesgo bajo (de 3,7 a 9,6 años, sobre todo ruido por las pocas muertes). No se reajusta el modelo: queda como limitación, y por eso el margen ± X es más ancho en jóvenes de riesgo bajo. Las cifras están en `docs/entregas/03_machine_learning.md`.

### App
- **La app usa el nivel más completo que permitan los datos del usuario:** los cuatro saltos son reales en test. No se promedian modelos, porque promediar con uno peor empeora el resultado.
- **Si falta una variable del modelo pero viene su pareja, se estima** con una ecuación ajustada sobre Gold (p. ej. hemoglobina desde el hematocrito), solo en parejas con correlación alta: se pierden menos variables sin pedir nada más al usuario.
- **El filtrado glomerular no es variable del modelo** (es redundante con creatinina, edad y sexo), pero el parser puede usarlo para recuperar la creatinina si falta.

## Restricciones técnicas
- Hosting en planes gratuitos.
- Cambios de método entre ciclos sin corrección oficial: fosfatasa alcalina y LDH más altas en 1999-2000, urea algo más alta en 2017-2018, RDW (la mediana pasa de 12,5 a 13,5 en 2013), insulina (salto de un 15 % entre 2007-2008 y 2009-2010) y avisos de la CDC sobre serie roja, plaquetas y leucocitos.
- Cuestionarios con saltos: la actividad física cambia de cuestionario en 2007; el tabaco de 18-19 años sale de las preguntas juveniles hasta 2012 (hasta 2010 no distingue exfumadores); y no hay alcohol para 18-19 años en 1999-2010.
- Variables medidas solo en parte de la muestra: triglicéridos e insulina (subgrupo en ayunas), CPK (solo 2011-2018) y PCR (sin 2011-2014).
- Los últimos ciclos tienen pocas defunciones por su seguimiento corto.

## Trampas
- **Reentrenar los modelos** (entre 5 y 27 minutos, según cómo ande el disco): hay que commitear antes el código y no tocar `src/` mientras entrena. Por qué: cada modelo guarda el commit y lo marca como `-dirty` si `src/` tiene cambios sin commitear, y la marca se calcula al guardar cada modelo, no al empezar. Después, los modelos se commitean aparte.
- **`src/bioage/models/s2_preprocessing` no se puede mover ni renombrar** sin reentrenar, y el paquete `bioage` tampoco. Por qué: los modelos guardados apuntan a su ruta de import.
- **Los modelos de `models/` no sirven para evaluar.** Por qué: están entrenados con toda Gold, test incluido.
- **La referencia de edades de los tests** se rehace solo tras cambiar el modelo a propósito, con `write_reference` de `tests/app/test_predict.py`, y se revisa el diff. Por qué: rehacerla tras un cambio involuntario escondería justo lo que el test tiene que detectar.
- **Ejecutar un notebook desde la terminal:** siempre con `uv run jupyter nbconvert`. Por qué: el `jupyter` global arranca el Python global, que no tiene scikit-survival; antes hacía falta un `JUPYTER_PATH` porque `nbconvert` no estaba en el entorno.
