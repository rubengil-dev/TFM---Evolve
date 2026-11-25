# Metadatos

## Qué contiene
Cómo se escribe, se organiza y se versiona el proyecto: las convenciones que seguimos (Estándares) y mis gustos personales dentro de ellas (Estilo).

Lo que no encaje en esta descripción no va aquí. Las decisiones propias del proyecto van en `TECNICO.md`; cómo trabajamos, en `PROTOCOLOS.md`.

## Actualización
- Casi inmutable: cambia cuando yo cambio de criterio o adoptamos una convención nueva.
- La configuración de las herramientas (ruff, pytest…) vive en `pyproject.toml`. Si cambia una regla de aquí, cambia allí también, y al revés.
- Si crece demasiado, avísame para dividirlo en dos archivos: estándares y estilo.


# Contenido

## Estándares

### Git
- **Commits:** Conventional Commits, en inglés. Cabecera `tipo(ámbito): descripción` en imperativo, de unos 72 caracteres como máximo, y cuerpo en viñetas con qué incluye y por qué. Tipos: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `build`, `ci`.
  ```
  feat(db): add habits table

  - Columns: id, name, frequency, created_at
  - Unique constraint on name per user
  ```
- No añadas la nota de co-autoría de Claude.
- **Ramas (Git Flow adaptado):**
  - `main` es la versión PRO: lo que ya tenemos y queremos proteger. En la fase 0 se trabaja directo en `main`, porque aún no hay nada que proteger.
  - Desde la fase 1, cada fase tiene su rama `phase-N`, donde se programa.
  - Cada feature sale de `phase-N` como `feat/nombre-corto` y vuelve a `phase-N` cuando está acabada y funciona.
  - `phase-N` entra en `main` solo cuando la fase está terminada y todo funciona.
  - Si algo se rompe en `main`, se arregla en `fix/nombre-corto` desde `main` y se integra en `main` y en la `phase-N` activa.
- **Merges:** siempre merge commit con `--no-ff`. Nada de squash ni rebase, para conservar los commits de cada rama. Sin Pull Requests.
- **Etiquetas de versión:** ninguna hasta terminar el MVP; entonces `v1.0.0`. Cada versión posterior sale de `FUTURO.md`.

### Estructura del proyecto
- **Nombres de archivos y carpetas:** sin acentos ni ñ.
- **Sin código:** sin estructura base fija; la decide la entrevista de cada proyecto. Archivos `categoria_nombre-variante.ext` (prefijo = categoría, sufijo = variante) y una carpeta por familia cuando un grupo de archivos se repite.
- **En la raíz:** `.gitignore`, `.gitattributes`, `LICENSE` y `README.md`.
- **LICENSE:** en todos los proyectos, MIT por defecto.

### README
- En inglés. El de la raíz: qué es, para quién y cómo se instala y ejecuta. Cada carpeta lleva el suyo, mínimo.
- El de una carpeta: su nombre como título, una frase y una lista con lo que contiene, una línea cada uno (nombre y qué hace). Debajo, solo si hace falta, cómo se ejecuta o una `NOTE`.
- Se actualiza el de una carpeta cuando cambia lo que contiene, y el de la raíz cuando cambia cómo se instala o se usa.

### Estructura del código (Python)
- **Carpetas:** `src/<paquete>/` (paquete en `snake_case`, repo en `kebab-case`), `tests/` replicando `src/` con archivos `test_<archivo>.py`, `scripts/` para tareas puntuales y `notebooks/`. Lo que usa la app vive en `src/`, no en `scripts/`.
- **Datos:** `data/` con capas numeradas: `01_bronze` (crudo, nunca se toca a mano), `02_silver` (limpio y validado), `03_gold` (listo para consumir).
- **En la raíz,** además de lo común: `pyproject.toml`, `uv.lock` y `.env.example`. `.env` no se sube a git.

