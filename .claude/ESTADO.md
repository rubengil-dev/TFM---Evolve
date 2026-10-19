# Qué hay en este archivo y cómo usarlo
- **Contiene:** en qué punto estamos respecto a las fases del proyecto, por dónde empezar la próxima sesión y lo pendiente para más adelante.
- **No contiene:** cifras, nombres de archivos, detalles de lo hecho ni decisiones ya cerradas.
- **Se actualiza:** al cerrar cada sesión.

## Próxima sesión
Empezar la fase de modelo, en este orden:
1. Estrategia para analíticas incompletas: imputación, un modelo por subconjunto de variables o modelos que toleren ausentes. Ojo: en NHANES los huecos van por ciclo y en la app por usuario.
2. Arquitectura: Cox como baseline; después, si compensa, árboles de supervivencia o deep learning.
3. Variables: cuál entra de cada pareja muy correlacionada y qué juego de cada combinación lineal.

## Fases
- [x] Datos
- [x] Preparación
- [ ] Modelo
- [ ] App: lectura del PDF, pantalla de revisión, cuestionario, resultado y front.
- [ ] Despliegue

## Entregas
- [x] Entrega 01: ideas de producto.
- [x] Entrega 02: datos y preparación.
- [ ] Entrega 03: por definir.
- [ ] Entrega 04: por definir.
- [ ] Entrega final: diciembre de 2026, día por confirmar.

## Pendiente para más adelante

### Tareas
- Conseguir analíticas de ejemplo de distintos laboratorios españoles para probar el parser (tengo PDFs propios).

### Decisiones abiertas
Modelo:
- Mínimo viable de variables: con qué datos faltantes se deja de calcular.
- Modo con cuestionario: un modelo aparte con hábitos o uno solo que tolere su ausencia, según el C-index.

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

### Pendiente de probar yo
Nada.
