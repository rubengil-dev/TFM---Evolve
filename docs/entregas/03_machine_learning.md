# Entrega 03: Machine Learning

El modelo estima el riesgo de morir en los próximos 10 años a partir de una analítica de sangre y lo traduce a **edad biológica**: la edad a la que una persona típica del mismo sexo tiene ese mismo riesgo. Parte de la tabla Gold de la Entrega 02 (`data/03_gold/gold.parquet`, 48.495 adultos de 18 a 79 años y 5.425 defunciones).

## 1. Qué problema resuelve el modelo

**Para quién?**
El producto está pensado para una persona sin formación médica, para que desde casa, pueda entender exactamente cómo está su cuerpo gracias a una analítica (y en caso pertinente, a un breve cuestionario). La decisión de predecir la edad biológica en vez de clasificar cómo bien/mal/regular reside en 2 puntos:

1. El número es mucho más explicativo, porque la diferencia con tu edad real puede darte mucha información que una simple clasificación básica.
2. Es más atractivo. Desde el punto de vista de la usabilidad, cómo seres humanos nos llama mucho más la atención saber nuestra "edad real" que si estamos bien/mal/regular.

**Porqué ML?**
Calcular la edad biológica requiere dar a cada parámetro un peso, calcular en base a ese peso y el estado del parámetro en el individuo cuánto aporta e integrar todos los parámetros en una sola métrica.

**Cómo?**
Según la literatura científica actual ([PhenoAge - Levine et al., 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5940111/)) se puede calcular la "edad biológica" en base al riesgo de mortalidad. Además, los datos no cuentan con una etiqueta "edad biológica", sino con el año en el que la persona murió (o si sigue viva para el último año en el que se comprobó). Por eso he utilizado un modelo de supervivencia COX a 10 años en base a los biomarcadores de una analítica. 

La decisión a 10 años viene dada por los datos. A 5 años hay pocas muertes, y a 15 solo 3 de los 10 ciclos tienen seguimiento completo.
El modelo resultante se compara con PhenoAge como referencia.

## 2. Datos de entrada y salida

La idea del modelo es obtener un riesgo de mortalidad entre 0 y 1 en comparación con una persona promedio de tu edad, que después será traducido a edad biológica. Por lo que el output del modelo es ese riesgo.

Para ello, el modelo siempre usa los mismos targets, típicos de un análisis de supervivencia: meses de seguimiento y muerte (0/1). Sin embargo, las entradas las he anidado en 4 niveles para poder dar distintas funcionalidades en el producto final:

1. **Biomarcadores base**: Incluye los más frecuentes en las analíticas para asegurar que la mayoría de usuarios puedan obtener un resultado rigoroso. Los biomarcadores concretos se pueden ver en: `src/config/model_sets.py`, línea 9, variable `BASE`.

2. **Biomarcadores completos**: Incluye más marcadores para conseguir un modelo más preciso que se pueda usar con aquellos que traigan una analítica más completa. Los biomarcadores concretos se pueden ver en: `src/config/model_sets.py`, línea 18, variable `EXTRAS`.
  - No incluye todos los biomarcadores, ya que por simplificación y mejora de los coeficientes se descataron aquellos sin efecto claro cuya salida no bajaba el C-index.

3. **Cuestionario**: Incluye la analítica base (nivel 1) más algunas preguntas relacionadas con sus hábitos. Se incluyen: tabaco, actividad física, horas sentado y horas de sueño. Se descartó el alcohol porque su efecto salió como rejuvenecedor y la literatura es firme respecto a lo perjudicial que es el alcohol.

4. **Completo**: Combinación de niveles 2 y 3.

La idea es poder ofrecer al usuario el mejor modelo posible en base a sus datos. Ver `punto 5` para más información.

**Nota**: De las variables con una gran correlación sólo se incluye una de ellas. Y respecto a la entrega anterior, donde en gold justificaba no imputar, dado el bajo porcentaje de nulos (en torno al 5% por variable) y que el mejor modelo tras las pruebas no funciona con nulos, se imputan los nulos usando la mediana estratificada por edad y sexo.

