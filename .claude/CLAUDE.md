# TFM: calculadora web de edad biológica

Al empezar cada sesión, lee enteros `.claude/CONTEXTO.md` (qué es el proyecto y lo ya decidido) y `.claude/ESTADO.md` (punto actual y lo abierto). 
    - Si ESTADO tiene una sección "PRÓXIMA SESIÓN", se empieza por ahí.

## Archivos
- `CONTEXTO.md`: estable, no se toca salvo que yo lo pida. Solo el qué y el porqué (producto, decisiones de fondo, restricciones), sin nombres de carpetas, archivos ni variables.
- `ESTADO.md`: foto del punto actual, no un historial: si algo se prueba, falla y se arregla, solo queda el resultado final. Tres secciones: PRÓXIMA SESIÓN (por dónde empezar), CONSTRUIDO (estructura, qué hace cada pieza, detalles de lo hecho) y PENDIENTE (plazos, tareas, decisiones abiertas, problemas conocidos).
- `HISTORICO.md`: una entrada breve por sesión (fecha, qué se hizo, decisiones con su motivo, incidencias, hashes de commit). Se escribe al cerrar, pero **no se lee** salvo que yo lo pida o haya que averiguar cuándo se rompió algo.
- `docs/entregas/`: las entregas hechas no se tocan salvo petición explícita. Las nuevas puedes escribirlas, pero no se commitean sin mi revisión.
- `data/` (NHANES, se descarga con script) y `private/` (analíticas reales) están ignoradas. Las analíticas reales nunca se suben al repo ni se pegan en ESTADO/CONTEXTO.

## Cómo explicarme las cosas
- Hablamos en español.
- Soy bioquímico: lo biomédico no hace falta explicármelo. Lo técnico (arquitectura, librerías, front, backend, hosting) en lenguaje llano, con opciones y una recomendación; si hace falta, pregúntame antes.
- Avísame cuando una decisión técnica perjudique la UX, el alcance del TFM o los límites de los planes gratuitos de hosting.

## Forma de trabajo
- Primero hablamos el tema hasta estar de acuerdo. Después lo implementas entero del tirón y resumes en pocas líneas qué has hecho, como un dev junior a su jefe de proyecto.
- Prioridad: MVP end-to-end funcional y desplegado antes de pulir cada pieza.
- Notebooks (`notebooks/`) independientes del código: no importan nada de `src/`. Las funciones reutilizables se escriben completas en el notebook y se duplican en `src/`; si cambian, se cambian en los dos sitios.
- Resultados del modelo (C-index, calibración, subconjuntos de variables) siempre con la semilla y la partición indicadas.
- Pruebas: las ejecutas tú (tests, scripts, servidor local + peticiones). Lo visual no lo puedes juzgar bien: déjamelo en ESTADO como "Pendiente de probar yo".

## Estilo de código
Antes de escribir o modificar código por primera vez en una sesión, lee `.claude/ESTILO.md` y síguelo. Solo una vez por sesión, y no lo leas si la sesión es solo de debate o decisiones.

## Entorno
- Python 3.11 en `.venv`: `py -3.11 -m venv .venv` y `.venv/Scripts/python -m pip install -r requirements.txt`.
- Al añadir una librería: instalarla en `.venv` y regenerar con `pip freeze > requirements.txt`.

## Cierre de sesión
Cuando diga "cerramos", "actualiza", "hemos terminado por hoy" o similar:
1. Test rápido solo de lo nuevo.
2. Actualiza `ESTADO.md` y dime resumidamente qué has cambiado para que dé el OK.
3. Si todo va bien, propón añadir la entrada de la sesión a `HISTORICO.md` con los hashes y commitéala.
4. Después propón commit, merge si aplica y push a GitHub. Con mi OK, ejecútalo.

## Git
- Cambios sencillos sin riesgo: en la rama actual. Features, bugs o cualquier cosa con riesgo: rama nueva, que se fusiona a `main` al cerrar la sesión si todo va bien.
- Commits y merges solo con mi OK. Mensajes breves.
