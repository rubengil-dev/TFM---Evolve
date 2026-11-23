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
- Subir PDF → peso y talla (y edad y sexo si el PDF no los trae), en los dos modos → (hábitos, si se elige ese modo) → ver resultado.
- La pantalla de revisión solo aparece si el parser marca algún valor como dudoso (sin reconocer, sin unidad, fuera del rango posible o edad y sexo ausentes), y solo con esos valores: revisarlo todo mete la fricción que la app quiere quitar. Se valida con los PDFs reales de Rubén; si fallan, se replantea. (Rubén, de acuerdo) Descartado: revisión siempre.
- La app lee los valores del PDF y normaliza los nombres de los parámetros (glucosa / gluc / GLU…) y las unidades antes de la pantalla de revisión.

### Modos
- Dos modos, a elección del usuario: solo con la analítica, o con la analítica más un cuestionario de hábitos de vida.
- El modo se elige con dos botones en la portada, y el de analítica + cuestionario es el destacado porque da la mejor respuesta. Al pulsar cualquiera se abre el selector de archivos. (Rubén, de acuerdo) Descartado: dos pestañas.
- El cuestionario va una pregunta por pantalla, al estilo Typeform: las opciones en tarjetas con icono y aclaración, que pasan solas a la siguiente pregunta; los números en una barra deslizable para el valor grueso con − y + en los extremos para el ajuste fino, y una barra de progreso fina arriba. Peso y talla siguen el mismo estilo. Los rangos de las barras son los rangos posibles del modelo. (Rubén, de acuerdo) Descartado: hélice como barra de progreso; fichas que se deslizan, demasiados toques para peso y talla.
- El cuestionario pregunta por tabaco, actividad física, horas sentado y horas de sueño.
- Preguntas sin inputs escritos y solo de datos objetivos: nada de autovaloraciones ("¿cómo de sana es tu dieta?", "¿cómo es tu salud?").
- **El alcohol no se pregunta, y la app explica por qué falta, en la pregunta del tabaco:** el modelo no lo usa (en los datos, beber sale protector por causalidad inversa) y el usuario espera verlo en un cuestionario de hábitos.

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
- Portada: título, los dos botones y, en una franja inferior muy visible, el aviso de que no es consejo médico.
- La franja está en la portada y en el resultado, no en el cuestionario ni en la carga: si está siempre, pasa a ser parte del fondo y deja de leerse. (Rubén, de acuerdo)
- Estética "microscopio": oscuro, verde profundo con acentos esmeralda, titulares en Fraunces y el aviso en amarillo de peligro con el símbolo de riesgo biológico. (Rubén, de acuerdo) Descartado: neón con red de partículas, no evoca biología; mezclar la hélice de ADN con las células en el fondo, recargado.
- Fondo animado en todas las pantallas: células flotando como bajo la lente. Manda la fluidez sobre la estética: si no va fluido, imagen fija.
- Al tocar el fondo salen destellos y nacen o explotan células; al pulsar botones, no.
- Pantalla de carga cosmética antes del resultado, de 1,5 a 2 segundos: una hélice de ADN verde que se construye de arriba abajo, "Calculando tu edad" y un porcentaje que sube rápido de 0 a 100. (Rubén, de acuerdo) Descartado: frases que cambian y lista de pasos; hélice bicolor, cansa la vista.
- En la portada, "solo analítica" va a la izquierda y "analítica + hábitos", destacado, a la derecha.
- Resto del diseño visual (cuestionario, carga, errores y resultado): se afina en la fase de app.

## Restricciones
- **Privacidad:** son datos de salud (categoría especial en el RGPD).
  - Minimizar el tratamiento y no almacenar nada: la app procesa todo en memoria y lo descarta.
  - No se usan etnia ni datos socioeconómicos.
  - Informar al usuario de forma clara de qué se hace con sus datos.
- **Formato de entrada:** PDF digital.
- **Plazos:** Entrega 04 (solución UX), el 29 de noviembre de 2026. Entrega final, el 9 de diciembre de 2026 (fecha del enunciado de la Entrega 04; ante la duda, la más corta).
