# Metadatos

## Qué contiene
Mapa de carpetas y archivos del proyecto, con una o dos palabras que dicen para qué sirve cada uno. Sin funciones ni código.

Lo que no encaje en esta descripción no va aquí. El contenido de `.claude/` no se lista: lo indexa `CLAUDE.md`.

## Actualización
- Se actualiza cuando se crea, mueve, renombra o borra una carpeta o un archivo, en el mismo cambio.
- Van todas las carpetas y todos los archivos, aunque git los ignore (p. ej. los datos). Solo se omite lo que se regenera (entornos virtuales, dependencias, cachés), el contenido de `.claude/`, los `README.md` de cada carpeta y los archivos de `tests/`, que se lista solo como carpeta con la nota `# replica src/`. De una carpeta con miles de archivos basta la carpeta.
- Cada línea: nombre y una o dos palabras. Si algo necesita más explicación, va en el `README.md` de su carpeta.


# Contenido

## Mapa
```
TFM/
├── .claude/                          # Archivos de Claude
├── .github/
│   └── workflows/
│       └── ci.yml                    # CI: ruff y tests
├── data/                             # Datos (fuera de git)
│   ├── 01_bronze/                    # NHANES crudo
│   │   ├── 1999_2000/ … 2017_2018/   # Ficheros de la CDC, por ciclo
│   │   └── manifest.csv              # Registro de descarga
│   ├── 02_silver/
│   │   ├── silver_raw.parquet        # Ciclos unidos
│   │   └── silver_clean.parquet      # Población limpia
│   └── 03_gold/
│       └── gold.parquet              # Tabla del modelo
├── docs/
│   ├── import_graph.md               # Grafo de imports
│   └── entregas/                     # Entregas del máster
│       ├── 01_ideas_producto.md      # Entrega 01
│       ├── 02_datos_y_preparacion.md # Entrega 02
│       ├── 02_gold_sample.csv        # Muestra de Gold
│       ├── 03_machine_learning.md    # Entrega 03
│       ├── 04_diseno_frontal_ux.md   # Entrega 04
│       ├── 04_capturas/              # Capturas de la Entrega 04
│       ├── enunciado3.pdf            # Enunciado 03 (fuera de git)
│       └── enunciado4.pdf            # Enunciado 04 (fuera de git)
├── frontend/                         # Web (React)
│   ├── public/
│   │   └── favicon.svg               # Icono
│   ├── src/
│   │   ├── components/
│   │   │   ├── CellBackground.tsx    # Fondo de células
│   │   │   ├── ChoiceCards.tsx       # Tarjetas de opciones
│   │   │   ├── GroupIcon.tsx         # Icono de cada grupo
│   │   │   ├── ImpossibleValue.tsx   # Ventana de valor imposible
│   │   │   ├── Logo.tsx              # Logo
│   │   │   ├── NumberSlider.tsx      # Barra de números
│   │   │   ├── OrganIcons.tsx        # Iconos anatómicos
│   │   │   ├── ProgressBar.tsx       # Barra de progreso
│   │   │   ├── ShareButtons.tsx      # Compartir y descargar
│   │   │   ├── WarningBar.tsx        # Franja del aviso
│   │   │   └── YearsTable.tsx        # Tabla de años
│   │   ├── config/
│   │   │   ├── errors.ts             # Textos de error
│   │   │   ├── example.ts            # Datos de ejemplo y demos
│   │   │   ├── groups.ts             # Grupos del resultado
│   │   │   └── questions.ts          # Preguntas
│   │   ├── pages/
│   │   │   ├── ErrorScreen.tsx       # Errores
│   │   │   ├── Landing.tsx           # Portada
│   │   │   ├── Loading.tsx           # Carga
│   │   │   ├── Questionnaire.tsx     # Cuestionario
│   │   │   └── Result.tsx            # Resultado
│   │   ├── utils/
│   │   │   ├── cells.ts              # Dibujo de una célula
│   │   │   └── picture.ts            # Imagen para compartir
│   │   ├── App.tsx                   # Pantalla activa
│   │   ├── index.css                 # Colores y fuentes
│   │   ├── main.tsx                  # Arranque
│   │   └── types.ts                  # Tipos comunes
│   ├── .gitignore                    # Fuera de git
│   ├── .oxlintrc.json                # Linter
│   ├── index.html                    # Página única
│   ├── package.json                  # Dependencias y comandos
│   ├── package-lock.json             # Versiones exactas (npm)
│   ├── tsconfig.app.json             # TypeScript de la app
│   ├── tsconfig.json                 # TypeScript raíz
│   ├── tsconfig.node.json            # TypeScript de Vite
│   └── vite.config.ts                # Vite
├── models/                           # Modelos entrenados
│   ├── routine.joblib                # Nivel 1
│   ├── extras.joblib                 # Nivel 2
│   ├── questionnaire.joblib          # Nivel 3
│   └── full.joblib                   # Nivel 4
├── notebooks/
│   ├── 01_exploration_raw.ipynb      # Exploración (entregable)
│   ├── 02_gold_sample.ipynb          # Muestra Entrega 02 (entregable)
│   ├── routine_correlations.ipynb    # Correlaciones de Routine
│   ├── models_lvl1.ipynb             # Nivel 1
│   ├── models_lvl2.ipynb             # Nivel 2
│   ├── models_lvl3.ipynb             # Nivel 3
│   ├── models_lvl4.ipynb             # Nivel 4
│   ├── biological_age.ipynb          # Riesgo a edad
│   ├── phenoage.ipynb                # Comparación PhenoAge
│   └── final_evaluation.ipynb        # Evaluación en test
├── private/                          # Analíticas reales en PDF (fuera de git)
├── src/
│   └── bioage/                       # Paquete del proyecto
│       ├── __init__.py
│       ├── main.py                   # Punto de entrada
│       ├── app/
│       │   ├── __init__.py
│       │   └── predict.py            # Predicción
│       ├── config/
│       │   ├── __init__.py
│       │   ├── corrections.py        # Correcciones CDC
│       │   ├── gold_columns.py       # Columnas de Gold
│       │   ├── model_levels.py       # Variables por nivel
│       │   ├── nhanes_codes.py       # Códigos de cuestionarios
│       │   ├── paths.py              # Rutas
│       │   ├── phenoage.py           # Constantes PhenoAge
│       │   ├── plausible_ranges.py   # Rangos posibles
│       │   ├── renames.py            # Renombres
│       │   ├── sources.py            # Fuentes externas
│       │   ├── study.py              # Parámetros del estudio
│       │   └── validation_rules.py   # Umbrales de validación
│       ├── modeling/
│       │   ├── __init__.py
│       │   ├── s1_split.py           # Split
│       │   ├── s2_preprocessing.py   # Preprocesado
│       │   ├── s3_algorithms.py      # Algoritmos
│       │   ├── s4_biological_age.py  # Riesgo a edad
│       │   └── s5_evaluation.py      # Evaluación
│       ├── pipeline/
│       │   ├── __init__.py
│       │   ├── s1_download_bronze.py # Descarga
│       │   ├── s2_build_raw_silver.py # Silver raw
│       │   ├── s3_build_clean_silver.py # Silver clean
│       │   ├── s4_build_gold.py      # Gold
│       │   └── s5_build_model.py     # Modelo final
│       └── utils/
│           ├── __init__.py
│           ├── data_download.py      # Descarga
│           ├── features.py           # Features derivadas
│           ├── nhanes.py             # Lectura de NHANES
│           ├── notebook_helpers.py   # Apoyo a notebooks
│           ├── phenoage.py           # Fórmula PhenoAge
│           ├── provenance.py         # Origen del modelo
│           ├── step_info.py          # Guardado y resúmenes
│           └── validation.py         # Validación de Gold
├── tests/                            # replica src/
├── .gitattributes                    # Saltos de línea
├── .gitignore                        # Archivos fuera de git
├── .pre-commit-config.yaml           # Hooks de pre-commit
├── LICENSE                           # Licencia MIT
├── pyproject.toml                    # Proyecto, dependencias y herramientas
├── README.md                         # Presentación del proyecto
└── uv.lock                           # Versiones exactas (uv)
```
