# Entrega 02: Datos y preparación

La idea final elegida es la calculadora web de edad biológica a partir de una analítica de sangre. Se entrenará un modelo de supervivencia (riesgo de mortalidad a partir de biomarcadores) y ese riesgo se traduce a una edad equivalente, al estilo PhenoAge (Levine et al., 2018).

## 1. ¿Qué datos necesita el producto?

**Observación** 
Cada una es un adulto de 18 a 79 años con analítica, medidas corporales y seguimiento de mortalidad. Una fila = una persona: cada ciclo de NHANES es una muestra independiente y nadie se repite. La restricción por edad se debe a que; menores de 18 tienen valores distintos a los adultos, y superiores a 79 NHANES los agrupa todos en 80 y no es interpretable.

**Datos Imprescindibles**

- Edad y sexo de cada persona.

- Analítica y mortalidad en las mismas personas: una cohorte con biomarcadores medidos en un momento y seguimiento posterior de quién fallece y cuándo. Sin desenlace no se puede entrenar un modelo de supervivencia.

- Los parámetros de dicha analítica deben estar en una analítica de rutina española (hemograma y bioquímica básica), medidos con métodos de laboratorio clínico y en unidades convertibles a las españolas.

- Tamaño suficiente: decenas de miles de personas y miles de defunciones, para estimar el efecto de muchas variables y tolerar huecos.

- Datos de uso libre y desidentificados.

**Datos Deseables**

- Analítica ampliada en toda la muestra (PCR, vitamina D, insulina, ferritina, TSH, B12…).

- Datos que el usuario conoce o puede responder: peso, talla, tensión y hábitos objetivos (tabaco, alcohol, actividad, sueño, dieta).

- Seguimiento largo y mismo protocolo de laboratorio durante todo el periodo.

- Mediciones repetidas de la misma persona en el tiempo.

- Otras estimaciones como DXA o VO2_Max habrían sido una gran incorporación, pero no son variables que el usuario conozca a la hora de la simulación.

**Qué cubre NHANES** 

- Todos los imprescindibles. 

- De los deseables: medidas, hábitos y parte de la analítica ampliada (PCR, vitamina D e insulina, esta última solo en ayunas).

No cubre ferritina y TSH en toda la muestra, ni mediciones repetidas. Además, tiene cambios de método entre ciclos.

**Granularidad e histórico** 

Una medición por persona más su seguimiento de mortalidad. Son 10 ciclos bienales, de 1999 a 2018, con un seguimiento mediano de 9,6 años.

## 2. Fuentes y viabilidad

| Fuente | Tipo | Acceso |
|---|---|---|
| **NHANES continuo 1999-2018** (CDC) | Open data: ficheros `.xpt` (SAS) por módulo y ciclo | Descarga directa por URL |
| **Linked Mortality Files** (NCHS), versión pública | Open data: un `.dat` de ancho fijo por ciclo, seguimiento hasta el 31/12/2019 | Descarga directa por URL |

- **Acceso reproducible:** `src/pipeline/download_bronze.py` descarga los 400 ficheros (~419 MB). Es reanudable, valida que lo recibido no sea una página de error y guarda un manifiesto con URL, tamaño y fecha.

- **Cobertura:** población no institucionalizada de EE. UU. Hay 54.809 adultos de 18 a 79 años elegibles para mortalidad y 48.495 entran en el estudio, con 5.425 defunciones. La analítica general está en el ~94% de las personas. El subgrupo en ayunas (triglicéridos, insulina) es ~50% y la CPK solo existe de 2011 a 2018.

- **Actualización:** NHANES sigue publicando ciclos, pero los posteriores a 2018 aún no tienen mortalidad pública. La versión con seguimiento hasta 2022 es de acceso restringido.

- **Estabilidad:** las URLs de la CDC son estables. Una caída puntual del servidor de mortalidad se resolvió con reintentos.

- **Alternativa:** si NHANES dejara de estar disponible, los datos ya descargados siguen sirviendo. Como fuente alternativa, UK Biobank, que requiere solicitud y es de pago. NHANES III está descartado porque usa métodos de laboratorio y un formato distintos.

