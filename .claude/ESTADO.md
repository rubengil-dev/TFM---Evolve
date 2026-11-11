# Qué hay en este archivo y cómo usarlo
- **Contiene:** en qué punto estamos respecto a las fases del proyecto, por dónde empezar la próxima sesión y lo pendiente para más adelante.
- **No contiene:** cifras, nombres de archivos, detalles de lo hecho ni decisiones ya cerradas.
- **Se actualiza:** al cerrar cada sesión.

## Próxima sesión
1. Revisión completa del proyecto: la última fue antes de todo el código del modelo.
2. Empezar la fase de app pensando en la Entrega 04 (solución UX): cerrar las decisiones abiertas de App y Resultado, empezando por el stack y el flujo de pantallas.

## Fases
- [x] Datos
- [x] Preparación
- [x] Modelo
- [ ] App: lectura del PDF, pantalla de revisión, cuestionario, resultado y front.
- [ ] Despliegue

## Entregas
- [x] Entrega 01: ideas de producto.
- [x] Entrega 02: datos y preparación.
- [x] Entrega 03: diseñar, desarrollar y evaluar una primera solución de Machine Learning.
- [ ] Entrega 04: solución UX [29 noviembre 2026].
- [ ] Entrega final: 13 diciembre de 2026.

## Pendiente para más adelante

### Tareas
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
- Separar las dependencias de la app de las del análisis.

### Mejoras futuras
- Triglicéridos sin ayuno: usarlos corrigiéndolos, además de los de ayunas.