**Evitar data lekeage**
El modelo solo conocerá los biomarcadores de la analítica y, en cuyo caso, las respuestas del cuestionario. Para evitarlo se ha excluido:

- No predictores: `seqn`, `cycle` ni `weight_exam`. El usuario no los tiene y el modelo puede aprender patrones de los ciclos.
- Todo el pre-procesado de los datos se hace sólo con train (incluyendo en las validaciones cruzadas).

  En este caso en concreto, el 100% de las variables predictoras están disponibles en el momento de la predicción por lo que no se necesitan más medidas.

**Sesgos**
Los datos utilizados para el entrenamiento son los de NHANES (EEUU), por lo que se asume la limitación en la posible diferencia entre poblaciones. Por ello, tampoco se han utilizado los pesos de NHANES para corregir la sobrerrepresentación realizada en el muestreo de NHANES para representar a EEUU.

## 3. Baseline y selección de modelos

Cómo baseline he elegido el modelo de supervivencia más simple que existe: asumir que la biológica es la cronológica. Por lo que este nivel incluye sólo sexo y edad. El punto está en que si la analítica no predice la mortalidad mejor que la edad ¿Qué estoy calculando?

Además se compara contra PhenoAge como referencia externa.

**Alternativas de ML.** 
En todos los niveles expuestos anteriormente se han hecho las mismas pruebas comparando los mismos modelos (todos usando el mismo preprocesado y validación cruzada)

- Cox: Es el modelo clásico de supervivencia, que al ser lineal es interpretable y rápido.
- Cox elastic net: Es idéntico al cox, pero elmina variables de forma autónoma estableciendo sus coeficientes en 0.
- Random survival forest (RSF): Es un modelo no lineal, por lo que se buscaba una alternativa diferente al cox.
- Gradient boosting (XGBoost): Cómo el RSF pero normalmente es más preciso.

En `notebooks/models_lvlN.ipynb` se pueden ver en detalle los coeficientes y las métricas de evaluación para elegir los modelos.
Por regla general, COX fue el modelo más preciso o presentaba una combinación de precisión e infraestimación mejor al resto de modelos. En los casos en los que no era mejor, la diferencia de los otros modelos no justificaba la pérdida de explicabilidad.

**Nota**: Generalmente se optimizó los 2 mejores modelos utilizando Optuna por ver si la optimización de los parámetros movía la aguja. No fue así.

## 4. Validación y evaluación

### 4.1 Separación
Se realizó un 80/20 aleatorio, estratificado por ciclo y muerte para evitar sesgos en base a las diferencias entre ciclos, además que los últimos tienen pocas muertes. 

- Train: 38.796 personas y 4.339 muertes
- Test: 9.699 personas y 1.086 muertes

A su vez, train se subdividió en 5 grupos para hacer validación cruzada sin data lekeage.

### 4.2 Métricas
- **C-index:** entre dos personas, cuántas veces el modelo da más riesgo a la que muere antes. Es la métrica estándar de supervivencia.
- **C-index misma edad:** es lo mismo, pero comparando solo a personas del mismo grupo de edad. Es la métrica principal porque la edad sola ya ordena muy bien (0,82) y la pregunta del producto es: ¿Entre dos personas de 45 años el modelo sabe cuál está peor?
- **Calibración en años:** por deciles de riesgo, cuántos años habría que sumar a la edad biológica para que el riesgo predicho cuadre con el observado. Si sale por encima de 0, el modelo infraestima, que es el error peor porque da falsa tranquilidad.
- **Mediana de (edad biológica − edad real)** por grupo de edad y sexo: la persona típica debería salir con su edad.
- **Intervalos de confianza** por bootstrap, con 200 remuestreos del test. Un nivel mejora al anterior si el intervalo de la diferencia queda entero por encima de 0.

**Resultados en test:**

| Modelo | C-index | C-index misma edad (IC 95 %) | Misma edad en validación cruzada |
|---|---|---|---|
| Baseline (edad y sexo) | 0,816 | 0,590 (0,571 a 0,609) | 0,598 |
| Nivel 1 (Base) | 0,842 | 0,677 (0,657 a 0,698) | 0,685 |
| Nivel 2 (Base + Extras) | 0,854 | 0,711 (0,689 a 0,732) | 0,720 |
| Nivel 3 (Base + Cuestionario) | 0,852 | 0,708 (0,690 a 0,729) | 0,716 |
| Nivel 4 (todo) | 0,861 | 0,729 (0,708 a 0,748) | 0,739 |