## 3. Usabilidad, privacidad y datos personales

- **Licencia:** NHANES y la mortalidad pública son de dominio público (gobierno de EE. UU.), con uso libre citando la fuente.

- **Datos personales:** vienen desidentificados de origen. Además, el NCHS perturba la versión pública de la mortalidad para evitar reidentificaciones. No hace falta anonimizar.

- **Minimización:** de 993 variables descargadas, solo 68 llegan a Gold. No se usan etnia, ingresos, educación ni geografía. La edad se limita a 79 años porque NHANES agrupa las edades superiores.

- **Producto final:** una analítica es un dato de salud (categoría especial del RGPD). Se procesa en memoria, no se almacena nada y no hay registro ni email. Se informa al usuario de forma clara.

## 4. Pipeline del modelado de datos

| Capa | Qué es | Resultado |
|---|---|---|
| **Bronze** | Ficheros tal como los publica la CDC, una carpeta por ciclo, con su nombre original | 400 files, ~419 MB |
| **Silver raw** | Un único fichero (raw) fruto de combinar los 10 ficheros resultantes de unir los ficheros de cada ciclo unidos por persona (SEQN) | 54.809 ppl, 993 cols |
| **Silver clean** | Silver raw limpio: filtrado por población de estudio, variables limpias y renombradas y unidades estandarizadas al sistema español | 48.495 ppl, 72 cols |
| **Gold** | Silver clean pero restringiendo a variables candidatas a predictor, features derivadas y desenlace | 48.495 ppl, 68 cols |

**Bronze → Silver raw**
- Unión de unos 25 ficheros por ciclo más la mortalidad, partiendo de los participantes de demografía. Las columnas repetidas entre ficheros se rellenan entre sí si coinciden.
- Alias entre ciclos unificados antes de apilar (ej: HDL tiene tres nombres distintos a lo largo de los ciclos).
- Filtro de adultos de 18 a 79 años elegibles para mortalidad.

**Silver raw → Silver clean**
- Exclusiones: sin examen físico, embarazadas (analítica alterada) y personas sin ningún valor de laboratorio (esencial para el producto final).
- Correcciones oficiales de la CDC por cambios de método: creatinina en 1999-2000 y 2005-2006, y 13 analitos en 2017-2018 por cambio de analizador.
- Códigos de "no sabe/no contesta" convertidos a nulos.
- Unidades de laboratorio español: urea (BUN × 2,14), PCR en mg/L (dos ensayos en una columna) y cociente albúmina/creatinina en orina en mg/g.
- Triglicéridos solo con ayuno ≥ 8 h.
- Tensión como media de hasta 4 lecturas.
- Cuestionarios convertidos a categóricas (ej: {tabaco: nunca/exfumador/fumador}). Las preguntas saltadas cuentan como "nunca".
- Pesos muestrales combinados para los 10 ciclos, según la regla de la CDC.

**Silver clean → Gold**
- **De las variables muy correlacionadas (r > 0,8) entra una:** hemoglobina (no hematocrito), VCM (no HCM), leucocitos (no neutrófilos absolutos) e IMC (no peso ni cintura). Del hemograma se usan recuentos absolutos, no porcentajes. 
    *NOTA*: Para el producto final, si el usuario incluye la variable descartada en vez de la seleccionada, el programa calculará la seleccionada en base a la descartada.
- **Features derivadas**: cociente neutrófilos/linfocitos (NLR), plaquetas/linfocitos (PLR), índice inmunoinflamatorio sistémico (SII), colesterol no-HDL, TG/HDL, AST/ALT, globulinas, cociente albúmina/globulina, urea/creatinina, filtrado glomerular CKD-EPI 2021 (sin raza), HOMA-IR y presión de pulso.
- Las 5 defunciones con 0 meses de seguimiento pasan a 0,1 meses, porque los modelos de supervivencia necesitan tiempo > 0.
    *NOTA*: Las features derivadas que son combinaciones lineales de otras (no-HDL, globulinas, presión de pulso) se dejan para probar cuáles hacen que el modelo prediga mejor.
