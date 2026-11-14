# Metadatos

## Qué contiene
Qué debe hacer el proyecto en el MVP, desde mi punto de vista y sin entrar en cómo se construye: funciones, reglas, experiencia de uso y restricciones que no son técnicas. Las decisiones de producto llevan cómo se decidieron.

Lo que no encaje en esta descripción no va aquí. Lo que queda fuera del MVP va a `FUTURO.md`.

## Actualización
Casi inmutable: se escribe en la entrevista inicial y solo cambia si yo lo pido porque añada o cambie algo de lo que debe hacer.

Lo que quiero que haga el proyecto se escribe tal cual: un requisito por línea, sin justificarlo. Solo las decisiones indican entre paréntesis cómo se decidieron, con `Descartado` en la misma línea solo si aporta (ver `PROTOCOLOS.md`). Lo que se afina más adelante no se desarrolla: se deja como "se afina en la fase X".

Se carga siempre, así que si crece demasiado (unas 300 líneas), avísame para dividirlo.


# Contenido

## Qué debe hacer

### Acceso
- Web pública y gratuita: se entra con un enlace, sin instalar nada.
- Interfaz en español.

### Flujo
- Subir PDF → revisar y corregir los datos extraídos (y responder el cuestionario, si se elige ese modo) → ver resultado.
- La app lee los valores del PDF y normaliza los nombres de los parámetros (glucosa / gluc / GLU…) y las unidades antes de la pantalla de revisión.

### Modos
- Dos modos, a elección del usuario: solo con la analítica, o con la analítica más un cuestionario de hábitos de vida.
- El cuestionario pregunta por tabaco, actividad física, horas sentado y horas de sueño.
- Preguntas sin inputs escritos y solo de datos objetivos: nada de autovaloraciones ("¿cómo de sana es tu dieta?", "¿cómo es tu salud?").
- **El alcohol no se pregunta, y la app explica por qué falta:** el modelo no lo usa (en los datos, beber sale protector por causalidad inversa) y el usuario espera verlo en un cuestionario de hábitos.

### Datos de entrada
- Usa lo que trae una analítica de rutina española, lo que se pide a menudo (p. ej. vitamina D) y lo que el usuario sabe sin pensar (edad, sexo, peso, talla), siempre que exista en NHANES.
- Edad y sexo se extraen del PDF si vienen; si no, se piden.
- Tensión arterial: dato opcional para afinar, nunca obligatorio.
- Solo adultos, dentro del rango de edad de los datos de entrenamiento (18 a 79 años).
- Las analíticas no traen siempre los mismos parámetros: si falta algún dato, se calcula igualmente con menos fiabilidad; si faltan demasiados, se avisa de que no se puede calcular.
- **Valor fuera del rango posible:** en la pantalla de revisión se pide al usuario que lo compruebe (puede ser una mala lectura del PDF); si lo confirma, la app no calcula la edad biológica y avisa de ir al médico cuanto antes. Son valores de emergencia o de una muestra defectuosa: dar una edad ahí sería engañoso.

### Resultado
Siempre:
- Edad biológica estimada ± X años y la diferencia con la edad cronológica. X depende de la precisión de cada caso: más ancho si faltan datos o en jóvenes de riesgo bajo.
- Los mejores y los peores parámetros del usuario, en tablas y explicados en lenguaje llano: cuántos años suma o resta cada uno frente a una persona media de su edad y sexo.
- Aviso de que no es consejo médico ni diagnóstico. No se dan recomendaciones (suplementos, tratamientos…), solo observaciones de los datos.
- Aviso asimétrico: salir por encima es señal para consultar, pero salir bien no significa estar sano.

Cuando se hace el cuestionario:
- Cuántos años suman o restan sus hábitos.

Cuando la edad biológica está por encima de un umbral (haya o no cuestionario):
- Recomendación de revisar la analítica con su médico.

## Experiencia de uso
- La UX tiene prioridad sobre afinar el modelo: el modelo es fácil de iterar, y una UX mal planteada obliga a rehacerla.
- Usable por cualquier persona: flujo corto, lenguaje claro sin jerga, responsive y pensado para móvil.
- Estados de carga y errores de parseo comprensibles y accionables: qué ha fallado y qué puede hacer el usuario.
- Diseño visual: se afina en la fase de app.

## Restricciones
- **Privacidad:** son datos de salud (categoría especial en el RGPD).
  - Minimizar el tratamiento y no almacenar nada: la app procesa todo en memoria y lo descarta.
  - No se usan etnia ni datos socioeconómicos.
  - Informar al usuario de forma clara de qué se hace con sus datos.
- **Formato de entrada:** PDF digital.
- **Plazos:** Entrega 04 (solución UX), el 29 de noviembre de 2026. Entrega final, el 13 de diciembre de 2026.
