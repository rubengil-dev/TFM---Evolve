# Qué hay en este archivo y cómo usarlo
- **Contiene:** en qué punto estamos respecto a las fases del proyecto, por dónde empezar la próxima sesión y lo pendiente para más adelante.
- **No contiene:** cifras, nombres de archivos, detalles de lo hecho ni decisiones ya cerradas.
- **Se actualiza:** al cerrar cada sesión.

## Próxima sesión
Seguir con la fase de modelo, por pasos pequeños y con lo que se analice en notebooks. Ya están hechos los bloques de variables, el split, el preprocesado, los cuatro modelos, la evaluación y el nivel 1. En este orden:
1. Programar y ejecutar el nivel 2 (Base + Extras) con los cuatro contendientes, y compararlo con Cox simple de Base.
2. Repetir con el nivel 3 (Base + Cuestionario) y con el 4 (los dos juntos), si es pertinente.
3. Rellenar `s4_biological_age.py` y medir cuánto mueve la edad biológica el salto del RDW.
4. Medir PhenoAge contra el mejor modelo de cada nivel.
5. Rellenar `s5_build_model.py`, que une todos los pasos.

## Fases
- [x] Datos
- [x] Preparación
- [ ] Modelo
- [ ] App: lectura del PDF, pantalla de revisión, cuestionario, resultado y front.
- [ ] Despliegue

## Entregas
- [x] Entrega 01: ideas de producto.
- [x] Entrega 02: datos y preparación.
- [ ] Entrega 03: diseñar, desarrollar y evaluar una primera solución de Machine Learning [15 noviembre 2026].
- [ ] Entrega 04: solución UX [29 noviembre 2026].
- [ ] Entrega final: 13 diciembre de 2026.

## Pendiente para más adelante

### Tareas
- Conseguir analíticas de ejemplo de distintos laboratorios españoles para probar el parser (tengo PDFs propios).
- Decidir cómo anonimizar los PDFs de `private/` antes de que Claude los lea; la app puede leerlos sin anonimizar en local.

### Decisiones abiertas
Modelo:
- Causalidad inversa: los muertos en los 2 primeros años, ya muy enfermos al hacerse la analítica, pueden inflar el C-index. Se dejan dentro (como PhenoAge) y se hace una prueba de sensibilidad quitándolos; si cae mucho, va a limitaciones.
- Pesos muestrales de NHANES: la primera prueba va sin ellos; revisar si se usan después, también al traducir el riesgo a edad.
- Métrica del error asimétrico: cómo penalizar más infraestimar la edad que sobreestimarla, y cómo medir las colas de error (casos que se desvían mucho).
- Mínimo viable de variables: con qué datos faltantes se deja de calcular.

Resultado:
- Cómo calcular y mostrar el margen ± X años.
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