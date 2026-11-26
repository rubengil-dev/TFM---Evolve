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
- El parser no busca la tensión: ningún modelo la usa.
- Entrega 04, 5.2: la tabla de grupos todavía tiene corazón y la tensión; la buena está en `config/app.py`.
- Para el parser: en los 6 PDFs de Rubén vienen de 2 a 5 de los 8 Extras, uno es un escaneo sin texto, y `pdfplumber` no se dejó instalar (archivo bloqueado, quizá el antivirus).
- Entrega 04: queda como borrador y se reescribe al acabar el resto (se entrega el domingo 29). A Rubén no le cuadran varias cosas, que dirá entonces.
- Entrega 04, esquema del flujo: rehacerlo simple, sin repetir el modo. Elegir modo y PDF → preguntas → carga → ¿se puede calcular? Sí: resultado. No: de ahí salen los errores. Si el PDF no se lee, se vuelve a la portada.
- Entrega 04, capturas: muchas menos, sin duplicar móvil y ordenador, y remitir a ejecutar la app. El enunciado exige al menos una imagen guardada en el repo y enlazada.
- Mirar el histograma de la diferencia entre edad biológica y real del notebook de edad biológica.
- Al desplegar: `ROOT` se calcula desde la ruta de `paths.py`, así que `models/` solo se encuentra si el hosting ejecuta desde el repo (instalación editable), no desde un paquete construido.
- Revisión pendiente de `feat/calculations` (lo hecho el 26-11 sin Rubén): mínimo de datos y modo al leer el PDF, Extras en `choose_level`, margen ± con sus cifras y el aviso gris, conclusiones de `missing_values` y `margin`. Después, commit y reentrenar los modelos, que llevan la marca `-dirty`.
