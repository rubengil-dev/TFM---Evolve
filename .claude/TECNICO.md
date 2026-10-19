# Qué hay en este archivo y cómo usarlo
- **Contiene:** cómo está hecho el proyecto: repo, entorno, comandos, estructura, datos y sus limitaciones conocidas. Es un resumen para no tener que buscarlo en el código.
- **No contiene:** el porqué de cada elección ni lo pendiente.
- **Se actualiza:** cuando cambia algo de lo que describe.

## Repo
- GitHub: https://github.com/rubengil-dev/TFM---Evolve. Rama principal: `main`.
- Saltos de línea LF, fijados en `.gitattributes`. Al reescribir archivos con scripts en Windows, conservar LF.
- Ignorados en git: `data/`, `private/`, `.venv/` y `.env`.

## Entorno
- Python 3.11 en `.venv`: `py -3.11 -m venv .venv` y `.venv/Scripts/python -m pip install -r requirements.txt`.
- Al añadir una librería: instalarla en `.venv` y regenerar con `pip freeze > requirements.txt`.
- Librerías clave: pandas y numpy, pyarrow (parquet), lifelines (supervivencia), requests (descarga) y matplotlib.

## Comandos
- Pipeline de datos completo, desde la raíz: `.venv/Scripts/python -m src.main`. Sin la descarga tarda menos de un minuto.

## Estructura
- `src/main.py`: único punto de entrada del pipeline; llama a cada `run()` en orden.
- `src/config/`: rutas, fuentes externas, parámetros del estudio, renombres, correcciones CDC y papel de cada columna de Gold.
- `src/utils/`: funciones compartidas por tema (descarga, lectura de NHANES, fórmulas de las features derivadas).
- `src/pipeline/`: un archivo por paso, cada uno con su `run()`.
- `notebooks/`: exploración y muestra para la Entrega 02.
- `docs/entregas/`: entregas del máster.
- `data/`: capas de datos; se regenera con el pipeline.
- `private/`: analíticas reales.

## Datos
- Bronze (`data/01_bronze/`): una carpeta por ciclo con los ficheros de la CDC y su nombre original, mortalidad incluida. La descarga es reanudable y deja un `manifest.csv`.
- Silver raw (`data/02_silver/silver_raw.parquet`): un único dataframe, una fila por persona, con los alias de laboratorio ya unificados entre ciclos.
- Silver clean (`data/02_silver/silver_clean.parquet`): población del estudio, correcciones CDC, unidades españolas, cuestionarios a respuestas de botón y pesos combinados.
- Gold (`data/03_gold/gold.parquet`): la tabla del modelo, con identificación, desenlace, predictores candidatos y features derivadas.

## Limitaciones conocidas de los datos
- Fosfatasa alcalina y LDH más altas en 1999-2000, sin ecuación oficial de corrección. Urea algo más alta en 2017-2018 incluso corregida.
- Actividad física con salto en 2007 por el cambio de cuestionario.
- Alcohol sin dato para 18-19 años en 1999-2006 (cuestionario solo para mayores de 20).
- Variables solo en parte de la muestra: subgrupo en ayunas (triglicéridos, insulina), CPK solo en 2011-2018 y PCR sin 2011-2014.
- Últimos ciclos con pocas defunciones por su seguimiento corto.