| Comparación | Mejora en C-index misma edad (IC 95 %) |
|---|---|
| Nivel 1 frente al baseline | **+0,087** (0,072 a 0,106) |
| Nivel 2 frente al 1 | +0,034 (0,021 a 0,045) |
| Nivel 3 frente al 1 | +0,031 (0,021 a 0,041) |
| Nivel 4 frente al 2 | +0,018 (0,010 a 0,026) |

**Frente a PhenoAge**
Con las 7.490 personas de test que tienen sus 9 variables:

- Nivel 1: empate (−0,003, de −0,017 a 0,015). Y cómo punto positivo PhenoAge necesita PCR y albúmina, que no están siempre presente.
- Nivel 2-4: en el nivel 2 superamos en +0,035 (0,018 a 0,054) y el 4 en +0,053. 

**Nota**: PhenoAge, para una persona típica de NHANES, estima entre 4 y 7 años menos, porque está calibrada con datos de 1988-1994. Los modelos propios la dejan dentro de ±1 año. Lo cuál es bastante positivo ya que infraestimar es el peor error posible.

### 4.3 Criterios fijados antes de abrir el test

| Criterio | Resultado | ¿Cumple? |
|---|---|---|
| Cada nivel supera al anterior | Los cuatro saltos, con el intervalo entero por encima de 0 | Sí |
| Sobreajuste: caída frente a la validación cruzada ≤ 0,02 | Caídas de 0,008 a 0,010 | Sí |
| Mediana de cada grupo de edad y sexo dentro de ±1,5 años | Máximo 1,05 años | Sí |
| El nivel 2 no queda por debajo de PhenoAge | Lo supera | Sí |
| Sin las muertes de los 2 primeros años, caída ≤ 0,02 | Caídas de 0,007 a 0,012 | Sí |
| Ningún decil de riesgo infraestima más de 2 años | De 3,7 a 9,6 años en los deciles de riesgo bajo | **No** |

### 4.4 Errores y limitaciones principales
1. **Infraestimación en riesgo bajo, que en la práctica son los jóvenes.** En los 5 primeros deciles, con edades biológicas medias de 16 a 43 años, la edad biológica puede quedarse corta hasta 9,6 años en un decil. Desde el decil 6 no pasa de 1,4 años. Es sobre todo ruido porque hay muy pocas muertes, y a esas edades una diferencia mínima de riesgo equivale a muchos años. El baseline (edad misma), infraestima hasta 5,2 años. 
  - Como el modelo presentará el resultado como Edad ± X, en este rango X será mayor y se asume la limitación ya que al ser jóvenes el riesgo bajo.
2. **Peor discriminación en 18-29 años**, con un C-index en ese grupo de 0,55 en el nivel 1 y de 0,70 en el 2. Hay muy pocas muertes jóvenes.
3. **Población de EE. UU. y cambios de método entre ciclos**, ya descritos en la Entrega 02. No se puede validar con analíticas españolas con mortalidad porque no hay datos públicos.

**Modelo final.** Tras la evaluación, cada nivel se reentrenó con todos los datos, train y test, que es lo que guarda `models/` para el producto. Ningún coeficiente cambia de signo y la edad biológica de cada persona se mueve menos de ±0,85 años en el 90 % de los casos. Las cifras del test siguen valiendo para este modelo.

## 5. Decisión y uso en el producto

**Solución elegida**: Cox con biomarcadores, un modelo por nivel, más la traducción del riesgo a edad. El producto usa el nivel más completo que permitan los datos del usuario, porque cada salto ha mejorado de verdad en test.

**Por qué.** Con la analítica básica ordena a personas de la misma edad +0,087 mejor que la edad sola, y con la ampliada supera a PhenoAge. Es tan preciso como XGBoost a efectos prácticos, explicable parámetro a parámetro, rápido y ligero para un hosting gratuito.