### Herramientas (Python)
- **uv** para entorno y dependencias; `uv.lock` se sube a git. Los proyectos con `.venv` y `requirements.txt` se migran a uv.
- **`pyproject.toml`** en todos: metadatos, dependencias y configuración de las herramientas.
- **Type hints** siempre y en todo.
- **ruff** revisa y formatea. También comprueba que existen docstrings y su forma (convención Google), salvo en `tests/`.
- **pytest** para los tests.
- **pre-commit** ejecuta ruff y los tests rápidos antes de cada commit.
- **CI:** GitHub Actions (`.github/workflows/`) ejecuta ruff y pytest en cada push. Se crea cuando el proyecto ya tiene tests.
- **Usar un proyecto desde otro equipo:** `uv add git+<url del repo>`. PyPI solo si se decide en `TECNICO.md`.

### Código (Python)
- **PEP 8.** `snake_case` (variables, funciones, módulos, archivos), `PascalCase` (clases), `MAYUSCULAS` (constantes), `_guion_bajo` (interno). Booleanos con `is_` / `has_`, funciones con verbo, sin abreviaturas raras. Tests: `test_<qué>_<condición>()`.
- **Idioma:** inglés en identificadores, docstrings y comentarios.
- **Docstrings Google** en módulos, clases y funciones, siempre. La primera línea dice qué hace, no cómo ni por qué. `Args:` si hay parámetros, `Returns:` si devuelve algo, `Raises:` si lanza excepciones. La brevedad manda. Excepción: los tests (`tests/`) no llevan docstring, porque su nombre `test_<qué>_<condición>` ya lo dice.
- **Imports:** bajo un único título `# Imports`, en tres bloques separados por una línea en blanco (librería estándar, externas, propias). Cada archivo importa solo lo que usa.
- **Errores:** se capturan excepciones concretas (`ValueError`, `KeyError`…), nunca un `except:` genérico.
- **`print` o `logging`:** `print` solo para lo que el usuario debe leer (el resumen de un script). Lo demás, `logging` con su nivel.
- **Rutas y configuración:** `pathlib` (`ROOT / "data" / "file.csv"`) en `paths.py`; fuentes externas y ajustes en `config.py`. Sin números ni rutas sueltos por el código.
- **`.env`** solo para secretos y lo que cambia según la máquina.

## Estilo

### Global
- **Simplicidad:** cada complicación responde a un problema real; si no, fuera.
- **Nombres descriptivos.** Si el código necesita un comentario largo para entenderse, mejor un nombre más claro.
- **Configuración separada de la lógica.**
- Las tablas de configuración escritas a mano se alinean en columnas.
- Carpetas de etapas numeradas (`01_`, `02_`) para que el orden alfabético sea el del proceso.

### Python
- **Comentarios:** títulos de bloque de una o pocas palabras (`# Imports`, `# Root`). Sin comentarios al final de la línea, salvo para aclarar algo no evidente (unidades, ejemplos, qué significa cada fila de una tabla).
- **Cabeceras:** la docstring de un archivo es una frase si hace una sola cosa; si contiene varias, la frase y debajo una lista con todas.
- **Flechas `→`** para transformaciones o flujos, solo en docstrings y comentarios: la consola de Windows no las muestra en un `print`.
- **Archivos:** cada archivo hace una sola cosa y su docstring lo dice. La función principal va arriba y se lee como un índice (solo llamadas con nombre claro). Las de apoyo, debajo, en el orden en que se llaman, aunque se usen una sola vez.
- **Un único punto de entrada** por programa (`main`), el único con `if __name__ == "__main__":`.
- **Utilidades compartidas** en una carpeta, un archivo por tema. Una función sale ahí cuando no es específica del archivo que la usa.

### Propio de este proyecto
- **Notebooks entregables:** llevan prefijo numérico (`01_`, `02_`) y son independientes: no importan nada de `src/`. Las funciones que comparten con el código se duplican y, si cambian, se actualizan en los dos sitios.
- **Notebooks de trabajo** (experimentos, pruebas): sin prefijo numérico, y sí importan de `src/`.
- **Configuración:** una carpeta `config/` con un archivo por tabla, en vez de un único `config.py`, porque son diez tablas largas. Las rutas siguen en `paths.py`.
- **Sin `.env.example`:** el proyecto no tiene secretos ni nada que cambie según la máquina. Se crea cuando aparezca el primero.
- **Pasos numerados con prefijo `s`** (`s1_`, `s2_`) en vez de `01_`: Python no importa módulos que empiezan por número.
