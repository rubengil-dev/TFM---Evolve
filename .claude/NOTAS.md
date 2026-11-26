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
- Para hablar el parser (propuesta de Claude, sin decidir): reglas (diccionario de sinónimos y patrones) y no un LLM, porque mandar la analítica a una API externa choca con "no se envían tus datos"; la v1 cubre solo los formatos de los 6 PDFs de Rubén y con otro intenta leer y, si no saca bastante, da `too_few`; los escaneados sin texto, fuera de la v1 (`unreadable`); librería: probar `pypdf` o `pdfminer.six` (PyMuPDF es AGPL); tabla de factores de unidades por analito solo con las que salgan en esos PDFs; edad desde la fecha de nacimiento y sexo si viene. Lo único que de verdad decide Rubén: reglas o IA.
- Para el parser: el texto de un valor imposible (`OddValue.text`) solo admite un número ("4,5", "950"); si el PDF trae "9,8 H" o "<5", hay que limpiarlo antes o la lectura falla con un error del servidor.
- Para el parser: en los 6 PDFs de Rubén vienen de 2 a 5 de los 8 Extras, uno es un escaneo sin texto, y `pdfplumber` no se dejó instalar (archivo bloqueado, quizá el antivirus).
- Mirar el histograma de la diferencia entre edad biológica y real del notebook de edad biológica.
- Al desplegar: `ROOT` se calcula desde la ruta de `paths.py`, así que `models/` solo se encuentra si el hosting ejecuta desde el repo (instalación editable), no desde un paquete construido.
- Tras las pruebas con amigos: mirar en los logs cuántos `too_few` llevan 6 o 9 valores que faltan (un bloque entero); si son muchos, pasar a una regla por bloques.
- Al elegir hosting: su proxy guarda las IPs aunque la app no lo haga; mirarlo y ajustar la letra pequeña ("no se guarda nada") si hace falta.
- Sesgo en los de 18-29: con los bloques juntos, el modelo les quita de 5 a 7 años (mueren más de lo que predice; solo 81 muertes, quizá accidentes y sobredosis que la analítica no ve). Estudiarlo después de la entrega; corregirlo ahora sería ajustar al ruido.
