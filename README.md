# Calculadora de edad biológica

TFM del máster de Data Science e IA de EVOLVE. Una web gratuita que estima la edad biológica a partir de una analítica de sangre real: el usuario sube el PDF, revisa los valores leídos y, si quiere, responde un cuestionario de hábitos.

No es consejo médico ni diagnóstico.

## Cómo funciona
- **Datos:** NHANES 1999-2018 (EE. UU.) con su mortalidad enlazada hasta 2019. Adultos de 18 a 79 años.
- **Modelo:** no existe una etiqueta de "edad biológica real", así que un modelo de supervivencia (Cox) estima el riesgo de morir a 10 años, y ese riesgo se traduce a la edad a la que una persona típica del mismo sexo tiene el mismo riesgo, al estilo de PhenoAge (Levine et al., 2018).
- **Cuatro niveles**, según lo que traiga el usuario: analítica básica, más analítica ampliada, más cuestionario, o todo junto.
- **Privacidad:** son datos de salud; la app procesa todo en memoria y no guarda nada.

El detalle de los datos, las decisiones y la evaluación está en [`docs/entregas/`](docs/entregas/).

## Estado
- Hecho: datos, preparación y modelo.
- En curso: la app (lectura del PDF, revisión, cuestionario y resultado) y su despliegue.

## Reproducirlo
Python 3.11, desde la raíz del repo (Windows):

```bash
py -3.11 -m venv .venv
.venv/Scripts/python -m pip install -r requirements-dev.txt
.venv/Scripts/python -m src.main
.venv/Scripts/python -m pytest
```

- `src.main` descarga NHANES (unos 400 MB, reanudable), construye las capas de datos y entrena los modelos de `models/`.
- Los tests que necesitan `data/` se saltan si no existe; el resto funciona con lo que hay en git.
- `requirements.txt` es solo lo que necesita la app para cargar un modelo y predecir; `requirements-dev.txt`, todo el análisis.

## Estructura
| Carpeta      | Qué contiene                                                                                   |
|--------------|------------------------------------------------------------------------------------------------|
| `src/`       | Pipeline (`pipeline/`), modelo (`models/`), configuración (`config/`) y utilidades (`utils/`)  |
| `models/`    | Un modelo entrenado por nivel, con sus datos de origen y las versiones de las librerías        |
| `notebooks/` | Exploración, comparación de modelos por nivel, edad biológica, PhenoAge y evaluación final     |
| `tests/`     | Tests con pytest; se ejecutan en GitHub Actions en cada push                                   |
| `docs/`      | Entregas del máster                                                                            |
| `data/`      | Capas Bronze → Silver → Gold; no está en git, se regenera con el pipeline                      |

## Limitaciones principales
- Población de referencia de EE. UU.: se asume equivalente a la española.
- Algunos analitos cambian de método entre ciclos sin corrección oficial (p. ej. RDW, que queda fuera del modelo).
- La edad biológica es menos precisa en personas jóvenes de riesgo bajo.