- **No se hace en Gold:** rellenar huecos (el modelo debe ser robusto a nulos), recortar extremos (aprendería del dataset entero), escalar ni codificar categorías (pre-processing).

**¿Qué hay en gold?**

Cada fila es una persona adulta con su analítica en la visita de examen y su desenlace: si ha fallecido y cuántos meses han pasado hasta la muerte o hasta el 31/12/2019.

| Grupo | Columnas | Uso |
|---|---|---|
| Identificación | `seqn`, `cycle`, `weight_exam` | Trazabilidad, partición por ciclo, peso muestral en el entrenamiento |
| Desenlace | `follow_up_months`, `death` | Variable objetivo del modelo de supervivencia |
| Demografía | `age`, `sex` | Predictores, y edad para traducir el riesgo a edad biológica |
| Hemograma (12) | leucocitos, hematíes, hemoglobina, VCM, CHCM, RDW, plaquetas, VPM, linfocitos, monocitos, eosinófilos, basófilos | Predictores |
| Bioquímica (27) | glucosa, urea, creatinina, ácido úrico, colesterol total, HDL, triglicéridos, AST, ALT, GGT, fosfatasa alcalina, bilirrubina, Na, K, Cl, Ca, P, proteínas, albúmina, hierro, LDH, CPK, HbA1c, PCR, vitamina D, insulina, albúmina/creatinina en orina | Predictores |
| Medidas (3) | IMC, tensión sistólica y diastólica | Predictores opcionales |
| Hábitos (7) | tabaco, frecuencia de alcohol, bebidas por día, actividad física, horas sentado, comida rápida, horas de sueño | Predictores del modo avanzado |
| Derivadas (12) | `nlr`, `plr`, `sii`, `non_hdl`, `tg_hdl`, `ast_alt`, `globulin`, `albumin_globulin`, `urea_creatinine`, `egfr`, `homa_ir`, `pulse_pressure` | Predictores candidatos |

Cobertura: la mayoría de las variables supera el 90%. Por debajo quedan la CPK (41%), la insulina y el HOMA-IR (47%), la comida rápida (50%), los triglicéridos y el TG/HDL (54%), las horas sentado (64%), el sueño (73%), la PCR (78%), el alcohol (87%) y la vitamina D (89%).

Hay variables que no se incluirán en el modelo pero se dejan en gold para permitir iteraciones posteriores del mismo.

## 5. Riesgos y limitaciones

1. La población de referencia es estadounidense, no española, por lo que se asume que la población es equivalente a la española.

2. Hay cambios de método entre ciclos sin corrección oficial (fosfatasa alcalina y LDH en 1999-2000, cuestionario de actividad en 2007), y los últimos ciclos tienen pocas defunciones por su seguimiento corto (71 en 2017-2018). 

3. Algunas variables solo existen en parte de la muestra (ayunas, CPK, PCR sin 2011-2014), y sus huecos dependen de la época. Si NHANES dejara de estar disponible, los datos descargados seguirían siendo válidos pero no podríamos actualizarlos sin cambiar la fuente.

## Datos y código

- **Muestra:** `docs/entregas/02_gold_sample.csv`, con 100 filas aleatorias de Gold (semilla 5), generada con `notebooks/02_gold_sample.ipynb`.
- **Reproducir todo el flujo** desde la raíz del repo (Python 3.11):
  ```bash
  py -3.11 -m venv .venv
  .venv/Scripts/python -m pip install -r requirements.txt
  .venv/Scripts/python -m src.main
  ```
  Descarga Bronze y construye Silver raw → Silver clean → Gold en `data/` (unos 45 s más la descarga).
- **Código:** `src/pipeline/` tiene un archivo por paso (`download_bronze`, `build_raw_silver`, `build_clean_silver`, `build_gold`). Las fuentes, renombres, correcciones y roles de las columnas de Gold están en `src/config/`, y las fórmulas de las features en `src/utils/features.py`.
