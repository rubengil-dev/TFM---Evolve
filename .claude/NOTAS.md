# Metadatos

## Qué contiene
Apuntes rápidos sin sitio claro todavía: decisiones pendientes que no bloquean, ideas, dudas y cosas a revisar.

Lo que no encaje en esta descripción no va aquí.

## Actualización
- Cualquiera de los dos añade una línea en cuanto surge algo, sin interpretarlo ni dejarlo para el final. Una línea por apunte, corta.
- Si está claro a qué archivo pertenece, va directo a ese archivo y no pasa por aquí.
- Si un apunte pasa a bloquear algo, se mueve a `ESTADO.md`.
- Se lee al empezar cada fase. Se ordena en la revisión integral (ver `PROTOCOLOS.md`): cada apunte pasa a su archivo o se borra.


# Contenido

## Decisiones pendientes
- La tabla de mejores y peores parámetros puede quedar fuera de la primera versión de la app si vamos justos.
- Almacén remoto de DVC: DagsHub o una carpeta local. Hay que elegirlo antes de montar DVC (fase 6).
- Versión del modelo: registro de MLflow, o etiqueta de git con las huellas de datos y modelo (fase 6).
- Monitorización: si se hace, qué se puede contar sin almacenar datos de salud (fase 6).

## Ideas y dudas
- Mirar el histograma de la diferencia entre edad biológica y real del notebook de edad biológica.
- Al desplegar: `ROOT` se calcula desde la ruta de `paths.py`, así que `models/` solo se encuentra si el hosting ejecuta desde el repo (instalación editable), no desde un paquete construido.
