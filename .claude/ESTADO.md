# Metadatos

## Qué contiene
Lo que frena el avance y lo que me toca a mí, más el contador para saber cuándo toca revisión integral. En qué fase estamos y qué falta no se repite aquí: lo dice `PLAN.md`.

Lo que no encaje en esta descripción no va aquí.

## Actualización
- Se actualiza al cerrar cada sesión y cuando aparece o se resuelve un bloqueo o una tarea mía.
- Solo guarda lo vigente: lo resuelto se borra. El historial está en git.
- Cada bloqueo dice qué frena, por qué y qué lo desbloquea, y la casilla de `PLAN.md` afectada se marca con `[/]`. Al resolverlo, esa casilla vuelve a `[ ]` o `[*]`.
- Un bloqueo puede ser una decisión pendiente que impide avanzar. Si no impide nada, va a `NOTAS.md`.
- Aquí va lo que me toca a mí y no puedes hacer tú: crear cuentas, darte claves o permisos, contratar un servicio, y lo que he dicho que no pruebo ahora (ver `PROTOCOLOS.md`).


# Contenido

## Revisión integral
Sesiones desde la última: 2

## Bloqueos
Todos son decisiones pendientes. Los de la fase 4 se cierran al empezarla, pensando en la Entrega 04 y empezando por el stack y el flujo de pantallas.

- **Stack de front y backend.** Frena todas las casillas de la fase 4: sin él no se puede escribir la app. Lo desbloquea: elegirlo.
- **Cómo elige el usuario el modo.** Frena el flujo de pantallas. Idea: dos pestañas, "solo analítica" por defecto y "analítica + cuestionario". Lo desbloquea: decidirlo con el flujo.
- **Diseño del parser y de la normalización de nombres y unidades.** Frena el parser. Lo desbloquea: decidirlo, y antes decidir cómo anonimizar los PDFs de `private/` para que Claude pueda leerlos (la app sí puede leerlos sin anonimizar, en local).
- **Mínimo viable de variables:** con qué datos faltantes se deja de calcular. Frena la validación de lo que entra al modelo. Lo desbloquea: decidirlo.
- **Resultado.** Frena la pantalla de resultado. Lo desbloquea: decidir estos cinco puntos.
  - Cómo calcular y mostrar el margen ± X años.
  - Cómo mostrar las edades biológicas fuera de 18-79 y la cola de personas muy por encima de su edad.
  - Cómo agrupar las variables ligadas (serie roja, transaminasas) en los mejores y peores parámetros, para que los signos se entiendan.
  - Cuántos parámetros mejores y peores se muestran.
  - Umbral de años por encima para remitir al médico.
- **Qué pide el profesor de MLOps** (registro de modelos, CI, monitorización). Frena DVC y MLflow, en la fase 6. Lo desbloquea: preguntárselo (me toca a mí).

## Me toca a mí
- Preguntar al profesor qué hay que demostrar de MLOps.
- Conseguir analíticas de ejemplo de distintos laboratorios españoles para probar el parser (tengo PDFs propios).
