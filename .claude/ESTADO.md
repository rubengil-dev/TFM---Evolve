# Qué hay en este archivo y cómo usarlo
- **Contiene:** en qué punto estamos respecto a las fases del proyecto, por dónde empezar la próxima sesión y lo pendiente para más adelante.
- **No contiene:** cifras, nombres de archivos, detalles de lo hecho ni decisiones ya cerradas.
- **Se actualiza:** al cerrar cada sesión.

## Próxima sesión
1. Empezar la fase de app pensando en la Entrega 04 (solución UX): cerrar las decisiones abiertas de App y Resultado, empezando por el stack y el flujo de pantallas. El punto 2.1 del plan va dentro.

## Fases
- [x] Datos
- [x] Preparación
- [x] Modelo
- [ ] App: lectura del PDF, pantalla de revisión, cuestionario, resultado y front.
- [ ] Despliegue
- [ ] MLOps (requisito nuevo del máster): tests, historial, versionado de datos y de modelos. Hechos los tests básicos, la CI y la trazabilidad de los modelos; faltan los puntos 2.2 a 2.4 del plan.

## Entregas
- [x] Entrega 01: ideas de producto.
- [x] Entrega 02: datos y preparación.
- [x] Entrega 03: diseñar, desarrollar y evaluar una primera solución de Machine Learning.
- [ ] Entrega 04: solución UX [29 noviembre 2026].
- [ ] Entrega final: 13 diciembre de 2026.

## Plan de mejoras
Sale de la revisión completa del 12 de noviembre de 2026. Cada punto dice qué, por qué y cómo. Dentro de cada bloque, el orden es el de ejecución. Del bloque 2, el 2.1 va con la app y el resto después de la Entrega 04, salvo que el profesor pida MLOps antes.

### Bloque 1: quick wins (fácil y aporta)
- [x] Hecho del 1.1 al 1.5. Lo que queda: al elegir el stack, añadir sus librerías a los requisitos de la app y completar el README.

### Bloque 2: hard wins (difícil y aporta mucho)
- [ ] **2.1 Validar lo que entra al modelo.**
  - Por qué: una columna ausente, una categoría mal escrita o un número como texto dan un error técnico, y un valor imposible devuelve una edad sin avisar.
  - Cómo: una validación en el módulo de predicción (columnas, tipos, categorías, rangos posibles y edad), con errores con código que el front traduce. Depende de cerrar el mínimo viable de variables.
- [ ] **2.2 Batería completa de tests.**
  - Por qué: las reglas de la CDC y de los cuestionarios son el código más delicado y nada avisa si se rompen.
  - Cómo: una Gold inventada pequeña como base; tests de Silver clean (empezando por los cortes de las correcciones y de los cuestionarios), validación de Gold, preprocesado y edad biológica.
- [ ] **2.3 DVC para datos y pipeline.**
  - Por qué: es el versionado de datos que piden; liga cada modelo a sus datos y detecta cambios en los ficheros de la CDC.
  - Cómo: una etapa por paso del pipeline, llamando al código actual; los modelos siguen en git y DVC solo anota su huella; la descarga no se borra al repetir. Antes, elegir el almacén remoto.
- [ ] **2.4 MLflow y notebooks al día.**
  - Por qué: los resultados solo viven en las salidas de los notebooks, y los de los niveles 1 a 4 quedaron desfasados al quitar el RDW.
  - Cómo: una función de registro llamada desde los notebooks y desde el paso del modelo, sin tocar la evaluación. Reejecutar los notebooks nivel a nivel y revisando juntos, porque las cifras pueden moverse respecto a las ya escritas.

### Bloque 3: quick fixes (aporta poco, pero hay que hacerlo)
- [ ] **3.1 Unificar los dos remuestreos y los dos bucles de validación cruzada de la evaluación.** Por qué: mismo código dos veces. Cómo: una función común para cada pareja.
- [ ] **3.2 Llevar al código las funciones copiadas entre notebooks de trabajo.** Por qué: están repetidas en hasta cinco notebooks. Cómo: moverlas e importarlas.
- [ ] **3.3 Una sola lista de categorías.** Por qué: la validación y el preprocesado guardan el mismo dato por separado. Cómo: que la validación importe la del estudio.
- [ ] **3.4 Imputador: pasarle la columna de forma explícita.** Por qué: hoy depende de un detalle interno de pandas. Cómo: junto al test de preprocesado del 2.2.
- [ ] **3.5 Limpiar lo que no se usa.** Por qué: quedan variables en la lista de logaritmos que ningún modelo usa y columnas de Silver que nadie lee. Cómo: borrarlas y comprobar que Gold no cambia.
- [ ] **3.6 Etiquetas en git.** Por qué: no se localizan las entregas ni las versiones del modelo. Cómo: una por entrega y una por modelo, la primera tras el 1.3.
- [ ] **3.7 Poner al día el contexto.** Por qué: el requisito de MLOps no está en el contexto del proyecto. Cómo: con mi OK.

## Pendiente para más adelante

### Tareas
- Preguntar al profesor qué hay que demostrar de MLOps (registro de modelos, CI, monitorización), antes del 2.3 y el 2.4.
- Conseguir analíticas de ejemplo de distintos laboratorios españoles para probar el parser (tengo PDFs propios).
- Decidir cómo anonimizar los PDFs de `private/` antes de que Claude los lea; la app puede leerlos sin anonimizar en local.
- Mirar el histograma de la diferencia entre edad biológica y real del notebook de edad biológica.

### Decisiones abiertas
Modelo:
- Mínimo viable de variables: con qué datos faltantes se deja de calcular.

Resultado:
- Cómo calcular y mostrar el margen ± X años. En test, la edad biológica es menos precisa con riesgo bajo (jóvenes): el margen tiene que ser más ancho ahí.
- Cómo mostrar las edades biológicas fuera de 18-79 y la cola de personas muy por encima de su edad.
- Definición de "mejor/peor parámetro". Propuesta para el MVP: cuánto empuja cada parámetro la edad frente a una persona media de la misma edad y sexo, agrupando las variables ligadas (serie roja, transaminasas) para que los signos se entiendan.
- Cuántos parámetros mejores/peores se muestran.
- Umbral de años por encima para remitir al médico.

App:
- Cómo elige el usuario el modo. Idea: dos pestañas, "solo analítica" por defecto y "analítica + cuestionario".
- Diseño visual.
- Diseño del parser y de la normalización de nombres y unidades.
- Stack de front y backend.

Despliegue:
- Hosting.

MLOps:
- Almacén remoto de DVC: DagsHub o una carpeta local.
- Versión del modelo: registro de MLflow, o etiqueta de git con las huellas de datos y modelo.
- Monitorización: si se hace, qué se puede contar sin almacenar datos de salud.

### Mejoras futuras
- Triglicéridos sin ayuno: usarlos corrigiéndolos, además de los de ayunas.