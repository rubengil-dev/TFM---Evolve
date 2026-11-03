# Qué hay en este archivo y cómo usarlo
- **Contiene:** en qué punto estamos respecto a las fases del proyecto, por dónde empezar la próxima sesión y lo pendiente para más adelante.
- **No contiene:** cifras, nombres de archivos, detalles de lo hecho ni decisiones ya cerradas.
- **Se actualiza:** al cerrar cada sesión.

## Próxima sesión
Empezar la fase de modelo, en este orden:
1. Fijar qué variables forman cada bloque (Base, Extras y Cuestionario), cuál entra de cada pareja muy correlacionada y qué juego de cada combinación lineal.
2. Montar `src/models/` y `src/train.py` y hacer de principio a fin el nivel 0 (baseline) y el nivel 1 (Base) con los cuatro contendientes.
3. Repetir con los niveles 2 y 3, cada uno en su notebook de trabajo.

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

### Decisiones abiertas
Modelo:
- Causalidad inversa: los muertos en los 2 primeros años, ya muy enfermos al hacerse la analítica, pueden inflar el C-index. Se dejan dentro (como PhenoAge) y se hace una prueba de sensibilidad quitándolos; si cae mucho, va a limitaciones.
- Pesos muestrales de NHANES: si se usan al entrenar y al evaluar.
- Métrica del error asimétrico: cómo penalizar más infraestimar la edad que sobreestimarla, y cómo medir las colas de error (casos que se desvían mucho).
- Mínimo viable de variables: con qué datos faltantes se deja de calcular.
- Criterio de mejora real entre niveles (propuesta: intervalo de confianza por bootstrap de la diferencia de C-index que no incluya el 0).

Resultado:
- Cómo calcular y mostrar el margen ± X años.
- Definición de "mejor/peor parámetro". Propuesta para el MVP: cuánto empuja cada parámetro la edad frente a una persona media de la misma edad y sexo.
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