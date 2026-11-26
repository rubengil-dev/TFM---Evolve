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
- Huecos de la revisión del 26-11 que piden decisión: (1) el ± a los 16-17 y 80-90 años es el de 18 y 79, aunque estén fuera de los datos; (2) un valor corregido que sigue siendo imposible no se detecta hasta después del cuestionario (sin `/api/correct` en la v1); (3) el mínimo de datos cuenta cuántos valores faltan y no cuáles: solo bioquímica (faltan 6) o solo hemograma (faltan 9) se rechazan aunque cumplen los 7 años; (4) el error base salta de unos 3 años a 0,4 al cruzar el umbral de riesgo (misma persona con glucosa 104 → ± 3, con 108 → sin ±), y con cuestionario sale más ancho que sin él (menos muertes desde 2007).

## Ideas y dudas
- El parser no busca la tensión: ningún modelo la usa.
- Entrega 04, 5.2: la tabla de grupos todavía tiene corazón y la tensión; la buena está en `config/app.py`.
- Para el parser: en los 6 PDFs de Rubén vienen de 2 a 5 de los 8 Extras, uno es un escaneo sin texto, y `pdfplumber` no se dejó instalar (archivo bloqueado, quizá el antivirus).
- Entrega 04: queda como borrador y se reescribe al acabar el resto (se entrega el domingo 29). A Rubén no le cuadran varias cosas, que dirá entonces.
- Entrega 04, esquema del flujo: rehacerlo simple, sin repetir el modo. Elegir modo y PDF → preguntas → carga → ¿se puede calcular? Sí: resultado. No: de ahí salen los errores. Si el PDF no se lee, se vuelve a la portada.
- Entrega 04, capturas: muchas menos, sin duplicar móvil y ordenador, y remitir a ejecutar la app. El enunciado exige al menos una imagen guardada en el repo y enlazada.
- Mirar el histograma de la diferencia entre edad biológica y real del notebook de edad biológica.
- Al desplegar: `ROOT` se calcula desde la ruta de `paths.py`, así que `models/` solo se encuentra si el hosting ejecuta desde el repo (instalación editable), no desde un paquete construido.
- Al elegir hosting: su proxy guarda las IPs aunque la app no lo haga; mirarlo y ajustar la letra pequeña ("no se guarda nada") si hace falta.
- Sesgo en los de 18-29: con los bloques juntos, el modelo les quita de 5 a 7 años (mueren más de lo que predice; solo 81 muertes, quizá accidentes y sobredosis que la analítica no ve). Estudiarlo después de la entrega; corregirlo ahora sería ajustar al ruido.