**¿Basta para el MVP?** Sí. La calidad es comparable o superior a la referencia publicada, no sobreajusta y la persona típica sale con su edad. La infraestimación en jóvenes de riesgo bajo no impide lanzarlo, pero condiciona cómo se presenta el resultado.

**Qué consume el frontal:**

| Salida | Significado |
|---|---|---|
| **Edad biológica** | La edad a la que una persona típica del mismo sexo tiene tu riesgo a 10 años. No deja de ser una estimación estadística, no un diagnóstico |
| **Diferencia con la edad real** | Te indica si estás mejor o peor que el promedio de tu edad. Por encima de un umbral, recomendación de revisar la analítica con su médico |
| **Margen ± X años** | La incertidumbre de la estimación: más ancho si faltan datos o en jóvenes de riesgo bajo |
| **Contribución de cada parámetro** | Cuántos años suma o resta cada parámetro frente a una persona media de su edad y sexo; de ahí salen los mejores y peores parámetros |
| **Años de los hábitos** | Cuándo se rellena el cuestionario, indica cuántos años suman o restan tus hábitos |

**Nota**: Al ser un producto "casero", siempre se acompañará el resultado de un aviso: "No es consejo médico ni diagnóstico."

## Para Julio
Cómo el proyecto empieza a tener infinidad de archivos, te dejo aquí un pequeño resumen del contexto de los archivos:

- **Entrada:** Gold de la Entrega 02 (`data/03_gold/gold.parquet`), generada por el pipeline.
- **Código del modelo:** `src/models/`, con un archivo por paso: `s1_split`, `s2_preprocessing`, `s3_algorithms`, `s4_biological_age` y `s5_evaluation`. Las variables de cada nivel están en `src/config/model_sets.py`, y el entrenamiento del modelo final, en `src/pipeline/s5_build_model.py`.
- **Experimentos:**
  - `notebooks/models_lvl1.ipynb` a `models_lvl4.ipynb`: comparación de algoritmos y selección de variables de cada nivel, con validación cruzada.
  - `notebooks/biological_age.ipynb`: traducción del riesgo a edad.
  - `notebooks/phenoage.ipynb`: comparación con PhenoAge.
  - **`notebooks/final_evaluation.ipynb`: evaluación final en test, con todas las cifras de los apartados 3 y 4.** Entrena con train sus propios modelos, con la misma función que el pipeline.
- **Salida para el producto:** `models/{base,extras,questionnaire,full}.joblib`. Cada archivo contiene el pipeline de preprocesado y modelo, la referencia para traducir el riesgo a edad y sus columnas.
  - Además, cada modelo guarda de dónde sale: la huella de los datos con que se entrenó, el commit del código y las versiones de Python y de las librerías. Si al cargarlo las versiones instaladas no coinciden, falla en vez de dar resultados distintos sin avisar.
- **Predicción para la app:** `src/models/predict.py` carga un modelo (`load_bundle`) y calcula la edad biológica (`predict_age`) sin necesitar las librerías de entrenamiento.
- **Tests:** `tests/`, con pytest. Comprueban que los cuatro modelos dan la misma edad que la referencia para unas personas inventadas, que la configuración es coherente y que el test sigue siendo exactamente el de la evaluación final. Se ejecutan solos en GitHub Actions en cada push.
- **Requisitos:** `requirements.txt` tiene solo lo que necesita la app para predecir; `requirements-dev.txt`, todo el análisis.
- **Visión general del proyecto:** `README.md`.


**Reproducir**
Desde la raíz del repo con Python 3.11:
  ```bash
  py -3.11 -m venv .venv
  .venv/Scripts/python -m pip install -r requirements-dev.txt
  .venv/Scripts/python -m src.main
  .venv/Scripts/python -m pytest
  ```
  Descarga NHANES, construye Gold y entrena el modelo final (unos 7 minutos más la descarga). Después, los tests comprueban que todo cuadra.
  Por último, ejecuta `notebooks/final_evaluation.ipynb`.

**Aviso:** el proyecto sigue vivo y no paro de trabajar en él, así que si algo del repo no cuadra exactamente con este documento, es por eso. Las cifras de los apartados 3 y 4 son las de la evaluación final, que no se ha vuelto a tocar.
