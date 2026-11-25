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
Sesiones desde la última: 0

## Bloqueos
Todos son decisiones pendientes. Los de la fase 4 se cierran al empezarla, pensando en la Entrega 04 y empezando por el stack y el flujo de pantallas.

- **Diseño del parser y de la normalización de nombres y unidades.** Frena el parser. Lo desbloquea: hablarlo, como tarde el 1 de diciembre de 2026. Claude puede leer los PDFs de `private/` sin anonimizar (decidido por Rubén).
- **Mínimo viable de variables:** con qué datos faltantes se deja de calcular. Frena la validación de lo que entra al modelo. Lo desbloquea: el notebook de elección del modelo, y antes que Rubén decida cuántos años puede moverse la edad por los datos que faltan (propuesta: 3).
- **Qué pide el profesor de MLOps** (registro de modelos, CI, monitorización). Frena DVC y MLflow, en la fase 6. Lo desbloquea: preguntárselo (me toca a mí).

## Me toca a mí
- Preguntar al profesor qué hay que demostrar de MLOps.
- Preguntar al profesor si, con la edad biológica 10 o más años por encima, se recomienda comentarla con el médico.
- Revisar el front entero, cuando todo esté conectado y funcionando.
- Conseguir analíticas de ejemplo de distintos laboratorios españoles para probar el parser (tengo PDFs propios).
