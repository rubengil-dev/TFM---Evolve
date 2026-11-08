# Qué hay en este archivo y cómo usarlo
- **Contiene:** cómo está hecho el proyecto: repo, entorno, comandos, estructura, datos y sus limitaciones conocidas. Es un resumen para no tener que buscarlo en el código.
- **No contiene:** el porqué de cada elección ni lo pendiente.
- **Se actualiza:** cuando cambia algo de lo que describe.

## Repo
- GitHub: https://github.com/rubengil-dev/TFM---Evolve. Rama principal: `main`.
- Ignorados en git: `data/`, `private/`, `.venv/` y `.env`. Windows, con Git Bash y PowerShell.

## Entorno
- Python 3.11 en `.venv`: `py -3.11 -m venv .venv` y `.venv/Scripts/python -m pip install -r requirements.txt`.
- Al añadir una librería: instalarla en `.venv` y regenerar con `pip freeze > requirements.txt`.
- Librerías clave: pandas y numpy, pyarrow (parquet), lifelines (supervivencia), scikit-learn (split y preprocesado), scikit-survival y xgboost (modelos), requests (descarga) y matplotlib.

## Comandos
- Pipeline completo, desde la raíz: `.venv/Scripts/python -m src.main`. Sin la descarga, los pasos de datos tardan menos de un minuto.
- Solo el modelo: `.venv/Scripts/python -c "from src.pipeline import s5_build_model; s5_build_model.run()"`.

## Estructura
- `src/main.py`: único punto de entrada del pipeline; llama a cada `run()` en orden.
- `src/config/`: rutas, fuentes externas, códigos de los cuestionarios, parámetros del estudio, renombres, correcciones CDC, papel de cada columna de Gold, rangos posibles por variable, umbrales de la validación y variables de cada bloque del modelo, con las descartadas.
- `src/utils/`: funciones compartidas por tema (descarga, lectura de NHANES, fórmulas de las features derivadas, resumen de cada capa, validación de Gold).
- `src/pipeline/`: un archivo por paso, numerado y con su `run()`: `s1_download_bronze`, `s2_build_raw_silver`, `s3_build_clean_silver`, `s4_build_gold` y `s5_build_model` (por ahora, sin lógica).
- `src/models/`: los subpasos que llama `s5_build_model`: `s1_split`, `s2_preprocessing`, `s3_algorithms`, `s4_biological_age` y `s5_evaluation`.
- `notebooks/`: exploración, muestra para la Entrega 02, correlaciones de las candidatas a Base y uno de trabajo por nivel del modelo y otro de la edad biológica.
- `docs/entregas/`: entregas del máster.
- `data/`: capas de datos; se regenera con el pipeline.
- `private/`: analíticas reales.

## Datos
- Bronze (`data/01_bronze/`): una carpeta por ciclo con los ficheros de la CDC y su nombre original, mortalidad incluida. La descarga es reanudable y deja un `manifest.csv`.
- Silver raw (`data/02_silver/silver_raw.parquet`): un único dataframe, una fila por persona, con los alias de laboratorio ya unificados entre ciclos.
- Silver clean (`data/02_silver/silver_clean.parquet`): población del estudio, correcciones CDC, unidades españolas, cuestionarios a respuestas de botón, pesos combinados y valores imposibles vaciados.
- Gold (`data/03_gold/gold.parquet`): la tabla del modelo y de la app, con identificación, desenlace, predictores candidatos (parejas correlacionadas incluidas) y features derivadas. Solo se guarda si pasa la validación.

## Limitaciones conocidas de los datos
- Fosfatasa alcalina y LDH más altas en 1999-2000, sin ecuación oficial de corrección. Urea algo más alta en 2017-2018 incluso corregida.
- RDW: la mediana pasa de 12,5 antes de 2013 a 13,5 en 2013-2018. La CDC lo atribuye al cambio de analizador de 2012 y no hay corrección oficial, porque no se pudieron repetir muestras antiguas. Está en Gold, pero ningún modelo lo usa.
- Serie roja, plaquetas y leucocitos: la CDC también avisa de posibles efectos de método en hematocrito, HCM, CHCM y leucocitos en 2013-2014, y de cambios de tendencia en plaquetas, hematíes, hematocrito, leucocitos y CHCM entre 2005-2006 y 2011-2012.
- Actividad física con salto en 2007 por el cambio de cuestionario.
- Tabaco de 18-19 años hasta 2012 sacado de las preguntas juveniles: hasta 2010 no distingue exfumadores.
- Alcohol sin dato para 18-19 años en 1999-2010: el cuestionario de adultos solo se pasó a mayores de 20, y el juvenil solo existe en 2009-2010.
- Insulina: armonizada, pero a igual IMC queda un salto de ~15% entre 2007-2008 y 2009-2010 que ninguna ecuación de la CDC explica.
- Variables solo en parte de la muestra: subgrupo en ayunas (triglicéridos, insulina), CPK solo en 2011-2018 y PCR sin 2011-2014.
- Últimos ciclos con pocas defunciones por su seguimiento corto.